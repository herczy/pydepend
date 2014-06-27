class Metric(object):
    '''
    Interface class for the various metrics.
    '''

    def calculate(self, node):
        '''
        Calculate the metric for the given node. A metric may be a number,
        a string or any other measurable value about the code.
        '''

        raise NotImplementedError('{}.calculate'.format(type(self).__name__))
