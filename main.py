import configparser
import crawler
import pymongo

import timeit

import multiarmedbandit

# Load configuration.
config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read('configuration.ini')

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
#db = client['aiatthewebscale']

cw = crawler.Crawler(config)
#users = []
mab = multiarmedbandit.MultiArmedBandit()

price = 1
reward = 0

# Timing.
start = timeit.timeit()

for i in range(1, 100001):
    if i % 10 == 0:
        print('At {0}'.format(i))

    context = cw.get(runId, i)

    proposal = mab.propose(context['context'], price=price)

    effect = cw.propose(runId, i, proposal)
    success = effect['effect']['Success']

    mab.update(success)

    reward = reward + success * price

    #user = {}
    #user['runid'] = runId
    #user['i'] = i
    #user.update(context)

    #users.append(user)

#db['users'].insert_many(users)

# Timing.
end = timeit.timeit()

print(end-start)

print('Reward: ' + reward)