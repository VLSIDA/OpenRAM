# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2005-2006 Jörg Lehmann <joergl@users.sourceforge.net>
# Copyright (C) 2005-2006 André Wobst <wobsta@users.sourceforge.net>
# Copyright (C) 2007 Michael Schindler <m-schindler@users.sourceforge.net>
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

import bbox, canvas, pswriter, pdfwriter

try:
    enumerate([])
except NameError:
    # fallback implementation for Python 2.2 and below
    def enumerate(list):
        return zip(xrange(len(list)), list)


class encoding:

    def __init__(self, name, filename):
        """ font encoding contained in filename """
        self.name = name
        self.filename = filename


class encodingfile:

    def __init__(self, name, filename):
        # XXX move the cursor to a module of its own
        from font.t1font import cursor
        self.name = name
        encfile = open(filename, "r")
        c = cursor(encfile.read(), "")
        encfile.close()

        # name of encoding
        self.encname = c.gettoken()
        token = c.gettoken()
        if token != "[":
            raise RuntimeError("cannot parse encoding file '%s', expecting '[' got '%s'" % (filename, token))
        self.encvector = []
        for i in range(256):
            token = c.gettoken()
            if token == "]":
                raise RuntimeError("not enough charcodes in encoding file '%s'" % filename)
            self.encvector.append(token)
        if c.gettoken() != "]":
            raise RuntimeError("too many charcodes in encoding file '%s'" % filename)
        token = c.gettoken()
        if token != "def":
            raise RuntimeError("cannot parse encoding file '%s', expecting 'def' got '%s'" % (filename, token))

    def decode(self, charcode):
        return self.encvector[charcode]

    def outputPS(self, file, writer):
        file.write("%%%%BeginProcSet: %s\n" % self.name)
        file.write("/%s\n"
                   "[" % self.name)
        for i, glyphname in enumerate(self.encvector):
            if i and not (i % 8):
                file.write("\n")
            else:
                file.write(" ")
            file.write(glyphname)
        file.write(" ] def\n"
                   "%%EndProcSet\n")

    def outputPDF(self, file, writer):
        file.write("<<\n"
                   "/Type /Encoding\n"
                   "/Differences\n"
                   "[ 0")
        for i, glyphname in enumerate(self.encvector):
            if i and not (i % 8):
                file.write("\n")
            else:
                file.write(" ")
            file.write(glyphname)
        file.write(" ]\n"
                   ">>\n")


class font:

    def __init__(self, basefontname, filename, encoding, slant, metric):
        self.basefontname = basefontname
        self.filename = filename
        self.encoding = encoding
        self.slant = slant # None or a float
        self.metric = metric

        if encoding is not None and slant is not None:
            self.encname = "%s-%s" % (basefontname, encoding.name)
            self.name = "%s-slant%f" % (self.encname, self.slant)
        elif encoding is not None:
            self.name = "%s-%s" % (basefontname, encoding.name)
        elif slant is not None:
            self.name = "%s-slant%f" % (basefontname, self.slant)
        else:
            self.name = basefontname


class text_pt(canvas.canvasitem):

    def __init__(self, x_pt, y_pt, font):
        self.font = font
        self.x_pt = x_pt
        self.y_pt = y_pt
        self.width_pt = 0
        self.height_pt = 0
        self.depth_pt = 0
        self.chars = []

    def addchar(self, char):
        metric = self.font.metric
        self.width_pt += metric.getwidth_pt(char)
        cheight_pt = metric.getwidth_pt(char)
        if cheight_pt > self.height_pt:
            self.height_pt = cheight_pt
        cdepth_pt = metric.getdepth_pt(char)
        if cdepth_pt > self.depth_pt:
            self.depth_pt = cdepth_pt
        self.chars.append(char)

    def bbox(self):
        return bbox.bbox_pt(self.x_pt, self.y_pt-self.depth_pt, self.x_pt+self.width_pt, self.y_pt+self.height_pt)

    def processPS(self, file, writer, context, registry, bbox):
        # note that we don't register PSfont as it is just a helper resource
        # which registers the needed components
        pswriter.PSfont(self.font, self.chars, registry)
        bbox += self.bbox()

        if ( context.font is None or
             context.font.name != self.font.name or
             context.font.metric.getsize_pt() !=  self.font.metric.getsize_pt() ):
            file.write("/%s %f selectfont\n" % (self.font.name, self.font.metric.getsize_pt()))
            context.font = self.font
        outstring = ""
        for char in self.chars:
            if char > 32 and char < 127 and chr(char) not in "()[]<>\\":
                ascii = "%s" % chr(char)
            else:
                ascii = "\\%03o" % char
            outstring += ascii
        file.write("%g %g moveto (%s) show\n" % (self.x_pt, self.y_pt, outstring))

    def processPDF(self, file, writer, context, registry, bbox):
        registry.add(pdfwriter.PDFfont(self.font, self.chars, writer, registry))
        bbox += self.bbox()

        if ( context.font is None or
             context.font.name != self.font.name or
             context.font.metric.getsize_pt() !=  self.font.metric.getsize_pt() ):
            file.write("/%s %f Tf\n" % (self.font.name, self.font.metric.getsize_pt()))
            context.font = self.font
        outstring = ""
        for char in self.chars:
            if 32 <= char <= 127 and chr(char) not in "()[]<>\\":
                ascii = "%s" % chr(char)
            else:
                ascii = "\\%03o" % char
            outstring += ascii
        if self.font.slant is None:
            slantvalue = 0
        else:
            slantvalue = self.font.slant
        file.write("1 0 %f 1 %f %f Tm (%s) Tj\n" % (slantvalue, self.x_pt, self.y_pt, outstring))

