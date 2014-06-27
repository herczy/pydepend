class ClassVisitor(object):
    def __init__(self):
        self.__visitors = {}
        self.__collect_visitors()

    def __collect_visitors(self):
        for attr in dir(self):
            value = getattr(self, attr)
            types = getattr(value, '__visitor__', ())
            if not types:
                continue

            for cls in types:
                self.__visitors[cls] = value

    def visit(self, value, *args, **kwargs):
        visitor = self.__get_visitor(value)
        return visitor(value, *args, **kwargs)

    def __get_visitor(self, value):
        key = type(value)

        if key not in self.__visitors:
            for cls, func in self.__visitors.items():
                if issubclass(key, cls):
                    self.__visitors[key] = func
                    break

        if key not in self.__visitors:
            return self.default

        return self.__visitors[key]

    def default(self, value, *args, **kwargs):
        raise TypeError(type(value).__name__)


def handle(*types):
    def __decorator(func):
        func.__visitor__ = types
        return func

    return __decorator
