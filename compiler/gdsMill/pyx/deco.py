# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2002-2006 Jörg Lehmann <joergl@users.sourceforge.net>
# Copyright (C) 2003-2004 Michael Schindler <m-schindler@users.sourceforge.net>
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

# TODO:
# - should we improve on the arc length -> arg parametrization routine or
#   should we at least factor it out?

from __future__ import nested_scopes

import sys, math
import attr, canvas, color, path, normpath, style, trafo, unit

try:
    from math import radians
except ImportError:
    # fallback implementation for Python 2.1 and below
    def radians(x): return x*math.pi/180

class _marker: pass

#
# Decorated path
#

class decoratedpath(canvas.canvasitem):
    """Decorated path

    The main purpose of this class is during the drawing
    (stroking/filling) of a path. It collects attributes for the
    stroke and/or fill operations.
    """

    def __init__(self, path, strokepath=None, fillpath=None,
                 styles=None, strokestyles=None, fillstyles=None,
                 ornaments=None):

        self.path = path

        # global style for stroking and filling and subdps
        self.styles = styles

        # styles which apply only for stroking and filling
        self.strokestyles = strokestyles
        self.fillstyles = fillstyles

        # the decoratedpath can contain additional elements of the
        # path (ornaments), e.g., arrowheads.
        if ornaments is None:
            self.ornaments = canvas.canvas()
        else:
            self.ornaments = ornaments

        self.nostrokeranges = None

    def ensurenormpath(self):
        """convert self.path into a normpath"""
        assert self.nostrokeranges is None or isinstance(self.path, path.normpath), "you don't understand what you are doing"
        self.path = self.path.normpath()

    def excluderange(self, begin, end):
        assert isinstance(self.path, path.normpath), "you don't understand what this is about"
        if self.nostrokeranges is None:
            self.nostrokeranges = [(begin, end)]
        else:
            ibegin = 0
            while ibegin < len(self.nostrokeranges) and self.nostrokeranges[ibegin][1] < begin:
                ibegin += 1

            if ibegin == len(self.nostrokeranges):
                self.nostrokeranges.append((begin, end))
                return

            iend = len(self.nostrokeranges) - 1
            while 0 <= iend and end < self.nostrokeranges[iend][0]:
                iend -= 1

            if iend == -1:
                self.nostrokeranges.insert(0, (begin, end))
                return

            if self.nostrokeranges[ibegin][0] < begin:
                begin = self.nostrokeranges[ibegin][0]
            if end < self.nostrokeranges[iend][1]:
                end = self.nostrokeranges[iend][1]

            self.nostrokeranges[ibegin:iend+1] = [(begin, end)]

    def bbox(self):
        pathbbox = self.path.bbox()
        ornamentsbbox = self.ornaments.bbox()
        if ornamentsbbox is not None:
            return ornamentsbbox + pathbbox
        else:
            return pathbbox

    def strokepath(self):
        if self.nostrokeranges:
            splitlist = []
            for begin, end in self.nostrokeranges:
                splitlist.append(begin)
                splitlist.append(end)
            split = self.path.split(splitlist)
            # XXX properly handle closed paths?
            result = split[0]
            for i in range(2, len(split), 2):
                result += split[i]
            return result
        else:
            return self.path

    def processPS(self, file, writer, context, registry, bbox):
        # draw (stroke and/or fill) the decoratedpath on the canvas
        # while trying to produce an efficient output, e.g., by
        # not writing one path two times

        # small helper
        def _writestyles(styles, context, registry, bbox):
            for style in styles:
                style.processPS(file, writer, context, registry, bbox)

        if self.strokestyles is None and self.fillstyles is None:
            if not len(self.ornaments):
                raise RuntimeError("Path neither to be stroked nor filled nor decorated in another way")
            # just draw additional elements of decoratedpath
            self.ornaments.processPS(file, writer, context, registry, bbox)
            return

        strokepath = self.strokepath()
        fillpath = self.path

        # apply global styles
        if self.styles:
            file.write("gsave\n")
            context = context()
            _writestyles(self.styles, context, registry, bbox)

        if self.fillstyles is not None:
            file.write("newpath\n")
            fillpath.outputPS(file, writer)

            if self.strokestyles is not None and strokepath is fillpath:
                # do efficient stroking + filling if respective paths are identical
                file.write("gsave\n")

                if self.fillstyles:
                    _writestyles(self.fillstyles, context(), registry, bbox)

                file.write("fill\n")
                file.write("grestore\n")

                acontext = context()
                if self.strokestyles:
                    file.write("gsave\n")
                    _writestyles(self.strokestyles, acontext, registry, bbox)

                file.write("stroke\n")
                # take linewidth into account for bbox when stroking a path
                bbox += strokepath.bbox().enlarged_pt(0.5*acontext.linewidth_pt)

                if self.strokestyles:
                    file.write("grestore\n")
            else:
                # only fill fillpath - for the moment
                if self.fillstyles:
                    file.write("gsave\n")
                    _writestyles(self.fillstyles, context(), registry, bbox)

                file.write("fill\n")
                bbox += fillpath.bbox()

                if self.fillstyles:
                    file.write("grestore\n")

        if self.strokestyles is not None and (strokepath is not fillpath or self.fillstyles is None):
            # this is the only relevant case still left
            # Note that a possible stroking has already been done.
            acontext = context()
            if self.strokestyles:
                file.write("gsave\n")
                _writestyles(self.strokestyles, acontext, registry, bbox)

            file.write("newpath\n")
            strokepath.outputPS(file, writer)
            file.write("stroke\n")
            # take linewidth into account for bbox when stroking a path
            bbox += strokepath.bbox().enlarged_pt(0.5*acontext.linewidth_pt)

            if self.strokestyles:
                file.write("grestore\n")

        # now, draw additional elements of decoratedpath
        self.ornaments.processPS(file, writer, context, registry, bbox)

        # restore global styles
        if self.styles:
            file.write("grestore\n")

    def processPDF(self, file, writer, context, registry, bbox):
        # draw (stroke and/or fill) the decoratedpath on the canvas

        def _writestyles(styles, context, registry, bbox):
            for style in styles:
                style.processPDF(file, writer, context, registry, bbox)

        def _writestrokestyles(strokestyles, context, registry, bbox):
            context.fillattr = 0
            for style in strokestyles:
                style.processPDF(file, writer, context, registry, bbox)
            context.fillattr = 1

        def _writefillstyles(fillstyles, context, registry, bbox):
            context.strokeattr = 0
            for style in fillstyles:
                style.processPDF(file, writer, context, registry, bbox)
            context.strokeattr = 1

        if self.strokestyles is None and self.fillstyles is None:
            if not len(self.ornaments):
                raise RuntimeError("Path neither to be stroked nor filled nor decorated in another way")
            # just draw additional elements of decoratedpath
            self.ornaments.processPDF(file, writer, context, registry, bbox)
            return

        strokepath = self.strokepath()
        fillpath = self.path

        # apply global styles
        if self.styles:
            file.write("q\n") # gsave
            context = context()
            _writestyles(self.styles, context, registry, bbox)

        if self.fillstyles is not None:
            fillpath.outputPDF(file, writer)

            if self.strokestyles is not None and strokepath is fillpath:
                # do efficient stroking + filling
                file.write("q\n") # gsave
                acontext = context()

                if self.fillstyles:
                    _writefillstyles(self.fillstyles, acontext, registry, bbox)
                if self.strokestyles:
                    _writestrokestyles(self.strokestyles, acontext, registry, bbox)

                file.write("B\n") # both stroke and fill
                # take linewidth into account for bbox when stroking a path
                bbox += strokepath.bbox().enlarged_pt(0.5*acontext.linewidth_pt)

                file.write("Q\n") # grestore
            else:
                # only fill fillpath - for the moment
                if self.fillstyles:
                    file.write("q\n") # gsave
                    _writefillstyles(self.fillstyles, context(), registry, bbox)

                file.write("f\n") # fill
                bbox += fillpath.bbox()

                if self.fillstyles:
                    file.write("Q\n") # grestore

        if self.strokestyles is not None and (strokepath is not fillpath or self.fillstyles is None):
            # this is the only relevant case still left
            # Note that a possible stroking has already been done.
            acontext = context()

            if self.strokestyles:
                file.write("q\n") # gsave
                _writestrokestyles(self.strokestyles, acontext, registry, bbox)

            strokepath.outputPDF(file, writer)
            file.write("S\n") # stroke
            # take linewidth into account for bbox when stroking a path
            bbox += strokepath.bbox().enlarged_pt(0.5*acontext.linewidth_pt)

            if self.strokestyles:
                file.write("Q\n") # grestore

        # now, draw additional elements of decoratedpath
        self.ornaments.processPDF(file, writer, context, registry, bbox)

        # restore global styles
        if self.styles:
            file.write("Q\n") # grestore

