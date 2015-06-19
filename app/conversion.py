
headerMap = { 5 : 0, 15 : 1, 35 : 2}
adtypeMap = { "skyscraper" : 0, "square" : 1, "banner" : 2}
colorMap = {"green" : 0, "blue" : 1, "red" : 2, "black" : 3, "white" : 4}
productIdMap = {x : x - 10 for x in range(10,26)}

proposalNames = {"header" : headerMap, "adtype" : adtypeMap, "color" : colorMap, "productid" : productIdMap}

agentMap = {"OSX" : 0, "Windows" : 1, "Linux" : 2, "mobile" : 3}
languageMap = {"EN" : 0, "NL" : 1, "GE" : 2, "NA" : 3}
ageMap = {x : x - 10 for x in range(10,111 )}
ageMap.update({999 : 101})
refererMap = {"Google" : 0, "Bing" : 1, "NA" : 2}

contextNames = {"Agent" : agentMap, "Language" : languageMap, "Age" : ageMap, "Referer" : refererMap}

invertMap = lambda mapping : {v: k for k, v in mapping.items()}

def proposalS2I(proposal):
    """Takes a proposal, and updates the header, adtype,color, and productid to change them from string to int"""
    newProposal = {name : proposalNames[name][proposal[name]] for name in proposalNames.keys()}
    result = proposal.copy()
    result.update(newProposal)
    return result

def proposalI2S(proposal):
    """Takes a proposal, and updates the header, adtype,color, and productid to change them from string to int"""
    newProposal = {name: invertMap(proposalNames[name])[proposal[name]] for name in proposalNames.keys()}
    result = proposal.copy()
    result.update(newProposal)
    return result
    
def contextS2I(context):
    """Takes a context, and updates the agent, language, age and referer from string to int"""
    newContext = {name : contextNames[name][context[name]] for name in contextNames.keys()}
    result = context.copy()
    result.update(newContext)
    return result

def contextI2S(context):
    """Takes a context, and updates the agent, language, age and referer from int to string"""
    newContext = {name: invertMap(contextNames[name])[context[name]] for name in contextNames.keys()}
    result = context.copy()
    result.update(newContext)
    return result
    
    
