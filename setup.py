import os
from setuptools import setup, find_packages


HERE = os.path.dirname(__file__)
version = open(
    os.path.join(HERE, 'VERSION')).read().strip()

filename = os.path.join(HERE, 'win32ctypes', 'version.py')
with open(filename, 'w') as handle:
    handle.write(f'__version__ = "{version}"\n')

setup(
    name='pywin32-ctypes',
    version=version,
    url='https://github.com/enthought/pywin32-ctypes',
    author='Enthought Inc',
    author_email='info@enthought.com',
    packages=find_packages(),
    license="BSD",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    zip_safe=False,
    test_suite='win32ctypes.tests')
