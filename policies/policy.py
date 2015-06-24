class Policy(object):
    def choose(self, context = []):
        """
        Lets the policy choose an arm given a context.
        :param context:
        :return: An arm.
        """
        pass
    	
    def update(self, arm, reward, context = []):
        """
        Updates the policy for a given arm, reward, and context.
        :param arm:
        :param reward:
        :param context:
        :return:
        """
        pass

    def arms(self):
        """
        Returns a list of arms of the policy.
        :return:
        """
        return 0

    def contexts(self):
        """
        Returns a list of context variables of the policy.
        :return:
        """
        return 0

    def name(self):
        """
        Returns the name of the policy.
        :return:
        """
        return "Policy"
