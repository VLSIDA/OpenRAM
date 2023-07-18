# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from numpy import cumsum
from openram import debug
from openram.base import vector
from openram.sram_factory import factory
from openram.tech import layer_properties as layer_props
from openram import OPTS
from .bitcell_base_array import bitcell_base_array


class global_bitcell_array(bitcell_base_array):
    """
    Creates a global bitcell array.
    Rows is an integer number for all local arrays.
    Cols is a list of the array widths.
    """
    def __init__(self, rows, cols, rbl=None, left_rbl=None, right_rbl=None, name=""):
        # The total of all columns will be the number of columns
        super().__init__(name=name, rows=rows, cols=sum(cols), column_offset=0)
        self.column_sizes = cols
        self.col_offsets = [0] + list(cumsum(cols)[:-1])

        debug.check(len(self.all_ports) < 3, "Only support dual port or less in global bitcell array.")

        # This is how many RBLs are in all the arrays
        if rbl is not None:
            self.rbl = rbl
        else:
            self.rbl = [0] * len(self.all_ports)
        # This specifies which RBL to put on the left or right by port number
        # This could be an empty list
        if left_rbl is not None:
            self.left_rbl = left_rbl
        else:
            self.left_rbl = []
        # This could be an empty list
        if right_rbl is not None:
            self.right_rbl = right_rbl
        else:
            self.right_rbl=[]
        self.rbls = self.left_rbl + self.right_rbl

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

        # Special case of a single local array
        if len(self.column_sizes) == 1:
            la = factory.create(module_type="local_bitcell_array",
                                rows=self.row_size,
                                cols=self.column_sizes[0],
                                rbl=self.rbl,
                                left_rbl=self.left_rbl,
                                right_rbl=self.right_rbl)
            self.local_mods.append(la)
            return

        for i, cols in enumerate(self.column_sizes):
            # Always add the left RBLs to the first subarray
            if i == 0:
                la = factory.create(module_type="local_bitcell_array",
                                    rows=self.row_size,
                                    cols=cols,
                                    rbl=self.rbl,
                                    left_rbl=self.left_rbl)
            # Add the right RBLs to the last subarray
            elif i == len(self.column_sizes) - 1:
                la = factory.create(module_type="local_bitcell_array",
                                    rows=self.row_size,
                                    cols=cols,
                                    rbl=self.rbl,
                                    right_rbl=self.right_rbl)
            # Middle subarrays do not have any RBLs
            else:
                la = factory.create(module_type="local_bitcell_array",
                                    rows=self.row_size,
                                    cols=cols,
                                    rbl=self.rbl)

            self.local_mods.append(la)

    def add_pins(self):

        self.add_bitline_pins()
        self.add_wordline_pins()

        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_bitline_pins(self):
        # FIXME: aren't these already defined via inheritence by bitcell base array?
        self.bitline_names = [[] for x in self.all_ports]
        self.rbl_bitline_names = [[] for x in self.all_ports]

        # The bit is which port the RBL is for
        for bit in self.rbls:
            for port in self.all_ports:
                self.rbl_bitline_names[bit].append("rbl_bl_{0}_{1}".format(port, bit))
            for port in self.all_ports:
                self.rbl_bitline_names[bit].append("rbl_br_{0}_{1}".format(port, bit))

        for col in range(self.column_size):
            for port in self.all_ports:
                self.bitline_names[port].append("bl_{0}_{1}".format(port, col))
            for port in self.all_ports:
                self.bitline_names[port].append("br_{0}_{1}".format(port, col))

        # Make a flat list too
        self.all_bitline_names = [x for sl in zip(*self.bitline_names) for x in sl]
        # Make a flat list too
        self.all_rbl_bitline_names = [x for sl in zip(*self.rbl_bitline_names) for x in sl]

        for port in self.left_rbl:
            self.add_pin_list(self.rbl_bitline_names[port], "INOUT")
        self.add_pin_list(self.all_bitline_names, "INOUT")
        for port in self.right_rbl:
            self.add_pin_list(self.rbl_bitline_names[port], "INOUT")

    def add_wordline_pins(self):

        self.rbl_wordline_names = [[] for x in self.all_ports]

        self.wordline_names = [[] for x in self.all_ports]

        for bit in self.all_ports:
            if self.rbl[bit] == 0:
                continue
            for port in self.all_ports:
                self.rbl_wordline_names[port].append("rbl_wl_{0}_{1}".format(port, bit))

        self.all_rbl_wordline_names = [x for sl in zip(*self.rbl_wordline_names) for x in sl]

        # Regular WLs
        for row in range(self.row_size):
            for port in self.all_ports:
                self.wordline_names[port].append("wl_{0}_{1}".format(port, row))

        self.all_wordline_names = [x for sl in zip(*self.wordline_names) for x in sl]

        for port in range(self.rbl[0]):
            self.add_pin(self.rbl_wordline_names[port][port], "INPUT")
        self.add_pin_list(self.all_wordline_names, "INPUT")
        for port in range(self.rbl[0], self.rbl[0] + self.rbl[1]):
            self.add_pin(self.rbl_wordline_names[port][port], "INPUT")

    def create_instances(self):
        """ Create the module instances used in this design """
        self.local_insts = []
        for col, mod in zip(self.col_offsets, self.local_mods):
            name = "la_{0}".format(col)
            self.local_insts.append(self.add_inst(name=name,
                                                  mod=mod))

            temp = []
            if col == 0:
                temp.extend(self.get_rbl_bitline_names(0))

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
                temp.extend(self.get_rbl_bitline_names(1))

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

        pass

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

        # Add the global word lines
        wl_layer = layer_props.global_bitcell_array.wordline_layer

        for wl_name in self.local_mods[0].get_inputs():
            for local_inst in self.local_insts:
                wl_pin = local_inst.get_pin(wl_name)
                self.add_via_stack_center(from_layer=wl_pin.layer,
                                          to_layer=wl_layer,
                                          offset=wl_pin.center())

            left_pin = self.local_insts[0].get_pin(wl_name)
            right_pin = self.local_insts[-1].get_pin(wl_name)
            self.add_layout_pin_segment_center(text=wl_name,
                                               layer=wl_layer,
                                               start=left_pin.lc(),
                                               end=right_pin.rc())

        if len(self.rbls) > 0:
            # Replica bitlines
            self.copy_layout_pin(self.local_insts[0], "rbl_bl_0_0")
            self.copy_layout_pin(self.local_insts[0], "rbl_br_0_0")

            if len(self.all_ports) > 1:
                self.copy_layout_pin(self.local_insts[0], "rbl_bl_1_0")
                self.copy_layout_pin(self.local_insts[0], "rbl_br_1_0")
                self.copy_layout_pin(self.local_insts[-1], "rbl_bl_0_1")
                self.copy_layout_pin(self.local_insts[-1], "rbl_br_0_1")
                self.copy_layout_pin(self.local_insts[-1], "rbl_bl_1_1")
                self.copy_layout_pin(self.local_insts[-1], "rbl_br_1_1")

        for inst in self.insts:
            self.copy_power_pins(inst, "vdd")
            self.copy_power_pins(inst, "gnd")

    def get_main_array_top(self):
        return self.local_insts[0].offset.y + self.local_mods[0].get_main_array_top()

    def get_main_array_bottom(self):
        return self.local_insts[0].offset.y + self.local_mods[0].get_main_array_bottom()

    def get_main_array_left(self):
        return self.local_insts[0].offset.x + self.local_mods[0].get_main_array_left()

    def get_main_array_right(self):
        return self.local_insts[-1].offset.x + self.local_mods[-1].get_main_array_right()

    def get_column_offsets(self):
        """
        Return an array of the x offsets of all the regular bits
        """
        offsets = []
        for inst in self.local_insts:
            offsets.extend(inst.lx() + x for x in inst.mod.get_column_offsets())
        return offsets

    def graph_exclude_bits(self, targ_row, targ_col):
        """
        Excludes bits in column from being added to graph except target
        """

        # This must find which local array includes the specified column
        # Find the summation of columns that is large and take the one before
        for i, col in enumerate(self.col_offsets):
            if col > targ_col:
                break
        else:
            i = len(self.local_mods)

        # This is the array with the column
        local_array = self.local_mods[i - 1]
        # We must also translate the global array column number to the local array column number
        local_col = targ_col - self.col_offsets[i - 1]

        for mod, inst in zip(self.local_mods, self.local_insts):
            if mod == local_array:
                mod.graph_exclude_bits(targ_row, local_col)
            else:
                # Otherwise, exclude the local array inst
                self.graph_inst_exclude.add(inst)

    def graph_exclude_replica_col_bits(self):
        """
        Exclude all but replica in every local array.
        """

        for mod in self.local_mods:
            mod.graph_exclude_replica_col_bits()

    def get_cell_name(self, inst_name, row, col):
        """Gets the spice name of the target bitcell."""

        # This must find which local array includes the specified column
        # Find the summation of columns that is large and take the one before
        for i, local_col in enumerate(self.col_offsets):
            if local_col > col:
                break
        else:
            # In this case, we it should be in the last bitcell array
            i = len(self.col_offsets)

        # This is the local instance
        local_inst = self.local_insts[i - 1]
        # This is the array with the column
        local_array = self.local_mods[i - 1]
        # We must also translate the global array column number to the local array column number
        local_col = col - self.col_offsets[i - 1]

        return local_array.get_cell_name(inst_name + "{}x".format(OPTS.hier_seperator) + local_inst.name, row, local_col)

    def clear_exclude_bits(self):
        """
        Clears the bit exclusions
        """
        for mod in self.local_mods:
            mod.clear_exclude_bits()
        self.init_graph_params()

    def graph_exclude_dffs(self):
        """Exclude dffs from graph as they do not represent critical path"""

        self.graph_inst_exclude.add(self.ctrl_dff_inst)
