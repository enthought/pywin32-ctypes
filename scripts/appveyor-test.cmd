mkdir testrun
copy .coveragerc testrun
cd testrun
coverage run -m unittest discover -v
if %errorlevel% neq 0 exit /b %errorlevel%
coverage report