# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2005-2006 André Wobst <wobsta@users.sourceforge.net>
# Copyright (C) 2006 Jörg Lehmann <joergl@users.sourceforge.net>
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

import array, binascii, re
try:
    import zlib
    haszlib = 1
except ImportError:
    haszlib = 0

try:
    enumerate([])
except NameError:
    # fallback implementation for Python 2.2 and below
    def enumerate(list):
        return zip(xrange(len(list)), list)

from pyx import trafo
from pyx.path import path, moveto_pt, lineto_pt, curveto_pt, closepath
import encoding

try:
    from _t1code import *
except:
    from t1code import *


class T1context:

    def __init__(self, t1font):
        """context for T1cmd evaluation"""
        self.t1font = t1font

        # state description
        self.x = None
        self.y = None
        self.wx = None
        self.wy = None
        self.t1stack = []
        self.psstack = []


######################################################################
# T1 commands
# Note, that the T1 commands are variable-free except for plain number,
# which are stored as integers. All other T1 commands exist as a single
# instance only

T1cmds = {}
T1subcmds = {}

class T1cmd:

    def __init__(self, code, subcmd=0):
        self.code = code
        self.subcmd = subcmd
        if subcmd:
            T1subcmds[code] = self
        else:
            T1cmds[code] = self

    def __str__(self):
        """returns a string representation of the T1 command"""
        raise NotImplementedError

    def updatepath(self, path, trafo, context):
        """update path instance applying trafo to the points"""
        raise NotImplementedError

    def gathercalls(self, seacglyphs, subrs, othersubrs, context):
        """gather dependancy information

        subrs is the "called-subrs" dictionary. gathercalls will insert the
        subr number as key having the value 1, i.e. subrs.keys() will become the
        numbers of used subrs. Similar seacglyphs will contain all glyphs in
        composite characters (subrs and othersubrs for those glyphs will also
        already be included) and othersubrs the othersubrs called.

        This method might will not properly update all information in the
        context (especially consuming values from the stack) and will also skip
        various tests for performance reasons. For most T1 commands it just
        doesn't need to do anything.
        """
        pass


# commands for starting and finishing

class _T1endchar(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 14)

    def __str__(self):
        return "endchar"

    def updatepath(self, path, trafo, context):
        pass

T1endchar = _T1endchar()


class _T1hsbw(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 13)

    def __str__(self):
        return "hsbw"

    def updatepath(self, path, trafo, context):
        sbx = context.t1stack.pop(0)
        wx = context.t1stack.pop(0)
        path.append(moveto_pt(*trafo.apply_pt(sbx, 0)))
        context.x = sbx
        context.y = 0
        context.wx = wx
        context.wy = 0

T1hsbw = _T1hsbw()


class _T1seac(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 6, subcmd=1)

    def __str__(self):
        return "seac"

    def updatepath(self, path, atrafo, context):
        sab = context.t1stack.pop(0)
        adx = context.t1stack.pop(0)
        ady = context.t1stack.pop(0)
        bchar = context.t1stack.pop(0)
        achar = context.t1stack.pop(0)
        aglyph = encoding.adobestandardencoding.decode(achar)
        bglyph = encoding.adobestandardencoding.decode(bchar)
        context.t1font.updateglyphpath(bglyph, path, atrafo, context)
        atrafo = atrafo * trafo.translate_pt(adx-sab, ady)
        context.t1font.updateglyphpath(aglyph, path, atrafo, context)

    def gathercalls(self, seacglyphs, subrs, othersubrs, context):
        bchar = context.t1stack.pop()
        achar = context.t1stack.pop()
        aglyph = encoding.adobestandardencoding.decode(achar)
        bglyph = encoding.adobestandardencoding.decode(bchar)
        seacglyphs[aglyph] = 1
        seacglyphs[bglyph] = 1
        context.t1font.gatherglyphcalls(bglyph, seacglyphs, subrs, othersubrs, context)
        context.t1font.gatherglyphcalls(aglyph, seacglyphs, subrs, othersubrs, context)

T1seac = _T1seac()


class _T1sbw(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 7, subcmd=1)

    def __str__(self):
        return "sbw"

    def updatepath(self, path, trafo, context):
        sbx = context.t1stack.pop(0)
        sby = context.t1stack.pop(0)
        wx = context.t1stack.pop(0)
        wy = context.t1stack.pop(0)
        path.append(moveto_pt(*trafo.apply_pt(sbx, sby)))
        context.x = sbx
        context.y = sby
        context.wx = wx
        context.wy = wy

