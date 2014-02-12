from __future__ import absolute_import

import ctypes
from ctypes.wintypes import (
    BOOL, DWORD, HANDLE, HMODULE, LONG, LPCWSTR, LPARAM, WCHAR, WORD,
    HRSRC, HGLOBAL, LPVOID)

from .util import check_null, check_zero, function_factory, LONG_PTR

kernel32 = ctypes.windll.kernel32


_LoadLibraryEx = function_factory(
        kernel32.LoadLibraryExW,
        [LPCWSTR, HANDLE, DWORD],
        HMODULE, check_null)

_FreeLibrary = function_factory(
    kernel32.FreeLibrary,
    [HMODULE],
    BOOL,
    check_zero)

ENUMRESTYPEPROC = ctypes.WINFUNCTYPE(BOOL, HMODULE, LONG, LPARAM)
_EnumResourceTypes = function_factory(
    kernel32.EnumResourceTypesW,
    [HMODULE, ENUMRESTYPEPROC, LONG_PTR],
    BOOL,
    check_zero)

ENUMRESNAMEPROC = ctypes.WINFUNCTYPE(BOOL, HMODULE, LONG, LONG, LPARAM)
_EnumResourceNames = function_factory(
    kernel32.EnumResourceNamesW,
    [HMODULE, DWORD, ENUMRESNAMEPROC, LONG_PTR],
    BOOL,
    check_zero)

ENUMRESLANGPROC = ctypes.WINFUNCTYPE(
    BOOL, HMODULE, WCHAR, WCHAR, WORD, LPARAM)
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
