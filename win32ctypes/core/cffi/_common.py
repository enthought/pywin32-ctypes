#
# (C) Copyright 2015 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from __future__ import absolute_import
from ._util import ffi


def IS_INTRESOURCE(x):
    return int(ffi.cast("uintptr_t", x)) >> 16 == 0
