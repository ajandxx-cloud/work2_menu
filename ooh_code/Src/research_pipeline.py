import csv
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import yaml

from Src.parser import Parser
from run_menu_compare import (
    aggregate_episode_metrics,
    build_eval_solver,
    evaluate_policy,
    normalize_checkpoint_path,
    paired_summary,
    restore_stdout,
    save_json,
)
from Src.config import Config
from Src.work2_runtime import Solver


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS_DIR = ROOT / "experiments"
STUDIES_DIR = EXPERIMENTS_DIR / "studies"
SUITES_DIR = EXPERIMENTS_DIR / "suites"
OUTPUTS_DIR = ROOT / "outputs"
ARTIFACTS_DIR = ROOT / "artifacts"
MANUSCRIPT_DIR = ROOT / "manuscript"

SUMMARY_NUMERIC_KEYS = [
    "episodes",
    "served_customers",
    "travel_time",
    "travel_cost",
    "service_cost",
    "failure_cost",
    "discount_cost",
    "charge_revenue",
    "total_cost",
    "net_profit",
    "home_pickup_count",
    "average_menu_size",
    "avg_meeting_point_count_per_menu",
    "home_pickup_only_share",
    "home_pickup_only_with_feasible_meeting_point_share",
    "home_pickup_share",
    "avg_walk_distance",
    "avg_pickup_time_deviation",
    "avg_in_vehicle_time",
    "avg_chosen_predicted_cost",
    "avg_chosen_price",
    "avg_menu_build_time",
    "avg_step_time",
    "opt_out_rate",
    "acceptance_rate",
    "non_home_acceptance_rate",
    "consumer_surplus",
    "price_at_floor_fraction",
    "price_at_ceil_fraction",
    "mean_net_profit_gap_vs_reference",
    "mean_total_cost_gap_vs_reference",
    "net_profit_win_rate_vs_reference",
    "net_profit_gap_ci95_half_width_vs_reference",
    "mean_net_profit_gap_vs_baseline",
    "mean_total_cost_gap_vs_baseline",
    "net_profit_win_rate_vs_baseline",
    "net_profit_gap_ci95_half_width_vs_baseline",
    "avg_fn_pruning_rate",
    "avg_fn_pruned_near",
    "avg_fn_pruned_mid",
    "avg_fn_pruned_far",
    "avg_eta_mae",
    "avg_ivt_mae",
    "avg_displayed_eta_mae",
    "avg_displayed_ivt_mae",
    "avg_displayed_eta_bias",
    "avg_displayed_ivt_bias",
    "displayed_eta_p50",
    "displayed_eta_p90",
    "displayed_eta_p95",
    "displayed_ivt_p50",
    "displayed_ivt_p90",
    "displayed_ivt_p95",
    "exact_gap_logged_share",
    "avg_exact_menu_value",
    "avg_greedy_menu_value",
    "avg_relative_optimality_gap",
    "avg_menu_overlap_rate",
    "avg_exact_build_time",
    "avg_greedy_build_time",
    "avg_exact_gap_candidate_count",
]

CSV_FIELD_ORDER = [
    "study_name",
    "study_type",
    "study_role",
    "suite_name",
    "suite_run_id",
    "run_id",
    "timestamp_utc",
    "manifest_hash",
    "code_version_marker",
    "split_id",
    "train_split",
    "test_split",
    "seed",
    "trace_seed",
    "variant_tag",
    "variant_label",
    "policy",
    "menu_k",
    "ablation_tag",
    "is_reference",
    "reference_tag",
    "reference_policy",
    "paired_reference_policy",
    "paired_baseline_policy",
    "checkpoint_path",
    "checkpoint_reused",
    "checkpoint_source",
    "is_behavior_non_degenerate",
] + SUMMARY_NUMERIC_KEYS

STUDY_ONLY_ARG_KEYS = {
    "eval_episodes",
    "trace_seed",
    "shared_checkpoint_path",
    "skip_train",
    "menu_k_values",
}


def utc_now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_id_from_hash(short_hash):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{timestamp}_{short_hash[:8]}"


def slugify(value):
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", str(value).strip())
    return text.strip("_") or "item"


