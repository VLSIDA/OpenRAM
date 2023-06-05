# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os


# Attempt to add the source code to the PYTHONPATH here before running globals.init_openram()
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


# Find the conda installer script
if os.path.exists(OPENRAM_HOME + "/install_conda.sh"):
    CONDA_INSTALLER = OPENRAM_HOME + "/install_conda.sh"
    CONDA_HOME = OPENRAM_HOME + "/miniconda"
elif os.path.exists(OPENRAM_HOME + "/../install_conda.sh"):
    CONDA_INSTALLER = OPENRAM_HOME + "/../install_conda.sh"
    CONDA_HOME = os.path.abspath(OPENRAM_HOME + "/../miniconda")
# Override CONDA_HOME if it's set as an environment variable
if "CONDA_HOME" in os.environ.keys():
    CONDA_HOME = os.environ["CONDA_HOME"]
# Add CONDA_HOME to environment variables just in case
try:
    os.environ["CONDA_HOME"] = CONDA_HOME
except:
    from openram import debug
    debug.warning("Couldn't find conda setup directory.")


# Import everything in globals.py
from .globals import *
# Import classes in the "openram" namespace
from .sram_config import *
from .sram import *
from .rom_config import *
from .rom import *


# Add a meta path finder for custom modules
from importlib.abc import MetaPathFinder
class custom_module_finder(MetaPathFinder):
    """
    This class is a 'hook' in Python's import system. If it encounters a module
    that can be customized, it checks if there is a custom module specified in
    the configuration file. If there is a custom module, it is imported instead
    of the default one.
    """
    def find_spec(self, fullname, path, target=None):
        # Get package and module names
        package_name = fullname.split(".")[0]
        module_name = fullname.split(".")[-1]
        # Skip if the package is not openram
        if package_name != "openram":
            return None
        # Search for the module name in customizable modules
        from openram import OPTS
        for k, v in OPTS.__dict__.items():
            if module_name == v:
                break
        else:
            return None
        # Search for the custom module
        import sys
        # Try to find the module in sys.path
        for path in sys.path:
            # Skip this path if not directory
            if not os.path.isdir(path):
                continue
            for file in os.listdir(path):
                # If there is a script matching the custom module name,
                # import it with the default module name
                if file == (module_name + ".py"):
                    from importlib.util import spec_from_file_location
                    return spec_from_file_location(module_name, "{0}/{1}.py".format(path, module_name))
        return None
# Python calls meta path finders and asks them to handle the module import if
# they can
sys.meta_path.insert(0, custom_module_finder())
