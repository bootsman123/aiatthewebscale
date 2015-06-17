import numpy as np
import matplotlib.pyplot as plt

from policies.epsilongreedy import EpsilonGreedy
from policies.thompsonsampling import ThompsonSampling

from analyzer import Analyzer

# With context.
#K = 3
#A = 4
#R = np.array([[0.25, 0.25, 0.25, 0.25], [0.7, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.7]])

# Without context.
A = 4
rewards = np.array([0.1, 0.1, 0.7, 0.1])
policy = EpsilonGreedy(A)

# Run multi-armed bandit.
analyzer = Analyzer(policy, rewards)
arms, rewards = analyzer.analyze()

# Plot accuracy:
# The probability of the policy to select the best arm.
# (Only usable in case in which you know what the best arm is.)
bestArm = np.argmax(rewards)
correctArms = arms == bestArm


plt.
plt.show()

print(np.cumsum(correctArms))




# Plot performance:
# The average reward of the policy.

