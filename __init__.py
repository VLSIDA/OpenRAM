# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os
import sys

# Attempt to add the source code to the PYTHONPATH here before running globals.init_openram().
try:
    OPENRAM_HOME = os.path.abspath(os.environ.get("OPENRAM_HOME"))
except:
    import openram
    OPENRAM_HOME = os.path.dirname(openram.__file__) + "/compiler"

if not os.path.isdir(OPENRAM_HOME):
    assert False

if OPENRAM_HOME not in sys.path:
    sys.path.insert(0, OPENRAM_HOME)