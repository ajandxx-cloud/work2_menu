import argparse
from datetime import datetime


class Parser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description=(
                "Work2 experiments for many-to-one DRT service menu optimization "
                "over meeting point and pickup time-window bundles."
            )
        )

        now = datetime.now()
        timestamp = f"{now.month}|{now.day}|{now.hour}:{now.minute}:{now.second}"

        parser.add_argument("--seed", default=1234, type=int, help="Random seed used for training and evaluation.")
        parser.add_argument(
            "--save_count",
            default=50,
            type=int,
            help="Maximum number of intermediate training snapshots used to trigger checkpoint/result saves.",
        )
        parser.add_argument(
            "--log_output",
            default="term_file",
            choices=["term_file", "term", "file"],
            help="Where to mirror runtime logs.",
        )
        parser.add_argument("--debug", default=True, type=self.str2bool, help="Enable debug-friendly defaults.")
        parser.add_argument(
            "--save_model",
            default=True,
            type=self.str2bool,
            help="Save shared predictor checkpoints during training.",
        )
        parser.add_argument(
            "--eval_only",
            default=False,
            type=self.str2bool,
            help="Skip learning updates and run frozen evaluation only.",
        )
        parser.add_argument(
            "--freeze_learning",
            default=False,
            type=self.str2bool,
            help="Disable replay-buffer writes and gradient updates.",
        )
        parser.add_argument("--load_checkpoint_path", default="", help=argparse.SUPPRESS)

        parser.add_argument("--timestamp", default=timestamp, help=argparse.SUPPRESS)
        parser.add_argument(
            "--experiment_name",
            default="work2_menu",
            help="Top-level run name used under the outputs directory.",
        )
        parser.add_argument(
            "--run_suffix",
            default="default",
            help="Optional suffix appended to the run name when saving outputs.",
        )

        parser.add_argument(
            "--max_episodes",
            default=10,
            type=int,
            help="Number of training episodes for the shared bundle predictor.",
        )
        parser.add_argument(
            "--max_steps_r",
            default=700,
            type=int,
            help="Negative-binomial r parameter controlling episode request counts.",
        )
        parser.add_argument(
            "--max_steps_p",
            default=0.5,
            type=float,
            help="Negative-binomial p parameter controlling episode request counts.",
        )
        parser.add_argument(
            "--load_data",
            default=True,
            type=self.str2bool,
            help="Load bundled benchmark instances instead of using generated toy data.",
        )
        parser.add_argument(
            "--instance",
            default="RC",
            choices=["Austin", "Seattle", "C", "R", "RC"],
            help="Benchmark instance used for training and evaluation.",
        )
        parser.add_argument(
            "--data_seed",
            default=0,
            choices=[0, 1, 2, 3],
            type=int,
            help="Training split identifier for the selected benchmark instance.",
        )
        parser.add_argument(
            "--data_seed_test",
            default=1,
            choices=[0, 1, 2, 3],
            type=int,
            help="Evaluation split identifier for the selected benchmark instance.",
        )

        parser.add_argument(
            "--menu_policy",
            default="menu_optimization",
            choices=[
                "offer_all_feasible_bundles",
                "nearest_heuristic",
                "top_k_cheapest",
                "top_k_passenger_utility",
                "revenue_greedy",
                "menu_optimization",
                "insertion_cost_greedy",
                "min_lateness",
                "random_top_k",
            ],
            help="Menu construction policy used whenever a single policy must be instantiated.",
        )
        parser.add_argument("--menu_k", default=3, type=int, help="Maximum number of non-home (OOH) offers shown in menu. Total menu size = 1 (home) + menu_k (OOH).")
        parser.add_argument(
            "--menu_keep_home",
            default=True,
            type=self.str2bool,
            help="Always retain the home-pickup option in the displayed choice set.",
        )
        parser.add_argument(
            "--menu_use_exact_eval",
            default=True,
            type=self.str2bool,
            help="Use exact subset enumeration when the feasible bundle set is small.",
        )
        parser.add_argument(
            "--menu_exact_threshold",
            default=8,
            type=int,
            help="Maximum feasible meeting-point bundle count for exact menu enumeration.",
        )
        parser.add_argument(
            "--menu_selection_solver",
            default="auto",
            choices=["auto", "exact", "greedy"],
            help=(
                "Menu subset solver. 'auto' uses exact enumeration for small feasible sets "
                "and greedy forward selection otherwise; 'exact' forces enumeration when the "
                "candidate count is below menu_exact_threshold; 'greedy' always uses forward selection."
            ),
        )
        parser.add_argument(
            "--menu_exact_gap_threshold",
            default=8,
            type=int,
            help="Maximum non-home candidate count for logging exact-vs-greedy optimality diagnostics.",
        )
        parser.add_argument(
            "--menu_time_filtering",
            default=True,
            type=self.str2bool,
            help="Filter out bundles whose predicted pickup time falls outside the passenger's acceptable interval.",
        )
        parser.add_argument(
            "--pref_window_half_width",
            default=600.0,
            type=float,
            help="Half-width of the passenger's acceptable pickup interval in seconds.",
        )
        parser.add_argument(
            "--display_window_half_width",
            default=150.0,
            type=float,
            help="Half-width of the displayed pickup window in seconds.",
        )
        parser.add_argument(
            "--menu_window_slots_each_side",
            default=2,
            type=int,
            help="Number of candidate pickup-window centers generated on each side of the preferred pickup time.",
        )
        parser.add_argument(
            "--menu_target_arrival_time",
            default=8.5 * 3600,
            type=float,
            help="Target arrival time used to derive preferred pickup times.",
        )
        parser.add_argument(
            "--menu_pref_buffer_seconds",
            default=300.0,
            type=float,
            help="Buffer between predicted pickup and target arrival time.",
        )
        parser.add_argument(
            "--menu_pref_noise_std",
            default=60.0,
            type=float,
            help="Standard deviation of pickup-time preference noise in seconds.",
        )
        parser.add_argument(
            "--menu_travel_time_weight",
            default=-0.002,
            type=float,
            help="Passenger utility weight for predicted in-vehicle time.",
        )
        parser.add_argument(
            "--menu_pickup_time_weight",
            default=-0.0015,
            type=float,
            help="Passenger utility weight for pickup-time deviation.",
        )
        parser.add_argument(
            "--menu_score_lambda_margin",
            default=1.0,
            type=float,
            help="Weight on expected margin in fast candidate scoring.",
        )
        parser.add_argument(
            "--menu_score_lambda_walk",
            default=1.0,
            type=float,
            help="Weight on normalized walking disutility in fast candidate scoring.",
        )
        parser.add_argument(
            "--menu_score_lambda_time",
            default=1.0,
            type=float,
            help="Weight on normalized pickup-time deviation in fast candidate scoring.",
        )
        parser.add_argument(
            "--menu_score_lambda_ivt",
            default=0.5,
            type=float,
            help="Weight on normalized in-vehicle time in fast candidate scoring.",
        )
        parser.add_argument(
            "--menu_route_delay_lambda",
            default=1.0,
            type=float,
            help="Penalty weight on route-delay burden in menu-value evaluation.",
        )
        parser.add_argument(
            "--menu_capacity_risk_lambda",
            default=0.1,
            type=float,
            help="Penalty weight on low remaining-capacity risk in menu-value evaluation.",
        )
        parser.add_argument(
            "--menu_use_time_head",
            default=True,
            type=self.str2bool,
            help="Use auxiliary ETA and in-vehicle-time prediction heads.",
        )
        parser.add_argument(
            "--menu_time_prediction_blend",
            default=0.35,
            type=float,
            help="Blend weight for learned ETA/IVT heads versus heuristic proxies.",
        )
        parser.add_argument(
            "--menu_use_oracle_eta",
            default=False,
            type=self.str2bool,
            help="When True, use heuristic ETA (bypassing CNN blend) for ETA-based filtering. Proxy for oracle ETA in ablation experiments.",
        )
        parser.add_argument(
            "--menu_eta_variant",
            default="deployed",
            choices=["deployed", "heuristic", "stronger", "oracle"],
            help="ETA lane used by Phase 22 comparisons: deployed blend, heuristic-only, stronger calibrated ETA, or oracle-style filtering.",
        )
        parser.add_argument(
            "--menu_stronger_eta_gamma",
            default=0.2,
            type=float,
            help="Calibration shrinkage for the stronger ETA lane: 0=heuristic, 1=deployed blended ETA.",
        )
        parser.add_argument(
            "--menu_eta_filter_mode",
            default="hard",
            choices=["hard", "calibrated", "interval", "none"],
            help=(
                "ETA filter mode for bundle pruning. "
                "'hard': prune if eta outside [earliest, latest] (v1 default). "
                "'calibrated': prune if P(eta > latest) > 0.9 using empirical ETA std=5703s. "
                "'interval': prune if [eta-5703, eta+5703] has zero overlap with [earliest, latest]. "
                "'none': no ETA filtering (v2 default)."
            ),
        )
        parser.add_argument(
            "--menu_time_scale",
            default=3600.0,
            type=float,
            help="Normalization scale used by the ETA and in-vehicle-time heads.",
        )
        parser.add_argument(
            "--eta_scale",
            default=0.25,
            type=float,
            help="Strength of route-delay adjustment in heuristic ETA construction.",
        )

        parser.add_argument(
            "--candidate_meeting_points",
            default=8,
            type=int,
            help="Number of nearby meeting points retained before bundle construction.",
        )
        parser.add_argument("--n_vehicles", default=15, type=int, help="Number of vehicles in the fleet.")
        parser.add_argument("--veh_capacity", default=25, type=int, help="Vehicle capacity per operating day.")
        parser.add_argument(
            "--fraction_capacity_limited_meeting_points",
            default=0.38,
            type=float,
            help="Fraction of meeting points with finite capacity in loaded benchmark instances.",
        )
        parser.add_argument(
            "--meeting_point_capacity",
            default=50,
            type=int,
            help="Capacity of each capacity-limited meeting point.",
        )

        parser.add_argument(
            "--incentive_sens",
            default=-0.25,
            type=float,
            help="Passenger price-sensitivity coefficient for displayed charge adjustments.",
        )
        parser.add_argument(
            "--base_util",
            default=-2.0,
            type=float,
            help="Shared baseline utility across displayed alternatives.",
        )
        parser.add_argument(
            "--home_pickup_utility",
            default=3.2,
            type=float,
            help="Alternative-specific utility bonus for the home-pickup option.",
        )
        parser.add_argument(
            "--outside_option_util",
            default=0.0,
            type=float,
            help="Outside-option utility level in the MNL choice model. Default 0.0 normalizes the outside option; positive values make opting out more attractive.",
        )
        parser.add_argument(
            "--dissatisfaction",
            default=False,
            type=self.str2bool,
            help="Legacy dissatisfaction penalty switch retained for simulator compatibility.",
        )

        parser.add_argument(
            "--revenue",
            default=50,
            type=float,
            help="Base revenue collected when a passenger accepts service.",
        )
        parser.add_argument(
            "--menu_pricing_mode",
            default="lambertw",
            choices=["lambertw", "cost_plus", "flat_markdown"],
            help=(
                "Displayed-pricing rule for limited menus. "
                "'lambertw' uses the implemented common-offset heuristic; "
                "'cost_plus' sets price = clip(eval_cost - revenue); "
                "'flat_markdown' applies one clipped constant adjustment to every displayed bundle."
            ),
        )
        parser.add_argument(
            "--menu_pricing_constant",
            default=-3.0,
            type=float,
            help="Constant displayed charge adjustment used when menu_pricing_mode='flat_markdown'.",
        )
        parser.add_argument(
            "--max_charge_adjustment",
            default=5.0,
            type=float,
            help="Upper bound on displayed charge adjustments or surcharges.",
        )
        parser.add_argument(
            "--min_charge_adjustment",
            default=-6.0,
            type=float,
            help="Lower bound on displayed charge adjustments or discounts.",
        )
        parser.add_argument("--fuel_cost", default=0.6, type=float, help="Fuel cost coefficient per travel unit.")
        parser.add_argument("--truck_speed", default=30, type=float, help="Vehicle speed used for synthetic travel times.")
        parser.add_argument(
            "--clip_service_time",
            default=10,
            type=float,
            help="Maximum service time in minutes when generating synthetic service durations.",
        )
        parser.add_argument("--driver_wage", default=30, type=float, help="Driver wage per hour.")
        parser.add_argument(
            "--home_pickup_failure_prob",
            default=0.1,
            type=float,
            help="Failure probability assigned to the home-pickup option.",
        )
        parser.add_argument(
            "--home_pickup_failure_cost",
            default=20.0,
            type=float,
            help="Expected failure penalty applied to home pickup.",
        )
        parser.add_argument(
            "--reopt",
            default=10000000,
            type=int,
            help="Frequency of intermediate HGS route re-optimization during simulation.",
        )
        parser.add_argument(
            "--hgs_reopt_time",
            default=1.1,
            type=float,
            help="Time limit in seconds for intermediate HGS re-optimization.",
        )
        parser.add_argument(
            "--hgs_final_time",
            default=1.5,
            type=float,
            help="Time limit in seconds for final HGS route recovery at episode end.",
        )

        parser.add_argument("--gpu", default=0, type=int, help="Set to 1 to use CUDA when available, else 0 for CPU.")
        parser.add_argument("--grid_dim", default=11, type=int, help="Spatial grid dimension for the state encoder.")
        parser.add_argument("--hexa", default=False, type=self.str2bool, help="Use hexagonal cells instead of square cells.")
        parser.add_argument("--n_input_layers", default=2, type=int, help="Number of temporal layers in the state encoder.")
        parser.add_argument(
            "--only_phase_one",
            default=False,
            type=self.str2bool,
            help="Stop after the initial supervised warm-start phase.",
        )
        parser.add_argument(
            "--initial_phase_epochs",
            default=50,
            type=int,
            help="Maximum number of epochs during the initial supervised warm-start phase.",
        )
        parser.add_argument("--buffer_size", default=500, type=int, help="Replay-buffer size for supervised bundle learning.")
        parser.add_argument("--batch_size", default=256, type=int, help="Mini-batch size for predictor updates.")
        parser.add_argument("--learning_rate", default=1e-3, type=float, help="Learning rate for the shared predictor.")
        parser.add_argument(
            "--init_theta_cnn",
            default=0.75,
            type=float,
            help="Initial blend weight on routing heuristics versus learned cost prediction.",
        )
        parser.add_argument(
            "--cool_theta_cnn",
            default=(1 / 850),
            type=float,
            help="Decay applied to the heuristic-to-predictor blend weight over time.",
        )
        parser.add_argument(
            "--linearModel",
            default=False,
            type=self.str2bool,
            help="Use a linear predictor instead of a CNN-based predictor.",
        )
        parser.add_argument("--optim", default="adam", choices=["adam", "sgd", "rmsprop"], help="Optimizer type.")
        parser.add_argument(
            "--use3d_conv",
            default=False,
            type=self.str2bool,
            help="Use 3D convolution instead of 2D convolution.",
        )
        parser.add_argument("--n_filters", default=16, type=int, help="Number of filters in the first convolutional layer.")
        parser.add_argument("--dropout", default=0.05, type=float, help="Dropout rate of the fully connected layers.")

        self.parser = parser

    def finalize_args(self, args):
        args.experiment = args.experiment_name
        args.folder_suffix = args.run_suffix
        args.k = args.candidate_meeting_points
        args.parcelpoint_capacity = args.meeting_point_capacity
        args.fraction_capacitated = args.fraction_capacity_limited_meeting_points
        args.home_util = args.home_pickup_utility
        args.home_failure = args.home_pickup_failure_prob
        args.failure_cost = args.home_pickup_failure_cost
        args.max_price = args.max_charge_adjustment
        args.min_price = args.min_charge_adjustment
        args.algo_name = "DSPO_Menu"
        args.env_name = "Parcelpoint_py"
        args.menu_mode = True
        args.pricing = False
        return args

    def parse_args(self, args=None):
        return self.finalize_args(self.parser.parse_args(args=args))

    def str2bool(self, text):
        if isinstance(text, bool):
            return text
        normalized = str(text).strip().lower()
        if normalized in {"true", "1", "yes", "y"}:
            return True
        if normalized in {"false", "0", "no", "n"}:
            return False
        raise argparse.ArgumentTypeError("Boolean value expected.")

    def get_parser(self):
        return self.parser
