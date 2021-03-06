import logging
import timeit
import time

import numpy as np
import matplotlib.pyplot as plt

from app.crawler import Crawler
from app.multiarmedbandit import MultiArmedBandit
from app.provider import Provider

# Load settings.
import settings

# Setup logging.
logging.basicConfig(level=settings.LOG_LEVEL)
logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Setup apps.
crawler = Crawler(settings)
multiarmedbandit = MultiArmedBandit(settings) # MultiArmedBandit.load('objects/mab-without-user-10075-100000.clf')
#provider = Provider(settings)

# Range values.
runIdList = list(range(10001, 10100, 1))
iList = list(range(1, 2000, 1))

# Statistics.
rewards = np.zeros((len(runIdList), len(iList)))

# Timing.
startTime = timeit.default_timer()

for runIdIdx, runId in enumerate(runIdList):
    for iIdx, i in enumerate(iList):
        logger.info('At interaction {i} for runId {runId}'.format(i = i, runId = runId))
        #if i % 10000 == 0:
        #    # Save objects.
        #    logger.info('Saved objects')
        #    multiarmedbandit.save('objects/mab-with-user-and-polynomial-{0}-{1}.clf'.format(runId, i))
        #    np.save('objects/rewards-with-user-and-polynomial-{0}-{1}'.format(runId, i), rewards)

        # Retrieve and update context with user information.
        context = crawler.get(runId, i)
        #userContext = provider.get(context['context'])
        #context['context'].update(userContext)

        # Generate a proposal.
        proposal = multiarmedbandit.propose(context['context'])

        # Retrieve effect based on proposal.
        effect = crawler.propose(runId, i, proposal)

        # Update policies.
        multiarmedbandit.update(effect['effect'])

        # Update database.
        #provider.put(runId, i, context, proposal, effect)

        # Update statistics.
        rewards[runIdIdx, iIdx] = effect['effect']['Success'] * proposal['price']

    logger.info('Computation time for run {0}: {1}'.format(runId, time.strftime('%H:%M:%S', time.gmtime(timeit.default_timer() - startTime))))

# End timing.
logger.info('Total computation time: {}'.format(time.strftime('%H:%M:%S', time.gmtime(timeit.default_timer() - startTime))))

logger.info('Saved objects')
multiarmedbandit.save('objects/mab-with-user-and-polynomial-{0}-{1}.clf'.format(runId, i))
np.save('objects/rewards-with-user-and-polynomial-{0}-{1}'.format(runId, i), rewards)

# Output statistics.
logger.info('Total reward: {}'.format(np.sum(rewards)))
logger.info('Total mean reward over {0} runs: {1}'.format(len(runIdList), np.sum(np.mean(rewards, axis = 1))))
logger.info('Total standard deviation over {0} runs: {1}'.format(len(runIdList), np.std(rewards)))
logger.info('Mean reward per run over {0} runs: {1}'.format(len(runIdList), np.mean(rewards, axis = 1)))

# Plot statistics.
plt.plot(np.cumsum(rewards.T, axis = 0))
plt.suptitle('Reward of all runs for policy')
plt.ylabel('Cumulative reward')
plt.xlabel('Number of interactions')
plt.show()