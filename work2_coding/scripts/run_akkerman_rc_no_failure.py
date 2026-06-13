import argparse
import csv
import json
import math
import sys
from argparse import Namespace
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Src.config import Config  # noqa: E402
from Src.parser import Parser  # noqa: E402
import Src.Utils.Utils as Utils  # noqa: E402


STRATEGIES = ["NoOOH", "OnlyOOH", "NoPricing", "StaticPricing", "DSPO", "DSPO_Menu"]
RAW_FIELDS = [
    "strategy",
    "seed",
    "home_delivery",
    "travel_costs",
    "service_costs",
    "failure_costs",
    "discount_costs",
    "charge_revenue",
    "avg_discount",
    "avg_charge",
    "total_costs",
    "log_path",
]
SUMMARY_FIELDS = [
    "strategy",
    "n_runs",
    "home_delivery_mean",
    "travel_costs_mean",
    "service_costs_mean",
    "failure_costs_mean",
    "discount_costs_mean",
    "charge_revenue_mean",
    "avg_discount_mean",
    "avg_charge_mean",
    "total_costs_mean",
    "total_costs_ci95",
    "savings_vs_noooh_mean",
]


def parse_seeds(text):
    if text is None or str(text).strip() == "":
        return []
    seeds = []
    for part in str(text).split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = [int(item.strip()) for item in part.split("-", 1)]
            step = 1 if end >= start else -1
            seeds.extend(range(start, end + step, step))
        else:
            seeds.append(int(part))
    return list(dict.fromkeys(seeds))


def parse_optional_float(text):
    if text is None:
        return None
    if isinstance(text, str) and text.strip().lower() in {"none", "null", "na"}:
        return None
    return float(text)


def parser_defaults():
    return vars(Parser().get_parser().parse_args([]))


def strategy_overrides(strategy):
    if strategy == "NoOOH":
        return {
            "algo_name": "Baseline",
            "pricing": True,
            "service_mode": "home_only",
            "price_home": 0.0,
            "price_pp": 0.0,
        }
    if strategy == "OnlyOOH":
        return {
            "algo_name": "Baseline",
            "pricing": True,
            "service_mode": "ooh_only",
            "price_home": 0.0,
            "price_pp": 0.0,
        }
    if strategy == "NoPricing":
        return {
            "algo_name": "Baseline",
            "pricing": True,
            "service_mode": "mixed",
            "price_home": 0.0,
            "price_pp": 0.0,
        }
    if strategy == "StaticPricing":
        return {
            "algo_name": "Baseline",
            "pricing": True,
            "service_mode": "mixed",
            "price_home": 2.0,
            "price_pp": -5.0,
        }
    if strategy == "DSPO":
        return {
            "algo_name": "DSPO",
            "pricing": True,
            "service_mode": "mixed",
        }
    if strategy == "DSPO_Menu":
        return {
            "algo_name": "DSPO_Menu",
            "pricing": True,
            "service_mode": "mixed",
            "menu_mode": True,
            "menu_policy": "menu_optimization",
            "menu_eta_filter_mode": "none",
            "menu_time_filtering": False,
            "method_variant": "DSPO_original",
            "attention_enabled": False,
        }
    raise ValueError("Unknown strategy: " + str(strategy))


def akkerman_base_args(seed, run_id, smoke=False, max_episodes=None, outside_option_util=None):
    args = parser_defaults()
    args.update(
        {
            "seed": int(seed),
            "run_mode": "smoke" if smoke else "formal",
            "log_output": "file",
            "debug": False,
            "save_model": True,
            "experiment": "akkerman_rc_no_failure",
            "folder_suffix": "_" + run_id,
            "instance": "RC",
            "max_steps_r": 90,
            "max_steps_p": 0.5,
            "revenue": 50.0,
            "driver_wage": 30.0,
            "truck_speed": 30.0,
            "max_price": 2.0,
            "min_price": -10.0,
            "home_failure": 0.0,
            "failure_cost": 0.0,
            "outside_option_util": outside_option_util,
            "quit_threshold": None,
            "pricing": True,
            "load_data": True,
            "data_seed": 0,
            "data_seed_test": 1,
            "home_util": 3.95,
            "incentive_sens": -0.175,
            "k": 5,
            "init_theta_cnn": 1.0,
            "initial_phase_epochs": 10,
            "batch_size": 128,
            "n_filters": 8,
            "menu_mode": False,
            "method_variant": "DSPO_original",
            "attention_enabled": False,
            "menu_eta_filter_mode": "none",
            "menu_time_filtering": False,
        }
    )
    args["max_episodes"] = int(max_episodes if max_episodes is not None else (1 if smoke else 10))
    if smoke:
        args["hgs_reopt_time"] = 0.1
        args["hgs_final_time"] = 0.1
    return args


