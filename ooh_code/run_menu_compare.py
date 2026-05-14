import copy
import json
import math
import os
import re
import sys
from time import time

import numpy as np

from Src.config import Config
from Src.parser import Parser
from Src.work2_runtime import Solver

_INCENTIVE_SENS_BETA = -0.25  # matches parser.py default; used for consumer surplus computation


def clone_args(args, **overrides):
    new_args = copy.deepcopy(args)
    for key, value in overrides.items():
        setattr(new_args, key, value)
    return new_args


def mean_or_zero(values):
    if len(values) == 0:
        return 0.0
    return float(np.mean(values))


def percentile_or_zero(values, q):
    if len(values) == 0:
        return 0.0
    return float(np.percentile(values, q))


def confidence_half_width(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) <= 1:
        return 0.0
    return float(1.96 * np.std(arr, ddof=1) / math.sqrt(len(arr)))


def normalize_checkpoint_path(checkpoint_path):
    if checkpoint_path is None or checkpoint_path == "":
        return ""
    checkpoint_path = os.path.abspath(checkpoint_path)
    if os.path.isfile(checkpoint_path):
        checkpoint_path = os.path.dirname(checkpoint_path)
    if os.path.isdir(checkpoint_path):
        return os.path.join(checkpoint_path, "")
    return checkpoint_path


def restore_stdout():
    current_stdout = sys.stdout
    if current_stdout is sys.__stdout__:
        return
    try:
        current_stdout.flush()
    except Exception:
        pass
    sys.stdout = sys.__stdout__
    log_handle = getattr(current_stdout, "log", None)
    if log_handle is not None:
        try:
            log_handle.close()
        except Exception:
            pass


def build_eval_solver(args, checkpoint_path):
    eval_args = clone_args(
        args,
        eval_only=True,
        freeze_learning=True,
        load_checkpoint_path=checkpoint_path,
        log_output="file",
    )
    restore_stdout()
    config = Config(eval_args)
    solver = Solver(config=config)
    solver.model.eval_mode()
    restore_stdout()
    return config, solver


def set_policy(solver, menu_policy, menu_k):
    solver.config.menu_policy = menu_policy
    solver.config.menu_k = int(menu_k)
    solver.model.menu_policy = menu_policy
    solver.model.menu_k = int(menu_k)


