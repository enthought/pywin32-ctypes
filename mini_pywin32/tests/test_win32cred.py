from __future__ import absolute_import

import unittest

import win32cred

from mini_pywin32._winerrors import ERROR_NOT_FOUND
from mini_pywin32.win32cred import (
    CredDelete, CredRead, CredWrite, CRED_PERSIST_ENTERPRISE,
    CRED_TYPE_GENERIC)


class TestCred(unittest.TestCase):

    def test_write_simple(self):
        username = "john"
        password = "doefsajfsakfj"
        comment = "Created by MiniPyWin32Cred test suite"

        target = "{0}@{1}".format(username, password)

        credentials = {"Type": CRED_TYPE_GENERIC,
                       "TargetName": target,
                       "UserName": username,
                       "CredentialBlob": password,
                       "Comment": comment,
                       "Persist": CRED_PERSIST_ENTERPRISE}

        CredWrite(credentials, 0)

        res = win32cred.CredRead(TargetName=target, Type=CRED_TYPE_GENERIC)

        self.assertEqual(res["Type"], CRED_TYPE_GENERIC)
        self.assertEqual(
            unicode(res["CredentialBlob"], encoding='utf-16'),
            password)
        self.assertEqual(res["UserName"], username)
        self.assertEqual(res["TargetName"], target)
        self.assertEqual(res["Comment"], comment)

    def test_read_simple(self):
        username = "john"
        password = "doe"
        comment = "Created by MiniPyWin32Cred test suite"

        target = "{0}@{1}".format(username, password)

        r_credentials = {"Type": CRED_TYPE_GENERIC,
                       "TargetName": target,
                       "UserName": username,
                       "CredentialBlob": password,
                       "Comment": comment,
                       "Persist": CRED_PERSIST_ENTERPRISE}
        win32cred.CredWrite(r_credentials, 0)

        credentials = CredRead(target, CRED_TYPE_GENERIC)

        # XXX: the fact that we have to decode the password when reading, but
        # not encode when writing is a bit insane, but that's what pywin32
        # seems to do as well, and we try to be backward compatible here.
        self.assertEqual(credentials["CredentialBlob"].decode("utf-16"),
                         password)
        self.assertEqual(credentials["UserName"], username)
        self.assertEqual(credentials["TargetName"], target)
        self.assertEqual(credentials["Comment"], comment)

    def test_read_doesnt_exists(self):
        target = "Floupi_dont_exists@MiniPyWin"
        with self.assertRaises(WindowsError) as ctx:
            CredRead(target, CRED_TYPE_GENERIC)
        self.assertTrue(ctx.exception.winerror, ERROR_NOT_FOUND)

    def test_delete_simple(self):
        username = "john"
        password = "doe"
        comment = "Created by MiniPyWin32Cred test suite"

        target = "{0}@{1}".format(username, password)

        r_credentials = {"Type": CRED_TYPE_GENERIC,
                       "TargetName": target,
                       "UserName": username,
                       "CredentialBlob": password,
                       "Comment": comment,
                       "Persist": CRED_PERSIST_ENTERPRISE}
        CredWrite(r_credentials, 0)

        credentials = win32cred.CredRead(target, CRED_TYPE_GENERIC)
        self.assertTrue(credentials is not None)

        CredDelete(target, CRED_TYPE_GENERIC)

        with self.assertRaises(WindowsError) as ctx:
            CredRead(target, CRED_TYPE_GENERIC)
        self.assertEqual(ctx.exception.winerror, ERROR_NOT_FOUND)

    def test_delete_doesnt_exists(self):
        target = "Floupi_doesnt_exists@MiniPyWin32"

        with self.assertRaises(WindowsError) as ctx:
            CredDelete(target, CRED_TYPE_GENERIC)
        self.assertEqual(ctx.exception.winerror, ERROR_NOT_FOUND)
