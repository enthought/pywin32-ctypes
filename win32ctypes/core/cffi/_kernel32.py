#
# (C) Copyright 2015 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from __future__ import absolute_import

from ._util import (
    ffi, check_null, check_zero, HMODULE, PVOID, RESOURCE, resource)

ffi.cdef("""

typedef int WINBOOL;
typedef WINBOOL (__stdcall *ENUMRESTYPEPROC) (HANDLE, LPTSTR, LONG_PTR);
typedef WINBOOL (__stdcall *ENUMRESNAMEPROC) (HANDLE, LPCTSTR, LPTSTR, LONG_PTR);
typedef WINBOOL (__stdcall *ENUMRESLANGPROC) (HANDLE, LPCTSTR, LPCTSTR, WORD, LONG_PTR);

BOOL WINAPI Beep(DWORD dwFreq, DWORD dwDuration);
UINT WINAPI GetACP(void);
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
    check_zero(
        kernel32.EnumResourceNamesW(
            PVOID(hModule), RESOURCE(lpszType), callback, lParam))


def _EnumResourceLanguages(hModule, lpType, lpName, lpEnumFunc, lParam):
    callback = ffi.callback('ENUMRESLANGPROC', lpEnumFunc)
    check_zero(
        kernel32.EnumResourceLanguagesW(
            PVOID(hModule), RESOURCE(lpType),
            RESOURCE(lpName), callback, lParam))


def _FindResourceEx(hModule, lpType, lpName, wLanguage):
    return check_null(
        kernel32.FindResourceExW(
            PVOID(hModule), RESOURCE(lpType), RESOURCE(lpName), wLanguage))


def _SizeofResource(hModule, hResInfo):
    return check_zero(kernel32.SizeofResource(PVOID(hModule), hResInfo))


def _LoadResource(hModule, hResInfo):
    return check_null(kernel32.LoadResource(PVOID(hModule), hResInfo))


def _LockResource(hResData):
    return check_null(kernel32.LockResource(hResData))
