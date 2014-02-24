#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

__all__ = [
    "CredWrite", "CredRead", "CRED_TYPE_GENERIC", "CRED_PERSIST_ENTERPRISE"]

import ctypes

from ._common import _PyBytes_FromStringAndSize, _GetACP
from .compat import is_unicode, unicode
from . import _win32cred

CRED_TYPE_GENERIC = 0x1
CRED_PERSIST_ENTERPRISE = 0x3


def CredWrite(credential, flag):
    """
    Mimic pywin32 win32cred.CredWrite.

    Parameters
    ----------
    credential: dict
        Dict of parameters to be passed to win32 API CredWrite
    flag: int

    Returns
    -------
    credentials: dict
        A dictionary containing the following:

            - Type: the type of credential (see MSDN)
            - TargetName: the target to use (string)
            - Persist: see MSDN
            - UserName: the retrieved username
            - CredentialBlob: the password (as a *string*, not an encoded
              binary stream - this function takes care of the encoding).
            - Comment: a string
    """

    unsupported = set(credential.keys()) - _win32cred.SUPPORTED_CREDKEYS
    if len(unsupported):
        raise ValueError("Unsupported keys: {0}".format(unsupported))
    if flag != 0:
        raise ValueError("flag != 0 not yet supported")

    c_creds = _win32cred.CREDENTIAL()
    c_pcreds = ctypes.pointer(c_creds)

    ctypes.memset(c_pcreds, flag, ctypes.sizeof(c_creds))

    for key in _win32cred.SUPPORTED_CREDKEYS:
        if key in credential:
            if key != 'CredentialBlob':
                setattr(c_creds, key, credential[key])
            else:
                blob = _make_blob(credential['CredentialBlob'])
                blob_data = ctypes.create_unicode_buffer(blob)
                # Create_unicode_buffer adds a NULL at the end of the string
                # we do not want that.
                c_creds.CredentialBlobSize = \
                    ctypes.sizeof(blob_data) - ctypes.sizeof(ctypes.c_wchar)
                c_creds.CredentialBlob = ctypes.cast(
                    blob_data, _win32cred.LPBYTE)

    _win32cred._CredWrite(c_pcreds, 0)


def CredRead(TargetName, Type):
    """
    Mimic pywin32 win32cred.CreadRead.

    Parameters
    ----------
    TargetName: str-like
        The target name to fetch from the keyring.

    Returns
    -------
    credentials: dict
        A dictionary containing the following:

            - UserName: the retrieved username
            - CredentialBlob: the password (as an utf-16 encoded 'string')

        None if the target name was not found.
    """
    if not Type == CRED_TYPE_GENERIC:
        raise ValueError("Type != CRED_TYPE_GENERIC not yet supported")

    flag = 0
    c_pcreds = _win32cred.PCREDENTIAL()

    _win32cred._CredRead(TargetName, Type, flag, ctypes.byref(c_pcreds))
    try:
        c_creds = c_pcreds.contents
        credential = {}
        for key in _win32cred.SUPPORTED_CREDKEYS:
            if key != 'CredentialBlob':
                credential[key] = getattr(c_creds, key)
            else:
                blob = _PyBytes_FromStringAndSize(
                    c_creds.CredentialBlob, c_creds.CredentialBlobSize)
                credential['CredentialBlob'] = blob
        return credential
    finally:
        _win32cred.advapi.CredFree(c_pcreds)


def CredDelete(TargetName, Type):
    """
    Remove the given target name from the stored credentials.

    Mimic pywin32 win32cred.CreadDelete.

    Parameters
    ----------
    TargetName: str-like
        The target name to fetch from the keyring.
    """
    if not Type == CRED_TYPE_GENERIC:
        raise ValueError("Type != CRED_TYPE_GENERIC not yet supported.")
    _win32cred._CredDelete(TargetName, Type, 0)


def _make_blob(password):
    """ Convert the input string password into a unicode blob as required for
    Credentials.

    """
    if is_unicode(password):
        return password
    else:
        code_page = _GetACP()
        return unicode(password, encoding=str(code_page), errors='strict')
