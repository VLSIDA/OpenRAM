#
#
# Copyright (C) 2002-2005 Jorg Lehmann <joergl@users.sourceforge.net>
# Copyright (C) 2002-2006 Andre Wobst <wobsta@users.sourceforge.net>
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

"""Python graphics package

PyX is a Python package for the creation of PostScript and PDF files. It
combines an abstraction of the PostScript drawing model with a TeX/LaTeX
interface. Complex tasks like 2d and 3d plots in publication-ready quality are
built out of these primitives.
"""

from .version import version
__version__ = version

__all__ = ["attr", "box", "bitmap", "canvas", "color", "connector", "deco", "deformer", "document",
           "epsfile", "graph", "mesh", "path", "pattern", "style", "trafo", "text", "unit"]


# automatically import main modules into pyx namespace
for module in __all__:
    __import__(module, globals(), locals(), [])
