# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California
# All rights reserved.
#
import sys
from tech import drc, parameter
from math import log
import debug
import design
from sram_factory import factory
from vector import vector

from globals import OPTS

class port_address(design.design):
    """
    Create the address port (row decoder and wordline driver)..
    """

    def __init__(self, cols, rows, name=""):
        
        self.num_cols = cols
        self.num_rows = rows
        self.addr_size = int(log(self.num_rows, 2))
        
        if name == "":
            name = "port_address_{0}_{1}".format(cols,rows)
        design.design.__init__(self, name)
        debug.info(2, "create data port of cols {0} rows {1}".format(cols,rows))

        self.create_netlist()
        if not OPTS.netlist_only:
            debug.check(len(self.all_ports)<=2,"Bank layout cannot handle more than two ports.")
            self.create_layout()
            self.add_boundary()


    def create_netlist(self):
        self.add_pins()
        self.add_modules()
        self.create_row_decoder()
        self.create_wordline_driver()
        
    def create_layout(self):
        self.place_instances()
        self.route_layout()
        self.DRC_LVS()

    def add_pins(self):
        """ Adding pins for port address module"""

        for bit in range(self.addr_size):
            self.add_pin("addr_{0}".format(bit),"INPUT")
        
        self.add_pin("wl_en", "INPUT")

        for bit in range(self.num_rows):
            self.add_pin("wl_{0}".format(bit),"OUTPUT")
        
        self.add_pin("vdd","POWER")
        self.add_pin("gnd","GROUND")

        
    def route_layout(self):
        """ Create routing amoung the modules """
        self.route_pins()
        self.route_internal()
        self.route_supplies()
        
    def route_supplies(self):
        """ Propagate all vdd/gnd pins up to this level for all modules """
        for inst in self.insts:
            self.copy_power_pins(inst,"vdd")
            self.copy_power_pins(inst,"gnd")

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
            decoder_out_pos = self.row_decoder_inst.get_pin("decode_{}".format(row)).rc()
            driver_in_pos = self.wordline_driver_inst.get_pin("in_{}".format(row)).lc()
            mid1 = decoder_out_pos.scale(0.5,1)+driver_in_pos.scale(0.5,0)
            mid2 = decoder_out_pos.scale(0.5,0)+driver_in_pos.scale(0.5,1)
            self.add_path("metal1", [decoder_out_pos, mid1, mid2, driver_in_pos])


            
        
    def add_modules(self):

        self.row_decoder = factory.create(module_type="decoder",
                                          rows=self.num_rows)
        self.add_mod(self.row_decoder)
        
        self.wordline_driver = factory.create(module_type="wordline_driver",
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

        # A space for wells or jogging m2
        self.m2_gap = max(2*drc("pwell_to_nwell") + drc("well_enclosure_active"),
                          3*self.m2_pitch)
        
        row_decoder_offset = vector(0,0)
        wordline_driver_offset = vector(self.row_decoder.width + self.m2_gap,0)
        
        self.wordline_driver_inst.place(wordline_driver_offset)
        self.row_decoder_inst.place(row_decoder_offset)

        self.height = self.row_decoder.height
        self.width = self.wordline_driver_inst.rx()
