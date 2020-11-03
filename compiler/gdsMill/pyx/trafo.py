# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2002-2006 Jörg Lehmann <joergl@users.sourceforge.net>
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

import math
import attr, canvas, deformer, unit
import bbox as bboxmodule

# global epsilon (used to judge whether a matrix is singular)
_epsilon = (1e-5)**2

def set(epsilon=None):
    global _epsilon
    if epsilon is not None:
        _epsilon = epsilon


# some helper routines

def _rmatrix(angle):
    phi = math.pi*angle/180.0

    return  ((math.cos(phi), -math.sin(phi)),
             (math.sin(phi),  math.cos(phi)))

def _rvector(angle, x, y):
    phi = math.pi*angle/180.0

    return  ((1-math.cos(phi))*x + math.sin(phi)    *y,
              -math.sin(phi)   *x + (1-math.cos(phi))*y)


def _mmatrix(angle):
    phi = math.pi*angle/180.0

    return ( (math.cos(phi)*math.cos(phi)-math.sin(phi)*math.sin(phi),
              -2*math.sin(phi)*math.cos(phi)                ),
             (-2*math.sin(phi)*math.cos(phi),
              math.sin(phi)*math.sin(phi)-math.cos(phi)*math.cos(phi) ) )

class _marker: pass

# Exception

class TrafoException(Exception):
    pass

# trafo: affine transformations

class trafo_pt(canvas.canvasitem, deformer.deformer):

    """affine transformation (coordinates in constructor in pts)

    Note that though the coordinates in the constructor are in
    pts (which is useful for internal purposes), all other
    methods only accept units in the standard user notation.

    """

    def __init__(self, matrix=((1, 0), (0, 1)), vector=(0, 0), epsilon=_marker):
        """Return trafo with given transformation matrix and vector. If epsilon
        is passed it is used instead of the global epsilon defined in the module to
        check whether the matrix is singular or not. Use epsilon=None to turn of this
        checking.
        """
        if epsilon is _marker:
            epsilon = _epsilon
        self.epsilon = epsilon
        if epsilon is not None and abs(matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]) < epsilon:
            raise TrafoException("transformation matrix must not be singular")
        else:
            self.matrix = matrix
        self.vector = vector

    def __mul__(self, other):
        if isinstance(other, trafo_pt):
            if self.epsilon is None or other.epsilon is None:
                epsilon = None
            elif self.epsilon <= other.epsilon:
                epsilon = self.epsilon
            else:
                epsilon = other.epsilon
            matrix = ( ( self.matrix[0][0]*other.matrix[0][0] +
                         self.matrix[0][1]*other.matrix[1][0],
                         self.matrix[0][0]*other.matrix[0][1] +
                         self.matrix[0][1]*other.matrix[1][1] ),
                       ( self.matrix[1][0]*other.matrix[0][0] +
                         self.matrix[1][1]*other.matrix[1][0],
                         self.matrix[1][0]*other.matrix[0][1] +
                         self.matrix[1][1]*other.matrix[1][1] )
                     )

            vector = ( self.matrix[0][0]*other.vector[0] +
                       self.matrix[0][1]*other.vector[1] +
                       self.vector[0],
                       self.matrix[1][0]*other.vector[0] +
                       self.matrix[1][1]*other.vector[1] +
                       self.vector[1] )

            return trafo_pt(matrix=matrix, vector=vector, epsilon=epsilon)
        else:
            raise NotImplementedError("can only multiply two transformations")

    def __str__(self):
        return "[%f %f %f %f %f %f]" % \
               ( self.matrix[0][0], self.matrix[1][0],
                 self.matrix[0][1], self.matrix[1][1],
                 self.vector[0], self.vector[1] )

    def processPS(self, file, writer, context, registry, bbox):
        file.write("[%f %f %f %f %f %f] concat\n" % \
                    ( self.matrix[0][0], self.matrix[1][0],
                      self.matrix[0][1], self.matrix[1][1],
                      self.vector[0], self.vector[1] ) )

    def processPDF(self, file, writer, context, registry, bbox):
        file.write("%f %f %f %f %f %f cm\n" % \
                    ( self.matrix[0][0], self.matrix[1][0],
                      self.matrix[0][1], self.matrix[1][1],
                      self.vector[0], self.vector[1] ) )

    def bbox(self):
        return bboxmodule.empty()

    def apply_pt(self, x_pt, y_pt):
        """apply transformation to point (x_pt, y_pt) in pts"""
        return ( self.matrix[0][0]*x_pt + self.matrix[0][1]*y_pt + self.vector[0],
                 self.matrix[1][0]*x_pt + self.matrix[1][1]*y_pt + self.vector[1] )

    def apply(self, x, y):
        # for the transformation we have to convert to points
        tx, ty = self.apply_pt(unit.topt(x), unit.topt(y))
        return tx * unit.t_pt, ty * unit.t_pt

    def deform(self, path):
        return path.transformed(self)

    def inverse(self):
        det = 1.0*(self.matrix[0][0]*self.matrix[1][1] - self.matrix[0][1]*self.matrix[1][0])
        matrix = ( ( self.matrix[1][1]/det, -self.matrix[0][1]/det),
                   (-self.matrix[1][0]/det,  self.matrix[0][0]/det) )
        return ( trafo_pt(matrix=matrix, epsilon=self.epsilon) *
                 trafo_pt(vector=(-self.vector[0], -self.vector[1]), epsilon=self.epsilon) )

    def mirrored(self, angle):
        return mirror(angle, epsilon=self.epsilon) * self

    def rotated_pt(self, angle, x=None, y=None):
        return rotate_pt(angle, x, y, epsilon=self.epsilon) * self

    def rotated(self, angle, x=None, y=None):
        return rotate(angle, x, y, epsilon=self.epsilon) * self

    def scaled_pt(self, sx, sy=None, x=None, y=None):
        return scale_pt(sx, sy, x, y, epsilon=self.epsilon) * self

    def scaled(self, sx, sy=None, x=None, y=None):
        return scale(sx, sy, x, y, epsilon=self.epsilon) * self

    def slanted_pt(self, a, angle=0, x=None, y=None):
        return slant_pt(a, angle, x, y, epsilon=self.epsilon) * self

    def slanted(self, a, angle=0, x=None, y=None):
        return slant(a, angle, x, y, epsilon=self.epsilon) * self

    def translated_pt(self, x, y):
        return translate_pt(x, y, epsilon=self.epsilon) * self

    def translated(self, x, y):
        return translate(x, y, epsilon=self.epsilon) * self


