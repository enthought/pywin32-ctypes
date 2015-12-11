@echo off
"%sdkverpath%" -q -version:"%sdkver%"
call setenv /x64

mkdir testrun
copy .coveragerc testrun
cd testrun
echo.Test using CTYPES
coverage run -m unittest discover -v win32ctypes
if %errorlevel% neq 0 exit /b %errorlevel%
pip install --upgrade cffi
if %errorlevel% neq 0 exit /b %errorlevel%
echo.Test using CFFI
coverage run -a -m unittest discover -v win32ctypes
