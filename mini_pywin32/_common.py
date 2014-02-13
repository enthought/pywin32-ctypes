""" Common constants and wrapped functions
"""
from __future__ import absolute_import

import ctypes
from ctypes import pythonapi, POINTER, c_void_p
from ctypes.wintypes import BYTE, UINT

from ._util import function_factory

PPy_UNICODE = c_void_p


kernel32 = ctypes.windll.kernel32


if ctypes.sizeof(ctypes.c_long) == ctypes.sizeof(ctypes.c_void_p):
    LONG_PTR = ctypes.c_long
elif ctypes.sizeof(ctypes.c_longlong) == ctypes.sizeof(ctypes.c_void_p):
    LONG_PTR = ctypes.c_longlong

LPBYTE = POINTER(BYTE)

_PyString_FromStringAndSize = function_factory(
    pythonapi.PyString_FromStringAndSize,
    return_type=ctypes.py_object)

_GetACP = function_factory(
    kernel32.GetACP,
    None,
    UINT)
