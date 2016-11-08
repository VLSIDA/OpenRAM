# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2002-2004, 2006 Jörg Lehmann <joergl@users.sourceforge.net>
# Copyright (C) 2003-2006 Michael Schindler <m-schindler@users.sourceforge.net>
# Copyright (C) 2002-2007 André Wobst <wobsta@users.sourceforge.net>
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

import binascii, colorsys, math, struct, warnings
import attr, style, pdfwriter

# device-dependend (nonlinear) functions for color conversion
# UCRx : [0,1] -> [-1, 1] UnderColorRemoval (removes black from c, y, m)
# BG   : [0,1] -> [0, 1]  BlackGeneration (generate the black from the nominal k-value)
# as long as we have no further knowledge we define them linearly with constants 1
def _UCRc(x): return x
def _UCRm(x): return x
def _UCRy(x): return x
def _BG(x): return x

def set(UCRc=None, UCRm=None, UCRy=None, BG=None):
    global _UCRc
    global _UCRm
    global _UCRy
    global _BG

    if UCRc is not None:
        _UCRc = UCRc
    if UCRm is not None:
        _UCRm = UCRm
    if UCRy is not None:
        _UCRy = UCRy
    if BG is not None:
        _BG = BG


class color(attr.exclusiveattr, style.strokestyle, style.fillstyle):

    """base class for all colors"""

    def __init__(self):
        attr.exclusiveattr.__init__(self, color)


clear = attr.clearclass(color)


class grey(color):

    """grey tones"""

    def __init__(self, gray):
        color.__init__(self)
        if gray<0 or gray>1: raise ValueError
        self.color = {"gray": gray}

    def processPS(self, file, writer, context, registry, bbox):
        file.write("%(gray)g setgray\n" % self.color)

    def processPDF(self, file, writer, context, registry, bbox):
        if context.strokeattr:
            file.write("%(gray)f G\n" % self.color)
        if context.fillattr:
            file.write("%(gray)f g\n" % self.color)

    def cmyk(self):
        return cmyk(0, 0, 0, 1 - self.color["gray"])

    def grey(self):
        return grey(**self.color)
    gray = grey

    def hsb(self):
        return hsb(0, 0, self.color["gray"])

    def rgb(self):
        return rgb(self.color["gray"], self.color["gray"], self.color["gray"])

    def colorspacestring(self):
        return "/DeviceGray"

    def tostring8bit(self):
        return chr(int(self.color["gray"]*255))

grey.black = grey(0.0)
grey.white = grey(1.0)
gray = grey


class rgb(color):

    """rgb colors"""

    def __init__(self, r=0.0, g=0.0, b=0.0):
        color.__init__(self)
        if r<0 or r>1 or g<0 or g>1 or b<0 or b>1: raise ValueError
        self.color = {"r": r, "g": g, "b": b}

    def processPS(self, file, writer, context, registry, bbox):
        file.write("%(r)g %(g)g %(b)g setrgbcolor\n" % self.color)

    def processPDF(self, file, writer, context, registry, bbox):
        if context.strokeattr:
            file.write("%(r)f %(g)f %(b)f RG\n" % self.color)
        if context.fillattr:
            file.write("%(r)f %(g)f %(b)f rg\n" % self.color)

    def cmyk(self):
        # conversion to cmy
        c, m, y = 1 - self.color["r"], 1 - self.color["g"], 1 - self.color["b"]
        # conversion from cmy to cmyk with device-dependent functions
        k = min([c, m, y])
        return cmyk(min(1, max(0, c - _UCRc(k))),
                    min(1, max(0, m - _UCRm(k))),
                    min(1, max(0, y - _UCRy(k))),
                    _BG(k))

    def grey(self):
        return grey(0.3*self.color["r"] + 0.59*self.color["g"] + 0.11*self.color["b"])
    gray = grey

    def hsb(self):

        values = self.color.values()
        values.sort()
        z, y, x = values
        r, g, b = self.color["r"], self.color["g"], self.color["b"]
        try:
            if r == x and g == z:
                return hsb((5 + (x-b)/(x-z)) / 6.0, (x - z) / x, x)
            elif r == x and g > z:
                return hsb((1 - (x-g)/(x-z)) / 6.0, (x - z) / x, x)
            elif g == x and b == z:
                return hsb((1 + (x-r)/(x-z)) / 6.0, (x - z) / x, x)
            elif g == x and b > z:
                return hsb((3 - (x-b)/(x-z)) / 6.0, (x - z) / x, x)
            elif b == x and r == z:
                return hsb((3 + (x-g)/(x-z)) / 6.0, (x - z) / x, x)
            elif b == x and r > z:
                return hsb((5 - (x-r)/(x-z)) / 6.0, (x - z) / x, x)
            else:
                raise ValueError
        except ZeroDivisionError:
            return hsb(0, 0, x)

    def rgb(self):
        return rgb(**self.color)

    def colorspacestring(self):
        return "/DeviceRGB"

    def tostring8bit(self):
        return struct.pack("BBB", int(self.color["r"]*255), int(self.color["g"]*255), int(self.color["b"]*255))

    def tohexstring(self, cssstrip=1, addhash=1):
        hexstring = binascii.b2a_hex(self.to8bitstring())
        if cssstrip and hexstring[0] == hexstring[1] and hexstring[2] == hexstring[3] and hexstring[4] == hexstring[5]:
            hexstring = "".join([hexstring[0], hexstring[1], hexstring[2]])
        if addhash:
            hexstring = "#" + hexstring
        return hexstring


