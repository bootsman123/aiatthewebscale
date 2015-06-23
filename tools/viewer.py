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

contextNames = settings.CONTEXT.keys()
proposalNames = settings.PROPOSAL.keys()

pipeline = [
    {
        '$group':
        {
            '_id':
            {
                'context': '$context.Agent',
                'proposal': '$proposal.header'
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
cursor = db['events'].aggregate(pipeline)

nContext = 4
contextLabels = ('mobile', 'Linux', 'OSX', 'Windows')

nProposal = 3
proposalLabels = headers

data = np.zeros((nContext, nProposal))

# Iterate over cursor.



fig, ax = plt.subplots()

for index in itertools.product(range(nContext), range(nProposal)):
    element = cursor.next()
    data[index[0], index[1]] = element['success'] / element['total']

    plt.text(index[1] + 0.5, index[0] + 0.5, '%.4f' % data[index[0], index[1]],
         horizontalalignment='center',
         verticalalignment='center',
         )

heatmap = ax.pcolor(data, cmap=plt.cm.Blues)

ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor = False)
ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor = False)

ax.set_xticklabels(proposalLabels, minor = False)
ax.set_yticklabels(contextLabels, minor = False)

plt.colorbar(heatmap)
plt.show()













'''
pipeline = [
    {
        '$project':
        {
            'referer': '$context.Referer',
            'success': { '$cond': [{'$eq': ['$effect.Success', 1]}, 1, 0] },
            'failure': { '$cond': [{'$eq': ['$effect.Success', 0]}, 1, 0] },
        }
    },
    {
        '$group':
        {
            '_id': '$referer',
            'success': {'$sum': '$success'},
            'failure': {'$sum': '$failure'},
            'total': {'$sum': 1}
        }
    }
]
events = db['events'].aggregate(pipeline)

referers = []
successes = []
failures = []
totals = []

for event in events:
    referers.append(event['_id'])
    successes.append(event['success'])
    failures.append(event['failure'])
    totals.append(event['total'])

length = len(referers)
totals = np.array(totals)
successes = np.divide(np.array(successes), totals)
failures = np.divide(np.array(failures), totals)

plt.bar(np.arange(length), successes, 1.0/length, color = 'g', label = 'Success')
plt.bar(np.arange(length) + 1.0/length + 0.05, failures, 1.0/length, color = 'r', label = 'Failure')
plt.xticks(np.arange(length) + 1.0/length, referers)
plt.xlabel('Referer')
plt.ylabel('Percentage')
plt.legend()
plt.show()
'''