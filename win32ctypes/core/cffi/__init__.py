#
# (C) Copyright 2014-2023 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
import logging
# Initialize the ffi cdef
from . import _cdefinitions  # noqa

logger = logging.getLogger(__name__)
logger.debug('Loaded cffi backend')