def train_model(config, model):
    max_steps = int(config.n_vehicles * config.veh_capacity) - 1
    for _ in range(int(config.max_episodes)):
        state = config.env.reset()
        model.reset()
        done = False
        step = 0
        last_stats = None
        route_data = None
        while not done and step < max_steps:
            action = model.get_action(state, training=True)
            state, done, last_stats, route_data = config.env.step(action=action)
            step += 1
            model.update(route_data, state, False)
        if route_data is not None and last_stats is not None:
            travel_time = model.update(route_data, state, True)
            Utils.total_costs(last_stats[1], last_stats[2], travel_time, last_stats[3], last_stats[6], config)


def _safe_mean(values):
    values = [float(value) for value in values if value is not None and math.isfinite(float(value))]
    return float(np.mean(values)) if values else 0.0


def evaluate_model(config, model, episodes):
    max_steps = int(config.n_vehicles * config.veh_capacity) - 1
    cost_multiplier = (config.driver_wage + config.fuel_cost * config.truck_speed) / 3600
    totals = {
        "requests": 0,
        "home": 0,
        "travel_costs": 0.0,
        "service_costs": 0.0,
        "failure_costs": 0.0,
        "discount_sum": 0.0,
        "charge_sum": 0.0,
    }
    discount_values = []
    charge_values = []

    for _ in range(int(episodes)):
        state = config.test_env.reset()
        model.reset()
        done = False
        step = 0
        last_stats = None
        route_data = None
        while not done and step < max_steps:
            action = model.get_action(state, training=False)
            state, done, last_stats, route_data = config.test_env.step(action=action)
            step += 1

        if last_stats is None or route_data is None:
            continue
        travel_time = config.test_env.reopt_for_eval(route_data)
        charge_values.extend([float(value) for value in last_stats[3]])
        discount_values.extend([float(value) for value in last_stats[6]])
        totals["requests"] += int(last_stats[0])
        totals["home"] += int(last_stats[1])
        totals["travel_costs"] += float(travel_time) * cost_multiplier
        totals["service_costs"] += float(last_stats[2]) * cost_multiplier
        totals["failure_costs"] += float(last_stats[1]) * float(config.home_failure) * float(config.failure_cost)
        totals["charge_sum"] += float(sum(last_stats[3]))
        totals["discount_sum"] += float(sum(last_stats[6]))

    denom = max(int(episodes), 1)
    total_costs = (
        totals["travel_costs"]
        + totals["service_costs"]
        + totals["failure_costs"]
        - totals["discount_sum"]
        - totals["charge_sum"]
    ) / denom
    return {
        "home_delivery": float(totals["home"] / max(totals["requests"], 1)),
        "travel_costs": float(totals["travel_costs"] / denom),
        "service_costs": float(totals["service_costs"] / denom),
        "failure_costs": float(totals["failure_costs"] / denom),
        "discount_costs": float(-totals["discount_sum"] / denom),
        "charge_revenue": float(totals["charge_sum"] / denom),
        "avg_discount": float(-_safe_mean(discount_values)),
        "avg_charge": float(_safe_mean(charge_values)),
        "total_costs": float(total_costs),
    }


def _close_logger(logger):
    try:
        logger.flush()
    except Exception:
        pass
    try:
        logger.log.close()
    except Exception:
        pass


def run_strategy(strategy, seed, run_id, smoke=False, max_episodes=None, eval_episodes=20, outside_option_util=None):
    runtime_args = akkerman_base_args(
        seed,
        run_id + "_" + strategy,
        smoke=smoke,
        max_episodes=max_episodes,
        outside_option_util=outside_option_util,
    )
    runtime_args.update(strategy_overrides(strategy))
    runtime_args["folder_suffix"] = "_" + run_id + "_" + strategy

    original_stdout = sys.stdout
    logger = None
    config = None
    try:
        config = Config(Namespace(**runtime_args))
        logger = sys.stdout
        model = config.algo(config=config)
        if strategy in {"DSPO", "DSPO_Menu"}:
            train_model(config, model)
        metrics = evaluate_model(config, model, episodes=eval_episodes)
        log_path = str(Path(config.paths["logs"]) / "logfile.log")
    finally:
        sys.stdout = original_stdout
        if logger is not None:
            _close_logger(logger)

    row = {
        "strategy": strategy,
        "seed": int(seed),
        **metrics,
        "log_path": log_path if config is not None else "",
    }
    return row


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_raw_csv(path):
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for field in RAW_FIELDS:
            if field not in {"strategy", "log_path"}:
                row[field] = float(row[field])
        row["seed"] = int(row["seed"])
    return rows


