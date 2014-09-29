import pydepend.version

import os.path
import sys
import glob

try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup


setup(
    name="pydepend",
    description="JDepend clone for Python 2 and 3",
    license="BSD",
    version=pydepend.version.PYDEPEND_VERSION_STRING,
    author="Viktor Hercinger",
    author_email="hercinger.viktor@gmail.com",
    maintainer="Viktor Hercinger",
    maintainer_email="hercinger.viktor@gmail.com",
    packages=[
      'pydepend',
      'pydepend.ext',
    ],
    entry_points = {
        'console_scripts': [
            'pydepend = pydepend.__main__:main',
        ],
    }
)
