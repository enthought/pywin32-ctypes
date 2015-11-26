#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
import os
__version__ = open(
    os.path.join(
        os.path.dirname(__file__), '..', 'VERSION')).read().strip()
