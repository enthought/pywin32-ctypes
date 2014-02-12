#! /bin/sh
set -e

export DISPLAY=:99.0

PYTHON="c:/Python27/python.exe"
COVERAGE="c:/Python27/Scripts/coverage.exe"

wine ${PYTHON} -m nose.core mini_pywin32
wine ${COVERAGE} erase
wine ${COVERAGE} run -m nose.core mini_pywin32
wine ${COVERAGE} report --include=mini_pywin32*
