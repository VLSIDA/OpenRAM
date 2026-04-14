#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

import sys
from openram import OPTS

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

sys.path.append("{}/{}".format(dir_path,'tech_configs'))

if not hasattr(OPTS, 'tech_file'):
    OPTS.tech_file = 'tech_cypress_cell'
#TODO: FIX THIS TERRIBLE HACK JUST FOR TESTING EXECUTING 
exec('from {} import *'.format(OPTS.tech_file))
