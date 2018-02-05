
.. image:: https://ci.appveyor.com/api/projects/status/62xqtrro26gw3l4x/branch/master?svg=true
  :target: https://ci.appveyor.com/project/EnthoughtOSS/pywin32-ctypes

.. image:: https://codecov.io/github/enthought/pywin32-ctypes/coverage.svg?branch=master
   :target: https://codecov.io/github/enthought/pywin32-ctypes?branch=master

.. image:: https://readthedocs.org/projects/pywin32-ctypes/badge/?version=master
   :target: http://pywin32-ctypes.readthedocs.org/en/latest/?badge=master
   :alt: Documentation Status

A reimplementation of pywin32 that is pure python. The default
behaviour will try to use cffi (>= 1.3.0), if available, and fall back
to using ctypes. Please note that there is no need to have a compiler
available on installation or at runtime.

Usage
=====

Example::

  # Equivalent to 'import win32api' from pywin32.
  from win32ctypes.pywin32 import win32api

  win32api.LoadLibraryEx(sys.executable, 0, win32api.LOAD_LIBRARY_AS_DATAFILE)

.. note::

   Currently pywin32ctypes implements only a very small subset
   of pywin32, for internal needs at Enthought. We do welcome
   additional features and PRs, though.

Development setup
=================

The following should be good enough::

  pip install -r dev_requirements.txt
  python install -e

.. note::

   - While pywin32-ctypes should regularly be tested on windows, you can also
     develop/test on unix by using wine
