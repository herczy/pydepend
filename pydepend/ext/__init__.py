from .cyclomatic import CyclomaticComplexityPlugin
from .simple import SimpleReportPlugin


BUILTIN_MODULES = [
    CyclomaticComplexityPlugin(),
    SimpleReportPlugin(),
]
