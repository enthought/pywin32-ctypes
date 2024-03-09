#
# (C) Copyright 2014-2024 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
import ctypes
from ctypes import POINTER, Structure, c_char_p, cast
from ctypes.wintypes import (
    BOOL, DWORD, FILETIME, LPCWSTR, LPWSTR)

from ._common import LPBYTE, _PyBytes_FromStringAndSize
from ._util import function_factory, check_false_factory, dlls


class CREDENTIAL_ATTRIBUTE(Structure):
    _fields_ = [
        ('Keyword', LPWSTR),
        ('Flags', DWORD),
        ('ValueSize', DWORD),
        ('Value', LPBYTE)]

    @classmethod
    def fromdict(cls, attribute):
        c_attribute = cls()
        c_pattribute = PCREDENTIAL_ATTRIBUTE(c_attribute)
        ctypes.memset(c_pattribute, 0, ctypes.sizeof(c_attribute))
        c_attribute.populate(attribute)
        return c_attribute

    def populate(self, attribute):
        # Transfer values
        self.Keyword = attribute['Keyword']
        self.Flags = attribute.get('Flags', 0)
        value = attribute['Value']
        blob = c_char_p(value)
        self.Value = cast(blob, LPBYTE)
        self.ValueSize = len(value)


PCREDENTIAL_ATTRIBUTE = POINTER(CREDENTIAL_ATTRIBUTE)


class CREDENTIAL(Structure):
    _fields_ = [
        ('Flags', DWORD),
        ('Type', DWORD),
        ('TargetName', LPWSTR),
        ('Comment', LPWSTR),
        ('LastWritten', FILETIME),
        ('CredentialBlobSize', DWORD),
        ('CredentialBlob', LPBYTE),
        ('Persist', DWORD),
        ('AttributeCount', DWORD),
        ('Attributes', PCREDENTIAL_ATTRIBUTE),
        ('TargetAlias', LPWSTR),
        ('UserName', LPWSTR)]

    @classmethod
    def fromdict(cls, credential):
        c_credentials = cls()
        c_pcredentials = PCREDENTIAL(c_credentials)
        ctypes.memset(c_pcredentials, 0, ctypes.sizeof(c_credentials))
        for key in credential:
            if key == 'CredentialBlob':
                blob_data, blob_size = _make_blob(credential['CredentialBlob'])
                c_credentials.CredentialBlob = blob_data
                c_credentials.CredentialBlobSize = blob_size
            elif key == 'Attributes':
                attributes = credential.get('Attributes', '')
                count = len(attributes)
                if count == 0:
                    continue
                data = (PCREDENTIAL_ATTRIBUTE * count)()
                for index in range(count):
                    attribute = CREDENTIAL_ATTRIBUTE.fromdict(
                        attributes[index])
                    data[index] = PCREDENTIAL_ATTRIBUTE(attribute)
                c_credentials.Attributes = cast(data, PCREDENTIAL_ATTRIBUTE)
                c_credentials.AttributeCount = count
            else:
                setattr(c_credentials, key, credential[key])
        return c_credentials


_data = []
PCREDENTIAL = POINTER(CREDENTIAL)
PPCREDENTIAL = POINTER(PCREDENTIAL)
PPPCREDENTIAL = POINTER(PPCREDENTIAL)


def credential_attribute2dict(c_attribute):
    attribute = {}
    attribute['Keyword'] = c_attribute.Keyword
    attribute['Flags'] = c_attribute.Flags
    size = c_attribute.ValueSize
    if size > 0:
        value = _PyBytes_FromStringAndSize(
            cast(c_attribute.Value, c_char_p), size)
        attribute['Value'] = value
    return attribute


def credential2dict(c_credential):
    credential = {}

    for key, type_ in CREDENTIAL._fields_:
        if key == 'CredentialBlob':
            blob = _PyBytes_FromStringAndSize(
                cast(c_credential.CredentialBlob, c_char_p),
                c_credential.CredentialBlobSize)
            credential['CredentialBlob'] = blob
        elif key == 'Attributes':
            attributes = []
            count = c_credential.AttributeCount
            data = c_credential.Attributes
            for index in range(count):
                attribute = credential_attribute2dict(data[index])
                attributes.append(attribute)
            credential['Attributes'] = tuple(attributes)
        else:
            credential[key] = getattr(c_credential, key)
    return credential


def _make_blob(data):
    ''' Convert a string to LPBYTE compatible blob dict values

    '''
    blob_data = ctypes.create_unicode_buffer(data)
    # Create_unicode_buffer adds a NULL at the end of the
    # string we do not want that.
    blob_size = (
        ctypes.sizeof(blob_data) - ctypes.sizeof(ctypes.c_wchar))
    blob_pointer = cast(blob_data, LPBYTE)
    return blob_pointer, blob_size


_CredWrite = function_factory(
    dlls.advapi32.CredWriteW,
    [PCREDENTIAL, DWORD],
    BOOL,
    check_false_factory('CredWrite'))

_CredRead = function_factory(
    dlls.advapi32.CredReadW,
    [LPCWSTR, DWORD, DWORD, PPCREDENTIAL],
    BOOL,
    check_false_factory('CredRead'))

_CredDelete = function_factory(
    dlls.advapi32.CredDeleteW,
    [LPCWSTR, DWORD, DWORD],
    BOOL,
    check_false_factory('CredDelete'))

_CredEnumerate = function_factory(
    dlls.advapi32.CredEnumerateW,
    [LPCWSTR, DWORD, POINTER(DWORD), PPPCREDENTIAL],
    BOOL,
    check_false_factory('CredEnumerate'))

_CredFree = function_factory(dlls.advapi32.CredFree, [PCREDENTIAL])
