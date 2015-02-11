#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

from __future__ import absolute_import

from win32ctypes.core import _common, _kernel32
from win32ctypes.pywin32.pywintypes import pywin32error

LOAD_LIBRARY_AS_DATAFILE = 0x2


def LoadLibraryEx(FileName, handle, flags):
    if not handle == 0:
        raise ValueError("handle != 0 not supported")
    with pywin32error():
        return _kernel32._LoadLibraryEx(FileName, 0, flags)


def EnumResourceTypes(hModule):
    resource_types = []

    def callback(hModule, typeid, param):
        resource_types.append(typeid)
        return True

    with pywin32error():
        _kernel32._EnumResourceTypes(
            hModule, _kernel32.ENUMRESTYPEPROC(callback), 0)
    return resource_types


def EnumResourceNames(hModule, type_):
    resource_names = []

    def callback(hModule, type_, type_name, param):
        resource_names.append(type_name)
        return True

    with pywin32error():
        _kernel32._EnumResourceNames(
            hModule, type_, _kernel32.ENUMRESNAMEPROC(callback), 0)
    return resource_names


def EnumResourceLanguages(hModule, type_, name):
    resource_languages = []

    def callback(hModule, type_name, res_name, language_id, param):
        resource_languages.append(language_id)
        return True

    with pywin32error():
        _kernel32._EnumResourceLanguages(
            hModule, type_, name, _kernel32.ENUMRESLANGPROC(callback), 0)
    return resource_languages


def LoadResource(hModule, type_, name, language):
    with pywin32error():
        hrsrc = _kernel32._FindResourceEx(hModule, type_, name, language)
        size = _kernel32._SizeofResource(hModule, hrsrc)
        hglob = _kernel32._LoadResource(hModule, hrsrc)
        pointer = _kernel32._LockResource(hglob)
    return _common._PyBytes_FromStringAndSize(pointer, size)


def FreeLibrary(hModule):
    with pywin32error():
        return _kernel32._FreeLibrary(hModule)
