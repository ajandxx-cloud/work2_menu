"""Paired replay contracts and normalized-row helpers for Work2 studies."""

import hashlib
import json
from copy import deepcopy

from Src.policy_adapters import adapter_metadata


STUDY_EXECUTION_STATUSES = {
    "completed",
    "contract_only",
    "diagnostic",
    "incomplete",
    "blocked",
    "failed",
}

NORMALIZED_ROW_FIELDS = [
    "schema_version",
    "study_id",
    "study_name",
    "manifest_path",
    "run_id",
    "tier",
    "run_mode",
    "policy_tag",
    "candidate_id",
    "method",
    "product_mode",
    "time_window_mode",
    "menu_mode",
    "pricing_mode",
    "method_variant",
    "attention_enabled",
    "attention_mode",
    "attention_strength",
    "attention_weight_summary",
    "attention_pair_id",
    "attention_pair_complete",
    "split_id",
    "seed",
    "data_seed",
    "data_seed_test",
    "trace_id",
    "trace_hash",
    "manifest_hash",
    "settings_hash",
    "checkpoint_load_status",
    "checkpoint_path",
    "checkpoint_hash",
    "checkpoint_required",
    "checkpoint_intentional_mismatch",
    "pricing",
    "hgs_reopt_time",
    "hgs_final_time",
    "menu_k",
    "max_candidates",
    "filter_mode",
    "effective_policy",
    "menu_selection_solver_effective",
    "solver_fallback_reason",
    "exact_enumerated_menu_count",
    "relative_optimality_gap",
    "menu_overlap_rate",
    "menu_build_time",
    "menu_utilization",
    "choice_entropy",
    "accepted_count",
    "served_count",
    "served_rate",
    "acceptance_rate",
    "optout_rate",
    "home_share",
    "meeting_point_uptake_rate",
    "count_opted_out",
    "count_accepted_home",
    "count_accepted_meeting_point",
    "charge_revenue",
    "discount_cost",
    "net_price_revenue",
    "net_profit",
    "operational_cost",
    "total_cost",
    "net_objective_proxy",
    "service_time_total",
    "uptake_regime",
    "diagnostic",
    "comparison_role",
    "cost_bound",
    "placeholder_only",
    "status",
    "execution_status",
    "error_type",
    "error_message",
    "git_commit",
    "git_dirty",
    "git_status_summary",
]

OPTIONAL_ROW_FIELDS = {
    "checkpoint_hash",
    "menu_selection_solver_effective",
    "solver_fallback_reason",
    "exact_enumerated_menu_count",
    "relative_optimality_gap",
    "menu_overlap_rate",
    "menu_build_time",
    "menu_utilization",
    "choice_entropy",
    "accepted_count",
    "served_count",
    "served_rate",
    "acceptance_rate",
    "optout_rate",
    "home_share",
    "meeting_point_uptake_rate",
    "count_opted_out",
    "count_accepted_home",
    "count_accepted_meeting_point",
    "charge_revenue",
    "discount_cost",
    "net_price_revenue",
    "net_profit",
    "operational_cost",
    "total_cost",
    "service_time_total",
    "error_type",
    "error_message",
    "git_status_summary",
}


def stable_json_hash(value, prefix, length=16):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return prefix + "-" + digest[:length]


def trace_identity(study_name, split_id, args):
    trace_fields = {
        "study_name": study_name,
        "split_id": split_id,
        "seed": args.get("seed"),
        "data_seed": args.get("data_seed"),
        "data_seed_test": args.get("data_seed_test"),
        "instance": args.get("instance"),
        "max_episodes": args.get("max_episodes"),
        "max_steps_r": args.get("max_steps_r"),
        "max_steps_p": args.get("max_steps_p"),
        "uptake_regime": args.get("uptake_regime"),
    }
    trace_id = stable_json_hash(trace_fields, "trace", length=14)
    trace_hash = stable_json_hash(trace_fields, "tracehash", length=32)
    return trace_id, trace_hash


