# -*- coding: ISO-8859-1 -*-
#
#
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

import string

class AFMError(Exception):
    pass

# reader states
_READ_START       = 0
_READ_MAIN        = 1
_READ_DIRECTION   = 2
_READ_CHARMETRICS = 3
_READ_KERNDATA    = 4
_READ_TRACKKERN   = 5
_READ_KERNPAIRS   = 6
_READ_COMPOSITES  = 7
_READ_END         = 8

# various parsing functions
def _parseint(s):
    try:
        return int(s)
    except:
        raise AFMError("Expecting int, got '%s'" % s)

def _parsehex(s):
    try:
        if s[0] != "<" or s[-1] != ">":
            raise AFMError()
        return int(s[1:-1], 16)
    except:
        raise AFMError("Expecting hexadecimal int, got '%s'" % s)

def _parsefloat(s):
    try:
        return float(s)
    except:
        raise AFMError("Expecting float, got '%s'" % s)

def _parsefloats(s, nos):
    try:
        numbers = s.split()
        result = map(float, numbers)
        if len(result) != nos:
            raise AFMError()
    except:
        raise AFMError("Expecting list of %d numbers, got '%s'" % (s, nos))
    return result

def _parsestr(s):
    # XXX: check for invalid characters in s
    return s

def _parsebool(s):
    s = s.rstrip()
    if s == "true":
       return 1
    elif s == "false":
       return 0
    else:
        raise AFMError("Expecting boolean, got '%s'" % s)


class AFMcharmetrics:
    def __init__(self, code, widths=None, vvector=None, name=None, bbox=None, ligatures=None):
        self.code = code
        if widths is None:
            self.widths = [None] * 2
        else:
            self.widths = widths
        self.vvector = vvector
        self.name = name
        self.bbox = bbox
        if ligatures is None:
            self.ligatures = []
        else:
            self.ligatures = ligatures


class AFMtrackkern:
    def __init__(self, degree, min_ptsize, min_kern, max_ptsize, max_kern):
        self.degree = degree
        self.min_ptsize = min_ptsize
        self.min_kern = min_kern
        self.max_ptsize = max_ptsize
        self.max_kern = max_kern


class AFMkernpair:
    def __init__(self, name1, name2, x, y):
        self.name1 = name1
        self.name2 = name2
        self.x = x
        self.y = y


class AFMcomposite:
    def __init__(self, name, parts):
        self.name = name
        self.parts = parts


