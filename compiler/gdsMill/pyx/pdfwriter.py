# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2005-2006 Jörg Lehmann <joergl@users.sourceforge.net>
# Copyright (C) 2005-2006 André Wobst <wobsta@users.sourceforge.net>
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

import cStringIO, copy, warnings, time
try:
    import zlib
    haszlib = 1
except:
    haszlib = 0

import bbox, unit, style, type1font, version

try:
    enumerate([])
except NameError:
    # fallback implementation for Python 2.2 and below
    def enumerate(list):
        return zip(xrange(len(list)), list)

try:
    dict([])
except NameError:
    # fallback implementation for Python 2.1
    def dict(list):
        result = {}
        for key, value in list:
            result[key] = value
        return result


class PDFregistry:

    def __init__(self):
        self.types = {}
        # we want to keep the order of the resources
        self.objects = []
        self.resources = {}
        self.procsets = {"PDF": 1}
        self.merged = None

    def add(self, object):
        """ register object, merging it with an already registered object of the same type and id """
        sameobjects = self.types.setdefault(object.type, {})
        if sameobjects.has_key(object.id):
            sameobjects[object.id].merge(object)
        else:
            self.objects.append(object)
            sameobjects[object.id] = object

    def getrefno(self, object):
        if self.merged:
            return self.merged.getrefno(object)
        else:
            return self.types[object.type][object.id].refno

    def mergeregistry(self, registry):
        for object in registry.objects:
            self.add(object)
        registry.merged = self

    def write(self, file, writer, catalog):
        # first we set all refnos
        refno = 1
        for object in self.objects:
            object.refno = refno
            refno += 1

        # second, all objects are written, keeping the positions in the output file
        fileposes = []
        for object in self.objects:
            fileposes.append(file.tell())
            file.write("%i 0 obj\n" % object.refno)
            object.write(file, writer, self)
            file.write("endobj\n")

        # xref
        xrefpos = file.tell()
        file.write("xref\n"
                   "0 %d\n"
                   "0000000000 65535 f \n" % refno)

        for filepos in fileposes:
            file.write("%010i 00000 n \n" % filepos)

        # trailer
        file.write("trailer\n"
                   "<<\n"
                   "/Size %i\n" % refno)
        file.write("/Root %i 0 R\n" % self.getrefno(catalog))
        file.write("/Info %i 0 R\n" % self.getrefno(catalog.PDFinfo))
        file.write(">>\n"
                   "startxref\n"
                   "%i\n" % xrefpos)
        file.write("%%EOF\n")

    def addresource(self, resourcetype, resourcename, object, procset=None):
        self.resources.setdefault(resourcetype, {})[resourcename] = object
        if procset:
            self.procsets[procset] = 1

    def writeresources(self, file):
        file.write("/Resources <<\n")
        file.write("/ProcSet [ %s ]\n" % " ".join(["/%s" % p for p in self.procsets.keys()]))
        if self.resources:
            for resourcetype, resources in self.resources.items():
                file.write("/%s <<\n%s\n>>\n" % (resourcetype, "\n".join(["/%s %i 0 R" % (name, self.getrefno(object))
                                                                          for name, object in resources.items()])))
        file.write(">>\n")


class PDFobject:

    def __init__(self, type, _id=None):
        """create a PDFobject
          - type has to be a string describing the type of the object
          - _id is a unique identification used for the object if it is not None.
            Otherwise id(self) is used
        """
        self.type = type
        if _id is None:
            self.id = id(self)
        else:
            self.id = _id

    def merge(self, other):
        pass

    def write(self, file, writer, registry):
        raise NotImplementedError("write method has to be provided by PDFobject subclass")


