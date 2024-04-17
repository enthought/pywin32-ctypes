#
# Tests addapted from the test_pywintypes.py of pywin32 to test the
# win32ctypes implementation
#
import os
import sys
import unittest
import contextlib
import tempfile
import shutil
import faulthandler
import datetime
import time

from win32ctypes import pywin32
from win32ctypes.pywin32.pywintypes import error

class TestPyWINTypes(unittest.TestCase):

    # the pywin32ctypes implementation
    module = pywin32.pywintypes

    def testPyTimeFormat(self):
        struct_current = time.localtime()
        pytime_current = self.module.Time(struct_current)
        # try and test all the standard parts of the format
        # Note we used to include '%Z' testing, but that was pretty useless as
        # it always returned the local timezone.
        format_strings = "%a %A %b %B %c %d %H %I %j %m %M %p %S %U %w %W %x %X %y %Y"
        for fmt in format_strings.split():
            v1 = pytime_current.Format(fmt)
            v2 = time.strftime(fmt, struct_current)
            self.assertEqual(v1, v2, "format %s failed - %r != %r" % (fmt, v1, v2))

    def testPyTimePrint(self):
        # This used to crash with an invalid, or too early time.
        # We don't really want to check that it does cause a ValueError
        # (as hopefully this wont be true forever).  So either working, or
        # ValueError is OK.
        try:
            t = self.module.Time(-2)
            t.Format()
        except ValueError:
            return

    def testTimeInDict(self):
        d = {}
        d["t1"] = self.module.Time(1)
        self.assertEqual(d["t1"], self.module.Time(1))

    def testPyTimeCompare(self):
        t1 = self.module.Time(100)
        t1_2 = self.module.Time(100)
        t2 = self.module.Time(101)

        self.assertEqual(t1, t1_2)
        self.assertTrue(t1 <= t1_2)
        self.assertTrue(t1_2 >= t1)

        self.assertNotEqual(t1, t2)
        self.assertTrue(t1 < t2)
        self.assertTrue(t2 > t1)

    def testPyTimeCompareOther(self):
        t1 = self.module.Time(100)
        t2 = None
        self.assertNotEqual(t1, t2)

    def testTimeTuple(self):
        now = datetime.datetime.now()  # has usec...
        # timetuple() lost usec - pt must be <=...
        pt = self.module.Time(now.timetuple())
        # *sob* - only if we have a datetime object can we compare like this.
        if isinstance(pt, datetime.datetime):
            self.assertTrue(pt <= now)

    def testTimeTuplems(self):
        now = datetime.datetime.now()  # has usec...
        tt = now.timetuple() + (now.microsecond // 1000,)
        pt = self.module.Time(tt)
        # we can't compare if using the old type, as it loses all sub-second res.
        if isinstance(pt, datetime.datetime):
            # but even with datetime, we lose sub-millisecond.
            expectedDelta = datetime.timedelta(milliseconds=1)
            self.assertTrue(-expectedDelta < (now - pt) < expectedDelta)

    def testPyTimeFromTime(self):
        t1 = self.module.Time(time.time())
        self.assertTrue(self.module.Time(t1) is t1)
