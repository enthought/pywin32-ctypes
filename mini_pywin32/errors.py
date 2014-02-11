class MiniPyWin32Exception(Exception):
    pass

class Win32Error(MiniPyWin32Exception):
    def __init__(self, message, winerror):
        self.message = message
        self.winerror = winerror
