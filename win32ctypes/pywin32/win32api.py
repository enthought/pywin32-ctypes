#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
""" A module, encapsulating the Windows Win32 API. """

from __future__ import absolute_import

from win32ctypes.core import _common, _kernel32, _backend
from win32ctypes.pywin32.pywintypes import pywin32error as _pywin32error

LOAD_LIBRARY_AS_DATAFILE = 0x2
LANG_NEUTRAL = 0x00


def LoadLibraryEx(fileName, handle, flags):
    """ Loads the specified DLL, and returns the handle.

    Parameters
    ----------
    fileName : unicode
        The filename of the module to load.

    handle : int
        Reserved, always zero.

    flags : int
        The action to be taken when loading the module.

    Returns
    -------
    handle : hModule
        The handle of the loaded module

    See also
    --------
    - `LoadLibraryEx MSDN reference <https://msdn.microsoft.com/en-us/library/windows/desktop/ms684179(v=vs.85).aspx>`_

    """
    if not handle == 0:
        raise ValueError("handle != 0 not supported")
    with _pywin32error():
        return _kernel32.dll._LoadLibraryEx(fileName, 0, flags)


def EnumResourceTypes(hModule):
    """ Enumerates resource types within a module.

    Parameters
    ----------
    hModule : handle
        The handle to the module.

    Returns
    -------
    resource_types : list
       The list of resource types in the module.

    See also
    --------
    - `EnumResourceTypes MSDN reference <https://msdn.microsoft.com/en-us/library/windows/desktop/ms648039(v=vs.85).aspx>`_

    """
    resource_types = []

    def callback(hModule, type_, param):
        resource_types.append(type_)
        return True

    with _pywin32error():
        _kernel32.dll._EnumResourceTypes(
            hModule, _kernel32.ENUMRESTYPEPROC(callback), 0)
    return resource_types


def EnumResourceNames(hModule, resType):
    """ Enumerates all the resources of the specified type within a module.

    Parameters
    ----------
    hModule : handle
        The handle to the module.
    resType : str : int
        The type of resource to enumerate. If ``resType`` is a string
        starting with '#' is should be followed by the decimal number
        that define the integer resource type identifier.

    Returns
    -------
    resource_names : list
       The list of resource names (unicode strings) of the specific
       resource type in the module.

    See also
    --------
    - `EnumResourceNames MSDN reference <https://msdn.microsoft.com/en-us/library/windows/desktop/ms648037(v=vs.85).aspx>`_
    - `Predefined resource types <https://msdn.microsoft.com/en-us/library/windows/desktop/ms648009(v=vs.85).aspx>`_

    """
    resource_names = []

    def callback(hModule, type_, type_name, param):
        resource_names.append(type_name)
        return True

    with _pywin32error():
        _kernel32.dll._EnumResourceNames(
            hModule, resType, _kernel32.ENUMRESNAMEPROC(callback), 0)
    return resource_names


def EnumResourceLanguages(hModule, lpType, lpName):
    """ List languages of a resource module.

    Parameters
    ----------
    hModule : handle
        Handle to the resource module.

    lpType : str : int
        The type of resource to enumerate. If ``lpType`` is a string
        starting with '#', it should be followed by the decimal number
        that define the integer resource type identifier.

    lpName : str : int
        The name of resource to enumerate. If ``lpType`` is a string
        starting with '#', it should be followed by the decimal number
        that define the integer resource type identifier.

    Returns
    -------
    resource_languages : list
        List of the resource language ids.


    See also
    --------
    - `EnumResourceLanguages MSDN reference <https://msdn.microsoft.com/en-us/library/windows/desktop/ms648035(v=vs.85).aspx>`_
    - `Predefined resource types <https://msdn.microsoft.com/en-us/library/windows/desktop/ms648009(v=vs.85).aspx>`_
    - `Predefined resource language ids <https://msdn.microsoft.com/en-us/library/windows/desktop/dd318693(v=vs.85).aspx>`_

    """
    resource_languages = []

    def callback(hModule, type_name, res_name, language_id, param):
        resource_languages.append(language_id)
        return True

    with _pywin32error():
        _kernel32.dll._EnumResourceLanguages(
            hModule, lpType, lpName,
            _kernel32.ENUMRESLANGPROC(callback), 0)
    return resource_languages


