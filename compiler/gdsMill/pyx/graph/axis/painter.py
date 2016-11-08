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


import math
from pyx import canvas, color, attr, text, style, unit, box, path
from pyx import trafo as trafomodule
from pyx.graph.axis import tick


goldenmean = 0.5 * (math.sqrt(5) + 1)


class axiscanvas(canvas.canvas):
    """axis canvas"""

    def __init__(self, painter, graphtexrunner):
        """initializes the instance
        - sets extent to zero
        - sets labels to an empty list"""
        canvas._canvas.__init__(self)
        self.extent_pt = 0
        self.labels = []
        if isinstance(painter, _text) and painter.texrunner:
            self.settexrunner(painter.texrunner)
        else:
            self.settexrunner(graphtexrunner)


class rotatetext:
    """create rotations accordingly to tick directions"""

    def __init__(self, direction, epsilon=1e-10):
        self.direction = direction
        self.epsilon = epsilon

    def trafo(self, dx, dy):
        direction = self.direction + math.atan2(dy, dx) * 180 / math.pi
        while (direction > 180 + self.epsilon):
            direction -= 360
        while (direction < -180 - self.epsilon):
            direction += 360
        while (direction > 90 + self.epsilon):
            direction -= 180
        while (direction < -90 - self.epsilon):
            direction += 180
        return trafomodule.rotate(direction)


rotatetext.parallel = rotatetext(90)
rotatetext.orthogonal = rotatetext(180)


class _text:
    """a painter with a texrunner"""

    def __init__(self, texrunner=None):
        self.texrunner = texrunner


class _title(_text):
    """class for painting an axis title"""

    defaulttitleattrs = [text.halign.center, text.vshift.mathaxis]

    def __init__(self, titledist=0.3*unit.v_cm,
                       titleattrs=[],
                       titledirection=rotatetext.parallel,
                       titlepos=0.5,
                       **kwargs):
        self.titledist = titledist
        self.titleattrs = titleattrs
        self.titledirection = titledirection
        self.titlepos = titlepos
        _text.__init__(self, **kwargs)

    def paint(self, canvas, data, axis, axispos):
        if axis.title is not None and self.titleattrs is not None:
            x, y = axispos.vtickpoint_pt(self.titlepos)
            dx, dy = axispos.vtickdirection(self.titlepos)
            titleattrs = self.defaulttitleattrs + self.titleattrs
            if self.titledirection is not None:
                titleattrs.append(self.titledirection.trafo(dx, dy))
            title = canvas.text_pt(x, y, axis.title, titleattrs)
            canvas.extent_pt += unit.topt(self.titledist)
            title.linealign_pt(canvas.extent_pt, -dx, -dy)
            canvas.extent_pt += title.extent_pt(dx, dy)


class geometricseries(attr.changeattr):

    def __init__(self, initial, factor):
        self.initial = initial
        self.factor = factor

    def select(self, index, total):
        return self.initial * (self.factor ** index)


class ticklength(geometricseries): pass

_base = 0.12 * unit.v_cm

ticklength.SHORT = ticklength(_base/math.sqrt(64), 1/goldenmean)
ticklength.SHORt = ticklength(_base/math.sqrt(32), 1/goldenmean)
ticklength.SHOrt = ticklength(_base/math.sqrt(16), 1/goldenmean)
ticklength.SHort = ticklength(_base/math.sqrt(8), 1/goldenmean)
ticklength.Short = ticklength(_base/math.sqrt(4), 1/goldenmean)
ticklength.short = ticklength(_base/math.sqrt(2), 1/goldenmean)
ticklength.normal = ticklength(_base, 1/goldenmean)
ticklength.long = ticklength(_base*math.sqrt(2), 1/goldenmean)
ticklength.Long = ticklength(_base*math.sqrt(4), 1/goldenmean)
ticklength.LOng = ticklength(_base*math.sqrt(8), 1/goldenmean)
ticklength.LONg = ticklength(_base*math.sqrt(16), 1/goldenmean)
ticklength.LONG = ticklength(_base*math.sqrt(32), 1/goldenmean)