def settings_hash(args):
    return stable_json_hash(args, "settings", length=16)


def attention_pair_identity(setting):
    args = setting["args"]
    pair_fields = {
        "study_name": setting["study_name"],
        "split_id": setting["split_id"],
        "trace_id": setting["trace_id"],
        "seed": args.get("seed"),
        "data_seed": args.get("data_seed"),
        "data_seed_test": args.get("data_seed_test"),
        "pricing": args.get("pricing"),
        "checkpoint_path": args.get("checkpoint_path"),
        "menu_policy": args.get("menu_policy"),
        "menu_eta_filter_mode": args.get("menu_eta_filter_mode"),
        "menu_objective_mode": args.get("menu_objective_mode"),
        "menu_k": args.get("menu_k"),
        "max_candidates": args.get("max_candidates"),
        "hgs_reopt_time": args.get("hgs_reopt_time"),
        "hgs_final_time": args.get("hgs_final_time"),
    }
    return stable_json_hash(pair_fields, "attnpair", length=16)


def resolve_paired_settings(manifest, manifest_hash_value=None):
    from Src.experiment_contracts import manifest_hash, resolve_policy_args

    manifest_hash_value = manifest_hash_value or manifest_hash(manifest)
    settings = []
    for split in manifest.get("splits", []):
        split_id = split["split_id"]
        for policy in manifest.get("policies", []):
            args = resolve_policy_args(manifest, split, policy)
            args["uptake_regime"] = split.get("uptake_regime", args.get("uptake_regime", "unspecified"))
            trace_id, trace_hash = trace_identity(manifest["name"], split_id, args)
            metadata = adapter_metadata(policy["tag"])
            metadata.update(policy.get("metadata", {}))
            setting = {
                "study_name": manifest["name"],
                "manifest_path": manifest.get("_path", ""),
                "tier": manifest["tier"],
                "run_mode": manifest["run_mode"],
                "split_id": split_id,
                "policy_tag": policy["tag"],
                "args": args,
                "policy_metadata": metadata,
                "trace_id": trace_id,
                "trace_hash": trace_hash,
                "manifest_hash": manifest_hash_value,
                "settings_hash": settings_hash({
                    "study": manifest["name"],
                    "split_id": split_id,
                    "policy_tag": policy["tag"],
                    "args": args,
                }),
            }
            settings.append(setting)
    validate_paired_settings(settings, manifest.get("paired_fields", []), manifest.get("varied_fields", []))
    return settings


def validate_paired_settings(settings, paired_fields, varied_fields=None):
    varied = set(varied_fields or [])
    groups = {}
    for setting in settings:
        groups.setdefault(setting["split_id"], []).append(setting)

    for split_id, split_settings in groups.items():
        if not split_settings:
            continue
        baseline = split_settings[0]
        for setting in split_settings[1:]:
            for field in paired_fields:
                if field in varied:
                    continue
                base_value = baseline["args"].get(field)
                variant_value = setting["args"].get(field)
                if base_value != variant_value:
                    raise ValueError(
                        "paired replay drift in split "
                        + str(split_id)
                        + " policy "
                        + str(setting["policy_tag"])
                        + " field "
                        + str(field)
                        + ": baseline="
                        + repr(base_value)
                        + " variant="
                        + repr(variant_value)
                    )
    return True


def checkpoint_row_metadata(args, override=None):
    metadata = {
        "checkpoint_load_status": "not_requested",
        "checkpoint_path": args.get("checkpoint_path", ""),
        "checkpoint_hash": None,
        "checkpoint_required": bool(args.get("require_checkpoint", False)),
        "checkpoint_intentional_mismatch": bool(args.get("allow_checkpoint_mismatch", False)),
    }
    if metadata["checkpoint_required"]:
        metadata["checkpoint_load_status"] = "contract_required"
    if override:
        metadata.update(override)
    return metadata


