from __future__ import print_function

from math import sqrt, trunc
from os import fsync, path
from time import time
import sys

import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import float32

from Environments.OOH.containers import Fleet, Location, Vehicle


class Logger(object):
    fwrite_frequency = 1800

    def __init__(self, log_path, method):
        self.terminal = sys.stdout
        self.file = "file" in method
        self.term = "term" in method
        self.log = open(path.join(log_path, "logfile.log"), "w", encoding="utf-8")
        self.last_flush = time()

    def write(self, message):
        if self.term:
            self.terminal.write(message)

        if self.file:
            self.log.write(message)
            if (time() - self.last_flush) > self.fwrite_frequency:
                self.flush()
                self.last_flush = time()

    def flush(self):
        self.log.flush()
        fsync(self.log.fileno())


def total_costs(count_home, service_times, travel_time, discount_costs, charge_revenue, config):
    cost_multiplier = (config.driver_wage + config.fuel_cost) / 3600
    total_cost = (service_times + travel_time) * cost_multiplier + sum(discount_costs) - sum(charge_revenue)
    total_cost += count_home * config.home_failure * config.failure_cost
    return total_cost


def plot_training_curves(rewards, config):
    plt.figure()
    plt.ylabel("Monetary unit")
    plt.xlabel("Episode")
    plt.title("Training performance")
    plt.plot(rewards)
    plt.savefig(config.paths["results"] + "training_curve.png")
    plt.close()
    np.save(config.paths["results"] + "training_curve", rewards)


def sixhump_func(x, y):
    return (4 - 2.1 * x ** 2 + (x ** 4 / 3)) * x ** 2 + x * y + (-4 + 4 * y ** 2) * x ** 2 + 6


def calculate_service_time(coords, clip_service_time):
    max_xcoord = max(coords, key=lambda coord: coord.x).x
    max_ycoord = max(coords, key=lambda coord: coord.y).y
    min_xcoord = min(coords, key=lambda coord: coord.x).x
    min_ycoord = min(coords, key=lambda coord: coord.y).y
    diff_x = max_xcoord - min_xcoord
    diff_y = max_ycoord - min_ycoord

    mult_x = 6
    mult_y = 4
    service_times = np.zeros([0])
    for coord in coords:
        x1 = (((coord.x - min_xcoord) / diff_x) * mult_x) - 3
        y1 = (((coord.y - min_ycoord) / diff_y) * mult_y) - 2
        sixhump = np.around(np.clip(sixhump_func(x1, y1), 1, clip_service_time), decimals=2) * 60
        service_times = np.append(service_times, sixhump)
    return service_times


