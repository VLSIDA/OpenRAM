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

class local_bitcell_array(bitcell_base_array.bitcell_base_array):
    """
    A local bitcell array is a bitcell array with a wordline driver.
    This can either be a single aray on its own if there is no hierarchical WL
    or it can be combined into a larger array with hierarchical WL.
    """
    def __init__(self, rows, cols, rbl, add_rbl=None, name=""):
        super().__init__(name, rows, cols, 0)
        debug.info(2, "create local array of size {} rows x {} cols words".format(rows, cols))

        self.rows = rows
        self.cols = cols
        self.rbl = rbl
        if add_rbl == None:
            self.add_rbl = rbl
        else:
            self.add_rbl = add_rbl

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
        self.cell = factory.create(module_type="bitcell")

        self.bitcell_array = factory.create(module_type="replica_bitcell_array",
                                            cols=self.cols,
                                            rows=self.rows,
                                            rbl=self.rbl,
                                            add_rbl=self.add_rbl)
        self.add_mod(self.bitcell_array)

        self.wl_array = factory.create(module_type="wordline_buffer_array",
                                       rows=self.rows + 1,
                                       cols=self.cols)
        self.add_mod(self.wl_array)

    def add_pins(self):

        self.wordline_names = []
        self.driver_wordline_outputs = []
        self.array_wordline_inputs = []
        
        # Port 0
        wordline_inputs = [x for x in self.bitcell_array.get_wordline_names(0) if not x.startswith("dummy")]
        if len(self.all_ports) > 1:
            # Drop off the RBL for port 1
            self.wordline_names.append(wordline_inputs[:-1])
        else:
            self.wordline_names.append(wordline_inputs)
        self.driver_wordline_outputs.append([x + "i" for x in self.wordline_names[-1]])
        self.array_wordline_inputs.append([x + "i" if not x.startswith("dummy") else "gnd" for x in self.bitcell_array.get_wordline_names(0)])

        # Port 1
        if len(self.all_ports) > 1:
            self.wordline_names.append([x for x in self.bitcell_array.get_wordline_names(1) if not x.startswith("dummy")][1:])
            self.driver_wordline_outputs.append([x + "i" for x in self.wordline_names[-1]])
            self.array_wordline_inputs.append([x + "i" if not x.startswith("dummy") else "gnd" for x in self.bitcell_array.get_wordline_names(1)])

        self.all_driver_wordline_inputs = [x for x in self.bitcell_array.get_wordline_names() if not x.startswith("dummy")]
        self.replica_names = self.bitcell_array.get_rbl_wordline_names()

        self.gnd_wl_names = []

        # Connect unused RBL WL to gnd
        array_rbl_names = set([x for x in self.bitcell_array.get_all_wordline_names() if x.startswith("rbl")])
        dummy_rbl_names = set([x for x in self.bitcell_array.get_all_wordline_names() if x.startswith("dummy")])
        rbl_wl_names = set([x for port in self.all_ports for x in self.bitcell_array.get_rbl_wordline_names(port)])
        self.gnd_wl_names = list((array_rbl_names - rbl_wl_names) | dummy_rbl_names)
        
        self.all_array_wordline_inputs = [x + "i" if x not in self.gnd_wl_names else "gnd" for x in self.bitcell_array.get_wordline_names()]

        self.bitline_names = self.bitcell_array.bitline_names
        
        # Arrays are always:
        # word lines (bottom to top)
        # bit lines (left to right)
        # vdd
        # gnd
        for port in self.all_ports:
            self.add_pin_list(self.wordline_names[port], "INPUT")
        for port in self.all_ports:
            self.add_pin_list(self.bitline_names[port], "INOUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_instances(self):
        """ Create the module instances used in this design """

        self.wl_insts = []
        for port in self.all_ports:
            self.wl_insts.append(self.add_inst(name="wl_driver",
                                               mod=self.wl_array))
            self.connect_inst(self.wordline_names[port] + self.driver_wordline_outputs[port] + ["vdd", "gnd"])

        self.bitcell_array_inst = self.add_inst(name="array",
                                                mod=self.bitcell_array)

        self.connect_inst(self.all_array_wordline_inputs + self.bitline_names + ["vdd", "gnd"])

    def place(self):
        """ Place the bitcelll array to the right of the wl driver. """
        # FIXME: Replace this with a tech specific paramter
        driver_to_array_spacing = 3 * self.m3_pitch

        self.wl_insts[0].place(vector(0, self.cell.height))

        self.bitcell_array_inst.place(vector(self.wl_insts[0].rx() + driver_to_array_spacing,
                                             0))

        if len(self.all_ports) > 1:
            self.wl_insts[1].place(vector(self.bitcell_array_inst.rx() + self.wl_array.width + driver_to_array_spacing,
                                          2 * self.cell.height),
                                   mirror="MY")

        self.height = self.bitcell_array.height
        self.width = self.bitcell_array_inst.rx()

    def route_unused_wordlines(self):
        """ Connect the unused RBL and dummy wordlines to gnd """

        for wl_name in self.gnd_wl_names:
            pin = self.bitcell_array_inst.get_pin(wl_name)
            pin_layer = pin.layer
            layer_pitch = 1.5 * getattr(self, "{}_pitch".format(pin_layer))
            left_pin_loc = pin.lc()
            right_pin_loc = pin.rc()

            # Place the pins a track outside of the array
            left_loc = left_pin_loc - vector(layer_pitch, 0)
            right_loc = right_pin_loc + vector(layer_pitch, 0)
            self.add_power_pin("gnd", left_loc, directions=("H", "H"))
            self.add_power_pin("gnd", right_loc, directions=("H", "H"))

            # Add a path to connect to the array
            self.add_path(pin_layer, [left_loc, left_pin_loc])
            self.add_path(pin_layer, [right_loc, right_pin_loc])
        
    def add_layout_pins(self):

        for (x, y) in zip(self.bitline_names, self.bitcell_array.get_inouts()):
            self.copy_layout_pin(self.bitcell_array_inst, y, x)

        for port in self.all_ports:
            for (x, y) in zip(self.wordline_names[port], self.wl_array.get_inputs()):
                self.copy_layout_pin(self.wl_insts[port], y, x)

        supply_insts = [*self.wl_insts, self.bitcell_array_inst]
        for pin_name in ["vdd", "gnd"]:
            for inst in supply_insts:
                pin_list = inst.get_pins(pin_name)
                for pin in pin_list:
                    self.add_power_pin(name=pin_name,
                                       loc=pin.center(),
                                       start_layer=pin.layer)
            
    def route(self):

        for port in self.all_ports:
            if port == 0:
                array_names = [x for x in self.bitcell_array.get_wordline_names(port) if not x.startswith("dummy")]
                if len(self.all_ports) > 1:
                    # Drop off the RBL for port 1
                    array_names = array_names[:-1]
            else:
                array_names = [x for x in self.bitcell_array.get_wordline_names(port) if not x.startswith("dummy")][1:]

            for (driver_name, array_name) in zip(self.wl_array.get_outputs(), array_names):
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
                self.add_path(out_pin.layer, [out_loc, mid_loc, in_loc])
            
        self.route_unused_wordlines()
            
