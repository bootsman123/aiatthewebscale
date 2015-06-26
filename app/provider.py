import pymongo

class Provider(object):
    def __init__(self, settings):
        self._settings = settings
        self._client = pymongo.MongoClient(self._settings.DB_HOST, self._settings.DB_PORT)
        self._database = self._client[settings.DB_NAME]

    def get(self, context):
        """
        Get additional variables for the given context.
        :param context:
        :return:
        """
        pipeline = [
            {
                '$match':
                {
                    'context.ID': context['ID']
                }
            },
            {
                '$project':
                {
                    'price': {'$multiply': ['$effect.Success', '$proposal.price']}
                }
            },
            {
                '$group':
                {
                    '_id': None,
                    'UserAveragePrice': {'$avg': '$price'},
                    #'UserMinimumPrice': {'$min': '$price'},
                    #'UserMaximumPrice': {'$max': '$price'},
                    'UserTotalPurchases': {'$sum': 1}
                }
            }
        ]
        userContext = list(self._database[self._settings.DB_COLLECTION].aggregate(pipeline))

        if len(userContext) == 0:
            return {'UserAveragePrice': self._settings.UNKNOWN_VALUE,
                    #'UserMaximumPrice': self._settings.UNKNOWN_VALUE,
                    #'UserMinimumPrice': self._settings.UNKNOWN_VALUE,
                    'UserTotalPurchases': self._settings.UNKNOWN_VALUE}
        else:
            userContext = userContext[0]
            userContext['UserTotalPurchases'] = min(userContext['UserTotalPurchases'], 1)
            return userContext

    def put(self, runId, i, context, proposal, effect):
        """
        Put data into the database.
        :param runId:
        :param i:
        :param context:
        :param proposal:
        :param effect:
        :return:
        """
        event = {}
        event['runid'] = runId
        event['i'] = i
        event.update(context)
        event.update(effect)
        event.update({'proposal': proposal})

        self._database[self._settings.DB_COLLECTION].insert(event)

