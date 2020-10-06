# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California 
# All rights reserved.
#
from bitcell_base_array import bitcell_base_array
from sram_factory import factory
from tech import GDS,layer,drc,parameter,cell_properties
from tech import cell_properties as props
from globals import OPTS


class dummy_array(bitcell_base_array):
    """
    Generate a dummy row/column for the replica array.
    """
    def __init__(self, rows, cols, column_offset=0, mirror=0, name=""):
        super().__init__(rows=rows, cols=cols, column_offset=column_offset, name=name)
        self.mirror = mirror

        # This will create a default set of bitline/wordline names
        self.create_all_bitline_names()
        self.create_all_wordline_names()

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()
        
    def create_netlist(self):
        """ Create and connect the netlist """
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):

        self.place_array("dummy_r{0}_c{1}", self.mirror)

        self.add_layout_pins()

        self.add_boundary()
        
        self.DRC_LVS()

    def add_modules(self):
        """ Add the modules used in this design """
        
        if not props.compare_ports(props.bitcell_array.use_custom_cell_arrangement):
            self.dummy_cell = factory.create(module_type="dummy_{}".format(OPTS.bitcell))
            self.cell = factory.create(module_type="bitcell")
        else:
            self.dummy_cell = factory.create(module_type="s8_bitcell", version = "opt1")
            self.dummy_cell2 = factory.create(module_type="s8_bitcell", version = "opt1a")
            self.add_mod(factory.create(module_type="s8_internal", version = "wlstrap"))
            self.add_mod(factory.create(module_type="s8_internal", version = "wlstrap_p"))
            self.cell = factory.create(module_type="s8_bitcell", version = "opt1")
            self.add_mod(self.dummy_cell2)
        self.add_mod(self.dummy_cell)
        
    def create_instances(self):
        """ Create the module instances used in this design """
        self.cell_inst = {}
        if not props.compare_ports(props.bitcell_array.use_custom_cell_arrangement):
            for col in range(self.column_size):
                for row in range(self.row_size):
                    name = "bit_r{0}_c{1}".format(row, col)
                    self.cell_inst[row, col]=self.add_inst(name=name,
                                                        mod=self.dummy_cell)
                    self.connect_inst(self.get_bitcell_pins(row, col))
        else:
            from tech import custom_cell_arrangement
            custom_cell_arrangement(self) 

    def add_pins(self):
        # bitline pins are not added because they are floating
        for wl_name in self.get_wordline_names():
            self.add_pin(wl_name, "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")
                
    def add_layout_pins(self):
        """ Add the layout pins """

        # Add the bitline metal, but not as pins since they are going to just be floating
        # For some reason, LVS has an issue if we don't add this metal
        bitline_names = self.cell.get_all_bitline_names()
        for col in range(self.column_size):
            for port in self.all_ports:
                bl_pin = self.cell_inst[0, col].get_pin(bitline_names[2 * port])
                self.add_rect(layer=bl_pin.layer,
                              offset=bl_pin.ll().scale(1, 0),
                              width=bl_pin.width(),
                              height=self.height)
                br_pin = self.cell_inst[0, col].get_pin(bitline_names[2 * port + 1])
                self.add_rect(layer=br_pin.layer,
                              offset=br_pin.ll().scale(1, 0),
                              width=br_pin.width(),
                              height=self.height)
        
        wl_names = self.cell.get_all_wl_names()
        if not props.compare_ports(props.bitcell_array.use_custom_cell_arrangement):
            for row in range(self.row_size):
                for port in self.all_ports:
                    wl_pin = self.cell_inst[row, 0].get_pin(wl_names[port])
                    self.add_layout_pin(text="wl_{0}_{1}".format(port, row),
                                        layer=wl_pin.layer,
                                        offset=wl_pin.ll().scale(0, 1),
                                        width=self.width,
                                        height=wl_pin.height())
        else:
            for row in range(self.row_size):
                for port in self.all_ports:
                    for wl in range(len(wl_names)):
                        wl_pin = self.cell_inst[row, 0].get_pin("wl{}".format(wl))
                        self.add_layout_pin(text="wl{0}_{1}_{2}".format(wl, port, row),
                                            layer=wl_pin.layer,
                                            offset=wl_pin.ll().scale(0, 1),
                                            width=self.width,
                                            height=wl_pin.height())

        # Copy a vdd/gnd layout pin from every cell
        if not props.compare_ports(props.bitcell_array.use_custom_cell_arrangement):
            for row in range(self.row_size):
                for col in range(self.column_size):
                    inst = self.cell_inst[row, col]
                    for pin_name in ["vdd", "gnd"]:
                        self.copy_layout_pin(inst, pin_name)
        else:
            for row in range(self.row_size):
                for col in range(self.column_size):
                    inst = self.cell_inst[row, col]
                    for pin_name in ["vpwr", "vgnd"]:
                        self.copy_layout_pin(inst, pin_name)
        

    def input_load(self):
        # FIXME: This appears to be old code from previous characterization. Needs to be updated.
        wl_wire = self.gen_wl_wire()
        return wl_wire.return_input_cap()
