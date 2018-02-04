#
# (C) Copyright 2014-2018 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from __future__ import absolute_import

import sys
import importlib

from . import _winerrors  # noqa

try:
    import cffi
except ImportError:
    _backend = 'ctypes'
else:
    del cffi
    _backend = 'cffi'


class BackendFinder(object):

    def __init__(self, modules):
        self.redirected_modules = [
            'win32ctypes.core.{}'.format(module)
            for module in modules]

    def find_module(self, fullname, path=None):
        if fullname in self.redirected_modules:
            return self
        else:
            return None

    def load_module(self, fullname):
        module_name = fullname.split('.')[-1]
        if _backend == 'ctypes':
            new_fullname = 'win32ctypes.core.ctypes.{}'
        else:
            new_fullname = 'win32ctypes.core.cffi.{}'
        module = importlib.import_module(
            new_fullname.format(module_name))
        return module


sys.meta_path.append(BackendFinder([
    '_dll', '_authentication', '_time',
    '_common', '_resource', '_nl_support',
    '_system_information']))
