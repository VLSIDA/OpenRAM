# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2004-2006 André Wobst <wobsta@users.sourceforge.net>
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

import struct, warnings, binascii
try:
    import zlib
    haszlib = 1
except:
    haszlib = 0

import bbox, canvas, pswriter, pdfwriter, trafo, unit

def ascii85lines(datalen):
    if datalen < 4:
        return 1
    return (datalen + 56)/60

def ascii85stream(file, data):
    """Encodes the string data in ASCII85 and writes it to
    the stream file. The number of lines written to the stream
    is known just from the length of the data by means of the
    ascii85lines function. Note that the tailing newline character
    of the last line is not added by this function, but it is taken
    into account in the ascii85lines function."""
    i = 3 # go on smoothly in case of data length equals zero
    l = 0
    l = [None, None, None, None]
    for i in range(len(data)):
        c = data[i]
        l[i%4] = ord(c)
        if i%4 == 3:
            if i%60 == 3 and i != 3:
                file.write("\n")
            if l:
                # instead of
                # l[3], c5 = divmod(256*256*256*l[0]+256*256*l[1]+256*l[2]+l[3], 85)
                # l[2], c4 = divmod(l[3], 85)
                # we have to avoid number > 2**31 by
                l[3], c5 = divmod(256*256*l[0]+256*256*l[1]+256*l[2]+l[3], 85)
                l[2], c4 = divmod(256*256*3*l[0]+l[3], 85)
                l[1], c3 = divmod(l[2], 85)
                c1  , c2 = divmod(l[1], 85)
                file.write(struct.pack('BBBBB', c1+33, c2+33, c3+33, c4+33, c5+33))
            else:
                file.write("z")
    if i%4 != 3:
        for j in range((i%4) + 1, 4):
            l[j] = 0
        l[3], c5 = divmod(256*256*l[0]+256*256*l[1]+256*l[2]+l[3], 85)
        l[2], c4 = divmod(256*256*3*l[0]+l[3], 85)
        l[1], c3 = divmod(l[2], 85)
        c1  , c2 = divmod(l[1], 85)
        file.write(struct.pack('BBBB', c1+33, c2+33, c3+33, c4+33)[:(i%4)+2])

_asciihexlinelength = 64
def asciihexlines(datalen):
    return (datalen*2 + _asciihexlinelength - 1) / _asciihexlinelength

def asciihexstream(file, data):
    hexdata = binascii.b2a_hex(data)
    for i in range((len(hexdata)-1)/_asciihexlinelength + 1):
        file.write(hexdata[i*_asciihexlinelength: i*_asciihexlinelength+_asciihexlinelength])
        file.write("\n")


class image:

    def __init__(self, width, height, mode, data, compressed=None):
        if width <= 0 or height <= 0:
            raise ValueError("valid image size")
        if mode not in ["L", "RGB", "CMYK"]:
            raise ValueError("invalid mode")
        if compressed is None and len(mode)*width*height != len(data):
            raise ValueError("wrong size of uncompressed data")
        self.size = width, height
        self.mode = mode
        self.data = data
        self.compressed = compressed

    def tostring(self, *args):
        if len(args):
            raise RuntimeError("encoding not supported in this implementation")
        return self.data

    def convert(self, model):
        raise RuntimeError("color model conversion not supported in this implementation")


class jpegimage(image):

    def __init__(self, file):
        try:
            data = file.read()
        except:
            data = open(file, "rb").read()
        pos = 0
        nestinglevel = 0
        try:
            while 1:
                if data[pos] == "\377" and data[pos+1] not in ["\0", "\377"]:
                    # print "marker: 0x%02x \\%03o" % (ord(data[pos+1]), ord(data[pos+1]))
                    if data[pos+1] == "\330":
                        if not nestinglevel:
                            begin = pos
                        nestinglevel += 1
                    elif not nestinglevel:
                        raise ValueError("begin marker expected")
                    elif data[pos+1] == "\331":
                        nestinglevel -= 1
                        if not nestinglevel:
                            end = pos + 2
                            break
                    elif data[pos+1] in ["\300", "\301"]:
                        l, bits, height, width, components = struct.unpack(">HBHHB", data[pos+2:pos+10])
                        if bits != 8:
                            raise ValueError("implementation limited to 8 bit per component only")
                        try:
                            mode = {1: "L", 3: "RGB", 4: "CMYK"}[components]
                        except KeyError:
                            raise ValueError("invalid number of components")
                        pos += l+1
                    elif data[pos+1] == "\340":
                        l, id, major, minor, dpikind, xdpi, ydpi = struct.unpack(">H5sBBBHH", data[pos+2:pos+16])
                        if dpikind == 1:
                            self.info = {"dpi": (xdpi, ydpi)}
                        elif dpikind == 2:
                            self.info = {"dpi": (xdpi*2.54, ydpi*2.45)}
                        # else do not provide dpi information
                        pos += l+1
                pos += 1
        except IndexError:
            raise ValueError("end marker expected")
        image.__init__(self, width, height, mode, data[begin:end], compressed="DCT")


