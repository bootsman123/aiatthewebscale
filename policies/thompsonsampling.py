from policies.policy import Policy

import numpy as np
import numpy.random as random
from math import sqrt, log
		
class ThompsonSampling(Policy):
    def __init__(self, numberOfArms, numberOfContextVariables = 0, R = 0.05, epsilon = 0.25, delta = 0.1, ):
        """
        Construct a new Thompson Sampling policy.
        :param numberOfArms: Number of arms.
        :param numberOfContextVariables: Number of context variables.
        :param R:
        :param epsilon:
        :param delta:
        :return:
        """
        self.n = numberOfArms
        self.d = numberOfContextVariables + self.n
        self.B = np.eye(self.d)
        self.Binv = np.linalg.inv(self.B)
        self.mu = np.zeros(self.d)
        self.f = np.zeros(self.d)
        self.v = 1#R * sqrt((24.0/epsilon) * self.d * log(1.0/delta))

    def choose(self, context = []):
        muc = random.multivariate_normal(self.mu, self.v**2.0 * self.Binv)
        b = np.hstack((np.zeros(self.n), context))
        rewards = np.zeros(self.n)
        for i in range(self.n):
            b[i] = 1
            rewards[i] = np.dot(b, muc)
            b[i] = 0

        return np.argmax(rewards)
		
    def update(self, arm, reward, context = []):
        b = np.hstack((np.zeros(self.n), context))
        b[arm] = 1
        self.B = self.B + np.outer(b, b)
        self.Binv = np.linalg.inv(self.B)
        self.f = self.f + (b * reward)
        self.mu = np.dot(self.Binv, self.f)

    def numberOfArms(self):
        return self.n

    def numberOfContextVariables(self):
        return self.d - self.n

    def name(self):
        return "Thompson Sampling"
