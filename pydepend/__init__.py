from .metric import cyclomatic


class Schema(object):
    __schemas = {}

    @classmethod
    def register(cls, name, calc, helpstr):
        cls.__schemas[name] = cls(name, calc, helpstr)

    @classmethod
    def get(cls, name):
        return cls.__schemas[name]

    @classmethod
    def list(cls):
        return tuple(cls.__schemas.values())

    def __init__(self, name, calc, helpstr):
        self.__name = name
        self.__calc = calc
        self.__helpstr = helpstr

    @property
    def name(self):
        return self.__name

    @property
    def calc(self):
        return self.__calc

    @property
    def helpstr(self):
        return self.__helpstr


Schema.register('cyclomatic',
                cyclomatic.cyclomatic_complexity,
                'Cyclomatic compexity calculator')