T1sbw = _T1sbw()


# path construction commands

class _T1closepath(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 9)

    def __str__(self):
        return "closepath"

    def updatepath(self, path, trafo, context):
        path.append(closepath())
        # The closepath in T1 is different from PostScripts in that it does
        # *not* modify the current position; hence we need to add an additional
        # moveto here ...
        path.append(moveto_pt(*trafo.apply_pt(context.x, context.y)))

T1closepath = _T1closepath()


class _T1hlineto(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 6)

    def __str__(self):
        return "hlineto"

    def updatepath(self, path, trafo, context):
        dx = context.t1stack.pop(0)
        path.append(lineto_pt(*trafo.apply_pt(context.x + dx, context.y)))
        context.x += dx

T1hlineto = _T1hlineto()


class _T1hmoveto(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 22)

    def __str__(self):
        return "hmoveto"

    def updatepath(self, path, trafo, context):
        dx = context.t1stack.pop(0)
        path.append(moveto_pt(*trafo.apply_pt(context.x + dx, context.y)))
        context.x += dx

T1hmoveto = _T1hmoveto()


class _T1hvcurveto(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 31)

    def __str__(self):
        return "hvcurveto"

    def updatepath(self, path, trafo, context):
        dx1 = context.t1stack.pop(0)
        dx2 = context.t1stack.pop(0)
        dy2 = context.t1stack.pop(0)
        dy3 = context.t1stack.pop(0)
        path.append(curveto_pt(*(trafo.apply_pt(context.x + dx1,       context.y) +
                                 trafo.apply_pt(context.x + dx1 + dx2, context.y + dy2) +
                                 trafo.apply_pt(context.x + dx1 + dx2, context.y + dy2 + dy3))))
        context.x += dx1+dx2
        context.y += dy2+dy3

T1hvcurveto = _T1hvcurveto()


class _T1rlineto(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 5)

    def __str__(self):
        return "rlineto"

    def updatepath(self, path, trafo, context):
        dx = context.t1stack.pop(0)
        dy = context.t1stack.pop(0)
        path.append(lineto_pt(*trafo.apply_pt(context.x + dx, context.y + dy)))
        context.x += dx
        context.y += dy

T1rlineto = _T1rlineto()


class _T1rmoveto(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 21)

    def __str__(self):
        return "rmoveto"

    def updatepath(self, path, trafo, context):
        dx = context.t1stack.pop(0)
        dy = context.t1stack.pop(0)
        path.append(moveto_pt(*trafo.apply_pt(context.x + dx, context.y + dy)))
        context.x += dx
        context.y += dy

T1rmoveto = _T1rmoveto()


class _T1rrcurveto(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 8)

    def __str__(self):
        return "rrcurveto"

    def updatepath(self, path, trafo, context):
        dx1 = context.t1stack.pop(0)
        dy1 = context.t1stack.pop(0)
        dx2 = context.t1stack.pop(0)
        dy2 = context.t1stack.pop(0)
        dx3 = context.t1stack.pop(0)
        dy3 = context.t1stack.pop(0)
        path.append(curveto_pt(*(trafo.apply_pt(context.x + dx1,             context.y + dy1) +
                                 trafo.apply_pt(context.x + dx1 + dx2,       context.y + dy1 + dy2) +
                                 trafo.apply_pt(context.x + dx1 + dx2 + dx3, context.y + dy1 + dy2 + dy3))))
        context.x += dx1+dx2+dx3
        context.y += dy1+dy2+dy3

T1rrcurveto = _T1rrcurveto()


class _T1vlineto(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 7)

    def __str__(self):
        return "vlineto"

    def updatepath(self, path, trafo, context):
        dy = context.t1stack.pop(0)
        path.append(lineto_pt(*trafo.apply_pt(context.x, context.y + dy)))
        context.y += dy

T1vlineto = _T1vlineto()


class _T1vmoveto(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 4)

    def __str__(self):
        return "vmoveto"

    def updatepath(self, path, trafo, context):
        dy = context.t1stack.pop(0)
        path.append(moveto_pt(*trafo.apply_pt(context.x, context.y + dy)))
        context.y += dy

T1vmoveto = _T1vmoveto()


