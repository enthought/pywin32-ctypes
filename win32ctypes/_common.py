#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

""" Common constants and wrapped functions
"""
from __future__ import absolute_import

import ctypes
from ctypes import pythonapi, POINTER, c_void_p, py_object
from ctypes.wintypes import BYTE, UINT

from .compat import PY3
from ._util import function_factory

PPy_UNICODE = c_void_p


kernel32 = ctypes.windll.kernel32


if ctypes.sizeof(ctypes.c_long) == ctypes.sizeof(ctypes.c_void_p):
    LONG_PTR = ctypes.c_long
elif ctypes.sizeof(ctypes.c_longlong) == ctypes.sizeof(ctypes.c_void_p):
    LONG_PTR = ctypes.c_longlong

LPBYTE = POINTER(BYTE)

if PY3:
    _PyBytes_FromStringAndSize = function_factory(
        pythonapi.PyBytes_FromStringAndSize,
        return_type=py_object)
else:
    _PyBytes_FromStringAndSize = function_factory(
        pythonapi.PyString_FromStringAndSize,
        return_type=py_object)

_GetACP = function_factory(
    kernel32.GetACP,
    None,
    UINT)
