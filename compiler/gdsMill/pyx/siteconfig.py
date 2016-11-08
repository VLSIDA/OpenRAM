# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2004-2005 André Wobst <wobsta@users.sourceforge.net>
#
# This file is part of PyX (http://pyx.sourceforge.net/).
#
# PyX is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PyX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyX; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# This file configures PyX search paths relative to the current
# position, e.g. for local usage. When installing PyX via distutils
# the contents of this file is not copied to the PyX installation.
# Instead the correct information about the paths from the installation
# process are used.
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import os

lfsdir = os.path.join(os.path.dirname(__file__), "lfs")
sharedir = os.path.join(os.path.dirname(__file__), "..", "contrib")
pyxrcdir = os.path.join(os.path.dirname(__file__), "..")

