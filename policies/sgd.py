__author__ = 'fenno_000'

from policies.policy import Policy

import numpy as np
import numpy.random as random
from math import sqrt, log
from sklearn.linear_model import SGDClassifier, SGDRegressor

class SGD(Policy):
    def __init__(self, numberOfArms, numberOfContextVariables = 0, warm_start = 50):
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
        self.d = numberOfContextVariables + 1
        self.model = SGDRegressor(loss = 'squared_loss')
        self.randomsleft = 50

    def choose(self, context = []):
        if self.randomsleft > 0 or np.random.rand() < 0.05:
            self.randomsleft -= 1
            return np.random.randint(self.n)
        b = np.hstack((np.zeros(self.n), context))
        rewards = np.zeros(self.n)
        for i in range(self.n):
            b[i] = 1
            rewards[i] = self.model.predict(b)
            b[i] = 0
            #rewards[i] = self.model.predict_proba(b.reshape(1,self.d))[0,1]
        return np.argmax(rewards)#np.random.choice(np.where(rewards == rewards.max())[0])#np.argmax(rewards)

    def update(self, arm, reward, context = []):
        #rewards = np.round(reward)
        context = np.hstack((np.zeros(self.n), context))
        context[arm] = 1
        #print context, reward
        self.model.partial_fit(np.array([context]), np.array([reward]))

    def numberOfArms(self):
        return self.n

    def numberOfContextVariables(self):
        return self.d - 1

    def name(self):
        return "SGD Classifier"
