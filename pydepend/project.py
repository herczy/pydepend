import ast
import os.path
import imp

from .collector import Collector


class Project(object):
    def __scan_module(self, fq_name, path=None):
        modpath = self.__resolve_module_path(fq_name, path=path)
        return self.__scan_path(modpath)

    def __resolve_module_path(self, name, path=None):
        if not isinstance(name, tuple):
            name = tuple(name.split('.'))

        assert isinstance(name, tuple)
        assert len(name) > 0

        path = path or self.__path
        modfile, pathname, description = imp.find_module(name[0], path)
        if modfile:
            modfile.close()

        submodule = name[1:]
        if not submodule:
            return pathname

        return self.__resolve_module_path(submodule, path=[pathname])

    def __scan_path(self, path):
        yield self.__get_module_name(path), path

        if os.path.isdir(path):
            for name in os.listdir(path):
                if name.startswith('__init__.'):
                    continue

                fullpath = os.path.join(path, name)
                for res in self.__scan_path(fullpath):
                    yield self.__get_module_name(fullpath), fullpath

    def __get_module_name(self, path):
        if os.path.isdir(path):
            if not os.path.isfile(os.path.join(path, '__init__.py')):
                return ()

            dirname, basename = os.path.split(path)
            return self.__get_module_name(dirname) + (basename,)

        for suffix, mode, desc in imp.get_suffixes():
            if path.endswith(suffix):
                dirname, basename = os.path.split(path)
                return self.__get_module_name(dirname) + (basename[:-len(suffix)],)

    def __init__(self, path=None):
        self.__path = list(path)
        self.__modules = {}

    def add_package(self, fq_name):
        self.__modules.update(('.'.join(module), path) for module, path in self.__scan_module(fq_name))

    @property
    def modules(self):
        return frozenset(self.__modules)

    def get_module_node(self, name):
        return Collector.collect_from_file(self.__modules[name])
