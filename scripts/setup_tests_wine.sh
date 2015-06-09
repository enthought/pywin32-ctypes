#! /bin/sh
set -e

export DISPLAY=:99.0

if [ "${BITS}" = "64" ]; then
    MSI_END=".amd64.msi"
    WINE="wine64"
else
    MSI_END=".msi"
    WINE="wine"
fi

if [ "${TRAVIS_PYTHON_VERSION}" = "2.6" ]; then
    PYTHON_MSI="python-2.6.6${MSI_END}"
    PYTHON_URL="http://www.python.org/ftp/python/2.6.6/${PYTHON_MSI}"
    PYTHON_DIR="c:/Python26/"
    PYVERSION="cp26"
    TEMP_DIR="temp26"
elif [ "${TRAVIS_PYTHON_VERSION}" = "2.7" ]; then
    PYTHON_MSI="python-2.7.9${MSI_END}"
    PYTHON_URL="http://www.python.org/ftp/python/2.7.9/${PYTHON_MSI}"
    PYTHON_DIR="c:/Python27/"
    PYVERSION="cp27"
    TEMP_DIR="temp27"
elif [ "${TRAVIS_PYTHON_VERSION}" = "3.2" ]; then
    PYTHON_MSI="python-3.2.5${MSI_END}"
    PYTHON_URL="http://www.python.org/ftp/python/3.2.5/${PYTHON_MSI}"
    PYTHON_DIR="c:/Python32/"
    PYVERSION="cp32"
    TEMP_DIR="temp32"
elif [ "${TRAVIS_PYTHON_VERSION}" = "3.3" ]; then
    PYTHON_MSI="python-3.3.4${MSI_END}"
    PYTHON_URL="http://www.python.org/ftp/python/3.3.4/${PYTHON_MSI}"
    PYTHON_DIR="c:/Python33/"
    PYVERSION="cp33"
    TEMP_DIR="temp33"
elif [ "${TRAVIS_PYTHON_VERSION}" = "3.4" ]; then
    PYTHON_MSI="python-3.4.3${MSI_END}"
    PYTHON_URL="http://www.python.org/ftp/python/3.4.3/${PYTHON_MSI}"
    PYTHON_DIR="c:/Python34/"
    PYVERSION="cp34"
    TEMP_DIR="temp34"
else
    echo "Python ${TRAVIS_PYTHON_VERSION} not supported."
    exit 1;
fi

# install python
wget ${PYTHON_URL}
${WINE} msiexec /i ${PYTHON_MSI} /qn
PYTHON="${PYTHON_DIR}python.exe"

# bootstrap pip
wget https://bootstrap.pypa.io/get-pip.py
${WINE} ${PYTHON} get-pip.py
if [ "${TRAVIS_PYTHON_VERSION}" = "2.6" ]; then
   PIP="${PYTHON} -m pip.__main__"
else
   PIP="${PYTHON} -m pip"
fi
${WINE} ${PIP} --version

# install coverage
${WINE} ${PIP} install --no-binary coverage coverage

# install unittest2 (if necessary)
if [ "${TRAVIS_PYTHON_VERSION}" = "2.6" ]; then
    ${WINE} ${PIP} install unittest2
fi

# install cffi (if necessary)
if [ "${CFFI}" = "true" ]; then
    ${WINE} ${PIP} install --only-binary cffi cffi
fi

# install pywin32
if [ "${TRAVIS_PYTHON_VERSION}" = "2.6" ]; then

    PYTHON_SITE_PACKAGES="${PYTHON_DIR}/lib/site-packages"
    if [ "${BITS}" = "64" ]; then
	PYWIN32_EXE="pywin32-219.win-amd64-py${TRAVIS_PYTHON_VERSION}.exe"
	PYWIN32_URL="http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/${PYWIN32_EXE}/download"
    else
	PYWIN32_EXE="pywin32-219.win32-py${TRAVIS_PYTHON_VERSION}.exe"
	PYWIN32_URL="http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/${PYWIN32_EXE}/download"
    fi
    wget ${PYWIN32_URL} -O ${PYWIN32_EXE}
    zip -FFv ${PYWIN32_EXE} --out fixed.zip
    unzip -o -qq fixed.zip -d ${TEMP_DIR}
    ${WINE} xcopy /R /E /Y /I  ${TEMP_DIR}/PLATLIB ${PYTHON_SITE_PACKAGES}
    ${WINE} ${PYTHON} ${TEMP_DIR}/SCRIPTS/pywin32_postinstall.py -install
else
    ${WINE} ${PIP} install --only-binary pypiwin32 pypiwin32
fi

# install pywin32-ctypes
${WINE} ${PYTHON} setup.py install