class regular(_title):
    """class for painting the ticks and labels of an axis"""

    defaulttickattrs = []
    defaultgridattrs = []
    defaultbasepathattrs = [style.linecap.square]
    defaultlabelattrs = [text.halign.center, text.vshift.mathaxis]

    def __init__(self, innerticklength=ticklength.normal,
                       outerticklength=None,
                       tickattrs=[],
                       gridattrs=None,
                       basepathattrs=[],
                       labeldist=0.3*unit.v_cm,
                       labelattrs=[],
                       labeldirection=None,
                       labelhequalize=0,
                       labelvequalize=1,
                       **kwargs):
        self.innerticklength = innerticklength
        self.outerticklength = outerticklength
        self.tickattrs = tickattrs
        self.gridattrs = gridattrs
        self.basepathattrs = basepathattrs
        self.labeldist = labeldist
        self.labelattrs = labelattrs
        self.labeldirection = labeldirection
        self.labelhequalize = labelhequalize
        self.labelvequalize = labelvequalize
        _title.__init__(self, **kwargs)

    def paint(self, canvas, data, axis, axispos):
        for t in data.ticks:
            t.temp_v = axis.convert(data, t)
            t.temp_x_pt, t.temp_y_pt = axispos.vtickpoint_pt(t.temp_v)
            t.temp_dx, t.temp_dy = axispos.vtickdirection(t.temp_v)
        maxticklevel, maxlabellevel = tick.maxlevels(data.ticks)
        labeldist_pt = unit.topt(self.labeldist)

        # create & align t.temp_labelbox
        for t in data.ticks:
            if t.labellevel is not None:
                labelattrs = attr.selectattrs(self.labelattrs, t.labellevel, maxlabellevel)
                if labelattrs is not None:
                    labelattrs = self.defaultlabelattrs + labelattrs
                    if self.labeldirection is not None:
                        labelattrs.append(self.labeldirection.trafo(t.temp_dx, t.temp_dy))
                    if t.labelattrs is not None:
                        labelattrs.extend(t.labelattrs)
                    t.temp_labelbox = canvas.texrunner.text_pt(t.temp_x_pt, t.temp_y_pt, t.label, labelattrs)
        if len(data.ticks) > 1:
            equaldirection = 1
            for t in data.ticks[1:]:
                if t.temp_dx != data.ticks[0].temp_dx or t.temp_dy != data.ticks[0].temp_dy:
                    equaldirection = 0
        else:
            equaldirection = 0
        if equaldirection and ((not data.ticks[0].temp_dx and self.labelvequalize) or
                               (not data.ticks[0].temp_dy and self.labelhequalize)):
            if self.labelattrs is not None:
                box.linealignequal_pt([t.temp_labelbox for t in data.ticks if t.labellevel is not None],
                                      labeldist_pt, -data.ticks[0].temp_dx, -data.ticks[0].temp_dy)
        else:
            for t in data.ticks:
                if t.labellevel is not None and self.labelattrs is not None:
                    t.temp_labelbox.linealign_pt(labeldist_pt, -t.temp_dx, -t.temp_dy)

        for t in data.ticks:
            if t.ticklevel is not None and self.tickattrs is not None:
                tickattrs = attr.selectattrs(self.defaulttickattrs + self.tickattrs, t.ticklevel, maxticklevel)
                if tickattrs is not None:
                    innerticklength = attr.selectattr(self.innerticklength, t.ticklevel, maxticklevel)
                    outerticklength = attr.selectattr(self.outerticklength, t.ticklevel, maxticklevel)
                    if innerticklength is not None or outerticklength is not None:
                        if innerticklength is None:
                            innerticklength = 0
                        if outerticklength is None:
                            outerticklength = 0
                        innerticklength_pt = unit.topt(innerticklength)
                        outerticklength_pt = unit.topt(outerticklength)
                        x1 = t.temp_x_pt + t.temp_dx * innerticklength_pt
                        y1 = t.temp_y_pt + t.temp_dy * innerticklength_pt
                        x2 = t.temp_x_pt - t.temp_dx * outerticklength_pt
                        y2 = t.temp_y_pt - t.temp_dy * outerticklength_pt
                        canvas.stroke(path.line_pt(x1, y1, x2, y2), tickattrs)
                        if outerticklength_pt > canvas.extent_pt:
                            canvas.extent_pt = outerticklength_pt
                        if -innerticklength_pt > canvas.extent_pt:
                            canvas.extent_pt = -innerticklength_pt
            if self.gridattrs is not None:
                gridattrs = attr.selectattrs(self.defaultgridattrs + self.gridattrs, t.ticklevel, maxticklevel)
                if gridattrs is not None:
                    canvas.stroke(axispos.vgridpath(t.temp_v), gridattrs)
            if t.labellevel is not None and self.labelattrs is not None:
                canvas.insert(t.temp_labelbox)
                canvas.labels.append(t.temp_labelbox)
                extent_pt = t.temp_labelbox.extent_pt(t.temp_dx, t.temp_dy) + labeldist_pt
                if extent_pt > canvas.extent_pt:
                    canvas.extent_pt = extent_pt

        if self.labelattrs is None:
            canvas.labels = None

        if self.basepathattrs is not None:
            canvas.stroke(axispos.vbasepath(), self.defaultbasepathattrs + self.basepathattrs)

        # for t in data.ticks:
        #     del t.temp_v    # we've inserted those temporary variables ... and do not care any longer about them
        #     del t.temp_x_pt
        #     del t.temp_y_pt
        #     del t.temp_dx
        #     del t.temp_dy
        #     if t.labellevel is not None and self.labelattrs is not None:
        #         del t.temp_labelbox

        _title.paint(self, canvas, data, axis, axispos)


