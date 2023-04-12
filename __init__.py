# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os

# Attempt to add the source code to the PYTHONPATH here before running globals.init_openram().
try:
    OPENRAM_HOME = os.path.abspath(os.environ.get("OPENRAM_HOME"))
except:
    OPENRAM_HOME = os.path.dirname(os.path.abspath(__file__)) + "/compiler"

if not os.path.isdir(OPENRAM_HOME):
    assert False

# Make sure that OPENRAM_HOME is an environment variable just in case
if "OPENRAM_HOME" not in os.environ.keys():
    os.environ["OPENRAM_HOME"] = OPENRAM_HOME

# Prepend $OPENRAM_HOME to __path__ so that openram will use those modules
__path__.insert(0, OPENRAM_HOME)


# Find the conda installation directory
if os.path.exists(OPENRAM_HOME + "/install_conda.sh"):
    CONDA_HOME = OPENRAM_HOME + "/miniconda"
elif os.path.exists(OPENRAM_HOME + "/../install_conda.sh"):
    CONDA_HOME = os.path.abspath(OPENRAM_HOME + "/../miniconda")

# Add CONDA_HOME to environment variables
try:
    os.environ["CONDA_HOME"] = CONDA_HOME
except:
    from openram import debug
    debug.warning("Couldn't find install_conda.sh")


# Import everything in globals.py
from .globals import *
# Import classes in the "openram" namespace
# sram_config should be imported before sram
from .sram_config import *
from .sram import *

from .rom_config import *
from .rom import *