def rgbfromhexstring(hexstring):
    hexstring = hexstring.strip().lstrip("#")
    if len(hexstring) == 3:
        hexstring = "".join([hexstring[0], hexstring[0], hexstring[1], hexstring[1], hexstring[2], hexstring[2]])
    elif len(hexstring) != 6:
        raise ValueError("3 or 6 digit hex number expected (with optional leading hash character)")
    return rgb(*[value/255.0 for value in struct.unpack("BBB", binascii.a2b_hex(hexstring))])

rgb.red   = rgb(1, 0, 0)
rgb.green = rgb(0, 1, 0)
rgb.blue  = rgb(0, 0, 1)
rgb.white = rgb(1, 1, 1)
rgb.black = rgb(0, 0, 0)


class hsb(color):

    """hsb colors"""

    def __init__(self, h=0.0, s=0.0, b=0.0):
        color.__init__(self)
        if h<0 or h>1 or s<0 or s>1 or b<0 or b>1: raise ValueError
        self.color = {"h": h, "s": s, "b": b}

    def processPS(self, file, writer, context, registry, bbox):
        file.write("%(h)g %(s)g %(b)g sethsbcolor\n" % self.color)

    def processPDF(self, file, writer, context, registry, bbox):
        r, g, b = colorsys.hsv_to_rgb(self.color["h"], self.color["s"], self.color["b"])
        rgb(r, g, b).processPDF(file, writer, context, registry, bbox)

    def cmyk(self):
        return self.rgb().cmyk()

    def grey(self):
        return self.rgb().grey()
    gray = grey

    def hsb(self):
        return hsb(**self.color)

    def rgb(self):
        h, s, b = self.color["h"], self.color["s"], self.color["b"]
        i = int(6*h)
        f = 6*h - i
        m, n, k = 1 - s, 1 - s*f, 1 - s*(1-f)
        if i == 1:
            return rgb(b*n, b, b*m)
        elif i == 2:
            return rgb(b*m, b, b*k)
        elif i == 3:
            return rgb(b*m, b*n, b)
        elif i == 4:
            return rgb(b*k, b*m, b)
        elif i == 5:
            return rgb(b, b*m, b*n)
        else:
            return rgb(b, b*k, b*m)

    def colorspacestring(self):
        raise RuntimeError("colorspace string not available for hsb colors")


