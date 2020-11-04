# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2002-2006 Jörg Lehmann <joergl@users.sourceforge.net>
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

import string
import canvas, bbox, pykpathsea, unit, trafo, pswriter

# PostScript-procedure definitions (cf. 5002.EPSF_Spec_v3.0.pdf)
# with important correction in EndEPSF:
#   end operator is missing in the spec!

_BeginEPSF = pswriter.PSdefinition("BeginEPSF", """{
  /b4_Inc_state save def
  /dict_count countdictstack def
  /op_count count 1 sub def
  userdict begin
  /showpage { } def
  0 setgray 0 setlinecap
  1 setlinewidth 0 setlinejoin
  10 setmiterlimit [ ] 0 setdash newpath
  /languagelevel where
  {pop languagelevel
  1 ne
    {false setstrokeadjust false setoverprint
    } if
  } if
} bind""")

_EndEPSF = pswriter.PSdefinition("EndEPSF", """{
  end
  count op_count sub {pop} repeat
  countdictstack dict_count sub {end} repeat
  b4_Inc_state restore
} bind""")


class linefilereader:
    """a line by line file reader

    This line by line file reader allows for '\n', '\r' and
    '\r\n' as line separation characters. Line separation
    characters are not modified (binary mode). It implements
    a readline, a read and a close method similar to a regular
    file object."""

    # note: '\n\r' is not considered to be a linebreak as its documented
    #       in the DSC spec #5001, while '\n\r' *is* a *single* linebreak
    #       according to the EPSF spec #5002

    def __init__(self, filename, typicallinelen=257):
        """Opens the file filename for reading.

        typicallinelen defines the default buffer increase
        to find the next linebreak."""

        # note: The maximal line size in an EPS is 255 plus the
        #       linebreak characters. However, we also handle
        #       lines longer than that.

        self.file = open(filename, "rb")
        self.buffer = ""
        self.typicallinelen = typicallinelen

    def read(self, count=None, EOFmsg="unexpected end of file"):
        """read bytes from the file

        count is the number of bytes to be read when set. Then count
        is unset, the rest of the file is returned. EOFmsg is used
        to raise a IOError, when the end of the file is reached while
        reading count bytes or when the rest of the file is empty when
        count is unset. When EOFmsg is set to None, less than the
        requested number of bytes might be returned."""
        if count is not None:
            if count > len(self.buffer):
                self.buffer += self.file.read(count - len(self.buffer))
            if EOFmsg is not None and len(self.buffer) < count:
                raise IOError(EOFmsg)
            result = self.buffer[:count]
            self.buffer = self.buffer[count:]
            return result
        else:
            self.buffer += self.file.read()
            if EOFmsg is not None and not len(self.buffer):
                raise IOError(EOFmsg)
            result = self.buffer
            self.buffer = ""
            return result

    def readline(self, EOFmsg="unexpected end of file"):
        """reads a line from the file

        Lines are separated by '\n', '\r' or '\r\n'. The line separation
        strings are included in the return value. The last line might not
        end with an line separation string. Reading beyond the file generates
        an IOError with the EOFmsg message. When EOFmsg is None, an empty
        string is returned when reading beyond the end of the file."""
        EOF = 0
        while 1:
            crpos = self.buffer.find("\r")
            nlpos = self.buffer.find("\n")
            if nlpos == -1 and (crpos == -1 or crpos == len(self.buffer) - 1) and not EOF:
                newbuffer = self.file.read(self.typicallinelen)
                if not len(newbuffer):
                    EOF = 1
                self.buffer += newbuffer
            else:
                eol = len(self.buffer)
                if not eol and EOFmsg is not None:
                    raise IOError(EOFmsg)
                if nlpos != -1:
                    eol = nlpos + 1
                if crpos != -1 and (nlpos == -1 or crpos < nlpos - 1):
                    eol = crpos + 1
                result = self.buffer[:eol]
                self.buffer = self.buffer[eol:]
                return result

    def close(self):
        "closes the file"
        self.file.close()


def _readbbox(filename):
    """returns bounding box of EPS file filename"""

    file = linefilereader(filename)

    # check the %! header comment
    if not file.readline().startswith("%!"):
        raise IOError("file doesn't start with a '%!' header comment")

    bboxatend = 0
    # parse the header (use the first BoundingBox)
    while 1:
        line = file.readline()
        if not line:
            break
        if line.startswith("%%BoundingBox:") and not bboxatend:
            values = line.split(":", 1)[1].split()
            if values == ["(atend)"]:
                bboxatend = 1
            else:
                if len(values) != 4:
                    raise IOError("invalid number of bounding box values")
                return bbox.bbox_pt(*map(int, values))
        elif (line.rstrip() == "%%EndComments" or
              (len(line) >= 2 and line[0] != "%" and line[1] not in string.whitespace)):
            # implicit end of comments section
            break
    if not bboxatend:
        raise IOError("no bounding box information found")

    # parse the body
    nesting = 0 # allow for nested documents
    while 1:
        line = file.readline()
        if line.startswith("%%BeginData:"):
            values = line.split(":", 1)[1].split()
            if len(values) > 3:
                raise IOError("invalid number of arguments")
            if len(values) == 3:
                if values[2] == "Lines":
                    for i in xrange(int(values[0])):
                        file.readline()
                elif values[2] != "Bytes":
                    raise IOError("invalid bytesorlines-value")
                else:
                    file.read(int(values[0]))
            else:
                file.read(int(values[0]))
            line = file.readline()
            # ignore tailing whitespace/newline for binary data
            if (len(values) < 3 or values[2] != "Lines") and not len(line.strip()):
                line = file.readline()
            if line.rstrip() != "%%EndData":
                raise IOError("missing EndData")
        elif line.startswith("%%BeginBinary:"):
            file.read(int(line.split(":", 1)[1]))
            line = file.readline()
            # ignore tailing whitespace/newline
            if not len(line.strip()):
                line = file.readline()
            if line.rstrip() != "%%EndBinary":
                raise IOError("missing EndBinary")
        elif line.startswith("%%BeginDocument:"):
            nesting += 1
        elif line.rstrip() == "%%EndDocument":
            if nesting < 1:
                raise IOError("unmatched EndDocument")
            nesting -= 1
        elif not nesting and line.rstrip() == "%%Trailer":
            break

    usebbox = None
    # parse the trailer (use the last BoundingBox)
    line = True
    while line:
        line = file.readline(EOFmsg=None)
        if line.startswith("%%BoundingBox:"):
            values = line.split(":", 1)[1].split()
            if len(values) != 4:
                raise IOError("invalid number of bounding box values")
            usebbox = bbox.bbox_pt(*map(int, values))
    if not usebbox:
        raise IOError("missing bounding box information in document trailer")
    return usebbox


