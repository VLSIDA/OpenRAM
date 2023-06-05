# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

class _bank:
    def __init__(self, stack, pitch):
        # bank
        # column address route: stack, pitch
        # m1_stack, m2_pitch (default)
        # m2_stack, m3_pitch (sky130)
        self.stack = stack
        self.pitch = pitch


class _hierarchical_decoder:
    def __init__(self,
                 bus_layer,
                 bus_directions,
                 input_layer,
                 output_layer,
                 vertical_supply):
        # hierarchical_decoder
        # bus_layer, bus_directions, bus_pitch, bus_space, input_layer, output_layer, output_layer_pitch
        # m2, pref, m2_pitch, m2_space, m1, m3, m3_pitch
        # m1, nonpref, m1_pitch, m2_space, m2, li, li_pitch (sky130)
        #
        # vertical vdd/gnd
        # special jogging
        self.bus_layer = bus_layer
        self.bus_directions = bus_directions
        self.input_layer = input_layer
        self.output_layer = output_layer
        self.vertical_supply = vertical_supply


class _hierarchical_predecode:
    def __init__(self,
                 bus_layer,
                 bus_directions,
                 bus_space_factor,
                 input_layer,
                 output_layer,
                 vertical_supply,
                 force_horizontal_input_contact):
        # hierarchical_predecode
        # bus_layer, bus_directions, bus_pitch, bus_space, input_layer, output_layer, output_layer_pitch
        # m2, pref, m2_pitch, m2_space, m1, m1, m1_pitch
        # m1, nonpref, m1_pitch, 1`.5*m1_space, m2, li, li_pitch (sky130)
        #
        # vertical vdd/gnd
        # special jogging
        self.bus_layer = bus_layer
        self.bus_directions = bus_directions
        self.bus_space_factor = bus_space_factor
        self.input_layer = input_layer
        self.output_layer = output_layer
        self.vertical_supply = vertical_supply
        self.force_horizontal_input_contact = force_horizontal_input_contact


class _column_mux_array:
    def __init__(self,
                 select_layer,
                 select_pitch,
                 bitline_layer):
        # column_mux_array
        # sel_layer, sel_pitch, bitline_layer
        # m1, m2_pitch, m2
        # m3, m3_pitch, m1 (sky130)
        self.select_layer = select_layer
        self.select_pitch= select_pitch
        self.bitline_layer = bitline_layer


class _port_address:
    def __init__(self,
                 supply_offset):
        # port_adress
        # special supply offset
        self.supply_offset = supply_offset


class _port_data:
    def __init__(self,
                 channel_route_bitlines,
                 enable_layer):
        # port_data
        # connect bitlines instead of chanel route

        # sense_amp_array
        # en_layer
        # m1
        # m3 (sky130)

        # precharge_array
        # en_bar_layer
        # m1
        # m3 (sky130)
        self.channel_route_bitlines = channel_route_bitlines
        self.enable_layer = enable_layer


class _replica_column:
    def __init__(self,
                 even_rows):
        # replica_column
        # even row check (sky130)
        self.even_rows = even_rows


class _wordline_driver:
    def __init__(self,
                 vertical_supply):
        # wordline_buffer_array
        # vertical vdd/gnd (sky130)
        # wordline_driver_array
        # vertical vdd/gnd (sky130)
        # wordline_driver
        # vertical vdd/gnd (sky130)
        self.vertical_supply = vertical_supply


class _bitcell_array:
    def __init__(self,
                 wordline_layer,
                 wordline_pitch_factor=2):
        self.wordline_layer = wordline_layer
        self.wordline_pitch_factor = wordline_pitch_factor


class layer_properties():
    """
    This contains meta information about the module routing layers. These
    can be overriden in the tech.py file.
    """
    def __init__(self):

        self._bank = _bank(stack="m1_stack",
                           pitch="m2_pitch")

        self._hierarchical_decoder = _hierarchical_decoder(bus_layer="m2",
                                                           bus_directions="pref",
                                                           input_layer="m1",
                                                           output_layer="m3",
                                                           vertical_supply=False)

        self._hierarchical_predecode = _hierarchical_predecode(bus_layer="m2",
                                                               bus_directions="pref",
                                                               bus_space_factor=1,
                                                               input_layer="m1",
                                                               output_layer="m1",
                                                               vertical_supply=False,
                                                               force_horizontal_input_contact=False)

        self._column_mux_array = _column_mux_array(select_layer="m1",
                                                   select_pitch="m2_pitch",
                                                   bitline_layer="m2")

        self._port_address = _port_address(supply_offset=False)

        self._port_data = _port_data(channel_route_bitlines=True,
                                     enable_layer="m1")

        self._replica_column = _replica_column(even_rows=False)

        self._wordline_driver = _wordline_driver(vertical_supply=False)

        self._local_bitcell_array = _bitcell_array(wordline_layer="m2")

        self._global_bitcell_array = _bitcell_array(wordline_layer="m3")

    @property
    def bank(self):
        return self._bank

    @property
    def column_mux_array(self):
        return self._column_mux_array

    @property
    def hierarchical_decoder(self):
        return self._hierarchical_decoder

    @property
    def hierarchical_predecode(self):
        return self._hierarchical_predecode

    @property
    def port_address(self):
        return self._port_address

    @property
    def port_data(self):
        return self._port_data

    @property
    def replica_column(self):
        return self._replica_column

    @property
    def wordline_driver(self):
        return self._wordline_driver

    @property
    def global_bitcell_array(self):
        return self._global_bitcell_array

    @property
    def local_bitcell_array(self):
        return self._local_bitcell_array

