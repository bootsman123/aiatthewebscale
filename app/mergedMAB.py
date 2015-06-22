__author__ = 'fenno_000'

from policies.thompsonsampling import ThompsonSampling as DefaultPolicy
#from policies.epsilongreedy import EpsilonGreedy as DefaultPolicy
from app.conversion import proposalI2S, contextNumbers, contextS2I

class MergedMAB(object):

    def __init__(self, Policy = None, **kwargs):
        self._context = []

        if Policy is None:
            Policy = DefaultPolicy

        #numberOfArms = [3,3,5,16], numberOfContextVariables = [4,4,3,102],

        self.proposalPol = Policy(**kwargs)

        self.header = 0
        self.adtype = 0
        self.color = 0
        self.productId = 0

    def propose(self, context, price = None):
           """Given a context, proposes a page
           both argument and return value in dict format

           context: ID, Agent, Language, Age, Referer"
           page: header, adtype, color, productid, price

           optionally can add a constant price to the proposal, since changing the
            price based on context is not implemented yet
           """
           self._context = context

           self.header, self.adtype, self.color, self.productId = self.proposalPol(self._context)

           proposal = {"header" : self.header, "adtype" : self.adtype, "color" : self.color, "productid" : self.productId}

           if price is not None:
               proposal["price"] = price

           return proposalI2S( proposal )

    """
    Updates all the policies with the given success (either 1 or 0).
    :param success
    """
    def update(self, success):
         self.proposalPol.update((self.header, self.adtype, self.color, self.productId), success, self._context)
