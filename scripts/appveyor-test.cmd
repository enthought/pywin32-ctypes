@echo off

mkdir testrun
copy .coveragerc testrun
cd testrun
echo. Test using ctypes
coverage run -m unittest discover -v win32ctypes
if %errorlevel% neq 0 exit /b %errorlevel%
pip install --cache-dir C:/egg_cache --upgrade cffi>=1.3.0
if %errorlevel% neq 0 exit /b %errorlevel%
echo. Test using cffi
coverage run -a -m unittest discover -v win32ctypes
