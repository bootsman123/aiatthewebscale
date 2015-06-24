__author__ = 'fenno_000'

from policies.policy import Policy

import numpy as np
import numpy.polynomial.polynomial as polynomial

class PriceSampling(Policy):
    def __init__(self, degree = 2):
        """
        Construct a new Thompson Sampling policy.
        :param arms: List of arms.
        :param contexts: List of context variables.
        :return:
        """
        self.d = degree + 1

        self.B = np.eye(self.d)
        self.Binv = np.linalg.inv(self.B)
        self.mu = np.zeros(self.d)
        self.f = np.zeros(self.d)
        self.v = 1 #R * sqrt((24.0/epsilon) * self.d * log(1.0/delta))

    def choose(self, context = []):
        muc = np.random.multivariate_normal(self.mu, self.v**2.0 * self.Binv)

        roots = polynomial.polyroots(muc)
        roots = np.hstack((0.1, roots, 50))
        rewards = [polynomial.polyval(x, muc) for x in roots]
        return roots[np.argmax(rewards)]

    def update(self, arm, reward, context = []):

        b = [arm**float(x) for x in range(self.d)]

        self.B = self.B + np.outer(b, b)
        self.Binv = np.linalg.inv(self.B)
        self.f = self.f + (b * reward)
        self.mu = np.dot(self.Binv, self.f)


    def name(self):
        return "Price Thompson Sampling"
