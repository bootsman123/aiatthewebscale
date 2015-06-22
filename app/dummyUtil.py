__author__ = 'fenno_000'

import numpy as np

def createContext(context, arm, n_context, n_arm):
    """
    :param context: the context as an array, for example: [1,2,54,3]
    :param arm:  The arm(s) you want to choose, for example: [3,2,2,10]
    :param n_context: Maximum number of context variables, for example: [4,4,101,3]
    :param n_arm: Maximum number of arms, for example: [3,3,5,16]
    :return: An array of ordered dummy variables, 1 if the combination of arm/context is fulfulled
    """

    #print context, arm, n_context, n_arm

    contextResult = np.zeros(np.sum(np.outer(n_arm, n_context)))
    cumsumarm = np.hstack((0, np.cumsum(np.sum(np.outer(n_arm, n_context), axis=0))))
    for i, a in enumerate(arm):
        armoffset = cumsumarm[i]
        cumsumcontext = np.hstack((0, np.cumsum(np.outer(n_arm, n_context)[i,:])))
        for j, c in enumerate(context):
            contextoffset = cumsumcontext[j]
            #print armoffset, contextoffset, i, j, a, c, "combination: ", (c, j), ",", (a, i), " : ", armoffset + contextoffset + (a*n_context[j]) + c
            contextResult[ armoffset + contextoffset + (a*n_context[j]) + c ] = 1
    return contextResult

if __name__ == '__main__':
    #print createContext([0,0,9,2], [0], [4,4,11,3], [3])
    #print createContext([1], [2], [5], [6])
    print createContext([5], [3], [3], [4])