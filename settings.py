import logging
import collections
import numpy as np

# Team.
TEAM_ID = 'Banditos'
TEAM_PASS = 'bb7419a64fa2b8b0aa4e9ba999f13f93'

# Datebase.
DB_HOST = 'localhost'
DB_PORT = 27017

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
CONTEXT = collections.OrderedDict([('Age', (lambda value : np.digitize([value], AGES)[0] - 1, lambda index : AGES[index])),
                                   ('Agent', (lambda value : AGENTS.index(value), lambda index : AGENTS[index])),
                                   ('Language', (lambda value : LANGUAGES.index(value), lambda index : LANGUAGES[index])),
                                   ('Referer', (lambda value : REFERERS.index(value), lambda index : REFERERS[index]))])

# Proposal values.
AD_TYPES = ['skyscraper', 'square', 'banner']
COLORS = ['green', 'blue', 'red', 'black', 'white']
HEADERS = ['5', '15', '35']
PRODUCT_IDS = list(range(10, 26, 1))
PROPOSAL = collections.OrderedDict([('adtype', (lambda value : AD_TYPES.index(value), lambda index : AD_TYPES[index])),
                                    ('color', (lambda value : COLORS.index(value), lambda index : COLORS[index])),
                                    ('header', (lambda value : HEADERS.index(value), lambda index : HEADERS[index])),
                                    ('productid', (lambda value : PRODUCT_IDS.index(value), lambda index : PRODUCT_IDS[index]))])