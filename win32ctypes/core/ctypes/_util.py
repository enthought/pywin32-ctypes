#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

""" Utility functions to help with ctypes wrapping.
"""
from __future__ import absolute_import
from functools import partial
from collections import namedtuple

from ctypes import GetLastError, FormatError


def make_error(function, function_name=None):
    code = GetLastError()
    description = FormatError(code).strip()
    if function_name is None:
        function_name = function.__name__
    exception = WindowsError()
    exception.winerror = code
    exception.function = function_name
    exception.strerror = description
    return exception


def check_null(function_name, result, function, arguments, *args):
    if result is None:
        raise make_error(function, function_name)
    return result


def check_false(function_name, result, function, arguments, *args):
    if not bool(result):
        raise make_error(function, function_name)
    else:
        return True


def check_zero(function_name, result, function, arguments, *args):
    if result == 0:
        raise make_error(function, function_name)
    return result



Wrapping = namedtuple(
    'Wrapping',
    ['real_name', 'argument_types', 'return_type', 'error_checking'])


class DLL(object):

    def __init__(self, dll, functions):
        self._dll = dll
        self._functions = functions

    def __getattr__(self, name):
        wrapping = self._functions.get(name, None)
        if wrapping is None:
            message = 'Function {} is not currently wrapped'
            raise AttributeError(message.format(name))
        function = getattr(self._dll, wrapping.real_name)
        if wrapping.argument_types is not None:
            function.argtypes = wrapping.argument_types
        if wrapping.return_type is not None:
            function.restype = wrapping.return_type
        if wrapping.error_checking is not None:
            function.errcheck = partial(wrapping.error_checking, name[1:])
        # Cache wrapped function
        self.__dict__[name] = function
        return function
