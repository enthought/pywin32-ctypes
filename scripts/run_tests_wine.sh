#! /bin/sh
set -e

export DISPLAY=:99.0

if [ "${TRAVIS_PYTHON_VERSION}" = "2.7" ]; then
    COVERAGE="c:/Python27/Scripts/coverage.exe"
elif [ "${TRAVIS_PYTHON_VERSION}" = "3.2" ]; then
    COVERAGE="c:/Python32/Scripts/coverage.exe"
else
    exit 1;
fi

wine ${COVERAGE} erase
wine ${COVERAGE} run -m nose.core win32ctypes
wine ${COVERAGE} report --include=win32ctypes*
