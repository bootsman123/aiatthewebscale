from policies.policy import Policy

import numpy as np
import numpy.random as random
from itertools import product
		
class ThompsonSampling(Policy):
    def __init__(self, arms, contexts, R = 0.5, epsilon = 0.01, delta = 0.2):
        """
        Construct a new Thompson Sampling policy.
        :param arms: List of arms.
        :param contexts: List of context variables.
        :param R:
        :param epsilon:
        :param delta:
        :return:
        """
        self.n_arms = np.array(arms)
        self.n_contexts = np.array(contexts)
        self.d = np.sum(np.outer(self.n_contexts, self.n_arms))

        self.B = np.eye(self.d)
        self.Binv = np.linalg.inv(self.B)
        self.mu = np.zeros(self.d)
        self.f = np.zeros(self.d)
        self.v = 1 #R * sqrt((24.0/epsilon) * self.d * log(1.0/delta))

    def choose(self, context = []):
        muc = random.multivariate_normal(self.mu, self.v**2.0 * self.Binv)
        rewards = np.zeros(self.n_arms)

        for i, arm in enumerate(product(*[range(arm) for arm in self.n_arms])):
            b = self.createContext(context, arm)
            rewards[arm] = np.dot(b, muc)

        return np.unravel_index(np.argmax(rewards), self.n_arms)
		
    def update(self, arm, reward, context = []):
        b = self.createContext(context, arm)
        self.B = self.B + np.outer(b, b)
        self.Binv = np.linalg.inv(self.B)
        self.f = self.f + (b * reward)
        self.mu = np.dot(self.Binv, self.f)

    def createContext(self, context, arm):
        """
        :param context: the context as an array, for example: [1,2,54,3]
        :param arm:  The arm(s) you want to choose, for example: [3,2,2,10]
        :param n_context: Maximum number of context variables, for example: [4,4,101,3]
        :param n_arm: Maximum number of arms, for example: [3,3,5,16]
        :return: An array of ordered dummy variables, 1 if the combination of arm/context is fulfilled
        """
        contextResult = np.zeros(np.sum(np.outer(self.n_arms, self.n_contexts)))
        cumsumarm = np.hstack((0, np.cumsum(np.sum(np.outer(self.n_arms, self.n_contexts), axis=0))))
        for i, a in enumerate(arm):
            armoffset = cumsumarm[i]
            cumsumcontext = np.hstack((0, np.cumsum(np.outer(self.n_arms, self.n_contexts)[i,:])))
            for j, c in enumerate(context):
                contextoffset = cumsumcontext[j]
                #print armoffset, contextoffset, i, j, a, c, "combination: ", (c, j), ",", (a, i), " : ", armoffset + contextoffset + (a*n_context[j]) + c
                contextResult[ armoffset + contextoffset + (a*self.n_contexts[j]) + c ] = 1
        return contextResult

    def arms(self):
        return self.n_arms

    def context(self):
        return self.n_contexts

    def name(self):
        return "Thompson Sampling"