def extract_menu_metrics(menu_logs):
    displayed_counts = []
    displayed_meeting_point_counts = []
    feasible_meeting_point_counts = []
    home_only_steps = 0
    home_only_with_feasible_meeting_point_steps = 0
    home_pickup_choices = 0
    non_home_acceptances = 0
    walk_distances = []
    pickup_deviations = []
    in_vehicle_times = []
    chosen_predicted_costs = []
    chosen_prices = []
    menu_build_times = []
    opt_out_count = 0
    consumer_surplus_values = []
    price_at_floor_count = 0
    price_at_ceil_count = 0
    accepted_count = 0
    fn_pruning_rates = []
    fn_pruned_near_counts = []
    fn_pruned_mid_counts = []
    fn_pruned_far_counts = []
    eta_abs_errors = []
    ivt_abs_errors = []
    displayed_eta_abs_errors = []
    displayed_ivt_abs_errors = []
    displayed_eta_signed_errors = []
    displayed_ivt_signed_errors = []
    exact_menu_values = []
    greedy_menu_values = []
    relative_optimality_gaps = []
    menu_overlap_rates = []
    exact_build_times = []
    greedy_build_times = []
    exact_gap_candidate_counts = []
    exact_gap_logged_count = 0

    for log in menu_logs:
        displayed_offers = log.get("displayed_offers", [])
        displayed_counts.append(len(displayed_offers))
        displayed_meeting_point_count = sum(0 if offer.get("is_home", False) else 1 for offer in displayed_offers)
        displayed_meeting_point_counts.append(int(displayed_meeting_point_count))
        feasible_meeting_point_count = 0
        if len(displayed_offers) > 0:
            metadata = displayed_offers[0].get("metadata") or {}
            feasible_meeting_point_count = int(
                metadata.get("feasible_meeting_point_count", displayed_meeting_point_count)
            )
            fn_rate = metadata.get("fn_pruning_rate")
            if fn_rate is not None:
                fn_pruning_rates.append(float(fn_rate))
            fn_near = metadata.get("fn_pruned_near")
            if fn_near is not None:
                fn_pruned_near_counts.append(int(fn_near))
            fn_mid = metadata.get("fn_pruned_mid")
            if fn_mid is not None:
                fn_pruned_mid_counts.append(int(fn_mid))
            fn_far = metadata.get("fn_pruned_far")
            if fn_far is not None:
                fn_pruned_far_counts.append(int(fn_far))
            if metadata.get("exact_gap_logged"):
                exact_gap_logged_count += 1
                if metadata.get("exact_menu_value") is not None:
                    exact_menu_values.append(float(metadata.get("exact_menu_value")))
                if metadata.get("greedy_menu_value") is not None:
                    greedy_menu_values.append(float(metadata.get("greedy_menu_value")))
                if metadata.get("relative_optimality_gap") is not None:
                    relative_optimality_gaps.append(float(metadata.get("relative_optimality_gap")))
                if metadata.get("menu_overlap_rate") is not None:
                    menu_overlap_rates.append(float(metadata.get("menu_overlap_rate")))
                if metadata.get("exact_build_time") is not None:
                    exact_build_times.append(float(metadata.get("exact_build_time")))
                if metadata.get("greedy_build_time") is not None:
                    greedy_build_times.append(float(metadata.get("greedy_build_time")))
                if metadata.get("exact_gap_candidate_count") is not None:
                    exact_gap_candidate_counts.append(float(metadata.get("exact_gap_candidate_count")))
        for offer in displayed_offers:
            if offer.get("is_home", False):
                continue
            metadata = offer.get("metadata") or {}
            true_eta = metadata.get("true_eta")
            true_ivt = metadata.get("true_ivt")
            pred_eta = offer.get("predicted_eta")
            pred_ivt = offer.get("predicted_in_vehicle_time")
            if true_eta is not None and pred_eta is not None:
                signed_error_eta = float(pred_eta) - float(true_eta)
                displayed_eta_abs_errors.append(abs(signed_error_eta))
                displayed_eta_signed_errors.append(signed_error_eta)
            if true_ivt is not None and pred_ivt is not None:
                signed_error_ivt = float(pred_ivt) - float(true_ivt)
                displayed_ivt_abs_errors.append(abs(signed_error_ivt))
                displayed_ivt_signed_errors.append(signed_error_ivt)
        feasible_meeting_point_counts.append(int(feasible_meeting_point_count))
        if displayed_meeting_point_count == 0:
            home_only_steps += 1
            if feasible_meeting_point_count > 0:
                home_only_with_feasible_meeting_point_steps += 1
        chosen_offer = log.get("chosen_offer")
        if log.get("opted_out", False):
            opt_out_count += 1
        if chosen_offer is None:
            continue
        home_pickup_choices += int(bool(chosen_offer.get("is_home", False)))
        if (not log.get("opted_out", False)) and (not chosen_offer.get("is_home", False)):
            non_home_acceptances += 1
        walk_distances.append(float(chosen_offer.get("walk_distance", 0.0)))
        pickup_deviations.append(float(chosen_offer.get("time_deviation", 0.0)))
        in_vehicle_times.append(float(chosen_offer.get("predicted_in_vehicle_time", 0.0)))
        chosen_predicted_costs.append(float(chosen_offer.get("predicted_cost", 0.0)))
        price = float(chosen_offer.get("price", 0.0))
        chosen_prices.append(price)
        metadata = chosen_offer.get("metadata") or {}
        menu_build_times.append(float(metadata.get("menu_build_time", 0.0)))
        true_eta = metadata.get("true_eta")
        true_ivt = metadata.get("true_ivt")
        pred_eta = chosen_offer.get("predicted_eta")
        pred_ivt = chosen_offer.get("predicted_in_vehicle_time")
        if true_eta is not None and pred_eta is not None and not chosen_offer.get("is_home", False):
            eta_abs_errors.append(abs(float(pred_eta) - float(true_eta)))
        if true_ivt is not None and pred_ivt is not None and not chosen_offer.get("is_home", False):
            ivt_abs_errors.append(abs(float(pred_ivt) - float(true_ivt)))
        if not log.get("opted_out", False):
            full_utility = float(chosen_offer.get("predicted_utility") or 0.0)
            consumer_surplus_values.append(full_utility - _INCENTIVE_SENS_BETA * price)
            p_min = float(metadata.get("p_min", -6.0))
            p_max = float(metadata.get("p_max", 5.0))
            if abs(price - p_min) < 1e-6:
                price_at_floor_count += 1
            if abs(price - p_max) < 1e-6:
                price_at_ceil_count += 1
            accepted_count += 1

    return {
        "displayed_bundle_count_sequence": displayed_counts,
        "feasible_meeting_point_count_sequence": feasible_meeting_point_counts,
        "avg_meeting_point_count_per_menu": mean_or_zero(displayed_meeting_point_counts),
        "average_menu_size": mean_or_zero(displayed_counts),
        "home_pickup_only_share": float(home_only_steps / len(menu_logs)) if len(menu_logs) > 0 else 0.0,
        "home_pickup_only_with_feasible_meeting_point_share": (
            float(home_only_with_feasible_meeting_point_steps / len(menu_logs)) if len(menu_logs) > 0 else 0.0
        ),
        "home_pickup_share": float(home_pickup_choices / len(menu_logs)) if len(menu_logs) > 0 else 0.0,
        "acceptance_rate": float(1.0 - opt_out_count / len(menu_logs)) if len(menu_logs) > 0 else 0.0,
        "non_home_acceptance_rate": float(non_home_acceptances / len(menu_logs)) if len(menu_logs) > 0 else 0.0,
        "avg_walk_distance": mean_or_zero(walk_distances),
        "avg_pickup_time_deviation": mean_or_zero(pickup_deviations),
        "avg_in_vehicle_time": mean_or_zero(in_vehicle_times),
        "avg_chosen_predicted_cost": mean_or_zero(chosen_predicted_costs),
        "avg_chosen_price": mean_or_zero(chosen_prices),
        "avg_menu_build_time": mean_or_zero(menu_build_times),
        "opt_out_rate": float(opt_out_count / len(menu_logs)) if len(menu_logs) > 0 else 0.0,
        "consumer_surplus": mean_or_zero(consumer_surplus_values),
        "price_at_floor_fraction": float(price_at_floor_count / accepted_count) if accepted_count > 0 else 0.0,
        "price_at_ceil_fraction": float(price_at_ceil_count / accepted_count) if accepted_count > 0 else 0.0,
        "avg_fn_pruning_rate": mean_or_zero(fn_pruning_rates),
        "avg_fn_pruned_near": mean_or_zero(fn_pruned_near_counts),
        "avg_fn_pruned_mid": mean_or_zero(fn_pruned_mid_counts),
        "avg_fn_pruned_far": mean_or_zero(fn_pruned_far_counts),
        "avg_eta_mae": mean_or_zero(eta_abs_errors),
        "avg_ivt_mae": mean_or_zero(ivt_abs_errors),
        "avg_displayed_eta_mae": mean_or_zero(displayed_eta_abs_errors),
        "avg_displayed_ivt_mae": mean_or_zero(displayed_ivt_abs_errors),
        "avg_displayed_eta_bias": mean_or_zero(displayed_eta_signed_errors),
        "avg_displayed_ivt_bias": mean_or_zero(displayed_ivt_signed_errors),
        "displayed_eta_p50": percentile_or_zero(displayed_eta_abs_errors, 50),
        "displayed_eta_p90": percentile_or_zero(displayed_eta_abs_errors, 90),
        "displayed_eta_p95": percentile_or_zero(displayed_eta_abs_errors, 95),
        "displayed_ivt_p50": percentile_or_zero(displayed_ivt_abs_errors, 50),
        "displayed_ivt_p90": percentile_or_zero(displayed_ivt_abs_errors, 90),
        "displayed_ivt_p95": percentile_or_zero(displayed_ivt_abs_errors, 95),
        "exact_gap_logged_share": float(exact_gap_logged_count / len(menu_logs)) if len(menu_logs) > 0 else 0.0,
        "avg_exact_menu_value": mean_or_zero(exact_menu_values),
        "avg_greedy_menu_value": mean_or_zero(greedy_menu_values),
        "avg_relative_optimality_gap": mean_or_zero(relative_optimality_gaps),
        "avg_menu_overlap_rate": mean_or_zero(menu_overlap_rates),
        "avg_exact_build_time": mean_or_zero(exact_build_times),
        "avg_greedy_build_time": mean_or_zero(greedy_build_times),
        "avg_exact_gap_candidate_count": mean_or_zero(exact_gap_candidate_counts),
    }


