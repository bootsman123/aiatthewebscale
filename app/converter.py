import numpy as np
import collections

class Converter(object):
    def __init__(self, settings):
        """
        Construct a new converter with conversions defined in the settings.
        :param settings:
        :return:
        """
        self._settings = settings

    def __valuesToIndices(self, mappings, values):
        """
        Convert values to indices based on a mapping.
        :param mapping:
        :param values:
        :return:
        """
        indices = np.empty(0, dtype=np.int_)

        for key, _ in mappings.items():
            # Lookup the index of the value of the values in the map.
            index = mappings[key](values[key])

            indices = np.hstack((indices, index))

        return indices

    def __indicesToValues(self, mappings, indices):
        """
        Convert indices to values based on a mapping.
        :param mapping:
        :param indices:
        :return:
        """
        values = collections.OrderedDict()

        i = 0
        for key, _ in mappings.items():
            values[key] = mappings[key](indices[i])

            i = i + 1

        return values

    def proposalToIndices(self, proposal):
        """
        Convert proposal to indices.
        :param proposal:
        :return:
        """
        return self.__valuesToIndices(self._settings.PROPOSAL_VALUE_TO_INDEX, proposal)

    def indicesToProposal(self, indices):
        """
        Convert indices to proposal.
        :param indices:
        :return:
        """
        return self.__indicesToValues(self._settings.PROPOSAL_INDEX_TO_VALUE, indices)

    def contextToIndices(self, context):
        """
        Convert context to indices.
        :param context:
        :return:
        """
        return self.__valuesToIndices(self._settings.CONTEXT_VALUE_TO_INDEX, context)

    def indicesToContext(self, indices):
        """
        Convert indices to context.
        :param indices:
        :return:
        """
        return self.__indicesToValues(self._settings.CONTEXT_INDEX_TO_VALUE, indices)

    def contextToDummies(self, context):
        """
        Convert a context to dummy variables.
        Ignores ID of the user.
        :param context:
        :return:
        """
        dummies = np.empty(0, dtype=np.int_)

        for key, _ in self._settings.CONTEXT.items():
            # Lookup the index of the value of the context in the map.
            index = self._settings.CONTEXT[key].index(context[key])

            # Create dummy variable.
            dummy = np.zeros(len(self._settings.CONTEXT[key]))
            dummy[index] = 1

            dummies = np.hstack((dummies, dummy))

        return dummies

    def dummiesToContext(self, dummies):
        """
        Convert dummy variables to a context.
        :param dummies:
        :return:
        """
        context = collections.OrderedDict()

        start = 0
        for key, _ in self._settings.CONTEXT.items():
            end = start + len(self._settings.CONTEXT[key])

            # Extract dummy.
            dummy = dummies[start:end]
            index = np.argmax(dummy)

            context[key] = self._settings.CONTEXT[key][index]

            start = end

        return context