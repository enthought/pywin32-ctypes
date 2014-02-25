#! /bin/sh
set -e

export DISPLAY=:99.0

if [ "${TRAVIS_PYTHON_VERSION}" = "2.6" ]; then
    PYTHON_MSI="python-2.6.6.msi"
    PYTHON_URL="http://www.python.org/ftp/python/2.6.6/${PYTHON_MSI}"
    PYTHON="c:/Python26/python.exe"
    EASY_INSTALL="c:/Python26/Scripts/easy_install.exe"
    PIP="c:/Python26/Scripts/pip.exe"
elif [ "${TRAVIS_PYTHON_VERSION}" = "2.7" ]; then
    PYTHON_MSI="python-2.7.6.msi"
    PYTHON_URL="http://www.python.org/ftp/python/2.7.6/${PYTHON_MSI}"
    PYTHON="c:/Python27/python.exe"
    EASY_INSTALL="c:/Python27/Scripts/easy_install.exe"
    PIP="c:/Python27/Scripts/pip.exe"
elif [ "${TRAVIS_PYTHON_VERSION}" = "3.2" ]; then
    PYTHON_MSI="python-3.2.5.msi"
    PYTHON_URL="http://www.python.org/ftp/python/3.2.5/${PYTHON_MSI}"
    PYTHON="c:/Python32/python.exe"
    EASY_INSTALL="c:/Python32/Scripts/easy_install.exe"
    PIP="c:/Python32/Scripts/pip.exe"
elif [ "${TRAVIS_PYTHON_VERSION}" = "3.3" ]; then
    PYTHON_MSI="python-3.3.4.msi"
    PYTHON_URL="http://www.python.org/ftp/python/3.3.4/${PYTHON_MSI}"
    PYTHON="c:/Python33/python.exe"
    EASY_INSTALL="c:/Python33/Scripts/easy_install.exe"
    PIP="c:/Python33/Scripts/pip.exe"
else
    echo "Python ${TRAVIS_PYTHON_VERSION} not supported."
    exit 1;
fi

PYWIN32_EXE="pywin32-218.win32-py${TRAVIS_PYTHON_VERSION}.exe"
PYWIN32_URL="http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/pywin32-218.win32-py${TRAVIS_PYTHON_VERSION}.exe/download"

wget ${PYTHON_URL}
wine msiexec /i ${PYTHON_MSI} /qn

wget https://pypi.python.org/packages/source/s/setuptools/setuptools-2.2.tar.gz
tar xf setuptools-2.2.tar.gz
(cd setuptools-2.2 && wine ${PYTHON} setup.py install)

wine ${EASY_INSTALL} nose coverage

wget ${PYWIN32_URL} -O ${PYWIN32_EXE}

wine ${EASY_INSTALL} ${PYWIN32_EXE}
