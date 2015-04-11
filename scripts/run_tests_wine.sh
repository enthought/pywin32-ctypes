#! /bin/sh
set -e

export DISPLAY=:99.0

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

wine ${COVERAGE} erase
wine ${COVERAGE} run -m unittest discover
wine ${COVERAGE} report
