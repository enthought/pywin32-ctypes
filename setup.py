import os
from setuptools import setup, find_packages

version = open(
    os.path.join(
        os.path.dirname(__file__),
        'win32ctypes', 'VERSION')).read().strip()
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
