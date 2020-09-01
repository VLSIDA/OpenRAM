# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import bitcell_base_array
from globals import OPTS
from sram_factory import factory
from vector import vector
import debug
from numpy import cumsum


class global_bitcell_array(bitcell_base_array.bitcell_base_array):
    """
    Creates a global bitcell array.
    Rows is an integer number for all local arrays.
    Cols is a list of the array widths.
    add_left_rbl and add_right_
    """
    def __init__(self, rows, cols, name=""):
        # The total of all columns will be the number of columns
        super().__init__(name=name, rows=rows, cols=cols, column_offset=0)
        self.cols = cols
        self.num_cols = sum(cols)
        self.col_offsets = [0] + list(cumsum(self.cols)[:-1])
        self.rows = rows

        debug.check(len(self.all_ports)<=2, "Only support dual port or less in global bitcell array.")
        self.rbl = [1, 1 if len(self.all_ports)>1 else 0]
        self.left_rbl = self.rbl[0]
        self.right_rbl = self.rbl[1]
        
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()
        
    def create_netlist(self):
        """ Create and connect the netlist """
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):

        self.place()

        self.route()
        
        self.add_layout_pins()

        self.add_boundary()
        
        self.DRC_LVS()

    def add_modules(self):
        """ Add the modules used in this design """
        self.local_mods = []

        if self.cols == 1:
            la = factory.create(module_type="local_bitcell_array", rows=self.rows, cols=self.cols[0], rbl=self.rbl, add_rbl=[self.left_rbl, self.right_rbl])
            self.add_mod(la)
            self.local_mods.append(la)
            return
        
        for i, cols in enumerate(self.cols):
            # Always add the left RBLs to the first subarray and the right RBLs to the last subarray
            if i == 0:
                la = factory.create(module_type="local_bitcell_array", rows=self.rows, cols=cols, rbl=self.rbl, add_rbl=[self.left_rbl, 0])
            elif i == len(self.cols) - 1:
                la = factory.create(module_type="local_bitcell_array", rows=self.rows, cols=cols, rbl=self.rbl, add_rbl=[0, self.right_rbl])
            else:
                la = factory.create(module_type="local_bitcell_array", rows=self.rows, cols=cols, rbl=self.rbl, add_rbl=[0, 0])
                
            self.add_mod(la)
            self.local_mods.append(la)

    # We make these on our own and don't use the base names
    def create_all_wordline_names(self):
        pass

    # We make these on our own and don't use the base names
    def create_all_bitline_names(self):
        pass
            
    def add_pins(self):

        self.add_bitline_pins()
        self.add_wordline_pins()

        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_bitline_pins(self):
        self.bitline_names = []

        for port in self.all_ports:
            self.bitline_names.append("rbl_bl_{0}_{1}".format(port, 0))
            self.bitline_names.append("rbl_br_{0}_{1}".format(port, 0))
        
        for col in range(self.num_cols):
            for port in self.all_ports:
                self.bitline_names.append("bl_{0}_{1}".format(port, col))
                self.bitline_names.append("br_{0}_{1}".format(port, col))

        if len(self.all_ports) > 1:
            for port in self.all_ports:
                self.bitline_names.append("rbl_bl_{0}_{1}".format(port, 1))
                self.bitline_names.append("rbl_br_{0}_{1}".format(port, 1))
                
        self.add_pin_list(self.bitline_names, "INOUT")
            
    def add_wordline_pins(self):

        self.wordline_names = []
        
        self.wordline_names.append("rbl_wl_0_0")
            
        # Regular WLs
        for row in range(self.rows):
            for port in self.all_ports:
                self.wordline_names.append("wl_{0}_{1}".format(port, row))

        if len(self.all_ports) > 1:
            self.wordline_names.append("rbl_wl_1_1")

        self.add_pin_list(self.wordline_names, "INPUT")

    def create_instances(self):
        """ Create the module instances used in this design """

        
        self.local_insts = []
        for col, mod in zip(self.col_offsets, self.local_mods):
            name = "la_{0}".format(col)
            self.local_insts.append(self.add_inst(name=name,
                                                  mod=mod))
            
            temp = []
            if col == 0:
                temp.append("rbl_bl_0_0")
                temp.append("rbl_br_0_0")
                if len(self.all_ports) > 1:
                    temp.append("rbl_bl_1_0")
                    temp.append("rbl_br_1_0")
        
            port_inouts = [x for x in mod.get_inouts() if x.startswith("bl") or x.startswith("br")]
            for pin_name in port_inouts:
                # Offset of the last underscore that defines the bit number
                bit_index = pin_name.rindex('_')
                # col is the bit offset of the local array,
                # while col_value is the offset within this array
                col_value = int(pin_name[bit_index + 1:])
                # Name of signal without the bit
                base_name = pin_name[:bit_index]
                # Strip the bit and add the new one
                new_name = "{0}_{1}".format(base_name, col + col_value)
                temp.append(new_name)
            
            if len(self.all_ports) > 1 and mod == self.local_mods[-1]:
                temp.append("rbl_bl_0_1")
                temp.append("rbl_br_0_1")
                temp.append("rbl_bl_1_1")
                temp.append("rbl_br_1_1")

            for port in self.all_ports:
                port_inputs = [x for x in mod.get_inputs() if "wl_{}".format(port) in x]
                temp.extend(port_inputs)
                    
            temp.append("vdd")
            temp.append("gnd")
            self.connect_inst(temp)
        
    def place(self):
        offset = vector(0, 0)
        for inst in self.local_insts:
            inst.place(offset)
            offset = inst.rx() + 3 * self.m3_pitch

        self.height = self.local_mods[0].height
        self.width = self.local_insts[-1].rx()

    def route(self):

        # Route the global wordlines (assumes pins all line up)
        for port in self.all_ports:
            port_inputs = [x for x in self.local_mods[0].get_inputs() if "wl_{}".format(port) in x]
            for i, pin_name in enumerate(port_inputs):
                pins = [x.get_pin(pin_name) for x in self.local_insts]

                y_offset = pins[0].cy()
                if port == 0:
                    y_offset -= 1.5 * self.m3_pitch
                else:
                    y_offset += 1.5 * self.m3_pitch
                    
                start_offset = vector(pins[0].lx(), y_offset)
                end_offset = vector(pins[-1].rx(), y_offset)
                self.add_layout_pin_segment_center(text=pin_name,
                                                   layer="m3",
                                                   start=start_offset,
                                                   end=end_offset)

                for pin in pins:
                    self.add_via_stack_center(from_layer=pin.layer,
                                              to_layer="m3",
                                              offset=pin.center())
                    end_offset = vector(pin.cx(), y_offset)
                    self.add_path("m3", [pin.center(), end_offset])                                  
            
    def add_layout_pins(self):

        # Regular bitlines
        for col, inst in zip(self.col_offsets, self.local_insts):
            for port in self.all_ports:
                port_inouts = [x for x in inst.mod.get_inouts() if x.startswith("bl_{}".format(port)) or x.startswith("br_{}".format(port))]
                for pin_name in port_inouts:
                    # Offset of the last underscore that defines the bit number
                    bit_index = pin_name.rindex('_')
                    # col is the bit offset of the local array,
                    # while col_value is the offset within this array
                    col_value = int(pin_name[bit_index + 1:])
                    # Name of signal without the bit
                    base_name = pin_name[:bit_index]
                    # Strip the bit and add the new one
                    new_name = "{0}_{1}".format(base_name, col + col_value)
                    self.copy_layout_pin(inst, pin_name, new_name)

                    
        # Replica bitlines
        self.copy_layout_pin(self.local_insts[0], "rbl_bl_0_0")
        self.copy_layout_pin(self.local_insts[0], "rbl_br_0_0")
        
        if len(self.all_ports) > 1:
            self.copy_layout_pin(self.local_insts[-1], "rbl_bl_1_0")
            self.copy_layout_pin(self.local_insts[-1], "rbl_br_1_0")

        for inst in self.insts:
            self.copy_power_pins(inst, "vdd")
            self.copy_power_pins(inst, "gnd")
