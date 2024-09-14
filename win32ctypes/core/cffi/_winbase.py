#
# (C) Copyright 2024 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
import enum
from ._util import ffi

ffi.cdef("""

typedef struct _FILETIME {
  DWORD dwLowDateTime;
  DWORD dwHighDateTime;
} FILETIME, *PFILETIME, *LPFILETIME;

""")


class _FILETIME(object):

    def __call__(self):
        return ffi.new("PFILETIME")[0]

    @classmethod
    def fromdict(cls, filetime):
        factory = cls()
        c_filetime = factory()
        c_filetime.dwLowDateTime = filetime['dwLowDateTime']
        c_filetime.dwHighDateTime = filetime['dwHighDateTime']
        return c_filetime

def PFILETIME(value=None):
    return ffi.new("PFILETIME", ffi.NULL if value is None else value)


FILETIME = _FILETIME()
LPFILETIME = PFILETIME
