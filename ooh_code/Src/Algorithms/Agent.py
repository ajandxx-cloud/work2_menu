# Parent to all algorithm
from os import path
import os


class Agent:

    def __init__(self, config):      
        self.config = config

        # Abstract class variables
        self.modules = None

    def init(self):
         for name, m in self.modules:
             m.to(self.config.device)

    def clear_gradients(self):
        for _, module in self.modules:
            module.optim.zero_grad()
            
    def clear_actor_gradients(self):
        self.modules[0][1].optim.zero_grad()

    def clear_critic_gradients(self):
        self.modules[1][1].optim.zero_grad()

    def save(self):
        if self.config.save_model:
            for name, module in self.modules:
                module.save(self.config.paths['checkpoint'] + name+'.pt')

    def load(self, checkpoint_path=None):
        prefix = checkpoint_path if checkpoint_path is not None else self.config.paths['checkpoint']
        if path.isdir(prefix):
            prefix = path.join(prefix, '')
        for name, module in self.modules:
            ckpt_file = prefix + name + '.pt'
            if not os.path.exists(ckpt_file):
                continue  # Variant uses different model architecture — keep random init
            try:
                module.load(ckpt_file)
            except (RuntimeError, Exception):
                # State-dict mismatch (e.g., CNN_2d weights into CNNSetMenuNet).
                # Expected when evaluating a variant with a different menu_model.
                pass

    def train_mode(self):
        for _, module in self.modules:
            module.train()

    def eval_mode(self):
        for _, module in self.modules:
            module.eval()

    def step(self, loss, clip_norm=False):
        self.clear_gradients()
        loss.backward()
        for _, module in self.modules:
            module.step(clip_norm)
            
    def actor_step(self, loss, clip_norm=False):
        self.clear_actor_gradients()
        loss.backward()
        self.modules[0][1].step(clip_norm)
    def critic_step(self, loss, clip_norm=False):
        self.clear_actor_gradients()
        loss.backward()
        self.modules[1][1].step(clip_norm)

    def reset(self):
        for _, module in self.modules:
            module.reset()
