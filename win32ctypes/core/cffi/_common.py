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
    """ Check if x is an index into the id list.

    """
    return int(ffi.cast("uintptr_t", x)) >> 16 == 0


def RESOURCE(resource):
    """ Convert a resource into a compatible input for cffi.

    """
    if isinstance(resource, (int, long)):
        resource = ffi.cast('wchar_t *', resource)
    elif isinstance(resource, str):
        resource = unicode(resource)
    return resource


def resource(lpRESOURCEID):
    """ Convert the windows RESOURCE into a python friendly object.
    """
    if IS_INTRESOURCE(lpRESOURCEID):
        resource = int(ffi.cast("uintptr_t", lpRESOURCEID))
    else:
        resource = ffi.string(lpRESOURCEID)
    return resource