class cmyk(color):

    """cmyk colors"""

    def __init__(self, c=0.0, m=0.0, y=0.0, k=0.0):
        color.__init__(self)
        if c<0 or c>1 or m<0 or m>1 or y<0 or y>1 or k<0 or k>1: raise ValueError
        self.color = {"c": c, "m": m, "y": y, "k": k}

    def processPS(self, file, writer, context, registry, bbox):
        file.write("%(c)g %(m)g %(y)g %(k)g setcmykcolor\n" % self.color)

    def processPDF(self, file, writer, context, registry, bbox):
        if context.strokeattr:
            file.write("%(c)f %(m)f %(y)f %(k)f K\n" % self.color)
        if context.fillattr:
            file.write("%(c)f %(m)f %(y)f %(k)f k\n" % self.color)

    def cmyk(self):
        return cmyk(**self.color)

    def grey(self):
        return grey(1 - min([1, 0.3*self.color["c"] + 0.59*self.color["m"] +
                                0.11*self.color["y"] + self.color["k"]]))
    gray = grey

    def hsb(self):
        return self.rgb().hsb()

    def rgb(self):
        # conversion to cmy:
        c = min(1, self.color["c"] + self.color["k"])
        m = min(1, self.color["m"] + self.color["k"])
        y = min(1, self.color["y"] + self.color["k"])
        # conversion from cmy to rgb:
        return rgb(1 - c, 1 - m, 1 - y)

    def colorspacestring(self):
        return "/DeviceCMYK"

    def tostring8bit(self):
        return struct.pack("BBBB", int(self.color["c"]*255), int(self.color["m"]*255), int(self.color["y"]*255), int(self.color["k"]*255))

cmyk.GreenYellow    = cmyk(0.15, 0, 0.69, 0)
cmyk.Yellow         = cmyk(0, 0, 1, 0)
cmyk.Goldenrod      = cmyk(0, 0.10, 0.84, 0)
cmyk.Dandelion      = cmyk(0, 0.29, 0.84, 0)
cmyk.Apricot        = cmyk(0, 0.32, 0.52, 0)
cmyk.Peach          = cmyk(0, 0.50, 0.70, 0)
cmyk.Melon          = cmyk(0, 0.46, 0.50, 0)
cmyk.YellowOrange   = cmyk(0, 0.42, 1, 0)
cmyk.Orange         = cmyk(0, 0.61, 0.87, 0)
cmyk.BurntOrange    = cmyk(0, 0.51, 1, 0)
cmyk.Bittersweet    = cmyk(0, 0.75, 1, 0.24)
cmyk.RedOrange      = cmyk(0, 0.77, 0.87, 0)
cmyk.Mahogany       = cmyk(0, 0.85, 0.87, 0.35)
cmyk.Maroon         = cmyk(0, 0.87, 0.68, 0.32)
cmyk.BrickRed       = cmyk(0, 0.89, 0.94, 0.28)
cmyk.Red            = cmyk(0, 1, 1, 0)
cmyk.OrangeRed      = cmyk(0, 1, 0.50, 0)
cmyk.RubineRed      = cmyk(0, 1, 0.13, 0)
cmyk.WildStrawberry = cmyk(0, 0.96, 0.39, 0)
cmyk.Salmon         = cmyk(0, 0.53, 0.38, 0)
cmyk.CarnationPink  = cmyk(0, 0.63, 0, 0)
cmyk.Magenta        = cmyk(0, 1, 0, 0)
cmyk.VioletRed      = cmyk(0, 0.81, 0, 0)
cmyk.Rhodamine      = cmyk(0, 0.82, 0, 0)
cmyk.Mulberry       = cmyk(0.34, 0.90, 0, 0.02)
cmyk.RedViolet      = cmyk(0.07, 0.90, 0, 0.34)
cmyk.Fuchsia        = cmyk(0.47, 0.91, 0, 0.08)
cmyk.Lavender       = cmyk(0, 0.48, 0, 0)
cmyk.Thistle        = cmyk(0.12, 0.59, 0, 0)
cmyk.Orchid         = cmyk(0.32, 0.64, 0, 0)
cmyk.DarkOrchid     = cmyk(0.40, 0.80, 0.20, 0)
cmyk.Purple         = cmyk(0.45, 0.86, 0, 0)
cmyk.Plum           = cmyk(0.50, 1, 0, 0)
cmyk.Violet         = cmyk(0.79, 0.88, 0, 0)
cmyk.RoyalPurple    = cmyk(0.75, 0.90, 0, 0)
cmyk.BlueViolet     = cmyk(0.86, 0.91, 0, 0.04)
cmyk.Periwinkle     = cmyk(0.57, 0.55, 0, 0)
cmyk.CadetBlue      = cmyk(0.62, 0.57, 0.23, 0)
cmyk.CornflowerBlue = cmyk(0.65, 0.13, 0, 0)
cmyk.MidnightBlue   = cmyk(0.98, 0.13, 0, 0.43)
cmyk.NavyBlue       = cmyk(0.94, 0.54, 0, 0)
cmyk.RoyalBlue      = cmyk(1, 0.50, 0, 0)
cmyk.Blue           = cmyk(1, 1, 0, 0)
cmyk.Cerulean       = cmyk(0.94, 0.11, 0, 0)
cmyk.Cyan           = cmyk(1, 0, 0, 0)
cmyk.ProcessBlue    = cmyk(0.96, 0, 0, 0)
cmyk.SkyBlue        = cmyk(0.62, 0, 0.12, 0)
cmyk.Turquoise      = cmyk(0.85, 0, 0.20, 0)
cmyk.TealBlue       = cmyk(0.86, 0, 0.34, 0.02)
cmyk.Aquamarine     = cmyk(0.82, 0, 0.30, 0)
cmyk.BlueGreen      = cmyk(0.85, 0, 0.33, 0)
cmyk.Emerald        = cmyk(1, 0, 0.50, 0)
cmyk.JungleGreen    = cmyk(0.99, 0, 0.52, 0)
cmyk.SeaGreen       = cmyk(0.69, 0, 0.50, 0)
cmyk.Green          = cmyk(1, 0, 1, 0)
cmyk.ForestGreen    = cmyk(0.91, 0, 0.88, 0.12)
cmyk.PineGreen      = cmyk(0.92, 0, 0.59, 0.25)
cmyk.LimeGreen      = cmyk(0.50, 0, 1, 0)
cmyk.YellowGreen    = cmyk(0.44, 0, 0.74, 0)
cmyk.SpringGreen    = cmyk(0.26, 0, 0.76, 0)
cmyk.OliveGreen     = cmyk(0.64, 0, 0.95, 0.40)
cmyk.RawSienna      = cmyk(0, 0.72, 1, 0.45)
cmyk.Sepia          = cmyk(0, 0.83, 1, 0.70)
cmyk.Brown          = cmyk(0, 0.81, 1, 0.60)
cmyk.Tan            = cmyk(0.14, 0.42, 0.56, 0)
cmyk.Gray           = cmyk(0, 0, 0, 0.50)
cmyk.Grey           = cmyk.Gray
cmyk.Black          = cmyk(0, 0, 0, 1)
cmyk.White          = cmyk(0, 0, 0, 0)
cmyk.white          = cmyk.White
cmyk.black          = cmyk.Black

