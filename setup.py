#!/usr/bin/env python

from setuptools import setup, find_packages
from os.path import abspath, dirname, join

HERE = abspath(dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    import codecs
    with codecs.open(join(HERE, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    import re    
    _file = read(*file_paths)
    _match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", _file, re.M)
    if _match:
        return _match.group(1)
    raise RuntimeError("Unable to find version string.")

if __name__ == "__main__":
    setup(
        name="stubby",
        version=find_version("stubby", "version.py"),
        author="Praveen G Shirali",
        author_email="praveengshirali@gmail.com",
        include_package_data=True,
        package_data={"stubby": ["app-context.xml"]},
        packages=find_packages(),
        entry_points='''
            [console_scripts]
            stubby=stubby.main:main
        ''',
    )
