# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2002-2004 Jörg Lehmann <joergl@users.sourceforge.net>
# Copyright (C) 2003-2004 Michael Schindler <m-schindler@users.sourceforge.net>
# Copyright (C) 2002-2004 André Wobst <wobsta@users.sourceforge.net>
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


from pyx import text
from pyx.graph.axis import tick


class _Itexter:

    def labels(self, ticks):
        """fill the label attribute of ticks
        - ticks is a list of instances of tick
        - for each element of ticks the value of the attribute label is set to
          a string appropriate to the attributes num and denom of that tick
          instance
        - label attributes of the tick instances are just kept, whenever they
          are not equal to None
        - the method might modify the labelattrs attribute of the ticks; be sure
          to not modify it in-place!"""


class decimal:
    "a texter creating decimal labels (e.g. '1.234' or even '0.\overline{3}')"

    __implements__ = _Itexter

    def __init__(self, prefix="", infix="", suffix="", equalprecision=0,
                       decimalsep=".", thousandsep="", thousandthpartsep="",
                       plus="", minus="-", period=r"\overline{%s}",
                       labelattrs=[text.mathmode]):
        r"""initializes the instance
        - prefix, infix, and suffix (strings) are added at the begin,
          immediately after the minus, and at the end of the label,
          respectively
        - decimalsep, thousandsep, and thousandthpartsep (strings)
          are used as separators
        - plus or minus (string) is inserted for non-negative or negative numbers
        - period (string) is taken as a format string generating a period;
          it has to contain exactly one string insert operators "%s" for the
          period; usually it should be r"\overline{%s}"
        - labelattrs is a list of attributes to be added to the label attributes
          given in the painter"""
        self.prefix = prefix
        self.infix = infix
        self.suffix = suffix
        self.equalprecision = equalprecision
        self.decimalsep = decimalsep
        self.thousandsep = thousandsep
        self.thousandthpartsep = thousandthpartsep
        self.plus = plus
        self.minus = minus
        self.period = period
        self.labelattrs = labelattrs

    def labels(self, ticks):
        labeledticks = []
        maxdecprecision = 0
        for tick in ticks:
            if tick.label is None and tick.labellevel is not None:
                labeledticks.append(tick)
                m, n = tick.num, tick.denom
                if m < 0: m = -m
                if n < 0: n = -n
                quotient, remainder = divmod(m, n)
                quotient = str(quotient)
                if len(self.thousandsep):
                    l = len(quotient)
                    tick.label = ""
                    for i in range(l):
                        tick.label += quotient[i]
                        if not ((l-i-1) % 3) and l > i+1:
                            tick.label += self.thousandsep
                else:
                    tick.label = quotient
                if remainder:
                    tick.label += self.decimalsep
                oldremainders = []
                tick.temp_decprecision = 0
                while (remainder):
                    tick.temp_decprecision += 1
                    if remainder in oldremainders:
                        tick.temp_decprecision = None
                        periodstart = len(tick.label) - (len(oldremainders) - oldremainders.index(remainder))
                        tick.label = tick.label[:periodstart] + self.period % tick.label[periodstart:]
                        break
                    oldremainders += [remainder]
                    remainder *= 10
                    quotient, remainder = divmod(remainder, n)
                    if not ((tick.temp_decprecision - 1) % 3) and tick.temp_decprecision > 1:
                        tick.label += self.thousandthpartsep
                    tick.label += str(quotient)
                if maxdecprecision < tick.temp_decprecision:
                    maxdecprecision = tick.temp_decprecision
        if self.equalprecision:
            for tick in labeledticks:
                if tick.temp_decprecision is not None:
                    if tick.temp_decprecision == 0 and maxdecprecision > 0:
                        tick.label += self.decimalsep
                    for i in range(tick.temp_decprecision, maxdecprecision):
                        if not ((i - 1) % 3) and i > 1:
                            tick.label += self.thousandthpartsep
                        tick.label += "0"
        for tick in labeledticks:
            if tick.num * tick.denom < 0:
                plusminus = self.minus
            else:
                plusminus = self.plus
            tick.label = "%s%s%s%s%s" % (self.prefix, plusminus, self.infix, tick.label, self.suffix)
            tick.labelattrs = tick.labelattrs + self.labelattrs

            # del tick.temp_decprecision  # we've inserted this temporary variable ... and do not care any longer about it