class AFMfile:

    def __init__(self, filename):
       self.filename = filename
       self.metricssets = 0                     # int, optional
       self.fontname = None                     # str, required
       self.fullname = None                     # str, optional
       self.familyname = None                   # str, optional
       self.weight = None                       # str, optional
       self.fontbbox = None                     # 4 floats, required
       self.version = None                      # str, optional
       self.notice = None                       # str, optional
       self.encodingscheme = None               # str, optional
       self.mappingscheme = None                # int, optional (not present in base font programs)
       self.escchar = None                      # int, required if mappingscheme == 3
       self.characterset = None                 # str, optional
       self.characters = None                   # int, optional
       self.isbasefont = 1                      # bool, optional
       self.vvector = None                      # 2 floats, required if metricssets == 2
       self.isfixedv = None                     # bool, default: true if vvector present, false otherwise
       self.capheight = None                    # float, optional
       self.xheight = None                      # float, optional
       self.ascender = None                     # float, optional
       self.descender = None                    # float, optional
       self.underlinepositions = [None] * 2     # int, optional (for each direction)
       self.underlinethicknesses = [None] * 2   # float, optional (for each direction)
       self.italicangles = [None] * 2           # float, optional (for each direction)
       self.charwidths = [None] * 2             # 2 floats, optional (for each direction)
       self.isfixedpitchs = [None] * 2          # bool, optional (for each direction)
       self.charmetrics = None                  # list of character metrics information, optional
       self.trackkerns = None                   # list of track kernings, optional
       self.kernpairs = [None] * 2              # list of list of kerning pairs (for each direction), optional
       self.composites = None                   # list of composite character data sets, optional
       self.parse()
       if self.isfixedv is None:
           self.isfixedv = self.vvector is not None
       # XXX we should check the constraints on some parameters

    # the following methods process a line when the reader is in the corresponding
    # state and return the new state
    def _processline_start(self, line):
        key, args = line.split(None, 1)
        if key != "StartFontMetrics":
            raise AFMError("Expecting StartFontMetrics, no found")
        return _READ_MAIN, None

    def _processline_main(self, line):
        try:
            key, args = line.split(None, 1)
        except ValueError:
            key = line.rstrip()
        if key == "Comment":
            return _READ_MAIN, None
        elif key == "MetricsSets":
            self.metricssets = _parseint(args)
            if direction is not None:
                raise AFMError("MetricsSets not allowed after first (implicit) StartDirection")
        elif key == "FontName":
            self.fontname = _parsestr(args)
        elif key == "FullName":
            self.fullname = _parsestr(args)
        elif key == "FamilyName":
            self.familyname = _parsestr(args)
        elif key == "Weight":
            self.weight = _parsestr(args)
        elif key == "FontBBox":
            self.fontbbox = _parsefloats(args, 4)
        elif key == "Version":
            self.version = _parsestr(args)
        elif key == "Notice":
            self.notice = _parsestr(args)
        elif key == "EncodingScheme":
            self.encodingscheme = _parsestr(args)
        elif key == "MappingScheme":
            self.mappingscheme = _parseint(args)
        elif key == "EscChar":
            self.escchar = _parseint(args)
        elif key == "CharacterSet":
            self.characterset = _parsestr(args)
        elif key == "Characters":
            self.characters = _parseint(args)
        elif key == "IsBaseFont":
            self.isbasefont = _parsebool(args)
        elif key == "VVector":
            self.vvector = _parsefloats(args, 2)
        elif key == "IsFixedV":
            self.isfixedv = _parsebool(args)
        elif key == "CapHeight":
            self.capheight = _parsefloat(args)
        elif key == "XHeight":
            self.xheight = _parsefloat(args)
        elif key == "Ascender":
            self.ascender = _parsefloat(args)
        elif key == "Descender":
            self.descender = _parsefloat(args)
        elif key == "StartDirection":
            direction = _parseint(args)
            if 0 <= direction <= 2:
                return _READ_DIRECTION, direction
            else:
                raise AFMError("Wrong direction number %d" % direction)
        elif (key == "UnderLinePosition" or key == "UnderlineThickness" or key == "ItalicAngle" or
              key == "Charwidth" or key == "IsFixedPitch"):
            # we implicitly entered a direction section, so we should process the line again
            return self._processline_direction(line, 0)
        elif key == "StartCharMetrics":
            if self.charmetrics is not None:
                raise AFMError("Multiple character metrics sections")
            self.charmetrics = [None] * _parseint(args)
            return _READ_CHARMETRICS, 0
        elif key == "StartKernData":
            return _READ_KERNDATA, None
        elif key == "StartComposites":
            if self.composites is not None:
                raise AFMError("Multiple composite character data sections")
            self.composites = [None] * _parseint(args)
            return _READ_COMPOSITES, 0
        elif key == "EndFontMetrics":
            return _READ_END, None
        elif key[0] in string.lowercase:
            # ignoring private commands
            pass
        return _READ_MAIN, None

    def _processline_direction(self, line, direction):
        try:
            key, args = line.split(None, 1)
        except ValueError:
            key = line.rstrip()
        if key == "UnderLinePosition":
            self.underlinepositions[direction] = _parseint(args)
        elif key == "UnderlineThickness":
            self.underlinethicknesses[direction] = _parsefloat(args)
        elif key == "ItalicAngle":
            self.italicangles[direction] = _parsefloat(args)
        elif key == "Charwidth":
            self.charwidths[direction] = _parsefloats(args, 2)
        elif key == "IsFixedPitch":
            self.isfixedpitchs[direction] = _parsebool(args)
        elif key == "EndDirection":
            return _READ_MAIN, None
        else:
            # we assume that we are implicitly leaving the direction section again,
            # so try to reprocess the line in the header reader state
            return self._processline_main(line)
        return _READ_DIRECTION, direction

    def _processline_charmetrics(self, line, charno):
        if line.rstrip() == "EndCharMetrics":
            if charno != len(self.charmetrics):
                raise AFMError("Fewer character metrics than expected")
            return _READ_MAIN, None
        if charno >= len(self.charmetrics):
            raise AFMError("More character metrics than expected")

        char = None
        for s in line.split(";"):
            s = s.strip()
            if not s:
               continue
            key, args = s.split(None, 1)
            if key == "C":
                if char is not None:
                    raise AFMError("Cannot define char code twice")
                char = AFMcharmetrics(_parseint(args))
            elif key == "CH":
                if char is not None:
                    raise AFMError("Cannot define char code twice")
                char = AFMcharmetrics(_parsehex(args))
            elif key == "WX" or key == "W0X":
                char.widths[0] = _parsefloat(args), 0
            elif key == "W1X":
                char.widths[1] = _parsefloat(args), 0
            elif key == "WY" or key == "W0Y":
                char.widths[0] = 0, _parsefloat(args)
            elif key == "W1Y":
                char.widths[1] = 0, _parsefloat(args)
            elif key == "W" or key == "W0":
                char.widths[0] = _parsefloats(args, 2)
            elif key == "W1":
                char.widths[1] = _parsefloats(args, 2)
            elif key == "VV":
                char.vvector = _parsefloats(args, 2)
            elif key == "N":
                # XXX: we should check that name is valid (no whitespcae, etc.)
                char.name = _parsestr(args)
            elif key == "B":
                char.bbox = _parsefloats(args, 4)
            elif key == "L":
                successor, ligature = args.split(None, 1)
                char.ligatures.append((_parsestr(successor), ligature))
            else:
                raise AFMError("Undefined command in character widths specification: '%s'", s)
        if char is None:
            raise AFMError("Character metrics not defined")

        self.charmetrics[charno] = char
        return _READ_CHARMETRICS, charno+1

    def _processline_kerndata(self, line):
        try:
            key, args = line.split(None, 1)
        except ValueError:
            key = line.rstrip()
        if key == "Comment":
            return _READ_KERNDATA, None
        if key == "StartTrackKern":
            if self.trackkerns is not None:
                raise AFMError("Multiple track kernings data sections")
            self.trackkerns = [None] * _parseint(args)
            return _READ_TRACKKERN, 0
        elif key == "StartKernPairs" or key == "StartKernPairs0":
            if self.kernpairs[0] is not None:
                raise AFMError("Multiple kerning pairs data sections for direction 0")
            self.kernpairs[0] = [None] * _parseint(args)
            return _READ_KERNPAIRS, (0, 0)
        elif key == "StartKernPairs1":
            if self.kernpairs[1] is not None:
                raise AFMError("Multiple kerning pairs data sections for direction 0")
            self.kernpairs[1] = [None] * _parseint(args)
            return _READ_KERNPAIRS, (1, 0)
        elif key == "EndKernData":
            return _READ_MAIN, None
        else:
            raise AFMError("Unsupported key %s in kerning data section" % key)

    def _processline_trackkern(self, line, i):
        try:
            key, args = line.split(None, 1)
        except ValueError:
            key = line.rstrip()
        if key == "Comment":
            return _READ_TRACKKERN, i
        elif key == "TrackKern":
            if i >= len(self.trackkerns):
                raise AFMError("More track kerning data sets than expected")
            degrees, args = args.split(None, 1)
            self.trackkerns[i] = AFMtrackkern(int(degrees), *_parsefloats(args, 4))
            return _READ_TRACKKERN, i+1
        elif key == "EndTrackKern":
            if i < len(self.trackkerns):
                raise AFMError("Fewer track kerning data sets than expected")
            return _READ_KERNDATA, None
        else:
            raise AFMError("Unsupported key %s in kerning data section" % key)

    def _processline_kernpairs(self, line, (direction, i)):
        try:
            key, args = line.split(None, 1)
        except ValueError:
            key = line.rstrip()
        if key == "Comment":
            return _READ_KERNPAIRS, (direction, i)
        elif key == "EndKernPairs":
            if i < len(self.kernpairs[direction]):
                raise AFMError("Fewer kerning pairs than expected")
            return _READ_KERNDATA, None
        else:
            if i >= len(self.kernpairs[direction]):
                raise AFMError("More kerning pairs than expected")
            if key == "KP":
                try:
                    name1, name2, x, y = args.split()
                except:
                    raise AFMError("Expecting name1, name2, x, y, got '%s'" % args)
                self.kernpairs[direction][i] = AFMkernpair(name1, name2, _parsefloat(x), _parsefloat(y))
            elif key == "KPH":
                try:
                    hex1, hex2, x, y = args.split()
                except:
                    raise AFMError("Expecting <hex1>, <hex2>, x, y, got '%s'" % args)
                self.kernpairs[direction][i] = AFMkernpair(_parsehex(hex1), _parsehex(hex2),
                                                           _parsefloat(x), _parsefloat(y))
            elif key == "KPX":
                try:
                    name1, name2, x = args.split()
                except:
                    raise AFMError("Expecting name1, name2, x, got '%s'" % args)
                self.kernpairs[direction][i] = AFMkernpair(name1, name2, _parsefloat(x), 0)
            elif key == "KPY":
                try:
                    name1, name2, y = args.split()
                except:
                    raise AFMError("Expecting name1, name2, x, got '%s'" % args)
                self.kernpairs[direction][i] = AFMkernpair(name1, name2, 0, _parsefloat(y))
            else:
                raise AFMError("Unknown key '%s' in kern pair section" % key)
            return _READ_KERNPAIRS, (direction, i+1)

    def _processline_composites(self, line, i):
        if line.rstrip() == "EndComposites":
            if i < len(self.composites):
                raise AFMError("Fewer composite character data sets than expected")
            return _READ_MAIN, None
        if i >= len(self.composites):
            raise AFMError("More composite character data sets than expected")

        name = None
        no = None
        parts = []
        for s in line.split(";"):
            s = s.strip()
            if not s:
               continue
            key, args = s.split(None, 1)
            if key == "CC":
                try:
                    name, no = args.split()
                except:
                    raise AFMError("Expecting name number, got '%s'" % args)
                no = _parseint(no)
            elif key == "PCC":
                try:
                    name1, x, y = args.split()
                except:
                    raise AFMError("Expecting name x y, got '%s'" % args)
                parts.append((name1, _parsefloat(x), _parsefloat(y)))
            else:
                raise AFMError("Unknown key '%s' in composite character data section" % key)
        if len(parts) != no:
            raise AFMError("Wrong number of composite characters")
        self.composites[i] = AFMcomposite(name, parts)
        return _READ_COMPOSITES, i+1

    def parse(self):
        f = open(self.filename, "r")
        try:
             # state of the reader, consisting of 
             #  - the main state, i.e. the type of the section
             #  - a parameter sstate
             state = _READ_START, None
             # Note that we do a line by line processing here, since one
             # of the states (_READ_DIRECTION) can be entered implicitly, i.e.
             # without a corresponding StartDirection section and we thus
             # may need to reprocess a line in the context of the new state
             for line in f:
                line = line[:-1]
                mstate, sstate = state
                if mstate == _READ_START:
                    state = self._processline_start(line)
                else: 
                    # except for the first line, any empty will be ignored
                    if not line.strip():
                       continue
                    if mstate == _READ_MAIN:
                        state = self._processline_main(line)
                    elif mstate == _READ_DIRECTION:
                        state = self._processline_direction(line, sstate)
                    elif mstate == _READ_CHARMETRICS:
                        state = self._processline_charmetrics(line, sstate)
                    elif mstate == _READ_KERNDATA:
                        state = self._processline_kerndata(line)
                    elif mstate == _READ_TRACKKERN:
                        state = self._processline_trackkern(line, sstate)
                    elif mstate == _READ_KERNPAIRS:
                        state = self._processline_kernpairs(line, sstate)
                    elif mstate == _READ_COMPOSITES:
                        state = self._processline_composites(line, sstate)
                    else:
                        raise RuntimeError("Undefined state in AFM reader")
        finally:
            f.close()

if __name__ == "__main__":
    a = AFMfile("/opt/local/share/texmf-dist/fonts/afm/yandy/lucida/lbc.afm")
    print a.charmetrics[0].name
    a = AFMfile("/usr/share/enscript/hv.afm")
    print a.charmetrics[32].name