#
# Path decorators
#

class deco:

    """decorators

    In contrast to path styles, path decorators depend on the concrete
    path to which they are applied. In particular, they don't make
    sense without any path and can thus not be used in canvas.set!

    """

    def decorate(self, dp, texrunner):
        """apply a style to a given decoratedpath object dp

        decorate accepts a decoratedpath object dp, applies PathStyle
        by modifying dp in place.
        """

        pass

#
# stroked and filled: basic decos which stroked and fill,
# respectively the path
#

class _stroked(deco, attr.exclusiveattr):

    """stroked is a decorator, which draws the outline of the path"""

    def __init__(self, styles=[]):
        attr.exclusiveattr.__init__(self, _stroked)
        self.styles = attr.mergeattrs(styles)
        attr.checkattrs(self.styles, [style.strokestyle])

    def __call__(self, styles=[]):
        # XXX or should we also merge self.styles
        return _stroked(styles)

    def decorate(self, dp, texrunner):
        if dp.strokestyles is not None:
            raise RuntimeError("Cannot stroke an already stroked path")
        dp.strokestyles = self.styles

stroked = _stroked()
stroked.clear = attr.clearclass(_stroked)


class _filled(deco, attr.exclusiveattr):

    """filled is a decorator, which fills the interior of the path"""

    def __init__(self, styles=[]):
        attr.exclusiveattr.__init__(self, _filled)
        self.styles = attr.mergeattrs(styles)
        attr.checkattrs(self.styles, [style.fillstyle])

    def __call__(self, styles=[]):
        # XXX or should we also merge self.styles
        return _filled(styles)

    def decorate(self, dp, texrunner):
        if dp.fillstyles is not None:
            raise RuntimeError("Cannot fill an already filled path")
        dp.fillstyles = self.styles

