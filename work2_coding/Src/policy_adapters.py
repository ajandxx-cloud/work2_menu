"""Policy tag adapters for Work2 robust-menu study manifests."""

from copy import deepcopy


REQUIRED_POLICY_TAGS = [
    "full_display",
    "home_only",
    "nearest_heuristic",
    "top_k_cheapest",
    "min_lateness",
    "hard_filter",
    "no_filter_diagnostic",
    "robust_risk_adjusted",
    "robust_service_guarded",
]

OPTIONAL_POLICY_TAGS = [
    "random_top_k",
    "contract_no_menu",
    "contract_fixed_menu",
    "contract_random_menu",
    "contract_optimized_menu",
    "mainline_no_menu",
    "mainline_fixed_menu",
    "mainline_random_menu",
    "mainline_optimized_m",
    "mainline_optimized_mw",
    "mainline_optimized_fixed_window",
    "mainline_optimized_adaptive",
]

ATTENTION_POLICY_TAGS = [
    "DSPO_original",
    "DSPO_attention",
]

MAINLINE_POLICY_TAGS = [
    "mainline_no_menu",
    "mainline_fixed_menu",
    "mainline_random_menu",
    "mainline_optimized_m",
    "mainline_optimized_mw",
    "mainline_optimized_fixed_window",
    "mainline_optimized_adaptive",
]

POLICY_ONLY_FIELDS = {
    "menu_policy",
    "menu_eta_filter_mode",
    "menu_time_filtering",
    "menu_objective_mode",
    "menu_eta_chance_threshold",
    "menu_eta_soft_penalty_lambda",
    "service_quit_penalty",
    "service_quit_rate_guardrail",
    "menu_outside_penalty_lambda",
    "menu_optout_guardrail",
    "menu_selection_solver",
    "menu_use_exact_eval",
    "product_mode",
    "time_window_mode",
    "menu_contract_mode",
    "menu_pricing_mode",
    "method_variant",
    "attention_enabled",
    "attention_mode",
    "attention_strength",
    "attention_weight_eta_risk",
    "attention_weight_walk",
    "attention_weight_time",
    "attention_weight_cost",
    "attention_weight_route_delay",
    "attention_weight_capacity_risk",
    "attention_weight_price",
}

ADAPTER_DEFAULTS = {
    "algo_name": "DSPO_Menu",
    "menu_mode": True,
}

