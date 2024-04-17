#
# (C) Copyright 2014-2024 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
import os
import sys
import unittest

import win32cred
from parameterized import parameterized

from win32ctypes.core._winerrors import ERROR_NOT_FOUND
from win32ctypes.pywin32.pywintypes import error
from win32ctypes.pywin32.win32cred import (
    CredDelete, CredRead, CredWrite, CredEnumerate,
    CRED_PERSIST_ENTERPRISE, CRED_TYPE_GENERIC,
    CRED_ENUMERATE_ALL_CREDENTIALS)

# find the pywin32 version
version_file = os.path.join(
    os.path.dirname(
        os.path.dirname(win32cred.__file__)), 'pywin32.version.txt')
if os.path.exists(version_file):
    with open(version_file) as handle:
        pywin32_build = handle.read().strip()
else:
    pywin32_build = None


def _demo_attributes(multiple=False):
    keyword = 'mysecret-attribute'
    attribute1 = {
        'Keyword': keyword,
        'Value': b'Created by MiniPyWin32Cred test suite', 'Flags': 0}
    attribute2 = {
        'Keyword': keyword + '12',
        'Value': b'Attribute from MiniPyWin32', 'Flags': 0}
    if multiple:
        return (attribute1, attribute2)
    else:
        return (attribute1,)


def _demo_credentials(UserName=u'jone', multiple=False):
    return {
        'Type': CRED_TYPE_GENERIC,
        'TargetName': u'jone@doe',
        'UserName': UserName,
        'CredentialBlob': u'doefsajfsakfj',
        'Attributes': _demo_attributes(multiple),
        'Comment': u'Created by MiniPyWin32Cred test suite',
        'Persist': CRED_PERSIST_ENTERPRISE}


TEST_SUPPORTED_CREDENTIALS = [
    (_demo_credentials(), _demo_attributes()),
    (_demo_credentials(UserName=None), _demo_attributes())]

TEST_CREDENTIALS = TEST_SUPPORTED_CREDENTIALS + [
    (_demo_credentials(multiple=True), _demo_attributes(multiple=True)),
    (_demo_credentials(UserName=None, multiple=True), _demo_attributes(multiple=True))]  # noqa


class TestCred(unittest.TestCase):

    def setUp(self):
        from pywintypes import error
        try:
            win32cred.CredDelete(u'jone@doe', CRED_TYPE_GENERIC)
        except error:
            pass

    @parameterized.expand(TEST_SUPPORTED_CREDENTIALS)
    @unittest.skipIf(
        pywin32_build == '223' and sys.version_info[:2] == (3, 7),
        'pywin32 version 223 bug with CredRead (mhammond/pywin32#1232)')
    def test_write_to_pywin32(self, r_credentials, r_attributes):
        # given
        target = u'jone@doe'
        CredWrite(r_credentials)

        # when
        credentials = win32cred.CredRead(
            TargetName=target, Type=CRED_TYPE_GENERIC)

        # then
        self.assertEqual(credentials['Type'], CRED_TYPE_GENERIC)
        self.assertEqual(credentials['UserName'], r_credentials['UserName'])
        self.assertEqual(credentials['TargetName'], 'jone@doe')
        self.assertEqual(
            credentials['Comment'], 'Created by MiniPyWin32Cred test suite')
        # XXX: the fact that we have to decode the password when reading, but
        # not encode when writing is a bit strange, but that's what pywin32
        # seems to do and we try to be backward compatible here.
        self.assertEqual(
            credentials['CredentialBlob'].decode('utf-16'), 'doefsajfsakfj')

    @parameterized.expand(TEST_CREDENTIALS)
    def test_read_from_pywin32(self, r_credentials, r_attributes):
        # given
        target = 'jone@doe'
        win32cred.CredWrite(r_credentials)

        # when
        credentials = CredRead(target, CRED_TYPE_GENERIC)

        # then
        self.assertEqual(credentials['UserName'], r_credentials['UserName'])
        self.assertEqual(credentials['TargetName'], 'jone@doe')
        self.assertEqual(credentials['Attributes'], r_attributes)
        self.assertEqual(
            credentials['Comment'], 'Created by MiniPyWin32Cred test suite')
        self.assertEqual(
            credentials['CredentialBlob'].decode('utf-16'), 'doefsajfsakfj')

    @parameterized.expand(TEST_SUPPORTED_CREDENTIALS)
    def test_read_write(self, r_credentials, r_attributes):
        # given
        target = 'jone@doe'
        r_credentials = r_credentials

        # when
        CredWrite(r_credentials)
        credentials = CredRead(target, CRED_TYPE_GENERIC)

        self.assertEqual(credentials['UserName'], r_credentials['UserName'])
        self.assertEqual(credentials['TargetName'], 'jone@doe')
        self.assertEqual(credentials['Attributes'], r_attributes)
        self.assertEqual(
            credentials['Comment'], 'Created by MiniPyWin32Cred test suite')
        self.assertEqual(
            credentials['CredentialBlob'].decode('utf-16'), 'doefsajfsakfj')

    def test_enumerate_filter(self):
        # given
        r_credentials = _demo_credentials()
        CredWrite(r_credentials)

        # when
        credentials = CredEnumerate('jone*')[0]

        # then
        self.assertEqual(credentials['UserName'], 'jone')
        self.assertEqual(credentials['TargetName'], 'jone@doe')
        self.assertEqual(
            credentials['Comment'], 'Created by MiniPyWin32Cred test suite')
        self.assertEqual(
            credentials['CredentialBlob'].decode('utf-16'), 'doefsajfsakfj')

    def test_enumerate_no_filter(self):
        # given
        r_credentials = _demo_credentials()
        CredWrite(r_credentials)

        # when
        pywin32_result = win32cred.CredEnumerate()
        credentials = CredEnumerate()

        # then
        self.assertEqual(len(credentials), len(pywin32_result))

    def test_enumerate_all(self):
        # when
        credentials = CredEnumerate(Flags=CRED_ENUMERATE_ALL_CREDENTIALS)

        # then
        self.assertGreater(len(credentials), 1)

    def test_read_doesnt_exists(self):
        # given
        target = 'Floupi_dont_exists@MiniPyWin'

        # when/then
        with self.assertRaises(error) as ctx:
            CredRead(target, CRED_TYPE_GENERIC)
        self.assertTrue(ctx.exception.winerror, ERROR_NOT_FOUND)

    def test_delete_simple(self):
        # given
        target = 'jone@doe'
        r_credentials = _demo_credentials()
        CredWrite(r_credentials, 0)
        credentials = CredRead(target, CRED_TYPE_GENERIC)
        self.assertIsNotNone(credentials)

        # when
        CredDelete(target, CRED_TYPE_GENERIC)

        # then
        with self.assertRaises(error) as ctx:
            CredRead(target, CRED_TYPE_GENERIC)
        self.assertEqual(ctx.exception.winerror, ERROR_NOT_FOUND)
        self.assertEqual(ctx.exception.funcname, 'CredRead')

    def test_delete_doesnt_exists(self):
        # given
        target = 'Floupi_doesnt_exists@MiniPyWin32'

        # when/then
        with self.assertRaises(error) as ctx:
            CredDelete(target, CRED_TYPE_GENERIC)
        self.assertEqual(ctx.exception.winerror, ERROR_NOT_FOUND)
        self.assertEqual(ctx.exception.funcname, 'CredDelete')


if __name__ == '__main__':
    unittest.main()