class PDFcatalog(PDFobject):

    def __init__(self, document, writer, registry):
        PDFobject.__init__(self, "catalog")
        self.PDFpages = PDFpages(document, writer, registry)
        registry.add(self.PDFpages)
        self.PDFinfo = PDFinfo()
        registry.add(self.PDFinfo)

    def write(self, file, writer, registry):
        file.write("<<\n"
                   "/Type /Catalog\n"
                   "/Pages %i 0 R\n" % registry.getrefno(self.PDFpages))
        if writer.fullscreen:
            file.write("/PageMode /FullScreen\n")
        file.write(">>\n")


class PDFinfo(PDFobject):

    def __init__(self):
        PDFobject.__init__(self, "info")

    def write(self, file, writer, registry):
        if time.timezone < 0:
            # divmod on positive numbers, otherwise the minutes have a different sign from the hours
            timezone = "-%02i'%02i'" % divmod(-time.timezone/60, 60)
        elif time.timezone > 0:
            timezone = "+%02i'%02i'" % divmod(time.timezone/60, 60)
        else:
            timezone = "Z00'00'"

        def pdfstring(s):
            r = ""
            for c in s:
                if 32 <= ord(c) <= 127 and c not in "()[]<>\\":
                    r += c
                else:
                    r += "\\%03o" % ord(c)
            return r

        file.write("<<\n")
        if writer.title:
            file.write("/Title (%s)\n" % pdfstring(writer.title))
        if writer.author:
            file.write("/Author (%s)\n" % pdfstring(writer.author))
        if writer.subject:
            file.write("/Subject (%s)\n" % pdfstring(writer.subject))
        if writer.keywords:
            file.write("/Keywords (%s)\n" % pdfstring(writer.keywords))
        file.write("/Creator (PyX %s)\n" % version.version)
        file.write("/CreationDate (D:%s%s)\n" % (time.strftime("%Y%m%d%H%M"), timezone))
        file.write(">>\n")


class PDFpages(PDFobject):

    def __init__(self, document, writer, registry):
        PDFobject.__init__(self, "pages")
        self.PDFpagelist = []
        for pageno, page in enumerate(document.pages):
            page = PDFpage(page, pageno, self, writer, registry)
            registry.add(page)
            self.PDFpagelist.append(page)

    def write(self, file, writer, registry):
        file.write("<<\n"
                   "/Type /Pages\n"
                   "/Kids [%s]\n"
                   "/Count %i\n"
                   ">>\n" % (" ".join(["%i 0 R" % registry.getrefno(page)
                                       for page in self.PDFpagelist]),
                             len(self.PDFpagelist)))


class PDFpage(PDFobject):

    def __init__(self, page, pageno, PDFpages, writer, registry):
        PDFobject.__init__(self, "page")
        self.PDFpages = PDFpages
        self.page = page

        # every page uses its own registry in order to find out which
        # resources are used within the page. However, the
        # pageregistry is also merged in the global registry
        self.pageregistry = PDFregistry()

        self.PDFcontent = PDFcontent(page, writer, self.pageregistry)
        self.pageregistry.add(self.PDFcontent)
        registry.mergeregistry(self.pageregistry)

    def write(self, file, writer, registry):
        file.write("<<\n"
                   "/Type /Page\n"
                   "/Parent %i 0 R\n" % registry.getrefno(self.PDFpages))
        paperformat = self.page.paperformat
        if paperformat:
            file.write("/MediaBox [0 0 %f %f]\n" % (unit.topt(paperformat.width), unit.topt(paperformat.height)))
        else:
            file.write("/MediaBox [%f %f %f %f]\n" % self.PDFcontent.bbox.highrestuple_pt())
        if self.PDFcontent.bbox and writer.writebbox:
            file.write("/CropBox [%f %f %f %f]\n" % self.PDFcontent.bbox.highrestuple_pt())
        if self.page.rotated:
            file.write("/Rotate 90\n")
        file.write("/Contents %i 0 R\n" % registry.getrefno(self.PDFcontent))
        self.pageregistry.writeresources(file)
        file.write(">>\n")


