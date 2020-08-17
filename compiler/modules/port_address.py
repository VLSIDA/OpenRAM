# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California
# All rights reserved.
#
from math import log, ceil
import debug
import design
from sram_factory import factory
from vector import vector
from tech import layer
from globals import OPTS


class port_address(design.design):
    """
    Create the address port (row decoder and wordline driver)..
    """

    def __init__(self, cols, rows, name=""):
        
        self.num_cols = cols
        self.num_rows = rows
        self.addr_size = ceil(log(self.num_rows, 2))
        
        if name == "":
            name = "port_address_{0}_{1}".format(cols, rows)
        super().__init__(name)
        debug.info(2, "create data port of cols {0} rows {1}".format(cols, rows))

        self.create_netlist()
        if not OPTS.netlist_only:
            debug.check(len(self.all_ports) <= 2, "Bank layout cannot handle more than two ports.")
            self.create_layout()
            self.add_boundary()

    def create_netlist(self):
        self.add_pins()
        self.add_modules()
        self.create_row_decoder()
        self.create_wordline_driver()
        
    def create_layout(self):
        if "li" in layer:
            self.route_layer = "li"
        else:
            self.route_layer = "m1"
        self.place_instances()
        self.route_layout()
        self.DRC_LVS()

    def add_pins(self):
        """ Adding pins for port address module"""

        for bit in range(self.addr_size):
            self.add_pin("addr_{0}".format(bit), "INPUT")
        
        self.add_pin("wl_en", "INPUT")

        for bit in range(self.num_rows):
            self.add_pin("wl_{0}".format(bit), "OUTPUT")
        
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")
        
    def route_layout(self):
        """ Create routing amoung the modules """
        self.route_pins()
        self.route_internal()
        self.route_supplies()
        
    def route_supplies(self):
        """ Propagate all vdd/gnd pins up to this level for all modules """
        for inst in self.insts:
            self.copy_power_pins(inst, "vdd")
            self.copy_power_pins(inst, "gnd")

    def route_pins(self):
        for row in range(self.addr_size):
            decoder_name = "addr_{}".format(row)
            self.copy_layout_pin(self.row_decoder_inst, decoder_name)

        for row in range(self.num_rows):
            driver_name = "wl_{}".format(row)
            self.copy_layout_pin(self.wordline_driver_inst, driver_name)

        self.copy_layout_pin(self.wordline_driver_inst, "en", "wl_en")
            
    def route_internal(self):
        for row in range(self.num_rows):
            # The pre/post is to access the pin from "outside" the cell to avoid DRCs
            decoder_out_pin = self.row_decoder_inst.get_pin("decode_{}".format(row))
            decoder_out_pos = decoder_out_pin.rc()
            driver_in_pin = self.wordline_driver_inst.get_pin("in_{}".format(row))
            driver_in_pos = driver_in_pin.lc()
            self.add_zjog(self.route_layer, decoder_out_pos, driver_in_pos, var_offset=0.3)

            self.add_via_stack_center(from_layer=decoder_out_pin.layer,
                                      to_layer=self.route_layer,
                                      offset=decoder_out_pos)

            self.add_via_stack_center(from_layer=driver_in_pin.layer,
                                      to_layer=self.route_layer,
                                      offset=driver_in_pos)
        
    def add_modules(self):

        self.row_decoder = factory.create(module_type="decoder",
                                          num_outputs=self.num_rows)
        self.add_mod(self.row_decoder)
        
        self.wordline_driver = factory.create(module_type="wordline_driver_array",
                                              rows=self.num_rows,
                                              cols=self.num_cols)
        self.add_mod(self.wordline_driver)
        
    def create_row_decoder(self):
        """  Create the hierarchical row decoder  """
        
        self.row_decoder_inst = self.add_inst(name="row_decoder",
                                              mod=self.row_decoder)

        temp = []
        for bit in range(self.addr_size):
            temp.append("addr_{0}".format(bit))
        for row in range(self.num_rows):
            temp.append("dec_out_{0}".format(row))
        temp.extend(["vdd", "gnd"])
        self.connect_inst(temp)

    def create_wordline_driver(self):
        """ Create the Wordline Driver """

        self.wordline_driver_inst = self.add_inst(name="wordline_driver",
                                                  mod=self.wordline_driver)

        temp = []
        for row in range(self.num_rows):
            temp.append("dec_out_{0}".format(row))
        for row in range(self.num_rows):
            temp.append("wl_{0}".format(row))
        temp.append("wl_en")
        temp.append("vdd")
        temp.append("gnd")
        self.connect_inst(temp)

    def place_instances(self):
        """
        Compute the offsets and place the instances.
        """

        row_decoder_offset = vector(0, 0)
        wordline_driver_offset = vector(self.row_decoder.width, 0)
        self.wordline_driver_inst.place(wordline_driver_offset)
        self.row_decoder_inst.place(row_decoder_offset)
        # Pass this up
        self.predecoder_height = self.row_decoder.predecoder_height

        self.height = self.row_decoder.height
        self.width = self.wordline_driver_inst.rx()
