# See LICENSE for licensing information.
#
# Copyright (c) 2016-2020 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

class _cell:
    def __init__(self, port_order, port_types, port_map=None, hard_cell=True, boundary_layer="boundary"):
        
        # Specifies if this is a hard (i.e. GDS) cell
        self._hard_cell = hard_cell
        self._boundary_layer = boundary_layer
        
        # Specifies the port directions
        self._port_types_map = {x: y for (x, y) in zip(port_order, port_types)}
        
        # Specifies a map from OpenRAM names to cell names
        # by default it is 1:1
        if not port_map:
            self._port_map = {x: x for x in port_order}

        # Update mapping of names
        self._original_port_order = port_order
        self._port_order = port_order

        # Create an index array
        self._port_indices = [self._port_order.index(x) for x in self._original_port_order]
        
        # Update ordered name list
        self._port_names = [self._port_map[x] for x in self._port_order]
        
        # Update ordered type list
        self._port_types = [self._port_types_map[x] for x in self._port_order]
        
    @property
    def hard_cell(self):
        return self._hard_cell

    @property
    def port_names(self):
        return self._port_names

    @property
    def port_order(self):
        return self._port_order

    @port_order.setter
    def port_order(self, x):
        self._port_order = x
        # Update ordered name list in the new order
        self._port_names = [self._port_map[x] for x in self._port_order]
        # Update ordered type list in the new order
        self._port_types = [self._port_types_map[x] for x in self._port_order]
        # Update the index array
        self._port_indices = [self._port_order.index(x) for x in self._original_port_order]

    @property
    def port_indices(self):
        return self._port_indices
        
    @property
    def port_map(self):
        return self._port_map
    
    @port_map.setter
    def port_map(self, x):
        self._port_map = x
        # Update ordered name list to use the new names
        self._port_names = [self.port_map[x] for x in self._port_order]
    
    @property
    def port_types(self):
        return self._port_types

    @property
    def boundary_layer(self):
        return self._boundary_layer

    @boundary_layer.setter
    def boundary_layer(self, x):
        self._boundary_layer = x
        
    
class _pins:
    def __init__(self, pin_dict):
        # make the pins elements of the class to allow "." access.
        # For example: props.bitcell.cell_1port.pin.bl = "foobar"
        for k, v in pin_dict.items():
            self.__dict__[k] = v


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


class _bitcell(_cell):
    def __init__(self, port_order, port_types, port_map=None, storage_nets=["Q", "Q_bar"], mirror=None, end_caps=False):
        super().__init__(port_order, port_types, port_map)

        self.end_caps = end_caps
        
        if not mirror:
            self.mirror = _mirror_axis(True, False)
        else:
            self.mirror = mirror

        self.storage_nets = storage_nets

    
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

        self._ptx = _ptx(model_is_subckt=False,
                         bin_spice_models=False)

        self._pgate = _pgate(add_implants=False)

        self._inv_dec = _cell(["A", "Z", "vdd", "gnd"],
                              ["INPUT", "OUTPUT", "POWER", "GROUND"])
        
        self._nand2_dec = _cell(["A", "B", "Z", "vdd", "gnd"],
                                ["INPUT", "INPUT", "OUTPUT", "POWER", "GROUND"])
        
        self._nand3_dec = _cell(["A", "B", "C", "Z", "vdd", "gnd"],
                                ["INPUT", "INPUT", "INPUT", "OUTPUT", "POWER", "GROUND"])
        
        self._nand4_dec = _cell(["A", "B", "C", "D", "Z", "vdd", "gnd"],
                                ["INPUT", "INPUT", "INPUT", "INPUT", "OUTPUT", "POWER", "GROUND"])
        
        self._dff = _cell(["D", "Q", "clk", "vdd", "gnd"],
                          ["INPUT", "OUTPUT", "INPUT", "POWER", "GROUND"])

        self._write_driver = _cell(['din', 'bl', 'br', 'en', 'vdd', 'gnd'],
                                   ["INPUT", "OUTPUT", "OUTPUT", "INPUT", "POWER", "GROUND"])

        self._sense_amp = _cell(['bl', 'br', 'dout', 'en', 'vdd', 'gnd'],
                                ["INPUT", "INPUT", "OUTPUT", "INPUT", "POWER", "GROUND"])

        self._bitcell_1port = _bitcell(["bl", "br", "wl", "vdd", "gnd"],
                                       ["OUTPUT", "OUTPUT", "INPUT", "POWER", "GROUND"])

        self._bitcell_2port = _bitcell(["bl0", "br0", "bl1", "br1", "wl0", "wl1", "vdd", "gnd"],
                                       ["OUTPUT", "OUTPUT", "OUTPUT", "OUTPUT", "INPUT", "INPUT", "POWER", "GROUND"])

        self._col_cap_2port = _bitcell(["bl0", "br0", "bl1", "br1", "vdd"],
                                       ["OUTPUT", "OUTPUT", "OUTPUT", "OUTPUT", "POWER"])

        self._row_cap_2port = _bitcell(["wl0", "wl1", "gnd"],
                                       ["INPUT", "INPUT", "POWER", "GROUND"])

    @property
    def ptx(self):
        return self._ptx

    @property
    def pgate(self):
        return self._pgate

    @property
    def inv_dec(self):
        return self._inv_dec

    @property
    def nand2_dec(self):
        return self._nand2_dec
    
    @property
    def nand3_dec(self):
        return self._nand3_dec
    
    @property
    def nand4_dec(self):
        return self._nand4_dec
    
    @property
    def dff(self):
        return self._dff

    @property
    def write_driver(self):
        return self._write_driver

    @property
    def sense_amp(self):
        return self._sense_amp

    @property
    def bitcell_1port(self):
        return self._bitcell_1port
    
    @property
    def bitcell_2port(self):
        return self._bitcell_2port

    @property
    def col_cap_2port(self):
        return self._col_cap_2port

    @property
    def row_cap_2port(self):
        return self._row_cap_2port
    
