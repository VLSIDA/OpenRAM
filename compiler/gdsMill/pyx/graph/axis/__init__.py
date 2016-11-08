# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2004-2006 André Wobst <wobsta@users.sourceforge.net>
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


__allmodules__ = ["painter", "parter", "rater", "texter", "tick"]
for module in __allmodules__:
    __import__(module, globals(), locals(), [])

import axis
__allaxis__ = ["linear", "lin", "logarithmic", "log",
               "bar", "nestedbar", "split",
               "sizedlinear", "sizedlin", "autosizedlinear", "autosizedlin",
               "anchoredaxis", "linkedaxis",
               "anchoredpathaxis", "pathaxis"]
for importfromaxis in __allaxis__:
    locals()[importfromaxis] = getattr(axis, importfromaxis)

__all__ = __allmodules__ + __allaxis__
