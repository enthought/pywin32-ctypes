#! /bin/sh
set -e

export DISPLAY=":99.0"

PYTHON="c:/Python27/python.exe"
EASY_INSTALL="c:/Python27/Scripts/easy_install.exe"
PIP="c:/Python27/Scripts/pip.exe"

wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
wget http://www.python.org/ftp/python/2.7.6/python-2.7.6.msi
wine msiexec /i python-2.7.6.msi /qn

wine ${PYTHON} ez_setup.py
wine ${EASY_INSTALL} pip
wine ${PIP} nose coverage
