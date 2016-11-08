# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2002-2004 Jörg Lehmann <joergl@users.sourceforge.net>
# Copyright (C) 2003-2004 Michael Schindler <m-schindler@users.sourceforge.net>
# Copyright (C) 2002-2004 André Wobst <wobsta@users.sourceforge.net>
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


import types, math
import bbox, path, unit, trafo

class _marker: pass

class BoxCrossError(Exception): pass

class polygon_pt:

    def __init__(self, corners=None, center=None):
        self.corners = corners
        self.center = center
        if self.center is None:
            self._ensurecenter()

    def _ensurecenter(self):
        if self.center is None:
            self.center = 0, 0
            for corn in self.corners:
                self.center = self.center[0] + corn[0], self.center[1] + corn[1]
            self.center = self.center[0]/len(self.corners), self.center[1]/len(self.corners)

    def path(self, centerradius=None, bezierradius=None, beziersoftness=None):
        pathitems = []
        if centerradius is not None and self.center is not None:
            r = unit.topt(centerradius)
            pathitems.append(path.arc_pt(self.center[0], self.center[1], r, 0, 360))
            pathitems.append(path.closepath())
        if bezierradius is not None or beziersoftness is not None:
            raise ValueError("smooth functionality removed; apply smooth deformer on path")
        pathitems.append(path.moveto_pt(self.corners[0][0], self.corners[0][1]))
        for x, y in self.corners[1:]:
            pathitems.append(path.lineto_pt(x, y))
        pathitems.append(path.closepath())
        return path.path(*pathitems)

    def transform(self, *trafos):
        for trafo in trafos:
            if self.center is not None:
                self.center = trafo.apply_pt(*self.center)
            self.corners = [trafo.apply_pt(*point) for point in self.corners]

    def reltransform(self, *trafos):
        if self.center is not None:
            trafos = ([trafo.translate_pt(-self.center[0], -self.center[1])] +
                      list(trafos) +
                      [trafo.translate_pt(self.center[0], self.center[1])])
        self.transform(*trafos)

    def successivepointnumbers(self):
        return [i and (i - 1, i) or (len(self.corners) - 1, 0) for i in range(len(self.corners))]

    def successivepoints(self):
        return [(self.corners[i], self.corners[j]) for i, j in self.successivepointnumbers()]

    def circlealignlinevector_pt(self, a, dx, dy, ex, ey, fx, fy, epsilon=1e-10):
        cx, cy = self.center
        gx, gy = ex - fx, ey - fy # direction vector
        if gx*gx + gy*gy < epsilon: # zero line length
            return None             # no solution -> return None
        rsplit = (dx*gx + dy*gy) * 1.0 / (gx*gx + gy*gy)
        bx, by = dx - gx * rsplit, dy - gy * rsplit
        if bx*bx + by*by < epsilon: # zero projection
            return None             # no solution -> return None
        if bx*gy - by*gx < 0: # half space
            return None       # no solution -> return None
        sfactor = math.sqrt((dx*dx + dy*dy) / (bx*bx + by*by))
        bx, by = a * bx * sfactor, a * by * sfactor
        alpha = ((bx+cx-ex)*dy - (by+cy-ey)*dx) * 1.0 / (gy*dx - gx*dy)
        if alpha > 0 - epsilon and alpha < 1 + epsilon:
                beta = ((ex-bx-cx)*gy - (ey-by-cy)*gx) * 1.0 / (gx*dy - gy*dx)
                return beta*dx, beta*dy # valid solution -> return align tuple
        # crossing point at the line, but outside a valid range
        if alpha < 0:
            return 0 # crossing point outside e
        return 1 # crossing point outside f

    def linealignlinevector_pt(self, a, dx, dy, ex, ey, fx, fy, epsilon=1e-10):
        cx, cy = self.center
        gx, gy = ex - fx, ey - fy # direction vector
        if gx*gx + gy*gy < epsilon: # zero line length
            return None             # no solution -> return None
        if gy*dx - gx*dy < -epsilon: # half space
            return None              # no solution -> return None
        if dx*gx + dy*gy > epsilon or dx*gx + dy*gy < -epsilon:
            if dx*gx + dy*gy < 0: # angle bigger 90 degree
                return 0 # use point e
            return 1 # use point f
        # a and g are othorgonal
        alpha = ((a*dx+cx-ex)*dy - (a*dy+cy-ey)*dx) * 1.0 / (gy*dx - gx*dy)
        if alpha > 0 - epsilon and alpha < 1 + epsilon:
            beta = ((ex-a*dx-cx)*gy - (ey-a*dy-cy)*gx) * 1.0 / (gx*dy - gy*dx)
            return beta*dx, beta*dy # valid solution -> return align tuple
        # crossing point at the line, but outside a valid range
        if alpha < 0:
            return 0 # crossing point outside e
        return 1 # crossing point outside f

    def circlealignpointvector_pt(self, a, dx, dy, px, py, epsilon=1e-10):
        if a*a < epsilon:
            return None
        cx, cy = self.center
        p = 2 * ((px-cx)*dx + (py-cy)*dy)
        q = ((px-cx)*(px-cx) + (py-cy)*(py-cy) - a*a)
        if p*p/4 - q < 0:
            return None
        if a > 0:
            alpha = - p / 2 + math.sqrt(p*p/4 - q)
        else:
            alpha = - p / 2 - math.sqrt(p*p/4 - q)
        return alpha*dx, alpha*dy

    def linealignpointvector_pt(self, a, dx, dy, px, py):
        cx, cy = self.center
        beta = (a*dx+cx-px)*dy - (a*dy+cy-py)*dx
        return a*dx - beta*dy - px + cx, a*dy + beta*dx - py + cy

    def alignvector_pt(self, a, dx, dy, alignlinevector, alignpointvector):
        n = math.hypot(dx, dy)
        dx, dy = dx / n, dy / n
        linevectors = map(lambda (p1, p2), self=self, a=a, dx=dx, dy=dy, alignlinevector=alignlinevector:
                                alignlinevector(a, dx, dy, *(p1 + p2)), self.successivepoints())
        for linevector in linevectors:
            if type(linevector) is types.TupleType:
                return linevector
        for i, j in self.successivepointnumbers():
            l1, l2 = linevectors[i], linevectors[j]
            if (l1 is not None or l2 is not None) and (l1 == 1 or l1 is None) and (l2 == 0 or l2 is None):
                return alignpointvector(a, dx, dy, *self.successivepoints()[j][0])
        return a*dx, a*dy

    def circlealignvector_pt(self, a, dx, dy):
        return self.alignvector_pt(a, dx, dy, self.circlealignlinevector_pt, self.circlealignpointvector_pt)

    def linealignvector_pt(self, a, dx, dy):
        return self.alignvector_pt(a, dx, dy, self.linealignlinevector_pt, self.linealignpointvector_pt)

    def circlealignvector(self, a, dx, dy):
        ndx, ndy = self.circlealignvector_pt(unit.topt(a), dx, dy)
        return ndx * unit.t_pt, ndy * unit.t_pt

    def linealignvector(self, a, dx, dy):
        ndx, ndy = self.linealignvector_pt(unit.topt(a), dx, dy)
        return ndx * unit.t_pt, ndy * unit.t_pt

    def circlealign_pt(self, *args):
        self.transform(trafo.translate_pt(*self.circlealignvector_pt(*args)))
        return self

    def linealign_pt(self, *args):
        self.transform(trafo.translate_pt(*self.linealignvector_pt(*args)))
        return self

    def circlealign(self, *args):
        self.transform(trafo.translate(*self.circlealignvector(*args)))
        return self

    def linealign(self, *args):
        self.transform(trafo.translate(*self.linealignvector(*args)))
        return self

    def extent_pt(self, dx, dy):
        n = math.hypot(dx, dy)
        dx, dy = dx / n, dy / n
        oldcenter = self.center
        if self.center is None:
            self.center = 0, 0
        x1, y1 = self.linealignvector_pt(0, dx, dy)
        x2, y2 = self.linealignvector_pt(0, -dx, -dy)
        self.center = oldcenter
        return (x1-x2)*dx + (y1-y2)*dy

    def extent(self, dx, dy):
        return self.extent_pt(dx, dy) * unit.t_pt

    def pointdistance_pt(self, x, y):
        result = None
        for p1, p2 in self.successivepoints():
            gx, gy = p2[0] - p1[0], p2[1] - p1[1]
            if gx * gx + gy * gy < 1e-10:
                dx, dy = p1[0] - x, p1[1] - y
            else:
                a = (gx * (x - p1[0]) + gy * (y - p1[1])) / (gx * gx + gy * gy)
                if a < 0:
                    dx, dy = p1[0] - x, p1[1] - y
                elif a > 1:
                    dx, dy = p2[0] - x, p2[1] - y
                else:
                    dx, dy = x - p1[0] - a * gx, y - p1[1] - a * gy
            new = math.hypot(dx, dy)
            if result is None or new < result:
                result = new
        return result

    def pointdistance(self, x, y):
        return self.pointdistance_pt(unit.topt(x), unit.topt(y)) * unit.t_pt

    def boxdistance_pt(self, other, epsilon=1e-10):
        # XXX: boxes crossing and distance calculation is O(N^2)
        for p1, p2 in self.successivepoints():
            for p3, p4 in other.successivepoints():
                a = (p4[1] - p3[1]) * (p3[0] - p1[0]) - (p4[0] - p3[0]) * (p3[1] - p1[1])
                b = (p2[1] - p1[1]) * (p3[0] - p1[0]) - (p2[0] - p1[0]) * (p3[1] - p1[1])
                c = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
                if (abs(c) > 1e-10 and
                    a / c > -epsilon and a / c < 1 + epsilon and
                    b / c > -epsilon and b / c < 1 + epsilon):
                    raise BoxCrossError
        result = None
        for x, y in other.corners:
            new = self.pointdistance_pt(x, y)
            if result is None or new < result:
                result = new
        for x, y in self.corners:
            new = other.pointdistance_pt(x, y)
            if result is None or new < result:
                result = new
        return result

    def boxdistance(self, other):
        return self.boxdistance_pt(other) * unit.t_pt

    def bbox(self):
        return bbox.bbox_pt(min([x[0] for x in self.corners]),
                          min([x[1] for x in self.corners]),
                          max([x[0] for x in self.corners]),
                          max([x[1] for x in self.corners]))