class _T1vhcurveto(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 30)

    def __str__(self):
        return "vhcurveto"

    def updatepath(self, path, trafo, context):
        dy1 = context.t1stack.pop(0)
        dx2 = context.t1stack.pop(0)
        dy2 = context.t1stack.pop(0)
        dx3 = context.t1stack.pop(0)
        path.append(curveto_pt(*(trafo.apply_pt(context.x,             context.y + dy1) +
                                 trafo.apply_pt(context.x + dx2,       context.y + dy1 + dy2) +
                                 trafo.apply_pt(context.x + dx2 + dx3, context.y + dy1 + dy2))))
        context.x += dx2+dx3
        context.y += dy1+dy2

T1vhcurveto = _T1vhcurveto()


# hint commands

class _T1dotsection(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 0, subcmd=1)

    def __str__(self):
        return "dotsection"

    def updatepath(self, path, trafo, context):
        pass

T1dotsection = _T1dotsection()


class _T1hstem(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 1)

    def __str__(self):
        return "hstem"

    def updatepath(self, path, trafo, context):
        y = context.t1stack.pop(0)
        dy = context.t1stack.pop(0)

T1hstem = _T1hstem()


class _T1hstem3(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 2, subcmd=1)

    def __str__(self):
        return "hstem3"

    def updatepath(self, path, trafo, context):
        y0 = context.t1stack.pop(0)
        dy0 = context.t1stack.pop(0)
        y1 = context.t1stack.pop(0)
        dy1 = context.t1stack.pop(0)
        y2 = context.t1stack.pop(0)
        dy2 = context.t1stack.pop(0)

T1hstem3 = _T1hstem3()


class _T1vstem(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 3)

    def __str__(self):
        return "vstem"

    def updatepath(self, path, trafo, context):
        x = context.t1stack.pop(0)
        dx = context.t1stack.pop(0)

T1vstem = _T1vstem()


class _T1vstem3(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 1, subcmd=1)

    def __str__(self):
        return "vstem3"

    def updatepath(self, path, trafo, context):
        self.x0 = context.t1stack.pop(0)
        self.dx0 = context.t1stack.pop(0)
        self.x1 = context.t1stack.pop(0)
        self.dx1 = context.t1stack.pop(0)
        self.x2 = context.t1stack.pop(0)
        self.dx2 = context.t1stack.pop(0)

T1vstem3 = _T1vstem3()


# arithmetic command

class _T1div(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 12, subcmd=1)

    def __str__(self):
        return "div"

    def updatepath(self, path, trafo, context):
        num2 = context.t1stack.pop()
        num1 = context.t1stack.pop()
        context.t1stack.append(divmod(num1, num2)[0])

    def gathercalls(self, seacglyphs, subrs, othersubrs, context):
        num2 = context.t1stack.pop()
        num1 = context.t1stack.pop()
        context.t1stack.append(divmod(num1, num2)[0])

T1div = _T1div()


# subroutine commands

class _T1callothersubr(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 16, subcmd=1)

    def __str__(self):
        return "callothersubr"

    def updatepath(self, path, trafo, context):
        othersubrnumber = context.t1stack.pop()
        n = context.t1stack.pop()
        for i in range(n):
            context.psstack.append(context.t1stack.pop())

    def gathercalls(self, seacglyphs, subrs, othersubrs, context):
        othersubrnumber = context.t1stack.pop()
        othersubrs[othersubrnumber] = 1
        n = context.t1stack.pop()
        for i in range(n):
            context.psstack.append(context.t1stack.pop())

T1callothersubr = _T1callothersubr()


class _T1callsubr(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 10)

    def __str__(self):
        return "callsubr"

    def updatepath(self, path, trafo, context):
        subr = context.t1stack.pop()
        context.t1font.updatesubrpath(subr, path, trafo, context)

    def gathercalls(self, seacglyphs, subrs, othersubrs, context):
        subr = context.t1stack.pop()
        subrs[subr] = 1
        context.t1font.gathersubrcalls(subr, seacglyphs, subrs, othersubrs, context)

T1callsubr = _T1callsubr()


class _T1pop(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 17, subcmd=1)

    def __str__(self):
        return "pop"

    def updatepath(self, path, trafo, context):
        context.t1stack.append(context.psstack.pop())

    def gathercalls(self, seacglyphs, subrs, othersubrs, context):
        context.t1stack.append(context.psstack.pop())

