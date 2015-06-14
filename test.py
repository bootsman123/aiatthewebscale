"""
The following script is intended to test different policies.
We assume a contextual multi-armed bandit problem, in which a user visits a web page k of K (i.e., context),
and chooses an action a of A (for example: to show or not to show add).

- K: Number of web pages
- A: Number of actions
- R: Reward matrix
"""

import numpy as np
from policies.epsilongreedy import EpsilonGreedy
from policies.thompsonsampling import ThompsonSampling

# With context.
#K = 3
#A = 4
#R = np.array([[0.25, 0.25, 0.25, 0.25], [0.7, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.7]])

# Without context.
K = 1
A = 4
R = np.array([[0.1, 0.1, 0.7, 0.1]])

N = 10000

# Run contextual multi-armed bandit.
policy = EpsilonGreedy(A)
arms = np.zeros((K, A))

for index in range(1, N + 1):
    # Generate context.
    k = np.random.choice(K)

    # Choose an arm.
    a = policy.choose_arm([k])

    # Compute reward.
    rb = np.random.choice(A, p=R[k, :]) == a # Discrete (binary): [0, 1]
    rd = np.random.choice(A, p=R[k, :]) # Discrete: [0..A)
    rc = R[k, a] # Continuous.

    policy.update(a, [k], rd)

    # Update statistics.
    arms[k, a] = arms[k, a] + 1

print('Real distribution:')
print(R)

np.set_printoptions(precision=2)
print('Summed distribution of chosen arms using a policy:')
print(np.divide(arms, np.sum(arms, axis=1).reshape(K, 1)))