class epsfile(canvas.canvasitem):

    """class for epsfiles"""

    def __init__(self,
                 x, y, filename,
                 width=None, height=None, scale=None, align="bl",
                 clip=1, translatebbox=1, bbox=None,
                 kpsearch=0):
        """inserts epsfile

        Object for an EPS file named filename at position (x,y). Width, height,
        scale and aligment can be adjusted by the corresponding parameters. If
        clip is set, the result gets clipped to the bbox of the EPS file. If
        translatebbox is not set, the EPS graphics is not translated to the
        corresponding origin. If bbox is not None, it overrides the bounding
        box in the epsfile itself. If kpsearch is set then filename is searched
        using the kpathsea library.
        """

        self.x_pt = unit.topt(x)
        self.y_pt = unit.topt(y)
        if kpsearch:
            self.filename = pykpathsea.find_file(filename, pykpathsea.kpse_pict_format)
        else:
            self.filename = filename
        self.mybbox = bbox or _readbbox(self.filename)

        # determine scaling in x and y direction
        self.scalex = self.scaley = scale

        if width is not None or height is not None:
            if scale is not None:
                raise ValueError("cannot set both width and/or height and scale simultaneously")
            if height is not None:
                self.scaley = unit.topt(height)/(self.mybbox.ury_pt-self.mybbox.lly_pt)
            if width is not None:
                self.scalex = unit.topt(width)/(self.mybbox.urx_pt-self.mybbox.llx_pt)

            if self.scalex is None:
                self.scalex = self.scaley
            if self.scaley is None:
                self.scaley = self.scalex

        # set the actual width and height of the eps file (after a
        # possible scaling)
        self.width_pt  = self.mybbox.urx_pt-self.mybbox.llx_pt
        if self.scalex:
            self.width_pt *= self.scalex

        self.height_pt = self.mybbox.ury_pt-self.mybbox.lly_pt
        if self.scaley:
            self.height_pt *= self.scaley

        # take alignment into account
        self.align       = align
        if self.align[0]=="b":
            pass
        elif self.align[0]=="c":
            self.y_pt -= self.height_pt/2.0
        elif self.align[0]=="t":
            self.y_pt -= self.height_pt
        else:
            raise ValueError("vertical alignment can only be b (bottom), c (center), or t (top)")

        if self.align[1]=="l":
            pass
        elif self.align[1]=="c":
            self.x_pt -= self.width_pt/2.0
        elif self.align[1]=="r":
            self.x_pt -= self.width_pt
        else:
            raise ValueError("horizontal alignment can only be l (left), c (center), or r (right)")

        self.clip = clip
        self.translatebbox = translatebbox

        self.trafo = trafo.translate_pt(self.x_pt, self.y_pt)

        if self.scalex is not None:
            self.trafo = self.trafo * trafo.scale_pt(self.scalex, self.scaley)

        if translatebbox:
            self.trafo = self.trafo * trafo.translate_pt(-self.mybbox.llx_pt, -self.mybbox.lly_pt)

    def bbox(self):
        return self.mybbox.transformed(self.trafo)

    def processPS(self, file, writer, context, registry, bbox):
        registry.add(_BeginEPSF)
        registry.add(_EndEPSF)
        bbox += self.bbox()
        try:
            epsfile=open(self.filename,"rb")
        except:
            raise IOError, "cannot open EPS file '%s'" % self.filename

        file.write("BeginEPSF\n")

        if self.clip:
            llx_pt, lly_pt, urx_pt, ury_pt = self.mybbox.transformed(self.trafo).highrestuple_pt()
            file.write("%g %g %g %g rectclip\n" % (llx_pt, lly_pt, urx_pt-llx_pt, ury_pt-lly_pt))

        self.trafo.processPS(file, writer, context, registry, bbox)

        file.write("%%%%BeginDocument: %s\n" % self.filename)
        file.write(epsfile.read())
        file.write("%%EndDocument\n")
        file.write("EndEPSF\n")

    def processPDF(self, file, writer, context, registry, bbox):
        raise RuntimeError("Including EPS files in PDF files not supported")
