import collections


class Column(object):
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name


class Row(collections.Mapping):
    def __init__(self, columns, values):
        self.__columns = list(columns)
        self.__values = dict(values)

    def __iter__(self):
        return iter(self.__columns)

    def __len__(self):
        return len(self.__columns)

    def __getitem__(self, key):
        if isinstance(key, int):
            key = self.__columns[key]

        return self.__values[key]


class Table(collections.Sequence):
    def __init__(self, columns):
        self.__columns = list(columns)
        self.__rows = []

    def add_row(self, *args, **kwargs):
        values = {}
        for index, arg in enumerate(args):
            values[self.__columns[index].name] = arg

        values.update(kwargs)
        self.__rows.append(Row([c.name for c in self.__columns], values))

    def __len__(self):
        return len(self.__rows)

    def __getitem__(self, key):
        return self.__rows[key]

    @classmethod
    def present_simple(cls):
        pass
