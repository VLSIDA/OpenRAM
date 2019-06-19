# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California 
# All rights reserved.
#

import debug
import design
from tech import drc, spice
from vector import vector
from globals import OPTS
from sram_factory import factory
import logical_effort
import bitcell_array
import replica_column
import dummy_array

class replica_bitcell_array(design.design):
    """
    Creates a bitcell arrow of cols x rows and then adds the replica and dummy columns
    and rows for one or two read ports. Replica columns are on the left and right, respectively.
    Dummy are the outside columns/rows with WL and BL tied to gnd.
    Requires a regular bitcell array, replica bitcell, and dummy bitcell (Bl/BR disconnected).
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

    def add_modules(self):
        """  Array and dummy/replica columns 

        d or D = dummy cell (caps to distinguish grouping)
        r or R = replica cell (caps to distinguish grouping)
        b or B = bitcell 
         replica columns 1 
         v              v
        bdDDDDDDDDDDDDDDdb <- Dummy row 
        bdDDDDDDDDDDDDDDrb <- Dummy row 
        br--------------rb
        br|   Array    |rb
        br| row x col  |rb
        br--------------rb
        brDDDDDDDDDDDDDDdb <- Dummy row
        bdDDDDDDDDDDDDDDdb <- Dummy row

          ^^^^^^^^^^^^^^^
          dummy rows cols x 1

        ^ dummy columns  ^
          1 x (rows + 4)
        """

        # Bitcell for port names only
        self.cell = factory.create(module_type="bitcell")

        # Bitcell array
        self.bitcell_array = factory.create(module_type="bitcell_array",
                                            cols=self.column_size,
                                            rows=self.row_size)
        self.add_mod(self.bitcell_array)

        # Replica bitline 
        self.replica_column = factory.create(module_type="replica_column",
                                                  rows=self.row_size + 4)
        self.add_mod(self.replica_column)
        
        # Dummy row
        self.dummy_row = factory.create(module_type="dummy_array",
                                        rows=1,
                                        cols=self.column_size)
        self.add_mod(self.dummy_row)

        # Dummy col
        self.dummy_col = factory.create(module_type="dummy_array",
                                        cols=1,
                                        rows=self.row_size + 4)
        self.add_mod(self.dummy_col)
        
        

    def add_pins(self):

        self.wl_names = [x for x in self.bitcell_array.pins if x.startswith("w")]
        self.bl_names = [x for x in self.bitcell_array.pins if x.startswith("b")]
        
        # top/bottom rows (in the middle)
        self.replica_wl_names = ["replica_"+x for x in self.cell.pins if x.startswith("w")]
        self.dummy_wl_names = ["dummy_"+x for x in self.cell.pins if x.startswith("w")]
        self.dummy_bl_names = ["dummy_"+x for x in self.cell.pins if x.startswith("b")]
        self.dummy_row_bl_names = self.bl_names

        # dummy row and replica on each side of the bitcell rows
        self.replica_col_wl_names = [x+"_0" for x in self.dummy_wl_names] \
                                    + ["replica_"+x+"_0" for x in self.cell.list_all_wl_names()] \
                                    + self.wl_names \
                                    + ["replica_"+x+"_1" for x in self.cell.list_all_wl_names()] \
                                    + [x+"_1" for x in self.dummy_wl_names]
        self.replica_bl_names = ["replica_"+x for x in self.cell.pins if x.startswith("b")]
        
        # left/right rows
        self.dummy_col_wl_names = self.replica_col_wl_names
        
        
        self.add_pin_list(self.bl_names)
        self.add_pin_list([x+"_0" for x in self.replica_bl_names])
        self.add_pin_list([x+"_1" for x in self.replica_bl_names]) 
        self.add_pin_list([x for x in self.replica_col_wl_names if not x.startswith("dummy")])

        self.add_pin("vdd")
        self.add_pin("gnd")

        
    def create_instances(self):
        """ Create the module instances used in this design """

        supplies = ["vdd", "gnd"]
        # Main array
        self.bitcell_array_inst=self.add_inst(name="bitcell_array",
                                              mod=self.bitcell_array)
        self.connect_inst(self.bitcell_array.pins)

        # Replica columns (two even if one port for now)
        self.replica_col_left_inst=self.add_inst(name="replica_col_left",
                                                 mod=self.replica_column)
        self.connect_inst([x+"_0" for x in self.replica_bl_names] + self.replica_col_wl_names + supplies)
        
        self.replica_col_right_inst=self.add_inst(name="replica_col_right",
                                                  mod=self.replica_column)
        self.connect_inst([x+"_1" for x in self.replica_bl_names] + self.replica_col_wl_names[::-1]  + supplies)
            
        # Replica rows with replica bitcell
        self.dummy_row_bottop_inst=self.add_inst(name="dummy_row_bottop",
                                                 mod=self.dummy_row)
        self.connect_inst(self.dummy_row_bl_names + [x+"_0" for x in self.replica_wl_names] + supplies)
        self.dummy_row_topbot_inst=self.add_inst(name="dummy_row_topbot",
                                                 mod=self.dummy_row)
        self.connect_inst(self.dummy_row_bl_names + [x+"_1" for x in self.replica_wl_names] + supplies)
        
        
        # Dummy rows without replica bitcell
        self.dummy_row_botbot_inst=self.add_inst(name="dummy_row_botbot",
                                                 mod=self.dummy_row)
        self.connect_inst(self.dummy_row_bl_names + [x+"_0" for x in self.dummy_wl_names] + supplies)
        self.dummy_row_toptop_inst=self.add_inst(name="dummy_row_toptop",
                                                 mod=self.dummy_row)
        self.connect_inst(self.dummy_row_bl_names + [x+"_1" for x in self.dummy_wl_names] + supplies)


        # Dummy columns
        self.dummy_col_left_inst=self.add_inst(name="dummy_col_left",
                                               mod=self.dummy_col)
        self.connect_inst([x+"_0" for x in self.dummy_bl_names] + self.dummy_col_wl_names + supplies)
        self.dummy_col_right_inst=self.add_inst(name="dummy_col_right",
                                               mod=self.dummy_col)
        self.connect_inst([x+"_1" for x in self.dummy_bl_names] + self.dummy_col_wl_names + supplies)
        

                
    def create_layout(self):

        self.height = (self.row_size+4)*self.dummy_row.height
        self.width = (self.column_size+4)*self.replica_column.width

        # This is a bitcell x bitcell offset to scale
        offset = vector(self.replica_column.width, self.dummy_row.height)
        
        self.bitcell_array_inst.place(offset=[0,0])
        self.replica_col_left_inst.place(offset=offset.scale(-1,-2))
        self.replica_col_right_inst.place(offset=offset.scale(0,2)+self.bitcell_array_inst.ur(),
                                            mirror="MX")
        
        self.dummy_row_toptop_inst.place(offset=offset.scale(0,2)+self.bitcell_array_inst.ul(),
                                         mirror="MX")
        self.dummy_row_topbot_inst.place(offset=offset.scale(0,0)+self.bitcell_array_inst.ul())
        self.dummy_row_bottop_inst.place(offset=offset.scale(0,0),
                                         mirror="MX")
        self.dummy_row_botbot_inst.place(offset=offset.scale(0,-2))

        self.dummy_col_left_inst.place(offset=offset.scale(-2,-2))
        self.dummy_col_right_inst.place(offset=offset.scale(1,-2)+self.bitcell_array_inst.lr())

        self.translate_all(offset.scale(-2,-2))
        
        self.add_layout_pins()
        
        self.add_boundary()
        
        self.DRC_LVS()

                
    def add_layout_pins(self):
        """ Add the layout pins """

        # Main array wl and bl/br
        pin_names = self.bitcell_array.get_pin_names()
        for pin_name in pin_names:
            if pin_name.startswith("wl"):
                pin_list = self.bitcell_array_inst.get_pins(pin_name)
                for pin in pin_list:
                    self.add_layout_pin_rect_center(text=pin_name,
                                                    layer=pin.layer,
                                                    offset=pin.center(),
                                                    width=self.width,
                                                    height=pin.height())
            elif pin_name.startswith("bl") or pin_name.startswith("br"):
                pin_list = self.bitcell_array_inst.get_pins(pin_name)
                for pin in pin_list:
                    self.add_layout_pin_rect_center(text=pin_name,
                                                    layer=pin.layer,
                                                    offset=pin.center(),
                                                    width=pin.width(),
                                                    height=self.height)


        for index,(side1,side2) in enumerate([("bottop","left"),("topbot","right")]):
            inst = getattr(self, "dummy_row_{}_inst".format(side1))
            pin_names = inst.mod.get_pin_names()
            for pin_name in pin_names:
                if pin_name.startswith("wl"):                    
                    pin_list = inst.get_pins(pin_name)
                    for pin in pin_list:
                        name = "replica_{0}_{1}".format(pin_name,index)
                        self.add_layout_pin_rect_center(text=name,
                                                        layer=pin.layer,
                                                        offset=pin.center(),
                                                        width=self.width,
                                                        height=pin.height())

        # Replica columns
        for index,side in enumerate(["left","right"]):
            inst = getattr(self, "replica_col_{}_inst".format(side))
            pin_names = inst.mod.get_pin_names()
            for pin_name in pin_names:
                if pin_name.startswith("bl") or pin_name.startswith("br"):
                    pin_list = inst.get_pins(pin_name)
                    for pin in pin_list:
                        name = "replica_{0}_{1}".format(pin_name,index)
                        self.add_layout_pin(text=name,
                                            layer=pin.layer,
                                            offset=pin.ll().scale(1,0),
                                            width=pin.width(),
                                            height=self.height)

                    
        for pin_name in ["vdd","gnd"]:
            for inst in [self.bitcell_array_inst,
                         self.replica_col_left_inst, self.replica_col_right_inst,
                         self.dummy_col_left_inst, self.dummy_col_right_inst,
                         self.dummy_row_toptop_inst, self.dummy_row_topbot_inst,
                         self.dummy_row_bottop_inst, self.dummy_row_botbot_inst]:
                pin_list = inst.get_pins(pin_name)
                for pin in pin_list:
                    self.add_power_pin(name=pin_name, loc=pin.center(), vertical=True, start_layer=pin.layer)


        # Non-pins

        for side in ["botbot", "toptop"]:
            inst = getattr(self, "dummy_row_{}_inst".format(side))
            pin_names = inst.mod.get_pin_names()
            for pin_name in pin_names:
                if pin_name.startswith("wl"):                    
                    pin_list = inst.get_pins(pin_name)
                    for pin in pin_list:
                        self.add_rect_center(layer=pin.layer,
                                             offset=pin.center(),
                                             width=self.width,
                                             height=pin.height())


        for side in ["left", "right"]:
            inst = getattr(self, "dummy_col_{}_inst".format(side))
            pin_names = inst.mod.get_pin_names()
            for pin_name in pin_names:
                if pin_name.startswith("b"):                    
                    pin_list = inst.get_pins(pin_name)
                    for pin in pin_list:
                        self.add_rect_center(layer=pin.layer,
                                             offset=pin.center(),
                                             width=pin.width(),
                                             height=self.height)
                        

    
    def analytical_delay(self, corner, slew, load):
        """Returns relative delay of the bitline in the bitcell array"""
        from tech import parameter
        #The load being driven/drained is mostly the bitline but could include the sense amp or the column mux.
        #The load from the bitlines is due to the drain capacitances from all the other bitlines and wire parasitics.
        drain_load = logical_effort.convert_farad_to_relative_c(parameter['bitcell_drain_cap'])
        wire_unit_load = .05 * drain_load #Wires add 5% to this.
        bitline_load = (drain_load+wire_unit_load)*self.row_size
        return [self.cell.analytical_delay(corner, slew, load+bitline_load)]
    
    def analytical_power(self, corner, load):
        """Power of Bitcell array and bitline in nW."""
        from tech import drc, parameter
        
        # Dynamic Power from Bitline
        bl_wire = self.gen_bl_wire()
        cell_load = 2 * bl_wire.return_input_cap() 
        bl_swing = parameter["rbl_height_percentage"]
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

    def output_load(self, bl_pos=0):
        bl_wire = self.gen_bl_wire()
        return bl_wire.wire_c # sense amp only need to charge small portion of the bl
                              # set as one segment for now

    def input_load(self):
        wl_wire = self.gen_wl_wire()
        return wl_wire.return_input_cap()

    def get_wordline_cin(self):
        """Get the relative input capacitance from the wordline connections in all the bitcell"""
        #A single wordline is connected to all the bitcells in a single row meaning the capacitance depends on the # of columns
        bitcell_wl_cin = self.cell.get_wl_cin()
        total_cin = bitcell_wl_cin * self.column_size
        return total_cin
