#
# (C) Copyright 2018 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from __future__ import absolute_import

import ctypes
from ctypes.wintypes import (
    DWORD, HANDLE, POINTER, BOOL, SHORT, WORD, LPDWORD,
    LPCTSTR, CHAR, WCHAR, UINT)
from subprocess import (  # noqa
    STD_INPUT_HANDLE, STD_OUTPUT_HANDLE, STD_ERROR_HANDLE)
from ._util import (
    check_invalid_handle, check_false, function_factory, dlls)


class CONSOLE_CURSOR_INFO(ctypes.Structure):
    _fields_ = [('dwSize', DWORD), ('bVisible', BOOL)]


class COORD(ctypes.Structure):
    _fields_ = [('X', SHORT), ('Y', SHORT)]


class SMALL_RECT(ctypes.Structure):
    _fields_ = [
      ('Left', SHORT),
      ('Top', SHORT),
      ('Right', SHORT),
      ('Bottom', SHORT)]


class _Char(ctypes.Union):
    _fields_ = [('UnicodeChar', WCHAR), ('AsciiChar', CHAR)]


class CHAR_INFO(ctypes.Structure):
    _anonymous_ = ('Char',)
    _fields_ = [('Char', _Char), ('Attributes', WORD)]


class FOCUS_EVENT_RECORD(ctypes.Structure):
    _fields_ = [('bSetFocus', BOOL)]


class KEY_EVENT_RECORD(ctypes.Structure):
    _anonymous_ = ('uChar',)
    _fields_ = [
        ('bKeyDown', BOOL),
        ('wRepeatCount', WORD),
        ('wVirtualKeyCode', WORD),
        ('wVirtualScanCode', WORD),
        ('uChar', _Char),
        ('dwControlKeyState', DWORD)]


class MENU_EVENT_RECORD(ctypes.Structure):
    _fields_ = [('dwCommandId', UINT)]


class MOUSE_EVENT_RECORD(ctypes.Structure):
    _fields_ = [
        ('dwMousePosition', COORD),
        ('dwButtonState', DWORD),
        ('dwControlKeyState', DWORD),
        ('dwEventFlags', DWORD)]


class WINDOW_BUFFER_SIZE_RECORD(ctypes.Structure):
    _fields_ = [('dwSize', COORD)]


class _Event(ctypes.Union):
    _fields_ = [
        ('KeyEvent', KEY_EVENT_RECORD),
        ('MouseEvent', MOUSE_EVENT_RECORD),
        ('WindowsBufferSizeEvent', WINDOW_BUFFER_SIZE_RECORD),
        ('MenuEvent', MENU_EVENT_RECORD),
        ('FocusEvent', FOCUS_EVENT_RECORD)]


class INPUT_RECORD(ctypes.Structure):

    _anonymous_ = ('Event',)
    _fields_ = [('EventType', WORD), ('Event', _Event)]


class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [
        ('dwSize', COORD),
        ('dwCursorPosition', COORD),
        ('wAttributes', WORD),
        ('srWindow', SMALL_RECT),
        ('dwMaximumWindowSize', COORD)]


class CONSOLE_FONT_INFO(ctypes.Structure):
    _fields_ = [
        ('nFont', DWORD),
        ('dwFontSize', COORD)]


PCHAR_INFO = POINTER(CHAR_INFO)
PFOCUS_EVENT_RECORD = POINTER(FOCUS_EVENT_RECORD)
PMENU_EVENT_RECORD = POINTER(MENU_EVENT_RECORD)
PCONSOLE_CURSOR_INFO = POINTER(CONSOLE_CURSOR_INFO)
PCONSOLE_FONT_INFO = POINTER(CONSOLE_FONT_INFO)
PCONSOLE_SCREEN_BUFFER_INFO = POINTER(CONSOLE_SCREEN_BUFFER_INFO)


_FreeConsole = function_factory(
    dlls.kernel32.FreeConsole, None, BOOL)

_AllocConsole = function_factory(
   dlls.kernel32.AllocConsole, None, BOOL)

_AttachConsole = function_factory(
   dlls.kernel32.AttachConsole, [DWORD], BOOL)

_GetStdHandle = function_factory(
    dlls.kernel32.GetStdHandle,
    [DWORD],
    HANDLE,
    check_invalid_handle)

_GetConsoleMode = function_factory(
    dlls.kernel32.GetConsoleMode,
    [HANDLE, LPDWORD],
    BOOL,
    check_false)

_GetConsoleCursorInfo = function_factory(
    dlls.kernel32.GetConsoleCursorInfo,
    [HANDLE, PCONSOLE_CURSOR_INFO],
    BOOL,
    check_false)

_SetConsoleCursorInfo = function_factory(
    dlls.kernel32.SetConsoleCursorInfo,
    [HANDLE, PCONSOLE_CURSOR_INFO],
    BOOL,
    check_false)

_SetConsoleCursorPosition = function_factory(
    dlls.kernel32.SetConsoleCursorPosition,
    [HANDLE, COORD],
    BOOL,
    check_false)

_GetConsoleScreenBufferInfo = function_factory(
    dlls.kernel32.GetConsoleScreenBufferInfo,
    [HANDLE, PCONSOLE_SCREEN_BUFFER_INFO],
    BOOL,
    check_false)

_GetCurrentConsoleFont = function_factory(
    dlls.kernel32.GetCurrentConsoleFont,
    [HANDLE, BOOL, PCONSOLE_FONT_INFO],
    BOOL,
    check_false)

_GetLargestConsoleWindowSize = function_factory(
   dlls.kernel32.GetLargestConsoleWindowSize, [HANDLE], COORD)

_AddConsoleAlias = function_factory(
    dlls.kernel32.AddConsoleAlias,
    [LPCTSTR, LPCTSTR, LPCTSTR],
    BOOL,
    check_false)
