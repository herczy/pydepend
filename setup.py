import os.path
import sys
import glob

try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup


setup(name="pydepend",
      description="JDepend clone for Python 2 and 3",
      license="BSD",
      version='0.1',
      author="Viktor Hercinger",
      author_email="hercinger.viktor@gmail.com",
      maintainer="Viktor Hercinger",
      maintainer_email="hercinger.viktor@gmail.com",
      packages=[
        'pydepend',
        'pydepend.ext',
      ])