def summarize_rows(rows):
    by_strategy = {}
    for row in rows:
        by_strategy.setdefault(row["strategy"], []).append(row)
    if "NoOOH" not in by_strategy:
        raise ValueError("NoOOH rows are required for savings_vs_noooh_mean")
    noooh_total = _safe_mean([row["total_costs"] for row in by_strategy["NoOOH"]])

    summary = []
    for strategy in STRATEGIES:
        strategy_rows = by_strategy.get(strategy, [])
        if not strategy_rows:
            continue
        totals = np.array([float(row["total_costs"]) for row in strategy_rows], dtype=float)
        ci95 = 0.0
        if len(totals) > 1:
            ci95 = float(1.96 * np.std(totals, ddof=1) / math.sqrt(len(totals)))
        summary.append(
            {
                "strategy": strategy,
                "n_runs": int(len(strategy_rows)),
                "home_delivery_mean": _safe_mean([row["home_delivery"] for row in strategy_rows]),
                "travel_costs_mean": _safe_mean([row["travel_costs"] for row in strategy_rows]),
                "service_costs_mean": _safe_mean([row["service_costs"] for row in strategy_rows]),
                "failure_costs_mean": _safe_mean([row["failure_costs"] for row in strategy_rows]),
                "discount_costs_mean": _safe_mean([row["discount_costs"] for row in strategy_rows]),
                "charge_revenue_mean": _safe_mean([row["charge_revenue"] for row in strategy_rows]),
                "avg_discount_mean": _safe_mean([row["avg_discount"] for row in strategy_rows]),
                "avg_charge_mean": _safe_mean([row["avg_charge"] for row in strategy_rows]),
                "total_costs_mean": float(np.mean(totals)),
                "total_costs_ci95": ci95,
                "savings_vs_noooh_mean": float(noooh_total - np.mean(totals)),
            }
        )
    return summary


def acceptance_gates(rows, summary, outside_option_util=None):
    summary_by_strategy = {row["strategy"]: row for row in summary}
    exact_baseline_gates_enabled = outside_option_util is None
    gates = {
        "failure_costs_zero": all(abs(float(row["failure_costs"])) <= 1e-9 for row in rows),
        "exact_baseline_gates_enabled": exact_baseline_gates_enabled,
        "NoOOH_home_delivery_ge_0_999": (
            True if not exact_baseline_gates_enabled
            else summary_by_strategy.get("NoOOH", {}).get("home_delivery_mean", 0.0) >= 0.999
        ),
        "OnlyOOH_home_delivery_le_0_001": (
            True if not exact_baseline_gates_enabled
            else summary_by_strategy.get("OnlyOOH", {}).get("home_delivery_mean", 1.0) <= 0.001
        ),
    }
    gates["passed"] = all(
        gates[key]
        for key in (
            "failure_costs_zero",
            "NoOOH_home_delivery_ge_0_999",
            "OnlyOOH_home_delivery_le_0_001",
        )
    )
    return gates


