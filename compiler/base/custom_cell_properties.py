# See LICENSE for licensing information.
#
# Copyright (c) 2016-2020 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from globals import OPTS


class _pins:
    def __init__(self, pin_dict):
        # make the pins elements of the class to allow "." access.
        # For example: props.bitcell.cell_1port.pin.bl = "foobar"
        for k, v in pin_dict.items():
            self.__dict__[k] = v


class _cell:
    def __init__(self, pin_dict):
        pin_dict.update(self._default_power_pins())
        self._pins = _pins(pin_dict)

    @property
    def pin(self):
        return self._pins

    def _default_power_pins(self):
        return {'vdd': 'vdd',
                'gnd': 'gnd'}


class _mirror_axis:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class _ptx:
    def __init__(self, model_is_subckt, bin_spice_models):
        self.model_is_subckt = model_is_subckt
        self.bin_spice_models = bin_spice_models


class _pgate:
    def __init__(self, add_implants):
        self.add_implants = add_implants


class _bitcell:
    def __init__(self, mirror, cell_1port, cell_2port):
        self.mirror = mirror
        self._1rw = cell_1port
        self._2rw = cell_2port

    def _default():
        axis = _mirror_axis(True, False)

        cell_1port = _cell({'bl': 'bl',
                            'br': 'br',
                            'wl': 'wl'})

        cell_2port = _cell({'bl0': 'bl0',
                            'br0': 'br0',
                            'bl1': 'bl1',
                            'br1': 'br1',
                            'wl0': 'wl0',
                            'wl1': 'wl1'})

        return _bitcell(cell_1port=cell_1port,
                        cell_2port=cell_2port,
                        mirror=axis)

    @property
    def cell_1port(self):
        return self._1rw

    @property
    def cell_2port(self):
        return self._2rw


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


class _bitcell_array:
    def __init__(self, use_custom_cell_arrangement):
        self.use_custom_cell_arrangement = use_custom_cell_arrangement


class cell_properties():
    """
    This contains meta information about the custom designed cells. For
    instance, pin names, or the axis on which they need to be mirrored. These
    can be overriden in the tech.py file.
    """
    def __init__(self):
        self.names = {}

        self.names["bitcell_1port"] = "cell_1rw"
        self.names["bitcell_2port"] = "cell_2rw"
        self.names["dummy_bitcell_1port"] = "dummy_cell_1rw"
        self.names["dummy_bitcell_2port"] = "dummy_cell_2rw"
        self.names["replica_bitcell_1port"] = "replica_cell_1rw"
        self.names["replica_bitcell_2port"] = "replica_cell_2rw"
        self.names["col_cap_bitcell_1port"] = "col_cap_cell_1rw"
        self.names["col_cap_bitcell_2port"] = "col_cap_cell_2rw"
        self.names["row_cap_bitcell_1port"] = "row_cap_cell_1rw"
        self.names["row_cap_bitcell_2port"] = "row_cap_cell_2rw"
        
        self._bitcell = _bitcell._default()

        self._ptx = _ptx(model_is_subckt=False,
                         bin_spice_models=False)

        self._pgate = _pgate(add_implants=False)

        self._dff = _dff(use_custom_ports=False,
                         custom_port_list=["D", "Q", "clk", "vdd", "gnd"],
                         custom_type_list=["INPUT", "OUTPUT", "INPUT", "POWER", "GROUND"],
                         clk_pin="clk")

        self._dff_buff = _dff_buff(use_custom_ports=False,
                                   custom_buff_ports=["D", "qint", "clk", "vdd", "gnd"],
                                   add_body_contacts=False)

        self._dff_buff_array = _dff_buff_array(use_custom_ports=False,
                                               add_body_contacts=False)

        self._write_driver = _cell({'din': 'din',
                                    'bl': 'bl',
                                    'br': 'br',
                                    'en': 'en'})

        self._sense_amp = _cell({'bl': 'bl',
                                 'br': 'br',
                                 'dout': 'dout',
                                 'en': 'en'})

        self._bitcell_array = _bitcell_array(use_custom_cell_arrangement=[])

    @property
    def bitcell(self):
        return self._bitcell

    @property
    def ptx(self):
        return self._ptx

    @property
    def pgate(self):
        return self._pgate

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

    @property
    def bitcell_array(self):
        return self._bitcell_array

    def compare_ports(self, port_list):
        use_custom_arrangement = False
        for ports in port_list:
            if ports == "{}R_{}W_{}RW".format(OPTS.num_r_ports, OPTS.num_w_ports, OPTS.num_rw_ports):
                use_custom_arrangement = True
                break
        return use_custom_arrangement
