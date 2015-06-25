from policies.thompsonsampling import ThompsonSampling
from policies.pricethompson import PriceSampling
from app.converter import Converter

class MultiArmedBandit(object):
    """
    Contextual multi-armed bandit.
    """

    CONTEXTS = [7,4,4,3]

    def __init__(self, settings, **kwargs):
        """
        Construct a new contextual multi-armed bandit.
        :param settings:
        """
        self._settings = settings
        self._converter = Converter(self._settings)

        self._adTypePolicy = ThompsonSampling(arms = [len(self._settings.AD_TYPES)], contexts = MultiArmedBandit.CONTEXTS, **kwargs)
        self._colorPolicy = ThompsonSampling(arms = [len(self._settings.COLORS)], contexts = MultiArmedBandit.CONTEXTS, **kwargs)
        self._headerPolicy = ThompsonSampling(arms = [len(self._settings.HEADERS)], contexts = MultiArmedBandit.CONTEXTS, **kwargs)
        self._productIdPolicy = ThompsonSampling(arms = [len(self._settings.PRODUCT_IDS)], contexts = MultiArmedBandit.CONTEXTS, **kwargs)
        self._pricePolicy = ThompsonSampling(arms = [len(self._settings.PRICES)], contexts = MultiArmedBandit.CONTEXTS, **kwargs)

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

        self._proposal = self._converter.indicesToProposal(indices)

        return self._proposal

    def update(self, effect):
        """
        Updates the policies for the given effect (either success = 1 or 0).
        """
        success = effect['Success']
        reward = self._proposal['price'] * success

        success = reward #works much better than just success

        self._adTypePolicy.update([self._adType], success, self._context)
        self._colorPolicy.update([self._color], success, self._context)
        self._headerPolicy.update([self._header], success, self._context)
        self._pricePolicy.update([self._price], success, self._context)
        self._productIdPolicy.update([self._productId], success, self._context)

    '''
    def draw(self):
        """
        makes a draw for every policy. can be used for a multithreading approach, doing this while crawling the web
        """
        self._adTypePolicy.draw()
        self._colorPolicy.draw()
        self._headerPolicy.draw()
        self._pricePolicy.draw()
        self._productIdPolicy.draw()
    '''
