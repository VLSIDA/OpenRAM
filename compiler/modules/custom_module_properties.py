# See LICENSE for licensing information.
#
# Copyright (c) 2016-2020 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

class _dff:
    def __init__(self, use_custom_ports, custom_port_list, custom_type_list):
        self.use_custom_ports = use_custom_ports
        self.custom_port_list = custom_port_list
        self.custom_type_list = custom_type_list

class module_properties():
    """
    TODO
    """
    def __init__(self):
        self.names = {}
        self._dff = _dff(use_custom_ports = False,
                         custom_port_list = [],
                         custom_type_list = [])

    @property
    def dff(self):
        return self._dff
