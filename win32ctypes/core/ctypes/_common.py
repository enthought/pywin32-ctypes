#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from __future__ import absolute_import

import sys
from ctypes import (
    POINTER, c_void_p, py_object, c_char_p, c_int, c_long, c_int64, c_longlong,
    PyDLL, sizeof, byref, cast)
from ctypes.wintypes import BYTE

from win32ctypes.core.compat import PY3
from ._util import Wrapping as W, DLL

PPy_UNICODE = c_void_p
LPBYTE = POINTER(BYTE)
is_64bits = sys.maxsize > 2**32
Py_ssize_t = c_int64 if is_64bits else c_int

if sizeof(c_long) == sizeof(c_void_p):
    LONG_PTR = c_long
elif sizeof(c_longlong) == sizeof(c_void_p):
    LONG_PTR = c_longlong
byreference = byref


def IS_INTRESOURCE(x):
    return x >> 16 == 0


def dereference(x):
    return x.contents


pythonapi = DLL(
    PyDLL("python dll", None, sys.dllhandle),
    functions={
        '_PyBytes_FromStringAndSize': W(
            'PyBytes_FromStringAndSize' if PY3 else 'PyString_FromStringAndSize',  # noqa
            [c_char_p, Py_ssize_t], py_object, None)})