def summarize_episode(config, stats, route_data, travel_time, step_times):
    cost_multiplier = (config.driver_wage + config.fuel_cost) / 3600.0
    charge_revenue = float(np.sum(stats[3])) if len(stats[3]) > 0 else 0.0
    discount_cost = float(-np.sum(stats[6])) if len(stats[6]) > 0 else 0.0
    travel_cost = float(travel_time) * cost_multiplier
    service_cost = float(stats[2]) * cost_multiplier
    failure_cost = float(stats[1]) * config.home_failure * config.failure_cost
    total_cost = travel_cost + service_cost + failure_cost + discount_cost - charge_revenue
    net_profit = charge_revenue - discount_cost - travel_cost - service_cost - failure_cost

    menu_logs = route_data.get("menu_logs", [])
    menu_metrics = extract_menu_metrics(menu_logs)

    return {
        "served_customers": int(len(route_data["id"]) - 1),
        "travel_time": float(travel_time),
        "travel_cost": float(travel_cost),
        "service_cost": float(service_cost),
        "failure_cost": float(failure_cost),
        "discount_cost": float(discount_cost),
        "charge_revenue": float(charge_revenue),
        "total_cost": float(total_cost),
        "net_profit": float(net_profit),
        "home_pickup_count": int(stats[1]),
        "avg_step_time": mean_or_zero(step_times),
        **menu_metrics,
    }


