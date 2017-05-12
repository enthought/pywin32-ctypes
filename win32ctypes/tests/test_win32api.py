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
import tempfile
import shutil
import os

import win32api

from win32ctypes import pywin32
from win32ctypes.pywin32.pywintypes import error
from win32ctypes.tests import compat


class TestWin32API(compat.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        shutil.copy(sys.executable, self.tempdir)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

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
            self.module.LoadLibraryEx(u'ttt.dll', 0, 0x2)

    def test_free_library(self):
        with self.load_library(win32api) as handle:
            self.assertTrue(win32api.FreeLibrary(handle) is None)
            self.assertNotEqual(self.module.FreeLibrary(handle), 0)

        with self.assertRaises(error):
            self.module.FreeLibrary(-3)

    def test_enum_resource_types(self):
        with self.load_library(win32api, u'shell32.dll') as handle:
            expected = win32api.EnumResourceTypes(handle)

        with self.load_library(pywin32.win32api, u'shell32.dll') as handle:
            resource_types = self.module.EnumResourceTypes(handle)

        self.assertEqual(resource_types, expected)

        with self.assertRaises(error):
            self.module.EnumResourceTypes(-3)

    def test_enum_resource_names(self):
        with self.load_library(win32api, u'shell32.dll') as handle:
            resource_types = win32api.EnumResourceTypes(handle)
            for resource_type in resource_types:
                expected = win32api.EnumResourceNames(handle, resource_type)
                resource_names = self.module.EnumResourceNames(
                    handle, resource_type)
                self.assertEqual(resource_names, expected)
                # check that the #<index> format works
                resource_names = self.module.EnumResourceNames(
                    handle, self._id2str(resource_type))
                self.assertEqual(resource_names, expected)

        with self.assertRaises(error):
            self.module.EnumResourceNames(2, 3)

    def test_enum_resource_languages(self):
        with self.load_library(win32api, u'shell32.dll') as handle:
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
                    # check that the #<index> format works
                    resource_languages = self.module.EnumResourceLanguages(
                        handle, self._id2str(resource_type),
                        self._id2str(resource_name))
                    self.assertEqual(resource_languages, expected)

        with self.assertRaises(error):
            self.module.EnumResourceLanguages(handle, resource_type, 2235)

    def test_load_resource(self):
        with self.load_library(win32api, u'explorer.exe') as handle:
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
                        # check that the #<index> format works
                        resource = self.module.LoadResource(
                            handle, self._id2str(resource_type),
                            self._id2str(resource_name),
                            resource_language)
                        self.assertEqual(resource, expected)

        with self.assertRaises(error):
            self.module.LoadResource(
                handle, resource_type, resource_name, 12435)

    def test_get_tick_count(self):
        self.assertGreater(self.module.GetTickCount(), 0.0)

    def test_get_windows_directory(self):
        self.assertEqual(
            self.module.GetWindowsDirectory().lower(), r"c:\windows")

    def test_get_system_directory(self):
        self.assertEqual(
            self.module.GetSystemDirectory().lower(), r"c:\windows\system32")

    def test_begin_and_end_update_resource(self):
        filename = os.path.join(self.tempdir, 'python.exe')
        handle = self.module.BeginUpdateResource(filename, False)
        self.module.EndUpdateResource(handle, False)

    def test_update_resource(self):
        # given
        module = self.module
        filename = os.path.join(self.tempdir, 'python.exe')
        with self.load_library(self.module, filename) as handle:
            resource_type = module.EnumResourceTypes(handle)[-1]
            resource_name = module.EnumResourceNames(handle, resource_type)[-1]
            resource_language = module.EnumResourceLanguages(
                handle, resource_type, resource_name)[-1]
            resource = module.LoadResource(
                handle, resource_type, resource_name, resource_language)

        # when
        handle = module.BeginUpdateResource(filename, False)
        try:
            self.assertEqual(module.UpdateResource(
                handle, resource_type, resource_name, resource[:-2],
                language=resource_language), 1)
        finally:
             self.assertEqual(module.EndUpdateResource(handle, False), 1)

        # then
        with self.load_library(self.module, filename) as handle:
            updated = module.LoadResource(
                handle, resource_type, resource_name, resource_language)
        self.assertEqual(len(updated), len(resource) - 2)
        self.assertEqual(updated, resource[:-2])

    def _id2str(self, type_id):
        if hasattr(type_id, 'index'):
            return type_id
        else:
            return u'#{0}'.format(type_id)


if __name__ == '__main__':
    unittest.main()
