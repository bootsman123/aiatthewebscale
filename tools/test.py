import numpy as np
import matplotlib.pyplot as plt

from policies.thompsonsampling import ThompsonSampling
from app.analyzer import Analyzer


# With context.
numberOfArms = 4
numberOfContextVariables = 3
payoffs = np.array([[0.25, 0.25, 0.25, 0.25], [0.7, 0.1, 0.1, 0.1], [0.1, 0.1, 0.7, 0.1]])
policy = ThompsonSampling([numberOfArms], [numberOfContextVariables])

# Without context.
'''
numberOfArms = 4
numberOfContextVariables = 0
payoffs = np.array([0.1, 0.1, 0.7, 0.1])
policy = ThompsonSampling(numberOfArms)
'''

# Run multi-armed bandit.
analyzer = Analyzer(policy, payoffs)
arms, rewards, contexts = analyzer.analyze()

# Plot arms.
colors = "bgrcmykw"
if policy.numberOfContextVariables() > 0:
    for nContext in range(policy.numberOfContextVariables()):
        contextIndices = np.argmax(contexts, axis = 1) == nContext

        plt.subplot(policy.numberOfContextVariables(), 1, nContext + 1)
        plt.title('Context {0}'.format(nContext))
        plt.hist(arms[contextIndices], bins=np.arange(policy.numberOfArms() + 1), histtype='stepfilled', color=colors[nContext])
else:
    plt.hist(arms, bins=np.arange(policy.numberOfArms() + 1))
plt.show()

# Plot accuracy:
# The probability of the policy to select the best arm.
# (Only usable in case in which you know what the best arm is.)
if policy.numberOfContextVariables() > 0:
    for nContext in range(policy.numberOfContextVariables()):
        payoffsForContext = payoffs[nContext, :]

        contextIndices = np.argmax(contexts, axis = 1) == nContext
        armsForContext = arms[contextIndices]
        armsDivider = np.array(list(range(1, len(arms) + 1)))[contextIndices]

        percentageCorrectArms = np.divide(np.cumsum(armsForContext == np.argmax(payoffsForContext)), armsDivider)

        plt.plot(armsDivider, percentageCorrectArms, label='Context {0}'.format(nContext))
else:
    percentageCorrectArms = np.divide(np.cumsum(arms == np.argmax(payoffs)), list(range(1, len(arms) + 1)))
    plt.plot(percentageCorrectArms, label='No context')

plt.suptitle('Accuracy of {0}'.format(policy.name()))
plt.ylabel('Probability of selecting best arm')
plt.xlabel('Number of interactions')
plt.legend()
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

