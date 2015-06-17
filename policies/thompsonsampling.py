from policies import Policy
import numpy as np
import numpy.random as random
from math import sqrt, log
		
class ThompsonSampling(Policy):
    def __init__(self , n_arms, R = 1.0, epsilon = 0.5, delta = 0.1, context_size = 0):
        self.n = n_arms
        self.d = context_size + 1 # @TODO: Fugly (the number of context variables).
        self.B = np.eye(self.d)
        self.Binv = np.linalg.inv(self.B)
        self.mu = np.zeros(self.d)
        self.f = np.zeros(self.d)
        self.v = R * sqrt((24.0/epsilon) * self.d * log(1.0/delta))

    def choose_arm(self, context = []):
        muc = random.multivariate_normal(self.mu, self.v**2.0 * self.Binv)
        b = np.hstack((context, 0))
        rewards = np.zeros(self.n)
        for i in range(self.n):
            b[-1] = i
            rewards[i] = np.dot(b, muc)
		
        return np.argmax(rewards)
		
    def update(self, arm, reward, context = []):
        b = np.hstack((context, arm))
        self.B = self.B + np.outer(b, b)
        self.Binv = np.linalg.inv(self.B)
        self.f = self.f + (b * reward)
        self.mu = np.dot(self.Binv, self.f)