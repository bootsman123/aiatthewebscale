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

rewards = np.array([20.0605, 14.286, 21.6325, 20.835, 21.511, 22.365, 18.4635, 11.737, 17.208, 19.215, 2.6385, 9.995, 16.2645, 17.441, 14.0165, 20.319,  20.684])
x = range(0, rewards.size, 1)
labels = [10001] + list(range(10004, 10004 + rewards.size - 1, 1))

plt.title('Mean reward per run')
plt.plot(x, rewards, 'bo-')
plt.xticks(x, labels)
plt.xlabel('Run')
plt.ylabel('Mean reward')
plt.show()


'''
pipeline = [
    {
        '$match':
        {
            'runid': 8050
        }
    },
    {
        '$group':
        {
            '_id':
            {
                        'user': '$context.ID'
            },
            'total': {'$sum': 1}
        }
    },
    {
            '$sort':
            {
                'total': 1
            }
    }
]
cursor = database['contexts'].aggregate(pipeline)

data = []
for document in cursor:
    if document['_id']['user'] != None:
        data.append(document['total'])

plt.plot(data)
plt.show()
'''

'''
# Plot all combinations of contexts and proposals to each other.
contextNames = ['Agent', 'Language', 'Referer']
proposalNames = ['adtype', 'color', 'header', 'productid']

for index, (contextName, proposalName) in enumerate(itertools.product(contextNames, proposalNames)):
    pipeline = [
        {
            '$match':
            {
                'runid': 7888
            }
        },
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
'''