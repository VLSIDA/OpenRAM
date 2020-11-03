# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2002-2006 Jörg Lehmann <joergl@users.sourceforge.net>
# Copyright (C) 2003-2005 Michael Schindler <m-schindler@users.sourceforge.net>
# Copyright (C) 2002-2006 André Wobst <wobsta@users.sourceforge.net>
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

from __future__ import nested_scopes

import math
from math import cos, sin, tan, acos, pi
try:
    from math import radians, degrees
except ImportError:
    # fallback implementation for Python 2.1
    def radians(x): return x*pi/180
    def degrees(x): return x*180/pi

import trafo, unit
from normpath import NormpathException, normpath, normsubpath, normline_pt, normcurve_pt
import bbox as bboxmodule

# set is available as an external interface to the normpath.set method
from normpath import set
# normpath's invalid is available as an external interface
from normpath import invalid

try:
    sum([])
except NameError:
    # fallback implementation for Python 2.2 and below
    def sum(list):
        return reduce(lambda x, y: x+y, list, 0)

try:
    enumerate([])
except NameError:
    # fallback implementation for Python 2.2 and below
    def enumerate(list):
        return zip(xrange(len(list)), list)

# use new style classes when possible
__metaclass__ = type

class _marker: pass

################################################################################

# specific exception for path-related problems
class PathException(Exception): pass

################################################################################
# Bezier helper functions
################################################################################

def _bezierpolyrange(x0, x1, x2, x3):
    tc = [0, 1]

    a = x3 - 3*x2 + 3*x1 - x0
    b = 2*x0 - 4*x1 + 2*x2
    c = x1 - x0

    s = b*b - 4*a*c
    if s >= 0:
        if b >= 0:
            q = -0.5*(b+math.sqrt(s))
        else:
            q = -0.5*(b-math.sqrt(s))

        try:
            t = q*1.0/a
        except ZeroDivisionError:
            pass
        else:
            if 0 < t < 1:
                tc.append(t)

        try:
            t = c*1.0/q
        except ZeroDivisionError:
            pass
        else:
            if 0 < t < 1:
                tc.append(t)

    p = [(((a*t + 1.5*b)*t + 3*c)*t + x0) for t in tc]

    return min(*p), max(*p)


def _arctobcurve(x_pt, y_pt, r_pt, phi1, phi2):
    """generate the best bezier curve corresponding to an arc segment"""

    dphi = phi2-phi1

    if dphi==0: return None

    # the two endpoints should be clear
    x0_pt, y0_pt = x_pt+r_pt*cos(phi1), y_pt+r_pt*sin(phi1)
    x3_pt, y3_pt = x_pt+r_pt*cos(phi2), y_pt+r_pt*sin(phi2)

    # optimal relative distance along tangent for second and third
    # control point
    l = r_pt*4*(1-cos(dphi/2))/(3*sin(dphi/2))

    x1_pt, y1_pt = x0_pt-l*sin(phi1), y0_pt+l*cos(phi1)
    x2_pt, y2_pt = x3_pt+l*sin(phi2), y3_pt-l*cos(phi2)

    return normcurve_pt(x0_pt, y0_pt, x1_pt, y1_pt, x2_pt, y2_pt, x3_pt, y3_pt)


def _arctobezierpath(x_pt, y_pt, r_pt, phi1, phi2, dphimax=45):
    apath = []

    phi1 = radians(phi1)
    phi2 = radians(phi2)
    dphimax = radians(dphimax)

    if phi2<phi1:
        # guarantee that phi2>phi1 ...
        phi2 = phi2 + (math.floor((phi1-phi2)/(2*pi))+1)*2*pi
    elif phi2>phi1+2*pi:
        # ... or remove unnecessary multiples of 2*pi
        phi2 = phi2 - (math.floor((phi2-phi1)/(2*pi))-1)*2*pi

    if r_pt == 0 or phi1-phi2 == 0: return []

    subdivisions = abs(int((1.0*(phi1-phi2))/dphimax))+1

    dphi = (1.0*(phi2-phi1))/subdivisions

    for i in range(subdivisions):
        apath.append(_arctobcurve(x_pt, y_pt, r_pt, phi1+i*dphi, phi1+(i+1)*dphi))

    return apath

def _arcpoint(x_pt, y_pt, r_pt, angle):
    """return starting point of arc segment"""
    return x_pt+r_pt*cos(radians(angle)), y_pt+r_pt*sin(radians(angle))

def _arcbboxdata(x_pt, y_pt, r_pt, angle1, angle2):
    phi1 = radians(angle1)
    phi2 = radians(angle2)

    # starting end end point of arc segment
    sarcx_pt, sarcy_pt = _arcpoint(x_pt, y_pt, r_pt, angle1)
    earcx_pt, earcy_pt = _arcpoint(x_pt, y_pt, r_pt, angle2)

    # Now, we have to determine the corners of the bbox for the
    # arc segment, i.e. global maxima/mimima of cos(phi) and sin(phi)
    # in the interval [phi1, phi2]. These can either be located
    # on the borders of this interval or in the interior.

    if phi2 < phi1:
        # guarantee that phi2>phi1
        phi2 = phi2 + (math.floor((phi1-phi2)/(2*pi))+1)*2*pi

    # next minimum of cos(phi) looking from phi1 in counterclockwise
    # direction: 2*pi*floor((phi1-pi)/(2*pi)) + 3*pi

    if phi2 < (2*math.floor((phi1-pi)/(2*pi))+3)*pi:
        minarcx_pt = min(sarcx_pt, earcx_pt)
    else:
        minarcx_pt = x_pt-r_pt

    # next minimum of sin(phi) looking from phi1 in counterclockwise
    # direction: 2*pi*floor((phi1-3*pi/2)/(2*pi)) + 7/2*pi

    if phi2 < (2*math.floor((phi1-3.0*pi/2)/(2*pi))+7.0/2)*pi:
        minarcy_pt = min(sarcy_pt, earcy_pt)
    else:
        minarcy_pt = y_pt-r_pt

    # next maximum of cos(phi) looking from phi1 in counterclockwise
    # direction: 2*pi*floor((phi1)/(2*pi))+2*pi

    if phi2 < (2*math.floor((phi1)/(2*pi))+2)*pi:
        maxarcx_pt = max(sarcx_pt, earcx_pt)
    else:
        maxarcx_pt = x_pt+r_pt

    # next maximum of sin(phi) looking from phi1 in counterclockwise
    # direction: 2*pi*floor((phi1-pi/2)/(2*pi)) + 1/2*pi

    if phi2 < (2*math.floor((phi1-pi/2)/(2*pi))+5.0/2)*pi:
        maxarcy_pt = max(sarcy_pt, earcy_pt)
    else:
        maxarcy_pt = y_pt+r_pt

    return minarcx_pt, minarcy_pt, maxarcx_pt, maxarcy_pt


