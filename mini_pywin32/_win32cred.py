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
    return unicode_str(password).encode("utf-16")

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

advapi = ctypes.windll.advapi32

_CredWrite = advapi.CredWriteW
_CredWrite.argtypes = [PCREDENTIAL, DWORD]
_CredWrite.restype = BOOL

_CredRead = advapi.CredReadW
_CredRead.argtypes = [c_wchar_p, DWORD, DWORD, POINTER(PCREDENTIAL)]
_CredRead.restype = BOOL

_CredDelete = advapi.CredDeleteW
_CredDelete.argtypes = [c_wchar_p, DWORD, DWORD]
_CredDelete.restype = BOOL

_PyString_FromStringAndSize = ctypes.pythonapi.PyString_FromStringAndSize
_PyString_FromStringAndSize.restype = py_object
