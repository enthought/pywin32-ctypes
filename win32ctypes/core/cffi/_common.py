#
# (C) Copyright 2015-2024 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from ._util import ffi


def _PyBytes_FromStringAndSize(pointer, size):
    buffer = ffi.buffer(pointer, size)
    return buffer[:]


def byreference(x):
    return ffi.new(ffi.getctype(ffi.typeof(x), '*'), x)


def dereference(x):
    return x[0]


def PDWORD(value=0):
    return ffi.new("DWORD *", value)
