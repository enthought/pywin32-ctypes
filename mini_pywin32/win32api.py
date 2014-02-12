from __future__ import absolute_import

from ctypes.wintypes import WORD


from . import _win32api, _win32cred

LOAD_LIBRARY_AS_DATAFILE = 0x2


def LoadLibraryEx(FileName, handle, flags):
    if not handle == 0:
        raise ValueError("handle != 0 not supported")
    c_filename = _win32api.LPCWSTR(FileName)
    c_flags = flags

    return _win32api._LoadLibraryEx(c_filename, 0, c_flags)


def EnumResourceTypes(hModule):
    resource_types = []

    def callback(hModule, typeid, lParam):
        resource_types.append(typeid)
        return True
    _win32api._EnumResourceTypes(
        hModule, _win32api._EnumResTypeProc(callback), None)
    return resource_types


def EnumResourceNames(hModule, Type):
    c_hmodule = _win32api.HMODULE(hModule)
    c_type = Type

    resource_names = []

    def callback(hModule, type_id, type_name, lParam):
        resource_names.append(type_name)
        return True
    _win32api._EnumResourceNames(
        c_hmodule, c_type, _win32api._EnumResNameProc(callback), None)
    return resource_names


def EnumResourceLanguages(hModule, Type, Name):
    c_hmodule = _win32api.HMODULE(hModule)
    c_type = Type
    c_name = Name

    resource_languages = []

    def callback(hModule, type_name, res_name, language_id, lParam):
        resource_languages.append(language_id)
        return True
    _win32api._EnumResourceLanguages(
        c_hmodule, c_type, c_name,
        _win32api._EnumResLanguagesProc(callback), None)
    return resource_languages


def LoadResource(hModule, type_, name, language):
    c_hModule = _win32api.HMODULE(hModule)
    c_type = type_
    c_name = name
    c_language = WORD(language)

    c_hrsrc = _win32api._FindResourceEx(c_hModule, c_type, c_name, c_language)

    assert c_hrsrc is not None, "Error handling missing"
    c_size = _win32api._SizeofResource(c_hModule, c_hrsrc)
    assert c_size != 0, "Error handling missing"
    c_hglob = _win32api._LoadResource(c_hModule, c_hrsrc)
    assert c_hglob is not None, "Error handling missing"
    c_pointer = _win32api._LockResource(c_hglob)
    assert c_hglob is not None, "Error handling missing"
    return _win32cred._PyString_FromStringAndSize(c_pointer, c_size)


def FreeLibrary(hModule):
    c_hModule = _win32api.HMODULE(hModule)
    return _win32api._FreeLibrary(c_hModule)
