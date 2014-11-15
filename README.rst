.. image:: https://travis-ci.org/enthought/pywin32-ctypes.png
  :target: https://travis-ci.org/enthought/pywin32-ctypes

A reimplementation of pywin32 that is pure python (uses ctypes).

Example of usage::

    # Equivalent to 'import win32api' from pywin32.
    from win32ctypes import win32api

    win32api.LoadLibraryEx(sys.executable, 0, win32api.LOAD_LIBRARY_AS_DATAFILE)

Note: this implements only a very small subset of pywin32, for internal needs
at Enthought. We do welcome additional features, though.

Development setup
=================

The following should be good enough::

	pip install -r dev_requirements.txt
	python setup.py develop

Note: because of the pywin32 dependency for tests, you most likely want to
create a virtualenv with --system-site-packages if you use virtualenv.

While pywin32-ctypes should regularly be tested on windows, you can also
develop/test on unix by using wine (see travis-ci configuration to set it up).
