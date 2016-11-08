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

import cStringIO, copy, time, math
import bbox, style, version, type1font, unit, trafo

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


class PSregistry:

    def __init__(self):
        # in order to keep a consistent order of the registered resources we
        # not only store them in a hash but also keep an ordered list (up to a
        # possible merging of resources, in which case the first instance is
        # kept)
        self.resourceshash = {}
        self.resourceslist = []

    def add(self, resource):
        rkey = (resource.type, resource.id)
        if self.resourceshash.has_key(rkey):
           self.resourceshash[rkey].merge(resource)
        else:
           self.resourceshash[rkey] = resource
           self.resourceslist.append(resource)

    def mergeregistry(self, registry):
        for resource in registry.resources:
            self.add(resource)

    def output(self, file, writer):
        """ write all PostScript code of the prolog resources """
        for resource in self.resourceslist:
            resource.output(file, writer, self)

#
# Abstract base class
#

class PSresource:

    """ a PostScript resource """

    def __init__(self, type, id):
        # Every PSresource has to have a type and a unique id.
        # Resources with the same type and id will be merged
        # when they are registered in the PSregistry
        self.type = type
        self.id = id

    def merge(self, other):
        """ merge self with other, which has to be a resource of the same type and with
        the same id"""
        pass

    def output(self, file, writer, registry):
        raise NotImplementedError("output not implemented for %s" % repr(self))

#
# Different variants of prolog items
#

class PSdefinition(PSresource):

    """ PostScript function definition included in the prolog """

    def __init__(self, id, body):
        self.type = "definition"
        self.id = id
        self.body = body

    def output(self, file, writer, registry):
        file.write("%%%%BeginRessource: %s\n" % self.id)
        file.write("%(body)s /%(id)s exch def\n" % self.__dict__)
        file.write("%%EndRessource\n")


class PSfont:

    def __init__(self, font, chars, registry):
        if font.filename:
            registry.add(PSfontfile(font.basefontname,
                                    font.filename,
                                    font.encoding,
                                    chars))
        if font.encoding and font.slant:
            assert font.encname
            # do first the reencoding and then the slanting:
            enc_basename, enc_finalname = font.basefontname, font.encname
            slt_basename, slt_finalname = tfont.encname, font.name
        elif font.encoding:
            enc_basename, enc_finalname = font.basefontname, font.name
        elif font.slant:
            slt_basename, slt_finalname = font.basefontname, font.name

        if font.encoding:
            registry.add(_ReEncodeFont)
            registry.add(PSfontencoding(font.encoding))
            registry.add(PSfontreencoding(enc_finalname, enc_basename, font.encoding.name))

        if font.slant:
            # we need the current fontmatrix in order to manipulate it:
            # for this we need to re-read the fontfile as below in
            # PSfontfile.ouput:
            # XXX Is there a better way to do this?
            t = trafo.trafo_pt(matrix=((1, font.slant), (0, 1)))
            if font.filename:
                # for the builtin fonts, we assume a trivial fontmatrix
                import font.t1font as t1fontmodule
                t1font = t1fontmodule.T1pfbfont(font.filename)
                m = t1font.fontmatrixpattern.search(t1font.data1)
                m11, m12, m21, m22, v1, v2 = map(float, m.groups()[:6])
                t *= trafo.trafo_pt(matrix=((m11, m12), (m21, m22)), vector=(v1, v2))
            else:
                raise NotImplementedError(
                "cannot slant unembedded fonts -- try to include \"download35.map\" in fontmaps")
            registry.add(PSfontslanting(slt_finalname, slt_basename, t.__str__()))


class PSfontfile(PSresource):

    """ PostScript font definition included in the prolog """

    def __init__(self, name, filename, encoding, chars):
        """ include type 1 font defined by the following parameters

        - name:        name of the PostScript font
        - filename:    name (without path) of file containing the font definition
        - encfilename: name (without path) of file containing used encoding of font
                       or None (if no encoding file used)
        - chars:       character list to fill usedchars

        """

        # Note that here we only need the encoding for selecting the used glyphs!

        self.type = "fontfile"
        self.id = self.name = name
        self.filename = filename
        if encoding is None:
            self.encodingfilename = None
        else:
            self.encodingfilename = encoding.filename
        self.usedchars = {}
        for char in chars:
            self.usedchars[char] = 1

        self.strip = 1

    def merge(self, other):
        if self.encodingfilename == other.encodingfilename:
            self.usedchars.update(other.usedchars)
        else:
            # TODO: need to resolve the encoding when several encodings are in the play
            self.strip = 0

    def output(self, file, writer, registry):
        import font.t1font
        font = font.t1font.T1pfbfont(self.filename)

        file.write("%%%%BeginFont: %s\n" % self.name)
        # file.write("%%Included glyphs: %s\n" % " ".join(usedglyphs))
        if self.strip:
            # XXX: access to the encoding file
            if self.encodingfilename:
                encodingfile = type1font.encodingfile(self.encodingfilename, self.encodingfilename)
                usedglyphs = dict([(encodingfile.decode(char)[1:], 1) for char in self.usedchars.keys()])
            else:
                font._encoding()
                usedglyphs = dict([(font.encoding.decode(char), 1) for char in self.usedchars.keys()])
            strippedfont = font.getstrippedfont(usedglyphs)
        else:
            strippedfont = font
        strippedfont.outputPS(file, writer)
        file.write("\n%%EndFont\n")


