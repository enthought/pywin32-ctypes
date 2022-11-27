#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
""" Interface to credentials management functions. """
from win32ctypes.core import _authentication, _common, _backend
from win32ctypes.pywin32.pywintypes import pywin32error as _pywin32error

CRED_TYPE_GENERIC = 0x1
CRED_PERSIST_SESSION = 0x1
CRED_PERSIST_LOCAL_MACHINE = 0x2
CRED_PERSIST_ENTERPRISE = 0x3
CRED_PRESERVE_CREDENTIAL_BLOB = 0
CRED_ENUMERATE_ALL_CREDENTIALS = 0x1


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
    c_creds = _authentication.CREDENTIAL.fromdict(Credential, Flags)
    c_pcreds = _authentication.PCREDENTIAL(c_creds)
    with _pywin32error():
        _authentication._CredWrite(c_pcreds, 0)


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
            ppcreds = _authentication.PPCREDENTIAL()
            _authentication._CredRead(TargetName, Type, flag, ppcreds)
            pcreds = _common.dereference(ppcreds)
        else:
            pcreds = _authentication.PCREDENTIAL()
            _authentication._CredRead(
                TargetName, Type, flag, _common.byreference(pcreds))
    try:
        return _authentication.credential2dict(_common.dereference(pcreds))
    finally:
        _authentication._CredFree(pcreds)


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
        _authentication._CredDelete(TargetName, Type, 0)


def CredEnumerate(Filter=None, Flags=0):
    """ Remove the given target name from the stored credentials.

    Parameters
    ----------
    Filter : unicode
        Matches credentials' target names by prefix, can be None.
    Flags : int
        Reserved, use 0 if passed in.

    Returns
    -------
    credentials : list
        Returns a sequence of CREDENTIAL dictionaries.

    """
    with _pywin32error():
        if _backend == 'cffi':
            pcount = _common.PDWORD()
            pppcreds = _authentication.PPPCREDENTIAL()
            _authentication._CredEnumerate(Filter, Flags, pcount, pppcreds)
            count = pcount[0]
            pppcreds = _common.ffi.cast(f"PCREDENTIAL*[{count}]", pppcreds)
            ppcreds = _common.dereference(pppcreds)
        else:
            import ctypes
            count = _common.DWORD()
            # Create a mutable pointer variable
            mem = ctypes.create_string_buffer(1)
            pppcreds = _common.cast(
                mem, _authentication.PPPCREDENTIAL)
            _authentication._CredEnumerate(
                Filter, Flags, _common.byreference(count), pppcreds)
            count = count.value
            pcreds = _common.dereference(_common.dereference(pppcreds))
    try:
        return [
            _authentication.credential2dict(pcreds[i])
            for i in range(count)]
    finally:
        _authentication._CredFree(pcreds)