################################################################################
# path context and pathitem base class
################################################################################

class context:

    """context for pathitem"""

    def __init__(self, x_pt, y_pt, subfirstx_pt, subfirsty_pt):
        """initializes a context for path items

        x_pt, y_pt are the currentpoint. subfirstx_pt, subfirsty_pt
        are the starting point of the current subpath. There are no
        invalid contexts, i.e. all variables need to be set to integer
        or float numbers.
        """
        self.x_pt = x_pt
        self.y_pt = y_pt
        self.subfirstx_pt = subfirstx_pt
        self.subfirsty_pt = subfirsty_pt


class pathitem:

    """element of a PS style path"""

    def __str__(self):
        raise NotImplementedError()

    def createcontext(self):
        """creates a context from the current pathitem

        Returns a context instance. Is called, when no context has yet
        been defined, i.e. for the very first pathitem. Most of the
        pathitems do not provide this method. Note, that you should pass
        the context created by createcontext to updatebbox and updatenormpath
        of successive pathitems only; use the context-free createbbox and
        createnormpath for the first pathitem instead.
        """
        raise PathException("path must start with moveto or the like (%r)" % self)

    def createbbox(self):
        """creates a bbox from the current pathitem

        Returns a bbox instance. Is called, when a bbox has to be
        created instead of updating it, i.e. for the very first
        pathitem. Most pathitems do not provide this method.
        updatebbox must not be called for the created instance and the
        same pathitem.
        """
        raise PathException("path must start with moveto or the like (%r)" % self)

    def createnormpath(self, epsilon=_marker):
        """create a normpath from the current pathitem

        Return a normpath instance. Is called, when a normpath has to
        be created instead of updating it, i.e. for the very first
        pathitem. Most pathitems do not provide this method.
        updatenormpath must not be called for the created instance and
        the same pathitem.
        """
        raise PathException("path must start with moveto or the like (%r)" % self)

    def updatebbox(self, bbox, context):
        """updates the bbox to contain the pathitem for the given
        context

        Is called for all subsequent pathitems in a path to complete
        the bbox information. Both, the bbox and context are updated
        inplace. Does not return anything.
        """
        raise NotImplementedError()

    def updatenormpath(self, normpath, context):
        """update the normpath to contain the pathitem for the given
        context

        Is called for all subsequent pathitems in a path to complete
        the normpath. Both the normpath and the context are updated
        inplace. Most pathitem implementations will use
        normpath.normsubpath[-1].append to add normsubpathitem(s).
        Does not return anything.
        """
        raise NotImplementedError()

    def outputPS(self, file, writer):
        """write PS representation of pathitem to file"""



################################################################################
# various pathitems
################################################################################
# Each one comes in two variants:
#  - one with suffix _pt. This one requires the coordinates
#    to be already in pts (mainly used for internal purposes)
#  - another which accepts arbitrary units


class closepath(pathitem):

    """Connect subpath back to its starting point"""

    __slots__ = ()

    def __str__(self):
        return "closepath()"

    def updatebbox(self, bbox, context):
        context.x_pt = context.subfirstx_pt
        context.y_pt = context.subfirsty_pt

    def updatenormpath(self, normpath, context):
        normpath.normsubpaths[-1].close()
        context.x_pt = context.subfirstx_pt
        context.y_pt = context.subfirsty_pt

    def outputPS(self, file, writer):
        file.write("closepath\n")


class moveto_pt(pathitem):

    """Start a new subpath and set current point to (x_pt, y_pt) (coordinates in pts)"""

    __slots__ = "x_pt", "y_pt"

    def __init__(self, x_pt, y_pt):
        self.x_pt = x_pt
        self.y_pt = y_pt

    def __str__(self):
        return "moveto_pt(%g, %g)" % (self.x_pt, self.y_pt)

    def createcontext(self):
        return context(self.x_pt, self.y_pt, self.x_pt, self.y_pt)

    def createbbox(self):
        return bboxmodule.bbox_pt(self.x_pt, self.y_pt, self.x_pt, self.y_pt)

    def createnormpath(self, epsilon=_marker):
        if epsilon is _marker:
            return normpath([normsubpath([normline_pt(self.x_pt, self.y_pt, self.x_pt, self.y_pt)])])
        else:
            return normpath([normsubpath([normline_pt(self.x_pt, self.y_pt, self.x_pt, self.y_pt)],
                                         epsilon=epsilon)])

    def updatebbox(self, bbox, context):
        bbox.includepoint_pt(self.x_pt, self.y_pt)
        context.x_pt = context.subfirstx_pt = self.x_pt
        context.y_pt = context.subfirsty_pt = self.y_pt

    def updatenormpath(self, normpath, context):
        if normpath.normsubpaths[-1].epsilon is not None:
            normpath.append(normsubpath([normline_pt(self.x_pt, self.y_pt, self.x_pt, self.y_pt)],
                                        epsilon=normpath.normsubpaths[-1].epsilon))
        else:
            normpath.append(normsubpath(epsilon=normpath.normsubpaths[-1].epsilon))
        context.x_pt = context.subfirstx_pt = self.x_pt
        context.y_pt = context.subfirsty_pt = self.y_pt

    def outputPS(self, file, writer):
        file.write("%g %g moveto\n" % (self.x_pt, self.y_pt) )


