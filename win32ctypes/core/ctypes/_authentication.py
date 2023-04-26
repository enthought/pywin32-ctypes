#
# (C) Copyright 2014-18 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
import ctypes
from ctypes import POINTER, Structure, c_void_p, c_wchar_p, c_char_p, cast
from ctypes.wintypes import (
    BOOL, DWORD, FILETIME, LPCWSTR)

from win32ctypes.core.compat import is_text
from ._common import LPBYTE, _PyBytes_FromStringAndSize
from ._util import function_factory, check_false_factory, dlls
from ._nl_support import _GetACP


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
        ("AttributeCount", DWORD),
        ("Attribute", c_void_p),
        ("TargetAlias", c_wchar_p),
        ("UserName", c_wchar_p)]

    @classmethod
    def fromdict(cls, credential):
        c_creds = cls()
        c_pcreds = PCREDENTIAL(c_creds)

        # zero-out memory
        ctypes.memset(c_pcreds, 0, ctypes.sizeof(c_creds))

        for key in credential:
            if key == 'CredentialBlob':
                blob_data, blob_size = _make_blob(credential['CredentialBlob'])
                c_creds.CredentialBlob = ctypes.cast(blob_data, LPBYTE)
                c_creds.CredentialBlobSize = blob_size
            else:
                setattr(c_creds, key, credential[key])
        return c_creds


PCREDENTIAL = POINTER(CREDENTIAL)
PPCREDENTIAL = POINTER(PCREDENTIAL)
PPPCREDENTIAL = POINTER(PPCREDENTIAL)


def credential2dict(creds):
    credential = {}
    for key, type_ in CREDENTIAL._fields_:
        if key == u'CredentialBlob':
            blob = _PyBytes_FromStringAndSize(
                cast(creds.CredentialBlob, c_char_p),
                creds.CredentialBlobSize)
            credential[u'CredentialBlob'] = blob
        else:
            credential[key] = getattr(creds, key)
    return credential


def _make_blob(data):
    """ Convert a string to credential compatible blob dict values

    """
    blob_data = ctypes.create_unicode_buffer(data)
    # Create_unicode_buffer adds a NULL at the end of the
    # string we do not want that.
    blob_size = (
        ctypes.sizeof(blob_data) - ctypes.sizeof(ctypes.c_wchar))
    blob_pointer = ctypes.cast(blob_data, LPBYTE)
    return blob_pointer, blob_size


_CredWrite = function_factory(
    dlls.advapi32.CredWriteW,
    [PCREDENTIAL, DWORD],
    BOOL,
    check_false_factory("CredWrite"))

_CredRead = function_factory(
    dlls.advapi32.CredReadW,
    [LPCWSTR, DWORD, DWORD, PPCREDENTIAL],
    BOOL,
    check_false_factory("CredRead"))

_CredDelete = function_factory(
    dlls.advapi32.CredDeleteW,
    [LPCWSTR, DWORD, DWORD],
    BOOL,
    check_false_factory("CredDelete"))

_CredEnumerate = function_factory(
    dlls.advapi32.CredEnumerateW,
    [LPCWSTR, DWORD, POINTER(DWORD), PPPCREDENTIAL],
    BOOL,
    check_false_factory("CredEnumerate"))

_CredFree = function_factory(dlls.advapi32.CredFree, [PCREDENTIAL])
