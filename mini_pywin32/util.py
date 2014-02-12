from ctypes import WinError


def check_null(result, func, arguments, *args):
    if result is None:
        raise WinError()
    return result


def check_zero(result, func, arguments, *args):
    if result == 0:
        raise WinError()
    return result
