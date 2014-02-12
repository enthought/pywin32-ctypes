""" Common constants and wrapped functions
"""
from __future__ import absolute_import

import ctypes
from ctypes import pythonapi, POINTER
from ctypes.wintypes import BYTE

from ._util import function_factory

if ctypes.sizeof(ctypes.c_long) == ctypes.sizeof(ctypes.c_void_p):
    LONG_PTR = ctypes.c_long
elif ctypes.sizeof(ctypes.c_longlong) == ctypes.sizeof(ctypes.c_void_p):
    LONG_PTR = ctypes.c_longlong

LPBYTE = POINTER(BYTE)

_PyString_FromStringAndSize = function_factory(
    pythonapi.PyString_FromStringAndSize,
    return_type=ctypes.py_object)
