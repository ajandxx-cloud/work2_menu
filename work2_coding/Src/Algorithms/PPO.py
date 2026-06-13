import numpy as np
import torch

from Src.Algorithms.Agent import Agent
from Src.Utils.Actor import Gaussian
from Src.Utils.Basis import get_Basis
from Src.Utils.Critic import Qval
from Src.Utils.Utils import get_dist_mat_HGS


class PPO(Agent):
    """Minimal Gaussian PPO-compatible policy used by run_ppo.py."""

    def __init__(self, config):
        super(PPO, self).__init__(config)
        self.load_data = config.load_data
        self.dist_matrix = config.dist_matrix
        self.state_features = get_Basis(config)
        self.action_dim = int(config.n_parcelpoints) + 1
        self.actor = Gaussian(self.state_features.feature_dim, self.action_dim, config)
        self.critic = Qval(self.state_features.feature_dim, self.action_dim, config)
        self.modules = [
            ("actor", self.actor),
            ("critic", self.critic),
            ("state_features", self.state_features),
        ]
        self.init()

    def _state_tensor(self, state):
        tensor = torch.tensor(state, dtype=torch.float32, device=self.config.device).reshape(1, -1)
        return self.state_features(tensor)

    def get_action(self, abstract_state, state, training=True):
        features = self._state_tensor(abstract_state)
        action_tensor, dist = self.actor.get_action(features, training=training)
        action = action_tensor.detach().cpu().numpy().reshape(-1)
        action = np.clip(action, self.config.min_price, self.config.max_price)
        return np.around(action, decimals=2), dist

    def update(self, s1, action, dist, reward, s2, done):
        return 0.0, 0.0

    def update_route(self, data, state, done=True):
        if not done:
            return 0.0
        if self.load_data:
            data["distance_matrix"] = get_dist_mat_HGS(self.dist_matrix, data["id"])
        result = self.config.env.utils.reopt_HGS(data)
        if isinstance(result, tuple):
            return result[1]
        return result.cost
