@echo off
"%sdkverpath%" -q -version:"%sdkver%"
call setenv /x64

rem install python packages
pip install --cache-dir C:/egg_cache coverage
pip install --cache-dir C:/egg_cache --only-binary pypiwin32 pypiwin32

rem install package
python setup.py install