def getdistance_euclidean(a, b):
    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def load_demand_data(root_path, instance, data_seed, clip_service_time, truck_speed):
    if instance in {"Austin", "Seattle"}:
        instance_folder = "Amazon_data"
        instance_size = "_700_"
    else:
        instance_folder = "HombergerGehring_data"
        instance_size = "_90_"

    instance_root = path.join(root_path, "Environments", "OOH", instance_folder, instance)
    if not path.exists(instance_root):
        raise ValueError(f"Failed to load demand data for instance {instance}.")

    prefix = path.join(instance_root, f"{instance}{instance_size}{data_seed}")
    coords_file = prefix + "_coords.txt"
    if not path.isfile(coords_file):
        raise ValueError(f"Missing coordinate file: {coords_file}")

    raw_coords = []
    with open(coords_file, "r", encoding="utf-8") as handle:
        for idx, line in enumerate(handle):
            if line.startswith("NODE"):
                continue
            loc = line.strip().split("\t")
            raw_coords.append((float(loc[1]), float(loc[2]), idx - 1))

    # Shift Amazon (lat/lon) coordinates so all values are non-negative (required by HGS solver)
    if instance_folder == "Amazon_data":
        min_x = min(c[0] for c in raw_coords)
        min_y = min(c[1] for c in raw_coords)
        shift_x = -min_x if min_x < 0 else 0.0
        shift_y = -min_y if min_y < 0 else 0.0
        raw_coords = [(x + shift_x, y + shift_y, i) for x, y, i in raw_coords]

    coords = np.zeros([0])
    for x, y, i in raw_coords:
        coords = np.append(coords, Location(x, y, i, 0))

    dist_matrix = np.empty(shape=(0, len(coords)), dtype=int)
    if instance_folder == "Amazon_data":
        matrix_file = prefix + "_dist_matrix.txt"
        if not path.isfile(matrix_file):
            raise ValueError(f"Missing distance-matrix file: {matrix_file}")
        with open(matrix_file, "r", encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("EDGE"):
                    continue
                dist_matrix = np.vstack([dist_matrix, np.array(list(map(int, line.strip().split("\t"))))])
    else:
        for origin in coords:
            row = []
            for destination in coords:
                row.append(int(getdistance_euclidean(origin, destination)) / truck_speed * 3600)
            dist_matrix = np.vstack([dist_matrix, np.array(row)])

    if instance == "Austin":
        n_meeting_points = 278
        adjacency = np.load(prefix + "_adjacency20.npy")
    elif instance == "Seattle":
        n_meeting_points = 299
        adjacency = np.load(prefix + "_adjacency20.npy")
    else:
        n_meeting_points = 10
        adjacency = np.ones(shape=(100 - n_meeting_points, n_meeting_points))

    service_times = calculate_service_time(coords, clip_service_time)
    return coords, dist_matrix, n_meeting_points, adjacency, service_times


def generate_demand_data(dim):
    coords = np.zeros([0])
    count = 1
    for i in range(dim):
        for j in range(dim):
            coords = np.append(coords, Location(float(i), float(j), count, 0))
            count += 1
    return coords


def get_dist_mat_HGS(dist_matrix, loc_ids):
    dist_mat = dist_matrix[loc_ids]
    return dist_mat[:, loc_ids]


def get_fleet(init_route_plan, num_vehicles, vehicle_capacity):
    vehicles = np.empty(shape=(0, num_vehicles))
    for vehicle_id in range(num_vehicles):
        vehicles = np.append(vehicles, Vehicle(init_route_plan.copy(), vehicle_capacity, vehicle_id))
    return Fleet(vehicles)


def extract_route_HGS(route, data):
    fleet = get_fleet([], data["num_vehicles"], data["vehicle_capacity"])
    vehicle_idx = 0
    for route_plan in route.routes:
        for stop_idx in route_plan:
            loc = Location(
                data["x_coordinates"][stop_idx],
                data["y_coordinates"][stop_idx],
                data["id"][stop_idx],
                data["time"][stop_idx],
            )
            insert_idx = len(fleet["fleet"][vehicle_idx]["routePlan"]) - 1
            fleet["fleet"][vehicle_idx]["routePlan"].insert(insert_idx, loc)
        vehicle_idx += 1
    return fleet


def get_matrix(coords, dim, hexa=False):
    max_xcoord = max(coords, key=lambda coord: coord.x).x
    max_ycoord = max(coords, key=lambda coord: coord.y).y
    min_xcoord = min(coords, key=lambda coord: coord.x).x
    min_ycoord = min(coords, key=lambda coord: coord.y).y

    customer_cells = np.empty((0, 2), dtype=int)
    min_x = min_xcoord
    diff_x = max_xcoord - min_xcoord
    min_y = min_ycoord
    diff_y = max_ycoord - min_ycoord

    if hexa:
        gridwidth = diff_x / dim
        gridheight = diff_y / dim
        c = gridwidth / 4
        m = c / gridwidth / 2

    for coord in coords:
        row = trunc(dim * ((coord.y - min_y) / diff_y) - 1e-5)
        if hexa:
            row_is_odd = row % 2 == 1
            if row_is_odd:
                column = trunc(dim * ((coord.x - (gridwidth / 2) - min_x) / diff_x) - 1e-5)
            else:
                column = trunc(dim * ((coord.x - min_x) / diff_x) - 1e-5)
            relative_y = coord.y - (row * gridheight)
            if row_is_odd:
                relative_x = (coord.x - (column * gridwidth)) - (gridwidth / 2)
            else:
                relative_x = coord.x - (column * gridwidth)

            if relative_y < (m * relative_x) + c:
                row -= 1
                if not row_is_odd:
                    column -= 1
            elif relative_y < (-m * relative_x) - c:
                row -= 1
                if row_is_odd:
                    column += 1
        else:
            column = trunc(dim * ((coord.x - min_x) / diff_x) - 1e-5)

        customer_cells = np.vstack((customer_cells, [column, row]))
    return customer_cells


class MemoryBuffer:
    def __init__(self, max_len, time_intervals, matrix_dim, target_dim, atype, config, aux_dim=1, stype=float32):
        self.features = torch.zeros(
            (max_len, time_intervals, matrix_dim, matrix_dim),
            dtype=stype,
            requires_grad=False,
            device=config.device,
        )
        self.capacity_features = torch.zeros(
            (max_len, aux_dim),
            dtype=stype,
            requires_grad=False,
            device=config.device,
        )
        self.target = torch.zeros((max_len, target_dim), dtype=atype, requires_grad=False, device=config.device)

        self.length = 0
        self.max_len = max_len
        self.atype = atype
        self.stype = stype
        self.config = config
        self.matrix_dim = matrix_dim
        self.time_intervals = time_intervals
        self.aux_dim = aux_dim

    @property
    def size(self):
        return self.length

    def reset(self):
        self.length = 0

    def _get(self, idx):
        return self.features[idx], self.capacity_features[idx], self.target[idx]

    def batch_sample(self, batch_size, randomize=True):
        if randomize:
            indices = np.random.permutation(self.length)
        else:
            indices = np.arange(self.length)

        for ids in [indices[i:i + batch_size] for i in range(0, self.length, batch_size)]:
            yield self._get(ids)

    def sample(self, batch_size):
        count = min(batch_size, self.length)
        return self._get(np.random.choice(self.length, count))

    def add(self, features, capacity_features, target):
        matrix_dim = self.matrix_dim
        time_intervals = self.time_intervals
        if len(features) != len(target) or len(features) != len(capacity_features):
            raise ValueError("MemoryBuffer: features and target are different lengths.")
        for idx in range(len(features)):
            pos = self.length
            if self.length < self.max_len:
                self.length += 1
            else:
                pos = np.random.randint(self.max_len)

            self.features[pos] = torch.tensor(features[idx].reshape(time_intervals, matrix_dim, matrix_dim), dtype=self.stype)
            self.capacity_features[pos] = torch.tensor(
                np.asarray(capacity_features[idx]).reshape(self.aux_dim),
                dtype=self.stype,
            )
            self.target[pos] = torch.tensor(
                np.asarray(target[idx]).reshape(self.target.shape[1]),
                dtype=self.atype,
            )

    def save(self, filename):
        torch.save(self.features, filename + "feat.pt")
        torch.save(self.capacity_features, filename + "cap_feat.pt")
        torch.save(self.target, filename + "target.pt")
