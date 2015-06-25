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

# Connect to database.
client = pymongo.MongoClient(settings.DB_HOST, settings.DB_PORT)
database = client['aiatthewebscale']

# Setup apps.
crawler = Crawler(settings)
multiarmedbandit = MultiArmedBandit(settings)

# Range values.
minRunId = 2350 # 10001
maxRunId = 2353 # 10100

minI = 1
maxI = 10000 # 100000

# Statistics.
rewards = np.zeros((maxRunId - minRunId + 1, maxI - minI + 1))

# Timing.
startTime = timeit.default_timer()

for runId in range(minRunId, maxRunId + 1, 1):
    for i in range(minI, maxI + 1):
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
        rewards[runId - minRunId, i - minI] = effect['effect']['Success'] * proposal['price']

# End timing.
elapsedTime = timeit.default_timer() - startTime

# Output statistics.
logger.info('Total computation time: {0} s'.format(elapsedTime))
logger.info('Total reward: {0}'.format(np.sum(rewards)))
logger.info('Total mean reward over {0} runs: {1}'.format(maxRunId - minRunId + 1, np.sum(np.mean(rewards, axis = 1))))
logger.info('Mean reward per run over {0} runs: {1}'.format(maxRunId - minRunId + 1, np.mean(rewards, axis = 1)))

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