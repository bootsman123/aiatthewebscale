import configparser
import pymongo
import matplotlib.pyplot as plt
import numpy as np
import itertools

# Load settings.
import settings

# Connect to database.
client = pymongo.MongoClient(settings.DB_HOST, settings.DB_PORT)
database = client['aiatthewebscale']

contextNames = ['Agent', 'Language', 'Referer']
proposalNames = ['adtype', 'color', 'header', 'productid']

for index, (contextName, proposalName) in enumerate(itertools.product(contextNames, proposalNames)):
    pipeline = [
        {
            '$group':
            {
                '_id':
                {
                    'context': '$context.{0}'.format(contextName),
                    'proposal': '$proposal.{0}'.format(proposalName)
                },
                'success': {'$sum': {'$cond': [{'$eq': ["$effect.Success", 1]}, 1, 0]}},
                'failure': {'$sum': {'$cond': [{'$eq': ["$effect.Success", 0]}, 1, 0]}},
                'total': {'$sum': 1}
            }
        },
        {
            '$sort':
            {
                '_id.context': -1,
                '_id.proposal': -1
            }
        }
    ]
    cursor = database['events'].aggregate(pipeline)

    # Get data from database.
    nContext = len(settings.CONTEXT[contextName])
    nProposal = len(settings.PROPOSAL[proposalName])
    data = np.zeros((nContext, nProposal))

    for document in cursor:
        context = settings.CONTEXT[contextName]
        proposal = settings.PROPOSAL[proposalName]

        contextIndex = context.index(document['_id']['context'])
        proposalIndex = proposal.index(document['_id']['proposal'])
        value = document['success'] / document['total']

        data[contextIndex, proposalIndex] = value

    # Plot graph.
    axes = plt.subplot(len(contextNames), len(proposalNames), index + 1)

    # Set labels for columns and rows.
    if index < len(proposalNames):
        axes.set_title(proposalName, size = 'large')

    if index % len(proposalNames) == 0:
        axes.set_ylabel(contextName, size = 'large')

    # Set individual cell values.
    if proposalName is not 'productid':
        for x in range(nContext):
            for y in range(nProposal):
                plt.text(y + 0.5, x + 0.5, '%.4f' % data[x, y],
                     horizontalalignment='center',
                     verticalalignment='center')

    heatmap = axes.pcolor(data, cmap=plt.cm.Blues)

    axes.set_xticks(np.arange(data.shape[1]) + 0.5, minor = False)
    axes.set_yticks(np.arange(data.shape[0]) + 0.5, minor = False)

    axes.set_xticklabels(settings.PROPOSAL[proposalName], minor = False)
    axes.set_yticklabels(settings.CONTEXT[contextName], minor = False)

plt.show()