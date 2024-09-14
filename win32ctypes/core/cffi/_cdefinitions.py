#
# (C) Copyright 2024 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
" C definitions for the ffi modules "

from ._util import ffi

# _dll module cdefs
ffi.cdef("""

HMODULE WINAPI LoadLibraryExW(LPCTSTR lpFileName, HANDLE hFile, DWORD dwFlags);
BOOL WINAPI FreeLibrary(HMODULE hModule);

""")

# _winbase module cdefs
ffi.cdef("""

typedef struct _FILETIME {
  DWORD dwLowDateTime;
  DWORD dwHighDateTime;
} FILETIME, *PFILETIME, *LPFILETIME;

""")

# _authentication module cdefs
ffi.cdef("""
typedef struct _CREDENTIAL_ATTRIBUTE {
  LPWSTR Keyword;
  DWORD  Flags;
  DWORD  ValueSize;
  LPBYTE Value;
} CREDENTIAL_ATTRIBUTE, *PCREDENTIAL_ATTRIBUTE;

typedef struct _CREDENTIAL {
  DWORD                 Flags;
  DWORD                 Type;
  LPWSTR                TargetName;
  LPWSTR                Comment;
  FILETIME              LastWritten;
  DWORD                 CredentialBlobSize;
  LPBYTE                CredentialBlob;
  DWORD                 Persist;
  DWORD                 AttributeCount;
  PCREDENTIAL_ATTRIBUTE Attributes;
  LPWSTR                TargetAlias;
  LPWSTR                UserName;
} CREDENTIAL, *PCREDENTIAL;


BOOL WINAPI CredReadW(
    LPCWSTR TargetName, DWORD Type, DWORD Flags, PCREDENTIAL *Credential);
BOOL WINAPI CredWriteW(PCREDENTIAL Credential, DWORD);
VOID WINAPI CredFree(PVOID Buffer);
BOOL WINAPI CredDeleteW(LPCWSTR TargetName, DWORD Type, DWORD Flags);
BOOL WINAPI CredEnumerateW(
    LPCWSTR Filter, DWORD Flags, DWORD *Count, PCREDENTIAL **Credential);
""")


# _nt_support module cdefs
ffi.cdef("""

UINT WINAPI GetACP(void);

""")


# _resource module cdefs
ffi.cdef("""

typedef int WINBOOL;
typedef WINBOOL (__stdcall *ENUMRESTYPEPROC) (HANDLE, LPTSTR, LONG_PTR);
typedef WINBOOL (__stdcall *ENUMRESNAMEPROC) (HANDLE, LPCTSTR, LPTSTR, LONG_PTR);
typedef WINBOOL (__stdcall *ENUMRESLANGPROC) (HANDLE, LPCTSTR, LPCTSTR, WORD, LONG_PTR);

BOOL WINAPI EnumResourceTypesW(
    HMODULE hModule, ENUMRESTYPEPROC lpEnumFunc, LONG_PTR lParam);
BOOL WINAPI EnumResourceNamesW(
    HMODULE hModule, LPCTSTR lpszType,
    ENUMRESNAMEPROC lpEnumFunc, LONG_PTR lParam);
BOOL WINAPI EnumResourceLanguagesW(
    HMODULE hModule, LPCTSTR lpType,
    LPCTSTR lpName, ENUMRESLANGPROC lpEnumFunc, LONG_PTR lParam);
HRSRC WINAPI FindResourceExW(
    HMODULE hModule, LPCTSTR lpType, LPCTSTR lpName, WORD wLanguage);
DWORD WINAPI SizeofResource(HMODULE hModule, HRSRC hResInfo);
HGLOBAL WINAPI LoadResource(HMODULE hModule, HRSRC hResInfo);
LPVOID WINAPI LockResource(HGLOBAL hResData);

HANDLE WINAPI BeginUpdateResourceW(LPCTSTR pFileName, BOOL bDeleteExistingResources);
BOOL WINAPI EndUpdateResourceW(HANDLE hUpdate, BOOL fDiscard);
BOOL WINAPI UpdateResourceW(HANDLE hUpdate, LPCTSTR lpType, LPCTSTR lpName, WORD wLanguage, LPVOID lpData, DWORD cbData);

""")  # noqa


# _system_information module cdefs
ffi.cdef("""

BOOL WINAPI Beep(DWORD dwFreq, DWORD dwDuration);
UINT WINAPI GetWindowsDirectoryW(LPTSTR lpBuffer, UINT uSize);
UINT WINAPI GetSystemDirectoryW(LPTSTR lpBuffer, UINT uSize);
DWORD WINAPI GetTickCount(void);

""")
