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
    LPCTSTR, LPTSTR, CHAR, TCHAR, WCHAR, UINT, LPVOID,
    LPWORD)
from subprocess import (  # noqa
    STD_INPUT_HANDLE, STD_OUTPUT_HANDLE, STD_ERROR_HANDLE)
from ._util import (
    check_invalid_handle, check_false, function_factory, dlls,
    check_zero)
from ._security import LPSECURITY_ATTRIBUTES


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


HANDLER_ROUTINE = ctypes.WINFUNCTYPE(BOOL, DWORD)

PHANDLER_ROUTINE = POINTER(HANDLER_ROUTINE)
PCHAR_INFO = POINTER(CHAR_INFO)
PFOCUS_EVENT_RECORD = POINTER(FOCUS_EVENT_RECORD)
PMENU_EVENT_RECORD = POINTER(MENU_EVENT_RECORD)
PCONSOLE_CURSOR_INFO = POINTER(CONSOLE_CURSOR_INFO)
PCONSOLE_FONT_INFO = POINTER(CONSOLE_FONT_INFO)
PCONSOLE_SCREEN_BUFFER_INFO = POINTER(CONSOLE_SCREEN_BUFFER_INFO)
PINPUT_RECORD = POINTER(INPUT_RECORD)
PSMALL_RECT = POINTER(SMALL_RECT)

_FreeConsole = function_factory(
    dlls.kernel32.FreeConsole, None, BOOL)

_AllocConsole = function_factory(
   dlls.kernel32.AllocConsole, None, BOOL)

_AttachConsole = function_factory(
   dlls.kernel32.AttachConsole, [DWORD], BOOL)

_GetStdHandle = function_factory(
    dlls.kernel32.GetStdHandle,
    [DWORD], HANDLE, check_invalid_handle)

_GetConsoleMode = function_factory(
    dlls.kernel32.GetConsoleMode,
    [HANDLE, LPDWORD], BOOL, check_false)

_GetConsoleCursorInfo = function_factory(
    dlls.kernel32.GetConsoleCursorInfo,
    [HANDLE, PCONSOLE_CURSOR_INFO], BOOL, check_false)

_SetConsoleCursorInfo = function_factory(
    dlls.kernel32.SetConsoleCursorInfo,
    [HANDLE, PCONSOLE_CURSOR_INFO], BOOL, check_false)

_SetConsoleCursorPosition = function_factory(
    dlls.kernel32.SetConsoleCursorPosition,
    [HANDLE, COORD], BOOL, check_false)

_GetConsoleScreenBufferInfo = function_factory(
    dlls.kernel32.GetConsoleScreenBufferInfo,
    [HANDLE, PCONSOLE_SCREEN_BUFFER_INFO], BOOL, check_false)

_GetCurrentConsoleFont = function_factory(
    dlls.kernel32.GetCurrentConsoleFont,
    [HANDLE, BOOL, PCONSOLE_FONT_INFO], BOOL, check_false)

_GetLargestConsoleWindowSize = function_factory(
   dlls.kernel32.GetLargestConsoleWindowSize, [HANDLE], COORD)

_AddConsoleAlias = function_factory(
    dlls.kernel32.AddConsoleAlias,
    [LPCTSTR, LPCTSTR, LPCTSTR], BOOL, check_false)

_CreateConsoleScreenBuffer = function_factory(
    dlls.kernel32.CreateConsoleScreenBuffer,
    [DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, LPVOID],
    HANDLE, check_invalid_handle)

_FillConsoleOutputAttribute = function_factory(
    dlls.kernel32.FillConsoleOutputAttribute,
    [HANDLE, WORD, DWORD, COORD, LPDWORD],
    BOOL, check_false)

_FillConsoleOutputCharacter = function_factory(
    dlls.kernel32.FillConsoleOutputCharacter,
    [HANDLE, TCHAR, DWORD, COORD, LPDWORD],
    BOOL, check_false)

_FlushConsoleInputBuffer = function_factory(
    dlls.kernel32.FlushConsoleInputBuffer,
    [HANDLE], BOOL, check_false)

_GenerateConsole = function_factory(
    dlls.kernel32.GenerateConsoleCtrlEvent,
    [DWORD, DWORD], BOOL, check_false)

_GetConsoleCP = function_factory(
    dlls.kernel32.GetConsoleCP, None, UINT)

_GetConsoleOutputCP = function_factory(
    dlls.kernel32.GetConsoleOutputCP, None, UINT)

_GetConsoleTitle = function_factory(
    dlls.kernel32.GetConsoleTitle,
    [LPTSTR, DWORD], DWORD, check_zero)

