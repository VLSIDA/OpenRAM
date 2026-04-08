# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2003-2006 Michael Schindler <m-schindler@users.sourceforge.net>
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
from math import pi, sin, cos, atan2, tan, hypot, acos, sqrt
import path, unit, mathutils, normpath
try:
    from math import radians, degrees
except ImportError:
    # fallback implementation for Python 2.1 and below
    def radians(x): return x*pi/180
    def degrees(x): return x*180/pi


#########################
##   helpers
#########################

class connector_pt(normpath.normpath):

    def omitends(self, box1, box2):
        """intersects a path with the boxes' paths"""

        # cut off the start of self
        # XXX how can decoration of this box1.path() be handled?
        sp = self.intersect(box1.path())[0]
        if sp:
            self.normsubpaths = self.split(sp[-1:])[1].normsubpaths

        # cut off the end of self
        sp = self.intersect(box2.path())[0]
        if sp:
            self.normsubpaths = self.split(sp[:1])[0].normsubpaths

    def shortenpath(self, dists):
        """shortens a path by the given distances"""

        # XXX later, this should be done by extended boxes instead of intersecting with circles
        # cut off the start of self
        center = self.atbegin_pt()
        cutpath = path.circle_pt(center[0], center[1], dists[0])
        try:
            cutpath = cutpath.normpath()
        except normpath.NormpathException:
            pass
        else:
            sp = self.intersect(cutpath)[0]
            self.normsubpaths = self.split(sp[-1:])[1].normsubpaths

        # cut off the end of self
        center = self.atend_pt()
        cutpath = path.circle_pt(center[0], center[1], dists[1])
        try:
            cutpath = cutpath.normpath()
        except normpath.NormpathException:
            pass
        else:
            sp = self.intersect(cutpath)[0]
            if sp:
                self.normsubpaths = self.split(sp[:1])[0].normsubpaths


################
## classes
################


class line_pt(connector_pt):

    def __init__(self, box1, box2, boxdists=[0,0]):

        self.box1 = box1
        self.box2 = box2

        connector_pt.__init__(self,
            [path.normsubpath([path.normline_pt(self.box1.center[0], self.box1.center[1],
                                                self.box2.center[0], self.box2.center[1])], closed=0)])

        self.omitends(box1, box2)
        self.shortenpath(boxdists)


class arc_pt(connector_pt):

    def __init__(self, box1, box2, relangle=45,
                 absbulge=None, relbulge=None, boxdists=[0,0]):

        # the deviation of arc from the straight line can be specified:
        # 1. By an angle between a straight line and the arc
        #    This angle is measured at the centers of the box.
        # 2. By the largest normal distance between line and arc: absbulge
        #    or, equivalently, by the bulge relative to the length of the
        #    straight line from center to center.
        # Only one can be used.

        self.box1 = box1
        self.box2 = box2

        tangent = (self.box2.center[0] - self.box1.center[0],
                   self.box2.center[1] - self.box1.center[1])
        distance = hypot(*tangent)
        tangent = tangent[0] / distance, tangent[1] / distance

        if relbulge is not None or absbulge is not None:
            # usage of bulge overrides the relangle parameter
            bulge = 0
            if absbulge is not None:
                bulge += absbulge
            if relbulge is not None:
                bulge += relbulge*distance
        else:
            # otherwise use relangle, which should be present
            bulge = 0.5 * distance * math.tan(0.5*radians(relangle))

        if abs(bulge) < normpath._epsilon:
            # fallback solution for too straight arcs
            connector_pt.__init__(self,
                [path.normsubpath([path.normline_pt(*(self.box1.center+self.box2.center))], closed=0)])
        else:
            radius = abs(0.5 * (bulge + 0.25 * distance**2 / bulge))
            centerdist = mathutils.sign(bulge) * (radius - abs(bulge))
            center = (0.5 * (self.box1.center[0] + self.box2.center[0]) + tangent[1]*centerdist,
                      0.5 * (self.box1.center[1] + self.box2.center[1]) - tangent[0]*centerdist)
            angle1 = atan2(self.box1.center[1] - center[1], self.box1.center[0] - center[0])
            angle2 = atan2(self.box2.center[1] - center[1], self.box2.center[0] - center[0])

            if bulge > 0:
                connectorpath = path.path(path.moveto_pt(*self.box1.center),
                                          path.arcn_pt(center[0], center[1], radius, degrees(angle1), degrees(angle2)))
                connector_pt.__init__(self, connectorpath.normpath().normsubpaths)
            else:
                connectorpath = path.path(path.moveto_pt(*self.box1.center),
                                          path.arc_pt(center[0], center[1], radius, degrees(angle1), degrees(angle2)))
                connector_pt.__init__(self, connectorpath.normpath().normsubpaths)

        self.omitends(box1, box2)
        self.shortenpath(boxdists)


