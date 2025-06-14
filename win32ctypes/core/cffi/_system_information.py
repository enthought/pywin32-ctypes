#
# (C) Copyright 2018-2024 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from ._util import ffi, dlls

# TODO: retrieve this value using ffi
MAX_PATH = 260
MAX_PATH_BUF = f'wchar_t[{MAX_PATH}]'


def _GetWindowsDirectory():
    buffer = ffi.new(MAX_PATH_BUF)
    directory = dlls.kernel32.GetWindowsDirectoryW(buffer, MAX_PATH)
    return ffi.unpack(buffer, directory)


def _GetSystemDirectory():
    buffer = ffi.new(MAX_PATH_BUF)
    directory = dlls.kernel32.GetSystemDirectoryW(buffer, MAX_PATH)
    return ffi.unpack(buffer, directory)


def _GetTickCount():
    return dlls.kernel32.GetTickCount()