filled = _filled()
filled.clear = attr.clearclass(_filled)

#
# Arrows
#

# helper function which constructs the arrowhead

def _arrowhead(anormpath, arclenfrombegin, direction, size, angle, constrictionlen):

    """helper routine, which returns an arrowhead from a given anormpath

    - arclenfrombegin: position of arrow in arc length from the start of the path
    - direction: +1 for an arrow pointing along the direction of anormpath or
                 -1 for an arrow pointing opposite to the direction of normpath
    - size: size of the arrow as arc length
    - angle. opening angle
    - constrictionlen: None (no constriction) or arc length of constriction.
    """

    # arc length and coordinates of tip
    tx, ty = anormpath.at(arclenfrombegin)

    # construct the template for the arrow by cutting the path at the
    # corresponding length
    arrowtemplate = anormpath.split([arclenfrombegin, arclenfrombegin - direction * size])[1]

    # from this template, we construct the two outer curves of the arrow
    arrowl = arrowtemplate.transformed(trafo.rotate(-angle/2.0, tx, ty))
    arrowr = arrowtemplate.transformed(trafo.rotate( angle/2.0, tx, ty))

    # now come the joining backward parts
    if constrictionlen is not None:
        # constriction point (cx, cy) lies on path
        cx, cy = anormpath.at(arclenfrombegin - direction * constrictionlen)
        arrowcr= path.line(*(arrowr.atend() + (cx,cy)))
        arrow = arrowl.reversed() << arrowr << arrowcr
    else:
        arrow = arrowl.reversed() << arrowr

    arrow[-1].close()

    return arrow