POLICY_ADAPTERS = {
    "full_display": {
        "description": "Display every feasible service bundle.",
        "overrides": {"menu_policy": "offer_all_feasible_bundles", "menu_eta_filter_mode": "hard"},
    },
    "home_only": {
        "description": "Accepted-home-only cost approximation boundary, not a recommended operating policy.",
        "comparison_role": "cost_bound",
        "cost_bound": True,
        "overrides": {"menu_policy": "home_only", "menu_eta_filter_mode": "hard"},
    },
    "nearest_heuristic": {
        "description": "Choose meeting points by distance/time proximity.",
        "overrides": {"menu_policy": "nearest_heuristic", "menu_eta_filter_mode": "hard"},
    },
    "top_k_cheapest": {
        "description": "Choose the cheapest predicted insertion-cost options.",
        "overrides": {"menu_policy": "top_k_cheapest", "menu_eta_filter_mode": "hard"},
    },
    "min_lateness": {
        "description": "Choose options with the least pickup-window lateness.",
        "overrides": {"menu_policy": "min_lateness", "menu_eta_filter_mode": "hard"},
    },
    "hard_filter": {
        "description": "Risk-adjusted objective with legacy hard ETA pruning.",
        "overrides": {
            "menu_policy": "risk_adjusted_expected_profit",
            "menu_eta_filter_mode": "hard",
        },
    },
    "no_filter_diagnostic": {
        "description": "Diagnostic upper-bound setting with ETA pruning disabled only.",
        "diagnostic": True,
        "overrides": {
            "menu_policy": "risk_adjusted_expected_profit",
            "menu_eta_filter_mode": "none",
            "menu_time_filtering": False,
        },
    },
    "robust_risk_adjusted": {
        "description": "Robust time-window menu with chance-constrained ETA handling.",
        "overrides": {
            "menu_policy": "risk_adjusted_expected_profit",
            "menu_eta_filter_mode": "chance_constraint",
            "menu_eta_chance_threshold": 0.25,
        },
    },
    "robust_service_guarded": {
        "description": "Robust expected-profit menu with service guardrails.",
        "overrides": {
            "menu_policy": "service_guarded_expected_profit",
            "menu_eta_filter_mode": "interval_overlap",
            "service_quit_rate_guardrail": 0.35,
        },
    },
    "random_top_k": {
        "description": "Optional random top-k floor baseline.",
        "optional": True,
        "overrides": {"menu_policy": "random_top_k", "menu_eta_filter_mode": "hard"},
    },
    "contract_no_menu": {
        "description": "Phase 2 no-menu contract: a single default home product plus outside option.",
        "optional": True,
        "comparison_role": "menu_mode",
        "menu_mode": "no_menu",
        "overrides": {
            "menu_policy": "home_only",
            "menu_eta_filter_mode": "hard",
            "menu_contract_mode": "no_menu",
            "product_mode": "m",
            "time_window_mode": "no_time_window",
            "menu_pricing_mode": "no_pricing",
        },
    },
    "contract_fixed_menu": {
        "description": "Phase 2 fixed-menu contract: nearest/top-k proximity baseline.",
        "optional": True,
        "comparison_role": "menu_mode",
        "menu_mode": "fixed_menu",
        "overrides": {
            "menu_policy": "nearest_heuristic",
            "menu_eta_filter_mode": "hard",
            "menu_contract_mode": "fixed_menu",
            "product_mode": "m+w+p",
            "time_window_mode": "fixed_window",
        },
    },
    "contract_random_menu": {
        "description": "Phase 2 random-menu contract: seeded random top-k from the same candidate pool.",
        "optional": True,
        "comparison_role": "menu_mode",
        "menu_mode": "random_menu",
        "overrides": {
            "menu_policy": "random_top_k",
            "menu_eta_filter_mode": "hard",
            "menu_contract_mode": "random_menu",
            "product_mode": "m+w+p",
            "time_window_mode": "fixed_window",
        },
    },
    "contract_optimized_menu": {
        "description": "Phase 2 optimized-menu contract: service-guarded expected-profit menu.",
        "optional": True,
        "comparison_role": "menu_mode",
        "menu_mode": "optimized_menu",
        "overrides": {
            "menu_policy": "service_guarded_expected_profit",
            "menu_eta_filter_mode": "interval_overlap",
            "service_quit_rate_guardrail": 0.35,
            "menu_contract_mode": "optimized_menu",
            "product_mode": "m+w+p",
            "time_window_mode": "adaptive_window",
        },
    },
    "mainline_no_menu": {
        "description": "V1 mainline no-menu baseline: default home product plus outside option.",
        "optional": True,
        "comparison_role": "menu_baseline",
        "menu_mode": "no_menu",
        "overrides": {
            "menu_policy": "home_only",
            "menu_eta_filter_mode": "hard",
            "menu_contract_mode": "no_menu",
            "product_mode": "m",
            "time_window_mode": "no_time_window",
            "menu_pricing_mode": "no_pricing",
        },
    },
    "mainline_fixed_menu": {
        "description": "V1 mainline fixed-menu proximity baseline.",
        "optional": True,
        "comparison_role": "menu_baseline",
        "menu_mode": "fixed_menu",
        "overrides": {
            "menu_policy": "nearest_heuristic",
            "menu_eta_filter_mode": "hard",
            "menu_contract_mode": "fixed_menu",
            "product_mode": "m+w+p",
            "time_window_mode": "fixed_window",
            "menu_pricing_mode": "lambertw",
        },
    },
    "mainline_random_menu": {
        "description": "V1 mainline random-menu baseline: seeded random top-k from the shared pool.",
        "optional": True,
        "comparison_role": "menu_baseline",
        "menu_mode": "random_menu",
        "overrides": {
            "menu_policy": "random_top_k",
            "menu_eta_filter_mode": "hard",
            "menu_contract_mode": "random_menu",
            "product_mode": "m+w+p",
            "time_window_mode": "fixed_window",
            "menu_pricing_mode": "lambertw",
        },
    },
    "mainline_optimized_m": {
        "description": "V1 mainline product ablation: meeting point only, no window or pricing.",
        "optional": True,
        "comparison_role": "product_ablation",
        "menu_mode": "optimized_menu",
        "overrides": {
            "menu_policy": "service_guarded_expected_profit",
            "menu_eta_filter_mode": "interval_overlap",
            "service_quit_rate_guardrail": 0.35,
            "menu_contract_mode": "optimized_menu",
            "product_mode": "m",
            "time_window_mode": "no_time_window",
            "menu_pricing_mode": "no_pricing",
        },
    },
    "mainline_optimized_mw": {
        "description": "V1 mainline product ablation: meeting point plus adaptive time window, no pricing.",
        "optional": True,
        "comparison_role": "product_ablation",
        "menu_mode": "optimized_menu",
        "overrides": {
            "menu_policy": "service_guarded_expected_profit",
            "menu_eta_filter_mode": "interval_overlap",
            "service_quit_rate_guardrail": 0.35,
            "menu_contract_mode": "optimized_menu",
            "product_mode": "m+w",
            "time_window_mode": "adaptive_window",
            "menu_pricing_mode": "no_pricing",
        },
    },
    "mainline_optimized_fixed_window": {
        "description": "V1 mainline time-window ablation: optimized menu with fixed windows.",
        "optional": True,
        "comparison_role": "time_window_ablation",
        "menu_mode": "optimized_menu",
        "overrides": {
            "menu_policy": "service_guarded_expected_profit",
            "menu_eta_filter_mode": "interval_overlap",
            "service_quit_rate_guardrail": 0.35,
            "menu_contract_mode": "optimized_menu",
            "product_mode": "m+w+p",
            "time_window_mode": "fixed_window",
            "menu_pricing_mode": "lambertw",
        },
    },
    "mainline_optimized_adaptive": {
        "description": "V1 mainline primary method: optimized menu with adaptive window and Lambert-W pricing.",
        "optional": True,
        "comparison_role": "primary_method",
        "menu_mode": "optimized_menu",
        "overrides": {
            "menu_policy": "service_guarded_expected_profit",
            "menu_eta_filter_mode": "interval_overlap",
            "service_quit_rate_guardrail": 0.35,
            "menu_contract_mode": "optimized_menu",
            "product_mode": "m+w+p",
            "time_window_mode": "adaptive_window",
            "menu_pricing_mode": "lambertw",
        },
    },
    "DSPO_original": {
        "description": "Original no-attention DSPO menu method for paired attention comparison.",
        "comparison_role": "method",
        "overrides": {
            "menu_policy": "risk_adjusted_expected_profit",
            "menu_eta_filter_mode": "chance_constraint",
            "menu_eta_chance_threshold": 0.25,
            "method_variant": "DSPO_original",
            "attention_enabled": False,
            "attention_mode": "deterministic",
        },
    },
    "DSPO_attention": {
        "description": "Attention-enhanced DSPO menu method with deterministic candidate attention.",
        "comparison_role": "method",
        "overrides": {
            "menu_policy": "risk_adjusted_expected_profit",
            "menu_eta_filter_mode": "chance_constraint",
            "menu_eta_chance_threshold": 0.25,
            "method_variant": "DSPO_attention",
            "attention_enabled": True,
            "attention_mode": "deterministic",
        },
    },
}