class PDFcontent(PDFobject):

    def __init__(self, page, writer, registry):
        PDFobject.__init__(self, registry, "content")
        contentfile = cStringIO.StringIO()
        self.bbox = bbox.empty()
        acontext = context()
        page.processPDF(contentfile, writer, acontext, registry, self.bbox)
        self.content = contentfile.getvalue()
        contentfile.close()

    def write(self, file, writer, registry):
        if writer.compress:
            content = zlib.compress(self.content)
        else:
            content = self.content
        file.write("<<\n"
                   "/Length %i\n" % len(content))
        if writer.compress:
            file.write("/Filter /FlateDecode\n")
        file.write(">>\n"
                   "stream\n")
        file.write(content)
        file.write("endstream\n")


class PDFfont(PDFobject):

    def __init__(self, font, chars, writer, registry):
        PDFobject.__init__(self, "font", font.name)
        registry.addresource("Font", font.name, self, procset="Text")

        self.fontdescriptor = PDFfontdescriptor(font, chars, writer, registry)
        registry.add(self.fontdescriptor)

        if font.encoding:
            self.encoding = PDFencoding(font.encoding, writer, registry)
            registry.add(self.encoding)
        else:
            self.encoding = None

        self.name = font.name
        self.basefontname = font.basefontname
        self.metric = font.metric

    def write(self, file, writer, registry):
        file.write("<<\n"
                   "/Type /Font\n"
                   "/Subtype /Type1\n")
        file.write("/Name /%s\n" % self.name)
        file.write("/BaseFont /%s\n" % self.basefontname)
        if self.fontdescriptor.fontfile is not None and self.fontdescriptor.fontfile.usedchars is not None:
            usedchars = self.fontdescriptor.fontfile.usedchars
            firstchar = min(usedchars.keys())
            lastchar = max(usedchars.keys())
            file.write("/FirstChar %d\n" % firstchar)
            file.write("/LastChar %d\n" % lastchar)
            file.write("/Widths\n"
                       "[")
            for i in range(firstchar, lastchar+1):
                if i and not (i % 8):
                    file.write("\n")
                else:
                    file.write(" ")
                if usedchars.has_key(i):
                    file.write("%f" % self.metric.getwidth_ds(i))
                else:
                    file.write("0")
            file.write(" ]\n")
        else:
            file.write("/FirstChar 0\n"
                       "/LastChar 255\n"
                       "/Widths\n"
                       "[")
            for i in range(256):
                if i and not (i % 8):
                    file.write("\n")
                else:
                    file.write(" ")
                try:
                    width = self.metric.getwidth_ds(i)
                except (IndexError, AttributeError):
                    width = 0
                file.write("%f" % width)
            file.write(" ]\n")
        file.write("/FontDescriptor %d 0 R\n" % registry.getrefno(self.fontdescriptor))
        if self.encoding:
            file.write("/Encoding %d 0 R\n" % registry.getrefno(self.encoding))
        file.write(">>\n")


class PDFfontdescriptor(PDFobject):

    def __init__(self, font, chars, writer, registry):
        PDFobject.__init__(self, "fontdescriptor", font.basefontname)

        if font.filename is None:
            self.fontfile = None
        else:
            self.fontfile = PDFfontfile(font.basefontname, font.filename, font.encoding, chars, writer, registry)
            registry.add(self.fontfile)

        self.name = font.basefontname
        self.fontinfo = font.metric.fontinfo()

    def write(self, file, writer, registry):
        file.write("<<\n"
                   "/Type /FontDescriptor\n"
                   "/FontName /%s\n" % self.name)
        if self.fontfile is None:
            file.write("/Flags 32\n")
        else:
            file.write("/Flags %d\n" % self.fontfile.getflags())
        file.write("/FontBBox [%d %d %d %d]\n" % self.fontinfo.fontbbox)
        file.write("/ItalicAngle %d\n" % self.fontinfo.italicangle)
        file.write("/Ascent %d\n" % self.fontinfo.ascent)
        file.write("/Descent %d\n" % self.fontinfo.descent)
        file.write("/CapHeight %d\n" % self.fontinfo.capheight)
        file.write("/StemV %d\n" % self.fontinfo.vstem)
        if self.fontfile is not None:
            file.write("/FontFile %d 0 R\n" % registry.getrefno(self.fontfile))
        file.write(">>\n")


