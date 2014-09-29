from __future__ import print_function

import os
import argparse
import sys

from .plugin import PluginManager, Context
from .project import Project
from .version import PYDEPEND_VERSION_STRING


class MetricContext(list):
    def register(self, metric):
        self.append(metric)


class ReportContext(dict):
    def register(self, name, report):
        self[name] = report


def main():
    version_string = '%(prog)s {}'.format(PYDEPEND_VERSION_STRING)

    parser = argparse.ArgumentParser(description='PyDepend runner')
    parser.add_argument('-r', '--report', default='simple',
                        help='Report type (default: %(default)s)')
    parser.add_argument('-o', '--output', default=None,
                        help='Output file name (default: stdout)')
    parser.add_argument('-L', '--list-plugins', action='store_true',
                        help='List the plugins that were loaded')
    parser.add_argument('--version', action='version', version=version_string)
    parser.add_argument('packages', nargs='*', metavar='PACKAGE',
                        help='List of python packages to scan')

    context = Context()
    context.set_option('arguments', tuple(sys.argv[1:]))
    context.set_option('environment', dict(os.environ))

    manager = PluginManager()

    options = parser.parse_args(context.options['arguments'])
    context.register('parsed', options)

    manager.setup_cli_options(parser)
    install = manager.setup(context)

    context.register('metrics', MetricContext())
    context.register('reports', ReportContext())
    manager.install(context, install)

    if options.list_plugins:
        for plugin in context.plugins:
            print(plugin.get_name(), 'in', plugin.__module__)

        return 0

    project = Project()
    for package in options.packages:
        project.add_package(package)

    for metric in context.metrics:
        project.add_metric(metric)

    project.set_report(context.reports[options.report])
    if options.output is None:
        project.report()

    else:
        with open(options.output, 'w') as out:
            project.report(out)


if __name__ == '__main__':
    exit(main())
