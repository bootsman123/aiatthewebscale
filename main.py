import logging
import timeit

import pymongo
import numpy as np

from app.converter import Converter
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

#converter = Converter(settings)
#context = collections.OrderedDict([('Age', 10.0), ('Agent', 'OSX'), ('ID', 2576), ('Language', 'EN'), ('Referer', 'NA')])

#indices = converter.contextToIndices(context)
#print(indices)
#print(converter.indicesToContext(indices))

crawler = Crawler(settings)
multiarmedbandit = MultiArmedBandit(settings)

# Range values.
minRunId = 2000 # 10001
maxRunId = 2001 # 10100

minI = 1
maxI = 500 # 100000

# Statistics.
price = 1
rewards = np.zeros((maxRunId - minRunId, maxI - minI))

# Timing
startTime = timeit.default_timer()

for runId in range(minRunId, maxRunId + 1, 1):
    for i in range(minI, maxI + 1):
        logger.info('At interaction {i} for runId {runId}'.format(i = i, runId = runId))

        # Retrieve context.
        context = crawler.get(runId, i)

        # Generate a proposal.
        proposal = multiarmedbandit.propose(context['context'], price=price)

        # Retrieve effect based on proposal.
        effect = crawler.propose(runId, i, proposal)

        # Update policies.
        multiarmedbandit.update(effect['effect'])

        # Update statistics.
        rewards[runId, i] = effect['effect']['Success'] * price

# Compute statistics.
elapsedTime = timeit.default_timer() - startTime

logger.info('Total computation time: {0}'.format(elapsedTime))
logger.info('Total reward: {0}'.format(np.sum(rewards)))
logger.info('Mean reward over {0} runs: {1}'.format(maxRunId - minRunId, np.mean(rewards, axis = 1)))