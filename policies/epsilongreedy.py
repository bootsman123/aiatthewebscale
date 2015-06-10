import numpy as np
from policies.policy2 import Policy

class EpsilonGreedy(Policy):
    def __init__(self,n_arms,epsilon_decay=50):
        self.n = n_arms
        self.counts = [0] * self.n  # example: number of views
        self.values = [0.] * self.n # example: number of clicks / views
        self.decay = epsilon_decay
        

    def choose_arm(self,context, contexts, proposals, scores):
        """Choose an arm for testing"""
        epsilon = self.get_epsilon()
        if np.random.random() > epsilon:
            # Exploit (use best arm)
            return np.argmax(self.values)
        else:
            # Explore (test all arms)
            return np.random.randint(self.n)

    def update(self,arm,reward):
        """Update an arm with some reward value""" # Example: click = 1; no click = 0
        self.counts[arm] = self.counts[arm] + 1
        n = self.counts[arm]
        value = self.values[arm]
        # Running product
        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.values[arm] = new_value

    def get_epsilon(self):
        """Produce epsilon"""
        total = np.sum(self.counts)
        return float(self.decay) / (total + float(self.decay))
