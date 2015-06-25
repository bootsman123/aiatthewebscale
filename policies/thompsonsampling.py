from policies.policy import Policy

import numpy as np
from itertools import product
from scipy.stats import multivariate_normal as mv
		
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
        self.d = np.sum(np.outer(self.n_contexts, self.n_arms)) + np.sum(self.n_contexts) + np.sum(self.n_arms) + 1

        self.B = np.eye(self.d)
        self.Binv = np.linalg.inv(self.B)
        self.mu = np.zeros(self.d)
        self.f = np.zeros(self.d)
        self.v = 1 #R * sqrt((24.0/epsilon) * self.d * log(1.0/delta))

        #These 4 variables are calculated once here, instead of over and over again for a LOT of iterations
        self._cumsumarm = np.hstack((0, np.cumsum(np.sum(np.outer(self.n_arms, self.n_contexts), axis=0))))
        self._cumsumcontext = [ np.hstack((0, np.cumsum(np.outer(self.n_arms, self.n_contexts)[i,:]))) for i in range(len(self.n_arms)) ]
        self._cumcontext = np.hstack((0, np.cumsum(self.n_contexts)))
        self._cumarms = np.hstack((0, np.cumsum(self.n_arms)))
        self.done = np.sum(np.outer(self.n_arms, self.n_contexts))
        self.dtwo = np.sum(self.n_contexts) + np.sum(self.n_arms) + 1


        self.muc = None

    def choose(self, context = []):

        if self.muc is None:
            L = np.linalg.cholesky(self.v**2.0 * self.Binv)
            norm = np.random.normal(size=self.d)
            self.muc = self.mu + np.dot(L, norm)

        rewards = np.zeros(self.n_arms)

        for i, arm in enumerate(product(*[range(arm) for arm in self.n_arms])):
            b = self.createContext(context, arm)
            rewards[arm] = np.dot(b, self.muc)

        self.muc = None
        return np.unravel_index(np.argmax(rewards), self.n_arms)
		
    def update(self, arm, reward, context = []):

        b = self.createContext(context, arm)
        self.B = self.B + np.outer(b, b)
        tempBinv = np.linalg.inv(self.B)

        x = np.sum(tempBinv)
        if np.isnan(x):
            print "Found invalid matrix, B^-1 contained nan!"
            self.B = self.B - np.outer(b,b)
            return

        self.Binv = tempBinv
        self.f = self.f + (b * reward)
        self.mu = np.dot(self.Binv, self.f)

    def createIntercept(self, context, arm):
        contextResult = np.zeros(self.dtwo)
        for i, c in enumerate(context):
            contextResult[self._cumcontext[i] + c] = 1
        for i, a in enumerate(arm):
            contextResult[np.sum(self.n_arms) + self._cumarms[i] + a] = 1
        contextResult[-1] = 1
        return contextResult

    def createContext(self, context, arm):
        """
        :param context: the context as an array, for example: [1,2,54,3]
        :param arm:  The arm(s) you want to choose, for example: [3,2,2,10]
        :param n_context: Maximum number of context variables, for example: [4,4,101,3]
        :param n_arm: Maximum number of arms, for example: [3,3,5,16]
        :return: An array of ordered dummy variables, 1 if the combination of arm/context is fulfilled
        """
        contextResult = np.zeros(self.done)
        for i, a in enumerate(arm):
            armoffset = self._cumsumarm[i]
            for j, c in enumerate(context):
                contextoffset = self._cumsumcontext[i][j]
                contextResult[ armoffset + contextoffset + (a*self.n_contexts[j]) + c ] = 1
        return np.hstack((self.createIntercept(context, arm), contextResult))

    def draw(self):
        L = np.linalg.cholesky(self.v**2.0 * self.Binv)
        norm = np.random.normal(size=self.d)
        self.muc = self.mu + np.dot(L, norm)

    def arms(self):
        return self.n_arms

    def contexts(self):
        return self.n_contexts

    def name(self):
        return "Thompson Sampling"
