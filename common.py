# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
"""
Common functions for top-level scripts
"""

import sys
import os


def make_openram_package():
    """ Make sure that OpenRAM can be used as a Python package. """

    import importlib.util

    # Find the package loader from python/site-packages
    openram_loader = importlib.util.find_spec("openram")

    # If openram library isn't found as a python package, import it from
    # the $OPENRAM_HOME path.
    if openram_loader is None:
        OPENRAM_HOME = os.getenv("OPENRAM_HOME")
        # Import using spec since the directory can be named something other
        # than "openram".
        spec = importlib.util.spec_from_file_location("openram", "{}/../__init__.py".format(OPENRAM_HOME))
        module = importlib.util.module_from_spec(spec)
        sys.modules["openram"] = module
        spec.loader.exec_module(module)
