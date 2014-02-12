from __future__ import absolute_import

from . import _win32api, _win32cred

LOAD_LIBRARY_AS_DATAFILE = 0x2


def LoadLibraryEx(FileName, handle, flags):
    if not handle == 0:
        raise ValueError("handle != 0 not supported")
    return _win32api._LoadLibraryEx(FileName, 0, flags)


def EnumResourceTypes(hModule):
    resource_types = []

    def callback(hModule, typeid, lParam):
        resource_types.append(typeid)
        return True

    _win32api._EnumResourceTypes(
        hModule, _win32api.ENUMRESTYPEPROC(callback), 0)
    return resource_types


def EnumResourceNames(hModule, Type):
    resource_names = []

    def callback(hModule, type_id, type_name, lParam):
        resource_names.append(type_name)
        return True

    _win32api._EnumResourceNames(
        hModule, Type, _win32api.ENUMRESNAMEPROC(callback), 0)
    return resource_names


def EnumResourceLanguages(hModule, Type, Name):
    resource_languages = []

    def callback(hModule, type_name, res_name, language_id, lParam):
        resource_languages.append(language_id)
        return True

    _win32api._EnumResourceLanguages(hModule, Type, Name, callback, None)
    return resource_languages


def LoadResource(hModule, type_, name, language):
    hrsrc = _win32api._FindResourceEx(hModule, type_, name, language)
    size = _win32api._SizeofResource(hModule, hrsrc)
    hglob = _win32api._LoadResource(hModule, hrsrc)
    pointer = _win32api._LockResource(hglob)
    return _win32cred._PyString_FromStringAndSize(pointer, size)


def FreeLibrary(hModule):
    return _win32api._FreeLibrary(hModule)