class lineto_pt(pathitem):

    """Append straight line to (x_pt, y_pt) (coordinates in pts)"""

    __slots__ = "x_pt", "y_pt"

    def __init__(self, x_pt, y_pt):
        self.x_pt = x_pt
        self.y_pt = y_pt

    def __str__(self):
        return "lineto_pt(%g, %g)" % (self.x_pt, self.y_pt)

    def updatebbox(self, bbox, context):
        bbox.includepoint_pt(self.x_pt, self.y_pt)
        context.x_pt = self.x_pt
        context.y_pt = self.y_pt

    def updatenormpath(self, normpath, context):
        normpath.normsubpaths[-1].append(normline_pt(context.x_pt, context.y_pt,
                                                     self.x_pt, self.y_pt))
        context.x_pt = self.x_pt
        context.y_pt = self.y_pt

    def outputPS(self, file, writer):
        file.write("%g %g lineto\n" % (self.x_pt, self.y_pt) )


class curveto_pt(pathitem):

    """Append curveto (coordinates in pts)"""

    __slots__ = "x1_pt", "y1_pt", "x2_pt", "y2_pt", "x3_pt", "y3_pt"

    def __init__(self, x1_pt, y1_pt, x2_pt, y2_pt, x3_pt, y3_pt):
        self.x1_pt = x1_pt
        self.y1_pt = y1_pt
        self.x2_pt = x2_pt
        self.y2_pt = y2_pt
        self.x3_pt = x3_pt
        self.y3_pt = y3_pt

    def __str__(self):
        return "curveto_pt(%g, %g, %g, %g, %g, %g)" % (self.x1_pt, self.y1_pt,
                                                       self.x2_pt, self.y2_pt,
                                                       self.x3_pt, self.y3_pt)

    def updatebbox(self, bbox, context):
        xmin_pt, xmax_pt = _bezierpolyrange(context.x_pt, self.x1_pt, self.x2_pt, self.x3_pt)
        ymin_pt, ymax_pt = _bezierpolyrange(context.y_pt, self.y1_pt, self.y2_pt, self.y3_pt)
        bbox.includepoint_pt(xmin_pt, ymin_pt)
        bbox.includepoint_pt(xmax_pt, ymax_pt)
        context.x_pt = self.x3_pt
        context.y_pt = self.y3_pt

    def updatenormpath(self, normpath, context):
        normpath.normsubpaths[-1].append(normcurve_pt(context.x_pt, context.y_pt,
                                                      self.x1_pt, self.y1_pt,
                                                      self.x2_pt, self.y2_pt,
                                                      self.x3_pt, self.y3_pt))
        context.x_pt = self.x3_pt
        context.y_pt = self.y3_pt

    def outputPS(self, file, writer):
        file.write("%g %g %g %g %g %g curveto\n" % (self.x1_pt, self.y1_pt,
                                                    self.x2_pt, self.y2_pt,
                                                    self.x3_pt, self.y3_pt))


class rmoveto_pt(pathitem):

    """Perform relative moveto (coordinates in pts)"""

    __slots__ = "dx_pt", "dy_pt"

    def __init__(self, dx_pt, dy_pt):
         self.dx_pt = dx_pt
         self.dy_pt = dy_pt

    def __str__(self):
        return "rmoveto_pt(%g, %g)" % (self.dx_pt, self.dy_pt)

    def updatebbox(self, bbox, context):
        bbox.includepoint_pt(context.x_pt + self.dx_pt, context.y_pt + self.dy_pt)
        context.x_pt += self.dx_pt
        context.y_pt += self.dy_pt
        context.subfirstx_pt = context.x_pt
        context.subfirsty_pt = context.y_pt

    def updatenormpath(self, normpath, context):
        context.x_pt += self.dx_pt
        context.y_pt += self.dy_pt
        context.subfirstx_pt = context.x_pt
        context.subfirsty_pt = context.y_pt
        if normpath.normsubpaths[-1].epsilon is not None:
            normpath.append(normsubpath([normline_pt(context.x_pt, context.y_pt,
                                                     context.x_pt, context.y_pt)],
                                        epsilon=normpath.normsubpaths[-1].epsilon))
        else:
            normpath.append(normsubpath(epsilon=normpath.normsubpaths[-1].epsilon))

    def outputPS(self, file, writer):
        file.write("%g %g rmoveto\n" % (self.dx_pt, self.dy_pt) )


class rlineto_pt(pathitem):

    """Perform relative lineto (coordinates in pts)"""

    __slots__ = "dx_pt", "dy_pt"

    def __init__(self, dx_pt, dy_pt):
        self.dx_pt = dx_pt
        self.dy_pt = dy_pt

    def __str__(self):
        return "rlineto_pt(%g %g)" % (self.dx_pt, self.dy_pt)

    def updatebbox(self, bbox, context):
        bbox.includepoint_pt(context.x_pt + self.dx_pt, context.y_pt + self.dy_pt)
        context.x_pt += self.dx_pt
        context.y_pt += self.dy_pt

    def updatenormpath(self, normpath, context):
        normpath.normsubpaths[-1].append(normline_pt(context.x_pt, context.y_pt,
                                                     context.x_pt + self.dx_pt, context.y_pt + self.dy_pt))
        context.x_pt += self.dx_pt
        context.y_pt += self.dy_pt

    def outputPS(self, file, writer):
        file.write("%g %g rlineto\n" % (self.dx_pt, self.dy_pt) )


