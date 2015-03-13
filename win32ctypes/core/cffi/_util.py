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


def function_factory(cfunction, error_check=None):
    if error_check is None:
        return cfunction
    else:
        def function(*args, **kwrgs):
            error_check(cfunction(*args, **kwrgs))
        return function


class ErrorWhen(object):

    def __init__(self, check):
        self._check = check

    def raise_error():
        code, message = ffi.getwinerror()
        exception = WindowsError()
        exception.errno = ffi.errno
        exception.winerror = code
        exception.strerror = message
        raise exception

    def __call__(self, value):
        if value == self._check:
            self._raise_error()
        else:
            return value


check_null = ErrorWhen(None)
check_zero = ErrorWhen(0)
