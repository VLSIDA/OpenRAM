# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram.base import design


class internal_base(design):

    def __init__(self, name, cell_name=None, prop=None):
        design.__init__(self, name, cell_name, prop)
