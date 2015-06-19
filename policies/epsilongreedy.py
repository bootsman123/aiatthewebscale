from policies.policy import Policy

import numpy as np

class EpsilonGreedy(Policy):
    def __init__(self, numberOfArms, epsilonDecay = 50):
        """
        Construct a new epsilon-Greedy policy.
        :param numberOfArms: Number of arms.
        :param epsilonDecay: Decay of epsilon.
        :return:
        """
        self.n = numberOfArms
        self.counts = [0] * self.n
        self.values = [0.] * self.n
        self.decay = epsilonDecay

    def choose(self, context = []):
        if np.random.random() > self.getEpsilon():
            # Exploit.
            return np.argmax(self.values)
        else:
            # Explore.
            return np.random.randint(self.n)

    def update(self, arm, reward, context = []):
        self.counts[arm] = self.counts[arm] + 1
        n = self.counts[arm]
        value = self.values[arm]

        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.values[arm] = new_value

    def getEpsilon(self):
        total = np.sum(self.counts)
        return float(self.decay) / (total + float(self.decay))

    def numberOfArms(self):
        return self.n

    def name(self):
        return "Epsilon Greedy"