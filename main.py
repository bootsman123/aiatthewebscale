import collections
import logging

import pymongo

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

converter = Converter(settings)
context = collections.OrderedDict([('Age', 19.0), ('Agent', 'OSX'), ('ID', 2576), ('Language', 'EN'), ('Referer', 'NA')])

#indices = converter.contextToIndices(context)
#print(converter.indicesToContext(indices))

crawler = Crawler(settings)
multiarmedbandit = MultiArmedBandit(settings)

price = 1
reward = 0

runId = 10

#for runId in range(10001, 10100 + 1):
for i in range(1, 5 + 1): # 100000 + 1
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
    reward = reward + effect['effect']['Success'] * price

logger.info('Total reward: {0}'.format(reward))