class linked(regular):
    """class for painting a linked axis"""

    def __init__(self, labelattrs=None, # turn off labels and title
                       titleattrs=None,
                       **kwargs):
        regular.__init__(self, labelattrs=labelattrs,
                               titleattrs=titleattrs,
                               **kwargs)


class bar(_title):
    """class for painting a baraxis"""

    defaulttickattrs = []
    defaultbasepathattrs = [style.linecap.square]
    defaultnameattrs = [text.halign.center, text.vshift.mathaxis]

    def __init__(self, innerticklength=None,
                       outerticklength=None,
                       tickattrs=[],
                       basepathattrs=[],
                       namedist=0.3*unit.v_cm,
                       nameattrs=[],
                       namedirection=None,
                       namepos=0.5,
                       namehequalize=0,
                       namevequalize=1,
                       **args):
        self.innerticklength = innerticklength
        self.outerticklength = outerticklength
        self.tickattrs = tickattrs
        self.basepathattrs = basepathattrs
        self.namedist = namedist
        self.nameattrs = nameattrs
        self.namedirection = namedirection
        self.namepos = namepos
        self.namehequalize = namehequalize
        self.namevequalize = namevequalize
        _title.__init__(self, **args)

    def paint(self, canvas, data, axis, positioner):
        namepos = []
        for name in data.names:
            subaxis = data.subaxes[name]
            v = subaxis.vmin + self.namepos * (subaxis.vmax - subaxis.vmin)
            x, y = positioner.vtickpoint_pt(v)
            dx, dy = positioner.vtickdirection(v)
            namepos.append((v, x, y, dx, dy))
        nameboxes = []
        if self.nameattrs is not None:
            for (v, x, y, dx, dy), name in zip(namepos, data.names):
                nameattrs = self.defaultnameattrs + self.nameattrs
                if self.namedirection is not None:
                    nameattrs.append(self.namedirection.trafo(tick.temp_dx, tick.temp_dy))
                nameboxes.append(canvas.texrunner.text_pt(x, y, str(name), nameattrs))
        labeldist_pt = canvas.extent_pt + unit.topt(self.namedist)
        if len(namepos) > 1:
            equaldirection = 1
            for np in namepos[1:]:
                if np[3] != namepos[0][3] or np[4] != namepos[0][4]:
                    equaldirection = 0
        else:
            equaldirection = 0
        if equaldirection and ((not namepos[0][3] and self.namevequalize) or
                               (not namepos[0][4] and self.namehequalize)):
            box.linealignequal_pt(nameboxes, labeldist_pt, -namepos[0][3], -namepos[0][4])
        else:
            for namebox, np in zip(nameboxes, namepos):
                namebox.linealign_pt(labeldist_pt, -np[3], -np[4])
        if self.basepathattrs is not None:
            p = positioner.vbasepath()
            if p is not None:
                canvas.stroke(p, self.defaultbasepathattrs + self.basepathattrs)
        if ( self.tickattrs is not None and
             (self.innerticklength is not None or self.outerticklength is not None) ):
            if self.innerticklength is not None:
                innerticklength_pt = unit.topt(self.innerticklength)
                if canvas.extent_pt < -innerticklength_pt:
                    canvas.extent_pt = -innerticklength_pt
            elif self.outerticklength is not None:
                innerticklength_pt = 0
            if self.outerticklength is not None:
                outerticklength_pt = unit.topt(self.outerticklength)
                if canvas.extent_pt < outerticklength_pt:
                    canvas.extent_pt = outerticklength_pt
            elif innerticklength_pt is not None:
                outerticklength_pt = 0
            for v in [data.subaxes[name].vminover for name in data.names] + [1]:
                x, y = positioner.vtickpoint_pt(v)
                dx, dy = positioner.vtickdirection(v)
                x1 = x + dx * innerticklength_pt
                y1 = y + dy * innerticklength_pt
                x2 = x - dx * outerticklength_pt
                y2 = y - dy * outerticklength_pt
                canvas.stroke(path.line_pt(x1, y1, x2, y2), self.defaulttickattrs + self.tickattrs)
        for (v, x, y, dx, dy), namebox in zip(namepos, nameboxes):
            newextent_pt = namebox.extent_pt(dx, dy) + labeldist_pt
            if canvas.extent_pt < newextent_pt:
                canvas.extent_pt = newextent_pt
        for namebox in nameboxes:
            canvas.insert(namebox)
        _title.paint(self, canvas, data, axis, positioner)


