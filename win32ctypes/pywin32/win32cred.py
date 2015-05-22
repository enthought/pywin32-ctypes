#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from __future__ import absolute_import

from win32ctypes.core import _advapi32, _common
from win32ctypes.pywin32.pywintypes import pywin32error

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
    c_creds = _advapi32.CREDENTIAL.fromdict(credential, flag)
    c_pcreds = _advapi32.PCREDENTIAL(c_creds)
    with pywin32error():
        _advapi32._CredWrite(c_pcreds, 0)


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
    ppcreds = _advapi32.PPCREDENTIAL()
    with pywin32error():
        _advapi32._CredRead(
            TargetName, Type, flag, ppcreds)
    try:
        return _advapi32.pcredential2dict(_common.dereference(ppcreds))
    finally:
        _advapi32._CredFree(ppcreds)


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
    with pywin32error():
        _advapi32._CredDelete(TargetName, Type, 0)