def genericalignequal_pt(method, polygons, a, dx, dy):
    vec = None
    for p in polygons:
        v = method(p, a, dx, dy)
        if vec is None or vec[0] * dx + vec[1] * dy < v[0] * dx + v[1] * dy:
            vec = v
    for p in polygons:
        p.transform(trafo.translate_pt(*vec))


def circlealignequal_pt(polygons, *args):
    genericalignequal_pt(polygon_pt.circlealignvector_pt, polygons, *args)

def linealignequal_pt(polygons, *args):
    genericalignequal_pt(polygon_pt.linealignvector_pt, polygons, *args)

def circlealignequal(polygons, a, *args):
    circlealignequal_pt(polygons, unit.topt(a), *args)

def linealignequal(polygons, a, *args):
    linealignequal_pt(polygons, unit.topt(a), *args)


def tile_pt(polygons, a, dx, dy):
    maxextent = polygons[0].extent_pt(dx, dy)
    for p in polygons[1:]:
        extent = p.extent_pt(dx, dy)
        if extent > maxextent:
            maxextent = extent
    delta = maxextent + a
    d = 0
    for p in polygons:
        p.transform(trafo.translate_pt(d*dx, d*dy))
        d += delta
    return delta


def tile(polygons, a, dx, dy):
    return tile_pt(polygons, unit.topt(a), dx, dy) * unit.t_pt


class polygon(polygon_pt):

    def __init__(self, corners=None, center=None, **args):
        corners = [[unit.topt(x) for x in corner] for corner in corners]
        if center is not None:
            center = unit.topt(center[0]), unit.topt(center[1])
        polygon_pt.__init__(self, corners=corners, center=center, **args)


class rect_pt(polygon_pt):

    def __init__(self, x, y, width, height, relcenter=(0, 0), abscenter=(0, 0),
                       corners=_marker, center=_marker, **args):
        if corners != _marker or center != _marker:
            raise ValueError
        polygon_pt.__init__(self, corners=((x, y),
                                         (x + width, y),
                                         (x + width, y + height),
                                         (x, y + height)),
                                center=(x + relcenter[0] * width + abscenter[0],
                                        y + relcenter[1] * height + abscenter[1]),
                                **args)


class rect(rect_pt):

    def __init__(self, x, y, width, height, relcenter=(0, 0), abscenter=(0, 0), **args):
        rect_pt.__init__(self, unit.topt(x), unit.topt(y), unit.topt(width), unit.topt(height),
                               relcenter=relcenter,
                               abscenter=(unit.topt(abscenter[0]), unit.topt(abscenter[1])), **args)

