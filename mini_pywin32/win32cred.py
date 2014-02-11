import ctypes

from .compat import unicode_str
from .errors import MiniPyWin32Exception

from . import _win32cred

__all__ = ["CredWrite", "CredRead", "CRED_TYPE_GENERIC", "CRED_PERSIST_ENTERPRISE"]

CRED_TYPE_GENERIC = 0x1
CRED_PERSIST_ENTERPRISE = 0x3

def _encode_password(password):
    return unicode_str(password)

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
    supported_keys = ("Type", "TargetName", "CredentialBlob", "Persist",
                      "UserName", "Comment")

    for k in credential:
        if not k in supported_keys:
            raise ValueError("Unsupported key: {0}".format(k))
    if flag != 0:
        raise ValueError("flag != 0 not yet supported")

    c_creds = _win32cred.CREDENTIAL()
    c_pcreds = ctypes.pointer(c_creds)

    ctypes.memset(c_pcreds, 0, ctypes.sizeof(c_creds))

    if "Type" in credential:
        c_creds.Type = credential["Type"]
    if "TargetName" in credential:
        c_creds.TargetName = credential["TargetName"]
    if "Persist" in credential:
        c_creds.Persist = credential["Persist"]
    if "UserName" in credential:
        c_creds.UserName = credential["UserName"]
    if "Comment" in credential:
        c_creds.Comment = credential["Comment"]
    if "CredentialBlob" in credential:
        blob = _encode_password(credential["CredentialBlob"])
        blob_data = ctypes.create_string_buffer(blob)
        # FIXME: I don't know what I am doing here...
        c_creds.CredentialBlobSize = len(blob)
        c_creds.CredentialBlob = ctypes.cast(blob_data, _win32cred.LPBYTE)

    res = _win32cred._CredWrite(c_pcreds, 0)
    if res != 1:
        raise MiniPyWin32Exception("Error while writing creds")

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
    """
    if not Type == CRED_TYPE_GENERIC:
        raise MiniPyWin32Exception("Type != CRED_TYPE_GENERIC not yet supported")

    c_target = ctypes.c_wchar_p(TargetName)
    c_type = Type
    c_flag = 0
    c_pcreds = _win32cred.PCREDENTIAL()

    res = _win32cred._CredRead(c_target, c_type, c_flag, ctypes.byref(c_pcreds))
    if res != 1:
        raise MiniPyWin32Exception("Error while reading creds")

    try:
        c_creds = c_pcreds.contents
        res = {}
        res["UserName"] = c_creds.UserName
        blob = _win32cred._PyString_FromStringAndSize(c_creds.CredentialBlob,
                c_creds.CredentialBlobSize)
        res["CredentialBlob"] = blob
        res["Comment"] = c_creds.Comment
        res["TargetName"] = c_creds.TargetName
        return res
    finally:
        _win32cred.advapi.CredFree(c_pcreds)
