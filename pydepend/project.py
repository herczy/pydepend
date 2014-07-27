import sys
import ast
import os.path
import imp

from .collector import Collector
from .report import Result, ResultCollection


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
        module_name = self.__get_module_name(path)
        if module_name is not None:
            if os.path.isfile(path):
                yield module_name, path

            elif os.path.isdir(path) and os.path.isfile(os.path.join(path, '__init__.py')):
                yield module_name, path

                for name in os.listdir(path):
                    if name.startswith('__init__.'):
                        continue

                    fullpath = os.path.join(path, name)
                    for res in self.__scan_path(fullpath):
                        yield res

    def __get_module_name(self, path):
        if os.path.isdir(path):
            if not os.path.isfile(os.path.join(path, '__init__.py')):
                return ()

            dirname, basename = os.path.split(path)
            return self.__get_module_name(dirname) + (basename,)

        if path.endswith('.py'):
            dirname, basename = os.path.split(path)
            return self.__get_module_name(dirname) + (basename[:-3],)

    def __init__(self, path=None):
        self.__path = list(path or sys.path)
        self.__modules = {}
        self.__metrics = []
        self.__report = None

    def add_package(self, fq_name):
        self.__modules.update(('.'.join(module), path) for module, path in self.__scan_module(fq_name))

    @property
    def modules(self):
        return frozenset(self.__modules)

    @property
    def path(self):
        return tuple(self.__path)

    def get_module_node(self, name):
        return Collector.collect_from_file(self.__modules[name])

    def add_metric(self, metric):
        self.__metrics.append(metric)

    @property
    def metrics(self):
        return tuple(self.__metrics)

    def set_report(self, report):
        self.__report = report

    def report(self, stream=sys.stdout):
        results = ResultCollection()

        for name in self.__modules:
            metrics = {}
            for metric in self.__metrics:
                metrics[metric.get_metric_name()] = metric.calculate(self.get_module_node(name))

            results.add(Result(name, metrics))

        stream.write(self.__report.report(results))
