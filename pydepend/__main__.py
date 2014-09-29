import os
import argparse
import sys

from .plugin import PluginManager, Context
from .project import Project


class MetricContext(list):
    def register(self, metric):
        self.append(metric)


class ReportContext(dict):
    def register(self, name, report):
        self[name] = report


def main():
    parser = argparse.ArgumentParser(description='PyDepend runner')
    parser.add_argument('-r', '--report', default='simple',
                        help='Report type (default: %(default)s)')
    parser.add_argument('-o', '--output', default=None,
                        help='Output file name (default: stdout)')
    parser.add_argument('packages', nargs='+', metavar='PACKAGE',
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