T1pop = _T1pop()


class _T1return(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 11)

    def __str__(self):
        return "return"

    def updatepath(self, path, trafo, context):
        pass

T1return = _T1return()


class _T1setcurrentpoint(T1cmd):

    def __init__(self):
        T1cmd.__init__(self, 33, subcmd=1)

    def __str__(self):
        return "setcurrentpoint" % self.x, self.y

    def updatepath(self, path, trafo, context):
        x = context.t1stack.pop(0)
        y = context.t1stack.pop(0)
        path.append(moveto_pt(*trafo.apply_pt(x, y)))
        context.x = x
        context.y = y

T1setcurrentpoint = _T1setcurrentpoint()


######################################################################

class cursor:
    """cursor to read a string token by token"""

    def __init__(self, data, startstring, eattokensep=1, tokenseps=" \t\r\n", tokenstarts="()<>[]{}/%"):
        """creates a cursor for the string data

        startstring is a string at which the cursor should start at. The first
        ocurance of startstring is used. When startstring is not in data, an
        exception is raised, otherwise the cursor is set to the position right
        after the startstring. When eattokenseps is set, startstring must be
        followed by a tokensep and this first tokensep is also consumed.
        tokenseps is a string containing characters to be used as token
        separators. tokenstarts is a string containing characters which 
        directly (even without intermediate token separator) start a new token.
        """
        self.data = data
        self.pos = self.data.index(startstring) + len(startstring)
        self.tokenseps = tokenseps
        self.tokenstarts = tokenstarts
        if eattokensep:
            if self.data[self.pos] not in self.tokenstarts:
                if self.data[self.pos] not in self.tokenseps:
                    raise ValueError("cursor initialization string is not followed by a token separator")
                self.pos += 1

    def gettoken(self):
        """get the next token

        Leading token separators and comments are silently consumed. The first token
        separator after the token is also silently consumed."""
        while self.data[self.pos] in self.tokenseps:
            self.pos += 1
        # ignore comments including subsequent whitespace characters
        while self.data[self.pos] == "%":
            while self.data[self.pos] not in "\r\n":
                self.pos += 1
            while self.data[self.pos] in self.tokenseps:
                self.pos += 1
        startpos = self.pos
        while self.data[self.pos] not in self.tokenseps:
            # any character in self.tokenstarts ends the token
            if self.pos>startpos and self.data[self.pos] in self.tokenstarts:
                break
            self.pos += 1
        result = self.data[startpos:self.pos]
        if self.data[self.pos] in self.tokenseps:
            self.pos += 1 # consume a single tokensep
        return result

    def getint(self):
        """get the next token as an integer"""
        return int(self.gettoken())

    def getbytes(self, count):
        """get the next count bytes"""
        startpos = self.pos
        self.pos += count
        return self.data[startpos: self.pos]


