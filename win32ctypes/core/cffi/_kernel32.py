#
# (C) Copyright 2015 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from __future__ import absolute_import

from ._util import ffi, check_null, check_zero, HMODULE, PVOID
from ._common import IS_INTRESOURCE

ffi.cdef("""

typedef int WINBOOL;
typedef WINBOOL (*ENUMRESTYPEPROC) (HANDLE, LPTSTR, LONG_PTR);
typedef WINBOOL (*ENUMRESNAMEPROC) (HANDLE, LPCTSTR, LPTSTR, LONG_PTR);
typedef WINBOOL (*ENUMRESLANGPROC) (HANDLE, LPCTSTR, LPCTSTR, WORD, LONG_PTR);


BOOL Beep(DWORD dwFreq, DWORD dwDuration);
UINT GetACP(void);
HMODULE LoadLibraryExW(LPCTSTR lpFileName, HANDLE hFile, DWORD dwFlags);
BOOL FreeLibrary(HMODULE hModule);
BOOL EnumResourceTypesW(
    HMODULE hModule, ENUMRESTYPEPROC lpEnumFunc, LONG_PTR lParam);
BOOL EnumResourceNamesW(
    HMODULE hModule, LPCTSTR lpszType,
    ENUMRESNAMEPROC lpEnumFunc, LONG_PTR lParam);
BOOL EnumResourceLanguagesW(
    HMODULE hModule, LPCTSTR lpType,
    LPCTSTR lpName, ENUMRESLANGPROC lpEnumFunc, LONG_PTR lParam);

""")

kernel32 = ffi.dlopen('kernel32.dll')


def ENUMRESTYPEPROC(callback):
    def wrapped(hModule, lpszType, lParam):
        if IS_INTRESOURCE(lpszType):
            resource_type = int(ffi.cast("uintptr_t", lpszType))
        else:
            resource_type = ffi.string(lpszType)
        return callback(hModule, resource_type, lParam)
    return wrapped


def ENUMRESNAMEPROC(callback):
    def wrapped(hModule, lpszType, lpszName, lParam):
        if IS_INTRESOURCE(lpszType):
            resource_type = int(ffi.cast("uintptr_t", lpszType))
        else:
            resource_type = ffi.string(lpszType)
        if IS_INTRESOURCE(lpszName):
            resource_name = int(ffi.cast("uintptr_t", lpszName))
        else:
            resource_name = ffi.string(lpszName)
        return callback(hModule, resource_type, resource_name, lParam)
    return wrapped


def ENUMRESLANGPROC(callback):
    def wrapped(hModule, lpszType, lpszName, wIDLanguage, lParam):
        if IS_INTRESOURCE(lpszType):
            resource_type = int(ffi.cast("uintptr_t", lpszType))
        else:
            resource_type = ffi.string(lpszType)
        if IS_INTRESOURCE(lpszName):
            resource_name = int(ffi.cast("uintptr_t", lpszName))
        else:
            resource_name = ffi.string(lpszName)
        return callback(
            hModule, resource_type, resource_name, wIDLanguage, lParam)
    return wrapped


def _GetACP():
    return kernel32.GetACP()


def _LoadLibraryEx(lpFilename, hFile, dwFlags):
    result = check_null(
        kernel32.LoadLibraryExW(
            unicode(lpFilename), ffi.NULL, dwFlags))
    return HMODULE(result)


def _FreeLibrary(hModule):
    check_zero(kernel32.FreeLibrary(PVOID(hModule)))


def _EnumResourceTypes(hModule, lpEnumFunc, lParam):
    callback = ffi.callback('ENUMRESTYPEPROC', lpEnumFunc)
    check_zero(
        kernel32.EnumResourceTypesW(PVOID(hModule), callback, lParam))


def _EnumResourceNames(hModule, lpszType, lpEnumFunc, lParam):
    callback = ffi.callback('ENUMRESNAMEPROC', lpEnumFunc)
    if isinstance(lpszType, (int, long)):
        lpszType = ffi.cast('wchar_t *', lpszType)
    check_zero(
        kernel32.EnumResourceNamesW(
            PVOID(hModule), lpszType, callback, lParam))


def _EnumResourceLanguages(hModule, lpType, lpName, lpEnumFunc, lParam):
    callback = ffi.callback('ENUMRESLANGPROC', lpEnumFunc)
    if isinstance(lpType, (int, long)):
        lpType = ffi.cast('wchar_t *', lpType)
    if isinstance(lpName, (int, long)):
        lpName = ffi.cast('wchar_t *', lpName)
    elif isinstance(lpName, str):
        lpName = unicode(lpName)
    check_zero(
        kernel32.EnumResourceLanguagesW(
            PVOID(hModule), lpType, lpName, callback, lParam))
