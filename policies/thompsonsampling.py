from policies.policy import Policy

import numpy as np
import numpy.random as random
from itertools import product
from app.dummyUtil import createContext
from math import sqrt, log
		
class ThompsonSampling(Policy):
    def __init__(self, numberOfArms, numberOfContextVariables, v = 1 ):
        """
        Construct a new Thompson Sampling policy.
        :param numberOfArms: Number of arms.
        :param numberOfContextVariables: Number of context variables.
        :param R:
        :param epsilon:
        :param delta:
        :return:
        """
        self.n = np.array(numberOfArms)
        self.n_context = np.array(numberOfContextVariables)
        self.d = np.sum(np.outer(self.n_context, self.n))

        self.B = np.eye(self.d)
        self.Binv = np.linalg.inv(self.B)
        self.mu = np.zeros(self.d)
        self.f = np.zeros(self.d)
        self.v = v #R * sqrt((24.0/epsilon) * self.d * log(1.0/delta))

    def choose(self, context = []):
        muc = random.multivariate_normal(self.mu, self.v**2.0 * self.Binv)
        rewards = np.zeros(self.n)

        for i, arm in enumerate(product(*[range(a) for a in self.n])):
            b = createContext(context, arm, self.n_context, self.n)
            rewards[arm] = np.dot(b, muc)

        return np.unravel_index(np.argmax(rewards), self.n)
		
    def update(self, arm, reward, context = []):

        b = createContext(context, arm, self.n_context, self.n)
        self.B = self.B + np.outer(b, b)
        self.Binv = np.linalg.inv(self.B)
        self.f = self.f + (b * reward)
        self.mu = np.dot(self.Binv, self.f)

    def numberOfArms(self):
        return self.n

    def numberOfContextVariables(self):
        return self.d

    def name(self):
        return "Thompson Sampling"