class T1font:

    eexecr = 55665
    charstringr = 4330

    def __init__(self, data1, data2eexec, data3):
        """initializes a t1font instance

        data1 and data3 are the two clear text data parts and data2 is
        the binary data part"""
        self.data1 = data1
        self._data2eexec = data2eexec
        self.data3 = data3

        # marker and value for decoded data
        self._data2 = None
        # note that data2eexec is set to none by setsubrcmds and setglyphcmds
        # this *also* denotes, that data2 is out-of-date; hence they are both
        # marked by an _ and getdata2 and getdata2eexec will properly resolve
        # the current state of decoding ...

        # marker and value for standard encoding check
        self.encoding = None

    def _eexecdecode(self, code):
        """eexec decoding of code"""
        return decoder(code, self.eexecr, 4)

    def _charstringdecode(self, code):
        """charstring decoding of code"""
        return decoder(code, self.charstringr, self.lenIV)

    def _eexecencode(self, data):
        """eexec encoding of data"""
        return encoder(data, self.eexecr, "PyX!")

    def _charstringencode(self, data):
        """eexec encoding of data"""
        return encoder(data, self.charstringr, "PyX!"[:self.lenIV])

    lenIVpattern = re.compile("/lenIV\s+(\d+)\s+def\s+")
    flexhintsubrs = [[3, 0, T1callothersubr, T1pop, T1pop, T1setcurrentpoint, T1return],
                     [0, 1, T1callothersubr, T1return],
                     [0, 2, T1callothersubr, T1return],
                     [T1return]]

    def _encoding(self):
        """helper method to lookup the encoding in the font"""
        c = cursor(self.data1, "/Encoding")
        token1 = c.gettoken()
        token2 = c.gettoken()
        if token1 == "StandardEncoding" and token2 == "def":
            self.encoding = encoding.adobestandardencoding
        else:
            encvector = [None]*256
            while 1:
                self.encodingstart = c.pos
                if c.gettoken() == "dup":
                    break
            while 1:
                i = c.getint()
                glyph = c.gettoken()
                if 0 <= i < 256:
                    encvector[i] = glyph[1:]
                token = c.gettoken(); assert token == "put"
                self.encodingend = c.pos
                token = c.gettoken()
                if token == "readonly" or token == "def":
                    break
                assert token == "dup"
            self.encoding = encoding.encoding(encvector)

    def _data2decode(self):
        """decodes data2eexec to the data2 string and the subr and glyphs dictionary

        It doesn't make sense to call this method twice -- check the content of
        data2 before calling. The method also keeps the subrs and charstrings
        start and end positions for later use."""
        self._data2 = self._eexecdecode(self._data2eexec)

        m = self.lenIVpattern.search(self._data2)
        if m:
            self.lenIV = int(m.group(1))
        else:
            self.lenIV = 4
        self.emptysubr = self._charstringencode(chr(11))

        # extract Subrs
        c = cursor(self._data2, "/Subrs")
        self.subrsstart = c.pos
        arraycount = c.getint()
        token = c.gettoken(); assert token == "array"
        self.subrs = []
        for i in range(arraycount):
            token = c.gettoken(); assert token == "dup"
            token = c.getint(); assert token == i
            size = c.getint()
            if not i:
                self.subrrdtoken = c.gettoken()
            else:
                token = c.gettoken(); assert token == self.subrrdtoken
            self.subrs.append(c.getbytes(size))
            token = c.gettoken()
            if token == "noaccess":
                token = "%s %s" % (token, c.gettoken())
            if not i:
                self.subrnptoken = token
            else:
                assert token == self.subrnptoken
        self.subrsend = c.pos

        # hasflexhintsubrs is a boolean indicating that the font uses flex or
        # hint replacement subrs as specified by Adobe (tm). When it does, the
        # first 4 subrs should all be copied except when none of them are used
        # in the stripped version of the font since we than get a font not
        # using flex or hint replacement subrs at all.
        self.hasflexhintsubrs = (arraycount >= len(self.flexhintsubrs) and
                                 [self.getsubrcmds(i)
                                  for i in range(len(self.flexhintsubrs))] == self.flexhintsubrs)

        # extract glyphs
        self.glyphs = {}
        self.glyphlist = [] # we want to keep the order of the glyph names
        c = cursor(self._data2, "/CharStrings")
        self.charstringsstart = c.pos
        c.getint()
        token = c.gettoken(); assert token == "dict"
        token = c.gettoken(); assert token == "dup"
        token = c.gettoken(); assert token == "begin"
        first = 1
        while 1:
            chartoken = c.gettoken()
            if chartoken == "end":
                break
            assert chartoken[0] == "/"
            size = c.getint()
            if first:
                self.glyphrdtoken = c.gettoken()
            else:
                token = c.gettoken(); assert token == self.glyphrdtoken
            self.glyphlist.append(chartoken[1:])
            self.glyphs[chartoken[1:]] = c.getbytes(size)
            if first:
                self.glyphndtoken = c.gettoken()
            else:
                token = c.gettoken(); assert token == self.glyphndtoken
            first = 0
        self.charstringsend = c.pos
        assert not self.subrs or self.subrrdtoken == self.glyphrdtoken

    def _cmds(self, code):
        """return a list of T1cmd's for encoded charstring data in code"""
        code = array.array("B", self._charstringdecode(code))
        cmds = []
        while code:
            x = code.pop(0)
            if x == 12: # this starts an escaped cmd
                cmds.append(T1subcmds[code.pop(0)])
            elif 0 <= x < 32: # those are cmd's
                cmds.append(T1cmds[x])
            elif 32 <= x <= 246: # short ints
                cmds.append(x-139)
            elif 247 <= x <= 250: # mid size ints
                cmds.append(((x - 247)*256) + code.pop(0) + 108)
            elif 251 <= x <= 254: # mid size ints
                cmds.append(-((x - 251)*256) - code.pop(0) - 108)
            else: # x = 255, i.e. full size ints
                y = ((code.pop(0)*256l+code.pop(0))*256+code.pop(0))*256+code.pop(0)
                if y > (1l << 31):
                    cmds.append(y - (1l << 32))
                else:
                    cmds.append(y)
        return cmds

    def _code(self, cmds):
        """return an encoded charstring data for list of T1cmd's in cmds"""
        code = array.array("B")
        for cmd in cmds:
            try:
                if cmd.subcmd:
                    code.append(12)
                code.append(cmd.code)
            except AttributeError:
                if -107 <= cmd <= 107:
                    code.append(cmd+139)
                elif 108 <= cmd <= 1131:
                    a, b = divmod(cmd-108, 256)
                    code.append(a+247)
                    code.append(b)
                elif -1131 <= cmd <= -108:
                    a, b = divmod(-cmd-108, 256)
                    code.append(a+251)
                    code.append(b)
                else:
                    if cmd < 0:
                        cmd += 1l << 32
                    cmd, x4 = divmod(cmd, 256)
                    cmd, x3 = divmod(cmd, 256)
                    x1, x2 = divmod(cmd, 256)
                    code.append(255)
                    code.append(x1)
                    code.append(x2)
                    code.append(x3)
                    code.append(x4)
        return self._charstringencode(code.tostring())

    def getsubrcmds(self, subr):
        """return a list of T1cmd's for subr subr"""
        if not self._data2:
            self._data2decode()
        return self._cmds(self.subrs[subr])

    def getglyphcmds(self, glyph):
        """return a list of T1cmd's for glyph glyph"""
        if not self._data2:
            self._data2decode()
        return self._cmds(self.glyphs[glyph])

    def setsubrcmds(self, subr, cmds):
        """replaces the T1cmd's by the list cmds for subr subr"""
        if not self._data2:
            self._data2decode()
        self._data2eexec = None
        self.subrs[subr] = self._code(cmds)

    def setglyphcmds(self, glyph, cmds):
        """replaces the T1cmd's by the list cmds for glyph glyph"""
        if not self._data2:
            self._data2decode()
        self._data2eexec = None
        self.glyphs[glyph] = self._code(cmds)

    def updatepath(self, cmds, path, trafo, context):
        for cmd in cmds:
            if isinstance(cmd, T1cmd):
                cmd.updatepath(path, trafo, context)
            else:
                context.t1stack.append(cmd)

    def updatesubrpath(self, subr, path, trafo, context):
        self.updatepath(self.getsubrcmds(subr), path, trafo, context)

    def updateglyphpath(self, glyph, path, trafo, context):
        self.updatepath(self.getglyphcmds(glyph), path, trafo, context)

    def gathercalls(self, cmds, seacglyphs, subrs, othersubrs, context):
        for cmd in cmds:
            if isinstance(cmd, T1cmd):
                cmd.gathercalls(seacglyphs, subrs, othersubrs, context)
            else:
                context.t1stack.append(cmd)

    def gathersubrcalls(self, subr, seacglyphs, subrs, othersubrs, context):
        self.gathercalls(self.getsubrcmds(subr), seacglyphs, subrs, othersubrs, context)

    def gatherglyphcalls(self, glyph, seacglyphs, subrs, othersubrs, context):
        self.gathercalls(self.getglyphcmds(glyph), seacglyphs, subrs, othersubrs, context)

    fontmatrixpattern = re.compile("/FontMatrix\s*\[\s*(-?[0-9.]+)\s+(-?[0-9.]+)\s+(-?[0-9.]+)\s+(-?[0-9.]+)\s+(-?[0-9.]+)\s+(-?[0-9.]+)\s*\]\s*(readonly\s+)?def")

    def getglyphpathwxwy_pt(self, glyph, size):
        m = self.fontmatrixpattern.search(self.data1)
        m11, m12, m21, m22, v1, v2 = map(float, m.groups()[:6])
        t = trafo.trafo_pt(matrix=((m11, m12), (m21, m22)), vector=(v1, v2)).scaled(size)
        context = T1context(self)
        p = path()
        self.updateglyphpath(glyph, p, t, context)
        wx, wy = t.apply_pt(context.wx, context.wy)
        return p, wx, wy

    def getglyphpath(self, glyph, size):
        """return a PyX path for glyph named glyph"""
        return self.getglyphpathwxwy_pt(glyph, size)[0]

    def getglyphwxwy_pt(self, glyph, size):
        return self.getglyphpathwxwy_pt(glyph, size)[1:]

    def getdata2(self, subrs=None, glyphs=None):
        """makes a data2 string

        subrs is a dict containing those subrs numbers as keys,
        which are to be contained in the subrsstring to be created.
        If subrs is None, all subrs in self.subrs will be used.
        The subrs dict might be modified *in place*.

        glyphs is a dict containing those glyph names as keys,
        which are to be contained in the charstringsstring to be created.
        If glyphs is None, all glyphs in self.glyphs will be used."""
        def addsubrs(subrs, result):
            if subrs is not None:
                # some adjustments to the subrs dict
                if subrs:
                    subrsindices = subrs.keys()
                    subrsmin = min(subrsindices)
                    subrsmax = max(subrsindices)
                    if self.hasflexhintsubrs and subrsmin < len(self.flexhintsubrs):
                        # According to the spec we need to keep all the flex and hint subrs
                        # as long as any of it is used.
                        for subr in range(len(self.flexhintsubrs)):
                            subrs[subr] = 1
                else:
                    subrsmax = -1
            else:
                # build a new subrs dict containing all subrs
                subrs = dict([(subr, 1) for subr in range(len(self.subrs))])
                subrsmax = len(self.subrs) - 1

            # build the string from all selected subrs
            result.append("%d array\n" % (subrsmax + 1))
            for subr in range(subrsmax+1):
                if subrs.has_key(subr):
                    code = self.subrs[subr]
                else:
                    code = self.emptysubr
                result.append("dup %d %d %s %s %s\n" % (subr, len(code), self.subrrdtoken, code, self.subrnptoken))

        def addcharstrings(glyphs, result):
            result.append("%d dict dup begin\n" % (glyphs is None and len(self.glyphlist) or len(glyphs)))
            for glyph in self.glyphlist:
                if glyphs is None or glyphs.has_key(glyph):
                    result.append("/%s %d %s %s %s\n" % (glyph, len(self.glyphs[glyph]), self.glyphrdtoken, self.glyphs[glyph], self.glyphndtoken))
            result.append("end\n")

        if self.subrsstart < self.charstringsstart:
            result = [self._data2[:self.subrsstart]]
            addsubrs(subrs, result)
            result.append(self._data2[self.subrsend:self.charstringsstart])
            addcharstrings(glyphs, result)
            result.append(self._data2[self.charstringsend:])
        else:
            result = [self._data2[:self.charstringsstart]]
            addcharstrings(glyphs, result)
            result.append(self._data2[self.charstringsend:self.subrsstart])
            addsubrs(subrs, result)
            result.append(self._data2[self.subrsend:])
        return "".join(result)

    def getdata2eexec(self):
        if self._data2eexec:
            return self._data2eexec
        # note that self._data2 is out-of-date here too, hence we need to call getdata2
        return self._eexecencode(self.getdata2())

    newlinepattern = re.compile("\s*[\r\n]\s*")
    uniqueidpattern = re.compile("/UniqueID\s+\d+\s+def\s+")

    def getstrippedfont(self, glyphs):
        """create a T1font instance containing only certain glyphs

        glyphs is a dict having the glyph names to be contained as keys.
        The glyphs dict might be modified *in place*.
        """
        # TODO: we could also strip othersubrs to those actually used

        # collect information about used glyphs and subrs
        seacglyphs = {}
        subrs = {}
        othersubrs = {}
        for glyph in glyphs.keys():
            self.gatherglyphcalls(glyph, seacglyphs, subrs, othersubrs, T1context(self))
        # while we have gathered all subrs for the seacglyphs alreadys, we
        # might have missed the glyphs themself (when they are not used stand-alone)
        glyphs.update(seacglyphs)
        glyphs[".notdef"] = 1

        # strip data1
        if not self.encoding:
            self._encoding()
        if self.encoding is encoding.adobestandardencoding:
            data1 = self.data1
        else:
            encodingstrings = []
            for char, glyph in enumerate(self.encoding.encvector):
                if glyph in glyphs.keys():
                    encodingstrings.append("dup %i /%s put\n" % (char, glyph))
            data1 = self.data1[:self.encodingstart] + "".join(encodingstrings) + self.data1[self.encodingend:]
        data1 = self.newlinepattern.subn("\n", data1)[0]
        data1 = self.uniqueidpattern.subn("", data1)[0]

        # strip data2
        data2 = self.uniqueidpattern.subn("", self.getdata2(subrs, glyphs))[0]

        # strip data3
        data3 = self.newlinepattern.subn("\n", self.data3)[0]

        # create and return the new font instance
        return T1font(data1.rstrip() + "\n", self._eexecencode(data2), data3.rstrip() + "\n")

    def getflags(self):
        # As a simple heuristics we assume non-symbolic fonts if and only
        # if the Adobe standard encoding is used. All other font flags are
        # not specified here.
        if not self.encoding:
            self._encoding()
        if self.encoding is encoding.adobestandardencoding:
            return 32
        return 4

    def outputPFA(self, file):
        """output the T1font in PFA format"""
        file.write(self.data1)
        data2eexechex = binascii.b2a_hex(self.getdata2eexec())
        linelength = 64
        for i in range((len(data2eexechex)-1)/linelength + 1):
            file.write(data2eexechex[i*linelength: i*linelength+linelength])
            file.write("\n")
        file.write(self.data3)

    def outputPFB(self, file):
        """output the T1font in PFB format"""
        data2eexec = self.getdata2eexec()
        def pfblength(data):
            l = len(data)
            l, x1 = divmod(l, 256)
            l, x2 = divmod(l, 256)
            x4, x3 = divmod(l, 256)
            return chr(x1) + chr(x2) + chr(x3) + chr(x4)
        file.write("\200\1")
        file.write(pfblength(self.data1))
        file.write(self.data1)
        file.write("\200\2")
        file.write(pfblength(data2eexec))
        file.write(data2eexec)
        file.write("\200\1")
        file.write(pfblength(self.data3))
        file.write(self.data3)
        file.write("\200\3")

    def outputPS(self, file, writer):
        """output the PostScript code for the T1font to the file file"""
        self.outputPFA(file)

    def outputPDF(self, file, writer):
        data2eexec = self.getdata2eexec()
        data3 = self.data3
        # we might be allowed to skip the third part ...
        if (data3.replace("\n", "")
                 .replace("\r", "")
                 .replace("\t", "")
                 .replace(" ", "")) == "0"*512 + "cleartomark":
            data3 = ""

        data = self.data1 + data2eexec + data3
        if writer.compress and haszlib:
            data = zlib.compress(data)

        file.write("<<\n"
                   "/Length %d\n"
                   "/Length1 %d\n"
                   "/Length2 %d\n"
                   "/Length3 %d\n" % (len(data), len(self.data1), len(data2eexec), len(data3)))
        if writer.compress and haszlib:
            file.write("/Filter /FlateDecode\n")
        file.write(">>\n"
                   "stream\n")
        file.write(data)
        file.write("\n"
                   "endstream\n")


