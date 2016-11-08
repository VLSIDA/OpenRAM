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


from pyx import unit, box
from pyx.graph.axis import tick


# rater
# conseptional remarks:
# - raters are used to calculate a rating for a realization of something
# - a rating means a positive floating point value
# - ratings are used to order those realizations by their suitability
#   (small ratings are better)
# - a rating of None means not suitable at all (those realizations should be
#   thrown out)


class cube:
    """a value rater
    - a cube rater has an optimal value, where the rate becomes zero
    - for a left (below the optimum) and a right value (above the optimum),
      the rating is value is set to 1 (modified by an overall weight factor
      for the rating)
    - the analytic form of the rating is cubic for both, the left and
      the right side of the rater, independently"""

    def __init__(self, opt, left=None, right=None, weight=1):
        """initializes the rater
        - by default, left is set to zero, right is set to 3*opt
        - left should be smaller than opt, right should be bigger than opt
        - weight should be positive and is a factor multiplicated to the rates"""
        if left is None:
            left = 0
        if right is None:
            right = 3*opt
        self.opt = opt
        self.left = left
        self.right = right
        self.weight = weight

    def rate(self, value, density):
        """returns a rating for a value
        - the density lineary rescales the rater (the optimum etc.),
          e.g. a value bigger than one increases the optimum (when it is
          positive) and a value lower than one decreases the optimum (when
          it is positive); the density itself should be positive"""
        opt = self.opt * density
        if value < opt:
            other = self.left * density
        elif value > opt:
            other = self.right * density
        else:
            return 0
        factor = (value - opt) / float(other - opt)
        return self.weight * (factor ** 3)


class distance:
    # TODO: update docstring
    """a distance rater (rates a list of distances)
    - the distance rater rates a list of distances by rating each independently
      and returning the average rate
    - there is an optimal value, where the rate becomes zero
    - the analytic form is linary for values above the optimal value
      (twice the optimal value has the rating one, three times the optimal
      value has the rating two, etc.)
    - the analytic form is reciprocal subtracting one for values below the
      optimal value (halve the optimal value has the rating one, one third of
      the optimal value has the rating two, etc.)"""

    def __init__(self, opt, weight=0.1):
        """inititializes the rater
        - opt is the optimal length (a visual PyX length)
        - weight should be positive and is a factor multiplicated to the rates"""
        self.opt = opt
        self.weight = weight

    def rate(self, distances, density):
        """rate distances
        - the distances are a list of positive floats in PostScript points
        - the density lineary rescales the rater (the optimum etc.),
          e.g. a value bigger than one increases the optimum (when it is
          positive) and a value lower than one decreases the optimum (when
          it is positive); the density itself should be positive"""
        if len(distances):
            opt = unit.topt(self.opt) / density
            rate = 0
            for distance in distances:
                if distance < opt:
                    rate += self.weight * (opt / distance - 1)
                else:
                    rate += self.weight * (distance / opt - 1)
            return rate / float(len(distances))


class rater:
    """a rater for ticks
    - the rating of axes is splited into two separate parts:
      - rating of the ticks in terms of the number of ticks, subticks,
        labels, etc.
      - rating of the label distances
    - in the end, a rate for ticks is the sum of these rates
    - it is useful to first just rate the number of ticks etc.
      and selecting those partitions, where this fits well -> as soon
      as an complete rate (the sum of both parts from the list above)
      of a first ticks is below a rate of just the number of ticks,
      subticks labels etc. of other ticks, those other ticks will never
      be better than the first one -> we gain speed by minimizing the
      number of ticks, where label distances have to be taken into account)
    - both parts of the rating are shifted into instances of raters
      defined above --- right now, there is not yet a strict interface
      for this delegation (should be done as soon as it is needed)"""

    def __init__(self, ticks, labels, range, distance):
        """initializes the axis rater
        - ticks and labels are lists of instances of a value rater
        - the first entry in ticks rate the number of ticks, the
          second the number of subticks, etc.; when there are no
          ticks of a level or there is not rater for a level, the
          level is just ignored
        - labels is analogous, but for labels
        - within the rating, all ticks with a higher level are
          considered as ticks for a given level
        - range is a value rater instance, which rates the covering
          of an axis range by the ticks (as a relative value of the
          tick range vs. the axis range), ticks might cover less or
          more than the axis range (for the standard automatic axis
          partition schemes an extention of the axis range is normal
          and should get some penalty)
        - distance is an distance rater instance"""
        self.ticks = ticks
        self.labels = labels
        self.range = range
        self.distance = distance

    def rateticks(self, axis, ticks, density):
        """rates ticks by the number of ticks, subticks, labels etc.
        - takes into account the number of ticks, subticks, labels
          etc. and the coverage of the axis range by the ticks
        - when there are no ticks of a level or there was not rater
          given in the constructor for a level, the level is just
          ignored
        - the method returns the sum of the rating results divided
          by the sum of the weights of the raters
        - within the rating, all ticks with a higher level are
          considered as ticks for a given level"""
        maxticklevel, maxlabellevel = tick.maxlevels(ticks)
        numticks = [0]*maxticklevel
        numlabels = [0]*maxlabellevel
        for t in ticks:
            if t.ticklevel is not None:
                for level in range(t.ticklevel, maxticklevel):
                    numticks[level] += 1
            if t.labellevel is not None:
                for level in range(t.labellevel, maxlabellevel):
                    numlabels[level] += 1
        rate = 0
        weight = 0
        for numtick, rater in zip(numticks, self.ticks):
            rate += rater.rate(numtick, density)
            weight += rater.weight
        for numlabel, rater in zip(numlabels, self.labels):
            rate += rater.rate(numlabel, density)
            weight += rater.weight
        return rate/weight

    def raterange(self, tickrange, datarange):
        """rate the range covered by the ticks compared to the range
        of the data
        - tickrange and datarange are the ranges covered by the ticks
          and the data in graph coordinates
        - usually, the datarange is 1 (ticks are calculated for a
          given datarange)
        - the ticks might cover less or more than the data range (for
          the standard automatic axis partition schemes an extention
          of the axis range is normal and should get some penalty)"""
        return self.range.rate(tickrange, datarange)

    def ratelayout(self, axiscanvas, density):
        """rate distances of the labels in an axis canvas
        - the distances should be collected as box distances of
          subsequent labels
        - the axiscanvas provides a labels attribute for easy
          access to the labels whose distances have to be taken
          into account
        - the density is used within the distancerate instance"""
        if axiscanvas.labels is None: # to disable any layout rating
            return 0
        if len(axiscanvas.labels) > 1:
            try:
                distances = [axiscanvas.labels[i].boxdistance_pt(axiscanvas.labels[i+1])
                             for i in range(len(axiscanvas.labels) - 1)]
            except box.BoxCrossError:
                return None
            return self.distance.rate(distances, density)
        else:
            return None


class linear(rater):
    """a rater with predefined constructor arguments suitable for a linear axis"""

    def __init__(self, ticks=[cube(4), cube(10, weight=0.5)],
                       labels=[cube(4)],
                       range=cube(1, weight=2),
                       distance=distance(1*unit.v_cm)):
        rater.__init__(self, ticks, labels, range, distance)

lin = linear


class logarithmic(rater):
    """a rater with predefined constructor arguments suitable for a logarithmic axis"""

    def __init__(self, ticks=[cube(5, right=20), cube(20, right=100, weight=0.5)],
                       labels=[cube(5, right=20), cube(5, right=20, weight=0.5)],
                       range=cube(1, weight=2),
                       distance=distance(1*unit.v_cm)):
        rater.__init__(self, ticks, labels, range, distance)

log = logarithmic