class exponential:
    "a texter creating labels with exponentials (e.g. '2\cdot10^5')"

    __implements__ = _Itexter

    def __init__(self, plus="", minus="-",
                       mantissaexp=r"{{%s}\cdot10^{%s}}",
                       skipexp0=r"{%s}",
                       skipexp1=None,
                       nomantissaexp=r"{10^{%s}}",
                       minusnomantissaexp=r"{-10^{%s}}",
                       mantissamin=tick.rational((1, 1)), mantissamax=tick.rational((10L, 1)),
                       skipmantissa1=0, skipallmantissa1=1,
                       mantissatexter=decimal()):
        r"""initializes the instance
        - plus or minus (string) is inserted for non-negative or negative exponents
        - mantissaexp (string) is taken as a format string generating the exponent;
          it has to contain exactly two string insert operators "%s" --
          the first for the mantissa and the second for the exponent;
          examples are r"{{%s}\cdot10^{%s}}" and r"{{%s}{\rm e}{%s}}"
        - skipexp0 (string) is taken as a format string used for exponent 0;
          exactly one string insert operators "%s" for the mantissa;
          None turns off the special handling of exponent 0;
          an example is r"{%s}"
        - skipexp1 (string) is taken as a format string used for exponent 1;
          exactly one string insert operators "%s" for the mantissa;
          None turns off the special handling of exponent 1;
          an example is r"{{%s}\cdot10}"
        - nomantissaexp (string) is taken as a format string generating the exponent
          when the mantissa is one and should be skipped; it has to contain
          exactly one string insert operators "%s" for the exponent;
          an examples is r"{10^{%s}}"
        - minusnomantissaexp (string) is taken as a format string generating the exponent
          when the mantissa is minus one and should be skipped; it has to contain
          exactly one string insert operators "%s" for the exponent;
          None turns off the special handling of mantissa -1;
          an examples is r"{-10^{%s}}"
        - mantissamin and mantissamax are the minimum and maximum of the mantissa;
          they are rational instances greater than zero and mantissamin < mantissamax;
          the sign of the tick is ignored here
        - skipmantissa1 (boolean) turns on skipping of any mantissa equals one
          (and minus when minusnomantissaexp is set)
        - skipallmantissa1 (boolean) as above, but all mantissas must be 1 (or -1)
        - mantissatexter is the texter for the mantissa
        - the skipping of a mantissa is stronger than the skipping of an exponent"""
        self.plus = plus
        self.minus = minus
        self.mantissaexp = mantissaexp
        self.skipexp0 = skipexp0
        self.skipexp1 = skipexp1
        self.nomantissaexp = nomantissaexp
        self.minusnomantissaexp = minusnomantissaexp
        self.mantissamin = mantissamin
        self.mantissamax = mantissamax
        self.mantissamindivmax = self.mantissamin / self.mantissamax
        self.mantissamaxdivmin = self.mantissamax / self.mantissamin
        self.skipmantissa1 = skipmantissa1
        self.skipallmantissa1 = skipallmantissa1
        self.mantissatexter = mantissatexter

    def labels(self, ticks):
        labeledticks = []
        for tick in ticks:
            if tick.label is None and tick.labellevel is not None:
                tick.temp_orgnum, tick.temp_orgdenom = tick.num, tick.denom
                labeledticks.append(tick)
                tick.temp_exp = 0
                if tick.num:
                    while abs(tick) >= self.mantissamax:
                        tick.temp_exp += 1
                        x = tick * self.mantissamindivmax
                        tick.num, tick.denom = x.num, x.denom
                    while abs(tick) < self.mantissamin:
                        tick.temp_exp -= 1
                        x = tick * self.mantissamaxdivmin
                        tick.num, tick.denom = x.num, x.denom
                if tick.temp_exp < 0:
                    tick.temp_exp = "%s%i" % (self.minus, -tick.temp_exp)
                else:
                    tick.temp_exp = "%s%i" % (self.plus, tick.temp_exp)
        self.mantissatexter.labels(labeledticks)
        if self.minusnomantissaexp is not None:
            allmantissa1 = len(labeledticks) == len([tick for tick in labeledticks if abs(tick.num) == abs(tick.denom)])
        else:
            allmantissa1 = len(labeledticks) == len([tick for tick in labeledticks if tick.num == tick.denom])
        for tick in labeledticks:
            if (self.skipallmantissa1 and allmantissa1 or
                (self.skipmantissa1 and (tick.num == tick.denom or
                                         (tick.num == -tick.denom and self.minusnomantissaexp is not None)))):
                if tick.num == tick.denom:
                    tick.label = self.nomantissaexp % tick.temp_exp
                else:
                    tick.label = self.minusnomantissaexp % tick.temp_exp
            else:
                if tick.temp_exp == "0" and self.skipexp0 is not None:
                    tick.label = self.skipexp0 % tick.label
                elif tick.temp_exp == "1" and self.skipexp1 is not None:
                    tick.label = self.skipexp1 % tick.label
                else:
                    tick.label = self.mantissaexp % (tick.label, tick.temp_exp)
            tick.num, tick.denom = tick.temp_orgnum, tick.temp_orgdenom

            # del tick.temp_orgnum    # we've inserted those temporary variables ... and do not care any longer about them
            # del tick.temp_orgdenom
            # del tick.temp_exp