_GetNumberOfConsoleInputEvents = function_factory(
    dlls.kernel32.GetNumberOfConsoleInputEvents,
    [HANDLE, LPDWORD], BOOL, check_false)

_GetNumberOfConsoleMouseButtons = function_factory(
    dlls.kernel32.GetNumberOfConsoleMouseButtons,
    [HANDLE, LPDWORD], BOOL, check_false)

_PeekConsoleInput = function_factory(
    dlls.kernel32.PeekConsoleInput,
    [HANDLE, PINPUT_RECORD, DWORD, LPDWORD], BOOL, check_false)

_ReadConsole = function_factory(
    dlls.kernel32.ReadConsole,
    [HANDLE, LPVOID, DWORD, LPDWORD, LPVOID], BOOL, check_false)

_ReadConsoleInput = function_factory(
    dlls.kernel32.ReadConsoleInput,
    [HANDLE, PINPUT_RECORD, DWORD, LPDWORD], BOOL, check_false)

_ReadConsoleOutput = function_factory(
    dlls.kernel32.ReadConsoleOuput,
    [HANDLE, PCHAR_INFO, COORD, COORD, PSMALL_RECT], BOOL, check_false)

_ReadConsoleOutputAttribute = function_factory(
    dlls.kernel32.ReadConsoleOuputAttribute,
    [HANDLE, LPWORD, DWORD, COORD, LPDWORD], BOOL, check_false)

_ReadConsoleOutputCharacter = function_factory(
    dlls.kernel32.ReadConsoleOuputCharacter,
    [HANDLE, LPTSTR, DWORD, COORD, LPDWORD], BOOL, check_false)

_ScrollConsoleScreenBuffer = function_factory(
    dlls.kernel32.ScrollConsoleScreenBuffer,
    [HANDLE, PSMALL_RECT, PSMALL_RECT, COORD, PCHAR_INFO],
    BOOL, check_false)

_SetConsoleActiveScreenBuffer = function_factory(
    dlls.kernel32.SetConsoleActiveScreenBuffer,
    [HANDLE], BOOL, check_false)

_SetConsoleCP = function_factory(
    dlls.kernel32.SetConsoleCP, [UINT], BOOL, check_false)

_SetConsoleCtrlHandler = function_factory(
    dlls.kernel32.SetConsoleCtrlHandler,
    [PHANDLER_ROUTINE, BOOL], BOOL, check_false)

_SetConsoleMode = function_factory(
    dlls.kernel32.SetConsoleMode,
    [HANDLE, DWORD], BOOL, check_false)

_SetConsoleOutputCP = function_factory(
    dlls.kernel32.SetConsoleOutputCP,
    [UINT], BOOL, check_false)

_SetConsoleScreenBufferSize = function_factory(
    dlls.kernel32.SetConsoleScreenBufferSize,
    [HANDLE, COORD], BOOL, check_false)

_SetConsoleTextAttribute = function_factory(
    dlls.kernel32.SetConsoleTextAttribute,
    [HANDLE, WORD], BOOL, check_false)

_SetConsoleTitle = function_factory(
    dlls.kernel32.SetConsoleTitle,
    [LPCTSTR, WORD], BOOL, check_false)

_SetConsoleWindowInfo = function_factory(
    dlls.kernel32.SetConsoleWindowInfo,
    [HANDLE, BOOL, PSMALL_RECT], BOOL, check_false)

_SetStdHandle = function_factory(
    dlls.kernel32.SetStdHandle,
    [DWORD, HANDLE], BOOL, check_false)

_WriteConsole = function_factory(
    dlls.kernel32.WriteConsole,
    [HANDLE, LPVOID, DWORD, LPDWORD, LPVOID], BOOL, check_false)

_WriteConsoleInput = function_factory(
    dlls.kernel32.WriteConsoleInput,
    [HANDLE, PINPUT_RECORD, DWORD, LPDWORD], BOOL, check_false)

_WriteConsoleOutput = function_factory(
    dlls.kernel32.WriteConsoleOutput,
    [HANDLE, PCHAR_INFO, COORD, COORD, PSMALL_RECT], BOOL, check_false)

_WriteConsoleOutputAttribute = function_factory(
    dlls.kernel32.WriteConsoleOutputAttribute,
    [HANDLE, LPWORD, DWORD, COORD, LPDWORD], BOOL, check_false)

_WriteConsoleOutputCharacter = function_factory(
    dlls.kernel32.WriteConsoleOutputCharacter,
    [HANDLE, LPCTSTR, DWORD, COORD, LPDWORD], BOOL, check_false)