class PDFfontfile(PDFobject):

    def __init__(self, name, filename, encoding, chars, writer, registry):
        PDFobject.__init__(self, "fontfile", filename)
        self.name = name
        self.filename = filename
        if encoding is None:
            self.encodingfilename = None
        else:
            self.encodingfilename = encoding.filename
        self.usedchars = {}
        for char in chars:
            self.usedchars[char] = 1

        self.strip = 1
        self.font = None

    def merge(self, other):
        if self.encodingfilename == other.encodingfilename:
            self.usedchars.update(other.usedchars)
        else:
            # TODO: need to resolve the encoding when several encodings are in the play
            self.strip = 0

    def mkfontfile(self):
        import font.t1font
        self.font = font.t1font.T1pfbfont(self.filename)

    def getflags(self):
        if self.font is None:
            self.mkfontfile()
        return self.font.getflags()

    def write(self, file, writer, registry):
        if self.font is None:
            self.mkfontfile()
        if self.strip:
            # XXX: access to the encoding file
            if self.encodingfilename:
                encodingfile = type1font.encodingfile(self.encodingfilename, self.encodingfilename)
                usedglyphs = dict([(encodingfile.decode(char)[1:], 1) for char in self.usedchars.keys()])
            else:
                self.font._encoding()
                usedglyphs = dict([(self.font.encoding.decode(char), 1) for char in self.usedchars.keys()])
            strippedfont = self.font.getstrippedfont(usedglyphs)
        else:
            strippedfont = self.font
        strippedfont.outputPDF(file, writer)


class PDFencoding(PDFobject):

    def __init__(self, encoding, writer, registry):
        PDFobject.__init__(self, "encoding", encoding.name)
        self.encoding = encoding

    def write(self, file, writer, registry):
        encodingfile = type1font.encodingfile(self.encoding.name, self.encoding.filename)
        encodingfile.outputPDF(file, writer)


class PDFwriter:

    def __init__(self, document, file,
                       title=None, author=None, subject=None, keywords=None,
                       fullscreen=0, writebbox=0, compress=1, compresslevel=6):
        try:
            file.write("")
        except:
            filename = file
            if not filename.endswith(".pdf"):
                filename += ".pdf"
            try:
                file = open(filename, "wb")
            except IOError:
                raise IOError("cannot open output file")

        self.title = title
        self.author = author
        self.subject = subject
        self.keywords = keywords
        self.fullscreen = fullscreen
        self.writebbox = writebbox
        if compress and not haszlib:
            compress = 0
            warnings.warn("compression disabled due to missing zlib module")
        self.compress = compress
        self.compresslevel = compresslevel

        # the PDFcatalog class automatically builds up the pdfobjects from a document
        registry = PDFregistry()
        catalog = PDFcatalog(document, self, registry)
        registry.add(catalog)

        file.write("%%PDF-1.4\n%%%s%s%s%s\n" % (chr(195), chr(182), chr(195), chr(169)))
        registry.write(file, self, catalog)
        file.close()


class context:

    def __init__(self):
        self.linewidth_pt = None
        # XXX there are both stroke and fill color spaces
        self.colorspace = None
        self.strokeattr = 1
        self.fillattr = 1
        self.font = None
        self.textregion = 0

    def __call__(self, **kwargs):
        newcontext = copy.copy(self)
        for key, value in kwargs.items():
            setattr(newcontext, key, value)
        return newcontext