class rcurveto_pt(pathitem):

    """Append rcurveto (coordinates in pts)"""

    __slots__ = "dx1_pt", "dy1_pt", "dx2_pt", "dy2_pt", "dx3_pt", "dy3_pt"

    def __init__(self, dx1_pt, dy1_pt, dx2_pt, dy2_pt, dx3_pt, dy3_pt):
        self.dx1_pt = dx1_pt
        self.dy1_pt = dy1_pt
        self.dx2_pt = dx2_pt
        self.dy2_pt = dy2_pt
        self.dx3_pt = dx3_pt
        self.dy3_pt = dy3_pt

    def __str__(self):
        return "rcurveto_pt(%g, %g, %g, %g, %g, %g)" % (self.dx1_pt, self.dy1_pt,
                                                        self.dx2_pt, self.dy2_pt,
                                                        self.dx3_pt, self.dy3_pt)

    def updatebbox(self, bbox, context):
        xmin_pt, xmax_pt = _bezierpolyrange(context.x_pt,
                                            context.x_pt+self.dx1_pt,
                                            context.x_pt+self.dx2_pt,
                                            context.x_pt+self.dx3_pt)
        ymin_pt, ymax_pt = _bezierpolyrange(context.y_pt,
                                            context.y_pt+self.dy1_pt,
                                            context.y_pt+self.dy2_pt,
                                            context.y_pt+self.dy3_pt)
        bbox.includepoint_pt(xmin_pt, ymin_pt)
        bbox.includepoint_pt(xmax_pt, ymax_pt)
        context.x_pt += self.dx3_pt
        context.y_pt += self.dy3_pt

    def updatenormpath(self, normpath, context):
        normpath.normsubpaths[-1].append(normcurve_pt(context.x_pt, context.y_pt,
                                                      context.x_pt + self.dx1_pt, context.y_pt + self.dy1_pt,
                                                      context.x_pt + self.dx2_pt, context.y_pt + self.dy2_pt,
                                                      context.x_pt + self.dx3_pt, context.y_pt + self.dy3_pt))
        context.x_pt += self.dx3_pt
        context.y_pt += self.dy3_pt

    def outputPS(self, file, writer):
        file.write("%g %g %g %g %g %g rcurveto\n" % (self.dx1_pt, self.dy1_pt,
                                                     self.dx2_pt, self.dy2_pt,
                                                     self.dx3_pt, self.dy3_pt))


class arc_pt(pathitem):

    """Append counterclockwise arc (coordinates in pts)"""

    __slots__ = "x_pt", "y_pt", "r_pt", "angle1", "angle2"

    def __init__(self, x_pt, y_pt, r_pt, angle1, angle2):
        self.x_pt = x_pt
        self.y_pt = y_pt
        self.r_pt = r_pt
        self.angle1 = angle1
        self.angle2 = angle2

    def __str__(self):
        return "arc_pt(%g, %g, %g, %g, %g)" % (self.x_pt, self.y_pt, self.r_pt,
                                               self.angle1, self.angle2)

    def createcontext(self):
        x_pt, y_pt = _arcpoint(self.x_pt, self.y_pt, self.r_pt, self.angle2)
        return context(x_pt, y_pt, x_pt, y_pt)

    def createbbox(self):
        return bboxmodule.bbox_pt(*_arcbboxdata(self.x_pt, self.y_pt, self.r_pt,
                                                self.angle1, self.angle2))

    def createnormpath(self, epsilon=_marker):
        if epsilon is _marker:
            return normpath([normsubpath(_arctobezierpath(self.x_pt, self.y_pt, self.r_pt, self.angle1, self.angle2))])
        else:
            return normpath([normsubpath(_arctobezierpath(self.x_pt, self.y_pt, self.r_pt, self.angle1, self.angle2),
                                         epsilon=epsilon)])

    def updatebbox(self, bbox, context):
        minarcx_pt, minarcy_pt, maxarcx_pt, maxarcy_pt = _arcbboxdata(self.x_pt, self.y_pt, self.r_pt,
                                                                      self.angle1, self.angle2)
        bbox.includepoint_pt(minarcx_pt, minarcy_pt)
        bbox.includepoint_pt(maxarcx_pt, maxarcy_pt)
        context.x_pt, context.y_pt = _arcpoint(self.x_pt, self.y_pt, self.r_pt, self.angle2)

    def updatenormpath(self, normpath, context):
        if normpath.normsubpaths[-1].closed:
            normpath.append(normsubpath([normline_pt(context.x_pt, context.y_pt,
                                                         *_arcpoint(self.x_pt, self.y_pt, self.r_pt, self.angle1))],
                                        epsilon=normpath.normsubpaths[-1].epsilon))
        else:
            normpath.normsubpaths[-1].append(normline_pt(context.x_pt, context.y_pt,
                                                         *_arcpoint(self.x_pt, self.y_pt, self.r_pt, self.angle1)))
        normpath.normsubpaths[-1].extend(_arctobezierpath(self.x_pt, self.y_pt, self.r_pt, self.angle1, self.angle2))
        context.x_pt, context.y_pt = _arcpoint(self.x_pt, self.y_pt, self.r_pt, self.angle2)

    def outputPS(self, file, writer):
        file.write("%g %g %g %g %g arc\n" % (self.x_pt, self.y_pt,
                                             self.r_pt,
                                             self.angle1,
                                             self.angle2))