def _first_value(*sources):
    for value in sources:
        if value is not None:
            return value
    return None


def canonical_pricing_mode(args, menu_metadata=None, policy_metadata=None):
    menu_metadata = menu_metadata or {}
    policy_metadata = policy_metadata or {}
    pricing_mode = _first_value(
        menu_metadata.get("pricing_mode"),
        args.get("pricing_mode"),
        args.get("menu_pricing_mode"),
        policy_metadata.get("pricing_mode"),
        "no_pricing",
    )
    if pricing_mode == "constant":
        return "flat_markdown"
    if pricing_mode == "zero":
        return "no_pricing"
    return str(pricing_mode)


def contract_modes(args, menu_metadata=None, policy_metadata=None):
    menu_metadata = menu_metadata or {}
    policy_metadata = policy_metadata or {}
    product_mode = str(_first_value(
        menu_metadata.get("product_mode"),
        args.get("product_mode"),
        policy_metadata.get("product_mode"),
        "m+w+p",
    ))
    time_window_mode = str(_first_value(
        menu_metadata.get("time_window_mode"),
        args.get("time_window_mode"),
        policy_metadata.get("time_window_mode"),
        "adaptive_window",
    ))
    menu_mode = str(_first_value(
        menu_metadata.get("menu_mode"),
        args.get("menu_contract_mode"),
        policy_metadata.get("menu_mode"),
        "optimized_menu",
    ))
    pricing_mode = canonical_pricing_mode(args, menu_metadata, policy_metadata)
    if product_mode != "m+w+p":
        pricing_mode = "no_pricing"
    return product_mode, time_window_mode, menu_mode, pricing_mode


def canonical_method(product_mode, time_window_mode, menu_mode, pricing_mode):
    return "__".join([str(product_mode), str(time_window_mode), str(menu_mode), str(pricing_mode)])


