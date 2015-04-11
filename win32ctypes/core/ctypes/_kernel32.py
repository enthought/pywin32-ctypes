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

from ._common import LONG_PTR
from ._util import check_null, check_zero, function_factory

_ENUMRESTYPEPROC = ctypes.WINFUNCTYPE(BOOL, HMODULE, LPVOID, LONG_PTR)
_ENUMRESNAMEPROC = ctypes.WINFUNCTYPE(BOOL, HMODULE, LPVOID, LPVOID, LONG_PTR)
_ENUMRESLANGPROC = ctypes.WINFUNCTYPE(
    BOOL, HMODULE, LPVOID, LPVOID, WORD, LONG_PTR)

kernel32 = ctypes.windll.kernel32


def ENUMRESTYPEPROC(callback):
    def wrapped(handle, type_, param):
        if type_ >> 16 == 0:
            type_ = int(type_)
        else:
            type_ = ctypes.cast(type_, LPCWSTR).value
        return callback(handle, type_, param)

    return _ENUMRESTYPEPROC(wrapped)


def ENUMRESNAMEPROC(callback):
    def wrapped(handle, type_, name, param):
        if type_ >> 16 == 0:
            type_ = int(type_)
        else:
            type_ = ctypes.cast(type_, LPCWSTR).value
        if name >> 16 == 0:
            name = int(name)
        else:
            name = ctypes.cast(name, LPCWSTR).value
        return callback(handle, type_, name, param)

    return _ENUMRESNAMEPROC(wrapped)


def ENUMRESLANGPROC(callback):
    def wrapped(handle, type_, name, language, param):
        if type_ >> 16 == 0:
            type_ = int(type_)
        else:
            type_ = ctypes.cast(type_, LPCWSTR).value
        if name >> 16 == 0:
            name = int(name)
        else:
            name = ctypes.cast(name, LPCWSTR).value
        return callback(handle, type_, name, language, param)

    return _ENUMRESLANGPROC(wrapped)

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

_SizeofResource = function_factory(
    kernel32.SizeofResource,
    [HMODULE, HRSRC],
    DWORD,
    check_zero)

_BaseEnumResourceNames = function_factory(
    kernel32.EnumResourceNamesW,
    [HMODULE, LPCWSTR, _ENUMRESNAMEPROC, LONG_PTR],
    BOOL,
    check_zero)

_BaseEnumResourceLanguages = function_factory(
    kernel32.EnumResourceLanguagesW,
    [HMODULE, LPCWSTR, LPCWSTR, _ENUMRESLANGPROC, LONG_PTR],
    BOOL,
    check_zero)

_BaseFindResourceEx = function_factory(
    kernel32.FindResourceExW,
    [HMODULE, LPCWSTR, LPCWSTR, WORD],
    HRSRC,
    check_null)


def _EnumResourceNames(hModule, lpszType, lpEnumFunc, lParam):
    resource_type = LPCWSTR(lpszType)
    return _BaseEnumResourceNames(
        hModule, resource_type, lpEnumFunc, lParam)


def _EnumResourceLanguages(hModule, lpType, lpName, lpEnumFunc, lParam):
    resource_type = LPCWSTR(lpType)
    resource_name = LPCWSTR(lpName)
    return _BaseEnumResourceLanguages(
        hModule, resource_type, resource_name, lpEnumFunc, lParam)


def _FindResourceEx(hModule, lpType, lpName, wLanguage):
    resource_type = LPCWSTR(lpType)
    resource_name = LPCWSTR(lpName)
    return _BaseFindResourceEx(
        hModule, resource_type, resource_name, wLanguage)
