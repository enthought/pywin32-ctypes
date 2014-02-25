#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

""" Utility functions to help with python wrapping.
"""
from __future__ import absolute_import

from ctypes import GetLastError, FormatError

from .pywintypes import error


def function_factory(
        function,  argument_types=None, return_type=None,
        error_checking=None):
    if argument_types is not None:
        function.argtypes = argument_types
    function.restype = return_type
    if error_checking is not None:
        function.errcheck = error_checking
    return function


def check_null_factory(func_name=None):
    def check_null(result, func, arguments, *args):
        if result is None:
            code = GetLastError()
            description = FormatError(code).strip()
            if func_name is None:
                raise error(code, func.__name__, description)
            else:
                raise error(code, func_name, description)
        return result
    return check_null

check_null = check_null_factory()


def check_zero_factory(func_name=None):
    def check_zero(result, func, arguments, *args):
        if result == 0:
            code = GetLastError()
            description = FormatError(code).strip()
            if func_name is None:
                raise error(code, func.__name__, description)
            else:
                raise error(code, func_name, description)
        return result
    return check_zero

check_zero = check_zero_factory()