class palette(attr.changelist):
    """color palettes

    A color palette is a discrete, ordered list of colors"""

palette.clear = attr.clearclass(palette)


class gradient(attr.changeattr):

    """base class for color gradients

    A gradient is a continuous collection of colors with a single parameter ranging from 0 to 1
    to address them"""

    def getcolor(self, param):
        """return color corresponding to param"""
        pass

    def select(self, index, n_indices):
        """return a color corresponding to an index out of n_indices"""
        if n_indices == 1:
            param = 0
        else:
            param = index / (n_indices - 1.0)
        return self.getcolor(param)

gradient.clear = attr.clearclass(gradient)


class lineargradient(gradient):

    """collection of two colors for a linear transition between them"""

    def __init__(self, mincolor, maxcolor):
        if mincolor.__class__ != maxcolor.__class__:
            raise ValueError
        self.colorclass = mincolor.__class__
        self.mincolor = mincolor
        self.maxcolor = maxcolor

    def getcolor(self, param):
        colordict = {}
        for key in self.mincolor.color.keys():
            colordict[key] = param * self.maxcolor.color[key] + (1 - param) * self.mincolor.color[key]
        return self.colorclass(**colordict)


class functiongradient(gradient):

    """collection of colors for an arbitray non-linear transition between them

    parameters:
    functions: a dictionary for the color values
    type:      a string indicating the color class
    """

    def __init__(self, functions, cls):
        self.functions = functions
        self.cls = cls

    def getcolor(self, param):
        colordict = {}
        for key in self.functions.keys():
            colordict[key] = self.functions[key](param)
        return self.cls(**colordict)


