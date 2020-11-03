# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2002-2004 Jörg Lehmann <joergl@users.sourceforge.net>
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

import types

scale = { 't':1, 'u':1, 'v':1, 'w':1, 'x':1 }

_default_unit = "cm"

_m = {
      'm' :   1,
      'cm':   0.01,
      'mm':   0.001,
      'inch': 0.01*2.54,
      'pt':   0.01*2.54/72,
    }

def set(uscale=None, vscale=None, wscale=None, xscale=None, defaultunit=None):
    if uscale is not None:
        scale['u'] = uscale
    if vscale is not None:
        scale['v'] = vscale
    if wscale is not None:
        scale['w'] = wscale
    if xscale is not None:
        scale['x'] = xscale
    if defaultunit is not None:
        global _default_unit
        _default_unit = defaultunit


def _convert_to(l, dest_unit="m"):
    if type(l) in (types.IntType, types.LongType, types.FloatType):
        return l * _m[_default_unit] * scale['u'] / _m[dest_unit]
    elif not isinstance(l, length):
        l = length(l)       # convert to length instance if necessary

    return (l.t + l.u*scale['u'] + l.v*scale['v'] + l.w*scale['w'] + l.x*scale['x']) / _m[dest_unit]

def tom(l):
    return _convert_to(l, "m")

def tocm(l):
    return _convert_to(l, "cm")

def tomm(l):
    return _convert_to(l, "mm")

def toinch(l):
    return _convert_to(l, "inch")

def topt(l):
    return _convert_to(l, "pt")

################################################################################
# class for generic length
################################################################################

class length:
    """ PyX lengths

    PyX lengths are composed of five components (t=true, u=user, v=visual,
    w=width, and x=TeX) which can be scaled separately (except for the true
    component, which is always unscaled). Lengths can be constructed in units
    of "pt", "mm", "cm", "m" and "inch". When no unit is given, a module
    default is used, which can be changed with the help of the module level function
    set().
    """

    def __init__(self, f=0, type="u", unit=None):
        """ create a length instance of the given type with a length f
        in the given unit. If unit is not set, the currently set default unit is used.
        """
        self.t = self.u = self.v = self.w = self.x = 0
        l = float(f) * _m[unit or _default_unit]
        if type == "t":
            self.t = l
        elif type == "u":
            self.u = l
        elif type == "v":
            self.v = l
        elif type == "w":
            self.w = l
        elif type == "x":
            self.x = l

    def __cmp__(self, other):
        # we try to convert self and other into meters and
        # if this fails, we give other a chance to do the comparison
        try:
            return cmp(tom(self), tom(other))
        except:
            # why does -cmp(other, self) not work?
            return -other.__cmp__(self)

    def __mul__(self, factor):
        result = length()
        result.t = factor * self.t
        result.u = factor * self.u
        result.v = factor * self.v
        result.w = factor * self.w
        result.x = factor * self.x
        return result

    __rmul__=__mul__

    def __div__(self, divisor):
        if isinstance(divisor, length):
            return tom(self) / tom(divisor)
        result = length()
        result.t = self.t / divisor
        result.u = self.u / divisor
        result.v = self.v / divisor
        result.w = self.w / divisor
        result.x = self.x / divisor
        return result

    __truediv__ = __div__

    def __add__(self, other):
        # convert to length if necessary
        if not isinstance(other, length):
            # if other is not a length, we try to convert it into a length and
            # if this fails, we give other a chance to do the addition
            try:
                other = length(other)
            except:
                return other + self
        result = length()
        result.t = self.t + other.t
        result.u = self.u + other.u
        result.v = self.v + other.v
        result.w = self.w + other.w
        result.x = self.x + other.x
        return result

    __radd__ = __add__

    def __sub__(self, other):
        # convert to length if necessary
        if not isinstance(other, length):
            # if other is not a length, we try to convert it into a length and
            # if this fails, we give other a chance to do the subtraction
            try:
                other = length(other)
            except:
                return -other + self
        result = length()
        result.t = self.t - other.t
        result.u = self.u - other.u
        result.v = self.v - other.v
        result.w = self.w - other.w
        result.x = self.x - other.x
        return result

    def __rsub__(self, other):
        # convert to length if necessary
        if not isinstance(other, length):
            other = length(other)
        result = length()
        result.t = other.t - self.t
        result.u = other.u - self.u
        result.v = other.v - self.v
        result.w = other.w - self.w
        result.x = other.x - self.x
        return result

    def __neg__(self):
        result = length()
        result.t = -self.t
        result.u = -self.u
        result.v = -self.v
        result.w = -self.w
        result.x = -self.x
        return result

    def __str__(self):
        return "(%(t)f t + %(u)f u + %(v)f v + %(w)f w + %(x)f x) m" % self.__dict__


################################################################################
# predefined instances which can be used as length units
################################################################################

# user lengths and unqualified length which are also user length
u_pt   = pt   = length(1, type="u", unit="pt")
u_m    = m    = length(1, type="u", unit="m")
u_mm   = mm   = length(1, type="u", unit="mm")
u_cm   = cm   = length(1, type="u", unit="cm")
u_inch = inch = length(1, type="u", unit="inch")

# true lengths
t_pt   = length(1, type="t", unit="pt")
t_m    = length(1, type="t", unit="m")
t_mm   = length(1, type="t", unit="mm")
t_cm   = length(1, type="t", unit="cm")
t_inch = length(1, type="t", unit="inch")

# visual lengths
v_pt   = length(1, type="v", unit="pt")
v_m    = length(1, type="v", unit="m")
v_mm   = length(1, type="v", unit="mm")
v_cm   = length(1, type="v", unit="cm")
v_inch = length(1, type="v", unit="inch")

# width lengths
w_pt   = length(1, type="w", unit="pt")
w_m    = length(1, type="w", unit="m")
w_mm   = length(1, type="w", unit="mm")
w_cm   = length(1, type="w", unit="cm")
w_inch = length(1, type="w", unit="inch")

# TeX lengths
x_pt   = length(1, type="x", unit="pt")
x_m    = length(1, type="x", unit="m")
x_mm   = length(1, type="x", unit="mm")
x_cm   = length(1, type="x", unit="cm")
x_inch = length(1, type="x", unit="inch")
