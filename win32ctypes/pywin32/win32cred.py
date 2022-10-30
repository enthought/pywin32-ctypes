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
        String that contains the filter for the returned credentials. Only 
        credentials with a TargetName matching the filter will be returned. 
        The filter specifies a name prefix followed by an asterisk. For 
        instance, the filter "FRED*" will return all credentials with a 
        TargetName beginning with the string "FRED".
    Flags : int
        The value of this parameter can be zero or more of the following 
        values combined with a bitwise-OR operation.

        CRED_ENUMERATE_ALL_CREDENTIALS (0x1)
        This function enumerates all of the credentials in the user's credential 
        set. The target name of each credential is returned in the 
        "namespace:attribute=target" format. If this flag is set and the 
        Filter parameter is not NULL, the function fails and returns ERROR_INVALID_FLAGS.

    """

    with _pywin32error():
        from win32ctypes.core.cffi._util import PVOID
        if _backend == 'cffi':
            ffi = _authentication.ffi
            pppcreds = _authentication.PPPCREDENTIAL()
            #pcount = ffi.new("DWORD *")
            pcount = _authentication.PDWORD()
            _authentication._CredEnumerate(Filter, Flags, pcount, pppcreds)
            count = pcount[0]
            pppcreds = ffi.cast(f"PCREDENTIAL*[{count}]", pppcreds)
            ppcreds = _common.dereference(pppcreds)
        else:
            raise NotImplementedError("Only cffi backend is supported")
    try:
        result_list = []
        for i in range(count):
            x = _authentication.credential2dict(ppcreds[i])
            result_list.append(x)
        return result_list
    finally:
        _authentication._CredFree(ppcreds)
        
    return []
