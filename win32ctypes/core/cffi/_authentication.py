#
# (C) Copyright 2015-2024 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from win32ctypes.core.compat import is_text
from ._util import ffi, check_false, dlls
from ._nl_support import _GetACP
from ._common import _PyBytes_FromStringAndSize


def make_unicode(password):
    """ Convert the input string to unicode.

    """
    if is_text(password):
        return password
    else:
        code_page = _GetACP()
        return password.decode(encoding=str(code_page), errors='strict')


class _CREDENTIAL(object):

    def __call__(self):
        return ffi.new("PCREDENTIAL")[0]

    @classmethod
    def fromdict(cls, credential, flags=0):
        factory = cls()
        c_credential = factory()
        values = []  # keep values in context during processing
        for key, value in credential.items():
            if key == 'CredentialBlob':
                blob = ffi.new('wchar_t[]', value)
                c_credential.CredentialBlob = ffi.cast('LPBYTE', blob)
                c_credential.CredentialBlobSize = ffi.sizeof(blob) - ffi.sizeof('wchar_t')  # noqa
                values.append(blob)
            elif key == 'Attributes':
                count = len(value)
                if count == 0:
                    continue
                elif count > 1:
                    raise ValueError('Multiple attributes are not supported')
                c_attribute = CREDENTIAL_ATTRIBUTE.fromdict(value[0])
                c_credential.Attributes = PCREDENTIAL_ATTRIBUTE(c_attribute)
                c_credential.AttributeCount = count
                values.append(c_attribute)
            elif key in ('Type', 'Persist', 'Flags'):
                setattr(c_credential, key, value)
            elif key in ('TargetName', 'Comment', 'TargetAlias', 'UserName'):
                if value is None:
                    setattr(c_credential, key, ffi.NULL)
                else:
                    blob_pointer = ffi.new('wchar_t[]', value)
                    setattr(
                        c_credential, key, ffi.cast('LPWSTR', blob_pointer))
                    values.append(blob_pointer)
        return c_credential


class _CREDENTIAL_ATTRIBUTE(object):

    def __call__(self):
        return ffi.new("PCREDENTIAL_ATTRIBUTE")[0]

    @classmethod
    def fromdict(cls, attribute, flags=0):
        factory = cls()
        c_attribute = factory()
        c_attribute.Flags = attribute.get('Flags', flags)
        keyword = attribute.get('Keyword', None)
        if keyword is None:
            c_attribute.Keyword = ffi.NULL
        else:
            blob_pointer = ffi.new('wchar_t[]', keyword)
            c_attribute.Keyword = ffi.cast('LPWSTR', blob_pointer)
        value = attribute['Value']
        if len(value) == 0:
            data, size = ffi.NULL,  0
        elif is_text(value):
            blob = ffi.new('wchar_t[]', value)
            data = ffi.cast('LPBYTE', blob)
            size = ffi.sizeof(blob) - ffi.sizeof('wchar_t')  # noqa
        else:
            data = ffi.new('BYTE[]', value)
            size = ffi.sizeof(blob_pointer) - ffi.sizeof('BYTE')
        c_attribute.Value = data
        c_attribute.ValueSize = size
        return c_attribute


CREDENTIAL = _CREDENTIAL()
CREDENTIAL_ATTRIBUTE = _CREDENTIAL_ATTRIBUTE()


def PCREDENTIAL(value=None):
    return ffi.new("PCREDENTIAL", ffi.NULL if value is None else value)


def PPCREDENTIAL(value=None):
    return ffi.new("PCREDENTIAL*", ffi.NULL if value is None else value)


def PPPCREDENTIAL(value=None):
    return ffi.new("PCREDENTIAL**", ffi.NULL if value is None else value)


def PCREDENTIAL_ATTRIBUTE(value=None):
    return ffi.new(
        "PCREDENTIAL_ATTRIBUTE", ffi.NULL if value is None else value)


def credential_attribute2dict(c_attribute):
    attribute = {}
    keyword = c_attribute.Keyword
    if keyword == ffi.NULL:
        attribute['Keyword'] = None
    else:
        attribute['Keyword'] = ffi.string(keyword)
    attribute['Flags'] = c_attribute.Flags
    size = c_attribute.ValueSize
    if size > 0:
        value = _PyBytes_FromStringAndSize(c_attribute.Value, size)
        attribute['Value'] = value
    return attribute


def credential2dict(c_credential):
    credential = {}
    for key in dir(c_credential):
        if key == 'CredentialBlob':
            data = _PyBytes_FromStringAndSize(
                c_credential.CredentialBlob, c_credential.CredentialBlobSize)
        elif key == 'Attributes':
            attributes = []
            count = c_credential.AttributeCount
            c_attributes = c_credential.Attributes
            for index in range(count):
                attribute = credential_attribute2dict(c_attributes[index])
                attributes.append(attribute)
            data = tuple(attributes)
        elif key == 'LastWritten':
            data = c_credential.LastWritten
        elif key in ('Type', 'Persist', 'Flags'):
            data = int(getattr(c_credential, key))
        elif key in ('TargetName', 'Comment', 'TargetAlias', 'UserName'):
            string_pointer = getattr(c_credential, key)
            if string_pointer == ffi.NULL:
                data = None
            else:
                data = ffi.string(string_pointer)
        else:
            continue
        credential[key] = data
    return credential


def _CredRead(TargetName, Type, Flags, ppCredential):
    target = make_unicode(TargetName)
    return check_false(
        dlls.advapi32.CredReadW(target, Type, Flags, ppCredential),
        'CredRead')


def _CredWrite(Credential, Flags):
    return check_false(
        dlls.advapi32.CredWriteW(Credential, Flags), 'CredWrite')


def _CredDelete(TargetName, Type, Flags):
    return check_false(
        dlls.advapi32.CredDeleteW(
            make_unicode(TargetName), Type, Flags), 'CredDelete')


def _CredEnumerate(Filter, Flags, Count, pppCredential):
    filter = make_unicode(Filter) if Filter is not None else ffi.NULL
    return check_false(
        dlls.advapi32.CredEnumerateW(filter, Flags, Count, pppCredential),
        'CredEnumerate')


_CredFree = dlls.advapi32.CredFree
