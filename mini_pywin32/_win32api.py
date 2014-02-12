from __future__ import absolute_import

import ctypes
from ctypes.wintypes import (
    BOOL, DWORD, HANDLE, HMODULE, LONG, LPCWSTR, WCHAR, WORD, HRSRC,
    HGLOBAL, LPVOID)

from ._common import LONG_PTR
from ._util import check_null, check_zero, function_factory

kernel32 = ctypes.windll.kernel32

ENUMRESTYPEPROC = ctypes.WINFUNCTYPE(BOOL, HMODULE, LONG, LONG_PTR)
ENUMRESNAMEPROC = ctypes.WINFUNCTYPE(BOOL, HMODULE, LONG, LONG, LONG_PTR)
ENUMRESLANGPROC = ctypes.WINFUNCTYPE(
    BOOL, HMODULE, WCHAR, WCHAR, WORD, LONG_PTR)

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
    [HMODULE, ENUMRESTYPEPROC, LONG_PTR],
    BOOL,
    check_zero)

_EnumResourceNames = function_factory(
    kernel32.EnumResourceNamesW,
    [HMODULE, DWORD, ENUMRESNAMEPROC, LONG_PTR],
    BOOL,
    check_zero)

_EnumResourceLanguages = function_factory(
    kernel32.EnumResourceLanguagesW,
    [HMODULE, LPCWSTR, LPCWSTR, ENUMRESLANGPROC, LONG_PTR],
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