class curve_pt(connector_pt):

    def __init__(self, box1, box2,
                 relangle1=45, relangle2=45,
                 absangle1=None, absangle2=None,
                 absbulge=0, relbulge=0.39, boxdists=[0,0]):

        # The deviation of the curve from a straight line can be specified:
        # A. By an angle at each center
        #    These angles are either absolute angles with origin at the positive x-axis
        #    or the relative angle with origin at the straight connection line
        # B. By the (expected) largest normal distance between line and arc: absbulge
        #    and/or by the (expected) bulge relative to the length of the
        #    straight line from center to center.
        # Here, we need both informations.
        #
        # a curve with relbulge=0.39 and relangle1,2=45 leads
        # approximately to the arc with angle=45

        self.box1 = box1
        self.box2 = box2

        rel = (self.box2.center[0] - self.box1.center[0],
               self.box2.center[1] - self.box1.center[1])
        distance = hypot(*rel)
        # absolute angle of the straight connection
        dangle = atan2(rel[1], rel[0])

        # calculate the armlength and absolute angles for the control points:
        # absolute and relative bulges are added
        bulge = abs(distance*relbulge + absbulge)

        if absangle1 is not None:
            angle1 = radians(absangle1)
        else:
            angle1 = dangle + radians(relangle1)
        if absangle2 is not None:
            angle2 = radians(absangle2)
        else:
            angle2 = dangle + radians(relangle2)

        # get the control points
        control1 = (cos(angle1), sin(angle1))
        control2 = (cos(angle2), sin(angle2))
        control1 = (self.box1.center[0] + control1[0] * bulge, self.box1.center[1] + control1[1] * bulge)
        control2 = (self.box2.center[0] - control2[0] * bulge, self.box2.center[1] - control2[1] * bulge)

        connector_pt.__init__(self,
               [path.normsubpath([path.normcurve_pt(*(self.box1.center +
                                                   control1 +
                                                   control2 + self.box2.center))], 0)])

        self.omitends(box1, box2)
        self.shortenpath(boxdists)


class twolines_pt(connector_pt):

    def __init__(self, box1, box2,
                 absangle1=None, absangle2=None,
                 relangle1=None, relangle2=None, relangleM=None,
                 length1=None, length2=None,
                 bezierradius=None, beziersoftness=1,
                 arcradius=None,
                 boxdists=[0,0]):

        # The connection with two lines can be done in the following ways:
        # 1. an angle at each box-center
        # 2. two armlengths (if they are long enough)
        # 3. angle and armlength at the same box
        # 4. angle and armlength at different boxes
        # 5. one armlength and the angle between the arms
        #
        # Angles at the box-centers can be relative or absolute
        # The angle in the middle is always relative
        # lengths are always absolute

        self.box1 = box1
        self.box2 = box2

        begin = self.box1.center
        end = self.box2.center
        rel = (self.box2.center[0] - self.box1.center[0],
               self.box2.center[1] - self.box1.center[1])
        distance = hypot(*rel)
        dangle = atan2(rel[1], rel[0])

        # find out what arguments are given:
        if relangle1 is not None: relangle1 = radians(relangle1)
        if relangle2 is not None: relangle2 = radians(relangle2)
        if relangleM is not None: relangleM = radians(relangleM)
        # absangle has priority over relangle:
        if absangle1 is not None: relangle1 = dangle - radians(absangle1)
        if absangle2 is not None: relangle2 = math.pi - dangle + radians(absangle2)

        # check integrity of arguments
        no_angles, no_lengths=0,0
        for anangle in (relangle1, relangle2, relangleM):
            if anangle is not None: no_angles += 1
        for alength in (length1, length2):
            if alength is not None: no_lengths += 1

        if no_angles + no_lengths != 2:
            raise NotImplementedError, "Please specify exactly two angles or lengths"

        # calculate necessary angles and armlengths
        # always length1 and relangle1

        # the case with two given angles
        # use the "sine-theorem" for calculating length1
        if no_angles == 2:
            if relangle1 is None: relangle1 = math.pi - relangle2 - relangleM
            elif relangle2 is None: relangle2 = math.pi - relangle1 - relangleM
            elif relangleM is None: relangleM = math.pi - relangle1 - relangle2
            length1 = distance * abs(sin(relangle2)/sin(relangleM))
            middle = self._middle_a(begin, dangle, length1, relangle1)
        # the case with two given lengths
        # uses the "cosine-theorem" for calculating length1
        elif no_lengths == 2:
            relangle1 = acos((distance**2 + length1**2 - length2**2) / (2.0*distance*length1))
            middle = self._middle_a(begin, dangle, length1, relangle1)
        # the case with one length and one angle
        else:
            if relangle1 is not None:
                if length1 is not None:
                    middle = self._middle_a(begin, dangle, length1, relangle1)
                elif length2 is not None:
                    length1 = self._missinglength(length2, distance, relangle1)
                    middle = self._middle_a(begin, dangle, length1, relangle1)
            elif relangle2 is not None:
                if length1 is not None:
                    length2 = self._missinglength(length1, distance, relangle2)
                    middle = self._middle_b(end, dangle, length2, relangle2)
                elif length2 is not None:
                    middle = self._middle_b(end, dangle, length2, relangle2)
            elif relangleM is not None:
                if length1 is not None:
                    length2 = self._missinglength(distance, length1, relangleM)
                    relangle1 = acos((distance**2 + length1**2 - length2**2) / (2.0*distance*length1))
                    middle = self._middle_a(begin, dangle, length1, relangle1)
                elif length2 is not None:
                    length1 = self._missinglength(distance, length2, relangleM)
                    relangle1 = acos((distance**2 + length1**2 - length2**2) / (2.0*distance*length1))
                    middle = self._middle_a(begin, dangle, length1, relangle1)
            else:
                raise NotImplementedError, "I found a strange combination of arguments"

        connectorpath = path.path(path.moveto_pt(*self.box1.center),
                                  path.lineto_pt(*middle),
                                  path.lineto_pt(*self.box2.center))
        connector_pt.__init__(self, connectorpath.normpath().normsubpaths)

        self.omitends(box1, box2)
        self.shortenpath(boxdists)

    def _middle_a(self, begin, dangle, length1, angle1):
        a = dangle - angle1
        dir = cos(a), sin(a)
        return begin[0] + length1*dir[0], begin[1] + length1*dir[1]

    def _middle_b(self, end, dangle, length2, angle2):
        # a = -math.pi + dangle + angle2
        return self._middle_a(end, -math.pi+dangle, length2, -angle2)

    def _missinglength(self, lenA, lenB, angleA):
        # calculate lenC, where side A and angleA are opposite
        tmp1 = lenB * cos(angleA)
        tmp2 = sqrt(tmp1**2 - lenB**2 + lenA**2)
        if tmp1 > tmp2: return tmp1 - tmp2
        return tmp1 + tmp2