def infer_study_role(manifest):
    explicit_role = manifest.get("study_role")
    if explicit_role:
        return str(explicit_role)

    study_name = str(manifest.get("name", ""))
    if study_name in {"austin_main", "seattle_main"}:
        return "impact"
    if study_name in {"filtering_baselines", "rc_main_optout", "rc_main"}:
        return "mechanism"
    return "support"


def behavior_gate(manifest):
    gate = dict(manifest.get("behavior_gate", {}))
    return {
        "min_acceptance_rate": float(gate.get("min_acceptance_rate", 0.05)),
        "max_acceptance_rate": float(gate.get("max_acceptance_rate", 0.30)),
        "max_opt_out_rate": float(gate.get("max_opt_out_rate", 0.90)),
    }


def acceptance_rate_from_row(row):
    acceptance_rate = row.get("acceptance_rate")
    if acceptance_rate is not None:
        return float(acceptance_rate)
    opt_out_rate = row.get("opt_out_rate")
    if opt_out_rate is not None:
        return float(1.0 - float(opt_out_rate))
    return None


def behavior_non_degenerate(acceptance_rate, opt_out_rate, gate):
    if acceptance_rate is None or opt_out_rate is None:
        return None
    return bool(
        gate["min_acceptance_rate"] <= float(acceptance_rate) <= gate["max_acceptance_rate"]
        and float(opt_out_rate) < gate["max_opt_out_rate"]
    )


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def write_yaml(path, payload):
    os.makedirs(Path(path).parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=True)


