import requests
import collections

class Crawler(object):
    def __init__(self, config):
        """
        Initialize a new crawler.
        """
        self._config = config

    def get(self, runId, i):
        """
        Returns the context based on a run and and interaction.
        :param runId:
        :param i:
        :return: The context (ID, Agent, Language, Age, Referer).
        """
        params = {
            'runid': runId,
            'i': i,
            'teamid': self._config.get('team', 'id'),
            'teampw': self._config.get('team', 'pass')
        }
        request = requests.get(self._config.get('website', 'context_url'), params=params)
        return request.json(object_pairs_hook=collections.OrderedDict)

    def propose(self, runId, i, parameters):
        """
        'Proposes' a new page to the user for the given run and interaction, and returns the behavioral response of the user.
        :param runId:
        :param i:
        :param parameters: The parameters which influence the probability of the purchase.
        :return: The behavioral response (i.e., 1 = buy, 0 = didn't buy).
        """
        params = {
            'i': runId,
            'runid': i,
            'teamid': self._config.get('team', 'id'),
            'teampw': self._config.get('team', 'pass'),
        }
        params.update(parameters)

        request = requests.get(self._config.get('website', 'propose_url'), params=params)
        return request.json()