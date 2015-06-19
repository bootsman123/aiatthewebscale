from configparser import ConfigParser
import logging

import pymongo

from app.crawler import Crawler
from app.multiarmedbandit import MultiArmedBandit



# Load configuration.
config = ConfigParser(interpolation=ConfigParser.ExtendedInterpolation())
config.read('configuration.ini')

# Setup logging.
logging.basicConfig(level=config.get('logging', 'level'))
logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Get configuration values.
headers = [config.get('header', header) for header in config.options('header')]
adTypes = [config.get('adtype', adtype) for adtype in config.options('adtype')]
colors = [config.get('color', color) for color in config.options('color')]
productIds = range(config.getint('productid', 'min'), config.getint('productid', 'max') + 1, config.getint('productid', 'step'))
price = range(config.getint('price', 'min'), config.getint('price', 'max') + 1, config.getint('price', 'step')) # Currently only integers, while they should be floats up to 2 decimals.

# Crawl pages for a given runId and interaction.
runId = 1 #random.randint(1, 1e4)

# Connect to database.
client = pymongo.MongoClient(config.get('database', 'host'), config.getint('database', 'port'))
db = client['aiatthewebscale']

crawler = Crawler(config)
multiarmedbandit = MultiArmedBandit()

price = 1
reward = 0
rewards = []

totalI = 500
for i in range(1, totalI + 1): #100001
    if i % 25 == 0:
        logger.info('At interaction {i} for runId {runId}'.format(i = i, runId = runId))

    # Retrieve context.
    context = cw.get(runId, i)

    # Generate a proposal.
    proposal = mab.propose(list(context['context'].values()), price=price)

    # Retrieve effect based on proposal.
    effect = cw.propose(runId, i, proposal)
    success = effect['effect']['Success']

    # Update policies.
    mab.update(success)

    reward = reward + success * price
    rewards.append(reward)

    # Update event.
    event = {}
    event['runid'] = runId
    event['i'] = i
    event.update(context)
    event.update(effect)
    event.update({'proposal': proposal})

    #db['events'].insert(event)

logger.info('Total interactions: {0}'.format(totalI))
logger.info('Total reward: {0}'.format(reward))

plot.plot(rewards)
plot.ylabel('Cumulative reward')
plot.xlabel('Number of interactions')
plot.show()