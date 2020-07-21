# See LICENSE for licensing information.
#
# Copyright (c) 2016-2020 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

class _pins:
    def __init__(self, pin_dict):
        # make the pins elements of the class to allow "." access.
        # For example: props.bitcell.cell_6t.pin.bl = "foobar"
        for k,v in pin_dict.items():
            self.__dict__[k] = v

class _cell:
    def __init__(self, pin_dict):
        pin_dict.update(self._default_power_pins())
        self._pins = _pins(pin_dict)

    @property
    def pin(self):
        return self._pins

    def _default_power_pins(self):
        return { 'vdd' : 'vdd', 'gnd' : 'gnd' }

class _mirror_axis:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class _bitcell:
    def __init__(self, mirror, split_wl, cell_6t, cell_1rw1r, cell_1w1r):
        self.mirror = mirror
        self.split_wl = split_wl
        self._6t = cell_6t
        self._1rw1r = cell_1rw1r
        self._1w1r = cell_1w1r

    def _default():
        axis = _mirror_axis(True, False)
        cell_6t = _cell({'bl' : 'bl',
                         'br' : 'br',
                         'wl' : 'wl'})

        cell_1rw1r = _cell({'bl0' : 'bl0',
                       'br0' : 'br0',
                       'bl1' : 'bl1',
                       'br1' : 'br1',
                       'wl0' : 'wl0',
                       'wl1' : 'wl1'})
        cell_1w1r =  _cell({'bl0' : 'bl0',
                       'br0' : 'br0',
                       'bl1' : 'bl1',
                       'br1' : 'br1',
                       'wl0' : 'wl0',
                       'wl1' : 'wl1'})
        return _bitcell(cell_6t=cell_6t,
                        cell_1rw1r=cell_1rw1r,
                        cell_1w1r=cell_1w1r,
                        split_wl = False,
                        mirror=axis)

    @property
    def cell_6t(self):
        return self._6t

    @property
    def cell_1rw1r(self):
        return self._1rw1r

    @property
    def cell_1w1r(self):
        return self._1w1r


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
    This contains meta information about the custom designed cells. For
    instance, pin names, or the axis on which they need to be mirrored. These
    can be overriden in the tech.py file.
    """
    def __init__(self):
        self.names = {}

        self._bitcell = _bitcell._default()
                                 
        self._dff = _dff(use_custom_ports = False,
                         custom_port_list = ["D", "Q", "clk", "vdd", "gnd"],
                         custom_type_list = ["INPUT", "OUTPUT", "INPUT", "POWER", "GROUND"],
                         clk_pin= "clk")
        
        self._dff_buff = _dff_buff(use_custom_ports = False,
                                   custom_buff_ports = ["D", "qint", "clk", "vdd", "gnd"],
                                   add_body_contacts = False)

        self._dff_buff_array = _dff_buff_array(use_custom_ports = False,
                                               add_body_contacts = False)

        self._write_driver = _cell({'din': 'din',
                                    'bl' : 'bl',
                                    'br' : 'br',
                                    'en' : 'en'})
        self._sense_amp = _cell({'bl'   : 'bl',
                                 'br'   : 'br',
                                 'dout' : 'dout',
                                 'en'   : 'en'})

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

    @property
    def write_driver(self):
        return self._write_driver

    @property
    def sense_amp(self):
        return self._sense_amp
