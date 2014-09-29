from pydepend.plugin import Plugin
from pydepend.report import Report


class SimpleReport(Report):
    def report(self, results):
        res = []
        for result in results.values():
            metrics = ', '.join('{} = {}'.format(k, v) for k, v in sorted(result.metrics.items()))
            res.append('{}: {}'.format(result.name, metrics))

        res.append('')

        return '\n'.join(res)


class SimpleReportPlugin(Plugin):
    def install(self, context):
        context.reports.register('simple', SimpleReport())
