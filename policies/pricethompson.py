__author__ = 'fenno_000'

from policies.policy import Policy

import numpy as np
from scipy.stats import multivariate_normal as mv

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

        self.muc = None

    def choose(self, context = []):

        if self.muc is None:
            self.muc = mv.rvs(self.mu, self.v**2.0 * self.Binv)

        rewardpoly = np.poly1d(self.muc)
        deriv = np.polyder(self.muc)

        roots = np.roots(deriv)
        roots = [x for x in roots if x.real == x and 0 < x and x <= 50]
        roots = np.hstack((1, roots, 50))
        rewards = [rewardpoly(x) for x in roots]
        self.muc = None
        return [roots[np.argmax(rewards)].real]

    def update(self, arm, reward, context = []):

        b = np.array([arm[0]**float(x) for x in range(self.d -1, -1, -1)])

        self.B = self.B + np.outer(b, b)
        self.Binv = np.linalg.inv(self.B)
        self.f = self.f + (b * reward)
        self.mu = np.dot(self.Binv, self.f)

    def draw(self):
        try:
            self.muc = mv.rvs(self.mu, self.v**2.0 * self.Binv)
        except np.linalg.linalg.LinAlgError:
            self.draw()


    def name(self):
        return "Price Thompson Sampling"
