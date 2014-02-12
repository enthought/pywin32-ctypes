import ctypes
from ctypes import WinError

if ctypes.sizeof(ctypes.c_long) == ctypes.sizeof(ctypes.c_void_p):
    LONG_PTR = ctypes.c_long
elif ctypes.sizeof(ctypes.c_longlong) == ctypes.sizeof(ctypes.c_void_p):
    LONG_PTR = ctypes.c_longlong


def function_factory(function, argument_types, return_type, error_checking):
    function.argtypes = argument_types
    function.restype = return_type
    function.errcheck = error_checking
    return function

def check_null(result, func, arguments, *args):
    if result is None:
        raise WinError()
    return result

def check_zero(result, func, arguments, *args):
    if result == 0:
        raise WinError()
    return result
