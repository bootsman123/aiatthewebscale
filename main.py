import configparser
import requests

# Load configuration.
config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read('configuration.ini')

# Get configuration values.
headers = [config.get('header', header) for header in config.options('header')]
adTypes = [config.get('adtype', adtype) for adtype in config.options('adtype')]
colors = [config.get('color', color) for color in config.options('color')]
productIds = range(config.getint('productid', 'min'), config.getint('productid', 'max') + 1, config.getint('productid', 'step'))
price = range(config.getint('price', 'min'), config.getint('price', 'max') + 1, config.getint('price', 'step')) # Currently only integers, while they should be floats up to 2 decimals.

# Context request.
context_params = {'i': 1,
                  'runid': 1,
                  'teamid': config.get('team', 'id'),
                  'teampw': config.get('team', 'pass')}
#request = requests.get(config.get('website', 'context_url'), params=context_params)
#json = request.json()

# Propose request.
propose_params = {'i': 1,
                  'runid': 1,
                  'teamid': config.get('team', 'id'),
                  'teampw': config.get('team', 'pass'),
                  'header': config.get('header', 'short'),
                  'adtype': config.get('adtype', 'skyscraper'),
                  'color': config.get('color', 'red'),
                  'productid': 10,
                  'price': 0.00}
#request = requests.get(config.get('website', 'propose_url'), params=propose_params)
#json = request.json()