from policies import Policy
import numpy as np
import numpy.random as random
from scipy.stats import mvn
from scipy.stats import norm
		
class GibbsSampling(Policy):
    def __init__(self , n_arms, context_size=4):
        self.n = n_arms
        self.d = context_size + 1
        self.B = np.eye(self.d)
        self.Binv = np.linalg.inv(self.B)
        self.beta = np.zeros(self.d)
        self.y = np.zeros((0))
        self.X = np.zeros((0, self.d))

        #self.stdnormal = multivariate_normal(mean=np.zeros((self.d)), cov = np.eye(self.d))

    def choose_arm(self, context, lower=-20):
        mean = np.dot(self.B, np.dot(self.X.T, self.y ))
        self.beta = random.multivariate_normal(mean, self.B)

        b = np.hstack((context, 0))
        rewards = np.zeros(self.n)
        param = np.dot(self.X.T, self.beta)
        low = lower * np.ones((self.d))
        for i in range(self.n):
            b[-1] = i
            rewards[i], _ = mvn.mvnun(low, b, np.zeros((self.d)), np.eye(self.d))
		
        return np.argmax(rewards)
		
    def update(self, arm, context, reward):
        self.Binv = self.Binv + np.dot(self.X.T, self.X)
        self.B = np.linalg.inv(self.Binv)
        b = np.hstack((context, arm))
        self.X = np.vstack((self.X, b))
		
        draw = 0
        while((reward != (draw > 0)) and draw):
            draw = random.normal(np.dot(b.T, self.beta), 1)

        self.y = np.hstack((self.y, draw))