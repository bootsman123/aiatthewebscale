import numpy as np

class Analyzer(object):
    def __init__(self, policy, payoffs = [], T = 10000):
        """
        Constructor.
        :param policy: Policy to analyze.
        :param payoffs: Payoffs for each arm [numberOfContextVariables, numberOfArms]
                        Example without context: [0.1, 0.1, 0.9] for three arms with no context
                        Example with context: [[0.1, 0.1, 0.9], [0.5, 0.1, 0.4]] for two contexts with three arms each.
        :param T: Time horizon (i.e., 1..T).
        :return:
        """
        self._policy = policy
        self._payoffs = np.array(payoffs)
        self._T = T

        '''
        # Check payoff matrix dimensions
        if self._payoffs.ndim == 1 and self._payoffs.shape[0] != self._policy.numberOfArms():
            raise ValueError("Invalid dimensions of the payoffs matrix. Expected ({0},), gotten ({1},).".format(self._policy.numberOfArms(),
                                                                                                                self._payoffs.shape[0]))
        elif self._payoffs.ndim == 2 and (self._payoffs.shape[0] != self._policy.numberOfContextVariables() or self._payoffs.shape[1] != self._policy.numberOfArms()):
            raise ValueError("Invalid dimensions of the payoffs matrix. Expected ({0},{1}), gotten ({2},{3}).".format(self._policy.numberOfContextVariables(),
                                                                                                                      self._policy.numberOfArms(),
                                                                                                                      self._payoffs.shape[0],
                                                                                                                      self._payoffs.shape[1]))
        elif self._payoffs.ndim != 1 and self._payoffs.ndim != 2:
            raise ValueError("Invalid dimensions of the payoffs matrix.")
        '''

    def analyze(self):
        """
        Analyze the policy.
        :return: arms, rewards, context (will be empty if no context is used)
        """
        # History variables.

        arms = np.empty(self._T)
        rewards = np.empty(self._T)
        contexts = np.empty(self._T)

        for t in range(self._T):
            if self._policy.numberOfContextVariables()[0] > 0:
                # Generate context.
                context = np.random.choice(self._policy.numberOfContextVariables()[0])

                arm = self._policy.choose([context])[0]
                reward = self._payoffs[context, arm]

                self._policy.update([arm], reward, [context])
            else:
                context = 0

                arm  = self._policy.choose()
                reward = self._payoffs[arm]

                self._policy.update(arm, reward)

            # Update history.
            arms[t] = arm
            rewards[t] = reward
            contexts[t] = context

        return arms, rewards, contexts