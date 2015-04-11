#! /bin/sh
set -e

export DISPLAY=:99.0

if [ "${TRAVIS_PYTHON_VERSION}" = "2.6" ]; then
    PYTHON_MSI="python-2.6.6.msi"
    PYTHON_URL="http://www.python.org/ftp/python/2.6.6/${PYTHON_MSI}"
    PYTHON_DIR="c:/Python26/"
    EASY_INSTALL="c:/Python26/Scripts/easy_install.exe"
    PIP="c:/Python26/Scripts/pip.exe"
    TEMP_DIR="temp26"
elif [ "${TRAVIS_PYTHON_VERSION}" = "2.7" ]; then
    PYTHON_MSI="python-2.7.6.msi"
    PYTHON_URL="http://www.python.org/ftp/python/2.7.6/${PYTHON_MSI}"
    PYTHON_DIR="c:/Python27/"
    EASY_INSTALL="c:/Python27/Scripts/easy_install.exe"
    PIP="c:/Python27/Scripts/pip.exe"
    TEMP_DIR="temp27"
elif [ "${TRAVIS_PYTHON_VERSION}" = "3.2" ]; then
    PYTHON_MSI="python-3.2.5.msi"
    PYTHON_URL="http://www.python.org/ftp/python/3.2.5/${PYTHON_MSI}"
    PYTHON_DIR="c:/Python32/"
    EASY_INSTALL="c:/Python32/Scripts/easy_install.exe"
    PIP="c:/Python32/Scripts/pip.exe"
    TEMP_DIR="temp32"
elif [ "${TRAVIS_PYTHON_VERSION}" = "3.3" ]; then
    PYTHON_MSI="python-3.3.4.msi"
    PYTHON_URL="http://www.python.org/ftp/python/3.3.4/${PYTHON_MSI}"
    PYTHON_DIR="c:/Python33/"
    EASY_INSTALL="c:/Python33/Scripts/easy_install.exe"
    PIP="c:/Python33/Scripts/pip.exe"
    TEMP_DIR="temp33"
else
    echo "Python ${TRAVIS_PYTHON_VERSION} not supported."
    exit 1;
fi

PYTHON="${PYTHON_DIR}python.exe"
PYWIN32_EXE="pywin32-218.win32-py${TRAVIS_PYTHON_VERSION}.exe"
PYWIN32_URL="http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/pywin32-218.win32-py${TRAVIS_PYTHON_VERSION}.exe/download"
PYTHON_SITE_PACKAGES="${PYTHON_DIR}/lib/site-packages"

wget ${PYTHON_URL}
wine msiexec /i ${PYTHON_MSI} /qn

wget https://pypi.python.org/packages/source/s/setuptools/setuptools-2.2.tar.gz
tar xf setuptools-2.2.tar.gz
(cd setuptools-2.2 && wine ${PYTHON} setup.py install)

wget ${PYWIN32_URL} -O ${PYWIN32_EXE}
zip -FFv ${PYWIN32_EXE} --out fixed.zip
unzip -o -qq fixed.zip -d ${TEMP_DIR}
wine xcopy /R /E /Y /I  ${TEMP_DIR}/PLATLIB ${PYTHON_SITE_PACKAGES}
wine ${PYTHON}  ${TEMP_DIR}/SCRIPTS/pywin32_postinstall.py -install

if [ "${TRAVIS_PYTHON_VERSION}" = "2.6" ]; then
    wget https://pypi.python.org/packages/source/u/unittest2/unittest2-1.0.1.tar.gz#md5=6614a229aa3619e0d11542dd8f2fd8b8
    tar -xvf unittest2-1.0.1.tar.gz
    (cd unittest2-1.0.1 && wine ${PYTHON} setup.py install)

fi
wine ${EASY_INSTALL} coverage
wine ${PYTHON} setup.py install