class trafo(trafo_pt):

    """affine transformation"""

    def __init__(self, matrix=((1,0), (0,1)), vector=(0, 0), epsilon=_marker):
        trafo_pt.__init__(self,
                          matrix, (unit.topt(vector[0]), unit.topt(vector[1])),
                          epsilon=epsilon)

#
# some standard transformations
#

class mirror(trafo):
    def __init__(self, angle=0, epsilon=_marker):
        trafo.__init__(self, matrix=_mmatrix(angle), epsilon=epsilon)


class rotate_pt(trafo_pt):
    def __init__(self, angle, x=None, y=None, epsilon=_marker):
        vector = 0, 0
        if x is not None or y is not None:
            if x is None or y is None:
                raise TrafoException("either specify both x and y or none of them")
            vector=_rvector(angle, x, y)

        trafo_pt.__init__(self, matrix=_rmatrix(angle), vector=vector, epsilon=epsilon)


class rotate(trafo_pt):
    def __init__(self, angle, x=None, y=None, epsilon=_marker):
        vector = 0, 0
        if x is not None or y is not None:
            if x is None or y is None:
                raise TrafoException("either specify both x and y or none of them")
            vector=_rvector(angle, unit.topt(x), unit.topt(y))

        trafo_pt.__init__(self, matrix=_rmatrix(angle), vector=vector, epsilon=epsilon)


class scale_pt(trafo_pt):
    def __init__(self, sx, sy=None, x=None, y=None, epsilon=_marker):
        if sy is None:
            sy = sx
        vector = 0, 0
        if x is not None or y is not None:
            if x is None or y is None:
                raise TrafoException("either specify both x and y or none of them")
            vector = (1-sx)*x, (1-sy)*y
        trafo_pt.__init__(self, matrix=((sx, 0), (0, sy)), vector=vector, epsilon=epsilon)


class scale(trafo):
    def __init__(self, sx, sy=None, x=None, y=None, epsilon=_marker):
        if sy is None:
            sy = sx
        vector = 0, 0
        if x is not None or y is not None:
            if x is None or y is None:
                raise TrafoException("either specify both x and y or none of them")
            vector = (1-sx)*x, (1-sy)*y
        trafo.__init__(self, matrix=((sx, 0), (0, sy)), vector=vector, epsilon=epsilon)


class slant_pt(trafo_pt):
    def __init__(self, a, angle=0, x=None, y=None, epsilon=_marker):
        t = ( rotate_pt(-angle, x, y, epsilon=epsilon) *
              trafo(matrix=((1, a), (0, 1)), epsilon=epsilon) *
              rotate_pt(angle, x, y, epsilon=epsilon) )
        trafo_pt.__init__(self, t.matrix, t.vector, epsilon=epsilon)


class slant(trafo):
    def __init__(self, a, angle=0, x=None, y=None, epsilon=_marker):
        t = ( rotate(-angle, x, y, epsilon=epsilon) *
              trafo(matrix=((1, a), (0, 1)), epsilon=epsilon) *
              rotate(angle, x, y, epsilon=epsilon) )
        trafo.__init__(self, t.matrix, t.vector, epsilon=epsilon)


class translate_pt(trafo_pt):
    def __init__(self, x, y, epsilon=_marker):
        trafo_pt.__init__(self, vector=(x, y), epsilon=epsilon)


class translate(trafo):
    def __init__(self, x, y, epsilon=_marker):
        trafo.__init__(self, vector=(x, y), epsilon=epsilon)
