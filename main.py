'''
For multiarmedbandit.py, extend context (use database):
- average price until now + additional class for unseen users
- minimum price until now
- maximum price until now
- how often has the user purchased something

Questions:
- Is this per run or for all runs together?
'''

import logging
import timeit
import time

import pymongo
import numpy as np
import matplotlib.pyplot as plt

from app.crawler import Crawler
from app.multiarmedbandit import MultiArmedBandit

# Load settings.
import settings

# Setup logging.
logging.basicConfig(level=settings.LOG_LEVEL)
logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Setup apps.
crawler = Crawler(settings)
multiarmedbandit = MultiArmedBandit(settings)

# Range values.
runIdList = [4522, 8940] + list(range(10001, 10100, 1))
iList = list(range(1, 100001, 1))

# Statistics.
rewards = np.zeros((len(runIdList), len(iList)))

# Timing.
startTime = timeit.default_timer()

for runIdIdx, runId in enumerate(runIdList):
    for iIdx, i in enumerate(iList):
        logger.info('At interaction {i} for runId {runId}'.format(i = i, runId = runId))

        # Retrieve context.
        context = crawler.get(runId, i)

        # Generate a proposal.
        proposal = multiarmedbandit.propose(context['context'])

        # Retrieve effect based on proposal.
        effect = crawler.propose(runId, i, proposal)

        # Update policies.
        multiarmedbandit.update(effect['effect'])

        # Update statistics.
        rewards[runIdIdx, iIdx] = effect['effect']['Success'] * proposal['price']

# End timing.
elapsedTime = timeit.default_timer() - startTime
logger.info('Total computation time: {}'.format(time.strftime('%H:%M:%S', time.gmtime(elapsedTime))))

# Output statistics.
logger.info('Total reward: {}'.format(np.sum(rewards)))
logger.info('Total mean reward over {0} runs: {1}'.format(len(runIdList), np.sum(np.mean(rewards, axis = 1))))
logger.info('Mean reward per run over {0} runs: {1}'.format(len(runIdList), np.mean(rewards, axis = 1)))

# Plot statistics.
plt.plot(np.cumsum(rewards.T, axis = 0))
plt.suptitle('Reward of all runs for policy')
plt.ylabel('Cumulative reward')
plt.xlabel('Number of interactions')
plt.show()

'''
x = np.arange(0, maxI - minI + 1, 1)
y = np.cumsum(np.mean(rewards, axis = 0))
error = np.std(rewards, axis = 0)

plt.errorbar(x, y, yerr = error)
plt.suptitle('Error bar of mean reward for policy')
plt.ylabel('Cumulative reward')
plt.xlabel('Number of interactions')
plt.show()
'''