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

    def get_metric_name(self):
        '''
        Return a string containing the full name of the metric.
        '''

        raise NotImplementedError('{}.get_metric_name'.format(type(self).__name__))
