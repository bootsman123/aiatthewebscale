from policies.thompsonsampling import ThompsonSampling
from policies.pricethompson import PriceSampling
from app.converter import Converter
import pymongo

class MultiArmedBandit(object):
    """
    Contextual multi-armed bandit.
    """

    CONTEXTS = [7,4,4,3]
    FILE_NAME = 'multiarmedbandit.clf'

    def __init__(self, settings, **kwargs):
        """
        Construct a new contextual multi-armed bandit.
        :param settings:
        """
        self._settings = settings

        # Connect to database.
        self._client = pymongo.MongoClient(self._settings.DB_HOST, self._settings.DB_PORT)
        self._database = self._client[self._settings.DB_NAME]

        self._converter = Converter(self._settings)

        # Setup policies.
        self._adTypePolicy = ThompsonSampling(arms = [len(self._settings.AD_TYPES)], contexts = MultiArmedBandit.CONTEXTS, **kwargs)
        self._colorPolicy = ThompsonSampling(arms = [len(self._settings.COLORS)], contexts = MultiArmedBandit.CONTEXTS, **kwargs)
        self._headerPolicy = ThompsonSampling(arms = [len(self._settings.HEADERS)], contexts = MultiArmedBandit.CONTEXTS, **kwargs)
        self._productIdPolicy = ThompsonSampling(arms = [len(self._settings.PRODUCT_IDS)], contexts = MultiArmedBandit.CONTEXTS, **kwargs)
        self._pricePolicy = ThompsonSampling(arms = [len(self._settings.PRICES)], contexts = MultiArmedBandit.CONTEXTS, **kwargs)
        #self._pricePolicy = PriceSampling(degree = 2)

        self._adType = 0
        self._color = 0
        self._header = 0
        self._productId = 0
        self._price = 0

        self._context = []
        self._proposal = []

    def propose(self, context):
        """
        Proposes parameters for the given context.
        :param context:
        :param price: Defaults to None.
        :return: Returns parameters.
        """
        self._context = self._converter.contextToIndices(context)

        self._adType = self._adTypePolicy.choose(self._context)[0]
        self._color = self._colorPolicy.choose(self._context)[0]
        self._header = self._headerPolicy.choose(self._context)[0]
        self._price = self._pricePolicy.choose(self._context)[0]
        self._productId = self._productIdPolicy.choose(self._context)[0]

        indices = [self._adType, self._color, self._header, self._price, self._productId]

        #indices[3] = 1
        self._proposal = self._converter.indicesToProposal(indices)
        #self._proposal['price'] = self._price

        return self._proposal

    def update(self, effect):
        """
        Updates the policies for the given effect (either success = 1 or 0).
        """
        success = effect['Success']
        reward = self._proposal['price'] * success

        self._adTypePolicy.update([self._adType], reward, self._context)
        self._colorPolicy.update([self._color], reward, self._context)
        self._headerPolicy.update([self._header], reward, self._context)
        self._pricePolicy.update([self._price], reward, self._context)
        self._productIdPolicy.update([self._productId], reward, self._context)

    def draw(self):
        """
        makes a draw for every policy. can be used for a multithreading approach, doing this while crawling the web
        """
        self._adTypePolicy.draw()
        self._colorPolicy.draw()
        self._headerPolicy.draw()
        self._pricePolicy.draw()
        self._productIdPolicy.draw()

    def save(self):
        self.save(MultiArmedBandit.FILE_NAME)

    def save(self, fileName):
        import dill

        with open(fileName, 'wb') as file:
            dill.dump(self, file)

    @staticmethod
    def load():
        return MultiArmedBandit.load(MultiArmedBandit.FILE_NAME)

    @staticmethod
    def load(fileName):
        import dill

        with open(fileName, 'rb') as file:
            return dill.load(file)

try:
   import cPickle as pickle
except:
   import pickle

'''These two functions pickle and unpickle a MAB, so that you can save the thompson sampling parameters for another run
for example, doing a single runID in multiple run.
The settings can't be saved since they are a module, but they are reassigned during the unpickle, which means nothing should happen,
as long as the settings module remains unchanged.
'''
def pickleMAB(mab, filename):
    mab._settings = None
    mab._converter = None
    with open(filename, 'wb') as output:
        pick = pickle.Pickler(output, protocol = -1)
        pick.dump(mab)

def unpickleMAB(filename, settings):
    with open(filename, 'rb') as input:
        pick = pickle.Unpickler(input)
        mab = pick.load()
    mab._settings = settings
    mab._converter = Converter(settings)
    return mab
