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
    author='Enthought Inc',
    author_email='info@enthought.com',
    packages=find_packages(),
    license="BSD",
    classifiers=[
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
    ],
    use_2to3=True,
    zip_safe=False,
)
