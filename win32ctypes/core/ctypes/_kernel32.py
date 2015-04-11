#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from __future__ import absolute_import

import ctypes
from ctypes.wintypes import (
    BOOL, DWORD, HANDLE, HMODULE, LONG, LPCWSTR, WCHAR, WORD, HRSRC,
    HGLOBAL, LPVOID, UINT)

from ._common import LONG_PTR, LPTSTR
from ._util import check_null, check_zero, function_factory

# While the lpszType is a LPTSTR we need to treat it as pointer
_ENUMRESTYPEPROC = ctypes.WINFUNCTYPE(BOOL, HMODULE, LPVOID, LONG_PTR)
ENUMRESNAMEPROC = ctypes.WINFUNCTYPE(BOOL, HMODULE, LONG, LONG, LONG_PTR)
ENUMRESLANGPROC = ctypes.WINFUNCTYPE(
    BOOL, HMODULE, WCHAR, WCHAR, WORD, LONG_PTR)

kernel32 = ctypes.windll.kernel32


def ENUMRESTYPEPROC(callback):
    def wrapped(hModule, typename, param):
        if typename >> 16 == 0:
            return callback(hModule, int(typename), param)
        else:
            return True

    return _ENUMRESTYPEPROC(wrapped)

_GetACP = function_factory(kernel32.GetACP, None, UINT)

_LoadLibraryEx = function_factory(
    kernel32.LoadLibraryExW,
    [LPCWSTR, HANDLE, DWORD],
    HMODULE, check_null)

_FreeLibrary = function_factory(
    kernel32.FreeLibrary,
    [HMODULE],
    BOOL,
    check_zero)

_EnumResourceTypes = function_factory(
    kernel32.EnumResourceTypesW,
    [HMODULE, _ENUMRESTYPEPROC, LONG_PTR],
    BOOL,
    check_zero)

_EnumResourceNames = function_factory(
    kernel32.EnumResourceNamesW,
    [HMODULE, DWORD, ENUMRESNAMEPROC, LONG_PTR],
    BOOL,
    check_zero)

_EnumResourceLanguages = function_factory(
    kernel32.EnumResourceLanguagesW,
    [HMODULE, DWORD, DWORD, ENUMRESLANGPROC, LONG_PTR],
    BOOL,
    check_zero)

_LoadResource = function_factory(
    kernel32.LoadResource,
    [HMODULE, HRSRC],
    HGLOBAL,
    check_zero)

_LockResource = function_factory(
    kernel32.LockResource,
    [HGLOBAL],
    LPVOID,
    check_null)

_FindResourceEx = function_factory(
    kernel32.FindResourceExW,
    [HMODULE, DWORD, DWORD, WORD],
    HRSRC,
    check_null)

_SizeofResource = function_factory(
    kernel32.SizeofResource,
    [HMODULE, HRSRC],
    DWORD,
    check_zero)
