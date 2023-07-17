# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import vector
from openram.sram_factory import factory
from openram.tech import layer_properties as layer_props
from openram import OPTS
from .bitcell_base_array import bitcell_base_array


class local_bitcell_array(bitcell_base_array):
    """
    A local bitcell array is a bitcell array with a wordline driver.
    This can either be a single aray on its own if there is no hierarchical WL
    or it can be combined into a larger array with hierarchical WL.
    """
    def __init__(self, rows, cols, rbl=None, left_rbl=None, right_rbl=None, name=""):
        super().__init__(name=name, rows=rows, cols=cols, column_offset=0)
        debug.info(2, "Creating {0} {1}x{2} rbl: {3} left_rbl: {4} right_rbl: {5}".format(name,
                                                                                          rows,
                                                                                          cols,
                                                                                          rbl,
                                                                                          left_rbl,
                                                                                          right_rbl))

        self.rows = rows
        self.cols = cols
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

        debug.check(len(self.all_ports) < 3, "Local bitcell array only supports dual port or less.")

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

        # We don't offset this because we need to align
        # the replica bitcell in the control logic
        # self.offset_all_coordinates()

    def create_netlist(self):
        """ Create and connect the netlist """
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):

        self.place()

        self.add_layout_pins()

        self.route()

        self.add_boundary()

        self.DRC_LVS()

    def add_modules(self):
        """ Add the modules used in this design """
        # This is just used for names
        self.cell = factory.create(module_type=OPTS.bitcell)

        self.bitcell_array = factory.create(module_type="capped_replica_bitcell_array",
                                            cols=self.cols,
                                            rows=self.rows,
                                            rbl=self.rbl,
                                            left_rbl=self.left_rbl,
                                            right_rbl=self.right_rbl)

        # FIXME: this won't allow asymetric configurations such as rbl=[0, 1]
        #        but neither does a lot of this code...
        rows = self.rows + (sum(self.rbl) != 0)
        self.wl_array = factory.create(module_type="wordline_buffer_array",
                                       rows=rows,
                                       cols=self.cols)

    def add_pins(self):
        # Outputs from the wordline driver (by port)
        self.driver_wordline_outputs = []
        # Inputs to the bitcell array (by port)
        self.array_wordline_inputs = []

        self.wordline_names = self.bitcell_array.wordline_names
        self.all_wordline_names = self.bitcell_array.all_wordline_names

        self.bitline_names = self.bitcell_array.bitline_names
        self.all_bitline_names = self.bitcell_array.all_bitline_names

        self.rbl_wordline_names = self.bitcell_array.rbl_wordline_names
        self.all_rbl_wordline_names = self.bitcell_array.all_rbl_wordline_names

        self.rbl_bitline_names = self.bitcell_array.rbl_bitline_names
        self.all_rbl_bitline_names = self.bitcell_array.all_rbl_bitline_names

        self.all_array_wordline_inputs = [x + "i" for x in self.bitcell_array.get_all_wordline_names()]

        # Arrays are always:
        # bit lines (left to right)
        # word lines (bottom to top)
        # vdd
        # gnd
        for port in self.left_rbl:
            self.add_pin_list(self.rbl_bitline_names[port], "INOUT")
        self.add_pin_list(self.all_bitline_names, "INOUT")
        for port in self.right_rbl:
            self.add_pin_list(self.rbl_bitline_names[port], "INOUT")
        for port in range(self.rbl[0]):
            self.add_pin(self.rbl_wordline_names[port][port], "INPUT")
        for port in self.all_ports:
            self.add_pin_list(self.wordline_names[port], "INPUT")
        for port in range(self.rbl[0], self.rbl[0] + self.rbl[1]):
            self.add_pin(self.rbl_wordline_names[port][port], "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_instances(self):
        """ Create the module instances used in this design """

        self.wl_insts = []
        self.driver_wordline_outputs = []
        for port in self.all_ports:
            self.wl_insts.append(self.add_inst(name="wl_driver{}".format(port),
                                               mod=self.wl_array))
            temp = []
            if self.rbl[port] != 0:
                temp += [self.get_rbl_wordline_names(port)[port]]
            if port == 0:
                temp += self.get_wordline_names(port)
            else:
                temp += self.get_wordline_names(port)[::-1]
            self.driver_wordline_outputs.append([x + "i" for x in temp])

            temp += self.driver_wordline_outputs[-1]
            temp += ["vdd", "gnd"]

            self.connect_inst(temp)

        self.bitcell_array_inst = self.add_inst(name="array",
                                                mod=self.bitcell_array)
        temp = []
        for port in self.left_rbl:
            temp += self.get_rbl_bitline_names(port)
        temp += self.all_bitline_names
        for port in self.right_rbl:
            temp += self.get_rbl_bitline_names(port)

        wl_temp = []
        for port in range(self.rbl[0]):
            wl_temp += [self.get_rbl_wordline_names(port)[port]]
        wl_temp += self.get_wordline_names()
        for port in range(self.rbl[0], sum(self.rbl)):
            wl_temp += [self.get_rbl_wordline_names(port)[port]]
        temp += [x + "i" for x in wl_temp]
        temp += ["vdd", "gnd"]
        self.connect_inst(temp)

    def place(self):
        """ Place the bitcelll array to the right of the wl driver. """

        # FIXME: Replace this with a tech specific parameter
        driver_to_array_spacing = 3 * self.m3_pitch

        wl_offset = vector(0, self.bitcell_array.get_replica_bottom())
        self.wl_insts[0].place(wl_offset)

        bitcell_array_offset = vector(self.wl_insts[0].rx() + driver_to_array_spacing, 0)
        self.bitcell_array_inst.place(bitcell_array_offset)

        if len(self.all_ports) > 1:
            rbl_wl_adder = self.cell.height * (self.rbl[1] != 0)
            wl_offset = vector(self.bitcell_array_inst.rx() + self.wl_array.width + driver_to_array_spacing,
                               self.bitcell_array.get_replica_bottom() + self.wl_array.height + rbl_wl_adder)
            self.wl_insts[1].place(wl_offset,
                                   mirror="XY")

        self.height = self.bitcell_array.height
        self.width = max(self.bitcell_array_inst.rx(), max([x.rx() for x in self.wl_insts]))

    def add_layout_pins(self):

        for x in self.get_inouts():
            self.copy_layout_pin(self.bitcell_array_inst, x)

        supply_insts = [*self.wl_insts, self.bitcell_array_inst]
        for pin_name in ["vdd", "gnd"]:
            for inst in supply_insts:
                pin_list = inst.get_pins(pin_name)
                for pin in pin_list:
                    self.copy_power_pin(pin)

    def route(self):

        global_wl_layer = layer_props.global_bitcell_array.wordline_layer
        global_wl_pitch = getattr(self, "{}_pitch".format(global_wl_layer))
        global_wl_pitch_factor = layer_props.global_bitcell_array.wordline_pitch_factor
        local_wl_layer = layer_props.local_bitcell_array.wordline_layer

        # Route the global wordlines
        for port in self.all_ports:
            if self.rbl[port] != 0:
                if port == 0:
                    wordline_names = [self.get_rbl_wordline_names(port)[port]] + self.get_wordline_names(port)
                else:
                    wordline_names = [self.get_rbl_wordline_names(port)[port]] + self.get_wordline_names(port)[::-1]
            else:
                if port == 0:
                    wordline_names = self.get_wordline_names(port)
                else:
                    wordline_names = self.get_wordline_names(port)[::-1]

            wordline_pins = self.wl_array.get_inputs()

            for (wl_name, in_pin_name) in zip(wordline_names, wordline_pins):
                # wl_pin = self.bitcell_array_inst.get_pin(wl_name)
                in_pin = self.wl_insts[port].get_pin(in_pin_name)

                y_offset = in_pin.cy()

                if port == 0:
                    y_offset -= global_wl_pitch_factor * global_wl_pitch
                else:
                    y_offset += global_wl_pitch_factor * global_wl_pitch
                mid = vector(in_pin.cx(), y_offset)

                self.add_layout_pin_rect_center(text=wl_name,
                                                layer=global_wl_layer,
                                                offset=mid)

                self.add_path(local_wl_layer, [in_pin.center(), mid])

                # A short jog to the global line
                self.add_via_stack_center(from_layer=in_pin.layer,
                                          to_layer=local_wl_layer,
                                          offset=in_pin.center(),
                                          min_area=True)
                self.add_path(local_wl_layer, [in_pin.center(), mid])
                self.add_via_stack_center(from_layer=local_wl_layer,
                                          to_layer=global_wl_layer,
                                          offset=mid,
                                          min_area=True)
                # Add the global WL pin
                self.add_layout_pin_rect_center(text=wl_name,
                                                layer=global_wl_layer,
                                                offset=mid)
        # Route the buffers
        for port in self.all_ports:
            driver_outputs = self.driver_wordline_outputs[port]

            for (driver_name, net_name) in zip(self.wl_insts[port].mod.get_outputs(), driver_outputs):
                array_name = net_name[:-1]
                out_pin = self.wl_insts[port].get_pin(driver_name)
                in_pin = self.bitcell_array_inst.get_pin(array_name)
                if port == 0:
                    out_loc = out_pin.rc()
                    mid_loc = vector(self.wl_insts[port].rx() + 1.5 * self.m3_pitch, out_loc.y)
                    in_loc = in_pin.lc()
                else:
                    out_loc = out_pin.lc()
                    mid_loc = vector(self.wl_insts[port].lx() - 1.5 * self.m3_pitch, out_loc.y)
                    in_loc = in_pin.rc()

                self.add_path(out_pin.layer, [out_loc, mid_loc])
                self.add_via_stack_center(from_layer=out_pin.layer,
                                          to_layer=in_pin.layer,
                                          offset=mid_loc)
                self.add_path(in_pin.layer, [mid_loc, in_loc])

    def get_main_array_top(self):
        return self.bitcell_array_inst.by() + self.bitcell_array.get_main_array_top()

    def get_main_array_bottom(self):
        return self.bitcell_array_inst.by() + self.bitcell_array.get_main_array_bottom()

    def get_main_array_left(self):
        return self.bitcell_array_inst.lx() + self.bitcell_array.get_main_array_left()

    def get_main_array_right(self):
        return self.bitcell_array_inst.lx() + self.bitcell_array.get_main_array_right()

    def get_column_offsets(self):
        """
        Return an array of the x offsets of all the regular bits
        """
        # must add the offset of the instance
        offsets = [self.bitcell_array_inst.lx() + x for x in self.bitcell_array.get_column_offsets()]
        return offsets

    def graph_exclude_bits(self, targ_row=None, targ_col=None):
        """
        Excludes bits in column from being added to graph except target
        """
        self.bitcell_array.graph_exclude_bits(targ_row, targ_col)

    def graph_exclude_replica_col_bits(self):
        """
        Exclude all but replica in the local array.
        """

        self.bitcell_array.graph_exclude_replica_col_bits()

    def get_cell_name(self, inst_name, row, col):
        """Gets the spice name of the target bitcell."""
        return self.bitcell_array.get_cell_name(inst_name + "{}x".format(OPTS.hier_seperator) + self.bitcell_array_inst.name, row, col)

    def clear_exclude_bits(self):
        """
        Clears the bit exclusions
        """
        self.bitcell_array.clear_exclude_bits()