class arcn_pt(pathitem):

    """Append clockwise arc (coordinates in pts)"""

    __slots__ = "x_pt", "y_pt", "r_pt", "angle1", "angle2"

    def __init__(self, x_pt, y_pt, r_pt, angle1, angle2):
        self.x_pt = x_pt
        self.y_pt = y_pt
        self.r_pt = r_pt
        self.angle1 = angle1
        self.angle2 = angle2

    def __str__(self):
        return "arcn_pt(%g, %g, %g, %g, %g)" % (self.x_pt, self.y_pt, self.r_pt,
                                                self.angle1, self.angle2)

    def createcontext(self):
        x_pt, y_pt = _arcpoint(self.x_pt, self.y_pt, self.r_pt, self.angle2)
        return context(x_pt, y_pt, x_pt, y_pt)

    def createbbox(self):
        return bboxmodule.bbox_pt(*_arcbboxdata(self.x_pt, self.y_pt, self.r_pt,
                                                self.angle2, self.angle1))

    def createnormpath(self, epsilon=_marker):
        if epsilon is _marker:
            return normpath([normsubpath(_arctobezierpath(self.x_pt, self.y_pt, self.r_pt, self.angle2, self.angle1))]).reversed()
        else:
            return normpath([normsubpath(_arctobezierpath(self.x_pt, self.y_pt, self.r_pt, self.angle2, self.angle1),
                                         epsilon=epsilon)]).reversed()

    def updatebbox(self, bbox, context):
        minarcx_pt, minarcy_pt, maxarcx_pt, maxarcy_pt = _arcbboxdata(self.x_pt, self.y_pt, self.r_pt,
                                                                      self.angle2, self.angle1)
        bbox.includepoint_pt(minarcx_pt, minarcy_pt)
        bbox.includepoint_pt(maxarcx_pt, maxarcy_pt)
        context.x_pt, context.y_pt = _arcpoint(self.x_pt, self.y_pt, self.r_pt, self.angle2)

    def updatenormpath(self, normpath, context):
        if normpath.normsubpaths[-1].closed:
            normpath.append(normsubpath([normline_pt(context.x_pt, context.y_pt,
                                                         *_arcpoint(self.x_pt, self.y_pt, self.r_pt, self.angle1))],
                                        epsilon=normpath.normsubpaths[-1].epsilon))
        else:
            normpath.normsubpaths[-1].append(normline_pt(context.x_pt, context.y_pt,
                                                         *_arcpoint(self.x_pt, self.y_pt, self.r_pt, self.angle1)))
        bpathitems = _arctobezierpath(self.x_pt, self.y_pt, self.r_pt, self.angle2, self.angle1)
        bpathitems.reverse()
        for bpathitem in bpathitems:
            normpath.normsubpaths[-1].append(bpathitem.reversed())
        context.x_pt, context.y_pt = _arcpoint(self.x_pt, self.y_pt, self.r_pt, self.angle2)

    def outputPS(self, file, writer):
        file.write("%g %g %g %g %g arcn\n" % (self.x_pt, self.y_pt,
                                              self.r_pt,
                                              self.angle1,
                                              self.angle2))


class arct_pt(pathitem):

    """Append tangent arc (coordinates in pts)"""

    __slots__ = "x1_pt", "y1_pt", "x2_pt", "y2_pt", "r_pt"

    def __init__(self, x1_pt, y1_pt, x2_pt, y2_pt, r_pt):
        self.x1_pt = x1_pt
        self.y1_pt = y1_pt
        self.x2_pt = x2_pt
        self.y2_pt = y2_pt
        self.r_pt = r_pt

    def __str__(self):
        return "arct_pt(%g, %g, %g, %g, %g)" % (self.x1_pt, self.y1_pt,
                                                self.x2_pt, self.y2_pt,
                                                self.r_pt)

    def _pathitems(self, x_pt, y_pt):
        """return pathitems corresponding to arct for given currentpoint x_pt, y_pt.

        The return is a list containing line_pt, arc_pt, a arcn_pt instances.

        This is a helper routine for updatebbox and updatenormpath,
        which will delegate the work to the constructed pathitem.
        """

        # direction of tangent 1
        dx1_pt, dy1_pt = self.x1_pt-x_pt, self.y1_pt-y_pt
        l1_pt = math.hypot(dx1_pt, dy1_pt)
        dx1, dy1 = dx1_pt/l1_pt, dy1_pt/l1_pt

        # direction of tangent 2
        dx2_pt, dy2_pt = self.x2_pt-self.x1_pt, self.y2_pt-self.y1_pt
        l2_pt = math.hypot(dx2_pt, dy2_pt)
        dx2, dy2 = dx2_pt/l2_pt, dy2_pt/l2_pt

        # intersection angle between two tangents in the range (-pi, pi).
        # We take the orientation from the sign of the vector product.
        # Negative (positive) angles alpha corresponds to a turn to the right (left)
        # as seen from currentpoint.
        if dx1*dy2-dy1*dx2 > 0:
            alpha = acos(dx1*dx2+dy1*dy2)
        else:
            alpha = -acos(dx1*dx2+dy1*dy2)

        try:
            # two tangent points
            xt1_pt = self.x1_pt - dx1*self.r_pt*tan(abs(alpha)/2)
            yt1_pt = self.y1_pt - dy1*self.r_pt*tan(abs(alpha)/2)
            xt2_pt = self.x1_pt + dx2*self.r_pt*tan(abs(alpha)/2)
            yt2_pt = self.y1_pt + dy2*self.r_pt*tan(abs(alpha)/2)

            # direction point 1 -> center of arc
            dmx_pt = 0.5*(xt1_pt+xt2_pt) - self.x1_pt
            dmy_pt = 0.5*(yt1_pt+yt2_pt) - self.y1_pt
            lm_pt = math.hypot(dmx_pt, dmy_pt)
            dmx, dmy = dmx_pt/lm_pt, dmy_pt/lm_pt

            # center of arc
            mx_pt = self.x1_pt + dmx*self.r_pt/cos(alpha/2)
            my_pt = self.y1_pt + dmy*self.r_pt/cos(alpha/2)

            # angle around which arc is centered
            phi = degrees(math.atan2(-dmy, -dmx))

            # half angular width of arc
            deltaphi = degrees(alpha)/2

            line = lineto_pt(*_arcpoint(mx_pt, my_pt, self.r_pt, phi-deltaphi))
            if alpha > 0:
                return [line, arc_pt(mx_pt, my_pt, self.r_pt, phi-deltaphi, phi+deltaphi)]
            else:
                return [line, arcn_pt(mx_pt, my_pt, self.r_pt, phi-deltaphi, phi+deltaphi)]

        except ZeroDivisionError:
            # in the degenerate case, we just return a line as specified by the PS
            # language reference
            return [lineto_pt(self.x1_pt, self.y1_pt)]

    def updatebbox(self, bbox, context):
        for pathitem in self._pathitems(context.x_pt, context.y_pt):
            pathitem.updatebbox(bbox, context)

    def updatenormpath(self, normpath, context):
        for pathitem in self._pathitems(context.x_pt, context.y_pt):
            pathitem.updatenormpath(normpath, context)

    def outputPS(self, file, writer):
        file.write("%g %g %g %g %g arct\n" % (self.x1_pt, self.y1_pt,
                                              self.x2_pt, self.y2_pt,
                                              self.r_pt))

