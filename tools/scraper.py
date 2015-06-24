from configparser import ConfigParser
from configparser import ExtendedInterpolation
import logging
import pymongo

import itertools

from app.crawler import Crawler

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
db = client['aiatthewebscale']

crawler = Crawler(settings)

# Compute all combinations.
for runId in range(10001, 10100 + 1):
    for i in range(1, 100000 + 1):
        logger.info('At interaction {i} for runId {runId}'.format(i = i, runId = runId))

        items = itertools.product(settings.HEADERS, settings.AD_TYPES, settings.COLORS, settings.PRODUCT_IDS)
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