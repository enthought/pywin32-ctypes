#
# (C) Copyright 2018 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from __future__ import absolute_import

import ctypes
from ctypes.wintypes import (
    DWORD, HANDLE, POINTER, BOOL, SHORT, WORD, LPDWORD,
    LPCTSTR, CHAR, WCHAR, UINT, LPVOID)


class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ('nlength', DWORD),
        ('ipSecurityDescription', LPVOID),
        ('bInheritHandle', BOOL)]


LPSECURITY_ATTRIBUTES = POINTER(SECURITY_ATTRIBUTES)
