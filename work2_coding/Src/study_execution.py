"""Execution-status helpers for Work2 robust-menu studies."""

import sys
from argparse import Namespace
from copy import deepcopy
import hashlib
import subprocess
from pathlib import Path

from Src.paired_replay import (
    annotate_attention_pair_completeness,
    build_normalized_row,
    checkpoint_row_metadata,
    resolve_paired_settings,
    validate_rows,
)


BLOCKING_TIERS = {"pilot", "formal"}


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _repo_root():
    return Path(__file__).resolve().parents[2]


def collect_git_provenance(repo_root=None):
    repo_root = Path(repo_root or _repo_root())
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(repo_root),
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--short"],
            cwd=str(repo_root),
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip().splitlines()
    except Exception as exc:  # pragma: no cover - defensive for non-git archives
        return {
            "git_commit": "unknown",
            "git_dirty": True,
            "git_status_summary": "git unavailable: " + str(exc),
        }

    return {
        "git_commit": commit,
        "git_dirty": bool(status),
        "git_status_summary": "; ".join(status[:20]),
    }


def checkpoint_path_for_manifest(manifest):
    checkpoint = manifest.get("shared_checkpoint") or {}
    path = checkpoint.get("path") or (manifest.get("base_args") or {}).get("checkpoint_path", "")
    return path or ""


def resolve_checkpoint_path(manifest, root=None):
    checkpoint_path = checkpoint_path_for_manifest(manifest)
    if not checkpoint_path:
        return Path("")
    path = Path(checkpoint_path)
    if path.is_absolute():
        return path
    return Path(root or Path(__file__).resolve().parents[1]) / path


def inspect_manifest_prerequisites(manifest, root=None, actual_execution=False, contract_only=False):
    blockers = []
    tier = manifest.get("tier", "")
    shared = manifest.get("shared_checkpoint") or {}
    checkpoint_required = bool(shared.get("required") or (manifest.get("base_args") or {}).get("require_checkpoint"))
    expected_status = shared.get("expected_status", "loaded")
    checkpoint_path = checkpoint_path_for_manifest(manifest)
    resolved_path = resolve_checkpoint_path(manifest, root=root)

    if contract_only and tier == "formal":
        blockers.append(
            {
                "code": "formal_placeholder_not_allowed",
                "severity": "blocking",
                "tier": tier,
                "message": "Formal studies cannot emit placeholder contract-only rows.",
            }
        )

    if tier in BLOCKING_TIERS and checkpoint_required:
        if not checkpoint_path:
            blockers.append(
                {
                    "code": "missing_checkpoint_path",
                    "severity": "blocking",
                    "tier": tier,
                    "expected_status": expected_status,
                    "checkpoint_path": "",
                    "message": "Required checkpoint path is missing from manifest.",
                }
            )
        elif not resolved_path.exists():
            blockers.append(
                {
                    "code": "missing_checkpoint_file",
                    "severity": "blocking",
                    "tier": tier,
                    "expected_status": expected_status,
                    "checkpoint_path": checkpoint_path,
                    "resolved_checkpoint_path": str(resolved_path),
                    "message": "Required checkpoint file is unavailable; refusing random-weight evidence.",
                }
            )

    return blockers


def checkpoint_metadata_for_setting(setting, manifest, root=None):
    args = setting["args"]
    metadata = checkpoint_row_metadata(args)
    if not metadata["checkpoint_required"]:
        return metadata

    checkpoint_path = metadata.get("checkpoint_path") or checkpoint_path_for_manifest(manifest)
    resolved_path = Path(checkpoint_path)
    if checkpoint_path and not resolved_path.is_absolute():
        resolved_path = Path(root or Path(__file__).resolve().parents[1]) / checkpoint_path
    metadata["checkpoint_path"] = checkpoint_path
    if resolved_path.exists():
        metadata["checkpoint_load_status"] = "loaded"
        metadata["checkpoint_hash"] = sha256_file(resolved_path)
    else:
        metadata["checkpoint_load_status"] = "failed"
        metadata["checkpoint_hash"] = None
    return metadata


