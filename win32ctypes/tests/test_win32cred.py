#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

from __future__ import absolute_import

import unittest

import win32cred

from win32ctypes.core._winerrors import ERROR_NOT_FOUND
from win32ctypes.pywin32.pywintypes import error
from win32ctypes.pywin32.win32cred import (
    CredDelete, CredRead, CredWrite,
    CRED_PERSIST_ENTERPRISE, CRED_TYPE_GENERIC)
from win32ctypes.tests import compat


class TestCred(compat.TestCase):

    def test_write_simple(self):
        username = u"john"
        password = u"doefsajfsakfj"
        comment = u"Created by MiniPyWin32Cred test suite"

        target = "{0}@{1}".format(username, password)

        credentials = {"Type": CRED_TYPE_GENERIC,
                       "TargetName": target,
                       "UserName": username,
                       "CredentialBlob": password,
                       "Comment": comment,
                       "Persist": CRED_PERSIST_ENTERPRISE}

        CredWrite(credentials)

        res = win32cred.CredRead(
            TargetName=target, Type=CRED_TYPE_GENERIC)

        self.assertEqual(res["Type"], CRED_TYPE_GENERIC)
        self.assertEqual(res["UserName"], username)
        self.assertEqual(res["TargetName"], target)
        self.assertEqual(res["Comment"], comment)
        self.assertEqual(
            res["CredentialBlob"].decode('utf-16'), password)

    def test_read_simple(self):
        username = "john"
        password = "doe"
        comment = u"Created by MiniPyWin32Cred test suite"

        target = u"{0}@{1}".format(username, password)

        r_credentials = {
            u"Type": CRED_TYPE_GENERIC,
            u"TargetName": target,
            u"UserName": username,
            u"CredentialBlob": password,
            u"Comment": comment,
            u"Persist": CRED_PERSIST_ENTERPRISE}
        win32cred.CredWrite(r_credentials)

        credentials = CredRead(target, CRED_TYPE_GENERIC)

        # XXX: the fact that we have to decode the password when reading, but
        # not encode when writing is a bit insane, but that's what pywin32
        # seems to do as well, and we try to be backward compatible here.
        self.assertEqual(credentials["UserName"], username)
        self.assertEqual(credentials["TargetName"], target)
        self.assertEqual(credentials["Comment"], comment)
        self.assertEqual(
            credentials["CredentialBlob"].decode("utf-16"), password)

    def test_read_doesnt_exists(self):
        target = "Floupi_dont_exists@MiniPyWin"
        with self.assertRaises(error) as ctx:
            CredRead(target, CRED_TYPE_GENERIC)
        self.assertTrue(ctx.exception.winerror, ERROR_NOT_FOUND)

    def test_delete_simple(self):
        username = "john"
        password = "doe"
        comment = "Created by MiniPyWin32Cred test suite"

        target = "{0}@{1}".format(username, password)

        r_credentials = {
            "Type": CRED_TYPE_GENERIC,
            "TargetName": target,
            "UserName": username,
            "CredentialBlob": password,
            "Comment": comment,
            "Persist": CRED_PERSIST_ENTERPRISE}
        CredWrite(r_credentials, 0)

        credentials = win32cred.CredRead(target, CRED_TYPE_GENERIC)
        self.assertTrue(credentials is not None)

        CredDelete(target, CRED_TYPE_GENERIC)

        with self.assertRaises(error) as ctx:
            CredRead(target, CRED_TYPE_GENERIC)
        self.assertEqual(ctx.exception.winerror, ERROR_NOT_FOUND)
        self.assertEqual(ctx.exception.funcname, "CredRead")

    def test_delete_doesnt_exists(self):
        target = u"Floupi_doesnt_exists@MiniPyWin32"

        with self.assertRaises(error) as ctx:
            CredDelete(target, CRED_TYPE_GENERIC)
        self.assertEqual(ctx.exception.winerror, ERROR_NOT_FOUND)
        self.assertEqual(ctx.exception.funcname, "CredDelete")


if __name__ == '__main__':
    unittest.main()
