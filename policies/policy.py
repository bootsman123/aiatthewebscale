class Policy(object):
    def choose_arm(self):
        pass
    	
    def update(self, arm, reward):
        pass

class ContextualPolicy(object):
    def choose_arm(self, context):
        pass

    def update(self, arm, context, reward):
        pass