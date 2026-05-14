import os
import sys
from collections import OrderedDict

import numpy as np
import torch
from yaml import dump

import Src.Utils.Utils as Utils
from Environments.OOH.Parcelpoint_py import Parcelpoint_py
from Src.Algorithms.DSPO_Menu import DSPO_Menu


class Config:
    def __init__(self, args):
        self.paths = OrderedDict()
        self.paths["root"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        seed = args.seed
        np.random.seed(seed)
        torch.manual_seed(seed)

        self.__dict__.update(vars(args))
        self.menu_route_delay_lambda = float(args.menu_route_delay_lambda)
        self.menu_capacity_risk_lambda = float(args.menu_capacity_risk_lambda)
        self.save_after = max(1, args.max_episodes // args.save_count) if args.max_episodes > 0 else 1

        self.run_name = args.experiment + args.folder_suffix
        self.paths["outputs_root"] = os.path.join(self.paths["root"], "outputs")
        self.paths["shared_training_root"] = os.path.join(
            self.paths["outputs_root"],
            "shared_training",
            self.run_name,
            str(args.seed),
        )
        self.paths["logs"] = os.path.join(self.paths["shared_training_root"], "logs", "")
        self.paths["checkpoint"] = os.path.join(self.paths["shared_training_root"], "checkpoints", "")
        self.paths["results"] = os.path.join(self.paths["shared_training_root"], "results", "")

        for directory in self.paths.values():
            if directory != self.paths["root"]:
                os.makedirs(directory, exist_ok=True)

        with open(os.path.join(self.paths["shared_training_root"], "args.yaml"), "w", encoding="utf-8") as handle:
            dump(args.__dict__, handle, default_flow_style=False, explicit_start=True)

        sys.stdout = Utils.Logger(self.paths["logs"], args.log_output)

        if args.load_data:
            (
                self.coords,
                self.dist_matrix,
                self.n_meeting_points,
                self.adjacency,
                self.service_times,
            ) = Utils.load_demand_data(
                self.paths["root"],
                args.instance,
                args.data_seed,
                args.clip_service_time,
                args.truck_speed,
            )
            (
                self.coords_test,
                self.dist_matrix_test,
                self.n_meeting_points_test,
                self.adjacency_test,
                self.service_times_test,
            ) = Utils.load_demand_data(
                self.paths["root"],
                args.instance,
                args.data_seed_test,
                args.clip_service_time,
                args.truck_speed,
            )
        else:
            train_coords = Utils.generate_demand_data(100)
            test_coords = Utils.generate_demand_data(100)
            self.coords = train_coords
            self.dist_matrix = []
            self.n_meeting_points = 6
            self.adjacency = np.ones(6)
            self.service_times = np.ones(len(train_coords))

            self.coords_test = test_coords
            self.dist_matrix_test = []
            self.n_meeting_points_test = 6
            self.adjacency_test = np.ones(6)
            self.service_times_test = np.ones(len(test_coords))

        self.n_parcelpoints = self.n_meeting_points
        self.n_parcelpoints_test = self.n_meeting_points_test

        self.env = self.build_environment(use_test_data=False)
        self.env.seed(seed)

        self.test_env = self.build_environment(use_test_data=True)
        self.test_env.seed(seed)

        self.algo = DSPO_Menu

        if args.gpu:
            self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device("cpu")
        self.cuda = 1 if self.device.type == "cuda" else 0
        if self.cuda:
            print("Number of GPUs available: ", torch.cuda.device_count())

        if args.optim == "adam":
            self.optim = torch.optim.Adam
        elif args.optim == "rmsprop":
            self.optim = torch.optim.RMSprop
        elif args.optim == "sgd":
            self.optim = torch.optim.SGD
        else:
            raise ValueError("Undefined optimizer type")

        print("=====Configurations=====\n", args)

    def build_environment(self, use_test_data):
        coords = self.coords_test if use_test_data else self.coords
        dist_matrix = self.dist_matrix_test if use_test_data else self.dist_matrix
        n_meeting_points = self.n_meeting_points_test if use_test_data else self.n_meeting_points
        adjacency = self.adjacency_test if use_test_data else self.adjacency
        service_times = self.service_times_test if use_test_data else self.service_times

        return Parcelpoint_py(
            model=self.algo_name,
            max_steps_r=self.max_steps_r,
            max_steps_p=self.max_steps_p,
            n_vehicles=self.n_vehicles,
            veh_capacity=self.veh_capacity,
            meeting_point_capacity=self.parcelpoint_capacity,
            fraction_capacitated=self.fraction_capacitated,
            incentive_sens=self.incentive_sens,
            base_util=self.base_util,
            home_util=self.home_util,
            reopt=self.reopt,
            load_data=self.load_data,
            coords=coords,
            dist_matrix=dist_matrix,
            n_meeting_points=n_meeting_points,
            adjacency=adjacency,
            service_times=service_times,
            dissatisfaction=self.dissatisfaction,
            hgs_time=self.hgs_reopt_time,
            menu_target_arrival_time=self.menu_target_arrival_time,
            menu_pref_window_half_width=self.pref_window_half_width,
            menu_pref_buffer_seconds=self.menu_pref_buffer_seconds,
            menu_pref_noise_std=self.menu_pref_noise_std,
            menu_travel_time_weight=self.menu_travel_time_weight,
            menu_pickup_time_weight=self.menu_pickup_time_weight,
            outside_option_util=self.outside_option_util,
        )
