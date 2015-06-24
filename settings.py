import logging
import collections

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
AGE = range(10, 111, 1)
AGENTS = ['OSX', 'Windows', 'Linux', 'mobile']
LANGUAGES = ['EN', 'NL', 'GE', 'NA']
REFERERS = ['Google', 'Bing', 'NA']
CONTEXT = collections.OrderedDict([('Age', AGE), ('Agent', AGENTS), ('Language', LANGUAGES), ('Referer', REFERERS)])

# Proposal values.
AD_TYPES = ['skyscraper', 'square', 'banner']
COLORS = ['green', 'blue', 'red', 'black', 'white']
HEADERS = ['5', '15', '35']
PRODUCT_IDS = range(10, 26, 1)
PROPOSAL = collections.OrderedDict([('adtype', AD_TYPES), ('color', COLORS), ('header', HEADERS), ('productid', PRODUCT_IDS)])