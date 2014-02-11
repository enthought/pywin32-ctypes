import unittest

import win32cred

from mini_pywin32.win32cred import CredRead, CredWrite, CRED_PERSIST_ENTERPRISE, CRED_TYPE_GENERIC

class TestCred(unittest.TestCase):
    def test_write_simple(self):
        service = "MiniPyWin32Cred"
        username = "john"
        password = "doe"
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
        self.assertEqual(res["CredentialBlob"], password)
        self.assertEqual(res["UserName"], username)
        self.assertEqual(res["TargetName"], target)
        self.assertEqual(res["Comment"], comment)
