#! /bin/sh
set -e

export DISPLAY=:99.0

PYTHON="c:/Python27/python.exe"
COVERAGE="c:/Python27/Scripts/coverage.exe"

wine ${PYTHON} -m nose.core win32ctypes
wine ${COVERAGE} erase
wine ${COVERAGE} run -m nose.core win32ctypes
wine ${COVERAGE} report --include=win32ctypes*
