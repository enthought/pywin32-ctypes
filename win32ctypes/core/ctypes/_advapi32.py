#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from __future__ import absolute_import

import ctypes
from ctypes import POINTER, Structure, c_void_p, c_wchar_p, c_char_p, cast
from ctypes.wintypes import (
    BOOL, DWORD, FILETIME, LPCWSTR)

from win32ctypes.core.compat import is_unicode
from ._common import LPBYTE, pythonapi
from ._util import check_zero, Wrapping as W, DLL
from . import _kernel32


SUPPORTED_CREDKEYS = set((
    u'Type', u'TargetName', u'Persist',
    u'UserName', u'Comment', u'CredentialBlob'))


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

    @classmethod
    def fromdict(cls, credential, flags=0):
        unsupported = set(credential.keys()) - SUPPORTED_CREDKEYS
        if len(unsupported):
            raise ValueError("Unsupported keys: {0}".format(unsupported))
        if flags != 0:
            raise ValueError("flag != 0 not yet supported")

        c_creds = cls()
        c_pcreds = PCREDENTIAL(c_creds)

        # zero-out memory
        ctypes.memset(c_pcreds, 0, ctypes.sizeof(c_creds))

        for key in SUPPORTED_CREDKEYS:
            if key in credential:
                if key != 'CredentialBlob':
                    setattr(c_creds, key, credential[key])
                else:
                    blob = make_unicode(credential['CredentialBlob'])
                    blob_data = ctypes.create_unicode_buffer(blob)
                    # Create_unicode_buffer adds a NULL at the end of the
                    # string we do not want that.
                    c_creds.CredentialBlobSize = \
                        ctypes.sizeof(blob_data) - \
                        ctypes.sizeof(ctypes.c_wchar)
                    c_creds.CredentialBlob = ctypes.cast(blob_data, LPBYTE)
        return c_creds


PCREDENTIAL = POINTER(CREDENTIAL)


def make_unicode(password):
    """ Convert the input string to unicode.

    """
    if is_unicode(password):
        return password
    else:
        code_page = _kernel32.dll._GetACP()
        return unicode(password, encoding=str(code_page), errors='strict')


def credential2dict(creds):
    credential = {}
    for key in SUPPORTED_CREDKEYS:
        if key != u'CredentialBlob':
            credential[key] = getattr(creds, key)
        else:
            blob = pythonapi._PyBytes_FromStringAndSize(
                cast(creds.CredentialBlob, c_char_p),
                creds.CredentialBlobSize)
            credential[u'CredentialBlob'] = blob
    return credential


wrapped_functions = {
        '_CredWrite': W('CredWriteW', [PCREDENTIAL, DWORD], BOOL, check_zero),
        '_CredRead': W('CredReadW', [LPCWSTR, DWORD, DWORD, POINTER(PCREDENTIAL)], BOOL, check_zero),  # noqa
        '_CredDelete': W('CredDeleteW', [LPCWSTR, DWORD, DWORD], BOOL, check_zero),  # noqa
        '_CredFree': W('CredFree', [PCREDENTIAL], None, None)}

dll = DLL(ctypes.WinDLL('advapi32'), functions=wrapped_functions)