def required_policy_tags():
    return list(REQUIRED_POLICY_TAGS)


def known_policy_tags(include_optional=True):
    tags = list(REQUIRED_POLICY_TAGS)
    if include_optional:
        tags.extend(OPTIONAL_POLICY_TAGS)
    tags.extend(ATTENTION_POLICY_TAGS)
    return tags


def attention_policy_tags():
    return list(ATTENTION_POLICY_TAGS)


def mainline_policy_tags():
    return list(MAINLINE_POLICY_TAGS)


def policy_adapter(tag):
    if tag not in POLICY_ADAPTERS:
        raise ValueError("unknown policy adapter tag: " + str(tag))
    adapter = deepcopy(POLICY_ADAPTERS[tag])
    adapter["tag"] = tag
    defaults = dict(ADAPTER_DEFAULTS)
    defaults.update(adapter.get("overrides", {}))
    adapter["overrides"] = defaults
    adapter["diagnostic"] = bool(adapter.get("diagnostic", False))
    return adapter


def adapter_overrides(tag):
    return policy_adapter(tag)["overrides"]


def adapter_metadata(tag):
    adapter = policy_adapter(tag)
    return {
        "policy_tag": tag,
        "diagnostic": bool(adapter.get("diagnostic", False)),
        "optional": bool(adapter.get("optional", False)),
        "comparison_role": adapter.get("comparison_role", "policy"),
        "menu_mode": adapter.get("menu_mode"),
        "cost_bound": bool(adapter.get("cost_bound", False)),
        "description": adapter.get("description", ""),
    }


def validate_required_adapter_coverage(parser_choices=None):
    missing = [tag for tag in REQUIRED_POLICY_TAGS if tag not in POLICY_ADAPTERS]
    if missing:
        raise ValueError("missing required policy adapters: " + ", ".join(missing))

    menu_choices = None
    eta_choices = None
    if parser_choices:
        menu_choices = set(parser_choices.get("menu_policy", []))
        eta_choices = set(parser_choices.get("menu_eta_filter_mode", []))

    for tag in known_policy_tags(include_optional=True):
        overrides = adapter_overrides(tag)
        if menu_choices is not None and overrides.get("menu_policy") not in menu_choices:
            raise ValueError("adapter " + tag + " uses unsupported menu_policy: " + str(overrides.get("menu_policy")))
        if eta_choices is not None and overrides.get("menu_eta_filter_mode") not in eta_choices:
            raise ValueError(
                "adapter " + tag + " uses unsupported menu_eta_filter_mode: " + str(overrides.get("menu_eta_filter_mode"))
            )
    return True


def validate_policy_only_overrides(tag, overrides, allowed_fields=None):
    allowed = set(POLICY_ONLY_FIELDS if allowed_fields is None else allowed_fields)
    allowed.update(ADAPTER_DEFAULTS.keys())
    bad = sorted(key for key in overrides if key not in allowed)
    if bad:
        raise ValueError("policy " + str(tag) + " changes non-policy fields: " + ", ".join(bad))
    return True