class PSfontencoding(PSresource):

    """ PostScript font encoding vector included in the prolog """

    def __init__(self, encoding):
        """ include font encoding vector specified by encoding """

        self.type = "fontencoding"
        self.id = encoding.name
        self.encoding = encoding

    def output(self, file, writer, registry):
        encodingfile = type1font.encodingfile(self.encoding.name, self.encoding.filename)
        encodingfile.outputPS(file, writer)


class PSfontslanting(PSresource):

    """ PostScript font slanting directive included in the prolog """

    def __init__(self, fontname, basefontname, matrixstring):
        """ include transformed font directive specified by

        - fontname:     PostScript FontName of the new slanted font
        - basefontname: PostScript FontName of the original font
        - slant:        the value of slanting
        """

        self.type = "fontslanting"
        self.id = self.fontname = fontname
        self.basefontname = basefontname
        self.matrixstring = matrixstring

    def output(self, file, writer, registry):
        file.write("%%%%BeginProcSet: %s\n" % self.fontname)
        file.write("/%s findfont\n" % self.basefontname)
        file.write("dup length dict begin\n")
        file.write("{ 1 index /FID ne {def} {pop pop} ifelse } forall\n")
        file.write("/FontMatrix %s readonly def\n" % self.matrixstring)
        file.write("currentdict\n")
        file.write("end\n")
        file.write("/%s exch definefont pop\n" % self.fontname)
        file.write("%%EndProcSet\n")

class PSfontreencoding(PSresource):

    """ PostScript font re-encoding directive included in the prolog """

    def __init__(self, fontname, basefontname, encodingname):
        """ include font re-encoding directive specified by

        - fontname:     PostScript FontName of the new reencoded font
        - basefontname: PostScript FontName of the original font
        - encname:      name of the encoding

        Before being able to reencode a font, you have to include the
        encoding via a fontencoding prolog item with name=encname

        """

        self.type = "fontreencoding"
        self.id = self.fontname = fontname
        self.basefontname = basefontname
        self.encodingname = encodingname

    def output(self, file, writer, registry):
        file.write("%%%%BeginProcSet: %s\n" % self.fontname)
        file.write("/%s /%s %s ReEncodeFont\n" % (self.basefontname, self.fontname, self.encodingname))
        file.write("%%EndProcSet\n")


_ReEncodeFont = PSdefinition("ReEncodeFont", """{
  5 dict
  begin
    /newencoding exch def
    /newfontname exch def
    /basefontname exch def
    /basefontdict basefontname findfont def
    /newfontdict basefontdict maxlength dict def
    basefontdict {
      exch dup dup /FID ne exch /Encoding ne and
      { exch newfontdict 3 1 roll put }
      { pop pop }
      ifelse
    } forall
    newfontdict /FontName newfontname put
    newfontdict /Encoding newencoding put
    newfontname newfontdict definefont pop
  end
}""")


class epswriter:

    def __init__(self, document, file):
        if len(document.pages) != 1:
            raise ValueError("EPS file can be constructed out of a single page document only")
        page = document.pages[0]
        canvas = page.canvas

        try:
            file.write("")
        except:
            filename = file
            if not filename.endswith(".eps"):
                filename += ".eps"
            try:
                file = open(filename, "w")
            except IOError:
                raise IOError("cannot open output file")
        else:
            filename = "stream"

        pagefile = cStringIO.StringIO()
        registry = PSregistry()
        acontext = context()
        pagebbox = bbox.empty()

        page.processPS(pagefile, self, acontext, registry, pagebbox)

        file.write("%!PS-Adobe-3.0 EPSF-3.0\n")
        if pagebbox:
            file.write("%%%%BoundingBox: %d %d %d %d\n" % pagebbox.lowrestuple_pt())
            file.write("%%%%HiResBoundingBox: %g %g %g %g\n" % pagebbox.highrestuple_pt())
        file.write("%%%%Creator: PyX %s\n" % version.version)
        file.write("%%%%Title: %s\n" % filename)
        file.write("%%%%CreationDate: %s\n" %
                   time.asctime(time.localtime(time.time())))
        file.write("%%EndComments\n")

        file.write("%%BeginProlog\n")
        registry.output(file, self)
        file.write("%%EndProlog\n")

        file.write(pagefile.getvalue())
        pagefile.close()

        file.write("showpage\n")
        file.write("%%Trailer\n")
        file.write("%%EOF\n")


