# See LICENSE for licensing information.
#
# Copyright (c) 2016-2020 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
class _mirror_axis:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class _bitcell:
    def __init__(self, mirror, split_wl):
        self.mirror = mirror
        self.split_wl = split_wl

class _dff:
    def __init__(self, use_custom_ports, custom_port_list, custom_type_list, clk_pin):
        self.use_custom_ports = use_custom_ports
        self.custom_port_list = custom_port_list
        self.custom_type_list = custom_type_list
        self.clk_pin = clk_pin

class _dff_buff:
    def __init__(self, use_custom_ports, custom_buff_ports, add_body_contacts):
        self.use_custom_ports = use_custom_ports
        self.buf_ports = custom_buff_ports
        self.add_body_contacts = add_body_contacts

class _dff_buff_array:
    def __init__(self, use_custom_ports, add_body_contacts):
        self.use_custom_ports = use_custom_ports
        self.add_body_contacts = add_body_contacts

class cell_properties():
    """
    TODO
    """
    def __init__(self):
        self.names = {}

        self._bitcell = _bitcell(mirror = _mirror_axis(True, False),
                                 split_wl = False)
                                 
        self._dff = _dff(use_custom_ports = False,
                         custom_port_list = ["D", "Q", "clk", "vdd", "gnd"],
                         custom_type_list = ["INPUT", "OUTPUT", "INPUT", "POWER", "GROUND"],
                         clk_pin= "clk")
        
        self._dff_buff = _dff_buff(use_custom_ports = False,
                                   custom_buff_ports = ["D", "qint", "clk", "vdd", "gnd"],
                                   add_body_contacts = False)

        self._dff_buff_array = _dff_buff_array(use_custom_ports = False,
                                               add_body_contacts = False)

    @property
    def bitcell(self):
        return self._bitcell

    @property
    def dff(self):
        return self._dff
    
    @property
    def dff_buff(self):
        return self._dff_buff

    @property
    def dff_buff_array(self):
        return self._dff_buff_array

