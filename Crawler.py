# Store in MongoDB
# users:
# - runid
# - i
# - context

import requests

class Crawler(object):
    """
    Initialize a new crawler.
    """
    def __init__(self, config):
        self._config = config

    """
    Returns the context based on a run and and interaction.
    :param runId
    :param i
    :return The context (ID, Agent, Language, Age, Referer).
    """
    def get(self, runId, i):
        params = {
            'runid': runId,
            'i': i,
            'teamid': self._config.get('team', 'id'),
            'teampw': self._config.get('team', 'pass')
        }
        request = requests.get(self._config.get('website', 'context_url'), params=params)
        return request.json()

    """
    'Proposes' a new page to the user for the given run and interaction, and returns the behavioral response of the user.
    :param runId
    :param i
    :param parameters The parameters which influence the probability of the purchase.
    :return The behavioral response (i.e., 1 = buy, 0 = didn't buy).
    """
    def propose(self, runId, i, parameters):
        params = {
            'i': runId,
            'runid': i,
            'teamid': self._config.get('team', 'id'),
            'teampw': self._config.get('team', 'pass'),
        }.update(parameters)
        request = requests.get(self._config.get('website', 'propose_url'), params=params)
        return request.json()