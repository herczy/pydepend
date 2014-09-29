import collections

Version = collections.namedtuple('Version', ['major', 'minor', 'patch'])

PYDEPEND_VERSION = Version(0, 1, 1)
PYDEPEND_VERSION_STRING = '{}.{}.{}'.format(*PYDEPEND_VERSION)
