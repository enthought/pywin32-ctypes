.. image:: https://travis-ci.org/enthought/pywin32-ctypes.png
  :target: https://travis-ci.org/enthought/pywin32-ctypes

.. image:: https://codecov.io/github/enthought/pywin32-ctypes/coverage.svg?branch=master
   :target: https://codecov.io/github/enthought/pywin32-ctypes?branch=master

A reimplementation of pywin32 that is pure python. The default
behaviour will try to use cffi (>= 1.3.0), if available, and fall back
to using ctypes. Please note that there is no need to have a compiler
available on installation or at runtime.

Example of usage::

    # Equivalent to 'import win32api' from pywin32.
    from win32ctypes.pywin32 import win32api

    win32api.LoadLibraryEx(sys.executable, 0, win32api.LOAD_LIBRARY_AS_DATAFILE)

Note: this implements only a very small subset of pywin32, for internal needs
at Enthought. We do welcome additional features and prs, though.

Development setup
=================

The following should be good enough::

	pip install -r dev_requirements.txt
	python setup.py develop

Note: because of the pywin32 dependency for tests, you most likely want to
create a virtualenv with --system-site-packages if you use virtualenv.

While pywin32-ctypes should regularly be tested on windows, you can also
develop/test on unix by using wine (see travis-ci configuration to set it up).
