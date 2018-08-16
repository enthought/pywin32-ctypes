import os
from setuptools import setup, find_packages


HERE = os.path.dirname(__file__)
version = open(
    os.path.join(HERE, 'VERSION')).read().strip()

filename = os.path.join(HERE, 'win32ctypes', 'version.py')
with open(filename, 'w') as handle:
    handle.write('__version__="%s"\n' % version)

setup(
    name='pywin32-ctypes',
    version=version,
    url='https://github.com/enthought/pywin32-ctypes',
    author='Enthought Inc',
    author_email='info@enthought.com',
    packages=find_packages(),
    license="BSD",
    classifiers=[
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False,
    test_suite='win32ctypes.tests',
)