_base = 6 * unit.v_pt

class arrow(deco, attr.attr):

    """arrow is a decorator which adds an arrow to either side of the path"""

    def __init__(self, attrs=[], pos=1, reversed=0, size=_base, angle=45, constriction=0.8):
        self.attrs = attr.mergeattrs([style.linestyle.solid, filled] + attrs)
        attr.checkattrs(self.attrs, [deco, style.fillstyle, style.strokestyle])
        self.pos = pos
        self.reversed = reversed
        self.size = size
        self.angle = angle
        self.constriction = constriction

    def __call__(self, attrs=None, pos=None, reversed=None, size=None, angle=None, constriction=_marker):
        if attrs is None:
            attrs = self.attrs
        if pos is None:
            pos = self.pos
        if reversed is None:
            reversed = self.reversed
        if size is None:
            size = self.size
        if angle is None:
            angle = self.angle
        if constriction is _marker:
            constriction = self.constriction
        return arrow(attrs=attrs, pos=pos, reversed=reversed, size=size, angle=angle, constriction=constriction)

    def decorate(self, dp, texrunner):
        dp.ensurenormpath()
        anormpath = dp.path

        # calculate absolute arc length of constricition
        # Note that we have to correct this length because the arrowtemplates are rotated
        # by self.angle/2 to the left and right. Hence, if we want no constriction, i.e., for
        # self.constriction = 1, we actually have a length which is approximately shorter
        # by the given geometrical factor.
        if self.constriction is not None:
            constrictionlen = arrowheadconstrictionlen = self.size * self.constriction * math.cos(radians(self.angle/2.0))
        else:
            # if we do not want a constriction, i.e. constriction is None, we still
            # need constrictionlen for cutting the path
            constrictionlen = self.size * 1 * math.cos(radians(self.angle/2.0))
            arrowheadconstrictionlen = None

        arclenfrombegin = self.pos * anormpath.arclen()
        direction = self.reversed and -1 or 1
        arrowhead = _arrowhead(anormpath, arclenfrombegin, direction, self.size, self.angle, arrowheadconstrictionlen)

        # add arrowhead to decoratedpath
        dp.ornaments.draw(arrowhead, self.attrs)

        # exlude part of the path from stroking when the arrow is strictly at the begin or the end
        if self.pos == 0 and self.reversed:
            dp.excluderange(0, min(self.size, constrictionlen))
        elif self.pos == 1 and not self.reversed:
            dp.excluderange(anormpath.end() - min(self.size, constrictionlen), anormpath.end())

arrow.clear = attr.clearclass(arrow)

# arrows at begin of path
barrow = arrow(pos=0, reversed=1)
barrow.SMALL = barrow(size=_base/math.sqrt(64))
barrow.SMALl = barrow(size=_base/math.sqrt(32))
barrow.SMAll = barrow(size=_base/math.sqrt(16))
barrow.SMall = barrow(size=_base/math.sqrt(8))
barrow.Small = barrow(size=_base/math.sqrt(4))
barrow.small = barrow(size=_base/math.sqrt(2))
barrow.normal = barrow(size=_base)
barrow.large = barrow(size=_base*math.sqrt(2))
barrow.Large = barrow(size=_base*math.sqrt(4))
barrow.LArge = barrow(size=_base*math.sqrt(8))
barrow.LARge = barrow(size=_base*math.sqrt(16))
barrow.LARGe = barrow(size=_base*math.sqrt(32))
barrow.LARGE = barrow(size=_base*math.sqrt(64))

# arrows at end of path
earrow = arrow()
earrow.SMALL = earrow(size=_base/math.sqrt(64))
earrow.SMALl = earrow(size=_base/math.sqrt(32))
earrow.SMAll = earrow(size=_base/math.sqrt(16))
earrow.SMall = earrow(size=_base/math.sqrt(8))
earrow.Small = earrow(size=_base/math.sqrt(4))
earrow.small = earrow(size=_base/math.sqrt(2))
earrow.normal = earrow(size=_base)
earrow.large = earrow(size=_base*math.sqrt(2))
earrow.Large = earrow(size=_base*math.sqrt(4))
earrow.LArge = earrow(size=_base*math.sqrt(8))
earrow.LARge = earrow(size=_base*math.sqrt(16))
earrow.LARGe = earrow(size=_base*math.sqrt(32))
earrow.LARGE = earrow(size=_base*math.sqrt(64))