gradient.Gray           = lineargradient(gray.white, gray.black)
gradient.Grey           = gradient.Gray
gradient.ReverseGray    = lineargradient(gray.black, gray.white)
gradient.ReverseGrey    = gradient.ReverseGray
gradient.BlackYellow    = functiongradient({ # compare this with reversegray above
    "r":(lambda x: 2*x*(1-x)**5 + 3.5*x**2*(1-x)**3 + 2.1*x*x*(1-x)**2 + 3.0*x**3*(1-x)**2 + x**0.5*(1-(1-x)**2)),
    "g":(lambda x: 1.5*x**2*(1-x)**3 - 0.8*x**3*(1-x)**2 + 2.0*x**4*(1-x) + x**4),
    "b":(lambda x: 5*x*(1-x)**5 - 0.5*x**2*(1-x)**3 + 0.3*x*x*(1-x)**2 + 5*x**3*(1-x)**2 + 0.5*x**6)},
    rgb)
gradient.RedGreen       = lineargradient(rgb.red, rgb.green)
gradient.RedBlue        = lineargradient(rgb.red, rgb.blue)
gradient.GreenRed       = lineargradient(rgb.green, rgb.red)
gradient.GreenBlue      = lineargradient(rgb.green, rgb.blue)
gradient.BlueRed        = lineargradient(rgb.blue, rgb.red)
gradient.BlueGreen      = lineargradient(rgb.blue, rgb.green)
gradient.RedBlack       = lineargradient(rgb.red, rgb.black)
gradient.BlackRed       = lineargradient(rgb.black, rgb.red)
gradient.RedWhite       = lineargradient(rgb.red, rgb.white)
gradient.WhiteRed       = lineargradient(rgb.white, rgb.red)
gradient.GreenBlack     = lineargradient(rgb.green, rgb.black)
gradient.BlackGreen     = lineargradient(rgb.black, rgb.green)
gradient.GreenWhite     = lineargradient(rgb.green, rgb.white)
gradient.WhiteGreen     = lineargradient(rgb.white, rgb.green)
gradient.BlueBlack      = lineargradient(rgb.blue, rgb.black)
gradient.BlackBlue      = lineargradient(rgb.black, rgb.blue)
gradient.BlueWhite      = lineargradient(rgb.blue, rgb.white)
gradient.WhiteBlue      = lineargradient(rgb.white, rgb.blue)
gradient.Rainbow        = lineargradient(hsb(0, 1, 1), hsb(2.0/3.0, 1, 1))
gradient.ReverseRainbow = lineargradient(hsb(2.0/3.0, 1, 1), hsb(0, 1, 1))
gradient.Hue            = lineargradient(hsb(0, 1, 1), hsb(1, 1, 1))
gradient.ReverseHue     = lineargradient(hsb(1, 1, 1), hsb(0, 1, 1))


class PDFextgstate(pdfwriter.PDFobject):

    def __init__(self, name, extgstate, registry):
        pdfwriter.PDFobject.__init__(self, "extgstate", name)
        registry.addresource("ExtGState", name, self)
        self.name = name
        self.extgstate = extgstate

    def write(self, file, writer, registry):
        file.write("%s\n" % self.extgstate)


class transparency(attr.exclusiveattr, style.strokestyle, style.fillstyle):

    def __init__(self, value):
        self.value = 1-value
        attr.exclusiveattr.__init__(self, transparency)

    def processPS(self, file, writer, context, registry, bbox):
        warnings.warn("Transparency not available in PostScript, proprietary ghostscript extension code inserted.")
        file.write("%f .setshapealpha\n" % self.value)

    def processPDF(self, file, writer, context, registry, bbox):
        if context.strokeattr and context.fillattr:
            registry.add(PDFextgstate("Transparency-%f" % self.value,
                                      "<< /Type /ExtGState /CA %f /ca %f >>" % (self.value, self.value), registry))
            file.write("/Transparency-%f gs\n" % self.value)
        elif context.strokeattr:
            registry.add(PDFextgstate("Transparency-Stroke-%f" % self.value,
                                      "<< /Type /ExtGState /CA %f >>" % self.value, registry))
            file.write("/Transparency-Stroke-%f gs\n" % self.value)
        elif context.fillattr:
            registry.add(PDFextgstate("Transparency-Fill-%f" % self.value,
                                      "<< /Type /ExtGState /ca %f >>" % self.value, registry))
            file.write("/Transparency-Fill-%f gs\n" % self.value)