class linkedbar(bar):
    """class for painting a linked baraxis"""

    def __init__(self, nameattrs=None, titleattrs=None, **kwargs):
        bar.__init__(self, nameattrs=nameattrs, titleattrs=titleattrs, **kwargs)

    def getsubaxis(self, subaxis, name):
        from pyx.graph.axis import linkedaxis
        return linkedaxis(subaxis, name)


class split(_title):
    """class for painting a splitaxis"""

    defaultbreaklinesattrs = []

    def __init__(self, breaklinesdist=0.05*unit.v_cm,
                       breaklineslength=0.5*unit.v_cm,
                       breaklinesangle=-60,
                       breaklinesattrs=[],
                       **args):
        self.breaklinesdist = breaklinesdist
        self.breaklineslength = breaklineslength
        self.breaklinesangle = breaklinesangle
        self.breaklinesattrs = breaklinesattrs
        self.sin = math.sin(self.breaklinesangle*math.pi/180.0)
        self.cos = math.cos(self.breaklinesangle*math.pi/180.0)
        _title.__init__(self, **args)

    def paint(self, canvas, data, axis, axispos):
        if self.breaklinesattrs is not None:
            breaklinesdist_pt = unit.topt(self.breaklinesdist)
            breaklineslength_pt = unit.topt(self.breaklineslength)
            breaklinesextent_pt = (0.5*breaklinesdist_pt*math.fabs(self.cos) +
                                   0.5*breaklineslength_pt*math.fabs(self.sin))
            if canvas.extent_pt < breaklinesextent_pt:
                canvas.extent_pt = breaklinesextent_pt
            for v in [data.subaxes[name].vminover for name in data.names[1:]]:
                # use a tangent of the basepath (this is independent of the tickdirection)
                p = axispos.vbasepath(v, None).normpath()
                breakline = p.tangent(0, length=self.breaklineslength)
                widthline = p.tangent(0, length=self.breaklinesdist).transformed(trafomodule.rotate(self.breaklinesangle+90, *breakline.atbegin()))
                # XXX Uiiii
                tocenter = map(lambda x: 0.5*(x[0]-x[1]), zip(breakline.atbegin(), breakline.atend()))
                towidth = map(lambda x: 0.5*(x[0]-x[1]), zip(widthline.atbegin(), widthline.atend()))
                breakline = breakline.transformed(trafomodule.translate(*tocenter).rotated(self.breaklinesangle, *breakline.atbegin()))
                breakline1 = breakline.transformed(trafomodule.translate(*towidth))
                breakline2 = breakline.transformed(trafomodule.translate(-towidth[0], -towidth[1]))
                canvas.fill(path.path(path.moveto_pt(*breakline1.atbegin_pt()),
                                  path.lineto_pt(*breakline1.atend_pt()),
                                  path.lineto_pt(*breakline2.atend_pt()),
                                  path.lineto_pt(*breakline2.atbegin_pt()),
                                  path.closepath()), [color.gray.white])
                canvas.stroke(breakline1, self.defaultbreaklinesattrs + self.breaklinesattrs)
                canvas.stroke(breakline2, self.defaultbreaklinesattrs + self.breaklinesattrs)
        _title.paint(self, canvas, data, axis, axispos)


class linkedsplit(split):

    def __init__(self, titleattrs=None, **kwargs):
        split.__init__(self, titleattrs=titleattrs, **kwargs)