class text(deco, attr.attr):
    """a simple text decorator"""

    def __init__(self, text, textattrs=[], angle=0, textdist=0.2,
                       relarclenpos=0.5, arclenfrombegin=None, arclenfromend=None,
                       texrunner=None):
        if arclenfrombegin is not None and arclenfromend is not None:
            raise ValueError("either set arclenfrombegin or arclenfromend")
        self.text = text
        self.textattrs = textattrs
        self.angle = angle
        self.textdist = textdist
        self.relarclenpos = relarclenpos
        self.arclenfrombegin = arclenfrombegin
        self.arclenfromend = arclenfromend
        self.texrunner = texrunner

    def decorate(self, dp, texrunner):
        if self.texrunner:
            texrunner = self.texrunner
        import text as textmodule
        textattrs = attr.mergeattrs([textmodule.halign.center, textmodule.vshift.mathaxis] + self.textattrs)

        dp.ensurenormpath()
        if self.arclenfrombegin is not None:
            x, y = dp.path.at(dp.path.begin() + self.arclenfrombegin)
        elif self.arclenfromend is not None:
            x, y = dp.path.at(dp.path.end() - self.arclenfromend)
        else:
            # relarcpos is used, when neither arcfrombegin nor arcfromend is given
            x, y = dp.path.at(self.relarclenpos * dp.path.arclen())

        t = texrunner.text(x, y, self.text, textattrs)
        t.linealign(self.textdist, math.cos(self.angle*math.pi/180), math.sin(self.angle*math.pi/180))
        dp.ornaments.insert(t)


class shownormpath(deco, attr.attr):

    def decorate(self, dp, texrunner):
        r_pt = 2
        dp.ensurenormpath()
        for normsubpath in dp.path.normsubpaths:
            for i, normsubpathitem in enumerate(normsubpath.normsubpathitems):
                if isinstance(normsubpathitem, normpath.normcurve_pt):
                    dp.ornaments.stroke(normpath.normpath([normpath.normsubpath([normsubpathitem])]), [color.rgb.green])
                else:
                    dp.ornaments.stroke(normpath.normpath([normpath.normsubpath([normsubpathitem])]), [color.rgb.blue])
        for normsubpath in dp.path.normsubpaths:
            for i, normsubpathitem in enumerate(normsubpath.normsubpathitems):
                if isinstance(normsubpathitem, normpath.normcurve_pt):
                    dp.ornaments.stroke(path.line_pt(normsubpathitem.x0_pt, normsubpathitem.y0_pt, normsubpathitem.x1_pt, normsubpathitem.y1_pt), [style.linestyle.dashed, color.rgb.red])
                    dp.ornaments.stroke(path.line_pt(normsubpathitem.x2_pt, normsubpathitem.y2_pt, normsubpathitem.x3_pt, normsubpathitem.y3_pt), [style.linestyle.dashed, color.rgb.red])
                    dp.ornaments.draw(path.circle_pt(normsubpathitem.x1_pt, normsubpathitem.y1_pt, r_pt), [filled([color.rgb.red])])
                    dp.ornaments.draw(path.circle_pt(normsubpathitem.x2_pt, normsubpathitem.y2_pt, r_pt), [filled([color.rgb.red])])
        for normsubpath in dp.path.normsubpaths:
            for i, normsubpathitem in enumerate(normsubpath.normsubpathitems):
                if not i:
                    x_pt, y_pt = normsubpathitem.atbegin_pt()
                    dp.ornaments.draw(path.circle_pt(x_pt, y_pt, r_pt), [filled])
                x_pt, y_pt = normsubpathitem.atend_pt()
                dp.ornaments.draw(path.circle_pt(x_pt, y_pt, r_pt), [filled])
