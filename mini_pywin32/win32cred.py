import ctypes

from ._common import _PyString_FromStringAndSize
from . import _win32cred

__all__ = [
    "CredWrite", "CredRead", "CRED_TYPE_GENERIC", "CRED_PERSIST_ENTERPRISE"]

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
                blob = _win32cred._encode_password(credential[
                    'CredentialBlob'])
                blob_data = ctypes.create_string_buffer(blob)
                # FIXME: I don't know what I am doing here...
                c_creds.CredentialBlobSize = len(blob)
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
                blob = _PyString_FromStringAndSize(
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