def build_normalized_row(
    setting,
    run_id,
    checkpoint_metadata=None,
    stats_metadata=None,
    menu_metadata=None,
    provenance_metadata=None,
    status="contract_only",
    execution_status="contract_only",
    placeholder_only=True,
):
    args = deepcopy(setting["args"])
    stats_metadata = stats_metadata or {}
    menu_metadata = menu_metadata or {}
    provenance_metadata = provenance_metadata or {}
    checkpoint_metadata = checkpoint_metadata or checkpoint_row_metadata(args)
    policy_metadata = setting.get("policy_metadata", {})
    product_mode, time_window_mode, menu_mode, pricing_mode = contract_modes(args, menu_metadata, policy_metadata)
    method = _first_value(
        menu_metadata.get("method"),
        canonical_method(product_mode, time_window_mode, menu_mode, pricing_mode),
    )

    row = {
        "schema_version": "normalized-row-v2",
        "study_id": setting["study_name"],
        "study_name": setting["study_name"],
        "manifest_path": setting.get("manifest_path", ""),
        "run_id": run_id,
        "tier": setting["tier"],
        "run_mode": setting["run_mode"],
        "policy_tag": setting["policy_tag"],
        "candidate_id": _first_value(menu_metadata.get("candidate_id"), stats_metadata.get("candidate_id"), "aggregate"),
        "method": method,
        "product_mode": product_mode,
        "time_window_mode": time_window_mode,
        "menu_mode": menu_mode,
        "pricing_mode": pricing_mode,
        "method_variant": _first_value(
            menu_metadata.get("method_variant"),
            args.get("method_variant"),
            policy_metadata.get("method_variant"),
            "DSPO_original",
        ),
        "attention_enabled": bool(_first_value(
            menu_metadata.get("attention_enabled"),
            args.get("attention_enabled"),
            policy_metadata.get("attention_enabled"),
            False,
        )),
        "attention_mode": _first_value(
            menu_metadata.get("attention_mode"),
            args.get("attention_mode"),
            policy_metadata.get("attention_mode"),
            "deterministic",
        ),
        "attention_strength": float(_first_value(
            menu_metadata.get("attention_strength"),
            args.get("attention_strength"),
            1.0,
        )),
        "attention_weight_summary": _first_value(menu_metadata.get("attention_weight_summary"), {}),
        "attention_pair_id": _first_value(menu_metadata.get("attention_pair_id"), attention_pair_identity(setting)),
        "attention_pair_complete": bool(menu_metadata.get("attention_pair_complete", False)),
        "split_id": setting["split_id"],
        "seed": args.get("seed"),
        "data_seed": args.get("data_seed"),
        "data_seed_test": args.get("data_seed_test"),
        "trace_id": setting["trace_id"],
        "trace_hash": setting["trace_hash"],
        "manifest_hash": setting["manifest_hash"],
        "settings_hash": setting["settings_hash"],
        "checkpoint_load_status": checkpoint_metadata.get("checkpoint_load_status"),
        "checkpoint_path": checkpoint_metadata.get("checkpoint_path", args.get("checkpoint_path", "")),
        "checkpoint_hash": checkpoint_metadata.get("checkpoint_hash"),
        "checkpoint_required": bool(checkpoint_metadata.get("checkpoint_required", args.get("require_checkpoint", False))),
        "checkpoint_intentional_mismatch": bool(checkpoint_metadata.get("checkpoint_intentional_mismatch", False)),
        "pricing": args.get("pricing"),
        "hgs_reopt_time": args.get("hgs_reopt_time"),
        "hgs_final_time": args.get("hgs_final_time"),
        "menu_k": args.get("menu_k"),
        "max_candidates": args.get("max_candidates"),
        "filter_mode": _first_value(menu_metadata.get("eta_filter_mode"), args.get("menu_eta_filter_mode")),
        "effective_policy": _first_value(menu_metadata.get("effective_menu_policy"), args.get("menu_policy")),
        "menu_selection_solver_effective": menu_metadata.get("menu_selection_solver_effective"),
        "solver_fallback_reason": menu_metadata.get("solver_fallback_reason"),
        "exact_enumerated_menu_count": menu_metadata.get("exact_enumerated_menu_count"),
        "relative_optimality_gap": menu_metadata.get("relative_optimality_gap"),
        "menu_overlap_rate": menu_metadata.get("menu_overlap_rate"),
        "menu_build_time": menu_metadata.get("menu_build_time"),
        "menu_utilization": menu_metadata.get("menu_utilization"),
        "choice_entropy": menu_metadata.get("choice_entropy"),
        "accepted_count": stats_metadata.get("accepted_count"),
        "served_count": stats_metadata.get("served_count"),
        "served_rate": stats_metadata.get("served_rate"),
        "acceptance_rate": stats_metadata.get("acceptance_rate"),
        "optout_rate": stats_metadata.get("optout_rate"),
        "home_share": stats_metadata.get("home_share"),
        "meeting_point_uptake_rate": stats_metadata.get("meeting_point_uptake_rate"),
        "count_opted_out": stats_metadata.get("count_opted_out"),
        "count_accepted_home": stats_metadata.get("count_accepted_home"),
        "count_accepted_meeting_point": stats_metadata.get("count_accepted_meeting_point"),
        "charge_revenue": stats_metadata.get("charge_revenue"),
        "discount_cost": stats_metadata.get("discount_cost"),
        "net_price_revenue": stats_metadata.get("net_price_revenue"),
        "net_profit": stats_metadata.get("net_profit"),
        "operational_cost": stats_metadata.get("operational_cost"),
        "total_cost": stats_metadata.get("total_cost"),
        "net_objective_proxy": _first_value(
            stats_metadata.get("net_objective_proxy"),
            menu_metadata.get("net_objective_proxy"),
            stats_metadata.get("net_price_revenue"),
            0.0,
        ),
        "service_time_total": stats_metadata.get("service_time_total"),
        "uptake_regime": args.get("uptake_regime", "unspecified"),
        "diagnostic": bool(policy_metadata.get("diagnostic", False)),
        "comparison_role": policy_metadata.get("comparison_role", "policy"),
        "cost_bound": bool(policy_metadata.get("cost_bound", False)),
        "placeholder_only": bool(placeholder_only),
        "status": status,
        "execution_status": execution_status,
        "error_type": _first_value(menu_metadata.get("error_type"), stats_metadata.get("error_type"), ""),
        "error_message": _first_value(menu_metadata.get("error_message"), stats_metadata.get("error_message"), ""),
        "git_commit": provenance_metadata.get("git_commit", "unknown"),
        "git_dirty": bool(provenance_metadata.get("git_dirty", False)),
        "git_status_summary": provenance_metadata.get("git_status_summary", ""),
    }
    accepted_count = _first_value(
        row.get("accepted_count"),
        (row.get("count_accepted_home") or 0) + (row.get("count_accepted_meeting_point") or 0)
        if row.get("count_accepted_home") is not None and row.get("count_accepted_meeting_point") is not None
        else None,
    )
    row["accepted_count"] = accepted_count
    row["served_count"] = _first_value(row.get("served_count"), accepted_count)
    total_choices = None
    if accepted_count is not None and row.get("count_opted_out") is not None:
        total_choices = float(accepted_count + row.get("count_opted_out"))
    row["served_rate"] = _first_value(
        row.get("served_rate"),
        float(row["served_count"] / total_choices) if total_choices else None,
    )
    operational_cost = _first_value(row.get("operational_cost"), row.get("service_time_total"))
    row["operational_cost"] = operational_cost
    row["total_cost"] = _first_value(
        row.get("total_cost"),
        (operational_cost or 0.0) + (row.get("discount_cost") or 0.0) if operational_cost is not None else None,
    )
    row["net_profit"] = _first_value(
        row.get("net_profit"),
        (row.get("net_price_revenue") or 0.0) - (operational_cost or 0.0)
        if row.get("net_price_revenue") is not None
        else None,
    )
    validate_normalized_row(row)
    return row