class T1pfafont(T1font):

    """create a T1font instance from a pfa font file"""

    def __init__(self, filename):
        d = open(filename, "rb").read()
        # hey, that's quick'n'dirty
        m1 = d.index("eexec") + 6
        m2 = d.index("0"*40)
        data1 = d[:m1]
        data2 = binascii.a2b_hex(d[m1: m2].replace(" ", "").replace("\r", "").replace("\n", ""))
        data3 = d[m2:]
        T1font.__init__(self, data1, data2, data3)


class T1pfbfont(T1font):

    """create a T1font instance from a pfb font file"""

    def __init__(self, filename):
        def pfblength(s):
            if len(s) != 4:
                raise ValueError("invalid string length")
            return (ord(s[0]) +
                    ord(s[1])*256 +
                    ord(s[2])*256*256 +
                    ord(s[3])*256*256*256)
        f = open(filename, "rb")
        mark = f.read(2); assert mark == "\200\1"
        data1 = f.read(pfblength(f.read(4)))
        mark = f.read(2); assert mark == "\200\2"
        data2 = ""
        while mark == "\200\2":
            data2 = data2 + f.read(pfblength(f.read(4)))
            mark = f.read(2)
        assert mark == "\200\1"
        data3 = f.read(pfblength(f.read(4)))
        mark = f.read(2); assert mark == "\200\3"
        assert not f.read(1)
        T1font.__init__(self, data1, data2, data3)

