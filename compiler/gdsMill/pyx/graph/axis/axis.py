# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2002-2004 Jörg Lehmann <joergl@users.sourceforge.net>
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

from __future__ import nested_scopes

import math, warnings
from pyx import attr, unit, text
from pyx.graph.axis import painter, parter, positioner, rater, texter, tick

try:
    enumerate([])
except NameError:
    # fallback implementation for Python 2.2 and below
    def enumerate(list):
        return zip(xrange(len(list)), list)

class _marker: pass


class axisdata:
    """axis data storage class

    Instances of this class are used to store axis data local to the
    graph. It will always contain an axispos instance provided by the
    graph during initialization."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class _axis:
    """axis"""

    def createlinked(self, data, positioner, graphtexrunner, errorname, linkpainter):
        canvas = painter.axiscanvas(self.painter, graphtexrunner)
        if linkpainter is not None:
            linkpainter.paint(canvas, data, self, positioner)
        return canvas


class NoValidPartitionError(RuntimeError):

    pass


class _regularaxis(_axis):
    """base implementation a regular axis

    Regular axis have a continuous variable like linear axes,
    logarithmic axes, time axes etc."""

    def __init__(self, min=None, max=None, reverse=0, divisor=None, title=None,
                       painter=painter.regular(), texter=texter.mixed(), linkpainter=painter.linked(),
                       density=1, maxworse=2, manualticks=[]):
        if min is not None and max is not None and min > max:
            min, max, reverse = max, min, not reverse
        self.min = min
        self.max = max
        self.reverse = reverse
        self.divisor = divisor
        self.title = title
        self.painter = painter
        self.texter = texter
        self.linkpainter = linkpainter
        self.density = density
        self.maxworse = maxworse
        self.manualticks = self.checkfraclist(manualticks)

    def createdata(self, errorname):
        return axisdata(min=self.min, max=self.max)

    zero = 0.0

    def adjustaxis(self, data, columndata, graphtexrunner, errorname):
        if self.min is None or self.max is None:
            for value in columndata:
                try:
                    value = value + self.zero
                except:
                    pass
                else:
                    if self.min is None and (data.min is None or value < data.min):
                        data.min = value
                    if self.max is None and (data.max is None or value > data.max):
                        data.max = value

    def checkfraclist(self, fracs):
        "orders a list of fracs, equal entries are not allowed"
        if not len(fracs): return []
        sorted = list(fracs)
        sorted.sort()
        last = sorted[0]
        for item in sorted[1:]:
            if last == item:
                raise ValueError("duplicate entry found")
            last = item
        return sorted

    def _create(self, data, positioner, graphtexrunner, parter, rater, errorname):
        errorname = " for axis %s" % errorname
        if data.min is None or data.max is None:
            raise RuntimeError("incomplete axis range%s" % errorname)

        def layout(data):
            self.adjustaxis(data, data.ticks, graphtexrunner, errorname)
            self.texter.labels(data.ticks)
            if self.divisor:
                for t in data.ticks:
                    t *= tick.rational(self.divisor)
            canvas = painter.axiscanvas(self.painter, graphtexrunner)
            if self.painter is not None:
                self.painter.paint(canvas, data, self, positioner)
            return canvas

        if parter is None:
            data.ticks = self.manualticks
            return layout(data)

        # a variant is a data copy with local modifications to test several partitions
        class variant:
            def __init__(self, data, **kwargs):
                self.data = data
                for key, value in kwargs.items():
                    setattr(self, key, value)

            def __getattr__(self, key):
                return getattr(data, key)

            def __cmp__(self, other):
                # we can also sort variants by their rate
                return cmp(self.rate, other.rate)

        # build a list of variants
        bestrate = None
        if self.divisor is not None:
            partfunctions = parter.partfunctions(data.min/self.divisor, data.max/self.divisor,
                                                 self.min is None, self.max is None)
        else:
            partfunctions = parter.partfunctions(data.min, data.max,
                                                 self.min is None, self.max is None)
        variants = []
        for partfunction in partfunctions:
            worse = 0
            while worse < self.maxworse:
                worse += 1
                ticks = partfunction()
                if ticks is None:
                    break
                ticks = tick.mergeticklists(self.manualticks, ticks, mergeequal=0)
                if ticks:
                    rate = rater.rateticks(self, ticks, self.density)
                    if self.reverse:
                        rate += rater.raterange(self.convert(data, ticks[0]) -
                                                self.convert(data, ticks[-1]), 1)
                    else:
                        rate += rater.raterange(self.convert(data, ticks[-1]) -
                                                self.convert(data, ticks[0]), 1)
                    if bestrate is None or rate < bestrate:
                        bestrate = rate
                        worse = 0
                    variants.append(variant(data, rate=rate, ticks=ticks))

        if not variants:
            raise RuntimeError("no axis partitioning found%s" % errorname)

        if len(variants) == 1 or self.painter is None:
            # When the painter is None, we could sort the variants here by their rating.
            # However, we didn't did this so far and there is no real reason to change that.
            data.ticks = variants[0].ticks
            return layout(data)

        # build the layout for best variants
        for variant in variants:
            variant.storedcanvas = None
        variants.sort()
        while not variants[0].storedcanvas:
            variants[0].storedcanvas = layout(variants[0])
            ratelayout = rater.ratelayout(variants[0].storedcanvas, self.density)
            if ratelayout is None:
                del variants[0]
                if not variants:
                    raise NoValidPartitionError("no valid axis partitioning found%s" % errorname)
            else:
                variants[0].rate += ratelayout
            variants.sort()
        self.adjustaxis(data, variants[0].ticks, graphtexrunner, errorname)
        data.ticks = variants[0].ticks
        return variants[0].storedcanvas


class linear(_regularaxis):
    """linear axis"""

    def __init__(self, parter=parter.autolinear(), rater=rater.linear(), **args):
        _regularaxis.__init__(self, **args)
        self.parter = parter
        self.rater = rater

    def convert(self, data, value):
        """axis coordinates -> graph coordinates"""
        if self.reverse:
            return (data.max - float(value)) / (data.max - data.min)
        else:
            return (float(value) - data.min) / (data.max - data.min)

    def create(self, data, positioner, graphtexrunner, errorname):
        return _regularaxis._create(self, data, positioner, graphtexrunner, self.parter, self.rater, errorname)

lin = linear


class logarithmic(_regularaxis):
    """logarithmic axis"""

    def __init__(self, parter=parter.autologarithmic(), rater=rater.logarithmic(),
                       linearparter=parter.autolinear(extendtick=None), **args):
        _regularaxis.__init__(self, **args)
        self.parter = parter
        self.rater = rater
        self.linearparter = linearparter

    def convert(self, data, value):
        """axis coordinates -> graph coordinates"""
        # TODO: store log(data.min) and log(data.max)
        if self.reverse:
            return (math.log(data.max) - math.log(float(value))) / (math.log(data.max) - math.log(data.min))
        else:
            return (math.log(float(value)) - math.log(data.min)) / (math.log(data.max) - math.log(data.min))

    def create(self, data, positioner, graphtexrunner, errorname):
        try:
            return _regularaxis._create(self, data, positioner, graphtexrunner, self.parter, self.rater, errorname)
        except NoValidPartitionError:
            if self.linearparter:
                warnings.warn("no valid logarithmic partitioning found for axis %s, switch to linear partitioning" % errorname)
                return _regularaxis._create(self, data, positioner, graphtexrunner, self.linearparter, self.rater, errorname)
            raise

log = logarithmic


class subaxispositioner(positioner._positioner):
    """a subaxis positioner"""

    def __init__(self, basepositioner, subaxis):
        self.basepositioner = basepositioner
        self.vmin = subaxis.vmin
        self.vmax = subaxis.vmax
        self.vminover = subaxis.vminover
        self.vmaxover = subaxis.vmaxover

    def vbasepath(self, v1=None, v2=None):
        if v1 is not None:
            v1 = self.vmin+v1*(self.vmax-self.vmin)
        else:
            v1 = self.vminover
        if v2 is not None:
            v2 = self.vmin+v2*(self.vmax-self.vmin)
        else:
            v2 = self.vmaxover
        return self.basepositioner.vbasepath(v1, v2)

    def vgridpath(self, v):
        return self.basepositioner.vgridpath(self.vmin+v*(self.vmax-self.vmin))

    def vtickpoint_pt(self, v, axis=None):
        return self.basepositioner.vtickpoint_pt(self.vmin+v*(self.vmax-self.vmin))

    def vtickdirection(self, v, axis=None):
        return self.basepositioner.vtickdirection(self.vmin+v*(self.vmax-self.vmin))


class bar(_axis):

    def __init__(self, subaxes=None, defaultsubaxis=linear(painter=None, linkpainter=None, parter=None),
                       dist=0.5, firstdist=None, lastdist=None, title=None, reverse=0,
                       painter=painter.bar(), linkpainter=painter.linkedbar()):
        self.subaxes = subaxes
        self.defaultsubaxis = defaultsubaxis
        self.dist = dist
        if firstdist is not None:
            self.firstdist = firstdist
        else:
            self.firstdist = 0.5 * dist
        if lastdist is not None:
            self.lastdist = lastdist
        else:
            self.lastdist = 0.5 * dist
        self.title = title
        self.reverse = reverse
        self.painter = painter
        self.linkpainter = linkpainter

    def createdata(self, errorname):
        data = axisdata(size=self.firstdist+self.lastdist-self.dist, subaxes={}, names=[])
        return data

    def addsubaxis(self, data, name, subaxis, graphtexrunner, errorname):
        subaxis = anchoredaxis(subaxis, graphtexrunner, "%s, subaxis %s" % (errorname, name))
        subaxis.setcreatecall(lambda: None)
        subaxis.sized = hasattr(subaxis.data, "size")
        if subaxis.sized:
            data.size += subaxis.data.size
        else:
            data.size += 1
        data.size += self.dist
        data.subaxes[name] = subaxis
        if self.reverse:
            data.names.insert(0, name)
        else:
            data.names.append(name)

    def adjustaxis(self, data, columndata, graphtexrunner, errorname):
        for value in columndata:

            # some checks and error messages
            try:
                len(value)
            except:
                raise ValueError("tuple expected by bar axis '%s'" % errorname)
            try:
                value + ""
            except:
                pass
            else:
                raise ValueError("tuple expected by bar axis '%s'" % errorname)
            assert len(value) == 2, "tuple of size two expected by bar axis '%s'" % errorname

            name = value[0]
            if name is not None and name not in data.names:
                if self.subaxes:
                    if self.subaxes[name] is not None:
                        self.addsubaxis(data, name, self.subaxes[name], graphtexrunner, errorname)
                else:
                    self.addsubaxis(data, name, self.defaultsubaxis, graphtexrunner, errorname)
        for name in data.names:
            subaxis = data.subaxes[name]
            if subaxis.sized:
                data.size -= subaxis.data.size
            subaxis.axis.adjustaxis(subaxis.data,
                                    [value[1] for value in columndata if value[0] == name],
                                    graphtexrunner,
                                    "%s, subaxis %s" % (errorname, name))
            if subaxis.sized:
                data.size += subaxis.data.size

    def convert(self, data, value):
        if value[0] is None:
            return None
        axis = data.subaxes[value[0]]
        vmin = axis.vmin
        vmax = axis.vmax
        return axis.vmin + axis.convert(value[1]) * (axis.vmax - axis.vmin)

    def create(self, data, positioner, graphtexrunner, errorname):
        canvas = painter.axiscanvas(self.painter, graphtexrunner)
        v = 0
        position = self.firstdist
        for name in data.names:
            subaxis = data.subaxes[name]
            subaxis.vmin = position / float(data.size)
            if subaxis.sized:
                position += subaxis.data.size
            else:
                position += 1
            subaxis.vmax = position / float(data.size)
            position += 0.5*self.dist
            subaxis.vminover = v
            if name == data.names[-1]:
                subaxis.vmaxover = 1
            else:
                subaxis.vmaxover = position / float(data.size)
            subaxis.setpositioner(subaxispositioner(positioner, subaxis))
            subaxis.create()
            canvas.insert(subaxis.canvas)
            if canvas.extent_pt < subaxis.canvas.extent_pt:
                canvas.extent_pt = subaxis.canvas.extent_pt
            position += 0.5*self.dist
            v = subaxis.vmaxover
        if self.painter is not None:
            self.painter.paint(canvas, data, self, positioner)
        return canvas

    def createlinked(self, data, positioner, graphtexrunner, errorname, linkpainter):
        canvas = painter.axiscanvas(self.painter, graphtexrunner)
        for name in data.names:
            subaxis = data.subaxes[name]
            subaxis = linkedaxis(subaxis, name)
            subaxis.setpositioner(subaxispositioner(positioner, data.subaxes[name]))
            subaxis.create()
            canvas.insert(subaxis.canvas)
            if canvas.extent_pt < subaxis.canvas.extent_pt:
                canvas.extent_pt = subaxis.canvas.extent_pt
        if linkpainter is not None:
            linkpainter.paint(canvas, data, self, positioner)
        return canvas


class nestedbar(bar):

    def __init__(self, defaultsubaxis=bar(dist=0, painter=None, linkpainter=None), **kwargs):
        bar.__init__(self, defaultsubaxis=defaultsubaxis, **kwargs)


class split(bar):

    def __init__(self, defaultsubaxis=linear(),
                       firstdist=0, lastdist=0,
                       painter=painter.split(), linkpainter=painter.linkedsplit(), **kwargs):
        bar.__init__(self, defaultsubaxis=defaultsubaxis,
                           firstdist=firstdist, lastdist=lastdist,
                           painter=painter, linkpainter=linkpainter, **kwargs)


class sizedlinear(linear):

    def __init__(self, size=1, **kwargs):
        linear.__init__(self, **kwargs)
        self.size = size

    def createdata(self, errorname):
        data = linear.createdata(self, errorname)
        data.size = self.size
        return data

sizedlin = sizedlinear


class autosizedlinear(linear):

    def __init__(self, parter=parter.autolinear(extendtick=None), **kwargs):
        linear.__init__(self, parter=parter, **kwargs)

    def createdata(self, errorname):
        data = linear.createdata(self, errorname)
        try:
            data.size = data.max - data.min
        except:
            data.size = 0
        return data

    def adjustaxis(self, data, columndata, graphtexrunner, errorname):
        linear.adjustaxis(self, data, columndata, graphtexrunner, errorname)
        try:
            data.size = data.max - data.min
        except:
            data.size = 0

    def create(self, data, positioner, graphtexrunner, errorname):
        min = data.min
        max = data.max
        canvas = linear.create(self, data, positioner, graphtexrunner, errorname)
        if min != data.min or max != data.max:
            raise RuntimeError("range change during axis creation of autosized linear axis")
        return canvas

autosizedlin = autosizedlinear


class anchoredaxis:

    def __init__(self, axis, graphtexrunner, errorname):
        assert not isinstance(axis, anchoredaxis), errorname
        self.axis = axis
        self.errorname = errorname
        self.graphtexrunner = graphtexrunner
        self.data = axis.createdata(errorname)
        self.canvas = None
        self.positioner = None

    def setcreatecall(self, function, *args, **kwargs):
        self._createfunction = function
        self._createargs = args
        self._createkwargs = kwargs

    def docreate(self):
        if not self.canvas:
            self._createfunction(*self._createargs, **self._createkwargs)

    def setpositioner(self, positioner):
        assert positioner is not None, self.errorname
        assert self.positioner is None, self.errorname
        self.positioner = positioner

    def convert(self, x):
        self.docreate()
        return self.axis.convert(self.data, x)

    def adjustaxis(self, columndata):
        if self.canvas is None:
            self.axis.adjustaxis(self.data, columndata, self.graphtexrunner, self.errorname)
        else:
            warnings.warn("ignore axis range adjustment of already created axis '%s'"  % self.errorname)

    def vbasepath(self, v1=None, v2=None):
        return self.positioner.vbasepath(v1=v1, v2=v2)

    def basepath(self, x1=None, x2=None):
        self.docreate()
        if x1 is None:
            if x2 is None:
                return self.positioner.vbasepath()
            else:
                return self.positioner.vbasepath(v2=self.axis.convert(self.data, x2))
        else:
            if x2 is None:
                return self.positioner.vbasepath(v1=self.axis.convert(self.data, x1))
            else:
                return self.positioner.vbasepath(v1=self.axis.convert(self.data, x1),
                                                 v2=self.axis.convert(self.data, x2))

    def vgridpath(self, v):
        return self.positioner.vgridpath(v)

    def gridpath(self, x):
        self.docreate()
        return self.positioner.vgridpath(self.axis.convert(self.data, x))

    def vtickpoint_pt(self, v):
        return self.positioner.vtickpoint_pt(v)

    def vtickpoint(self, v):
        return self.positioner.vtickpoint_pt(v) * unit.t_pt

    def tickpoint_pt(self, x):
        self.docreate()
        return self.positioner.vtickpoint_pt(self.axis.convert(self.data, x))

    def tickpoint(self, x):
        self.docreate()
        x_pt, y_pt = self.positioner.vtickpoint_pt(self.axis.convert(self.data, x))
        return  x_pt * unit.t_pt, y_pt * unit.t_pt

    def vtickdirection(self, v):
        return self.positioner.vtickdirection(v)

    def tickdirection(self, x):
        self.docreate()
        return self.positioner.vtickdirection(self.axis.convert(self.data, x))

    def create(self):
        if self.canvas is None:
            assert self.positioner is not None, self.errorname
            self.canvas = self.axis.create(self.data, self.positioner, self.graphtexrunner, self.errorname)
        return self.canvas


class linkedaxis(anchoredaxis):

    def __init__(self, linkedaxis=None, errorname="manual-linked", painter=_marker):
        self.painter = painter
        self.linkedto = None
        self.errorname = errorname
        self.canvas = None
        self.positioner = None
        if linkedaxis:
            self.setlinkedaxis(linkedaxis)

    def setlinkedaxis(self, linkedaxis):
        assert isinstance(linkedaxis, anchoredaxis), errorname
        self.linkedto = linkedaxis
        self.axis = linkedaxis.axis
        self.graphtexrunner = self.linkedto.graphtexrunner
        self.errorname = "%s (linked to %s)" % (self.errorname, linkedaxis.errorname)
        self.data = linkedaxis.data
        if self.painter is _marker:
            self.painter = linkedaxis.axis.linkpainter

    def create(self):
        assert self.linkedto is not None, self.errorname
        assert self.positioner is not None, self.errorname
        if self.canvas is None:
            self.linkedto.docreate()
            self.canvas = self.axis.createlinked(self.data, self.positioner, self.graphtexrunner, self.errorname, self.painter)
        return self.canvas


class anchoredpathaxis(anchoredaxis):
    """an anchored axis along a path"""

    def __init__(self, path, axis, **kwargs):
        anchoredaxis.__init__(self, axis, text.defaulttexrunner, "pathaxis")
        self.setpositioner(positioner.pathpositioner(path, **kwargs))
        self.create()

def pathaxis(*args, **kwargs):
    """creates an axiscanvas for an axis along a path"""
    return anchoredpathaxis(*args, **kwargs).canvas

