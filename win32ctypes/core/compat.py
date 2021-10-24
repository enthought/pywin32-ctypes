import sys

if sys.version_info[0] >= 3:
    PY3 = True
    PY2 = False
else:
    PY3 = False
    PY2 = True

if PY3:
    def is_bytes(b):
        return isinstance(b, bytes)

    def is_text(s):
        return isinstance(s, str)

    def is_integer(i):
        return isinstance(i, int)

    text_type = str
else:
    def is_text(s):
        return isinstance(s, unicode)  # noqa

    def is_bytes(b):
        return isinstance(b, (bytes, str))

    def is_integer(i):
        return isinstance(i, (int, long))  # noqa

    text_type = unicode  # noqa