def LoadResource(hModule, type, name, language=LANG_NEUTRAL):
    """ Find and Load a resource component.

    Parameters
    ----------
    handle : hModule
        The handle of the module containing the resource.
        Use None for current process executable.

    type : str : int
        The type of resource to load.

    name : str : int
        The name or Id of the resource to load.

    language : int
        Language to use, default is LANG_NEUTRAL.

    Returns
    -------
    resource : bytes
        The byte string blob of the resource

    See also
    --------
    - `FindResourceEx MSDN reference <https://msdn.microsoft.com/en-us/library/windows/desktop/ms648043(v=vs.85).aspx>`_
    - `SizeofResource MSDN reference <https://msdn.microsoft.com/en-us/library/windows/desktop/ms648048(v=vs.85).aspx>`_
    - `LoadResource MSDN reference <https://msdn.microsoft.com/en-us/library/windows/desktop/ms648046(v=vs.85).aspx>`_
    - `LockResource MSDN reference <https://msdn.microsoft.com/en-us/library/windows/desktop/ms648047(v=vs.85).aspx>`_
    - `Predefined resource types <https://msdn.microsoft.com/en-us/library/windows/desktop/ms648009(v=vs.85).aspx>`_
    - `Predefined resource language ids <https://msdn.microsoft.com/en-us/library/windows/desktop/dd318693(v=vs.85).aspx>`_

    """
    with _pywin32error():
        hrsrc = _kernel32.dll._FindResourceEx(hModule, type, name, language)
        size = _kernel32.dll._SizeofResource(hModule, hrsrc)
        hglob = _kernel32.dll._LoadResource(hModule, hrsrc)
        if _backend == 'ctypes':
            pointer = _common.cast(
                _kernel32.dll._LockResource(hglob), _common.c_char_p)
        else:
            pointer = _kernel32.dll._LockResource(hglob)
        return _common.pythonapi._PyBytes_FromStringAndSize(pointer, size)


def FreeLibrary(hModule):
    """ Free the loaded dynamic-link library (DLL) module.

    If necessary, decrements its reference count.

    Parameters
    ----------
    handle : hModule
        The handle to the library as returned by the LoadLibrary function.

    """
    with _pywin32error():
        return _kernel32.dll._FreeLibrary(hModule)


def GetTickCount():
    """ The number of milliseconds that have elapsed since startup

    Returns
    -------
    counts : int
        The millisecond counts since system startup. Can count up
        to 49.7 days.

    See also
    --------
    - `GetTickCount MSDN reference <https://msdn.microsoft.com/en-us/library/windows/desktop/ms724408%28v=vs.85%29.aspx>`_

    """
    return _kernel32.dll._GetTickCount()


def BeginUpdateResource(filename, delete):
    """ Get a handle that can be used by the :func:`UpdateResource`.

    Parameters
    ----------
    fileName : unicode
        The filename of the module to load.
    delete : bool
        When true all existing resources are deleted

    Returns
    -------
    result : hModule
        Handle of the resource.

    See also
    --------
    - `BeginUpdateResource MSDN reference <https://msdn.microsoft.com/en-us/library/windows/desktop/ms648030(v=vs.85).aspx>`_

    """
    with _pywin32error():
        return _kernel32.dll._BeginUpdateResource(filename, delete)


def EndUpdateResource(handle, discard):
    """ End the update resource of the handle.

    Parameters
    ----------
    handle : hModule
        The handle of the resource as it is returned
        by :func:`BeginUpdateResource`

    discard : bool
        When True all writes are discarded.

    See also
    --------
    - `EndUpdateResource MSDN reference <https://msdn.microsoft.com/en-us/library/windows/desktop/ms648032(v=vs.85).aspx>`_

    """
    with _pywin32error():
        _kernel32.dll._EndUpdateResource(handle, discard)


def UpdateResource(handle, type, name, data, language=LANG_NEUTRAL):
    """ Update a resource.

    Parameters
    ----------
    handle : hModule
        The handle of the resource file as returned by
        :func:`BeginUpdateResource`.

    type : str : int
        The type of resource to update.

    name : str : int
        The name or Id of the resource to update.

    data : bytes
        A bytes like object is expected.

    language : int
        Language to use, default is LANG_NEUTRAL.

    See also
    --------
    - `UpdateResource MSDN reference <https://msdn.microsoft.com/en-us/library/windows/desktop/ms648049(v=vs.85).aspx>`_

    """
    with _pywin32error():
        try:
            lp_data = bytes(data)
        except UnicodeEncodeError:
            # FIXME: In python 2.7 pipywin32219 can handle unicode.
            #        However the data are stored as bytes and it
            #        is not really possible to convert the information
            #        back into the original unicode string. This looks
            #        like a bug so we follow the python 3 behavior.
            raise TypeError(
                "a bytes-like object is required, not a 'unicode'")
        _kernel32.dll._UpdateResource(
            handle, type, name, language, lp_data, len(lp_data))


def GetWindowsDirectory():
    """ Get the ``Windows`` directory.

    Returns
    -------
    result : str
        The path to the ``Windows`` directory.

    See also
    --------
    - `GetWindowsDirectory MSDN reference <https://msdn.microsoft.com/en-us/library/windows/desktop/ms648049(v=vs.85).aspx>`_

    """
    with _pywin32error():
        # Note: pywin32 returns str on py27, unicode (which is str) on py3
        return str(_kernel32.dll._GetWindowsDirectory())


def GetSystemDirectory():
    """ Get the ``System`` directory.

    Returns
    -------
    result : str
        The path to the ``System`` directory.

    See also
    --------
    - `GetSystemDirectory MSDN reference <https://msdn.microsoft.com/en-us/library/windows/desktop/ms724373(v=vs.85).aspx>`_

    """
    with _pywin32error():
        # Note: pywin32 returns str on py27, unicode (which is str) on py3
        return str(_kernel32.dll._GetSystemDirectory())
