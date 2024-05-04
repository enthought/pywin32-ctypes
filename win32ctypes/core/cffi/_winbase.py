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


typedef struct _SYSTEMTIME {
  WORD wYear;
  WORD wMonth;
  WORD wDayOfWeek;
  WORD wDay;
  WORD wHour;
  WORD wMinute;
  WORD wSecond;
  WORD wMilliseconds;
} SYSTEMTIME, *PSYSTEMTIME, *LPSYSTEMTIME;

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


class _SYSTEMTIME(object):

    def __call__(self):
        return ffi.new("PSYSTEMTIME")[0]

    @classmethod
    def fromdict(cls, systemtime):
        factory = cls()
        c_systemtime = factory()
        c_systemtime.wYear = systemtime['Year']
        c_systemtime.wMonth = systemtime['Month']
        c_systemtime.wDayOfWeek = systemtime['DayOfWeek']
        c_systemtime.wDay = systemtime['Day']
        c_systemtime.wHour = systemtime['Hour']
        c_systemtime.wMinute = systemtime['Minute']
        c_systemtime.wSecond = systemtime['Second']
        c_systemtime.wMilliseconds = systemtime['Milliseconds']
        return c_systemtime


def PFILETIME(value=None):
    return ffi.new("PFILETIME", ffi.NULL if value is None else value)


def PSYSTEMTIME(value=None):
    return ffi.new("PSYSTEMTIME", ffi.NULL if value is None else value)


FILETIME = _FILETIME()
SYSTEMTIME = _SYSTEMTIME()
LPFILETIME = PFILETIME
LPSYSTEMTIME= PSYSTEMTIME
