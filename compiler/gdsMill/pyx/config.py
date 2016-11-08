# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2003-2004 Jörg Lehmann <joergl@users.sourceforge.net>
# Copyright (C) 2003-2005 André Wobst <wobsta@users.sourceforge.net>
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

import ConfigParser, os.path
import siteconfig

cflist = [os.path.join(siteconfig.pyxrcdir, "pyxrc"),  os.path.expanduser("~/.pyxrc")]

config = ConfigParser.ConfigParser()
config.read(cflist)

def get(section, option, default):
    try:
        return config.get(section, option)
    except:
        return default

def getint(section, option, default):
    try:
        return config.getint(section, option)
    except:
        return default

def getfloat(section, option, default):
    try:
        return config.getfloat(section, option)
    except:
        return default

def getboolean(section, option, default):
    try:
        return config.getboolean(section, option)
    except:
        return default

