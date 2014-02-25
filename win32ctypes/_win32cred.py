#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

"""
A pure python, ctypes-based replacement for win32cred features required by
keyring.
"""
from __future__ import absolute_import

import ctypes
from ctypes import POINTER, Structure, c_void_p, c_wchar_p
from ctypes.wintypes import (
    BOOL, DWORD, FILETIME, LPCWSTR)

from ._common import LPBYTE
from ._util import function_factory, check_zero_factory


class CREDENTIAL(Structure):
    _fields_ = [
        ("Flags", DWORD),
        ("Type", DWORD),
        ("TargetName", c_wchar_p),
        ("Comment", c_wchar_p),
        ("LastWritten", FILETIME),
        ("CredentialBlobSize", DWORD),
        ("CredentialBlob", LPBYTE),
        ("Persist", DWORD),
        ("_DO_NOT_USE_AttributeCount", DWORD),
        ("__DO_NOT_USE_Attribute", c_void_p),
        ("TargetAlias", c_wchar_p),
        ("UserName", c_wchar_p)]
PCREDENTIAL = POINTER(CREDENTIAL)

SUPPORTED_CREDKEYS = set((
    'Type', 'TargetName', 'Persist', 'UserName', 'Comment', 'CredentialBlob'))

advapi = ctypes.windll.advapi32

_CredWrite = function_factory(
    advapi.CredWriteW,
    [PCREDENTIAL, DWORD],
    BOOL,
    check_zero_factory("CredWrite"))

_CredRead = function_factory(
    advapi.CredReadW,
    [LPCWSTR, DWORD, DWORD, POINTER(PCREDENTIAL)],
    BOOL,
    check_zero_factory("CredRead"))

_CredDelete = function_factory(
    advapi.CredDeleteW,
    [LPCWSTR, DWORD, DWORD],
    BOOL,
    check_zero_factory("CredDelete"))
