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
    BOOL, DWORD, HANDLE, HMODULE, LPCWSTR, WORD, HRSRC,
    HGLOBAL, LPVOID, UINT, LPWSTR, MAX_PATH)

from ._common import LONG_PTR, IS_INTRESOURCE
from ._util import (
    check_null, check_zero, check_false, Wrapping as W, DLL)


_ENUMRESTYPEPROC = ctypes.WINFUNCTYPE(BOOL, HMODULE, LPVOID, LONG_PTR)
_ENUMRESNAMEPROC = ctypes.WINFUNCTYPE(BOOL, HMODULE, LPVOID, LPVOID, LONG_PTR)
_ENUMRESLANGPROC = ctypes.WINFUNCTYPE(
    BOOL, HMODULE, LPVOID, LPVOID, WORD, LONG_PTR)


def ENUMRESTYPEPROC(callback):
    def wrapped(handle, type_, param):
        if IS_INTRESOURCE(type_):
            type_ = int(type_)
        else:
            type_ = ctypes.cast(type_, LPCWSTR).value
        return callback(handle, type_, param)

    return _ENUMRESTYPEPROC(wrapped)


def ENUMRESNAMEPROC(callback):
    def wrapped(handle, type_, name, param):
        if IS_INTRESOURCE(type_):
            type_ = int(type_)
        else:
            type_ = ctypes.cast(type_, LPCWSTR).value
        if IS_INTRESOURCE(name):
            name = int(name)
        else:
            name = ctypes.cast(name, LPCWSTR).value
        return callback(handle, type_, name, param)

    return _ENUMRESNAMEPROC(wrapped)


def ENUMRESLANGPROC(callback):
    def wrapped(handle, type_, name, language, param):
        if IS_INTRESOURCE(type_):
            type_ = int(type_)
        else:
            type_ = ctypes.cast(type_, LPCWSTR).value
        if IS_INTRESOURCE(name):
            name = int(name)
        else:
            name = ctypes.cast(name, LPCWSTR).value
        return callback(handle, type_, name, language, param)

    return _ENUMRESLANGPROC(wrapped)


wrapped_functions = {
    '_GetACP': W('GetACP', None, UINT, None),
    '_LoadLibraryEx': W('LoadLibraryExW', [LPCWSTR, HANDLE, DWORD], HMODULE, check_null),  # noqa
    '_FreeLibrary': W('FreeLibrary', [HMODULE], BOOL, check_false),
    '_EnumResourceTypes': W('EnumResourceTypesW', [HMODULE, _ENUMRESTYPEPROC, LONG_PTR], BOOL, check_false),  # noqa
    '_LoadResource': W('LoadResource', [HMODULE, HRSRC], HGLOBAL, check_null),  # noqa
    '_LockResource': W('LockResource', [HGLOBAL], LPVOID, check_null),
    '_SizeofResource': W('SizeofResource', [HMODULE, HRSRC], DWORD, check_zero),  # noqa
    '_BaseEnumResourceNames': W('EnumResourceNamesW', [HMODULE, LPCWSTR, _ENUMRESNAMEPROC, LONG_PTR], BOOL, check_false),  # noqa
    '_BaseEnumResourceLanguages': W('EnumResourceLanguagesW', [HMODULE, LPCWSTR, LPCWSTR, _ENUMRESLANGPROC, LONG_PTR], BOOL, check_false),  # noqa
    '_BaseFindResourceEx': W('FindResourceExW', [HMODULE, LPCWSTR, LPCWSTR, WORD], HRSRC, check_null),  # noqa
    '_GetTickCount': W('GetTickCount', None, DWORD, None),  # noqa
    '_BeginUpdateResource': W('BeginUpdateResourceW', [LPCWSTR, BOOL], HANDLE, check_null),  # noqa
    '_EndUpdateResource': W('EndUpdateResourceW', [HANDLE, BOOL], BOOL, check_false),  # noqa
    '_BaseUpdateResource': W('UpdateResourceW', [HANDLE, LPCWSTR, LPCWSTR, WORD, LPVOID, DWORD], BOOL, check_false),  # noqa
    '_BaseGetWindowsDirectory': W('GetWindowsDirectoryW', [LPWSTR, UINT], UINT, check_zero),  # noqa
    '_BaseGetSystemDirectory': W('GetSystemDirectoryW', [LPWSTR, UINT], UINT, check_zero)}  # noqa


class KERNEL32(DLL):

    def _GetWindowsDirectory(self):
        buffer = ctypes.create_unicode_buffer(MAX_PATH)
        self._BaseGetWindowsDirectory(buffer, MAX_PATH)
        return ctypes.cast(buffer, LPCWSTR).value

    def _GetSystemDirectory(self):
        buffer = ctypes.create_unicode_buffer(MAX_PATH)
        self._BaseGetSystemDirectory(buffer, MAX_PATH)
        return ctypes.cast(buffer, LPCWSTR).value

    def _UpdateResource(
            self, hUpdate, lpType, lpName, wLanguage, lpData, cbData):
        lp_type = LPCWSTR(lpType)
        lp_name = LPCWSTR(lpName)
        self._BaseUpdateResource(
            hUpdate, lp_type, lp_name, wLanguage, lpData, cbData)

    def _EnumResourceNames(self, hModule, lpszType, lpEnumFunc, lParam):
        resource_type = LPCWSTR(lpszType)
        self._BaseEnumResourceNames(hModule, resource_type, lpEnumFunc, lParam)

    def _EnumResourceLanguages(
            self, hModule, lpType, lpName, lpEnumFunc, lParam):
        resource_type = LPCWSTR(lpType)
        resource_name = LPCWSTR(lpName)
        self._BaseEnumResourceLanguages(
            hModule, resource_type, resource_name, lpEnumFunc, lParam)

    def _FindResourceEx(self, hModule, lpType, lpName, wLanguage):
        resource_type = LPCWSTR(lpType)
        resource_name = LPCWSTR(lpName)
        return self._BaseFindResourceEx(
            hModule, resource_type, resource_name, wLanguage)


# Use a local copy of the kernel32 dll.
dll = KERNEL32(ctypes.WinDLL('kernel32'), functions=wrapped_functions)
