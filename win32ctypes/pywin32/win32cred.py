#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
""" Interface to credentials management functions. """

from __future__ import absolute_import

from win32ctypes.core import _advapi32, _common, _backend
from win32ctypes.pywin32.pywintypes import pywin32error as _pywin32error

CRED_TYPE_GENERIC = 0x1
CRED_PERSIST_ENTERPRISE = 0x3
CRED_PRESERVE_CREDENTIAL_BLOB = 0


def CredWrite(Credential, Flags=CRED_PRESERVE_CREDENTIAL_BLOB):
    """ Creates or updates a stored credential.

    Parameters
    ----------
    Credential : dict
        A dictionary corresponding to the PyWin32 ``PyCREDENTIAL``
        structure.
    Flags : int
        Always pass ``CRED_PRESERVE_CREDENTIAL_BLOB`` (i.e. 0).

    """
    c_creds = _advapi32.CREDENTIAL.fromdict(Credential, Flags)
    c_pcreds = _advapi32.PCREDENTIAL(c_creds)
    with _pywin32error():
        _advapi32.dll._CredWrite(c_pcreds, 0)


def CredRead(TargetName, Type, Flags=0):
    """ Retrieves a stored credential.

    Parameters
    ----------
    TargetName : unicode
        The target name to fetch from the keyring.
    Type : int
        One of the CRED_TYPE_* constants.
    Flags : int
        Reserved, always use 0.

    Returns
    -------
    credentials : dict
        ``None`` if the target name was not found or A dictionary
        corresponding to the PyWin32 ``PyCREDENTIAL`` structure.

    """
    if Type != CRED_TYPE_GENERIC:
        raise ValueError("Type != CRED_TYPE_GENERIC not yet supported")

    flag = 0
    with _pywin32error():
        if _backend == 'cffi':
            ppcreds = _advapi32.PPCREDENTIAL()
            _advapi32.dll._CredRead(TargetName, Type, flag, ppcreds)
            pcreds = _common.dereference(ppcreds)
        else:
            pcreds = _advapi32.PCREDENTIAL()
            _advapi32.dll._CredRead(
                TargetName, Type, flag, _common.byreference(pcreds))
    try:
        return _advapi32.credential2dict(_common.dereference(pcreds))
    finally:
        _advapi32.dll._CredFree(pcreds)


def CredDelete(TargetName, Type, Flags=0):
    """ Remove the given target name from the stored credentials.

    Parameters
    ----------
    TargetName : unicode
        The target name to fetch from the keyring.
    Type : int
        One of the CRED_TYPE_* constants.
    Flags : int
        Reserved, always use 0.

    """
    if not Type == CRED_TYPE_GENERIC:
        raise ValueError("Type != CRED_TYPE_GENERIC not yet supported.")
    with _pywin32error():
        _advapi32.dll._CredDelete(TargetName, Type, 0)
