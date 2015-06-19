import configparser

import pymongo


# Load configuration.
config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read('configuration.ini')

# Get configuration values.
headers = [config.get('header', header) for header in config.options('header')]
adTypes = [config.get('adtype', adtype) for adtype in config.options('adtype')]
colors = [config.get('color', color) for color in config.options('color')]
productIds = range(config.getint('productid', 'min'), config.getint('productid', 'max') + 1, config.getint('productid', 'step'))
price = range(config.getint('price', 'min'), config.getint('price', 'max') + 1, config.getint('price', 'step')) # Currently only integers, while they should be floats up to 2 decimals.

# Connect to database.
client = pymongo.MongoClient(config.get('database', 'host'), config.getint('database', 'port'))
db = client['aiatthewebscale']

cursor = db['users'].find()
print(cursor)