def blocked_rows_for_manifest(manifest, run_id, manifest_hash_value, blockers, max_policies=None, root=None):
    if manifest.get("tier") == "formal":
        return []
    settings = resolve_paired_settings(manifest, manifest_hash_value=manifest_hash_value)
    if max_policies is not None:
        allowed_tags = []
        for setting in settings:
            tag = setting["policy_tag"]
            if tag not in allowed_tags:
                allowed_tags.append(tag)
            if len(allowed_tags) >= max_policies:
                break
        settings = [setting for setting in settings if setting["policy_tag"] in set(allowed_tags)]

    provenance = collect_git_provenance()
    rows = []
    status = "blocked" if any(item.get("severity") == "blocking" for item in blockers) else "incomplete"
    for setting in settings:
        checkpoint = checkpoint_metadata_for_setting(setting, manifest, root=root)
        rows.append(
            build_normalized_row(
                setting,
                run_id=run_id,
                checkpoint_metadata=checkpoint,
                stats_metadata={
                    "acceptance_rate": None,
                    "optout_rate": None,
                    "count_opted_out": None,
                    "count_accepted_home": None,
                    "count_accepted_meeting_point": None,
                },
                menu_metadata={
                    "eta_filter_mode": setting["args"].get("menu_eta_filter_mode"),
                    "effective_menu_policy": setting["args"].get("menu_policy"),
                    "menu_selection_solver_effective": "not_executed",
                    "solver_fallback_reason": blockers[0]["code"] if blockers else "incomplete",
                },
                provenance_metadata=provenance,
                status=status,
                execution_status=status,
                placeholder_only=True,
            )
        )
    annotate_attention_pair_completeness(rows)
    validate_rows(rows)
    return rows


def _mean(values):
    values = [value for value in values if value is not None]
    return sum(values) / len(values) if values else None


def _settings_for_manifest(manifest, manifest_hash_value, max_policies=None):
    settings = resolve_paired_settings(manifest, manifest_hash_value=manifest_hash_value)
    if max_policies is None:
        return settings

    allowed_tags = []
    for setting in settings:
        tag = setting["policy_tag"]
        if tag not in allowed_tags:
            allowed_tags.append(tag)
        if len(allowed_tags) >= max_policies:
            break
    return [setting for setting in settings if setting["policy_tag"] in set(allowed_tags)]


def _completed_checkpoint_metadata(metadata, args):
    return {
        "checkpoint_load_status": metadata.get("checkpoint_load_status", "not_requested"),
        "checkpoint_path": metadata.get("checkpoint_path", args.get("checkpoint_path", "")),
        "checkpoint_hash": metadata.get("checkpoint_hash"),
        "checkpoint_required": bool(metadata.get("checkpoint_required", args.get("require_checkpoint", False))),
        "checkpoint_intentional_mismatch": bool(metadata.get("checkpoint_intentional_mismatch", False)),
    }


