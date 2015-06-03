import configparser
import random
import crawler as cw
import pymongo

# Team name: Banditos
# - Training on 1 runid, and test on another runid.
# - Store data in database.

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

crawler = cw.Crawler(config)
client = pymongo.MongoClient(config.get('database', 'host'), config.getint('database', 'port'))
db = client.aiatthewebscale

for i in range(1, 5): #range(1, 100000 + 1):
    user = cw.get(runId, i)
    t = db.users.insert_one(user)
    print(t)