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
        # For example: props.bitcell.cell_6t.pin.bl = "foobar"
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
    def __init__(self, mirror, cell_s8_6t, cell_6t, cell_1rw1r, cell_1w1r):
        self.mirror = mirror
        self._s8_6t = cell_s8_6t
        self._6t = cell_6t
        self._1rw1r = cell_1rw1r
        self._1w1r = cell_1w1r

    def _default():
        axis = _mirror_axis(True, False)

        cell_s8_6t = _cell({'bl': 'bl',
                            'br': 'br',
                            'wl': 'wl'})

        cell_6t = _cell({'bl': 'bl',
                         'br': 'br',
                         'wl': 'wl'})

        cell_1rw1r = _cell({'bl0': 'bl0',
                            'br0': 'br0',
                            'bl1': 'bl1',
                            'br1': 'br1',
                            'wl0': 'wl0',
                            'wl1': 'wl1'})

        cell_1w1r = _cell({'bl0': 'bl0',
                           'br0': 'br0',
                           'bl1': 'bl1',
                           'br1': 'br1',
                           'wl0': 'wl0',
                           'wl1': 'wl1'})

        return _bitcell(cell_s8_6t=cell_s8_6t,
                        cell_6t=cell_6t,
                        cell_1rw1r=cell_1rw1r,
                        cell_1w1r=cell_1w1r,
                        mirror=axis)

    @property
    def cell_s8_6t(self):
        return self._s8_6t

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
        self.names["bitcell"] = "cell_6t"
        self.names["bitcell_1rw_1r"] = "cell_1rw_1r"
        self.names["bitcell_1r_1w"] = "cell_1r_1w"
        self.names["dummy_bitcell"] = "dummy_cell_6t"
        self.names["dummy_bitcell_1rw_1r"] = "dummy_cell_1rw_1r"
        self.names["dummy_bitcell_1r_1w"] = "dummy_cell_1r_1w"
        self.names["replica_bitcell"] = "replica_cell_6t"
        self.names["replica_bitcell_1rw_1r"] = "replica_cell_1rw_1r"
        self.names["replica_bitcell_1r_1w"] = "replica_cell_1r_1w"
        self.names["col_cap_bitcell_6t"] = "col_cap_cell_6t"
        self.names["col_cap_bitcell_1rw_1r"] = "col_cap_cell_1rw_1r"
        self.names["col_cap_bitcell_1r_1w"] = "col_cap_cell_1r_1w"
        self.names["row_cap_bitcell_6t"] = "row_cap_cell_6t"
        self.names["row_cap_bitcell_1rw_1r"] = "row_cap_cell_1rw_1r"
        self.names["row_cap_bitcell_1r_1w"] = "row_cap_cell_1r_1w"

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