class mixed:
    "a texter creating decimal or exponential labels"

    __implements__ = _Itexter

    def __init__(self, smallestdecimal=tick.rational((1, 1000)),
                       biggestdecimal=tick.rational((9999, 1)),
                       equaldecision=1,
                       decimal=decimal(),
                       exponential=exponential()):
        """initializes the instance
        - smallestdecimal and biggestdecimal are the smallest and
          biggest decimal values, where the decimal texter should be used;
          they are rational instances; the sign of the tick is ignored here;
          a tick at zero is considered for the decimal texter as well
        - equaldecision (boolean) uses decimal texter or exponential texter
          globaly (set) or for each tick separately (unset)
        - decimal and exponential are texters to be used"""
        self.smallestdecimal = smallestdecimal
        self.biggestdecimal = biggestdecimal
        self.equaldecision = equaldecision
        self.decimal = decimal
        self.exponential = exponential

    def labels(self, ticks):
        decticks = []
        expticks = []
        for tick in ticks:
            if tick.label is None and tick.labellevel is not None:
                if not tick.num or (abs(tick) >= self.smallestdecimal and abs(tick) <= self.biggestdecimal):
                    decticks.append(tick)
                else:
                    expticks.append(tick)
        if self.equaldecision:
            if len(expticks):
                self.exponential.labels(ticks)
            else:
                self.decimal.labels(ticks)
        else:
            for tick in decticks:
                self.decimal.labels([tick])
            for tick in expticks:
                self.exponential.labels([tick])


