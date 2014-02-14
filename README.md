A reimplementation of pywin32 that is pure python (uses ctypes).

Example of usage:

```
# Equivalent to 'import win32api' from pywin32.
from win32ctypes import win32api

win32api.LoadLibraryEx(sys.executable, 0, win32api.LOAD_LIBRARY_AS_DATAFILE)
```

Note: this implements only a very small subset of pywin32, for internal needs
at Enthought. We do welcome additional features, though.