class PSimagedata(pswriter.PSresource):

    def __init__(self, name, data, singlestring, maxstrlen):
        pswriter.PSresource.__init__(self, "imagedata", name)
        self.data = data
        self.singlestring = singlestring
        self.maxstrlen = maxstrlen

    def output(self, file, writer, registry):
        file.write("%%%%BeginRessource: %s\n" % self.id)
        if self.singlestring:
            file.write("%%%%BeginData: %i ASCII Lines\n"
                       "<~" % ascii85lines(len(self.data)))
            ascii85stream(file, self.data)
            file.write("~>\n"
                         "%%EndData\n")
        else:
            datalen = len(self.data)
            tailpos = datalen - datalen % self.maxstrlen
            file.write("%%%%BeginData: %i ASCII Lines\n" %
                       ((tailpos/self.maxstrlen) * ascii85lines(self.maxstrlen) +
                        ascii85lines(datalen-tailpos)))
            file.write("[ ")
            for i in xrange(0, tailpos, self.maxstrlen):
                file.write("<~")
                ascii85stream(file, self.data[i: i+self.maxstrlen])
                file.write("~>\n")
            if datalen != tailpos:
                file.write("<~")
                ascii85stream(file, self.data[tailpos:])
                file.write("~>")
            file.write("]\n"
                       "%%EndData\n")
        file.write("/%s exch def\n" % self.id)
        file.write("%%EndRessource\n")


class PDFimagepalettedata(pdfwriter.PDFobject):

    def __init__(self, name, data):
        pdfwriter.PDFobject.__init__(self, "imagepalettedata", name)
        self.data = data

    def write(self, file, writer, registry):
        file.write("<<\n"
                   "/Length %d\n" % len(self.data))
        file.write(">>\n"
                   "stream\n")
        file.write(self.data)
        file.write("\n"
                   "endstream\n")


class PDFimage(pdfwriter.PDFobject):

    def __init__(self, name, width, height, palettecolorspace, palettedata, colorspace,
                       bitspercomponent, compressmode, data, registry):
        if palettedata is not None:
            procset = "ImageI"
        elif colorspace == "/DeviceGray":
            procset = "ImageB"
        else:
            procset = "ImageC"
        pdfwriter.PDFobject.__init__(self, "image", name)
        registry.addresource("XObject", name, self, procset=procset)
        if palettedata is not None:
            # acrobat wants a palette to be an object
            self.PDFpalettedata = PDFimagepalettedata(name, palettedata)
            registry.add(self.PDFpalettedata)
        self.name = name
        self.width = width
        self.height = height
        self.palettecolorspace = palettecolorspace
        self.palettedata = palettedata
        self.colorspace = colorspace
        self.bitspercomponent = bitspercomponent
        self.compressmode = compressmode
        self.data = data

    def write(self, file, writer, registry):
        file.write("<<\n"
                   "/Type /XObject\n"
                   "/Subtype /Image\n"
                   "/Width %d\n" % self.width)
        file.write("/Height %d\n" % self.height)
        if self.palettedata is not None:
            file.write("/ColorSpace [ /Indexed %s %i\n" % (self.palettecolorspace, len(self.palettedata)/3-1))
            file.write("%d 0 R\n" % registry.getrefno(self.PDFpalettedata))
            file.write("]\n")
        else:
            file.write("/ColorSpace %s\n" % self.colorspace)
        file.write("/BitsPerComponent %d\n" % self.bitspercomponent)
        file.write("/Length %d\n" % len(self.data))
        if self.compressmode:
            file.write("/Filter /%sDecode\n" % self.compressmode)
        file.write(">>\n"
                   "stream\n")
        file.write(self.data)
        file.write("\n"
                   "endstream\n")


