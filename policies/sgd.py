__author__ = 'fenno_000'

from policies.policy import Policy

import numpy as np
import numpy.random as random
from math import sqrt, log
from sklearn.linear_model import SGDClassifier

class SGD(Policy):
    def __init__(self, numberOfArms, numberOfContextVariables = 0 ):
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
        self.model = SGDClassifier(loss = 'log')

    def choose(self, context = []):

        b = np.hstack((context, 0))
        rewards = np.zeros(self.n)
        for i in range(self.n):
            b[-1] = i
            rewards[i] = self.model.predict(b)
        return np.argmax(rewards)

    def update(self, arm, reward, context = []):
        context = np.hstack((context, arm))
        self.model.partial_fit(context, reward)

    def numberOfArms(self):
        return self.n

    def numberOfContextVariables(self):
        return self.d - 1

    def name(self):
        return "SGD Classifier Thompson"
