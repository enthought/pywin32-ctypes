#! /bin/sh
set -e

export DISPLAY=:99.0

if [ "${BITS}" = "64" ]; then
    WINE="wine64"
else
    WINE="wine"
fi


if [ "${TRAVIS_PYTHON_VERSION}" = "2.6" ]; then
    PYTHON_DIR="c:/Python26/"
elif [ "${TRAVIS_PYTHON_VERSION}" = "2.7" ]; then
    PYTHON_DIR="c:/Python27/"
elif [ "${TRAVIS_PYTHON_VERSION}" = "3.2" ]; then
    PYTHON_DIR="c:/Python32/"
elif [ "${TRAVIS_PYTHON_VERSION}" = "3.3" ]; then
    PYTHON_DIR="c:/Python33/"
elif [ "${TRAVIS_PYTHON_VERSION}" = "3.4" ]; then
    PYTHON_DIR="c:/Python34/"
else
    echo "Python ${TRAVIS_PYTHON_VERSION} not supported."
    exit 1;
fi

PYTHON="${PYTHON_DIR}python.exe"
if [ "${TRAVIS_PYTHON_VERSION}" = "2.6" ]; then
   PIP="${PYTHON} -m pip.__main__"
else
   PIP="${PYTHON} -m pip"
fi
COVERAGE="${PYTHON_DIR}/scripts/coverage.exe"

mkdir -p testing
cp .coveragerc testing/
cd testing
${WINE} ${COVERAGE} erase

echo "TESTING CTYPES"
if [ "${TRAVIS_PYTHON_VERSION}" = "2.6" ]; then
    ${WINE} ${COVERAGE} run -m unittest2 discover win32ctypes -v
else
    ${WINE} ${COVERAGE} run -m unittest discover win32ctypes -v
fi

# install cffi
${WINE} ${PIP} install --only-binary cffi cffi

echo "TESTING CFFI"
if [ "${TRAVIS_PYTHON_VERSION}" = "2.6" ]; then
    ${WINE} ${COVERAGE} run -a -m unittest2 discover win32ctypes -v
else
    ${WINE} ${COVERAGE} run -a -m unittest discover win32ctypes -v
fi

${WINE} ${COVERAGE} report
