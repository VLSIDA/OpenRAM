# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
import design
from tech import drc, spice
from vector import vector
from globals import OPTS
from sram_factory import factory
import logical_effort

class bitcell_array(design.design):
    """
    Creates a rows x cols array of memory cells. Assumes bit-lines
    and word line is connected by abutment.
    Connects the word lines and bit lines.
    """
    def __init__(self, cols, rows, name):
        design.design.__init__(self, name)
        debug.info(1, "Creating {0} {1} x {2}".format(self.name, rows, cols))
        self.add_comment("rows: {0} cols: {1}".format(rows, cols))

        self.column_size = cols
        self.row_size = rows

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

        # We don't offset this because we need to align
        # the replica bitcell in the control logic
        #self.offset_all_coordinates()
        
        
    def create_netlist(self):
        """ Create and connect the netlist """
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):

        # We increase it by a well enclosure so the precharges don't overlap our wells
        self.height = self.row_size*self.cell.height 
        self.width = self.column_size*self.cell.width 
        
        xoffset = 0.0
        for col in range(self.column_size):
            yoffset = 0.0
            for row in range(self.row_size):
                name = "bit_r{0}_c{1}".format(row, col)

                if row % 2:
                    tempy = yoffset + self.cell.height
                    dir_key = "MX"
                else:
                    tempy = yoffset
                    dir_key = ""

                self.cell_inst[row,col].place(offset=[xoffset, tempy],
                                              mirror=dir_key)
                yoffset += self.cell.height
            xoffset += self.cell.width

        self.add_layout_pins()

        self.add_boundary()
        
        self.DRC_LVS()

    def add_pins(self):
        row_list = self.cell.get_all_wl_names()
        column_list = self.cell.get_all_bitline_names()
        for col in range(self.column_size):
            for cell_column in column_list:
                self.add_pin(cell_column+"_{0}".format(col), "INOUT")
        for row in range(self.row_size):
            for cell_row in row_list:
                    self.add_pin(cell_row+"_{0}".format(row), "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):
        """ Add the modules used in this design """
        self.cell = factory.create(module_type="bitcell")
        self.add_mod(self.cell)

    def get_bitcell_pins(self, col, row):
        """ Creates a list of connections in the bitcell, 
        indexed by column and row, for instance use in bitcell_array """

        bitcell_pins = []
        
        pin_names = self.cell.get_all_bitline_names()
        for pin in pin_names:
            bitcell_pins.append(pin+"_{0}".format(col))
        pin_names = self.cell.get_all_wl_names()
        for pin in pin_names:
            bitcell_pins.append(pin+"_{0}".format(row))
        bitcell_pins.append("vdd")
        bitcell_pins.append("gnd")
        
        return bitcell_pins
    
        
    def create_instances(self):
        """ Create the module instances used in this design """
        self.cell_inst = {}
        for col in range(self.column_size):
            for row in range(self.row_size):
                name = "bit_r{0}_c{1}".format(row, col)
                self.cell_inst[row,col]=self.add_inst(name=name,
                                                      mod=self.cell)
                self.connect_inst(self.get_bitcell_pins(col, row))
        
    def add_layout_pins(self):
        """ Add the layout pins """
        
        row_list = self.cell.get_all_wl_names()
        column_list = self.cell.get_all_bitline_names()
        
        for col in range(self.column_size):
            for cell_column in column_list:
                bl_pin = self.cell_inst[0,col].get_pin(cell_column)
                self.add_layout_pin(text=cell_column+"_{0}".format(col),
                                    layer=bl_pin.layer,
                                    offset=bl_pin.ll().scale(1,0),
                                    width=bl_pin.width(),
                                    height=self.height)

        for row in range(self.row_size):
            for cell_row in row_list:
                wl_pin = self.cell_inst[row,0].get_pin(cell_row)
                self.add_layout_pin(text=cell_row+"_{0}".format(row),
                                    layer=wl_pin.layer,
                                    offset=wl_pin.ll().scale(0,1),
                                    width=self.width,
                                    height=wl_pin.height())

        # For every second row and column, add a via for gnd and vdd
        for row in range(self.row_size):
            for col in range(self.column_size):
                inst = self.cell_inst[row,col]
                for pin_name in ["vdd", "gnd"]:
                    for pin in inst.get_pins(pin_name):
                        self.add_power_pin(name=pin_name, loc=pin.center(), vertical=True, start_layer=pin.layer)

    def analytical_power(self, corner, load):
        """Power of Bitcell array and bitline in nW."""
        from tech import drc, parameter
        
        # Dynamic Power from Bitline
        bl_wire = self.gen_bl_wire()
        cell_load = 2 * bl_wire.return_input_cap() 
        bl_swing = OPTS.rbl_delay_percentage
        freq = spice["default_event_rate"]
        bitline_dynamic = self.calc_dynamic_power(corner, cell_load, freq, swing=bl_swing)
        
        #Calculate the bitcell power which currently only includes leakage 
        cell_power = self.cell.analytical_power(corner, load)
        
        #Leakage power grows with entire array and bitlines.
        total_power = self.return_power(cell_power.dynamic + bitline_dynamic * self.column_size,
                                        cell_power.leakage * self.column_size * self.row_size)
        return total_power

    def gen_wl_wire(self):
        if OPTS.netlist_only:
            width = 0
        else:
            width = self.width
        wl_wire = self.generate_rc_net(int(self.column_size), width, drc("minwidth_metal1"))
        wl_wire.wire_c = 2*spice["min_tx_gate_c"] + wl_wire.wire_c # 2 access tx gate per cell
        return wl_wire

    def gen_bl_wire(self):
        if OPTS.netlist_only:
            height = 0
        else:
            height = self.height
        bl_pos = 0
        bl_wire = self.generate_rc_net(int(self.row_size-bl_pos), height, drc("minwidth_metal1"))
        bl_wire.wire_c =spice["min_tx_drain_c"] + bl_wire.wire_c # 1 access tx d/s per cell
        return bl_wire

    def get_wordline_cin(self):
        """Get the relative input capacitance from the wordline connections in all the bitcell"""
        #A single wordline is connected to all the bitcells in a single row meaning the capacitance depends on the # of columns
        bitcell_wl_cin = self.cell.get_wl_cin()
        total_cin = bitcell_wl_cin * self.column_size
        return total_cin
        
    def graph_exclude_bits(self, targ_row, targ_col):
        """Excludes bits in column from being added to graph except target"""
        #Function is not robust with column mux configurations
        for row in range(self.row_size):
            for col in range(self.column_size):
                if row == targ_row and col == targ_col:
                    continue
                self.graph_inst_exclude.add(self.cell_inst[row,col])
            
    def get_cell_name(self, inst_name, row, col):
        """Gets the spice name of the target bitcell.""" 
        return inst_name+'.x'+self.cell_inst[row,col].name, self.cell_inst[row,col]
