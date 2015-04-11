#! /bin/sh
set -e

export DISPLAY=:99.0

if [ "${MODE}" == *"64" ]; then
    WINE="wine64"
else
    WINE="wine"
fi



if [ "${TRAVIS_PYTHON_VERSION}" = "2.6" ]; then
    COVERAGE="c:/Python26/Scripts/coverage.exe"
elif [ "${TRAVIS_PYTHON_VERSION}" = "2.7" ]; then
    COVERAGE="c:/Python27/Scripts/coverage.exe"
elif [ "${TRAVIS_PYTHON_VERSION}" = "3.2" ]; then
    COVERAGE="c:/Python32/Scripts/coverage.exe"
elif [ "${TRAVIS_PYTHON_VERSION}" = "3.3" ]; then
    COVERAGE="c:/Python33/Scripts/coverage.exe"
else
    exit 1;
fi

mkdir -p testing
cp .coveragerc testing/
cd testing
${WINE} ${COVERAGE} erase
if [ "${TRAVIS_PYTHON_VERSION}" = "2.6" ]; then
    ${WINE} ${COVERAGE} run -m unittest2 discover win32ctypes -v
else
    ${WINE} ${COVERAGE} run -m unittest discover win32ctypes -v
fi

${WINE} ${COVERAGE} report
