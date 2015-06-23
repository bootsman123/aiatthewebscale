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

# Crawl pages for a given runId and interaction.
runId = 1 #random.randint(1, 1e4)

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
rewards = []

totalI = 200 #100001
for i in range(1, totalI + 1):
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
    reward = reward + effect['effect']['Success']

logger.info('Total interactions: {0}'.format(totalI))
logger.info('Total reward: {0}'.format(reward))