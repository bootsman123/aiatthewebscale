"""
The following script is intended to test different policies.
We assume a contextual multi-armed bandit problem, in which a user visits a web page k of K (i.e., context),
and chooses an action a of A (for example: to show or not to show add).

- K: Number of web pages
- A: Number of actions
- R: Reward matrix
"""

import numpy as np
import matplotlib

from policies.epsilongreedy import EpsilonGreedy
from policies.thompsonsampling import ThompsonSampling
from policies.gibbssampling import GibbsSampling

# With context.
#K = 3
#A = 4
#R = np.array([[0.25, 0.25, 0.25, 0.25], [0.7, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.7]])

# Without context.
K = 1
A = 4
R = np.array([[0.1, 0.1, 0.7, 0.1]])

T = 1000    # Horizon

# Run contextual multi-armed bandit.
policy = GibbsSampling(A, context_size=1)

# History variables.
contexts = np.empty(T)
arms = np.empty(T)
rewards = np.empty(T)

for t in range(T):
    # Generate context.
    context = np.random.choice(K)

    # Choose an arm.
    arm = policy.choose_arm([context])

    # Compute reward.
    rb = np.random.choice(A, p=R[context, :]) == arm # Discrete (binary): [0, 1]
    rd = np.random.choice(A, p=R[context, :]) # Discrete: [0..A)
    rc = R[context, arm] # Continuous.
    reward = rb

    policy.update(arm, [context], reward)

    # Update history.
    contexts[t] = context
    arms[t] = arm
    rewards[t] = reward

# Plot accuracy:
# The probability of the policy to select the best arm.
# (Only usable in case in which you know what the best arm is.)
bestArm = np.argmax(R)





# Plot performance:
# The average reward of the policy.



