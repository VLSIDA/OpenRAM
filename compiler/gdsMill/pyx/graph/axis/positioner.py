# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2005-2006 André Wobst <wobsta@users.sourceforge.net>
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

import math
from pyx import path, unit


class _positioner:
    """interface definition of axis tick position methods
    - these methods are used for the postitioning of the ticks
      when painting an axis"""
    # TODO: should we add a local transformation (for label text etc?)
    #       (this might replace tickdirection (and even tickposition?))

    def vbasepath(self, v1=None, v2=None):
        """return the basepath as a path
        - like basepath, but for graph coordinates"""

    def vgridpath(self, v):
        """return the gridpath as a path for a given position v
        in graph coordinates
        - might return None when no gridpath is available"""
        return None

    def vtickpoint_pt(self, v):
        """return tick position (x, y) in pts for a tick at position v in graph coordinates"""

    def vtickdirection(self, v):
        """return direction tuple (dx, dy) for a tick at position v in graph coordinates"""


class pathpositioner(_positioner):
    """axis tick position methods along an arbitrary path"""

    def __init__(self, p, direction=1):
        self.path = p
        self.normpath = p.normpath()
        self.arclen_pt = self.normpath.arclen_pt()
        self.arclen = self.arclen_pt * unit.t_pt
        self.direction = direction

    def vbasepath(self, v1=None, v2=None):
        if v1 is None:
            if v2 is None:
                return self.path
            else:
                return self.normpath.split(self.normpath.arclentoparam(v2 * self.arclen))[0]
        else:
            if v2 is None:
                return self.normpath.split(self.normpath.arclentoparam(v1 * self.arclen))[1]
            else:
                return self.normpath.split(*self.normpath.arclentoparam([v1 * self.arclen, v2 * self.arclen]))[1]

    def vtickpoint_pt(self, v):
        return self.normpath.at_pt(self.normpath.arclentoparam(v * self.arclen))

    def vtickdirection(self, v):
        return self.normpath.rotation(self.normpath.arclentoparam(v * self.arclen)).apply_pt(0, self.direction)


class lineaxispos_pt:
    """an axispos linear along a line with a fix direction for the ticks"""

    def __init__(self, x1_pt, y1_pt, x2_pt, y2_pt, fixtickdirection, vgridpath):
        self.x1_pt = x1_pt
        self.y1_pt = y1_pt
        self.x2_pt = x2_pt
        self.y2_pt = y2_pt
        self.fixtickdirection = fixtickdirection
        self.vgridpath = vgridpath

    def vbasepath(self, v1=None, v2=None):
        if v1 is None:
            v1 = 0
        if v2 is None:
            v2 = 1
        return path.line_pt((1-v1)*self.x1_pt+v1*self.x2_pt,
                            (1-v1)*self.y1_pt+v1*self.y2_pt,
                            (1-v2)*self.x1_pt+v2*self.x2_pt,
                            (1-v2)*self.y1_pt+v2*self.y2_pt)

    def vtickpoint_pt(self, v):
        return (1-v)*self.x1_pt+v*self.x2_pt, (1-v)*self.y1_pt+v*self.y2_pt

    def vtickdirection(self, v):
        return self.fixtickdirection


class flexlineaxispos_pt(lineaxispos_pt):
    """an axispos linear along a line with flexible direction for the ticks"""

    def __init__(self, vtickpoint_pt, vtickdirection, vgridpath):
        self.vtickpoint_pt = vtickpoint_pt
        self.vtickdirection = vtickdirection
        self.vgridpath = vgridpath

    def vbasepath(self, v1=None, v2=None):
        if v1 is None:
            v1 = 0
        if v2 is None:
            v2 = 1
        x1_pt, y1_pt = self.vtickpoint_pt(v1)
        x2_pt, y2_pt = self.vtickpoint_pt(v2)
        return path.line_pt(x1_pt, y1_pt, x2_pt, y2_pt)
