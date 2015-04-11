#
# (C) Copyright 2015 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from __future__ import absolute_import

from ._util import (
    ffi, check_null, check_zero, HMODULE, PVOID)

ffi.cdef("""

BOOL Beep(DWORD dwFreq, DWORD dwDuration);
UINT GetACP(void);
HMODULE LoadLibraryExW(LPCTSTR lpFileName, HANDLE hFile, DWORD dwFlags);
BOOL FreeLibrary(HMODULE hModule);

""")

kernel32 = ffi.dlopen('kernel32.dll')


def _GetACP():
    return kernel32.GetACP()


def _LoadLibraryEx(lpFilename, hFile, dwFlags):
    result = check_null(
        kernel32.LoadLibraryExW(
            unicode(lpFilename), ffi.NULL, dwFlags))
    return HMODULE(result)


def _FreeLibrary(hModule):
    check_zero(kernel32.FreeLibrary(PVOID(hModule)))
