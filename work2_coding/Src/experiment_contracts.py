"""Manifest loading and validation helpers for Work2 robust-menu studies."""

import argparse
import hashlib
from copy import deepcopy
from pathlib import Path

import yaml

from Src.parser import Parser
from Src.policy_adapters import (
    attention_policy_tags,
    adapter_metadata,
    adapter_overrides,
    known_policy_tags,
    required_policy_tags,
    validate_policy_only_overrides,
    validate_required_adapter_coverage,
)


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS_DIR = ROOT / "experiments"
if not EXPERIMENTS_DIR.exists():
    EXPERIMENTS_DIR = ROOT / "Experiments"
STUDIES_DIR = EXPERIMENTS_DIR / "studies"
SUITES_DIR = EXPERIMENTS_DIR / "suites"

VALID_TIERS = {"smoke", "pilot", "formal"}
VALID_RUN_MODES = {"smoke", "diagnostic", "pilot", "formal"}
REQUIRED_STUDY_FIELDS = {
    "schema_version",
    "name",
    "tier",
    "run_mode",
    "description",
    "base_args",
    "splits",
    "policies",
    "paired_fields",
    "output_schema",
}
REQUIRED_OUTPUT_FIELDS = {"normalized-row-v1", "fields"}
EXTRA_CONTRACT_ARG_FIELDS = {"uptake_regime"}


def _parser():
    return Parser().get_parser()


def parser_choices():
    choices = {}
    for action in _parser()._actions:
        if action.dest == argparse.SUPPRESS:
            continue
        if action.choices is not None:
            choices[action.dest] = list(action.choices)
    return choices


def parser_defaults():
    return vars(_parser().parse_args([]))


def parser_arg_names():
    return set(parser_defaults().keys())


def _manifest_path(kind, name_or_path):
    candidate = Path(name_or_path)
    if candidate.exists():
        return candidate
    if candidate.suffix != ".yaml":
        candidate = candidate.with_suffix(".yaml")
    base = STUDIES_DIR if kind == "study" else SUITES_DIR
    return base / candidate.name


def load_manifest(name_or_path, kind="study"):
    path = _manifest_path(kind, name_or_path)
    if not path.exists():
        raise FileNotFoundError("manifest not found: " + str(path))
    with path.open("r", encoding="utf-8") as handle:
        manifest = yaml.safe_load(handle) or {}
    manifest["_path"] = str(path)
    if kind == "suite" or manifest.get("type") == "suite":
        validate_suite(manifest)
    else:
        validate_manifest(manifest)
    return manifest


def load_suite(name_or_path):
    return load_manifest(name_or_path, kind="suite")


