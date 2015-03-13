#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

""" Utility functions to help with cffi wrapping.
"""
from __future__ import absolute_import

from cffi import FFI

ffi = FFI()
ffi.set_unicode(True)


def HMODULE(cdata):
    return int(ffi.cast("intptr_t", cdata))


def PVOID(x):
    return ffi.cast("void *", x)


class ErrorWhen(object):

    def __init__(self, check):
        self._check = check

    def __call__(self, value):
        if value == self._check:
            self._raise_error()
        else:
            return value

    def _raise_error(self):
        code, message = ffi.getwinerror()
        exception = WindowsError()
        exception.errno = ffi.errno
        exception.winerror = code
        exception.strerror = message
        exception.function = ''
        raise exception

check_null = ErrorWhen(ffi.NULL)
check_zero = ErrorWhen(0)