def _row_from_actual_replay(setting, run_id):
    from Src.config import Config

    args = deepcopy(setting["args"])
    args.update(
        {
            "eval_only": True,
            "freeze_learning": True,
            "log_output": "file",
            "run_id": run_id,
            "save_model": False,
        }
    )

    original_stdout = sys.stdout
    try:
        config = Config(Namespace(**args))
        model = config.algo(config=config)
        checkpoint_metadata = model.load_checkpoint(
            checkpoint_path=args.get("checkpoint_path", ""),
            require_checkpoint=args.get("require_checkpoint", False),
            allow_checkpoint_mismatch=args.get("allow_checkpoint_mismatch", False),
            run_mode=args.get("run_mode", "smoke"),
        )
    finally:
        sys.stdout = original_stdout

    env = config.test_env
    max_episodes = int(args.get("max_episodes", 1))
    max_steps = max(1, int(args.get("n_vehicles", 1)) * int(args.get("veh_capacity", 1)) - 1)
    totals = {
        "count_opted_out": 0,
        "count_accepted_home": 0,
        "count_accepted_meeting_point": 0,
        "service_time_total": 0.0,
        "charge_revenue": 0.0,
        "discount_cost": 0.0,
    }
    menu_build_times = []
    relative_gaps = []
    overlap_rates = []
    enumerated_counts = []
    last_policy_diagnostic = {}

    for _ in range(max_episodes):
        state = env.reset()
        model.reset()
        done = False
        steps = 0
        episode_totals = {
            "count_opted_out": 0,
            "count_accepted_home": 0,
            "count_accepted_meeting_point": 0,
        }
        last_stats = None
        while not done and steps < max_steps:
            action = model.get_action(state, training=False)
            state, done, stats, _ = env.step(action=action)
            last_stats = stats
            metadata = stats[8] if len(stats) > 8 and isinstance(stats[8], dict) else {}
            steps += 1

            for key in episode_totals:
                episode_totals[key] = int(metadata.get(key, episode_totals[key]))
            last_policy_diagnostic = dict(getattr(model, "last_policy_diagnostic", {}) or {})
            menu_build_times.append(float(getattr(model, "last_menu_build_time", 0.0)))
            if last_policy_diagnostic.get("relative_optimality_gap") is not None:
                relative_gaps.append(float(last_policy_diagnostic["relative_optimality_gap"]))
            if last_policy_diagnostic.get("menu_overlap_rate") is not None:
                overlap_rates.append(float(last_policy_diagnostic["menu_overlap_rate"]))
            if last_policy_diagnostic.get("exact_enumerated_menu_count") is not None:
                enumerated_counts.append(float(last_policy_diagnostic["exact_enumerated_menu_count"]))
        for key in totals:
            if key in episode_totals:
                totals[key] += episode_totals[key]
        if last_stats is not None:
            totals["service_time_total"] += float(last_stats[2])
            totals["charge_revenue"] += float(sum(last_stats[3]))
            totals["discount_cost"] += float(-sum(last_stats[6]))

    total_choices = totals["count_opted_out"] + totals["count_accepted_home"] + totals["count_accepted_meeting_point"]
    accepted = totals["count_accepted_home"] + totals["count_accepted_meeting_point"]
    stats_metadata = {
        **totals,
        "acceptance_rate": float(accepted / total_choices) if total_choices else 0.0,
        "optout_rate": float(totals["count_opted_out"] / total_choices) if total_choices else 0.0,
        "home_share": float(totals["count_accepted_home"] / total_choices) if total_choices else 0.0,
        "meeting_point_uptake_rate": float(totals["count_accepted_meeting_point"] / total_choices) if total_choices else 0.0,
        "net_price_revenue": float(totals["charge_revenue"] - totals["discount_cost"]),
    }
    menu_metadata = {
        "eta_filter_mode": args.get("menu_eta_filter_mode"),
        "effective_menu_policy": last_policy_diagnostic.get("effective_menu_policy", args.get("menu_policy")),
        "menu_selection_solver_effective": last_policy_diagnostic.get("menu_selection_solver_effective", "actual_replay"),
        "solver_fallback_reason": last_policy_diagnostic.get("solver_fallback_reason"),
        "exact_enumerated_menu_count": _mean(enumerated_counts),
        "relative_optimality_gap": _mean(relative_gaps),
        "menu_overlap_rate": _mean(overlap_rates),
        "menu_build_time": _mean(menu_build_times),
        "method_variant": last_policy_diagnostic.get("method_variant", args.get("method_variant", "DSPO_original")),
        "attention_enabled": last_policy_diagnostic.get("attention_enabled", args.get("attention_enabled", False)),
        "attention_mode": last_policy_diagnostic.get("attention_mode", args.get("attention_mode", "deterministic")),
        "attention_strength": last_policy_diagnostic.get("attention_strength", args.get("attention_strength", 1.0)),
        "attention_weight_summary": last_policy_diagnostic.get("attention_weight_summary", {}),
        "net_objective_proxy": stats_metadata["net_price_revenue"] - stats_metadata["service_time_total"],
    }

    return build_normalized_row(
        setting,
        run_id=run_id,
        checkpoint_metadata=_completed_checkpoint_metadata(checkpoint_metadata, args),
        stats_metadata=stats_metadata,
        menu_metadata=menu_metadata,
        provenance_metadata=collect_git_provenance(),
        status="completed",
        execution_status="completed",
        placeholder_only=False,
    )


def actual_rows_for_manifest(manifest, run_id, manifest_hash_value, max_policies=None):
    if manifest.get("tier") == "formal":
        raise ValueError("formal actual replay is not enabled for the conservative public runner")

    rows = []
    for setting in _settings_for_manifest(manifest, manifest_hash_value, max_policies=max_policies):
        rows.append(_row_from_actual_replay(setting, run_id))
    annotate_attention_pair_completeness(rows)
    validate_rows(rows)
    return rows
