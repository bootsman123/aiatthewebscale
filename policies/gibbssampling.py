from policies import Policy
import numpy as np
import numpy.random as random
from scipy.stats import norm
		
class GibbsSampling(Policy):
    def __init__(self , numberOfArms, numberOfContextVariables = 0):
        """
        Construct a new Gibbs Sampling policy.
        :param numberOfArms: Number of arms.
        :param numberOfContextVariables: Number of context variables.
        :return:
        """
        self.n = numberOfArms
        self.d = numberOfContextVariables + 1
        self.B = np.eye(self.d)
        self.Binv = np.linalg.inv(self.B)
        self.beta = np.zeros(self.d)
        self.y = np.zeros((0))
        self.X = np.zeros((0, self.d))

    def choose(self, context = []):
        mean = np.dot(self.B, np.dot(self.X.T, self.y ))
        self.beta = random.multivariate_normal(mean, self.B)

        b = np.hstack((context, 0))
        rewards = np.zeros(self.n)
        for i in range(self.n):
            b[-1] = i
            rewards[i] = norm.cdf(np.dot(b.T, self.beta), 0, 1)
		
        return np.argmax(rewards)
		
    def update(self, arm, reward, context = []):
        b = np.hstack((context, arm))
        self.X = np.vstack((self.X, b))
        self.Binv = self.Binv + np.dot(self.X.T, self.X)
        self.B = np.linalg.inv(self.Binv)
		
        draw = 0
        while((reward != (draw > 0)) and draw):
            draw = random.normal(np.dot(b.T, self.beta), 1)

        self.y = np.hstack((self.y, draw))

    def numberOfArms(self):
        return self.n

    def numberOfContextVariables(self):
        return self.d - 1

    def name(self):
        return "Gibbs Sampling"