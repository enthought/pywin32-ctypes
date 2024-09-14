#
# (C) Copyright 2022-2024 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
import unittest

from win32ctypes.core import _backend
from win32ctypes.core._authentication import (
    CREDENTIAL, CREDENTIAL_ATTRIBUTE,
    credential2dict, credential_attribute2dict)
from win32ctypes.core._winbase import FILETIME
from win32ctypes.constants import (
    CRED_TYPE_GENERIC, CRED_PERSIST_ENTERPRISE)


class TestCREDENTIAL(unittest.TestCase):

    maxDiff = None

    def test_fromdict(self):
        # given
        username = 'john'
        password = 'doefsajfsakfj'
        comment = 'Created by MiniPyWin32Cred test suite'
        target = '{0}@{1}'.format(username, password)
        data = {
            'Type': CRED_TYPE_GENERIC,
            'TargetName': target,
            'UserName': username,
            'CredentialBlob': password,
            'Comment': comment,
            'Persist': CRED_PERSIST_ENTERPRISE}

        # when
        result = CREDENTIAL.fromdict(data)

        # then
        self.assertEqual(result.Type, CRED_TYPE_GENERIC)
        self.assertEqual(result.Flags, 0)
        self.assertEqual(result.AttributeCount, 0)
        self.assertEqual(result.CredentialBlobSize, 26)
        self.assertEqual(result.Persist, CRED_PERSIST_ENTERPRISE)
        if _backend == 'cffi':
            from win32ctypes.core.cffi._util import ffi
            self.assertEqual(ffi.string(result.UserName), username)
            self.assertEqual(result.TargetAlias, ffi.NULL)
            self.assertEqual(ffi.string(result.Comment), comment)
            self.assertNotEqual(result.CredentialBlob, ffi.NULL)
        else:
            self.assertEqual(result.Comment, comment)
            self.assertEqual(result.UserName, username)
            self.assertIsNone(result.TargetAlias)

    def test_roundtrip(self):
        # given
        username = 'john'
        password = 'doefsajfsakfj'
        comment = 'Created by MiniPyWin32Cred test suite'
        target = '{0}@{1}'.format(username, password)
        keyword = 'mysecret-attribute'
        value = 'Created by MiniPyWin32Cred test suite'
        attribute1 = {'Keyword': keyword, 'Value': value, 'Flags': 2}
        data = {
            'Flags': 2,
            'TargetAlias': 'test',
            'Type': CRED_TYPE_GENERIC,
            'TargetName': target,
            'UserName': username,
            'CredentialBlob': password,
            'Comment': comment,
            'Attributes': (attribute1,),
            'Persist': CRED_PERSIST_ENTERPRISE}

        # when
        for _ in range(10):  # need to repeat to expose memory issues
            credential = CREDENTIAL.fromdict(data)
            result = credential2dict(credential)

            # then
            if _backend == 'ctypes':
                self.assertIsInstance(result['LastWritten'], FILETIME)
            del result['LastWritten']
            result['CredentialBlob'] = result['CredentialBlob'].decode('utf-16')  # noqa
            attribute = result['Attributes'][0]
            attribute['Value'] = attribute['Value'].decode('utf-16')
            self.assertEqual(result, data)


class TestCREDENTIAL_ATTRIBUTE(unittest.TestCase):

    def test_fromdict(self):
        # given
        keyword = 'mysecret-attribute'
        value = 'Created by MiniPyWin32Cred test suite'
        data = {
            'Keyword': keyword,
            'Flags': 2,
            'Value': value}

        # when
        result = CREDENTIAL_ATTRIBUTE.fromdict(data)

        # then
        self.assertEqual(result.Flags, 2)
        self.assertIsNotNone(result.Value)
        self.assertEqual(result.ValueSize, 74)
        if _backend == 'cffi':
            from win32ctypes.core.cffi._util import ffi
            self.assertEqual(
                ffi.string(result.Keyword), 'mysecret-attribute')
        else:
            self.assertEqual(result.Keyword, 'mysecret-attribute')

    def test_roundtrip_with_string(self):
        # given
        keyword = 'mysecret-attribute'
        value = 'Created by MiniPyWin32Cred test suite'
        data = {
            'Keyword': keyword,
            'Flags': 7,
            'Value': value}

        # when
        for _ in range(10):  # need to repeat to expose memory issues
            attribute = CREDENTIAL_ATTRIBUTE.fromdict(data)
            result = credential_attribute2dict(attribute)
            # then
            result['Value'] = result['Value'].decode('utf-16')
            self.assertEqual(result, data)

    def test_roundtrip_with_bytes(self):
        # given
        keyword = 'mysecret-attribute'
        value = b'Created by MiniPyWin32Cred test suite'
        data = {
            'Keyword': keyword,
            'Flags': 7,
            'Value': value}

        # when
        for _ in range(10):  # need to repeat to expose memory issues
            attribute = CREDENTIAL_ATTRIBUTE.fromdict(data)
            result = credential_attribute2dict(attribute)

        # then
        self.assertEqual(result, data)