#
# now the pathitems that convert from user coordinates to pts
#

class moveto(moveto_pt):

    """Set current point to (x, y)"""

    __slots__ = "x_pt", "y_pt"

    def __init__(self, x, y):
        moveto_pt.__init__(self, unit.topt(x), unit.topt(y))


class lineto(lineto_pt):

    """Append straight line to (x, y)"""

    __slots__ = "x_pt", "y_pt"

    def __init__(self, x, y):
        lineto_pt.__init__(self, unit.topt(x), unit.topt(y))


class curveto(curveto_pt):

    """Append curveto"""

    __slots__ = "x1_pt", "y1_pt", "x2_pt", "y2_pt", "x3_pt", "y3_pt"

    def __init__(self, x1, y1, x2, y2, x3, y3):
        curveto_pt.__init__(self,
                            unit.topt(x1), unit.topt(y1),
                            unit.topt(x2), unit.topt(y2),
                            unit.topt(x3), unit.topt(y3))

class rmoveto(rmoveto_pt):

    """Perform relative moveto"""

    __slots__ = "dx_pt", "dy_pt"

    def __init__(self, dx, dy):
        rmoveto_pt.__init__(self, unit.topt(dx), unit.topt(dy))


class rlineto(rlineto_pt):

    """Perform relative lineto"""

    __slots__ = "dx_pt", "dy_pt"

    def __init__(self, dx, dy):
        rlineto_pt.__init__(self, unit.topt(dx), unit.topt(dy))


class rcurveto(rcurveto_pt):

    """Append rcurveto"""

    __slots__ = "dx1_pt", "dy1_pt", "dx2_pt", "dy2_pt", "dx3_pt", "dy3_pt"

    def __init__(self, dx1, dy1, dx2, dy2, dx3, dy3):
        rcurveto_pt.__init__(self,
                             unit.topt(dx1), unit.topt(dy1),
                             unit.topt(dx2), unit.topt(dy2),
                             unit.topt(dx3), unit.topt(dy3))


class arcn(arcn_pt):

    """Append clockwise arc"""

    __slots__ = "x_pt", "y_pt", "r_pt", "angle1", "angle2"

    def __init__(self, x, y, r, angle1, angle2):
        arcn_pt.__init__(self, unit.topt(x), unit.topt(y), unit.topt(r), angle1, angle2)


class arc(arc_pt):

    """Append counterclockwise arc"""

    __slots__ = "x_pt", "y_pt", "r_pt", "angle1", "angle2"

    def __init__(self, x, y, r, angle1, angle2):
        arc_pt.__init__(self, unit.topt(x), unit.topt(y), unit.topt(r), angle1, angle2)


class arct(arct_pt):

    """Append tangent arc"""

    __slots__ = "x1_pt", "y1_pt", "x2_pt", "y2_pt", "r_pt"

    def __init__(self, x1, y1, x2, y2, r):
        arct_pt.__init__(self, unit.topt(x1), unit.topt(y1),
                         unit.topt(x2), unit.topt(y2), unit.topt(r))

#
# "combined" pathitems provided for performance reasons
#

class multilineto_pt(pathitem):

    """Perform multiple linetos (coordinates in pts)"""

    __slots__ = "points_pt"

    def __init__(self, points_pt):
        self.points_pt = points_pt

    def __str__(self):
        result = []
        for point_pt in self.points_pt:
            result.append("(%g, %g)" % point_pt )
        return "multilineto_pt([%s])" % (", ".join(result))

    def updatebbox(self, bbox, context):
        for point_pt in self.points_pt:
            bbox.includepoint_pt(*point_pt)
        if self.points_pt:
            context.x_pt, context.y_pt = self.points_pt[-1]

    def updatenormpath(self, normpath, context):
        x0_pt, y0_pt = context.x_pt, context.y_pt
        for point_pt in self.points_pt:
            normpath.normsubpaths[-1].append(normline_pt(x0_pt, y0_pt, *point_pt))
            x0_pt, y0_pt = point_pt
        context.x_pt, context.y_pt = x0_pt, y0_pt

    def outputPS(self, file, writer):
        for point_pt in self.points_pt:
            file.write("%g %g lineto\n" % point_pt )


class multicurveto_pt(pathitem):

    """Perform multiple curvetos (coordinates in pts)"""

    __slots__ = "points_pt"

    def __init__(self, points_pt):
        self.points_pt = points_pt

    def __str__(self):
        result = []
        for point_pt in self.points_pt:
            result.append("(%g, %g, %g, %g, %g, %g)" % point_pt )
        return "multicurveto_pt([%s])" % (", ".join(result))

    def updatebbox(self, bbox, context):
        for point_pt in self.points_pt:
            bbox.includepoint_pt(*point_pt[0: 2])
            bbox.includepoint_pt(*point_pt[2: 4])
            bbox.includepoint_pt(*point_pt[4: 6])
        if self.points_pt:
            context.x_pt, context.y_pt = self.points_pt[-1][4:]

    def updatenormpath(self, normpath, context):
        x0_pt, y0_pt = context.x_pt, context.y_pt
        for point_pt in self.points_pt:
            normpath.normsubpaths[-1].append(normcurve_pt(x0_pt, y0_pt, *point_pt))
            x0_pt, y0_pt = point_pt[4:]
        context.x_pt, context.y_pt = x0_pt, y0_pt

    def outputPS(self, file, writer):
        for point_pt in self.points_pt:
            file.write("%g %g %g %g %g %g curveto\n" % point_pt)


