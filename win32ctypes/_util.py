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


def check_null(result, func, arguments, *args):
    if result is None:
        code = GetLastError()
        description = FormatError(code).strip()
        raise error(code, func, description)
    return result


def check_zero(result, func, arguments, *args):
    if result == 0:
        code = GetLastError()
        description = FormatError(code).strip()
        raise error(code, func, description)
    return result