def manifest_hash(manifest):
    data = deepcopy(manifest)
    data.pop("_path", None)
    payload = yaml.safe_dump(data, sort_keys=True, default_flow_style=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _validate_unknown_args(args, context):
    valid = parser_arg_names() | EXTRA_CONTRACT_ARG_FIELDS
    bad = sorted(key for key in (args or {}) if key not in valid)
    if bad:
        raise ValueError(context + " contains unknown parser key(s): " + ", ".join(bad))


def _validate_choices(args, context):
    choices = parser_choices()
    for key, value in (args or {}).items():
        if key in choices and value not in choices[key]:
            raise ValueError(context + " has invalid " + key + "=" + repr(value))


def _validate_common_args(args, context):
    _validate_unknown_args(args, context)
    _validate_choices(args, context)
    if "menu_k" in args and int(args["menu_k"]) <= 0:
        raise ValueError(context + " has invalid menu_k=" + repr(args["menu_k"]))
    if "max_candidates" in args and int(args["max_candidates"]) <= 0:
        raise ValueError(context + " has invalid max_candidates=" + repr(args["max_candidates"]))
    if "run_mode" in args and args["run_mode"] not in VALID_RUN_MODES:
        raise ValueError(context + " has invalid run_mode=" + repr(args["run_mode"]))


def validate_manifest(manifest):
    missing = sorted(REQUIRED_STUDY_FIELDS - set(manifest.keys()))
    if missing:
        raise ValueError("study manifest missing required field(s): " + ", ".join(missing))
    if manifest["tier"] not in VALID_TIERS:
        raise ValueError("tier has invalid value: " + repr(manifest["tier"]))
    if manifest["run_mode"] not in VALID_RUN_MODES:
        raise ValueError("run_mode has invalid value: " + repr(manifest["run_mode"]))

    output_schema = manifest.get("output_schema") or {}
    if not REQUIRED_OUTPUT_FIELDS.issubset(set(output_schema.keys())):
        raise ValueError("output_schema must include normalized-row-v1 and fields")
    if not output_schema.get("fields"):
        raise ValueError("output_schema.fields cannot be empty")

    base_args = manifest.get("base_args") or {}
    _validate_common_args(base_args, "base_args")

    split_ids = []
    for split in manifest.get("splits", []):
        split_id = split.get("split_id")
        if not split_id:
            raise ValueError("split missing split_id")
        split_ids.append(split_id)
        if "seed" not in split:
            raise ValueError("split " + str(split_id) + " missing seed")
        split_args = split_args_overrides(split)
        _validate_common_args(split_args, "split " + str(split_id))
    if len(split_ids) != len(set(split_ids)):
        raise ValueError("duplicate split IDs in manifest: " + repr(split_ids))

    policy_tags = []
    for policy in manifest.get("policies", []):
        tag = policy.get("tag")
        if not tag:
            raise ValueError("policy missing tag")
        if tag not in known_policy_tags(include_optional=True):
            raise ValueError("invalid policy tag: " + str(tag))
        policy_tags.append(tag)
        policy_args = policy.get("args_overrides") or {}
        _validate_common_args(policy_args, "policy " + str(tag))
        validate_policy_only_overrides(tag, policy_args, set(manifest.get("varied_fields", [])))
        if tag == "no_filter_diagnostic" and not (policy.get("diagnostic") or policy.get("metadata", {}).get("diagnostic")):
            raise ValueError("no_filter_diagnostic policy must be marked diagnostic")
    if len(policy_tags) != len(set(policy_tags)):
        raise ValueError("duplicate policy tags in manifest: " + repr(policy_tags))

    required_tags = manifest.get("required_policy_tags")
    if required_tags is None:
        if manifest.get("comparison_family") == "attention_dspo":
            required_tags = attention_policy_tags()
            required_label = "required policy"
        else:
            required_tags = required_policy_tags()
            required_label = "required baseline policy"
    else:
        required_label = "required policy"
    missing_required = [tag for tag in required_tags if tag not in policy_tags]
    if missing_required:
        raise ValueError("manifest missing " + required_label + " tags: " + ", ".join(missing_required))
    _validate_attention_family(manifest, policy_tags)

    validate_required_adapter_coverage(parser_choices())
    _validate_checkpoint_contract(manifest)
    _validate_uptake_regimes(manifest)
    return True


def validate_suite(suite):
    if suite.get("type") != "suite":
        raise ValueError("suite manifest must set type: suite")
    if not suite.get("name"):
        raise ValueError("suite missing name")
    members = suite.get("members") or []
    if not members:
        raise ValueError("suite missing members")
    seen = set()
    for member in members:
        study = member.get("study") if isinstance(member, dict) else member
        if not study:
            raise ValueError("suite member missing study")
        if study in seen:
            raise ValueError("duplicate suite member: " + str(study))
        seen.add(study)
        path = _manifest_path("study", study)
        if not path.exists():
            raise FileNotFoundError("suite member manifest not found: " + str(path))
    return True


def suite_members(suite):
    return [member.get("study") if isinstance(member, dict) else member for member in suite.get("members", [])]


def split_args_overrides(split):
    args = {}
    for key in ("seed", "data_seed", "data_seed_test"):
        if key in split:
            args[key] = split[key]
    args.update(split.get("args_overrides") or {})
    if split.get("uptake_regime"):
        args["uptake_regime"] = split["uptake_regime"]
    return args


def _merged_args(manifest, split=None, policy=None, include_adapter=True):
    args = parser_defaults()
    args.update(manifest.get("base_args") or {})
    args["run_mode"] = manifest.get("run_mode", args.get("run_mode"))
    if split:
        args.update(split_args_overrides(split))
    if policy and include_adapter:
        args.update(adapter_overrides(policy["tag"]))
    if policy:
        args.update(policy.get("args_overrides") or {})
    return args


def parser_namespace_with_overrides(overrides):
    _validate_common_args(overrides, "overrides")
    args = parser_defaults()
    args.update(overrides or {})
    return argparse.Namespace(**args)


def resolve_policy_args(manifest, split, policy):
    args = _merged_args(manifest, split=split, policy=policy, include_adapter=True)
    _validate_common_args(args, "resolved policy " + str(policy.get("tag")))
    return args


def resolve_policy_namespace(manifest, split, policy):
    return argparse.Namespace(**resolve_policy_args(manifest, split, policy))


def resolved_policy_matrix(manifest):
    matrix = []
    for split in manifest.get("splits", []):
        for policy in manifest.get("policies", []):
            matrix.append(resolve_policy_args(manifest, split, policy))
    return matrix


def _validate_checkpoint_contract(manifest):
    if manifest["tier"] not in {"pilot", "formal"}:
        return
    checkpoint = manifest.get("shared_checkpoint") or {}
    if not checkpoint.get("required"):
        raise ValueError(manifest["tier"] + " manifests require shared_checkpoint.required=true")
    if not checkpoint.get("path"):
        raise ValueError(manifest["tier"] + " manifests require shared_checkpoint.path")
    base_args = manifest.get("base_args") or {}
    if not base_args.get("require_checkpoint"):
        raise ValueError(manifest["tier"] + " manifests require base_args.require_checkpoint=true")
    if not base_args.get("checkpoint_path"):
        raise ValueError(manifest["tier"] + " manifests require base_args.checkpoint_path")


def _validate_attention_family(manifest, policy_tags):
    if manifest.get("comparison_family") != "attention_dspo":
        return
    allowed = set(attention_policy_tags())
    non_main = [tag for tag in policy_tags if tag not in allowed]
    if non_main and not (manifest.get("diagnostic") or manifest.get("separate_suite")):
        raise ValueError("attention_dspo main manifests may only rank DSPO_original and DSPO_attention")
    varied = set(manifest.get("varied_fields", []))
    required_varied = {"method_variant", "attention_enabled", "attention_mode"}
    missing_varied = sorted(required_varied - varied)
    if missing_varied:
        raise ValueError("attention_dspo manifests missing varied attention field(s): " + ", ".join(missing_varied))


def _validate_uptake_regimes(manifest):
    regimes = {split.get("uptake_regime") for split in manifest.get("splits", []) if split.get("uptake_regime")}
    if manifest["tier"] in {"pilot", "formal"} and not {"low", "medium"}.issubset(regimes):
        if not manifest.get("uptake_regime_limitation"):
            raise ValueError("pilot/formal manifests require low and medium uptake regimes")
    if manifest["tier"] == "smoke" and not regimes:
        raise ValueError("smoke manifests require at least one uptake_regime")


def policy_metadata(policy):
    metadata = adapter_metadata(policy["tag"])
    metadata.update(policy.get("metadata", {}))
    if "diagnostic" in policy:
        metadata["diagnostic"] = bool(policy["diagnostic"])
    return metadata
