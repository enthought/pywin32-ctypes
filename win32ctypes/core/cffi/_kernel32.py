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
typedef WINBOOL (*ENUMRESTYPEPROC) (HANDLE, LPTSTR, LONG);

BOOL Beep(DWORD dwFreq, DWORD dwDuration);
UINT GetACP(void);
HMODULE LoadLibraryExW(LPCTSTR lpFileName, HANDLE hFile, DWORD dwFlags);
BOOL FreeLibrary(HMODULE hModule);
BOOL EnumResourceTypesW(
   HMODULE hModule, ENUMRESTYPEPROC lpEnumFunc, LONG_PTR lParam);

""")

kernel32 = ffi.dlopen('kernel32.dll')


def ENUMRESTYPEPROC(callback):
    def wrapped(hModule, lpszType, LParam):
        if IS_INTRESOURCE(lpszType):
            resource_type = int(ffi.cast("uintptr_t", lpszType))
        else:
            resource_type = ffi.string(lpszType)
        return callback(hModule, resource_type, LParam)
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


def _EnumResourceTypes(hModule, EnumFunc, lParam):
    callback = ffi.callback('ENUMRESTYPEPROC', EnumFunc)
    check_zero(
        kernel32.EnumResourceTypesW(PVOID(hModule), callback, lParam))