class rational:
    "a texter creating rational labels (e.g. 'a/b' or even 'a \over b')"
    # XXX: we use divmod here to be more expicit

    __implements__ = _Itexter

    def __init__(self, prefix="", infix="", suffix="",
                       numprefix="", numinfix="", numsuffix="",
                       denomprefix="", denominfix="", denomsuffix="",
                       plus="", minus="-", minuspos=0, over=r"{{%s}\over{%s}}",
                       equaldenom=0, skip1=1, skipnum0=1, skipnum1=1, skipdenom1=1,
                       labelattrs=[text.mathmode]):
        r"""initializes the instance
        - prefix, infix, and suffix (strings) are added at the begin,
          immediately after the minus, and at the end of the label,
          respectively
        - prefixnum, infixnum, and suffixnum (strings) are added
          to the labels numerator correspondingly
        - prefixdenom, infixdenom, and suffixdenom (strings) are added
          to the labels denominator correspondingly
        - plus or minus (string) is inserted for non-negative or negative numbers
        - minuspos is an integer, which determines the position, where the
          plus or minus sign has to be placed; the following values are allowed:
            1 - writes the plus or minus in front of the numerator
            0 - writes the plus or minus in front of the hole fraction
           -1 - writes the plus or minus in front of the denominator
        - over (string) is taken as a format string generating the
          fraction bar; it has to contain exactly two string insert
          operators "%s" -- the first for the numerator and the second
          for the denominator; by far the most common examples are
          r"{{%s}\over{%s}}" and "{{%s}/{%s}}"
        - usually the numerator and denominator are canceled; however,
          when equaldenom is set, the least common multiple of all
          denominators is used
        - skip1 (boolean) just prints the prefix, the plus or minus,
          the infix and the suffix, when the value is plus or minus one
          and at least one of prefix, infix and the suffix is present
        - skipnum0 (boolean) just prints a zero instead of
          the hole fraction, when the numerator is zero;
          no prefixes, infixes, and suffixes are taken into account
        - skipnum1 (boolean) just prints the numprefix, the plus or minus,
          the numinfix and the numsuffix, when the num value is plus or minus one
          and at least one of numprefix, numinfix and the numsuffix is present
        - skipdenom1 (boolean) just prints the numerator instead of
          the hole fraction, when the denominator is one and none of the parameters
          denomprefix, denominfix and denomsuffix are set and minuspos is not -1 or the
          fraction is positive
        - labelattrs is a list of attributes for a texrunners text method;
          None is considered as an empty list; labelattrs might be changed
          in the painter as well"""
        self.prefix = prefix
        self.infix = infix
        self.suffix = suffix
        self.numprefix = numprefix
        self.numinfix = numinfix
        self.numsuffix = numsuffix
        self.denomprefix = denomprefix
        self.denominfix = denominfix
        self.denomsuffix = denomsuffix
        self.plus = plus
        self.minus = minus
        self.minuspos = minuspos
        self.over = over
        self.equaldenom = equaldenom
        self.skip1 = skip1
        self.skipnum0 = skipnum0
        self.skipnum1 = skipnum1
        self.skipdenom1 = skipdenom1
        self.labelattrs = labelattrs

    def gcd(self, *n):
        """returns the greates common divisor of all elements in n
        - the elements of n must be non-negative integers
        - return None if the number of elements is zero
        - the greates common divisor is not affected when some
          of the elements are zero, but it becomes zero when
          all elements are zero"""
        if len(n) == 2:
            i, j = n
            if i < j:
                i, j = j, i
            while j > 0:
                i, (dummy, j) = j, divmod(i, j)
            return i
        if len(n):
            res = n[0]
            for i in n[1:]:
                res = self.gcd(res, i)
            return res

    def lcm(self, *n):
        """returns the least common multiple of all elements in n
        - the elements of n must be non-negative integers
        - return None if the number of elements is zero
        - the least common multiple is zero when some of the
          elements are zero"""
        if len(n):
            res = n[0]
            for i in n[1:]:
                res = divmod(res * i, self.gcd(res, i))[0]
            return res

    def labels(self, ticks):
        labeledticks = []
        for tick in ticks:
            if tick.label is None and tick.labellevel is not None:
                labeledticks.append(tick)
                tick.temp_rationalnum = tick.num
                tick.temp_rationaldenom = tick.denom
                tick.temp_rationalminus = 1
                if tick.temp_rationalnum < 0:
                    tick.temp_rationalminus = -tick.temp_rationalminus
                    tick.temp_rationalnum = -tick.temp_rationalnum
                if tick.temp_rationaldenom < 0:
                    tick.temp_rationalminus = -tick.temp_rationalminus
                    tick.temp_rationaldenom = -tick.temp_rationaldenom
                gcd = self.gcd(tick.temp_rationalnum, tick.temp_rationaldenom)
                (tick.temp_rationalnum, dummy1), (tick.temp_rationaldenom, dummy2) = divmod(tick.temp_rationalnum, gcd), divmod(tick.temp_rationaldenom, gcd)
        if self.equaldenom:
            equaldenom = self.lcm(*[tick.temp_rationaldenom for tick in ticks if tick.label is None])
            if equaldenom is not None:
                for tick in labeledticks:
                    factor, dummy = divmod(equaldenom, tick.temp_rationaldenom)
                    tick.temp_rationalnum, tick.temp_rationaldenom = factor * tick.temp_rationalnum, factor * tick.temp_rationaldenom
        for tick in labeledticks:
            rationalminus = rationalnumminus = rationaldenomminus = ""
            if tick.temp_rationalminus == -1:
                plusminus = self.minus
            else:
                plusminus = self.plus
            if self.minuspos == 0:
                rationalminus = plusminus
            elif self.minuspos == 1:
                rationalnumminus = plusminus
            elif self.minuspos == -1:
                rationaldenomminus = plusminus
            else:
                raise RuntimeError("invalid minuspos")
            if self.skipnum0 and tick.temp_rationalnum == 0:
                tick.label = "0"
            elif (self.skip1 and self.skipdenom1 and tick.temp_rationalnum == 1 and tick.temp_rationaldenom == 1 and
                  (len(self.prefix) or len(self.infix) or len(self.suffix)) and
                  not len(rationalnumminus) and not len(self.numprefix) and not len(self.numinfix) and not len(self.numsuffix) and
                  not len(rationaldenomminus) and not len(self.denomprefix) and not len(self.denominfix) and not len(self.denomsuffix)):
                tick.label = "%s%s%s%s" % (self.prefix, rationalminus, self.infix, self.suffix)
            else:
                if self.skipnum1 and tick.temp_rationalnum == 1 and (len(self.numprefix) or len(self.numinfix) or len(self.numsuffix)):
                    tick.temp_rationalnum = "%s%s%s%s" % (self.numprefix, rationalnumminus, self.numinfix, self.numsuffix)
                else:
                    tick.temp_rationalnum = "%s%s%s%i%s" % (self.numprefix, rationalnumminus, self.numinfix, tick.temp_rationalnum, self.numsuffix)
                if self.skipdenom1 and tick.temp_rationaldenom == 1 and not len(rationaldenomminus) and not len(self.denomprefix) and not len(self.denominfix) and not len(self.denomsuffix):
                    rational = tick.temp_rationalnum
                else:
                    tick.temp_rationaldenom = "%s%s%s%i%s" % (self.denomprefix, rationaldenomminus, self.denominfix, tick.temp_rationaldenom, self.denomsuffix)
                    rational = self.over % (tick.temp_rationalnum, tick.temp_rationaldenom)
                tick.label = "%s%s%s%s%s" % (self.prefix, rationalminus, self.infix, rational, self.suffix)
            tick.labelattrs = tick.labelattrs + self.labelattrs

            # del tick.temp_rationalnum    # we've inserted those temporary variables ... and do not care any longer about them
            # del tick.temp_rationaldenom
            # del tick.temp_rationalminus

