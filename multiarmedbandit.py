#from policies.thompsonsampling import ThompsonSampling as Policy
from policies.epsilongreedy import EpsilonGreedy as DefaultPolicy
from conversion import proposalI2S, contextS2I

class MultiArmedBandit(object):
    
    def __init__(self, Policy = None):
        self._context = {}

        if Policy is None:
            Policy = DefaultPolicy

        self.headerPol = Policy(3)
        self.adtypePol = Policy(3)
        self.colorPol = Policy(5)
        self.productIdPol = Policy(16)
        
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
           
           self._context = contextS2I( context )
           
           self.header = self.headerPol.choose_arm(self._context)
           self.adtype = self.adtypePol.choose_arm(self._context)
           self.color = self.colorPol.choose_arm(self._context)
           self.productId = self.productIdPol.choose_arm(self._context)

           proposal = {"header" : self.header, "adtype" : self.adtype, "color" : self.color, "productid" : self.productId}
           
           if price is not None:
               proposal["price"] = price
           
           return proposalI2S( proposal )
           
    """
    Updates all the policies with the given success (either 1 or 0).
    :param success
    """
    def update(self, success):
         self.headerPol.update(self.header, self._context, success)
         self.adtypePol.update(self.adtype, self._context, success)
         self.colorPol.update(self.color, self._context, success)
         self.productIdPol.update(self.productId, self._context, success)
         