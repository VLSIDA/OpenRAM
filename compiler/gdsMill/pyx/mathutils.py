# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2005-2006 Michael Schindler <m-schindler@users.sourceforge.net>
# Copyright (C) 2006 André Wobst <wobsta@users.sourceforge.net>
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

import math, types

# try:
#     import Numeric, LinearAlgebra
#     _has_numeric = 1
# except:
#     _has_numeric = 0


def sign(x):
    """sign of x, i.e. +1 or -1; returns 1 for x == 0"""
    if x >= 0:
        return 1
    return -1


def asinh(x):
    """Return the arc hyperbolic sine of x."""
    return math.log(x+math.sqrt(x*x+1))


def acosh(x):
    """Return the arc hyperbolic cosine of x."""
    return math.log(x+math.sqrt(x*x-1))


def _realroots_quadratic(a1, a0):
    """gives the real roots of x**2 + a1 * x + a0 = 0"""
    D = a1*a1 - 4*a0
    if D < 0:
        return []
    SD = math.sqrt(D)
    return [0.5 * (-a1 + SD), 0.5 * (-a1 - SD)]


def _realroots_cubic(a2, a1, a0):
    """gives the real roots of x**3 + a2 * x**2 + a1 * x + a0 = 0"""
    # see http://mathworld.wolfram.com/CubicFormula.html for details

    Q = (3*a1 - a2*a2) / 9.0
    R = (9*a2*a1 - 27*a0 - 2*a2*a2*a2) / 54.0
    D = Q*Q*Q + R*R

    if D > 0:         # one real and two complex roots
        SD = math.sqrt(D)
        if R + SD >= 0:
            S = (R + SD)**(1/3.0)
        else:
            S = -(-R - SD)**(1/3.0)
        if R - SD >= 0:
            T = (R - SD)**(1/3.0)
        else:
            T = -(SD - R)**(1/3.0)
        return [S + T - a2/3.0]
    elif D == 0:
        if Q == 0:    # one real root (R==0)
            return [-a2/3.0]
        else:         # two real roots (R>0, Q<0)
            S = -math.sqrt(-Q)
            return [2*S - a2/3.0, -S - a2/3.0]
    else:             # three real roots (Q<0)
        SQ = math.sqrt(-Q)
        arg = R / (SQ**3)
        if arg >= 1:
            theta = 0
        elif arg <= -1:
            theta = math.pi
        else:
            theta = math.acos(R/(SQ**3))
        return [2 * SQ * math.cos((theta + 2*2*i*math.pi)/3.0) - a2/3.0 for i in range(3)]


def _realroots_quartic(a3, a2, a1, a0):
    """gives the real roots of x**4 + a3 * x**3 + a2 * x**2 + a1 * x + a0 = 0"""
    # see http://mathworld.wolfram.com/QuarticEquation.html for details
    ys = _realroots_cubic(-a2, a1*a3 - 4*a0, 4*a0*a2 - a1*a1 - a0*a3*a3)
    ys = [y for y in ys if a3*a3-4*a2+4*y >= 0 and  y*y-4*a0 >= 0]
    if not ys:
        return []
    y1 = min(ys)
    if a3*y1-2*a1 < 0:
        return (_realroots_quadratic(0.5*(a3+math.sqrt(a3*a3-4*a2+4*y1)), 0.5*(y1-math.sqrt(y1*y1-4*a0))) +
                _realroots_quadratic(0.5*(a3-math.sqrt(a3*a3-4*a2+4*y1)), 0.5*(y1+math.sqrt(y1*y1-4*a0))))
    else:
        return (_realroots_quadratic(0.5*(a3+math.sqrt(a3*a3-4*a2+4*y1)), 0.5*(y1+math.sqrt(y1*y1-4*a0))) +
                _realroots_quadratic(0.5*(a3-math.sqrt(a3*a3-4*a2+4*y1)), 0.5*(y1-math.sqrt(y1*y1-4*a0))))


def realpolyroots(*cs):
    """returns the roots of a polynom with given coefficients

    polynomial with coefficients given in cs:
      0 = \sum_i  cs[i] * x^(len(cs)-i-1)
    """
    if not cs:
        return [0]
    try:
        f = 1.0/cs[0]
        cs = [f*c for c in cs[1:]]
    except ArithmeticError:
        return realpolyroots(*cs[1:])
    else:
        n = len(cs)
        if n == 0:
            return []
        elif n == 1:
            return [-cs[0]]
        elif n == 2:
            return _realroots_quadratic(*cs)
        elif n == 3:
            return _realroots_cubic(*cs)
        elif n == 4:
            return _realroots_quartic(*cs)
        else:
            raise RuntimeError("realpolyroots solver currently limited to polynoms up to the power of 4")


# def realpolyroots_eigenvalue(*cs):
#     # as realpolyroots but using an equivalent eigenvalue problem
#     # (this code is currently used for functional tests only)
#     if not _has_numeric:
#         raise RuntimeError("realpolyroots_eigenvalue depends on Numeric")
#     if not cs:
#         return [0]
#     try:
#         f = 1.0/cs[0]
#         cs = [f*c for c in cs[1:]]
#     except ArithmeticError:
#         return realpolyroots_eigenvalue(*cs[1:])
#     else:
#         if not cs:
#             return []
#         n = len(cs)
#         a = Numeric.zeros((n, n), Numeric.Float)
#         for i in range(n-1):
#             a[i+1][i] = 1
#         for i in range(n):
#             a[0][i] = -cs[i]
#         rs = []
#         for r in LinearAlgebra.eigenvalues(a):
#             if type(r) == types.ComplexType:
#                 if not r.imag:
#                     rs.append(r.real)
#             else:
#                 rs.append(r)
#         return rs
#
