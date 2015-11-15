#------------------------------------------------------------------------------
#
#  Copyright (c) 2015, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#------------------------------------------------------------------------------
import sys


def mock_modules():
    """ Mock missing modules if necessary """

    MOCK_MODULES = []
    MOCK_TYPES = []

    try:
        import cffi
    except ImportError:
        MOCK_MODULES = ['cffi']
        MOCK_TYPES = []
    else:
        del cffi

    TYPES = {
        mock_type: type(mock_type, bases, {'__module__': path})
        for path, mock_type, bases in MOCK_TYPES}

    class DocMock(object):

        def __init__(self, *args, **kwds):
            if '__doc_mocked_name__' in kwds:
                self.__docmock_name__ = kwds['__docmocked_name__']
            else:
                self.__docmock_name__ = 'Unknown'

        def __getattr__(self, name):
            if name in ('__file__', '__path__'):
                return '/dev/null'
            elif name == '__all__':
                return []
            else:
                return TYPES.get(name, DocMock(__docmock_name__=name))

        def __call__(self, *args, **kwards):
            return DocMock()

        def __iter__(self):
            return self

        def __next__(self):
            raise StopIteration()

        def next(self):
            raise StopIteration()

        @property
        def __name__(self):
            return self.__docmock_name__

        def __repr__(self):
            return '<DocMock.{}>'.format(self.__name__)

    sys.modules.update(
        (mod_name, DocMock(mocked_name=mod_name)) for mod_name in MOCK_MODULES)
    print('mocking modules {} and types {}'.format(MOCK_MODULES, MOCK_TYPES))
