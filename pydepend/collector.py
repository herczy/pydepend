import ast
import collections
import os.path

from .visitor import ClassVisitor, handle


class Node(object):
    FUNCTION = 'function'
    CLASS = 'class'

    def __init__(self, name, ast, filename):
        self.__name = name
        self.__ast = ast
        self.__filename = filename

    @property
    def name(self):
        return self.__name

    @property
    def ast(self):
        return self.__ast

    @property
    def filename(self):
        return self.__filename

    @property
    def classification(self):
        if isinstance(self.__ast, ast.FunctionDef):
            return self.FUNCTION

        elif isinstance(self.__ast, ast.ClassDef):
            return self.CLASS

        assert 0, "This should not be reachable"


class Collector(collections.Mapping):
    def __init__(self, code=None, basename=(), filename=None):
        self.__values = {}
        self.__keys = []

        if code is not None:
            if isinstance(code, str):
                code = ast.parse(code)

            for name, node in self.__collect_definitions(code).items():
                fq_name = '.'.join(basename + name)
                self.__values[fq_name] = Node(fq_name, node, filename)

            self.__keys = self.__determine_key_order()

    def __collect_definitions(self, code):
        definitions = {}
        _DefinitionCollector(definitions).visit(code)

        return definitions

    def __determine_key_order(self):
        return list(sorted(self.__values.keys(), key=lambda key: self.__values[key].ast.lineno))

    def __len__(self):
        return len(self.__values)

    def __iter__(self):
        return iter(self.__keys)

    def __getitem__(self, key):
        return self.__values[key]

    def join(self, other):
        for key, value in other.items():
            self.__values[key] = value
            self.__keys.append(key)

    @classmethod
    def __find_fq_name(cls, path):
        dirname, basename = os.path.split(os.path.normpath(path))
        name = (os.path.splitext(basename)[0],)
        if name == ('__init__',):
            name = ()

        if not os.path.isfile(os.path.join(dirname, '__init__.py')):
            return name

        return cls.__find_fq_name(dirname) + name

    @classmethod
    def load_from_path(cls, path):
        base = cls.__find_fq_name(path)

        if os.path.isfile(path):
            with open(path) as f:
                return cls(f.read(), basename=base, filename=os.path.abspath(path))

        res = cls()
        for sub in os.listdir(path):
            full = os.path.join(path, sub)

            if os.path.isfile(full):
                if os.path.splitext(full)[1] == '.py':
                    res.join(cls.load_from_path(full))

            else:
                res.join(cls.load_from_path(full))

        return res


class _DefinitionCollector(ClassVisitor):
    def __init__(self, target):
        super(_DefinitionCollector, self).__init__()

        self.__target = target
        self.__name = []

    @handle(ast.AST)
    def __visit_ast(self, node):
        for name in node._fields:
            self.visit(getattr(node, name))

    @handle(ast.FunctionDef)
    def __visit_function(self, node):
        fq_name = tuple(self.__name) + (node.name,)
        self.__target[fq_name] = node

    @handle(ast.ClassDef)
    def __visit_class(self, node):
        fq_name = tuple(self.__name) + (node.name,)
        self.__target[fq_name] = node

        self.__name.append(node.name)
        try:
            self.__visit_ast(node)

        finally:
            self.__name.pop()

    @handle(collections.Sequence)
    def __visit_sequence(self, node):
        for entry in node:
            self.visit(entry)

    @handle(str)
    def __visit_str(self, node):
        pass

    def default(self, node):
        pass