class line(line_pt):

    """a line is the straight connector between the centers of two boxes"""

    def __init__(self, box1, box2, boxdists=(0,0)):
        line_pt.__init__(self, box1, box2, boxdists=map(unit.topt, boxdists))


class curve(curve_pt):

    """a curve is the curved connector between the centers of two boxes.
    The constructor needs both angle and bulge"""


    def __init__(self, box1, box2,
                 relangle1=45, relangle2=45,
                 absangle1=None, absangle2=None,
                 absbulge=0, relbulge=0.39,
                 boxdists=[0,0]):
        curve_pt.__init__(self, box1, box2,
                          relangle1=relangle1, relangle2=relangle2,
                          absangle1=absangle1, absangle2=absangle2,
                          absbulge=unit.topt(absbulge), relbulge=relbulge,
                          boxdists=map(unit.topt, boxdists))

class arc(arc_pt):

    """an arc is a round connector between the centers of two boxes.
    The constructor gets
         either an angle in (-pi,pi)
         or a bulge parameter in (-distance, distance)
           (relbulge and absbulge are added)"""

    def __init__(self, box1, box2, relangle=45,
                 absbulge=None, relbulge=None, boxdists=[0,0]):
        if absbulge is not None:
            absbulge = unit.topt(absbulge)
        arc_pt.__init__(self, box1, box2,
                        relangle=relangle,
                        absbulge=absbulge, relbulge=relbulge,
                        boxdists=map(unit.topt, boxdists))


class twolines(twolines_pt):

    """a twolines is a connector consisting of two straight lines.
    The construcor takes a combination of angles and lengths:
      either two angles (relative or absolute)
      or two lenghts
      or one length and one angle"""

    def __init__(self, box1, box2,
                 absangle1=None, absangle2=None,
                 relangle1=None, relangle2=None, relangleM=None,
                 length1=None, length2=None,
                 bezierradius=None, beziersoftness=1,
                 arcradius=None,
                 boxdists=[0,0]):
        if length1 is not None:
            length1 = unit.topt(length1)
        if length2 is not None:
            length2 = unit.topt(length2)
        if bezierradius is not None:
            bezierradius = unit.topt(bezierradius)
        if arcradius is not None:
            arcradius = unit.topt(arcradius)
        twolines_pt.__init__(self, box1, box2,
                             absangle1=absangle1, absangle2=absangle2,
                             relangle1=relangle1, relangle2=relangle2,
                             relangleM=relangleM,
                             length1=length1, length2=length2,
                             bezierradius=bezierradius, beziersoftness=1,
                             arcradius=arcradius,
                             boxdists=map(unit.topt, boxdists))



