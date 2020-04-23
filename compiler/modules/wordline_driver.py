# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
import design
import math
import contact
from vector import vector
from sram_factory import factory
from globals import OPTS
from tech import cell_properties


class wordline_driver(design.design):
    """
    Creates a Wordline Driver
    Generates the wordline-driver to drive the bitcell
    """

    def __init__(self, name, rows, cols):
        design.design.__init__(self, name)
        debug.info(1, "Creating {0}".format(self.name))
        self.add_comment("rows: {0} cols: {1}".format(rows, cols))
        
        self.bitcell_rows = rows
        self.bitcell_cols = cols

        b = factory.create(module_type="bitcell")
        try:
            self.cell_multiple = cell_properties.bitcell.decoder_bitcell_multiple
        except AttributeError:
            self.cell_multiple = 1
        self.cell_height = self.cell_multiple * b.height
        
        # We may have more than one bitcell per decoder row
        self.num_rows = math.ceil(self.bitcell_rows / self.cell_multiple)
        # We will place this many final decoders per row
        self.decoders_per_row = math.ceil(self.bitcell_rows / self.num_rows)
        
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_drivers()
        
    def create_layout(self):
        self.setup_layout_constants()
        self.place_drivers()
        self.route_layout()
        self.route_vdd_gnd()
        self.offset_all_coordinates()
        self.add_boundary()
        self.DRC_LVS()
        
    def add_pins(self):
        # inputs to wordline_driver.
        for i in range(self.bitcell_rows):
            self.add_pin("in_{0}".format(i), "INPUT")
        # Outputs from wordline_driver.
        for i in range(self.bitcell_rows):
            self.add_pin("wl_{0}".format(i), "OUTPUT")
        self.add_pin("en", "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):
        self.and2 = factory.create(module_type="pand2",
                                   height=self.cell_height,
                                   size=self.bitcell_cols)
        self.add_mod(self.and2)
        
    def route_vdd_gnd(self):
        """
        Add a pin for each row of vdd/gnd which
        are must-connects next level up.
        """

        # Find the x offsets for where the vias/pins should be placed
        xoffset_list = [self.and_inst[0].lx()]
        for num in range(self.bitcell_rows):
            # this will result in duplicate polygons for rails, but who cares
            
            # use the inverter offset even though it will be the and's too
            (gate_offset, y_dir) = self.get_gate_offset(0,
                                                        self.and2.height,
                                                        num)
            # Route both supplies
            for name in ["vdd", "gnd"]:
                supply_pin = self.and_inst[num].get_pin(name)

                # Add pins in two locations
                for xoffset in xoffset_list:
                    pin_pos = vector(xoffset, supply_pin.cy())
                    self.add_power_pin(name, pin_pos)
            
    def create_drivers(self):
        self.and_inst = []
        for row in range(self.bitcell_rows):
            name_and = "wl_driver_and{}".format(row)

            # add and2
            self.and_inst.append(self.add_inst(name=name_and,
                                                mod=self.and2))
            self.connect_inst(["in_{0}".format(row),
                               "en",
                               "wl_{0}".format(row),
                               "vdd", "gnd"])

    def setup_layout_constants(self):
        # We may have more than one bitcell per decoder row
        self.driver_rows = math.ceil(self.bitcell_rows / self.cell_multiple)
        # We will place this many final decoders per row
        self.decoders_per_row = math.ceil(self.bitcell_rows / self.driver_rows)
            
    def place_drivers(self):
        and2_xoffset = 2 * self.m1_width + 5 * self.m1_space
        
        self.width = and2_xoffset + self.decoders_per_row * self.and2.width
        self.height = self.and2.height * self.driver_rows
        
        for inst_index in range(self.bitcell_rows):
            row = math.floor(inst_index / self.decoders_per_row)
            dec = inst_index % self.decoders_per_row
            
            if (row % 2):
                y_offset = self.and2.height * (row + 1)
                inst_mirror = "MX"
            else:
                y_offset = self.and2.height * row
                inst_mirror = "R0"

            x_offset = and2_xoffset + dec * self.and2.width
            and2_offset = [x_offset, y_offset]
            
            # add and2
            self.and_inst[inst_index].place(offset=and2_offset,
                                            mirror=inst_mirror)

    def route_layout(self):
        """ Route all of the signals """

        # Wordline enable connection
        en_offset = [self.m1_width + 2 * self.m1_space, 0]
        en_pin = self.add_layout_pin(text="en",
                                     layer="m2",
                                     offset=en_offset,
                                     width=self.m2_width,
                                     height=self.height)
        
        for inst_index in range(self.bitcell_rows):
            and_inst = self.and_inst[inst_index]
            row = math.floor(inst_index / self.decoders_per_row)
            dec = inst_index % self.decoders_per_row
            
            # en connection
            b_pin = and_inst.get_pin("B")
            b_pos = b_pin.center()
            clk_offset = vector(en_pin.bc().x, b_pos.y)
            self.add_segment_center(layer="m2",
                                    start=clk_offset,
                                    end=b_pos)
            self.add_via_center(layers=self.m1_stack,
                                offset=b_pos)

            # connect the decoder input pin to and2 A
            a_pin = and_inst.get_pin("A")
            a_pos = a_pin.center()
            a_offset = vector(clk_offset.x, a_pos.y)
            # must under the clk line in M1
            self.add_layout_pin_segment_center(text="in_{0}".format(row),
                                               layer="m1",
                                               start=vector(0, a_pos.y),
                                               end=a_pos)

            # output each WL on the right
            wl_offset = and_inst.get_pin("Z").rc()
            self.add_layout_pin_segment_center(text="wl_{0}".format(row),
                                               layer="m1",
                                               start=wl_offset,
                                               end=wl_offset - vector(self.m1_width, 0))

    def determine_wordline_stage_efforts(self, external_cout, inp_is_rise=True):
        """
        Follows the clk_buf to a wordline signal adding
        each stages stage effort to a list.
        """
        stage_effort_list = []
        
        stage1 = self.and2.get_stage_effort(external_cout, inp_is_rise)
        stage_effort_list.append(stage1)
        
        return stage_effort_list
        
    def get_wl_en_cin(self):
        """
        Get the relative capacitance of all
        the enable connections in the bank
        """
        # The enable is connected to a and2 for every row.
        total_cin = self.and2.get_cin() * self.rows
        return total_cin
