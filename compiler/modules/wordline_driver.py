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
        
        self.rows = rows
        self.cols = cols

        b = factory.create(module_type="bitcell")
        try:
            self.cell_multiple = cell_properties.bitcell.decoder_bitcell_multiple
        except AttributeError:
            self.cell_multiple = 1
        self.cell_height = self.cell_multiple * b.height
        
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
        for i in range(self.rows):
            self.add_pin("in_{0}".format(i), "INPUT")
        # Outputs from wordline_driver.
        for i in range(self.rows):
            self.add_pin("wl_{0}".format(i), "OUTPUT")
        self.add_pin("en", "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):
        self.and2 = factory.create(module_type="pand2",
                                   height=self.cell_height,
                                   size=self.cols)
        self.add_mod(self.and2)
        
    def route_vdd_gnd(self):
        """
        Add a pin for each row of vdd/gnd which
        are must-connects next level up.
        """

        # Find the x offsets for where the vias/pins should be placed
        xoffset_list = [self.and_inst[0].lx()]
        for num in range(self.rows):
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
        for row in range(self.rows):
            name_and = "wl_driver_and{}".format(row)

            # add and2
            self.and_inst.append(self.add_inst(name=name_and,
                                                mod=self.and2))
            self.connect_inst(["en",
                               "in_{0}".format(row),
                               "wl_{0}".format(row),
                               "vdd", "gnd"])

    def setup_layout_constants(self):
        # We may have more than one bitcell per decoder row
        self.num_rows = math.ceil(self.rows / self.cell_multiple)
        # We will place this many final decoders per row
        self.decoders_per_row = math.ceil(self.rows / self.num_rows)
            
    def place_drivers(self):
        and2_xoffset = 2 * self.m1_width + 5 * self.m1_space
        
        self.width = and2_xoffset + self.and2.width
        self.height = self.and2.height * self.num_rows
        
        for row in range(self.rows):
            #row = math.floor(inst_index / self.decoders_per_row)
            #dec = inst_index % self.decoders_per_row
            
            if (row % 2):
                y_offset = self.and2.height * (row + 1)
                inst_mirror = "MX"
            else:
                y_offset = self.and2.height * row
                inst_mirror = "R0"

            # x_off = self.internal_routing_width + dec * and_mod.width
            and2_offset = [and2_xoffset, y_offset]
            
            # add and2
            self.and_inst[row].place(offset=and2_offset,
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
        
        for row in range(self.rows):
            and_inst = self.and_inst[row]
            
            # en connection
            a_pin = and_inst.get_pin("A")
            a_pos = a_pin.lc()
            clk_offset = vector(en_pin.bc().x, a_pos.y)
            self.add_segment_center(layer="m1",
                                    start=clk_offset,
                                    end=a_pos)
            self.add_via_center(layers=self.m1_stack,
                                offset=clk_offset)

            # connect the decoder input pin to and2 B
            b_pin = and_inst.get_pin("B")
            b_pos = b_pin.lc()
            # needs to move down since B and input is
            # nearly aligned with A inv input
            up_or_down = self.m2_space if row % 2 else -self.m2_space
            input_offset = vector(0, b_pos.y + up_or_down)
            base_offset = vector(clk_offset.x, input_offset.y)
            contact_offset = vector(0.5 * self.m2_width + self.m2_space + 0.5 * contact.m1_via.width, 0)
            mid_via_offset = base_offset + contact_offset

            # must under the clk line in M1
            self.add_layout_pin_segment_center(text="in_{0}".format(row),
                                               layer="m1",
                                               start=input_offset,
                                               end=mid_via_offset)
            self.add_via_center(layers=self.m1_stack,
                                offset=mid_via_offset,
                                directions=("V", "V"))

            # now connect to the and2 B
            self.add_path("m2", [mid_via_offset, b_pos])
            contact_offset = b_pos - vector(0.5 * contact.m1_via.height, 0)
            self.add_via_center(layers=self.m1_stack,
                                offset=contact_offset,
                                directions=("H", "H"))

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
