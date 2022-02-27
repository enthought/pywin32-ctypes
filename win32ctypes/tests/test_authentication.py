#
# (C) Copyright 2022 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
import unittest

from win32ctypes.core._authentication import CREDENTIAL
from win32ctypes.constants import (
    CRED_TYPE_GENERIC, CRED_PERSIST_ENTERPRISE)


class TestCREDENTIAL(unittest.TestCase):

    def test_from_dict(self):
        # given
        username = u"john"
        password = u"doefsajfsakfj"
        comment = u"Created by MiniPyWin32Cred test suite"
        target = "{0}@{1}".format(username, password)
        data = {
            "Type": CRED_TYPE_GENERIC,
            "TargetName": target,
            "UserName": username,
            "CredentialBlob": password,
            "Comment": comment,
            "Persist": CRED_PERSIST_ENTERPRISE}

        # when
        result = CREDENTIAL.fromdict(data)

        # then
        self.assertEqual(result.Type, CRED_TYPE_GENERIC)
        self.assertEqual(result.TargetName, target)
        self.assertEqual(result.UserName, username)
        self.assertEqual(result.CredentialBlobSize, 26)
        self.assertEqual(result.Comment, comment)
        self.assertEqual(result.Persist, CRED_PERSIST_ENTERPRISE)