def write_csv(path, rows):
    os.makedirs(Path(path).parent, exist_ok=True)
    fieldnames = list(CSV_FIELD_ORDER)
    discovered = set(fieldnames)
    for row in rows:
        for key in row.keys():
            if key not in discovered:
                fieldnames.append(key)
                discovered.add(key)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_text(path, text):
    os.makedirs(Path(path).parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def manifest_hash(path):
    return hashlib.sha1(Path(path).read_bytes()).hexdigest()


def detect_code_version_marker():
    git_dir = ROOT / ".git"
    if git_dir.exists():
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
            marker = result.stdout.strip()
            if marker:
                return marker
        except Exception:
            pass

    digest = hashlib.sha1()
    include_paths = [
        ROOT / "run_menu_compare.py",
        ROOT / "requirements.txt",
    ]
    for base in [ROOT / "Src", ROOT / "Environments" / "OOH"]:
        if base.exists():
            include_paths.extend(sorted(base.rglob("*.py")))
    for path in include_paths:
        path = Path(path)
        if not path.exists() or not path.is_file():
            continue
        digest.update(str(path.relative_to(ROOT)).encode("utf-8"))
        digest.update(path.read_bytes())
    return f"nogit-{digest.hexdigest()[:12]}"


def resolve_manifest(name):
    direct = Path(name)
    if direct.exists():
        return direct

    candidates = []
    for base in [STUDIES_DIR, SUITES_DIR]:
        for suffix in ["", ".yaml", ".yml"]:
            candidate = base / f"{name}{suffix}"
            candidates.append(candidate)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Could not resolve study or suite manifest '{name}'.")


def load_manifest(name):
    path = resolve_manifest(name)
    manifest = read_yaml(path)
    if not isinstance(manifest, dict):
        raise ValueError(f"Manifest '{path}' must contain a mapping at the top level.")
    if "name" not in manifest:
        manifest["name"] = path.stem
    manifest["_manifest_path"] = str(path)
    manifest["_manifest_hash"] = manifest_hash(path)
    manifest["_kind"] = "suite" if Path(path).parent == SUITES_DIR else "study"
    return manifest


def parser_namespace_with_overrides(overrides):
    parser_builder = Parser()
    namespace = parser_builder.get_parser().parse_args(args=[])

    normalized = dict(overrides)
    if "menu_k_values" in normalized and isinstance(normalized["menu_k_values"], (list, tuple)):
        normalized["menu_k_values"] = ",".join(str(value) for value in normalized["menu_k_values"])

    extra_fields = {}
    for key, value in normalized.items():
        if not hasattr(namespace, key):
            if key in STUDY_ONLY_ARG_KEYS:
                extra_fields[key] = value
                continue
            raise ValueError(f"Unknown parser argument override '{key}'.")
        setattr(namespace, key, value)
    namespace = parser_builder.finalize_args(namespace)
    for key, value in extra_fields.items():
        setattr(namespace, key, value)
    return namespace


def split_slug(split):
    if "id" in split:
        return slugify(split["id"])
    return f"train{split['train_split']}_test{split['test_split']}"


def build_study_args(manifest, split, eval_overrides=None):
    manifest_hash_short = manifest["_manifest_hash"][:8]
    base_args = dict(manifest.get("base_args", {}))
    base_args.update(split.get("args_overrides", {}))
    base_args["data_seed"] = split["train_split"]
    base_args["data_seed_test"] = split["test_split"]
    base_args.setdefault("seed", 1234)
    base_args.setdefault("experiment_name", manifest["name"])
    base_args["run_suffix"] = f"{split_slug(split)}_{manifest_hash_short}"
    base_args.setdefault("log_output", "file")
    base_args.setdefault("save_model", True)
    base_args.setdefault("debug", True)
    base_args.setdefault("menu_policy", manifest.get("reference_policy", "offer_all_feasible_bundles"))

    if eval_overrides:
        base_args.update(eval_overrides)

    return parser_namespace_with_overrides(base_args)


def training_checkpoint_path_from_args(args):
    restore_stdout()
    config = Config(args)
    checkpoint_path = normalize_checkpoint_path(config.paths["checkpoint"])
    restore_stdout()
    return checkpoint_path


def train_or_reuse_shared_model(args, reuse_existing=True):
    restore_stdout()
    train_config = Config(args)
    checkpoint_path = normalize_checkpoint_path(train_config.paths["checkpoint"])
    checkpoint_file = os.path.join(checkpoint_path, "supervised_ml.pt")
    reused_checkpoint = bool(reuse_existing and os.path.exists(checkpoint_file))

    if not reused_checkpoint:
        solver = Solver(config=train_config)
        solver.train()

    restore_stdout()
    if not os.path.exists(checkpoint_file):
        raise FileNotFoundError(f"Expected shared checkpoint at '{checkpoint_file}'.")

    return {
        "checkpoint_path": checkpoint_path,
        "checkpoint_file": checkpoint_file,
        "checkpoint_source": "existing_checkpoint" if reused_checkpoint else "fresh_training",
        "checkpoint_reused": reused_checkpoint,
        "training_args": public_args_dict(args),
    }


def build_variant_solver(args, checkpoint_path):
    restore_stdout()
    config, solver = build_eval_solver(args, checkpoint_path)
    restore_stdout()
    return config, solver


def generate_request_traces(args, checkpoint_path, eval_episodes, trace_seed):
    config, solver = build_variant_solver(args, checkpoint_path)
    traces = config.test_env.generate_request_traces(eval_episodes, seed=trace_seed)
    del solver
    restore_stdout()
    return traces


def public_args_dict(args):
    hidden = {
        "timestamp",
        "load_checkpoint_path",
        "experiment",
        "folder_suffix",
        "algo_name",
        "env_name",
        "k",
        "parcelpoint_capacity",
        "fraction_capacitated",
        "home_util",
        "home_failure",
        "failure_cost",
        "max_price",
        "min_price",
        "menu_mode",
        "pricing",
    }
    payload = {}
    for key, value in vars(args).items():
        if key.startswith("_") or key in hidden:
            continue
        payload[key] = value
    return payload


def variant_specs_for_manifest(manifest):
    study_type = manifest["type"]
    if study_type == "policy_compare":
        specs = []
        seen = set()
        for item in manifest.get("policies", []):
            if isinstance(item, str):
                spec = {"tag": item, "label": item.replace("_", " "), "policy": item}
            else:
                spec = {
                    "tag": item["tag"],
                    "label": item.get("label", item["tag"].replace("_", " ")),
                    "policy": item.get("policy", item["tag"]),
                    "menu_k": item.get("menu_k"),
                    "args_overrides": item.get("args_overrides", {}),
                }
            if spec["tag"] in seen:
                continue
            specs.append(spec)
            seen.add(spec["tag"])
        return specs

    if study_type == "menu_k_robustness":
        policy = manifest.get("policy", "menu_optimization")
        specs = []
        for menu_k in manifest.get("menu_k_values", []):
            specs.append(
                {
                    "tag": f"{policy}_k{menu_k}",
                    "label": f"{policy} (k={menu_k})",
                    "policy": policy,
                    "menu_k": int(menu_k),
                    "args_overrides": {"menu_k": int(menu_k)},
                }
            )
        return specs

    if study_type == "ablation":
        baseline = manifest.get("baseline_variant", {})
        baseline_spec = {
            "tag": baseline.get("tag", "menu_optimization"),
            "label": baseline.get("label", "menu optimization"),
            "policy": baseline.get("policy", "menu_optimization"),
            "menu_k": baseline.get("menu_k"),
            "args_overrides": baseline.get("args_overrides", {}),
            "ablation_tag": "baseline",
        }
        specs = [baseline_spec]
        for item in manifest.get("ablations", []):
            specs.append(
                {
                    "tag": item["tag"],
                    "label": item.get("label", item["tag"].replace("_", " ")),
                    "policy": item.get("policy", baseline_spec["policy"]),
                    "menu_k": item.get("menu_k", baseline_spec.get("menu_k")),
                    "args_overrides": item.get("args_overrides", {}),
                    "ablation_tag": item["tag"],
                }
            )
        return specs

    raise ValueError(f"Unsupported study type '{study_type}'.")


def reference_variant_for_manifest(manifest):
    return {
        "tag": manifest.get("reference_tag", "full_display"),
        "label": manifest.get("reference_label", "full display"),
        "policy": manifest.get("reference_policy", "offer_all_feasible_bundles"),
        "menu_k": manifest.get("reference_menu_k"),
        "args_overrides": manifest.get("reference_args_overrides", {}),
    }


def baseline_variant_tag(manifest):
    if manifest["type"] != "ablation":
        return None
    baseline = manifest.get("baseline_variant", {})
    return baseline.get("tag", "menu_optimization")


def maybe_mean(values):
    filtered = [float(value) for value in values if value is not None]
    if not filtered:
        return None
    return float(np.mean(filtered))


def aggregate_rows(rows, group_keys):
    grouped = {}
    for row in rows:
        key = tuple(row.get(group_key) for group_key in group_keys)
        grouped.setdefault(key, []).append(row)

    summaries = []
    for key, items in grouped.items():
        base = {group_key: items[0].get(group_key) for group_key in group_keys}
        for carry_key in [
            "study_name",
            "study_type",
            "study_role",
            "suite_name",
            "suite_run_id",
            "run_id",
            "manifest_hash",
            "code_version_marker",
            "variant_label",
            "policy",
            "menu_k",
            "ablation_tag",
            "is_reference",
            "reference_tag",
            "reference_policy",
            "paired_reference_policy",
            "paired_baseline_policy",
        ]:
            base[carry_key] = items[0].get(carry_key)
        base["split_count"] = len(items)
        base["split_ids"] = ",".join(str(item.get("split_id")) for item in items)
        behavior_flags = [item.get("is_behavior_non_degenerate") for item in items if item.get("is_behavior_non_degenerate") is not None]
        base["is_behavior_non_degenerate"] = None if not behavior_flags else bool(all(behavior_flags))
        for numeric_key in SUMMARY_NUMERIC_KEYS:
            base[numeric_key] = maybe_mean([item.get(numeric_key) for item in items])
        summaries.append(base)
    return summaries


def output_root_for_study(study_name, run_id):
    root = OUTPUTS_DIR / "studies" / study_name / run_id
    root.mkdir(parents=True, exist_ok=True)
    return root


def latest_run_dir(study_name):
    base = OUTPUTS_DIR / "studies" / study_name
    if not base.exists():
        return None
    candidates = [item for item in base.iterdir() if item.is_dir()]
    if not candidates:
        return None
    return sorted(candidates)[-1]


def load_study_summary(study_name, run_id=None):
    if run_id is None:
        run_dir = latest_run_dir(study_name)
    else:
        run_dir = OUTPUTS_DIR / "studies" / study_name / run_id
    if run_dir is None:
        return None, None
    summary_path = run_dir / "study_summary.json"
    suite_path = run_dir / "suite_summary.json"
    if summary_path.exists():
        with open(summary_path, "r", encoding="utf-8") as handle:
            return json.load(handle), run_dir
    if suite_path.exists():
        with open(suite_path, "r", encoding="utf-8") as handle:
            return json.load(handle), run_dir
    return None, run_dir


def latest_resumable_run_id(name, kind="study", manifest_hash=None):
    base = OUTPUTS_DIR / "studies" / name
    if not base.exists():
        return None

    summary_filename = "suite_summary.json" if kind == "suite" else "study_summary.json"
    candidates = sorted([item for item in base.iterdir() if item.is_dir()], reverse=True)
    for candidate in candidates:
        snapshot_path = candidate / "manifest_snapshot.yaml"
        if manifest_hash is not None and snapshot_path.exists():
            try:
                snapshot = read_yaml(snapshot_path)
                candidate_hash = snapshot.get("_manifest_hash") or snapshot.get("manifest_hash")
                if candidate_hash and candidate_hash != manifest_hash:
                    continue
            except Exception:
                continue
        summary_path = candidate / summary_filename
        if not summary_path.exists():
            return candidate.name
        try:
            with open(summary_path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except Exception:
            return candidate.name
        status = payload.get("run_metadata", {}).get("status", "")
        if status != "completed":
            return candidate.name
    return None


def infer_split_state_from_disk(study_root):
    split_summaries = []
    normalized_rows = []
    splits_root = Path(study_root) / "splits"
    if not splits_root.exists():
        return split_summaries, normalized_rows

    for split_dir in sorted([item for item in splits_root.iterdir() if item.is_dir()]):
        summary_path = split_dir / "split_summary.json"
        if not summary_path.exists():
            continue
        with open(summary_path, "r", encoding="utf-8") as handle:
            split_summary = json.load(handle)
        split_summaries.append(split_summary)
        normalized_rows.extend(split_summary.get("rows", []))
    return split_summaries, normalized_rows


def suite_member_summaries(suite_manifest, suite_summary=None):
    summaries = []
    if suite_summary is not None:
        for member in suite_summary.get("member_runs", []):
            summary, run_dir = load_study_summary(member["study_name"], run_id=member["run_id"])
            if summary is not None:
                summaries.append((member["study_name"], summary, run_dir))
        if summaries:
            return summaries

    for member_name in suite_manifest.get("members", []):
        summary, run_dir = load_study_summary(member_name)
        if summary is not None:
            summaries.append((member_name, summary, run_dir))
    return summaries


def execute_study_manifest(manifest, reuse_existing=True, suite_name="", suite_run_id="", resume_run_id=""):
    if manifest.get("_kind") == "suite":
        return execute_suite_manifest(manifest, reuse_existing=reuse_existing, resume_run_id=resume_run_id)

    study_name = manifest["name"]
    if resume_run_id:
        run_id = resume_run_id
        study_root = OUTPUTS_DIR / "studies" / study_name / run_id
        study_root.mkdir(parents=True, exist_ok=True)
    else:
        run_id = run_id_from_hash(manifest["_manifest_hash"])
        study_root = output_root_for_study(study_name, run_id)

    existing_summary_path = study_root / "study_summary.json"
    existing_summary = None
    if existing_summary_path.exists():
        with open(existing_summary_path, "r", encoding="utf-8") as handle:
            existing_summary = json.load(handle)

    timestamp_utc = (
        existing_summary.get("run_metadata", {}).get("timestamp_utc", utc_now_iso())
        if existing_summary is not None
        else utc_now_iso()
    )
    code_version = (
        existing_summary.get("run_metadata", {}).get("code_version_marker", detect_code_version_marker())
        if existing_summary is not None
        else detect_code_version_marker()
    )
    write_yaml(study_root / "manifest_snapshot.yaml", manifest)
    study_role = infer_study_role(manifest)
    study_behavior_gate = behavior_gate(manifest)

    reference_variant = reference_variant_for_manifest(manifest)
    variants = [reference_variant] + variant_specs_for_manifest(manifest)
    deduped_variants = []
    seen_tags = set()
    for variant in variants:
        if variant["tag"] in seen_tags:
            continue
        deduped_variants.append(variant)
        seen_tags.add(variant["tag"])
    variants = deduped_variants

    if existing_summary is not None:
        all_rows = list(existing_summary.get("normalized_rows", []))
        split_summaries = list(existing_summary.get("splits", []))
    else:
        split_summaries, all_rows = infer_split_state_from_disk(study_root)
    completed_split_ids = {split_summary.get("split_id") for split_summary in split_summaries}

    def persist_study_summary(status):
        aggregate_variant_summary = aggregate_rows(
            all_rows,
            group_keys=["study_name", "variant_tag", "policy", "menu_k", "ablation_tag"],
        )
        aggregate_variant_summary.sort(key=lambda item: str(item["variant_tag"]))
        save_json(study_root / "normalized_rows.json", all_rows)
        write_csv(study_root / "normalized_rows.csv", all_rows)
        save_json(study_root / "aggregate_variant_summary.json", aggregate_variant_summary)
        write_csv(study_root / "aggregate_variant_summary.csv", aggregate_variant_summary)

        summary_payload = {
            "schema_version": 1,
            "study": {
                "name": study_name,
                "title": manifest.get("title", study_name),
                "type": manifest["type"],
                "study_role": study_role,
                "description": manifest.get("description", ""),
                "manifest_path": manifest["_manifest_path"],
                "manifest_hash": manifest["_manifest_hash"],
                "suite_name": suite_name,
                "suite_run_id": suite_run_id,
                "headline_variants": list(manifest.get("headline_variants", [])),
                "behavior_gate": study_behavior_gate,
            },
            "run_metadata": {
                "run_id": run_id,
                "timestamp_utc": timestamp_utc,
                "code_version_marker": code_version,
                "study_root": str(study_root),
                "status": status,
                "completed_splits": len(split_summaries),
                "expected_splits": len(manifest.get("splits", [])),
            },
            "splits": split_summaries,
            "normalized_rows": all_rows,
            "aggregate_variant_summary": aggregate_variant_summary,
        }
        save_json(study_root / "study_summary.json", summary_payload)
        return summary_payload

    for split in manifest.get("splits", []):
        split_id = split_slug(split)
        if split_id in completed_split_ids:
            continue
        split_root = study_root / "splits" / split_id
        split_root.mkdir(parents=True, exist_ok=True)

        base_args = build_study_args(manifest, split)
        train_args = parser_namespace_with_overrides(
            {
                **public_args_dict(base_args),
                "menu_policy": "offer_all_feasible_bundles",
                "eval_only": False,
                "freeze_learning": False,
                "load_checkpoint_path": "",
                "save_model": True,
                "log_output": "file",
            }
        )
        training_metadata = train_or_reuse_shared_model(train_args, reuse_existing=reuse_existing)
        trace_seed = split.get("trace_seed", manifest.get("trace_seed", base_args.seed))
        request_traces = generate_request_traces(
            base_args,
            training_metadata["checkpoint_path"],
            eval_episodes=base_args.eval_episodes,
            trace_seed=trace_seed,
        )
        np.save(split_root / "request_traces.npy", np.array(request_traces, dtype=object))

        variant_results = {}
        for variant in variants:
            eval_overrides = dict(variant.get("args_overrides", {}))
            if variant.get("menu_k") is not None:
                eval_overrides["menu_k"] = int(variant["menu_k"])
            variant_args = build_study_args(manifest, split, eval_overrides=eval_overrides)
            resolved_menu_k = variant.get("menu_k")
            if resolved_menu_k is None:
                resolved_menu_k = variant_args.menu_k
            _, solver = build_variant_solver(variant_args, training_metadata["checkpoint_path"])
            _, episodes = evaluate_policy(
                solver=solver,
                request_traces=request_traces,
                menu_policy=variant["policy"],
                menu_k=resolved_menu_k,
            )
            restore_stdout()
            summary = aggregate_episode_metrics(episodes)
            variant_results[variant["tag"]] = {
                "variant": variant,
                "episodes": episodes,
                "summary": summary,
            }
            save_json(split_root / f"{variant['tag']}_episode_metrics.json", episodes)
            save_json(split_root / f"{variant['tag']}_summary.json", summary)

        reference_result = variant_results[reference_variant["tag"]]
        baseline_tag = baseline_variant_tag(manifest)
        baseline_result = variant_results.get(baseline_tag) if baseline_tag else None

        split_rows = []
        for tag, result in variant_results.items():
            paired_vs_reference = None
            if tag != reference_variant["tag"]:
                paired_vs_reference = paired_summary(reference_result["episodes"], result["episodes"])
                save_json(split_root / f"{tag}_paired_vs_{reference_variant['tag']}.json", paired_vs_reference)

            paired_vs_baseline = None
            if baseline_result is not None and tag not in {reference_variant["tag"], baseline_tag}:
                paired_vs_baseline = paired_summary(baseline_result["episodes"], result["episodes"])
                save_json(split_root / f"{tag}_paired_vs_{baseline_tag}.json", paired_vs_baseline)

            row = {
                "study_name": study_name,
                "study_type": manifest["type"],
                "study_role": study_role,
                "suite_name": suite_name,
                "suite_run_id": suite_run_id,
                "run_id": run_id,
                "timestamp_utc": timestamp_utc,
                "manifest_hash": manifest["_manifest_hash"],
                "code_version_marker": code_version,
                "split_id": split_id,
                "train_split": split["train_split"],
                "test_split": split["test_split"],
                "seed": int(base_args.seed),
                "trace_seed": int(trace_seed),
                "variant_tag": tag,
                "variant_label": result["variant"].get("label", tag),
                "policy": result["variant"]["policy"],
                "menu_k": int(result["variant"].get("menu_k") or base_args.menu_k),
                "ablation_tag": result["variant"].get("ablation_tag", ""),
                "is_reference": bool(tag == reference_variant["tag"]),
                "reference_tag": reference_variant["tag"],
                "reference_policy": reference_variant["policy"],
                "paired_reference_policy": reference_variant["policy"],
                "paired_baseline_policy": baseline_result["variant"]["policy"] if baseline_result else "",
                "checkpoint_path": training_metadata["checkpoint_path"],
                "checkpoint_reused": training_metadata["checkpoint_reused"],
                "checkpoint_source": training_metadata["checkpoint_source"],
            }
            row.update(result["summary"])
            row["acceptance_rate"] = acceptance_rate_from_row(row)
            row["is_behavior_non_degenerate"] = behavior_non_degenerate(
                row.get("acceptance_rate"),
                row.get("opt_out_rate"),
                study_behavior_gate,
            )
            row["mean_net_profit_gap_vs_reference"] = (
                None if paired_vs_reference is None else paired_vs_reference["mean_net_profit_gap"]
            )
            row["mean_total_cost_gap_vs_reference"] = (
                None if paired_vs_reference is None else paired_vs_reference["mean_total_cost_gap"]
            )
            row["net_profit_win_rate_vs_reference"] = (
                None if paired_vs_reference is None else paired_vs_reference["net_profit_win_rate"]
            )
            row["net_profit_gap_ci95_half_width_vs_reference"] = (
                None if paired_vs_reference is None else paired_vs_reference["net_profit_gap_ci95_half_width"]
            )
            row["mean_net_profit_gap_vs_baseline"] = (
                None if paired_vs_baseline is None else paired_vs_baseline["mean_net_profit_gap"]
            )
            row["mean_total_cost_gap_vs_baseline"] = (
                None if paired_vs_baseline is None else paired_vs_baseline["mean_total_cost_gap"]
            )
            row["net_profit_win_rate_vs_baseline"] = (
                None if paired_vs_baseline is None else paired_vs_baseline["net_profit_win_rate"]
            )
            row["net_profit_gap_ci95_half_width_vs_baseline"] = (
                None if paired_vs_baseline is None else paired_vs_baseline["net_profit_gap_ci95_half_width"]
            )
            split_rows.append(row)
            all_rows.append(row)

        split_summary = {
            "split_id": split_id,
            "train_split": split["train_split"],
            "test_split": split["test_split"],
            "trace_seed": trace_seed,
            "training_metadata": training_metadata,
            "reference_variant_tag": reference_variant["tag"],
            "baseline_variant_tag": baseline_tag,
            "rows": split_rows,
        }
        split_summaries.append(split_summary)
        completed_split_ids.add(split_id)
        save_json(split_root / "split_summary.json", split_summary)
        persist_study_summary(status="in_progress")

    summary_payload = persist_study_summary(status="completed")
    return summary_payload


def execute_suite_manifest(manifest, reuse_existing=True, resume_run_id=""):
    suite_name = manifest["name"]
    if resume_run_id:
        run_id = resume_run_id
        suite_root = OUTPUTS_DIR / "studies" / suite_name / run_id
        suite_root.mkdir(parents=True, exist_ok=True)
    else:
        run_id = run_id_from_hash(manifest["_manifest_hash"])
        suite_root = output_root_for_study(suite_name, run_id)

    existing_suite_summary_path = suite_root / "suite_summary.json"
    existing_suite_summary = None
    if existing_suite_summary_path.exists():
        with open(existing_suite_summary_path, "r", encoding="utf-8") as handle:
            existing_suite_summary = json.load(handle)

    timestamp_utc = (
        existing_suite_summary.get("run_metadata", {}).get("timestamp_utc", utc_now_iso())
        if existing_suite_summary is not None
        else utc_now_iso()
    )
    code_version = (
        existing_suite_summary.get("run_metadata", {}).get("code_version_marker", detect_code_version_marker())
        if existing_suite_summary is not None
        else detect_code_version_marker()
    )
    write_yaml(suite_root / "manifest_snapshot.yaml", manifest)

    member_runs = list(existing_suite_summary.get("member_runs", [])) if existing_suite_summary is not None else []

    def persist_suite_summary(status):
        suite_summary = {
            "schema_version": 1,
            "suite": {
                "name": suite_name,
                "title": manifest.get("title", suite_name),
                "manifest_path": manifest["_manifest_path"],
                "manifest_hash": manifest["_manifest_hash"],
                "members": manifest.get("members", []),
            },
            "run_metadata": {
                "run_id": run_id,
                "timestamp_utc": timestamp_utc,
                "code_version_marker": code_version,
                "suite_root": str(suite_root),
                "status": status,
                "completed_members": len(member_runs),
                "expected_members": len(manifest.get("members", [])),
            },
            "member_runs": member_runs,
        }
        save_json(suite_root / "suite_summary.json", suite_summary)
        return suite_summary

    for member_name in manifest.get("members", []):
        member_manifest = load_manifest(member_name)
        existing_member = next((item for item in member_runs if item.get("study_name") == member_name), None)
        member_resume_run_id = ""
        if existing_member is not None:
            existing_member_summary, _ = load_study_summary(member_name, run_id=existing_member["run_id"])
            if existing_member_summary is not None and existing_member_summary.get("run_metadata", {}).get("status") == "completed":
                persist_suite_summary(status="in_progress")
                continue
            member_resume_run_id = existing_member["run_id"]
        else:
            candidate_resume = latest_resumable_run_id(
                member_name,
                kind="study",
                manifest_hash=member_manifest.get("_manifest_hash"),
            )
            if candidate_resume:
                candidate_summary, _ = load_study_summary(member_name, run_id=candidate_resume)
                if (
                    candidate_summary is None
                    or candidate_summary.get("study", {}).get("suite_run_id", "") in {"", run_id}
                ):
                    member_resume_run_id = candidate_resume

        member_summary = execute_study_manifest(
            member_manifest,
            reuse_existing=reuse_existing,
            suite_name=suite_name,
            suite_run_id=run_id,
            resume_run_id=member_resume_run_id,
        )
        member_entry = {
            "study_name": member_summary["study"]["name"],
            "run_id": member_summary["run_metadata"]["run_id"],
            "summary_path": os.path.join(
                member_summary["run_metadata"]["study_root"],
                "study_summary.json",
            ),
        }
        if existing_member is not None:
            member_runs = [member_entry if item.get("study_name") == member_name else item for item in member_runs]
        else:
            member_runs.append(member_entry)
        persist_suite_summary(status="in_progress")

    suite_summary = persist_suite_summary(status="completed")
    return suite_summary
