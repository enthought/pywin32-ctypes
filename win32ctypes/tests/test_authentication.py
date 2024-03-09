#
# (C) Copyright 2022-2024 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
import unittest

from win32ctypes.core._authentication import (
    CREDENTIAL, CREDENTIAL_ATTRIBUTE, FILETIME,
    credential2dict, credential_attribute2dict)
from win32ctypes.constants import (
    CRED_TYPE_GENERIC, CRED_PERSIST_ENTERPRISE)


class TestCREDENTIAL(unittest.TestCase):

    maxDiff = None

    def test_from_dict(self):
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
        self.assertEqual(result.TargetName, target)
        self.assertIsNone(result.TargetAlias)
        self.assertEqual(result.Flags, 0)
        self.assertEqual(result.AttributeCount, 0)
        self.assertIsNotNone(result.CredentialBlob)
        self.assertEqual(result.UserName, username)
        self.assertEqual(result.CredentialBlobSize, 26)
        self.assertEqual(result.Comment, comment)
        self.assertEqual(result.Persist, CRED_PERSIST_ENTERPRISE)

    def test_roundtrip(self):
        # given
        username = 'john'
        password = 'doefsajfsakfj'
        comment = 'Created by MiniPyWin32Cred test suite'
        target = '{0}@{1}'.format(username, password)
        keyword = 'mysecret-attribute'
        value = b'Created by MiniPyWin32Cred test suite'
        attribute1 = {'Keyword': keyword, 'Value': value, 'Flags': 2}
        attribute2 = {
            'Keyword': keyword + '12', 'Value': value[:10], 'Flags': 1}
        data = {
            'Type': CRED_TYPE_GENERIC,
            'TargetName': target,
            'UserName': username,
            'CredentialBlob': password,
            'Comment': comment,
            'Attributes': (attribute1, attribute2),
            'Persist': CRED_PERSIST_ENTERPRISE}

        # when
        credential = CREDENTIAL.fromdict(data)
        result = credential2dict(credential)

        # then
        data['TargetAlias'] = None
        data['Flags'] = 0
        self.assertIsInstance(result['LastWritten'], FILETIME)
        # Remove unused keys
        del result['LastWritten']
        del result['CredentialBlobSize']
        del result['AttributeCount']
        result['CredentialBlob'] = result['CredentialBlob'].decode('utf-16')
        for attribute in result['Attributes']:
            if 'Value' in attribute:
                attribute['Value'] = attribute['Value']
        self.assertEqual(result, data)


class TestCREDENTIAL_ATTRIBUTE(unittest.TestCase):

    def test_from_dict(self):
        # given
        keyword = 'mysecret-attribute'
        value = b'Created by MiniPyWin32Cred test suite'
        data = {
            'Keyword': keyword,
            'Flags': 2,
            'Value': value}

        # when
        result = CREDENTIAL_ATTRIBUTE.fromdict(data)

        # then
        self.assertEqual(result.Keyword, 'mysecret-attribute')
        self.assertEqual(result.Flags, 2)
        self.assertIsNotNone(result.Value)
        self.assertEqual(result.ValueSize, 37)

    def test_roundtrip(self):
        # given
        keyword = 'mysecret-attribute'
        value = b'Created by MiniPyWin32Cred test suite'
        data = {
            'Keyword': keyword,
            'Flags': 7,
            'Value': value}

        # when
        attribute = CREDENTIAL_ATTRIBUTE.fromdict(data)
        result = credential_attribute2dict(attribute)

        # then
        # Add missing keys to original data
        result['Value'] = result['Value']
        self.assertEqual(result, data)
