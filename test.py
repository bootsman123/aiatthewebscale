import numpy as np
import matplotlib.pyplot as plt

from policies.epsilongreedy import EpsilonGreedy
from policies.thompsonsampling import ThompsonSampling
from policies.gibbssampling import GibbsSampling

from analyzer import Analyzer

# With context.
numberOfArms = 4
numberOfContextVariables = 0
#payoffs = np.array([[0.25, 0.25, 0.25, 0.25], [0.7, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.7]])
payoffs = np.array([0.1, 0.1, 0.1, 0.7])
policy = GibbsSampling(numberOfArms, numberOfContextVariables)

# Without context.
'''
numberOfArms = 4
payoffs = np.array([0.1, 0.1, 0.7, 0.1])
policy = EpsilonGreedy(numberOfArms)
'''

# Run multi-armed bandit.
analyzer = Analyzer(policy, payoffs)
arms, rewards, contexts = analyzer.analyze()

# Plot accuracy:
# The probability of the policy to select the best arm.
# (Only usable in case in which you know what the best arm is.)
percentageCorrectArms = np.divide(np.cumsum(arms == np.argmax(payoffs)), list(range(1, len(arms) + 1)))

plt.plot(percentageCorrectArms)
plt.suptitle('Accuracy of policy')
plt.ylabel('Probability of selecting best arm')
plt.xlabel('Number of interactions')
plt.show()

# Plot regret:
# The regret of the policy.
'''
regret = 0

plt.plot(rewards)
plt.suptitle('Performance of policy')
plt.ylabel('Average reward')
plt.xlabel('Number of interactions')
plt.show()
'''