def aggregate_episode_metrics(episodes):
    metric_keys = [
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
    summary = {"episodes": int(len(episodes))}
    for key in metric_keys:
        summary[key] = mean_or_zero([episode[key] for episode in episodes])
    return summary


def compare_episode_menu_sizes(full_episodes, menu_episodes):
    same_length = True
    full_episode_avg_sizes = []
    menu_episode_avg_sizes = []
    menu_not_larger_flags = []
    for full_episode, menu_episode in zip(full_episodes, menu_episodes):
        full_counts = full_episode["displayed_bundle_count_sequence"]
        menu_counts = menu_episode["displayed_bundle_count_sequence"]
        if len(full_counts) != len(menu_counts):
            same_length = False
        full_avg = mean_or_zero(full_counts)
        menu_avg = mean_or_zero(menu_counts)
        full_episode_avg_sizes.append(full_avg)
        menu_episode_avg_sizes.append(menu_avg)
        menu_not_larger_flags.append(menu_avg <= full_avg + 1e-9)
    overall_full_avg = mean_or_zero(full_episode_avg_sizes)
    overall_menu_avg = mean_or_zero(menu_episode_avg_sizes)
    avg_gaps = [menu_avg - full_avg for full_avg, menu_avg in zip(full_episode_avg_sizes, menu_episode_avg_sizes)]
    return {
        "display_count_sequence_same_length": bool(same_length),
        "full_display_average_menu_size": overall_full_avg,
        "menu_recommendation_average_menu_size": overall_menu_avg,
        "mean_average_menu_size_gap": mean_or_zero(avg_gaps),
        "menu_not_larger_on_average": bool(overall_menu_avg <= overall_full_avg + 1e-9),
        "episode_share_menu_not_larger": float(np.mean(menu_not_larger_flags)) if len(menu_not_larger_flags) > 0 else 0.0,
    }


def paired_summary(full_episodes, menu_episodes):
    full_net = np.asarray([episode["net_profit"] for episode in full_episodes], dtype=float)
    menu_net = np.asarray([episode["net_profit"] for episode in menu_episodes], dtype=float)
    full_cost = np.asarray([episode["total_cost"] for episode in full_episodes], dtype=float)
    menu_cost = np.asarray([episode["total_cost"] for episode in menu_episodes], dtype=float)
    net_diff = menu_net - full_net
    cost_diff = menu_cost - full_cost
    menu_size_summary = compare_episode_menu_sizes(full_episodes, menu_episodes)
    return {
        "episodes": int(len(full_episodes)),
        "full_display_mean_net_profit": mean_or_zero(full_net.tolist()),
        "menu_optimization_mean_net_profit": mean_or_zero(menu_net.tolist()),
        "full_display_mean_total_cost": mean_or_zero(full_cost.tolist()),
        "menu_optimization_mean_total_cost": mean_or_zero(menu_cost.tolist()),
        "mean_net_profit_gap": mean_or_zero(net_diff.tolist()),
        "mean_total_cost_gap": mean_or_zero(cost_diff.tolist()),
        "net_profit_win_rate": float(np.mean(net_diff > 0.0)) if len(net_diff) > 0 else 0.0,
        "net_profit_gap_ci95_half_width": confidence_half_width(net_diff),
        **menu_size_summary,
    }


def evaluate_policy(solver, request_traces, menu_policy, menu_k=None):
    if menu_k is None:
        menu_k = solver.config.menu_k
    set_policy(solver, menu_policy=menu_policy, menu_k=menu_k)
    config = solver.config
    solver.test_env.seed(config.seed)
    solver.test_env.set_request_trace(request_traces)

    episodes = []
    for episode_idx in range(len(request_traces)):
        state = solver.test_env.reset(training=False)
        solver.model.reset()
        done = False
        step = 0
        step_times = []
        stats = None
        route_data = None

        while not done:
            start = time()
            action = solver.model.get_action(state, training=False)
            state, done, stats, route_data = solver.test_env.step(action=action)
            step_times.append(time() - start)
            step += 1
            if step >= solver.max_steps or done:
                break

        travel_time = solver.test_env.reopt_for_eval(route_data)
        episode_metrics = summarize_episode(config, stats, route_data, travel_time, step_times)
        episode_metrics["episode"] = int(episode_idx)
        episode_metrics["menu_policy"] = menu_policy
        episode_metrics["menu_k"] = int(menu_k)
        episodes.append(episode_metrics)

    solver.test_env.clear_request_trace()
    return config, episodes


def save_json(filename, payload):
    with open(filename, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def clear_stale_robustness_outputs(compare_root):
    if not os.path.isdir(compare_root):
        return
    for filename in os.listdir(compare_root):
        if re.fullmatch(r"menu_optimization_k\d+_episode_metrics\.json", filename):
            os.remove(os.path.join(compare_root, filename))


def build_compare_root(outputs_root, run_name, seed):
    return os.path.join(outputs_root, "menu_compare", run_name, str(seed))


def main():
    parser_builder = Parser()
    parser = parser_builder.get_parser()
    parser.add_argument(
        "--shared_checkpoint_path",
        default="",
        help="Path to a shared predictor checkpoint directory or checkpoint file.",
    )
    parser.add_argument(
        "--skip_train",
        default=False,
        type=parser_builder.str2bool,
        help="Skip shared-predictor training and evaluate from an existing checkpoint.",
    )
    parser.add_argument(
        "--eval_episodes",
        default=20,
        type=int,
        help="Number of frozen-evaluation episodes used in the paired menu comparison.",
    )
    parser.add_argument(
        "--trace_seed",
        default=-1,
        type=int,
        help="Seed used to generate replayable request traces; -1 reuses --seed.",
    )
    parser.add_argument(
        "--menu_k_values",
        default="1,2,3,5",
        help="Comma-separated menu-size values used in the robustness sweep.",
    )
    args = parser_builder.finalize_args(parser.parse_args())

    trace_seed = args.seed if args.trace_seed < 0 else args.trace_seed
    checkpoint_path = normalize_checkpoint_path(args.shared_checkpoint_path)

    if checkpoint_path == "" and args.skip_train:
        raise ValueError("skip_train=True requires --shared_checkpoint_path.")

    if checkpoint_path == "":
        train_args = clone_args(
            args,
            menu_policy="offer_all_feasible_bundles",
            eval_only=False,
            freeze_learning=False,
            load_checkpoint_path="",
        )
        restore_stdout()
        train_config = Config(train_args)
        train_solver = Solver(config=train_config)
        train_solver.train()
        restore_stdout()
        checkpoint_path = normalize_checkpoint_path(train_config.paths["checkpoint"])
        outputs_root = train_config.paths["outputs_root"]
        run_name = train_config.run_name
        shared_model_file = os.path.join(checkpoint_path, "supervised_ml.pt")
        if os.path.exists(shared_model_file):
            eval_config, eval_solver = build_eval_solver(args, checkpoint_path)
            trace_env = eval_config.test_env
        else:
            eval_config = train_config
            eval_solver = train_solver
            eval_solver.model.eval_mode()
            eval_solver.config.eval_only = True
            eval_solver.config.freeze_learning = True
            trace_env = eval_config.test_env
    else:
        eval_config, eval_solver = build_eval_solver(args, checkpoint_path)
        trace_env = eval_config.test_env
        outputs_root = eval_config.paths["outputs_root"]
        run_name = eval_config.run_name

    request_traces = trace_env.generate_request_traces(args.eval_episodes, seed=trace_seed)

    compare_root = build_compare_root(outputs_root, run_name, args.seed)
    os.makedirs(compare_root, exist_ok=True)
    clear_stale_robustness_outputs(compare_root)
    np.save(os.path.join(compare_root, "request_traces.npy"), np.array(request_traces, dtype=object))

    _, full_display_episodes = evaluate_policy(
        solver=eval_solver,
        request_traces=request_traces,
        menu_policy="offer_all_feasible_bundles",
        menu_k=args.menu_k,
    )
    _, menu_episodes = evaluate_policy(
        solver=eval_solver,
        request_traces=request_traces,
        menu_policy="menu_optimization",
        menu_k=args.menu_k,
    )

    full_summary = aggregate_episode_metrics(full_display_episodes)
    menu_summary = aggregate_episode_metrics(menu_episodes)
    main_paired_summary = paired_summary(full_display_episodes, menu_episodes)

    save_json(os.path.join(compare_root, "full_display_episode_metrics.json"), full_display_episodes)
    save_json(os.path.join(compare_root, "menu_optimization_episode_metrics.json"), menu_episodes)
    save_json(os.path.join(compare_root, "full_display_summary.json"), full_summary)
    save_json(os.path.join(compare_root, "menu_optimization_summary.json"), menu_summary)
    save_json(os.path.join(compare_root, "paired_summary.json"), main_paired_summary)

    robustness = []
    seen_k = set()
    for token in str(args.menu_k_values).split(","):
        token = token.strip()
        if token == "":
            continue
        menu_k = int(token)
        if menu_k == int(args.menu_k) or menu_k in seen_k:
            continue
        seen_k.add(menu_k)
        _, robustness_episodes = evaluate_policy(
            solver=eval_solver,
            request_traces=request_traces,
            menu_policy="menu_optimization",
            menu_k=menu_k,
        )
        robustness.append(
            {
                "menu_k": menu_k,
                "summary": aggregate_episode_metrics(robustness_episodes),
                "paired_vs_full_display": paired_summary(full_display_episodes, robustness_episodes),
            }
        )
        save_json(
            os.path.join(compare_root, f"menu_optimization_k{menu_k}_episode_metrics.json"),
            robustness_episodes,
        )
    save_json(os.path.join(compare_root, "robustness_menu_k_summary.json"), robustness)

    restore_stdout()
    print("Shared checkpoint:", checkpoint_path)
    print("Comparison outputs:", compare_root)
    print("Full display mean net profit:", full_summary["net_profit"])
    print("Menu optimization mean net profit:", menu_summary["net_profit"])
    print("Mean net profit gap (menu - full):", main_paired_summary["mean_net_profit_gap"])
    print("Net profit win rate:", main_paired_summary["net_profit_win_rate"])
    print("95% CI half width:", main_paired_summary["net_profit_gap_ci95_half_width"])


if __name__ == "__main__":
    main()
