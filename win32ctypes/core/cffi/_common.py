#
# (C) Copyright 2015 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from __future__ import absolute_import

from ._util import ffi


def _PyBytes_FromStringAndSize(pointer, size):
    buffer = ffi.buffer(pointer, size)
    return buffer[:]
