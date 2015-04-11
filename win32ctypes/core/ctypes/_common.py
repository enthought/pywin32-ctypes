#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from __future__ import absolute_import

import ctypes
from ctypes import pythonapi, POINTER, c_void_p, py_object
from ctypes.wintypes import BYTE

from win32ctypes.core.compat import PY3
from ._util import function_factory

PPy_UNICODE = c_void_p
LPBYTE = POINTER(BYTE)

if ctypes.sizeof(ctypes.c_long) == ctypes.sizeof(ctypes.c_void_p):
    LONG_PTR = ctypes.c_long
elif ctypes.sizeof(ctypes.c_longlong) == ctypes.sizeof(ctypes.c_void_p):
    LONG_PTR = ctypes.c_longlong

if PY3:
    _PyBytes_FromStringAndSize = function_factory(
        pythonapi.PyBytes_FromStringAndSize,
        return_type=py_object)
else:
    _PyBytes_FromStringAndSize = function_factory(
        pythonapi.PyString_FromStringAndSize,
        return_type=py_object)

IS_INTRESOURCE = lambda x: x >> 16 == 0