class pswriter:

    def __init__(self, document, file, writebbox=0):
        try:
            file.write("")
        except:
            filename = file
            if not filename.endswith(".ps"):
                filename += ".ps"
            try:
                file = open(filename, "w")
            except IOError:
                raise IOError("cannot open output file")
        else:
            filename = "stream"

        # We first have to process the content of the pages, writing them into the stream pagesfile
        # Doing so, we fill the registry and also calculate the page bounding boxes, which are
        # stored in page._bbox for every page
        pagesfile = cStringIO.StringIO()
        registry = PSregistry()

        # calculated bounding boxes of the whole document
        documentbbox = bbox.empty()

        for nr, page in enumerate(document.pages):
            # process contents of page
            pagefile = cStringIO.StringIO()
            acontext = context()
            pagebbox = bbox.empty()
            page.processPS(pagefile, self, acontext, registry, pagebbox)

            documentbbox += pagebbox

            pagesfile.write("%%%%Page: %s %d\n" % (page.pagename is None and str(nr+1) or page.pagename, nr+1))
            if page.paperformat:
                pagesfile.write("%%%%PageMedia: %s\n" % page.paperformat.name)
            pagesfile.write("%%%%PageOrientation: %s\n" % (page.rotated and "Landscape" or "Portrait"))
            if pagebbox and writebbox:
                pagesfile.write("%%%%PageBoundingBox: %d %d %d %d\n" % pagebbox.lowrestuple_pt())

            # page setup section
            pagesfile.write("%%BeginPageSetup\n")
            pagesfile.write("/pgsave save def\n")

            pagesfile.write("%%EndPageSetup\n")
            pagesfile.write(pagefile.getvalue())
            pagefile.close()
            pagesfile.write("pgsave restore\n")
            pagesfile.write("showpage\n")
            pagesfile.write("%%PageTrailer\n")

        file.write("%!PS-Adobe-3.0\n")
        if documentbbox and writebbox:
            file.write("%%%%BoundingBox: %d %d %d %d\n" % documentbbox.lowrestuple_pt())
            file.write("%%%%HiResBoundingBox: %g %g %g %g\n" % documentbbox.highrestuple_pt())
        file.write("%%%%Creator: PyX %s\n" % version.version)
        file.write("%%%%Title: %s\n" % filename)
        file.write("%%%%CreationDate: %s\n" %
                   time.asctime(time.localtime(time.time())))

        # required paper formats
        paperformats = {}
        for page in document.pages:
            if page.paperformat:
                paperformats[page.paperformat] = page.paperformat

        first = 1
        for paperformat in paperformats.values():
            if first:
                file.write("%%DocumentMedia: ")
                first = 0
            else:
                file.write("%%+ ")
            file.write("%s %d %d 75 white ()\n" % (paperformat.name,
                                                   unit.topt(paperformat.width),
                                                   unit.topt(paperformat.height)))

        # file.write(%%DocumentNeededResources: ") # register not downloaded fonts here

        file.write("%%%%Pages: %d\n" % len(document.pages))
        file.write("%%PageOrder: Ascend\n")
        file.write("%%EndComments\n")

        # document defaults section
        #file.write("%%BeginDefaults\n")
        #file.write("%%EndDefaults\n")

        # document prolog section
        file.write("%%BeginProlog\n")
        registry.output(file, self)
        file.write("%%EndProlog\n")

        # document setup section
        #file.write("%%BeginSetup\n")
        #file.write("%%EndSetup\n")

        file.write(pagesfile.getvalue())
        pagesfile.close()

        file.write("%%Trailer\n")
        file.write("%%EOF\n")

class context:

    def __init__(self):
        self.linewidth_pt = None
        self.colorspace = None
        self.font = None

    def __call__(self, **kwargs):
        newcontext = copy.copy(self)
        for key, value in kwargs.items():
            setattr(newcontext, key, value)
        return newcontext