class bitmap(canvas.canvasitem):

    def __init__(self, xpos, ypos, image, width=None, height=None, ratio=None,
                       PSstoreimage=0, PSmaxstrlen=4093, PSbinexpand=1,
                       compressmode="Flate", flatecompresslevel=6,
                       dctquality=75, dctoptimize=0, dctprogression=0):
        # keep a copy of the image instance to ensure different id's
        self.image = image

        self.xpos = xpos
        self.ypos = ypos
        self.imagewidth, self.imageheight = image.size
        self.PSstoreimage = PSstoreimage
        self.PSmaxstrlen = PSmaxstrlen
        self.PSbinexpand = PSbinexpand

        if width is not None or height is not None:
            self.width = width
            self.height = height
            if self.width is None:
                if ratio is None:
                    self.width = self.height * self.imagewidth / float(self.imageheight)
                else:
                    self.width = ratio * self.height
            elif self.height is None:
                if ratio is None:
                    self.height = self.width * self.imageheight / float(self.imagewidth)
                else:
                    self.height = (1.0/ratio) * self.width
            elif ratio is not None:
                raise ValueError("can't specify a ratio when setting width and height")
        else:
            if ratio is not None:
                raise ValueError("must specify width or height to set a ratio")
            widthdpi, heightdpi = image.info["dpi"] # fails when no dpi information available
            self.width = self.imagewidth / float(widthdpi) * unit.t_inch
            self.height = self.imageheight / float(heightdpi) * unit.t_inch

        self.xpos_pt = unit.topt(self.xpos)
        self.ypos_pt = unit.topt(self.ypos)
        self.width_pt = unit.topt(self.width)
        self.height_pt = unit.topt(self.height)

        # create decode and colorspace
        self.colorspace = self.palettecolorspace = self.palettedata = None
        if image.mode == "P":
            palettemode, self.palettedata = image.palette.getdata()
            self.decode = "[0 255]"
            try:
                self.palettecolorspace = {"L": "/DeviceGray",
                                          "RGB": "/DeviceRGB",
                                          "CMYK": "/DeviceCMYK"}[palettemode]
            except KeyError:
                warnings.warn("image with unknown palette mode '%s' converted to rgb image" % palettemode)
                image = image.convert("RGB")
                self.decode = "[0 1 0 1 0 1]"
                self.palettedata = None
                self.colorspace = "/DeviceRGB"
        elif len(image.mode) == 1:
            if image.mode != "L":
                image = image.convert("L")
                warnings.warn("specific single channel image mode not natively supported, converted to regular grayscale")
            self.decode = "[0 1]"
            self.colorspace = "/DeviceGray"
        elif image.mode == "CMYK":
            self.decode = "[0 1 0 1 0 1 0 1]"
            self.colorspace = "/DeviceCMYK"
        else:
            if image.mode != "RGB":
                image = image.convert("RGB")
                warnings.warn("image with unknown mode converted to rgb")
            self.decode = "[0 1 0 1 0 1]"
            self.colorspace = "/DeviceRGB"

        # create imagematrix
        self.imagematrixPS = (trafo.mirror(0)
                              .translated_pt(-self.xpos_pt, self.ypos_pt+self.height_pt)
                              .scaled_pt(self.imagewidth/self.width_pt, self.imageheight/self.height_pt))
        self.imagematrixPDF = (trafo.scale_pt(self.width_pt, self.height_pt)
                               .translated_pt(self.xpos_pt, self.ypos_pt))

        # check whether imagedata is compressed or not
        try:
            imagecompressed = image.compressed
        except:
            imagecompressed = None
        if compressmode != None and imagecompressed != None:
            raise ValueError("compression of a compressed image not supported")
        self.compressmode = compressmode
        if compressmode is not None and compressmode not in ["Flate", "DCT"]:
                raise ValueError("invalid compressmode '%s'" % compressmode)
        if imagecompressed is not None:
            self.compressmode = imagecompressed
            if imagecompressed not in ["Flate", "DCT"]:
                raise ValueError("invalid compressed image '%s'" % imagecompressed)
        if not haszlib and compressmode == "Flate":
            warnings.warn("zlib module not available, disable compression")
            self.compressmode = compressmode = None

        # create data
        if compressmode == "Flate":
            self.data = zlib.compress(image.tostring(), flatecompresslevel)
        elif compressmode == "DCT":
            self.data = image.tostring("jpeg", image.mode,
                                       dctquality, dctoptimize, dctprogression)
        else:
            self.data = image.tostring()

        self.PSsinglestring = self.PSstoreimage and len(self.data) < self.PSmaxstrlen
        if self.PSsinglestring:
            self.PSimagename = "image-%d-%s-singlestring" % (id(image), compressmode)
        else:
            self.PSimagename = "image-%d-%s-stringarray" % (id(image), compressmode)
        self.PDFimagename = "image-%d-%s" % (id(image), compressmode)

    def bbox(self):
        return bbox.bbox_pt(self.xpos_pt, self.ypos_pt,
                            self.xpos_pt+self.width_pt, self.ypos_pt+self.height_pt)

    def processPS(self, file, writer, context, registry, bbox):
        if self.PSstoreimage and not self.PSsinglestring:
            registry.add(pswriter.PSdefinition("imagedataaccess",
                                               "{ /imagedataindex load " # get list index
                                               "dup 1 add /imagedataindex exch store " # store increased index
                                               "/imagedataid load exch get }")) # select string from array
        if self.PSstoreimage:
            registry.add(PSimagedata(self.PSimagename, self.data, self.PSsinglestring, self.PSmaxstrlen))
        bbox += self.bbox()

        file.write("gsave\n")
        if self.palettedata is not None:
            file.write("[ /Indexed %s %i\n" % (self.palettecolorspace, len(self.palettedata)/3-1))
            file.write("%%%%BeginData: %i ASCII Lines\n" % ascii85lines(len(self.palettedata)))
            file.write("<~")
            ascii85stream(file, self.palettedata)
            file.write("~>\n"
                       "%%EndData\n")
            file.write("] setcolorspace\n")
        else:
            file.write("%s setcolorspace\n" % self.colorspace)

        if self.PSstoreimage and not self.PSsinglestring:
            file.write("/imagedataindex 0 store\n" # not use the stack since interpreters differ in their stack usage
                       "/imagedataid %s store\n" % self.PSimagename)

        file.write("<<\n"
                   "/ImageType 1\n"
                   "/Width %i\n" % self.imagewidth)
        file.write("/Height %i\n" % self.imageheight)
        file.write("/BitsPerComponent 8\n"
                   "/ImageMatrix %s\n" % self.imagematrixPS)
        file.write("/Decode %s\n" % self.decode)

        file.write("/DataSource ")
        if self.PSstoreimage:
            if self.PSsinglestring:
                file.write("/%s load" % self.PSimagename)
            else:
                file.write("/imagedataaccess load") # some printers do not allow for inline code here -> we store it in a resource
        else:
            if self.PSbinexpand == 2:
                file.write("currentfile /ASCIIHexDecode filter")
            else:
                file.write("currentfile /ASCII85Decode filter")
        if self.compressmode:
            file.write(" /%sDecode filter" % self.compressmode)
        file.write("\n")

        file.write(">>\n")

        if self.PSstoreimage:
            file.write("image\n")
        else:
            if self.PSbinexpand == 2:
                file.write("%%%%BeginData: %i ASCII Lines\n"
                           "image\n" % (asciihexlines(len(self.data)) + 1))
                asciihexstream(file, self.data)
            else:
                # the datasource is currentstream (plus some filters)
                file.write("%%%%BeginData: %i ASCII Lines\n"
                           "image\n" % (ascii85lines(len(self.data)) + 1))
                ascii85stream(file, self.data)
                file.write("~>\n")
            file.write("%%EndData\n")

        file.write("grestore\n")

    def processPDF(self, file, writer, context, registry, bbox):
        registry.add(PDFimage(self.PDFimagename, self.imagewidth, self.imageheight,
                              self.palettecolorspace, self.palettedata, self.colorspace,
                              8, self.compressmode, self.data, registry))
        bbox += self.bbox()

        file.write("q\n")
        self.imagematrixPDF.processPDF(file, writer, context, registry, bbox)
        file.write("/%s Do\n" % self.PDFimagename)
        file.write("Q\n")
