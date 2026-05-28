import argparse
import csv
import os
import sys
from copy import deepcopy
from pathlib import Path
from time import perf_counter


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Src.parser import Parser
from Src.research_pipeline import (
    build_variant_solver,
    generate_request_traces,
    parser_namespace_with_overrides,
    train_or_reuse_shared_model,
)
from run_menu_compare import aggregate_episode_metrics, restore_stdout


BASELINE_SCHEMA = [
    "method",
    "seed",
    "instance",
    "K",
    "L",
    "net_profit",
    "total_cost",
    "travel_cost",
    "service_cost",
    "base_revenue",
    "charge_revenue",
    "discount_cost",
    "quit_rate",
    "acceptance_rate",
    "mp_share",
    "home_share",
    "avg_walk",
    "avg_in_vehicle_time",
    "avg_price",
    "menu_regret",
    "topL_overlap",
    "runtime_sec",
]

_PARSER_BASE_KEYS = set(vars(Parser().get_parser().parse_args([])).keys())


BASELINE_METHODS = [
    {
        "method": "home_only",
        "policy": "home_only",
    },
    {
        "method": "nearest_L",
        "policy": "nearest_heuristic",
    },
    {
        "method": "cost_L_heuristic",
        "policy": "cost_l_heuristic",
    },
    {
        "method": "cnn_menu",
        "policy": "top_k_cheapest",
    },
    {
        "method": "full_candidate_cnn",
        "policy": "offer_all_feasible_bundles",
    },
]


def parse_csv_ints(text):
    return [int(token.strip()) for token in str(text).split(",") if token.strip()]


def build_base_args(seed, instance, candidate_pool_k, display_l):
    parser = Parser()
    args = parser.parse_args(
        [
            "--experiment_name",
            "work2_baseline_smoke",
            "--run_suffix",
            "_baseline_smoke",
            "--instance",
            instance,
            "--load_data",
            "true",
            "--data_seed",
            "0",
            "--data_seed_test",
            "1",
            "--seed",
            str(seed),
            "--max_episodes",
            "1",
            "--max_steps_r",
            "1",
            "--max_steps_p",
            "0.5",
            "--n_vehicles",
            "2",
            "--veh_capacity",
            "2",
            "--hgs_reopt_time",
            "0.1",
            "--hgs_final_time",
            "0.1",
            "--menu_k",
            str(display_l),
            "--candidate_meeting_points",
            str(candidate_pool_k),
            "--menu_keep_home",
            "true",
            "--save_model",
            "true",
            "--log_output",
            "file",
            "--debug",
            "true",
            "--gpu",
            "0",
        ]
    )
    args.eval_episodes = 1
    return args



def evaluate_with_logs(solver, request_traces, policy, display_l):
    config = solver.config
    solver.config.menu_policy = policy
    solver.config.menu_k = int(display_l)
    solver.model.menu_policy = policy
    solver.model.menu_k = int(display_l)
    solver.test_env.seed(config.seed)
    solver.test_env.set_request_trace(request_traces)

    episodes = []
    for episode_idx in range(len(request_traces)):
        state = solver.test_env.reset(training=False)
        solver.model.reset()
        done = False
        step_times = []
        stats = None
        route_data = None
        travel_time = 0.0
        while not done:
            start = perf_counter()
            action = solver.model.get_action(state, training=False)
            state, done, stats, route_data = solver.test_env.step(action=action)
            step_times.append(perf_counter() - start)
            if done:
                travel_time = solver.model.update(route_data, state, True)
        from run_menu_compare import summarize_episode

        episode_metrics = summarize_episode(config, stats, route_data, travel_time, step_times)
        episode_metrics["episode"] = int(episode_idx)
        episode_metrics["menu_policy"] = policy
        episode_metrics["menu_k"] = int(display_l)
        episode_metrics["_menu_logs"] = deepcopy(route_data.get("menu_logs", []))
        episodes.append(episode_metrics)

    solver.test_env.clear_request_trace()
    return episodes


def mean(values):
    values = [float(value) for value in values if value is not None]
    return sum(values) / len(values) if values else 0.0


def overlap_against_reference(method_episodes, reference_episodes):
    scores = []
    for ep, ref_ep in zip(method_episodes, reference_episodes):
        for log, ref_log in zip(ep.get("_menu_logs", []), ref_ep.get("_menu_logs", [])):
            chosen = {
                offer.get("bundle_id")
                for offer in log.get("displayed_offers", [])
                if not offer.get("is_home", False)
            }
            ref = {
                offer.get("bundle_id")
                for offer in ref_log.get("displayed_offers", [])
                if not offer.get("is_home", False)
            }
            denom = max(len(chosen), len(ref), 1)
            scores.append(len(chosen & ref) / denom)
    return mean(scores)


