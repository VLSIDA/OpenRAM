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

import cStringIO, warnings
import bbox, pswriter, pdfwriter, trafo, style, unit


class paperformat:

    def __init__(self, width, height, name=None):
        self.width = width
        self.height = height
        self.name = name

paperformat.A4 = paperformat(210 * unit.t_mm, 297  * unit.t_mm, "A4")
paperformat.A3 = paperformat(297 * unit.t_mm, 420  * unit.t_mm, "A3")
paperformat.A2 = paperformat(420 * unit.t_mm, 594  * unit.t_mm, "A2")
paperformat.A1 = paperformat(594 * unit.t_mm, 840  * unit.t_mm, "A1")
paperformat.A0 = paperformat(840 * unit.t_mm, 1188 * unit.t_mm, "A0")
paperformat.A0b = paperformat(910 * unit.t_mm, 1370 * unit.t_mm, None) # dedicated to our friends in Augsburg
paperformat.Letter = paperformat(8.5 * unit.t_inch, 11 * unit.t_inch, "Letter")
paperformat.Legal = paperformat(8.5 * unit.t_inch, 14 * unit.t_inch, "Legal")

def _paperformatfromstring(name):
    return getattr(paperformat, name.capitalize())


class page:

    def __init__(self, canvas, pagename=None, paperformat=None, rotated=0, centered=1, fittosize=0,
                 margin=1*unit.t_cm, bboxenlarge=1*unit.t_pt, bbox=None):
        self.canvas = canvas
        self.pagename = pagename
        # support for depricated string specification of paper formats
        try:
            paperformat + ""
        except:
            self.paperformat = paperformat
        else:
            self.paperformat = _paperformatfromstring(paperformat)
            warnings.warn("specification of paperformat by string is deprecated, use document.paperformat.%s instead" % paperformat.capitalize(), DeprecationWarning)

        self.rotated = rotated
        self.centered = centered
        self.fittosize = fittosize
        self.margin = margin
        self.bboxenlarge = bboxenlarge
        self.pagebbox = bbox

    def _process(self, processMethod, contentfile, writer, context, registry, bbox):
        assert not bbox

        # check whether we expect a page trafo and use a temporary canvasfile to insert the
        # pagetrafo in front after the bbox was calculated
        expectpagetrafo = self.paperformat and (self.rotated or self.centered or self.fittosize)
        if expectpagetrafo:
            canvasfile = cStringIO.StringIO()
        else:
            canvasfile = contentfile

        getattr(style.linewidth.normal, processMethod)(canvasfile, writer, context, registry, bbox)
        getattr(self.canvas, processMethod)(canvasfile, writer, context, registry, bbox)

        # usually its the bbox of the canvas enlarged by self.bboxenlarge, but
        # it might be a different bbox as specified in the page constructor
        if self.pagebbox:
            bbox.set(self.pagebbox)
        elif bbox:
            bbox.enlarge(self.bboxenlarge)

        if expectpagetrafo:

            if bbox:
                # calculate the pagetrafo
                paperwidth, paperheight = self.paperformat.width, self.paperformat.height

                # center (optionally rotated) output on page
                if self.rotated:
                    pagetrafo = trafo.rotate(90).translated(paperwidth, 0)
                    if self.centered or self.fittosize:
                        if not self.fittosize and (bbox.height() > paperwidth or bbox.width() > paperheight):
                            warnings.warn("content exceeds the papersize")
                        pagetrafo = pagetrafo.translated(-0.5*(paperwidth - bbox.height()) + bbox.bottom(),
                                                          0.5*(paperheight - bbox.width()) - bbox.left())
                else:
                    if not self.fittosize and (bbox.width() > paperwidth or bbox.height() > paperheight):
                        warnings.warn("content exceeds the papersize")
                    pagetrafo = trafo.translate(0.5*(paperwidth - bbox.width())  - bbox.left(),
                                                0.5*(paperheight - bbox.height()) - bbox.bottom())

                if self.fittosize:

                    if 2*self.margin > paperwidth or 2*self.margin > paperheight:
                        raise ValueError("Margins too broad for selected paperformat. Aborting.")

                    paperwidth -= 2 * self.margin
                    paperheight -= 2 * self.margin

                    # scale output to pagesize - margins
                    if self.rotated:
                        sfactor = min(unit.topt(paperheight)/bbox.width_pt(), unit.topt(paperwidth)/bbox.height_pt())
                    else:
                        sfactor = min(unit.topt(paperwidth)/bbox.width_pt(), unit.topt(paperheight)/bbox.height_pt())

                    pagetrafo = pagetrafo.scaled(sfactor, sfactor, self.margin + 0.5*paperwidth, self.margin + 0.5*paperheight)

                # apply the pagetrafo and write it to the contentfile
                bbox.transform(pagetrafo)
                pagetrafofile = cStringIO.StringIO()
                # context, bbox, registry are just passed as stubs (the trafo should not touch them)
                getattr(pagetrafo, processMethod)(pagetrafofile, writer, context, registry, bbox)
                contentfile.write(pagetrafofile.getvalue())
                pagetrafofile.close()

            contentfile.write(canvasfile.getvalue())
            canvasfile.close()

    def processPS(self, *args):
        self._process("processPS", *args)

    def processPDF(self, *args):
        self._process("processPDF", *args)


class document:

    """holds a collection of page instances which are output as pages of a document"""

    def __init__(self, pages=[]):
        self.pages = pages

    def append(self, page):
        self.pages.append(page)

    def writeEPSfile(self, file, *args, **kwargs):
        pswriter.epswriter(self, file, *args, **kwargs)

    def writePSfile(self, file, *args, **kwargs):
        pswriter.pswriter(self, file, *args, **kwargs)

    def writePDFfile(self, file, *args, **kwargs):
        pdfwriter.PDFwriter(self, file, *args, **kwargs)

    def writetofile(self, filename, *args, **kwargs):
        if filename.endswith(".eps"):
            self.writeEPSfile(filename, *args, **kwargs)
        elif filename.endswith(".ps"):
            self.writePSfile(filename, *args, **kwargs)
        elif filename.endswith(".pdf"):
            self.writePDFfile(filename, *args, **kwargs)
        else:
            raise ValueError("unknown file extension")
