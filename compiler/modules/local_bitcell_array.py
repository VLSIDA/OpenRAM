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
from tech import drc
import debug

class local_bitcell_array(bitcell_base_array.bitcell_base_array):
    """
    A local bitcell array is a bitcell array with a wordline driver.
    This can either be a single aray on its own if there is no hierarchical WL
    or it can be combined into a larger array with hierarchical WL.
    """
    def __init__(self, rows, cols, ports, left_rbl=0, right_rbl=0, add_replica=True, name=""):
        super().__init__(name, rows, cols, 0)
        debug.info(2, "create local array of size {} rows x {} cols words".format(rows,
                                                                                  cols + left_rbl + right_rbl))

        self.rows = rows
        self.cols = cols
        self.add_replica=add_replica
        self.all_ports = ports
        
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
                                            left_rbl=1,
                                            right_rbl=1 if len(self.all_ports)>1 else 0,
                                            bitcell_ports=self.all_ports,
                                            add_replica=self.add_replica)
        self.add_mod(self.bitcell_array)

        self.wl_array = factory.create(module_type="wordline_buffer_array",
                                       rows=self.rows + len(self.all_ports),
                                       cols=self.cols)
        self.add_mod(self.wl_array)

    def add_pins(self):

        self.bitline_names = self.bitcell_array.get_all_bitline_names()
        self.add_pin_list(self.bitline_names, "INOUT")
        self.driver_wordline_inputs = [x for x in self.bitcell_array.get_all_wordline_names() if not x.startswith("dummy")]
        self.driver_wordline_outputs = [x + "i" for x in self.driver_wordline_inputs]
        self.array_wordline_inputs = [x + "i" if not x.startswith("dummy") else "gnd" for x in self.bitcell_array.get_all_wordline_names()]
        self.add_pin_list(self.wordline_names, "INPUT")
        self.replica_names = self.bitcell_array.get_rbl_wordline_names()
        self.add_pin_list(self.replica_names, "INPUT")
        self.bitline_names = self.bitcell_array.get_inouts()
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_instances(self):
        """ Create the module instances used in this design """
        
        self.wl_inst = self.add_inst(name="wl_driver",
                                     mod=self.wl_array)
        self.connect_inst(self.driver_wordline_inputs + self.driver_wordline_outputs + ["vdd", "gnd"])

        self.bitcell_array_inst = self.add_inst(name="array",
                                                mod=self.bitcell_array,
                                                offset=self.wl_inst.lr())
        self.connect_inst(self.bitline_names + self.array_wordline_inputs + ["vdd", "gnd"])

    def place(self):
        """ Place the bitcelll array to the right of the wl driver. """

        self.wl_inst.place(vector(0, self.cell.height))
        # FIXME: Replace this with a tech specific paramter
        driver_to_array_spacing = 3 * self.m3_pitch
        self.bitcell_array_inst.place(vector(self.wl_inst.rx() + driver_to_array_spacing,
                                             0))

        self.height = self.bitcell_array.height
        self.width = self.bitcell_array_inst.rx()

    def route_unused_wordlines(self):
        """ Connect the unused RBL and dummy wordlines to gnd """
        gnd_wl_names = []

        # Connect unused RBL WL to gnd
        array_rbl_names = set([x for x in self.bitcell_array.get_all_wordline_names() if x.startswith("rbl")])
        dummy_rbl_names = set([x for x in self.bitcell_array.get_all_wordline_names() if x.startswith("dummy")])
        rbl_wl_names = set([self.bitcell_array.get_rbl_wordline_names(x) for x in self.all_ports])

        gnd_wl_names = list((array_rbl_names - rbl_wl_names) | dummy_rbl_names)

        for wl_name in gnd_wl_names:
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

        for (x, y) in zip(self.driver_wordline_inputs, self.wl_array.get_inputs()):
            self.copy_layout_pin(self.wl_inst, y, x)

        supply_insts = [self.wl_inst, self.bitcell_array_inst]
        for pin_name in ["vdd", "gnd"]:
            for inst in supply_insts:
                pin_list = inst.get_pins(pin_name)
                for pin in pin_list:
                    self.add_power_pin(name=pin_name,
                                       loc=pin.center(),
                                       start_layer=pin.layer)
            
    def route(self):
        array_names = [x for x in self.bitcell_array.get_all_wordline_names() if not x.startswith("dummy")]
        for (driver_name, array_name) in zip(self.wl_array.get_outputs(), array_names):
            out_pin = self.wl_inst.get_pin(driver_name)
            in_pin = self.bitcell_array_inst.get_pin(array_name)
            mid_loc = self.wl_inst.rx() + 1.5 * self.m3_pitch
            self.add_path(out_pin.layer, [out_pin.rc(), vector(mid_loc, out_pin.cy()), in_pin.lc()])
            
        self.route_unused_wordlines()
            
