import logging
import collections
import numpy as np

# Team.
TEAM_ID = 'Banditos'
TEAM_PASS = 'bb7419a64fa2b8b0aa4e9ba999f13f93'

# Datebase.
DB_HOST = 'localhost'
DB_PORT = 27017
DB_NAME = ''

# Logging.
LOG_LEVEL = logging.INFO

# Website.
BASE_URL = 'http://krabspin.uci.ru.nl'
CONTEXT_URL = '{0}/getcontext.json'.format(BASE_URL)
PROPOSE_URL = '{0}/proposePage.json'.format(BASE_URL)

# Context values.
AGES = [0, 9, 18, 30, 50, 65, 111, 999] # http://www.pewinternet.org/data-trend/internet-use/latest-stats/
AGENTS = ['OSX', 'Windows', 'Linux', 'mobile']
LANGUAGES = ['EN', 'NL', 'GE', 'NA']
REFERERS = ['Google', 'Bing', 'NA']
USER_BOUGHTS = [0, 1, 2] # 0 = unknown, 1 = never, 2 = at least once
USER_MINIMUM_PRICES = [0, 5, 10, 15, 20, 35, 50] # 0 = unknown
USER_MAXIMUM_PRICES = [0, 5, 10, 15, 20, 35, 50] # 0 = unknown
CONTEXT = collections.OrderedDict([('Age', AGES), ('Agent', AGENTS), ('Language', LANGUAGES), ('Referer', REFERERS)])
CONTEXT_VALUE_TO_INDEX = collections.OrderedDict([('Age', lambda value : np.digitize([value], AGES)[0] - 1),
                                                  ('Agent', lambda value : AGENTS.index(value)),
                                                  ('Language', lambda value : LANGUAGES.index(value)),
                                                  ('Referer', lambda value : REFERERS.index(value))])
CONTEXT_INDEX_TO_VALUE = collections.OrderedDict([('Age', lambda index : AGES[index]),
                                                  ('Agent', lambda index : AGENTS[index]),
                                                  ('Language', lambda index : LANGUAGES[index]),
                                                  ('Referer', lambda index : REFERERS[index])])

# Proposal values.
AD_TYPES = ['skyscraper', 'square', 'banner']
COLORS = ['green', 'blue', 'red', 'black', 'white']
HEADERS = ['5', '15', '35']
PRICES = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
PRODUCT_IDS = list(range(10, 26, 1))
PROPOSAL = collections.OrderedDict([('adtype', AD_TYPES), ('color', COLORS), ('header', HEADERS), ('price', PRICES), ('productid', PRODUCT_IDS)])
PROPOSAL_VALUE_TO_INDEX = collections.OrderedDict([('adtype', lambda value : AD_TYPES.index(value)),
                                                   ('color', lambda value : COLORS.index(value)),
                                                   ('header', lambda value : HEADERS.index(value)),
                                                   ('price', lambda value : np.digitize([value], PRICES)[0] - 1),
                                                   ('productid', lambda value : PRODUCT_IDS.index(value))])
PROPOSAL_INDEX_TO_VALUE = collections.OrderedDict([('adtype', lambda index : AD_TYPES[index]),
                                                   ('color', lambda index : COLORS[index]),
                                                   ('header', lambda index : HEADERS[index]),
                                                   ('price', lambda index : PRICES[index]),
                                                   ('productid', lambda index : PRODUCT_IDS[index])])