################################################################################
# path: PS style path
################################################################################

class path:

    """PS style path"""

    __slots__ = "pathitems", "_normpath"

    def __init__(self, *pathitems):
        """construct a path from pathitems *args"""

        for apathitem in pathitems:
            assert isinstance(apathitem, pathitem), "only pathitem instances allowed"

        self.pathitems = list(pathitems)
        # normpath cache (when no epsilon is set)
        self._normpath = None

    def __add__(self, other):
        """create new path out of self and other"""
        return path(*(self.pathitems + other.path().pathitems))

    def __iadd__(self, other):
        """add other inplace

        If other is a normpath instance, it is converted to a path before
        being added.
        """
        self.pathitems += other.path().pathitems
        self._normpath = None
        return self

    def __getitem__(self, i):
        """return path item i"""
        return self.pathitems[i]

    def __len__(self):
        """return the number of path items"""
        return len(self.pathitems)

    def __str__(self):
        l = ", ".join(map(str, self.pathitems))
        return "path(%s)" % l

    def append(self, apathitem):
        """append a path item"""
        assert isinstance(apathitem, pathitem), "only pathitem instance allowed"
        self.pathitems.append(apathitem)
        self._normpath = None

    def arclen_pt(self):
        """return arc length in pts"""
        return self.normpath().arclen_pt()

    def arclen(self):
        """return arc length"""
        return self.normpath().arclen()

    def arclentoparam_pt(self, lengths_pt):
        """return the param(s) matching the given length(s)_pt in pts"""
        return self.normpath().arclentoparam_pt(lengths_pt)

    def arclentoparam(self, lengths):
        """return the param(s) matching the given length(s)"""
        return self.normpath().arclentoparam(lengths)

    def at_pt(self, params):
        """return coordinates of path in pts at param(s) or arc length(s) in pts"""
        return self.normpath().at_pt(params)

    def at(self, params):
        """return coordinates of path at param(s) or arc length(s)"""
        return self.normpath().at(params)

    def atbegin_pt(self):
        """return coordinates of the beginning of first subpath in path in pts"""
        return self.normpath().atbegin_pt()

    def atbegin(self):
        """return coordinates of the beginning of first subpath in path"""
        return self.normpath().atbegin()

    def atend_pt(self):
        """return coordinates of the end of last subpath in path in pts"""
        return self.normpath().atend_pt()

    def atend(self):
        """return coordinates of the end of last subpath in path"""
        return self.normpath().atend()

    def bbox(self):
        """return bbox of path"""
        if self.pathitems:
            bbox = self.pathitems[0].createbbox()
            context = self.pathitems[0].createcontext()
            for pathitem in self.pathitems[1:]:
                pathitem.updatebbox(bbox, context)
            return bbox
        else:
            return bboxmodule.empty()

    def begin(self):
        """return param corresponding of the beginning of the path"""
        return self.normpath().begin()

    def curveradius_pt(self, params):
        """return the curvature radius in pts at param(s) or arc length(s) in pts

        The curvature radius is the inverse of the curvature. When the
        curvature is 0, None is returned. Note that this radius can be negative
        or positive, depending on the sign of the curvature."""
        return self.normpath().curveradius_pt(params)

    def curveradius(self, params):
        """return the curvature radius at param(s) or arc length(s)

        The curvature radius is the inverse of the curvature. When the
        curvature is 0, None is returned. Note that this radius can be negative
        or positive, depending on the sign of the curvature."""
        return self.normpath().curveradius(params)

    def end(self):
        """return param corresponding of the end of the path"""
        return self.normpath().end()

    def extend(self, pathitems):
        """extend path by pathitems"""
        for apathitem in pathitems:
            assert isinstance(apathitem, pathitem), "only pathitem instance allowed"
        self.pathitems.extend(pathitems)
        self._normpath = None

    def intersect(self, other):
        """intersect self with other path

        Returns a tuple of lists consisting of the parameter values
        of the intersection points of the corresponding normpath.
        """
        return self.normpath().intersect(other)

    def join(self, other):
        """join other path/normpath inplace

        If other is a normpath instance, it is converted to a path before
        being joined.
        """
        self.pathitems = self.joined(other).path().pathitems
        self._normpath = None
        return self

    def joined(self, other):
        """return path consisting of self and other joined together"""
        return self.normpath().joined(other).path()

    # << operator also designates joining
    __lshift__ = joined

    def normpath(self, epsilon=_marker):
        """convert the path into a normpath"""
        # use cached value if existent and epsilon is _marker
        if self._normpath is not None and epsilon is _marker:
            return self._normpath
        if self.pathitems:
            if epsilon is _marker:
                normpath = self.pathitems[0].createnormpath()
            else:
                normpath = self.pathitems[0].createnormpath(epsilon)
            context = self.pathitems[0].createcontext()
            for pathitem in self.pathitems[1:]:
                pathitem.updatenormpath(normpath, context)
        else:
            if epsilon is _marker:
                normpath = normpath([])
            else:
                normpath = normpath(epsilon=epsilon)
        if epsilon is _marker:
            self._normpath = normpath
        return normpath

    def paramtoarclen_pt(self, params):
        """return arc lenght(s) in pts matching the given param(s)"""
        return self.normpath().paramtoarclen_pt(params)

    def paramtoarclen(self, params):
        """return arc lenght(s) matching the given param(s)"""
        return self.normpath().paramtoarclen(params)

    def path(self):
        """return corresponding path, i.e., self"""
        return self

    def reversed(self):
        """return reversed normpath"""
        # TODO: couldn't we try to return a path instead of converting it
        #       to a normpath (but this might not be worth the trouble)
        return self.normpath().reversed()

    def rotation_pt(self, params):
        """return rotation at param(s) or arc length(s) in pts"""
        return self.normpath().rotation(params)

    def rotation(self, params):
        """return rotation at param(s) or arc length(s)"""
        return self.normpath().rotation(params)

    def split_pt(self, params):
        """split normpath at param(s) or arc length(s) in pts and return list of normpaths"""
        return self.normpath().split(params)

    def split(self, params):
        """split normpath at param(s) or arc length(s) and return list of normpaths"""
        return self.normpath().split(params)

    def tangent_pt(self, params, length):
        """return tangent vector of path at param(s) or arc length(s) in pts

        If length in pts is not None, the tangent vector will be scaled to
        the desired length.
        """
        return self.normpath().tangent_pt(params, length)

    def tangent(self, params, length=1):
        """return tangent vector of path at param(s) or arc length(s)

        If length is not None, the tangent vector will be scaled to
        the desired length.
        """
        return self.normpath().tangent(params, length)

    def trafo_pt(self, params):
        """return transformation at param(s) or arc length(s) in pts"""
        return self.normpath().trafo(params)

    def trafo(self, params):
        """return transformation at param(s) or arc length(s)"""
        return self.normpath().trafo(params)

    def transformed(self, trafo):
        """return transformed path"""
        return self.normpath().transformed(trafo)

    def outputPS(self, file, writer):
        """write PS code to file"""
        for pitem in self.pathitems:
            pitem.outputPS(file, writer)

    def outputPDF(self, file, writer):
        """write PDF code to file"""
        # PDF only supports normsubpathitems; we need to use a normpath
        # with epsilon equals None to prevent failure for paths shorter
        # than epsilon
        self.normpath(epsilon=None).outputPDF(file, writer)


