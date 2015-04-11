#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

import sys
import unittest
import contextlib

import win32api
from win32ctypes import pywin32
from win32ctypes.pywin32.pywintypes import error
from win32ctypes.tests import compat


class TestWin32API(compat.TestCase):

    module = pywin32.win32api

    @contextlib.contextmanager
    def load_library(self, module, library=sys.executable, flags=0x2):
        handle = module.LoadLibraryEx(library, 0, flags)
        try:
            yield handle
        finally:
            module.FreeLibrary(handle)

    def test_load_library_ex(self):
        with self.load_library(win32api) as expected:
            with self.load_library(self.module) as handle:
                self.assertEqual(handle, expected)

        with self.assertRaises(error):
            self.module.LoadLibraryEx('ttt.dll', 0, 0x2)

    def test_free_library(self):
        with self.load_library(win32api) as handle:
            self.assertTrue(win32api.FreeLibrary(handle) is None)
            self.assertNotEqual(self.module.FreeLibrary(handle), 0)

        with self.assertRaises(error):
            self.module.FreeLibrary(-3)

    def test_enum_resource_types(self):
        with self.load_library(win32api, 'shell32.dll') as handle:
            expected = win32api.EnumResourceTypes(handle)

        with self.load_library(pywin32.win32api, 'shell32.dll') as handle:
            resource_types = self.module.EnumResourceTypes(handle)

        self.assertEqual(resource_types, expected)

        with self.assertRaises(error):
            self.module.EnumResourceTypes(-3)

    def test_enum_resource_names(self):
        with self.load_library(win32api, 'shell32.dll') as handle:
            resource_types = win32api.EnumResourceTypes(handle)
            for resource_type in resource_types:
                expected = win32api.EnumResourceNames(handle, resource_type)
                resource_names = self.module.EnumResourceNames(
                    handle, resource_type)
            self.assertEqual(resource_names, expected)

        with self.assertRaises(error):
            self.module.EnumResourceNames(2, 3)

    def test_enum_resource_languages(self):
        with self.load_library(win32api, 'explorer.exe') as handle:
            resource_types = win32api.EnumResourceTypes(handle)
            for resource_type in resource_types:
                resource_names = win32api.EnumResourceNames(
                    handle, resource_type)
                for resource_name in resource_names:
                    expected = win32api.EnumResourceLanguages(
                        handle, resource_type, resource_name)
                    resource_languages = self.module.EnumResourceLanguages(
                        handle, resource_type, resource_name)
                    self.assertEqual(resource_languages, expected)

        with self.assertRaises(error):
            self.module.EnumResourceLanguages(handle, resource_type, 2235)

    def test_load_resource(self):
        with self.load_library(win32api, 'explorer.exe') as handle:
            resource_types = win32api.EnumResourceTypes(handle)
            for resource_type in resource_types:
                resource_names = win32api.EnumResourceNames(
                    handle, resource_type)
                for resource_name in resource_names:
                    resource_languages = win32api.EnumResourceLanguages(
                        handle, resource_type, resource_name)
                    for resource_language in resource_languages:
                        expected = win32api.LoadResource(
                            handle, resource_type, resource_name,
                            resource_language)
                        resource = self.module.LoadResource(
                            handle, resource_type, resource_name,
                            resource_language)
                        self.assertEqual(resource, expected)

        with self.assertRaises(error):
            self.module.LoadResource(
                handle, resource_type, resource_name, 12435)


if __name__ == '__main__':
    unittest.main()
