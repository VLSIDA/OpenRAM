import datetime
from pyx.graph import style
from pyx.graph.axis import axis, rater

"""some experimental code for creating a time axis
- it needs python 2.3 to be used (it is based on the new datetime data type)
- a timeaxis is always based on the datetime data type (there is no distinction between times and dates)
"""

class timeaxis(axis.linear):
    "time axis mapping based "

    # TODO: how to deal with reversed timeaxis?

    def __init__(self, parter=None, rater=rater.linear(), **args):
        axis._regularaxis.__init__(self, divisor=None, **args)
        self.parter = parter
        self.rater = rater

    def convert(self, data, x):
        # XXX float division of timedelta instances
        def mstimedelta(td):
            "return the timedelta in microseconds"
            return td.microseconds + 1000000*(td.seconds + 3600*24*td.days)
        return mstimedelta(x - data.min) / float(mstimedelta(data.max - data.min))
        # we could store float(mstimedelta(self.dx)) instead of self.dx, but
        # I prefer a different solution (not based on huge integers) for the
        # future

    zero = datetime.timedelta(0)


class timetick(datetime.datetime):

    def __init__(self, year, month, day, ticklevel=0, labellevel=0, label=None, labelattrs=[], **kwargs):
        datetime.datetime.__init__(self, year, month, day, **kwargs)
        self.ticklevel = ticklevel
        self.labellevel = labellevel
        self.label = label
        self.labelattrs = labelattrs[:]

    def merge(self, other):
        if self.ticklevel is None or (other.ticklevel is not None and other.ticklevel < self.ticklevel):
            self.ticklevel = other.ticklevel
        if self.labellevel is None or (other.labellevel is not None and other.labellevel < self.labellevel):
            self.labellevel = other.labellevel


class timetexter:

    def __init__(self, format="%c"):
        self.format = format

    def labels(self, ticks):
        for tick in ticks:
            if tick.labellevel is not None and tick.label is None:
                tick.label = tick.strftime(self.format)



