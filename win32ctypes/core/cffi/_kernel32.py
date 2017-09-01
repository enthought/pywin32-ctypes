#
# (C) Copyright 2015 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from __future__ import absolute_import

from win32ctypes.core.compat import unicode
from ._util import (
    ffi, check_null, check_zero, check_false, HMODULE, PVOID, RESOURCE, resource)

# TODO: retrieve this value using ffi
MAX_PATH = 260
MAX_PATH_BUF = u'wchar_t[{0}]'.format(MAX_PATH)

ffi.cdef("""

typedef int WINBOOL;
typedef WINBOOL (__stdcall *ENUMRESTYPEPROC) (HANDLE, LPTSTR, LONG_PTR);
typedef WINBOOL (__stdcall *ENUMRESNAMEPROC) (HANDLE, LPCTSTR, LPTSTR, LONG_PTR);
typedef WINBOOL (__stdcall *ENUMRESLANGPROC) (HANDLE, LPCTSTR, LPCTSTR, WORD, LONG_PTR);

BOOL WINAPI Beep(DWORD dwFreq, DWORD dwDuration);
UINT WINAPI GetACP(void);
DWORD WINAPI GetTickCount(void);
HMODULE WINAPI LoadLibraryExW(LPCTSTR lpFileName, HANDLE hFile, DWORD dwFlags);
BOOL WINAPI FreeLibrary(HMODULE hModule);
BOOL WINAPI EnumResourceTypesW(
    HMODULE hModule, ENUMRESTYPEPROC lpEnumFunc, LONG_PTR lParam);
BOOL WINAPI EnumResourceNamesW(
    HMODULE hModule, LPCTSTR lpszType,
    ENUMRESNAMEPROC lpEnumFunc, LONG_PTR lParam);
BOOL WINAPI EnumResourceLanguagesW(
    HMODULE hModule, LPCTSTR lpType,
    LPCTSTR lpName, ENUMRESLANGPROC lpEnumFunc, LONG_PTR lParam);
HRSRC WINAPI FindResourceExW(
    HMODULE hModule, LPCTSTR lpType, LPCTSTR lpName, WORD wLanguage);
DWORD WINAPI SizeofResource(HMODULE hModule, HRSRC hResInfo);
HGLOBAL WINAPI LoadResource(HMODULE hModule, HRSRC hResInfo);
LPVOID WINAPI LockResource(HGLOBAL hResData);

HANDLE WINAPI BeginUpdateResourceW(LPCTSTR pFileName, BOOL bDeleteExistingResources);
BOOL WINAPI EndUpdateResourceW(HANDLE hUpdate, BOOL fDiscard);
BOOL WINAPI UpdateResourceW(HANDLE hUpdate, LPCTSTR lpType, LPCTSTR lpName, WORD wLanguage, LPVOID lpData, DWORD cbData);
UINT WINAPI GetWindowsDirectoryW(LPTSTR lpBuffer, UINT uSize);
UINT WINAPI GetSystemDirectoryW(LPTSTR lpBuffer, UINT uSize);

""")

kernel32 = ffi.dlopen('kernel32.dll')


def ENUMRESTYPEPROC(callback):
    def wrapped(hModule, lpszType, lParam):
        return callback(hModule, resource(lpszType), lParam)
    return wrapped


def ENUMRESNAMEPROC(callback):
    def wrapped(hModule, lpszType, lpszName, lParam):
        return callback(
            hModule, resource(lpszType), resource(lpszName), lParam)
    return wrapped


def ENUMRESLANGPROC(callback):
    def wrapped(hModule, lpszType, lpszName, wIDLanguage, lParam):
        return callback(
            hModule, resource(lpszType), resource(lpszName),
            wIDLanguage, lParam)
    return wrapped


def _GetACP():
    return kernel32.GetACP()


def _GetWindowsDirectory():
    buffer = ffi.new(MAX_PATH_BUF)
    l = kernel32.GetWindowsDirectoryW(buffer, MAX_PATH)
    return ffi.unpack(buffer, l)


def _GetSystemDirectory():
    buffer = ffi.new(MAX_PATH_BUF)
    l = kernel32.GetSystemDirectoryW(buffer, MAX_PATH)
    return ffi.unpack(buffer, l)


def _GetTickCount():
    return kernel32.GetTickCount()


def _LoadLibraryEx(lpFilename, hFile, dwFlags):
    result = check_null(
        kernel32.LoadLibraryExW(
            unicode(lpFilename), ffi.NULL, dwFlags),
        function_name='LoadLibraryEx')
    return HMODULE(result)


def _FreeLibrary(hModule):
    check_false(
        kernel32.FreeLibrary(PVOID(hModule)),
        function_name='FreeLibrary')


def _EnumResourceTypes(hModule, lpEnumFunc, lParam):
    callback = ffi.callback('ENUMRESTYPEPROC', lpEnumFunc)
    check_false(
        kernel32.EnumResourceTypesW(PVOID(hModule), callback, lParam),
        function_name='EnumResourceTypes')


def _EnumResourceNames(hModule, lpszType, lpEnumFunc, lParam):
    callback = ffi.callback('ENUMRESNAMEPROC', lpEnumFunc)
    check_false(
        kernel32.EnumResourceNamesW(
            PVOID(hModule), RESOURCE(lpszType), callback, lParam),
        function_name='EnumResourceNames')


def _EnumResourceLanguages(hModule, lpType, lpName, lpEnumFunc, lParam):
    callback = ffi.callback('ENUMRESLANGPROC', lpEnumFunc)
    check_false(
        kernel32.EnumResourceLanguagesW(
            PVOID(hModule), RESOURCE(lpType),
            RESOURCE(lpName), callback, lParam),
        function_name='EnumResourceLanguages')


def _FindResourceEx(hModule, lpType, lpName, wLanguage):
    return check_null(
        kernel32.FindResourceExW(
            PVOID(hModule), RESOURCE(lpType), RESOURCE(lpName), wLanguage),
        function_name='FindResourceEx')


def _SizeofResource(hModule, hResInfo):
    return check_zero(
        kernel32.SizeofResource(PVOID(hModule), hResInfo),
        function_name='SizeofResource')


def _LoadResource(hModule, hResInfo):
    return check_null(
        kernel32.LoadResource(PVOID(hModule), hResInfo),
        function_name='LoadResource')


def _LockResource(hResData):
    return check_null(
        kernel32.LockResource(hResData),
        function_name='LockResource')


def _BeginUpdateResource(pFileName, bDeleteExistingResources):
    result = check_null(
        kernel32.BeginUpdateResourceW(
            unicode(pFileName), bDeleteExistingResources))
    return HMODULE(result)


def _EndUpdateResource(hUpdate, fDiscard):
    check_false(
        kernel32.EndUpdateResourceW(PVOID(hUpdate), fDiscard),
        function_name='EndUpdateResource')


def _UpdateResource(hUpdate, lpType, lpName, wLanguage, cData, cbData):
    lpData = ffi.from_buffer(cData)
    check_false(
        kernel32.UpdateResourceW(
            PVOID(hUpdate), RESOURCE(lpType), RESOURCE(lpName),
            wLanguage, PVOID(lpData), cbData),
        function_name='UpdateResource')
