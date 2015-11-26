@echo off
"%sdkverpath%" -q -version:"%sdkver%"
call setenv /x64

mkdir testrun
copy .coveragerc testrun
cd testrun
echo.Test using ctypes
coverage run -m unittest discover -v win32ctypes
if %errorlevel% neq 0 exit /b %errorlevel%
pip install --upgrade cffi==1.3.0 --no-binary cffi
if %errorlevel% neq 0 exit /b %errorlevel%
echo.Test using cffi
coverage run -a -m unittest discover -v win32ctypes
