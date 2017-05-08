#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from __future__ import absolute_import

import ctypes
import sys
from ctypes import pythonapi, POINTER, c_void_p, py_object, c_char_p
from ctypes import cast  # noqa imported here for convenience
from ctypes.wintypes import BYTE

from win32ctypes.core.compat import PY3
from ._util import function_factory

PPy_UNICODE = c_void_p
LPBYTE = POINTER(BYTE)
is_64bits = sys.maxsize > 2**32
Py_ssize_t = ctypes.c_int64 if is_64bits else ctypes.c_int

if ctypes.sizeof(ctypes.c_long) == ctypes.sizeof(ctypes.c_void_p):
    LONG_PTR = ctypes.c_long
elif ctypes.sizeof(ctypes.c_longlong) == ctypes.sizeof(ctypes.c_void_p):
    LONG_PTR = ctypes.c_longlong

if PY3:
    _PyBytes_FromStringAndSize = function_factory(
        pythonapi.PyBytes_FromStringAndSize,
        [c_char_p, Py_ssize_t],
        return_type=py_object)
else:
    _PyBytes_FromStringAndSize = function_factory(
        pythonapi.PyString_FromStringAndSize,
        [c_char_p, Py_ssize_t],
        return_type=py_object)

IS_INTRESOURCE = lambda x: x >> 16 == 0

byreference = ctypes.byref


def dereference(x):
    return x.contents
