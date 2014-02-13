"""
A pure python, ctypes-based replacement for win32cred features required by
keyring.
"""
from __future__ import absolute_import

import ctypes
from ctypes import POINTER, Structure
from ctypes.wintypes import (
    BOOL, DWORD, FILETIME, c_void_p, c_wchar_p, LPCWSTR)

from ._common import LPBYTE
from ._util import function_factory, check_zero


def _encode_password(password):
    return unicode(password)


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

SUPPORTED_CREDKEYS = {
    'Type', 'TargetName', 'Persist', 'UserName', 'Comment', 'CredentialBlob'}

advapi = ctypes.windll.advapi32

_CredWrite = function_factory(
    advapi.CredWriteW,
    [PCREDENTIAL, DWORD],
    BOOL,
    check_zero)

_CredRead = function_factory(
    advapi.CredReadW,
    [LPCWSTR, DWORD, DWORD, POINTER(PCREDENTIAL)],
    BOOL,
    check_zero)

_CredDelete = function_factory(
    advapi.CredDeleteW,
    [LPCWSTR, DWORD, DWORD],
    BOOL,
    check_zero)

