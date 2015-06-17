import numpy as np

class Analyzer(object):
    def __init__(self, policy, rewards = 0, T = 10000):
        """
        Constructor.
        :param policy: Policy to analyze.
        :param rewards: Rewards for each arm (i.e., [0.1, 0.1, 0.9] for three arms).
        :param T: Time horizon (i.e., 1..T).
        :return:
        """
        self._policy = policy
        self._rewards = rewards
        self._T = T

    def analyze(self):
        """
        Analyze the policy.
        :return:
        """
        # History variables.
        arms = np.empty(self._T)
        rewards = np.empty(self._T)

        for t in range(self._T):
            # Choose arm.
            arm  = self._policy.choose_arm()

            # Compute reward.
            reward = self._rewards[arm] # Continuous.

            # Update policy.
            self._policy.update(arm, reward)

            # Update history.
            arms[t] = arm
            rewards[t] = reward

        return arms, rewards

class ContextualAnalyzer(object):
    pass