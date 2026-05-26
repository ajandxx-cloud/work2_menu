from time import time

import numpy as np

import Src.Utils.Utils as Utils


class Solver:
    def __init__(self, config):
        self.config = config
        self.env = self.config.env
        self.test_env = self.config.test_env
        self.state_dim = np.shape(self.env.reset())[0]
        self.max_steps = int(config.n_vehicles * config.veh_capacity) - 1

        print("State space: {}".format(self.state_dim))

        self.model = config.algo(config=config)
        if getattr(self.config, "load_checkpoint_path", ""):
            self.model.load(self.config.load_checkpoint_path)
            # Checkpoints only store module weights, not the DSPO phase flag.
            # Evaluation should use the learned predictor heads instead of the
            # phase-one fallback policy.
            if getattr(self.config, "eval_only", False) and hasattr(self.model, "initial_phase"):
                self.model.initial_phase = False
            self.model.eval_mode()

    def train(self):
        if getattr(self.config, "eval_only", False):
            print("Skipping training because eval_only=True.")
            return

        rewards = []
        checkpoint = max(1, self.config.save_after)
        t0 = time()

        for episode in range(self.config.max_episodes):
            state = self.env.reset()
            self.model.reset()

            step = 0
            done = False
            while not done:
                action = self.model.get_action(state, training=True)
                state, done, stats, route_data = self.env.step(action=action)
                step += 1
                _ = self.model.update(route_data, state, False)
                if step >= self.max_steps or done:
                    travel_time = self.model.update(route_data, state, True)
                    rewards.append(
                        Utils.total_costs(
                            stats[1],
                            stats[2],
                            travel_time,
                            stats[3],
                            stats[6],
                            self.config,
                        )
                    )
                    break

            if episode % checkpoint == 0 or episode == self.config.max_episodes - 1:
                print("time required for " + str(checkpoint) + " episodes :" + str(time() - t0))
                Utils.plot_training_curves(rewards, self.config)
                t0 = time()

        self.model.save()
