# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
from vector import vector
import pgate
from sram_factory import factory


class pand3(pgate.pgate):
    """
    This is a simple buffer used for driving loads.
    """
    def __init__(self, name, size=1, height=None, vertical=False, add_wells=True):
        debug.info(1, "Creating pand3 {}".format(name))
        self.add_comment("size: {}".format(size))

        self.vertical = vertical
        self.size = size
        
        # Creates the netlist and layout
        pgate.pgate.__init__(self, name, height, add_wells)

    def create_netlist(self):
        self.add_pins()
        self.create_modules()
        self.create_insts()

    def create_modules(self):
        # Shield the cap, but have at least a stage effort of 4
        self.nand = factory.create(module_type="pnand3",
                                   height=self.height,
                                   add_wells=self.vertical)

        # Add the well tap to the inverter because when stacked
        # vertically it is sometimes narrower
        self.inv = factory.create(module_type="pdriver",
                                  size_list=[self.size],
                                  height=self.height,
                                  add_wells=self.add_wells)

        self.add_mod(self.nand)
        self.add_mod(self.inv)

    def create_layout(self):
        if self.vertical:
            self.height = 2 * self.nand.height
            self.width = max(self.nand.width, self.inv.width)
        else:
            self.width = self.nand.width + self.inv.width

        self.place_insts()
        self.add_wires()
        self.add_layout_pins()
        self.route_supply_rails()
        self.add_boundary()
        self.DRC_LVS()
        
    def add_pins(self):
        self.add_pin("A", "INPUT")
        self.add_pin("B", "INPUT")
        self.add_pin("C", "INPUT")
        self.add_pin("Z", "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_insts(self):
        self.nand_inst = self.add_inst(name="pand3_nand",
                                       mod=self.nand)
        self.connect_inst(["A", "B", "C", "zb_int", "vdd", "gnd"])
        
        self.inv_inst = self.add_inst(name="pand3_inv",
                                      mod=self.inv)
        self.connect_inst(["zb_int", "Z", "vdd", "gnd"])

    def place_insts(self):
        # Add NAND to the right
        self.nand_inst.place(offset=vector(0, 0))

        if self.vertical:
            # Add INV above
            self.inv_inst.place(offset=vector(self.inv.width,
                                              2 * self.nand.height),
                                mirror="XY")
        else:
            # Add INV to the right
            self.inv_inst.place(offset=vector(self.nand_inst.rx(), 0))

    def route_supply_rails(self):
        """ Add vdd/gnd rails to the top, (middle), and bottom. """
        self.add_layout_pin_rect_center(text="gnd",
                                        layer=self.route_layer,
                                        offset=vector(0.5 * self.width, 0),
                                        width=self.width)

        # Second gnd of the inverter gate
        if self.vertical:
            self.add_layout_pin_rect_center(text="gnd",
                                            layer=self.route_layer,
                                            offset=vector(0.5 * self.width, self.height),
                                            width=self.width)
        
        if self.vertical:
            # Shared between two gates
            y_offset = 0.5 * self.height
        else:
            y_offset = self.height
        self.add_layout_pin_rect_center(text="vdd",
                                        layer=self.route_layer,
                                        offset=vector(0.5 * self.width, y_offset),
                                        width=self.width)
            
    def add_wires(self):
        # nand Z to inv A
        z1_pin = self.nand_inst.get_pin("Z")
        a2_pin = self.inv_inst.get_pin("A")
        if self.vertical:
            route_layer = "m2"
            self.add_via_stack_center(offset=z1_pin.center(),
                                      from_layer=z1_pin.layer,
                                      to_layer=route_layer)
            self.add_zjog(route_layer,
                          z1_pin.uc(),
                          a2_pin.bc(),
                          "V")
            self.add_via_stack_center(offset=a2_pin.center(),
                                      from_layer=a2_pin.layer,
                                      to_layer=route_layer)
        else:
            route_layer = self.route_layer
            mid1_point = vector(z1_pin.cx(), a2_pin.cy())
            self.add_path(route_layer,
                          [z1_pin.center(), mid1_point, a2_pin.center()])

    def add_layout_pins(self):
        pin = self.inv_inst.get_pin("Z")
        self.add_layout_pin_rect_center(text="Z",
                                        layer=pin.layer,
                                        offset=pin.center(),
                                        width=pin.width(),
                                        height=pin.height())

        for pin_name in ["A", "B", "C"]:
            pin = self.nand_inst.get_pin(pin_name)
            self.add_layout_pin_rect_center(text=pin_name,
                                            layer=pin.layer,
                                            offset=pin.center(),
                                            width=pin.width(),
                                            height=pin.height())

    def analytical_delay(self, corner, slew, load=0.0):
        """ Calculate the analytical delay of DFF-> INV -> INV """
        nand_delay = self.nand.analytical_delay(corner,
                                                slew=slew,
                                                load=self.inv.input_load())
        inv_delay = self.inv.analytical_delay(corner,
                                              slew=nand_delay.slew,
                                              load=load)
        return nand_delay + inv_delay
    
    def get_stage_efforts(self, external_cout, inp_is_rise=False):
        """Get the stage efforts of the A or B -> Z path"""
        stage_effort_list = []
        stage1_cout = self.inv.get_cin()
        stage1 = self.nand.get_stage_effort(stage1_cout, inp_is_rise)
        stage_effort_list.append(stage1)
        last_stage_is_rise = stage1.is_rise
        
        stage2 = self.inv.get_stage_effort(external_cout, last_stage_is_rise)
        stage_effort_list.append(stage2)
        
        return stage_effort_list

    def get_cin(self):
        """Return the relative input capacitance of a single input"""
        return self.nand.get_cin()
        
