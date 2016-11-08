# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2002 Jörg Lehmann <joergl@users.sourceforge.net>
# Copyright (C) 2002 André Wobst <wobsta@users.sourceforge.net>
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

import os

styles = (("10pt", "article", "10pt", "" , ),
          ("11pt", "article", "11pt", "" , ),
          ("12pt", "article", "12pt", "" , ),
          ("10ptex", "article", "10pt", "\\usepackage{exscale}" , ),
          ("11ptex", "article", "11pt", "\\usepackage{exscale}" , ),
          ("12ptex", "article", "12pt", "\\usepackage{exscale}" , ),
          ("foils17pt", "foils", "17pt", "" , ),
          ("foils20pt", "foils", "20pt", "" , ),
          ("foils25pt", "foils", "25pt", "" , ),
          ("foils30pt", "foils", "30pt", "" , ), )

for style in styles:
    os.system("echo \'%s\n%s\n%s\n%s\'|latex createlfs.tex" % style)