def write_summary_json(path, rows, summary, gates, raw_csv, summary_csv, outside_option_util=None):
    payload = {
        "study": "akkerman_rc_no_failure",
        "description": "Synthetic RC reproduction with home delivery failure cost removed from objectives and outputs.",
        "parameters": {
            "instance": "RC",
            "max_steps_r": 90,
            "max_steps_p": 0.5,
            "revenue": 50,
            "driver_wage": 30,
            "truck_speed": 30,
            "max_price": 2,
            "min_price": -10,
            "home_failure": 0,
            "failure_cost": 0,
            "outside_option_util": outside_option_util,
            "quit_threshold": None,
            "pricing": True,
            "load_data": True,
            "data_seed": 0,
            "data_seed_test": 1,
        },
        "strategies": STRATEGIES,
        "n_rows": len(rows),
        "raw_csv": str(raw_csv),
        "summary_csv": str(summary_csv),
        "acceptance_gates": gates,
        "summary": summary,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def analyze(raw_csv, output_dir=None, outside_option_util=None):
    raw_csv = Path(raw_csv)
    rows = read_raw_csv(raw_csv)
    summary = summarize_rows(rows)
    gates = acceptance_gates(rows, summary, outside_option_util=outside_option_util)
    output_dir = Path(output_dir) if output_dir else raw_csv.parent
    summary_csv = output_dir / "summary.csv"
    summary_json = output_dir / "summary.json"
    write_csv(summary_csv, summary, SUMMARY_FIELDS)
    write_summary_json(summary_json, rows, summary, gates, raw_csv, summary_csv, outside_option_util=outside_option_util)
    if not gates["passed"]:
        raise SystemExit("Acceptance gates failed: " + json.dumps(gates, sort_keys=True))
    return summary_json


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Run Akkerman synthetic RC no-failure-cost reproduction.")
    parser.add_argument("--dry_run", action="store_true", help="Print planned runs without executing them")
    parser.add_argument("--smoke", action="store_true", help="Run one short seed/episode unless --seeds overrides it")
    parser.add_argument("--analyze", action="store_true", help="Analyze an existing raw CSV")
    parser.add_argument("--input", default="", help="Raw CSV to analyze")
    parser.add_argument("--seeds", default=None, help="Comma/range seed list, e.g. 0,1,2 or 0-29")
    parser.add_argument("--outside_option_util", default="None", type=parse_optional_float,
                        help="Passenger exit utility; None disables exit, numeric value enables outside option")
    parser.add_argument("--output_dir", default="", help="Output directory override")
    parser.add_argument("--max_episodes", type=int, default=0, help="Training episodes per learned strategy")
    parser.add_argument("--eval_episodes", type=int, default=0, help="Evaluation episodes per strategy/seed")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if args.analyze:
        if not args.input:
            raise SystemExit("--analyze requires --input")
        summary_json = analyze(args.input, output_dir=args.output_dir or None, outside_option_util=args.outside_option_util)
        print(summary_json)
        return summary_json

    seed_text = args.seeds if args.seeds is not None else ("0" if args.smoke else "0-29")
    seeds = parse_seeds(seed_text)
    if not seeds:
        raise SystemExit("No seeds resolved from --seeds")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = "smoke_" + stamp if args.smoke else "formal_" + stamp
    output_dir = Path(args.output_dir) if args.output_dir else ROOT / "outputs" / "akkerman_rc_no_failure" / run_id
    raw_csv = output_dir / "raw.csv"
    summary_csv = output_dir / "summary.csv"
    summary_json = output_dir / "summary.json"
    max_episodes = args.max_episodes if args.max_episodes > 0 else None
    eval_episodes = args.eval_episodes if args.eval_episodes > 0 else (1 if args.smoke else 20)

    plan = [
        {"strategy": strategy, "seed": seed}
        for seed in seeds
        for strategy in STRATEGIES
    ]
    if args.dry_run:
        print(json.dumps({
            "run_id": run_id,
            "output_dir": str(output_dir),
            "seeds": seeds,
            "strategies": STRATEGIES,
            "n_runs": len(plan),
            "smoke": bool(args.smoke),
            "outside_option_util": args.outside_option_util,
        }, indent=2, sort_keys=True))
        return None

    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in plan:
        print("running", item["strategy"], "seed", item["seed"])
        rows.append(
            run_strategy(
                item["strategy"],
                item["seed"],
                run_id,
                smoke=args.smoke,
                max_episodes=max_episodes,
                eval_episodes=eval_episodes,
                outside_option_util=args.outside_option_util,
            )
        )
        write_csv(raw_csv, rows, RAW_FIELDS)

    summary = summarize_rows(rows)
    gates = acceptance_gates(rows, summary, outside_option_util=args.outside_option_util)
    write_csv(summary_csv, summary, SUMMARY_FIELDS)
    write_summary_json(summary_json, rows, summary, gates, raw_csv, summary_csv, outside_option_util=args.outside_option_util)
    if not gates["passed"]:
        raise SystemExit("Acceptance gates failed: " + json.dumps(gates, sort_keys=True))
    print(summary_json)
    return summary_json


if __name__ == "__main__":
    main()