def summarize_row(
    method,
    seed,
    instance,
    candidate_pool_k,
    display_l,
    episodes,
    runtime_sec,
    base_revenue_per_customer,
    reference_episodes=None,
):
    summary = aggregate_episode_metrics(episodes)
    base_revenue = float(summary.get("served_customers", 0.0)) * float(base_revenue_per_customer)
    menu_regret = 0.0
    top_l_overlap = 1.0
    if reference_episodes is not None:
        ref_summary = aggregate_episode_metrics(reference_episodes)
        menu_regret = max(0.0, float(ref_summary.get("net_profit", 0.0)) - float(summary.get("net_profit", 0.0)))
        top_l_overlap = overlap_against_reference(episodes, reference_episodes)
    return {
        "method": method,
        "seed": int(seed),
        "instance": instance,
        "K": int(candidate_pool_k),
        "L": int(display_l),
        "net_profit": summary.get("net_profit", 0.0),
        "total_cost": summary.get("total_cost", 0.0),
        "travel_cost": summary.get("travel_cost", 0.0),
        "service_cost": summary.get("service_cost", 0.0),
        "base_revenue": base_revenue,
        "charge_revenue": summary.get("charge_revenue", 0.0),
        "discount_cost": summary.get("discount_cost", 0.0),
        "quit_rate": summary.get("opt_out_rate", 0.0),
        "acceptance_rate": summary.get("acceptance_rate", 0.0),
        "mp_share": summary.get("non_home_acceptance_rate", 0.0),
        "home_share": summary.get("home_pickup_share", 0.0),
        "avg_walk": summary.get("avg_walk_distance", 0.0),
        "avg_in_vehicle_time": summary.get("avg_in_vehicle_time", 0.0),
        "avg_price": summary.get("avg_chosen_price", 0.0),
        "menu_regret": menu_regret,
        "topL_overlap": top_l_overlap,
        "runtime_sec": float(runtime_sec),
    }


def write_rows(path, rows):
    os.makedirs(Path(path).parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=BASELINE_SCHEMA)
        writer.writeheader()
        writer.writerows(rows)


def run_one_seed(seed, instance, candidate_pool_k, display_l):
    base_args = build_base_args(seed, instance, candidate_pool_k, display_l)
    training = train_or_reuse_shared_model(base_args, reuse_existing=True)
    base_public_args = {key: value for key, value in vars(base_args).items() if key in _PARSER_BASE_KEYS}
    traces = generate_request_traces(
        base_args,
        training["checkpoint_path"],
        eval_episodes=base_args.eval_episodes,
        trace_seed=seed,
    )

    rows = []
    episode_cache = {}
    runtime_cache = {}

    for method_spec in BASELINE_METHODS:
        overrides = dict(method_spec.get("overrides", {}))
        overrides["menu_k"] = int(display_l)
        variant_args = parser_namespace_with_overrides({**base_public_args, **overrides})
        variant_args.eval_episodes = base_args.eval_episodes
        _, solver = build_variant_solver(variant_args, training["checkpoint_path"])
        start = perf_counter()
        episodes = evaluate_with_logs(solver, traces, method_spec["policy"], display_l)
        runtime_cache[method_spec["method"]] = perf_counter() - start
        episode_cache[method_spec["method"]] = episodes
        restore_stdout()

    reference = episode_cache.get("full_candidate_cnn")
    for method_spec in BASELINE_METHODS:
        method = method_spec["method"]
        rows.append(
            summarize_row(
                method,
                seed,
                instance,
                candidate_pool_k,
                display_l,
                episode_cache[method],
                runtime_cache[method],
                base_args.revenue,
                reference_episodes=reference if method != "full_candidate_cnn" else None,
            )
        )
    return rows


def main():
    parser = argparse.ArgumentParser(description="Run a tiny Work2 baseline smoke comparison with a fixed CSV schema.")
    parser.add_argument("--instance", default="RC")
    parser.add_argument("--K", type=int, default=10, help="Candidate meeting point pool size.")
    parser.add_argument("--L", type=int, default=3, help="Displayed non-home meeting point count.")
    parser.add_argument("--seeds", default="0", help="Comma-separated development seeds.")
    parser.add_argument(
        "--output",
        default=str(ROOT / "outputs" / "baseline_smoke" / "baseline_smoke.csv"),
    )
    args = parser.parse_args()

    rows = []
    for seed in parse_csv_ints(args.seeds):
        rows.extend(run_one_seed(seed, args.instance, args.K, args.L))

    write_rows(args.output, rows)
    restore_stdout()
    print("Baseline smoke CSV:", args.output)
    print("Rows:", len(rows))


if __name__ == "__main__":
    main()
