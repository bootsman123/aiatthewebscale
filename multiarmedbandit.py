
from policies import EpsilonGreedy as Policy
from conversion import proposalI2S, contextS2I

class MultiArmedBandit(object):
    
    def __init__(self):
        self.contexts = []
        self.pages = []
        self.scores = []
        
        
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
           
           context = contextS2I( context )
           
           self.header = self.headerPol.choose_arm(context, self.contexts, self.pages, self.scores)
           self.adtype = self.adtypePol.choose_arm(context, self.contexts, self.pages, self.scores)
           self.color = self.colorPol.choose_arm(context, self.contexts, self.pages, self.scores)
           self.productId = self.productIdPol.choose_arm(context, self.contexts, self.pages, self.scores)
           
           
           proposal = {"header" : self.header, "adtype" : self.adtype, "color" : self.color, "productid" : self.productId}
           self.contexts.append(context)
           self.pages.append(proposal)
           
           if price is not None:
               proposal["price"] = price
           
           return proposalI2S( proposal )
           
           
        
    def update(self, scorenum):
         """Saves the score of the previous propose call
         score should be an int"""
         self.scores.append(scorenum)
         self.headerPol.update(self.header, scorenum)
         self.adtypePol.update(self.adtype, scorenum)
         self.colorPol.update(self.color, scorenum)
         self.productIdPol.update(self.productId, scorenum)
         