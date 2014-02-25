#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

import sys
import unittest

import win32ctypes.win32api
import win32api

from win32ctypes.pywintypes import error
from win32ctypes.tests import compat


class TestWin32API(compat.TestCase):

    def setUp(self):
        self.handle = None

    def tearDown(self):
        if self.handle is not None:
            self._free_library(win32api, self.handle)

    def test_load_library_ex(self):
        self.handle = self._load_library(win32api)
        mini = self._load_library(win32ctypes.win32api)
        self.assertEqual(mini, self.handle)

        with self.assertRaises(error):
            win32ctypes.win32api.LoadLibraryEx('ttt.dll', 0, 0x2)

    def test_free_library(self):
        self.handle = self._load_library(win32api)
        self.assertTrue(self._free_library(win32api, self.handle) is None)
        self.assertNotEqual(
            self._free_library(win32ctypes.win32api, self.handle), 0)

        with self.assertRaises(error):
            self._free_library(win32ctypes.win32api, -3)

    def test_enum_resource_types(self):
        self.handle = self._load_library(win32api)
        original = self._enum_resource_types(win32api, self.handle)
        mini = self._enum_resource_types(win32ctypes.win32api, self.handle)
        self.assertEqual(mini, original)

        with self.assertRaises(error):
            win32ctypes.win32api.EnumResourceTypes(-3)

    def test_enum_resource_names(self):
        self.handle = self._load_library(win32api)
        resource_types = self._enum_resource_types(win32api, self.handle)

        for resource_type in resource_types:
            original = self._enum_resource_names(
                win32api, self.handle, resource_type)
            mini = self._enum_resource_names(
                win32ctypes.win32api, self.handle, resource_type)
            self.assertEqual(mini, original)

        with self.assertRaises(error):
            win32ctypes.win32api.EnumResourceNames(2, 3)

    def test_enum_resource_languages(self):
        handle = self._load_library(win32api)
        resource_types = self._enum_resource_types(win32api, handle)

        for resource_type in resource_types:
            resource_names = self._enum_resource_names(
                win32api, handle, resource_type)
            for resource_name in resource_names:
                original = self._enum_resource_languages(
                    win32api, handle, resource_type, resource_name)
                mini = self._enum_resource_languages(
                    win32ctypes.win32api, handle, resource_type,
                    resource_name)
                self.assertEqual(mini, original)

        with self.assertRaises(error):
            win32ctypes.win32api.EnumResourceLanguages(
                handle, resource_type, 2235)

    def test_load_resource(self):
        handle = self._load_library(win32api)
        resource_types = self._enum_resource_types(win32api, handle)

        for resource_type in resource_types:
            resource_names = self._enum_resource_names(
                win32api, handle, resource_type)
            for resource_name in resource_names:
                resource_languages = self._enum_resource_languages(
                    win32api, handle, resource_type, resource_name)
                for resource_language in resource_languages:
                    original = self._load_resource(
                        win32api, handle,
                        resource_type, resource_name,
                        resource_language)
                    mini = self._load_resource(
                        win32ctypes.win32api, handle,
                        resource_type, resource_name,
                        resource_language)
                    self.assertEqual(mini, original)

        with self.assertRaises(error):
            win32ctypes.win32api.LoadResource(
                handle, resource_type, resource_name, 12435)

    def _load_library(self, module):
        # backward shim for win32api module which does not export
        # LOAD_LIBRARY_AS_DATAFILE
        LOAD_LIBRARY_AS_DATAFILE = getattr(
            module, "LOAD_LIBRARY_AS_DATAFILE", 0x2)
        return module.LoadLibraryEx(
            sys.executable, 0, LOAD_LIBRARY_AS_DATAFILE)

    def _free_library(self, module, handle):
        return module.FreeLibrary(handle)

    def _enum_resource_types(self, module, handle):
        return module.EnumResourceTypes(handle)

    def _enum_resource_names(self, module, handle, resource_type):
        return module.EnumResourceNames(handle, resource_type)

    def _enum_resource_languages(self, module, handle, resource_type, name):
        return module.EnumResourceLanguages(handle, resource_type, name)

    def _load_resource(
            self, module, handle, resource_type,
            resource_name, resource_language):
        return module.LoadResource(
            handle, resource_type, resource_name, resource_language)


if __name__ == '__main__':
    unittest.main()
