from policies.thompsonsampling import ThompsonSampling
from app.converter import Converter

class MultiArmedBandit(object):
    """
    Contextual multi-armed bandit.
    """
    CONTEXTS = [7, 4, 4, 3]

    def __init__(self, settings, **kwargs):
        """
        Construct a new contextual multi-armed bandit.
        :param settings:
        """
        self._settings = settings
        self._converter = Converter(self._settings)

        self._adTypePolicy = ThompsonSampling(arms = [3], contexts = MultiArmedBandit.CONTEXTS, **kwargs)
        self._colorPolicy = ThompsonSampling(arms = [5], contexts = MultiArmedBandit.CONTEXTS, **kwargs)
        self._headerPolicy = ThompsonSampling(arms = [3], contexts = MultiArmedBandit.CONTEXTS, **kwargs)
        self._productIdPolicy = ThompsonSampling(arms = [16], contexts = MultiArmedBandit.CONTEXTS, **kwargs)

        self._adType = 0
        self._header = 0
        self._color = 0
        self._productId = 0

        self._context = []

    def propose(self, context, price = 0.0):
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
        self._productId = self._productIdPolicy.choose(self._context)[0]

        indices = [self._adType, self._color, self._header, price, self._productId]
        proposal = self._converter.indicesToProposal(indices)
        proposal['price'] = price

        return proposal

    def update(self, effect):
        """
        Updates the policies for the given effect (either success = 1 or 0).
        """
        success = effect['Success']

        self._adTypePolicy.update([self._adType], success, self._context)
        self._colorPolicy.update([self._color], success, self._context)
        self._headerPolicy.update([self._header], success, self._context)
        self._productIdPolicy.update([self._productId], success, self._context)





class MergedMultiArmedBandit(object):
    """
    Merged contextual multi-armed bandit.
    """
    ARMS = [3, 5, 3, 16]
    CONTEXTS = [7, 4, 4, 3]

    def __init__(self, settings, **kwargs):
        self._settings = settings
        self._converter = Converter(self._settings)

        self._policy = ThompsonSampling(arms = MergedMultiArmedBandit.ARMS, contexts = MergedMultiArmedBandit.CONTEXTS)

        self._adType = 0
        self._color = 0
        self._header = 0
        self._productId = 0

        self._context = []

    def propose(self, context, price = None):
        self._context = context

        # @TODO: Why this order?
        self._adType, self._color, self._header, self._productId = self._policy.choose(self._context)

        indices = [self._adType, self._color, self._header, price, self._productId]
        proposal = self._converter.indicesToProposal(indices)
        proposal['price'] = price

        return proposal

    def update(self, effect):
        success = effect['Success']
        self._policy.update((self._adType, self._color, self._header, self._productId), success, self._context)