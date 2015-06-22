from configparser import ConfigParser
from configparser import ExtendedInterpolation
import logging
import pymongo

import itertools

from app.crawler import Crawler

# Load configuration.
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('../configuration.ini')

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

# Compute all combinations.
runId = 1

for i in range(403, 100000 + 1):
    logger.info('At interaction {i} for runId {runId}'.format(i = i, runId = runId))

    items = itertools.product(headers, adTypes, colors, productIds)
    for item in items:
        parameters = {'header': item[0], 'adtype': item[1], 'color': item[2], 'productid': item[3], 'price': 1.00}

        context = crawler.get(runId, i)
        effect = crawler.propose(runId, i, parameters)

        # Update event.
        event = {}
        event['runid'] = runId
        event['i'] = i
        event.update(context)
        event.update(effect)
        event.update({'proposal': parameters})

        db['events'].insert(event)

# Get last interaction i:
# db.getCollection('events').aggregate({$group : {_id  : "",last : {$max : "$i"}}})