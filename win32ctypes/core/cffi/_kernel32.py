#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from __future__ import absolute_import

from ._util import ffi, function_factory, check_null

ffi.cdef("""

BOOL Beep(DWORD dwFreq, DWORD dwDuration);
UINT GetACP(void);
HMODULE LoadLibraryExW(LPCTSTR lpFileName, HANDLE hFile, DWORD dwFlags);

""")

kernel32 = ffi.dlopen('kernel32.dll')


def _GetACP():
    return kernel32.GetACP()

def _LoadLibraryEx(lpFilename, hFile, dwFlags):
    filename = ffi.new('LPCTSTR', lpFilename)
    return check_null(
        kernel32.LoadLibraryExW(
            filename, hFile, dwFlags))
