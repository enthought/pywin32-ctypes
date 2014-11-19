#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
__all__ = ['win32cred']

import warnings

warnings.warn(
    "Please use 'from win32ctypes.pywin32 import win32cred'",
    DeprecationWarning)

from win32ctypes.pywin32 import win32cred
