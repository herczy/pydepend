import collections


class Result(object):
    def __init__(self, name, metrics):
        self.__name = name
        self.__metrics = dict(metrics)

    @property
    def name(self):
        return self.__name

    @property
    def metrics(self):
        return dict(self.__metrics)

    def __eq__(self, other):
        return isinstance(other, Result) and self.__name == other.__name and self.__metrics == other.__metrics

    def __ne__(self, other):
        return not (self == other)

    def __stringify_metrics(self):
        return ', '.join('{!r} => {!r}'.format(k, v) for k, v in self.__metrics.items())

    def __str__(self):
        return '{}({})'.format(self.__name, self.__stringify_metrics())

    def __repr__(self):
        return '{}({}: {})'.format(type(self).__name__, self.__name, self.__stringify_metrics())


class ResultCollection(collections.Mapping):
    def __init__(self):
        self.__results = collections.OrderedDict()

    def add(self, result):
        self.__results[result.name] = result

    def __len__(self):
        return self.__results

    def __iter__(self):
        return iter(self.__results)

    def __getitem__(self, key):
        return self.__results[key]


class Report(object):
    '''
    Interface for defining reports printed to an output.
    '''

    def report(self, results):
        '''
        Report on the given reports.
        '''

        raise NotImplementedError('{}.report'.format(type(self).__name__))