def annotate_attention_pair_completeness(rows):
    groups = {}
    for row in rows:
        groups.setdefault(row.get("attention_pair_id"), []).append(row)
    for group in groups.values():
        methods = {row.get("method_variant") for row in group}
        complete = {"DSPO_original", "DSPO_attention"}.issubset(methods)
        for row in group:
            row["attention_pair_complete"] = bool(complete)
    return rows


def validate_normalized_row(row):
    missing = [field for field in NORMALIZED_ROW_FIELDS if field not in row]
    if missing:
        raise ValueError("normalized row missing required fields: " + ", ".join(missing))
    empty = [
        field
        for field in NORMALIZED_ROW_FIELDS
        if field not in OPTIONAL_ROW_FIELDS and row.get(field) is None
    ]
    if empty:
        raise ValueError("normalized row has empty required fields: " + ", ".join(empty))
    if row.get("tier") == "formal" and row.get("placeholder_only"):
        raise ValueError("formal normalized rows cannot be placeholder_only=True")
    if row.get("status") not in STUDY_EXECUTION_STATUSES:
        raise ValueError("normalized row has invalid status: " + repr(row.get("status")))
    if row.get("execution_status") not in STUDY_EXECUTION_STATUSES:
        raise ValueError("normalized row has invalid execution_status: " + repr(row.get("execution_status")))
    if row.get("status") == "completed" and row.get("placeholder_only"):
        raise ValueError("completed normalized rows cannot be placeholder_only=True")
    if row.get("status") == "completed" and row.get("execution_status") != "completed":
        raise ValueError("completed normalized rows require execution_status=completed")
    return True


def validate_rows(rows):
    for row in rows:
        validate_normalized_row(row)
    return True