#
# some special kinds of path, again in two variants
#

class line_pt(path):

    """straight line from (x1_pt, y1_pt) to (x2_pt, y2_pt) in pts"""

    def __init__(self, x1_pt, y1_pt, x2_pt, y2_pt):
        path.__init__(self, moveto_pt(x1_pt, y1_pt), lineto_pt(x2_pt, y2_pt))


class curve_pt(path):

    """bezier curve with control points (x0_pt, y1_pt),..., (x3_pt, y3_pt) in pts"""

    def __init__(self, x0_pt, y0_pt, x1_pt, y1_pt, x2_pt, y2_pt, x3_pt, y3_pt):
        path.__init__(self,
                      moveto_pt(x0_pt, y0_pt),
                      curveto_pt(x1_pt, y1_pt, x2_pt, y2_pt, x3_pt, y3_pt))


class rect_pt(path):

    """rectangle at position (x_pt, y_pt) with width_pt and height_pt in pts"""

    def __init__(self, x_pt, y_pt, width_pt, height_pt):
        path.__init__(self, moveto_pt(x_pt, y_pt),
                            lineto_pt(x_pt+width_pt, y_pt),
                            lineto_pt(x_pt+width_pt, y_pt+height_pt),
                            lineto_pt(x_pt, y_pt+height_pt),
                            closepath())


class circle_pt(path):

    """circle with center (x_pt, y_pt) and radius_pt in pts"""

    def __init__(self, x_pt, y_pt, radius_pt, arcepsilon=0.1):
        path.__init__(self, moveto_pt(x_pt+radius_pt, y_pt),
                            arc_pt(x_pt, y_pt, radius_pt, arcepsilon, 360-arcepsilon),
                            closepath())


class ellipse_pt(path):

    """ellipse with center (x_pt, y_pt) in pts,
    the two axes (a_pt, b_pt) in pts,
    and the angle angle of the first axis"""

    def __init__(self, x_pt, y_pt, a_pt, b_pt, angle, **kwargs):
        t = trafo.scale(a_pt, b_pt, epsilon=None).rotated(angle).translated_pt(x_pt, y_pt)
        p = circle_pt(0, 0, 1, **kwargs).normpath(epsilon=None).transformed(t).path()
        path.__init__(self, *p.pathitems)


class line(line_pt):

    """straight line from (x1, y1) to (x2, y2)"""

    def __init__(self, x1, y1, x2, y2):
        line_pt.__init__(self, unit.topt(x1), unit.topt(y1),
                               unit.topt(x2), unit.topt(y2))


class curve(curve_pt):

    """bezier curve with control points (x0, y1),..., (x3, y3)"""

    def __init__(self, x0, y0, x1, y1, x2, y2, x3, y3):
        curve_pt.__init__(self, unit.topt(x0), unit.topt(y0),
                                unit.topt(x1), unit.topt(y1),
                                unit.topt(x2), unit.topt(y2),
                                unit.topt(x3), unit.topt(y3))


class rect(rect_pt):

    """rectangle at position (x,y) with width and height"""

    def __init__(self, x, y, width, height):
        rect_pt.__init__(self, unit.topt(x), unit.topt(y),
                               unit.topt(width), unit.topt(height))


class circle(circle_pt):

    """circle with center (x,y) and radius"""

    def __init__(self, x, y, radius, **kwargs):
        circle_pt.__init__(self, unit.topt(x), unit.topt(y), unit.topt(radius), **kwargs)


class ellipse(ellipse_pt):

    """ellipse with center (x, y), the two axes (a, b),
    and the angle angle of the first axis"""

    def __init__(self, x, y, a, b, angle, **kwargs):
        ellipse_pt.__init__(self, unit.topt(x), unit.topt(y), unit.topt(a), unit.topt(b), angle, **kwargs)
