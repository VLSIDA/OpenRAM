# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import design
from openram.base import vector
from openram.sram_factory import factory
from openram.tech import parameter
from openram import OPTS


class pwrite_driver(design):
    """
    The pwrite_driver is two tristate inverters that drive the bitlines.
    The data input is first inverted before one tristate.
    The inverted enable is also generated to control one tristate.
    """
    def __init__(self, name, size=0):
        debug.error("pwrite_driver not implemented yet.", -1)
        debug.info(1, "creating pwrite_driver {}".format(name))
        super().__init__(name)
        self.size = size
        self.beta = parameter["beta"]
        self.pmos_width = self.beta * self.size * parameter["min_tx_size"]
        self.nmos_width = self.size * parameter["min_tx_size"]

        # The tech M2 pitch is based on old via orientations
        self.m2_pitch = self.m2_space + self.m2_width

        # Width is matched to the bitcell,
        # Height will be variable
        self.bitcell = factory.create(module_type=OPTS.bitcell)
        self.width = self.bitcell.width

        # Creates the netlist and layout
        # Since it has variable height, it is not a pgate.
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()
            self.DRC_LVS()

    def create_netlist(self):
        self.add_pins()
        self.add_modules()
        self.create_insts()

    def create_layout(self):
        self.place_modules()
        self.route_wires()
        self.route_supplies()
        self.add_boundary()

    def add_pins(self):
        self.add_pin("din", "INPUT")
        self.add_pin("bl", "OUTPUT")
        self.add_pin("br", "OUTPUT")
        self.add_pin("en", "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):

        # Tristate inverter
        self.tri = factory.create(module_type="ptristate_inv", height="min")
        debug.check(self.tri.width<self.width,
                    "Could not create tristate inverter to match bitcell width")

        #self.tbuf = factory.create(module_type="ptristate_buf",
        #height="min")
        #debug.check(self.tbuf.width<self.width,
        #"Could not create tristate buffer to match bitcell width")

        # Inverter for din and en
        self.inv = factory.create(module_type="pinv", under_rail_vias=True)

    def create_insts(self):
        # Enable inverter
        self.en_inst = self.add_inst(name="en_inv", mod=self.inv)
        self.connect_inst(["en", "en_bar", "vdd", "gnd"])

        # Din inverter
        self.din_inst = self.add_inst(name="din_inv", mod=self.inv)
        self.connect_inst(["din", "din_bar", "vdd", "gnd"])

        # Bitline tristate
        self.bl_inst = self.add_inst(name="bl_tri", mod=self.tri)
        self.connect_inst(["din_bar", "bl", "en", "en_bar", "vdd", "gnd"])

        # Bitline bar tristate
        self.br_inst = self.add_inst(name="br_tri", mod=self.tri)
        self.connect_inst(["din", "br", "en", "en_bar", "vdd", "gnd"])


    def place_modules(self):

        # Add enable to the right
        self.din_inst.place(vector(0, 0))

        # Add BR tristate above
        self.br_inst.place(vector(0, self.en_inst.uy()+self.br_inst.height), mirror="MX")

        # Add BL tristate buffer
        #print(self.bl_inst.width,self.width)
        self.bl_inst.place(vector(self.width,self.br_inst.uy()), mirror="MY")

        # Add din to the left
        self.en_inst.place(vector(self.width, self.bl_inst.uy()+self.en_inst.height), rotate=180)

        self.height = self.en_inst.uy()


    def route_bitlines(self):
        """
        Route the bitlines to the spacing of the bitcell
        ( even though there may be a column mux  )
        """

        # Second from left track and second from right track
        right_x = self.width + self.m2_pitch
        left_x = -self.m2_pitch

        bl_xoffset = left_x
        bl_out=vector(bl_xoffset, self.height)
        bl_in=self.bl_inst.get_pin("out").center()
        self.add_via_center(layers=self.m1_stack,
                            offset=bl_in)

        bl_mid = vector(bl_out.x,bl_in.y)
        self.add_path("m2", [bl_in, bl_mid, bl_out])

        self.add_layout_pin_rect_center(text="bl",
                                        layer="m2",
                                        offset=bl_out)

        br_xoffset = right_x
        br_out=vector(br_xoffset, self.height)
        br_in=self.br_inst.get_pin("out").center()
        self.add_via_center(layers=self.m1_stack,
                            offset=br_in)

        br_mid = vector(br_out.x,br_in.y)
        self.add_path("m2", [br_in, br_mid, br_out])
        self.add_layout_pin_rect_center(text="br",
                                        layer="m2",
                                        offset=br_out)

        #br_xoffset = b.get_pin("br".cx()
        #self.br_inst.get_pin("br")

    def route_din(self):

        # Left
        track_xoff = self.get_m2_track(1)

        din_loc = self.din_inst.get_pin("A").center()
        self.add_via_stack_center("m1", "m2", din_loc)
        din_track = vector(track_xoff,din_loc.y)

        br_in = self.br_inst.get_pin("in").center()
        self.add_via_stack_center("m1", "m2", br_in)
        br_track = vector(track_xoff,br_in.y)

        din_in = vector(track_xoff,0)

        self.add_path("m2", [din_in,  din_track, din_loc, din_track, br_track, br_in])

        self.add_layout_pin_rect_center(text="din",
                                        layer="m2",
                                        offset=din_in)

    def route_din_bar(self):

        # Left
        track_xoff = self.get_m4_track(self.din_bar_track)

        din_bar_in = self.din_inst.get_pin("Z").center()
        self.add_via_stack_center("m1", "m3", din_bar_in)
        din_bar_track = vector(track_xoff,din_bar_in.y)

        bl_in = self.bl_inst.get_pin("in").center()
        self.add_via_stack_center("m1", "m3", bl_in)
        bl_track = vector(track_xoff,bl_in.y)

        din_in = vector(track_xoff,0)

        self.add_wire(self.m3_stack, [din_bar_in, din_bar_track, bl_track, bl_in])

        self.add_layout_pin_rect_center(text="din",
                                        layer="m4",
                                        offset=din_in)


    def route_en_bar(self):
        # Enable in track
        track_xoff = self.get_m4_track(self.en_bar_track)

        # This M2 pitch is a hack since the A and Z pins align horizontally
        en_bar_loc = self.en_inst.get_pin("Z").uc()
        en_bar_track = vector(track_xoff, en_bar_loc.y)
        self.add_via_stack_center("m1", "m3", en_bar_loc)

        # This is a U route to the right down then left
        bl_en_loc = self.bl_inst.get_pin("en_bar").center()
        bl_en_track = vector(track_xoff, bl_en_loc.y)
        self.add_via_stack_center("m1", "m3", bl_en_loc)
        br_en_loc = self.br_inst.get_pin("en_bar").center()
        br_en_track = vector(track_xoff, bl_en_loc.y)
        self.add_via_stack_center("m1", "m3", br_en_loc)


        # L shape
        self.add_wire(self.m3_stack,
                      [en_bar_loc, en_bar_track, bl_en_track])
        # U shape
        self.add_wire(self.m3_stack,
                      [bl_en_loc, bl_en_track, br_en_track, br_en_loc])


    def route_en(self):

        # Enable in track
        track_xoff = self.get_m4_track(self.en_track)

        # The en pin will be over the vdd rail
        vdd_yloc = self.en_inst.get_pin("vdd").cy()
        self.add_layout_pin_segment_center(text="en",
                                           layer="m3",
                                           start=vector(0,vdd_yloc),
                                           end=vector(self.width,vdd_yloc))

        en_loc = self.en_inst.get_pin("A").center()
        en_rail = vector(en_loc.x, vdd_yloc)
        self.add_via_stack_center("m1", "m2", en_loc)
        self.add_path("m2", [en_loc, en_rail])
        self.add_via_stack_center("m2", "m3", en_rail)

        # Start point in the track on the pin rail
        en_track = vector(track_xoff, vdd_yloc)
        self.add_via_stack_center("m3", "m4", en_track)

        # This is a U route to the right down then left
        bl_en_loc = self.bl_inst.get_pin("en").center()
        bl_en_track = vector(track_xoff, bl_en_loc.y)
        self.add_via_stack_center("m1", "m3", bl_en_loc)
        br_en_loc = self.br_inst.get_pin("en").center()
        br_en_track = vector(track_xoff, bl_en_loc.y)
        self.add_via_stack_center("m1", "m3", br_en_loc)

        # U shape
        self.add_wire(self.m3_stack,
                      [en_track, bl_en_track, bl_en_loc, bl_en_track, br_en_track, br_en_loc])


    def get_m4_track(self,i):
        return 0.5*self.m4_space + i*(self.m4_width+self.m4_space)
    def get_m3_track(self,i):
        return 0.5*self.m3_space + i*(self.m3_width+self.m3_space)
    def get_m2_track(self,i):
        return 0.5*self.m2_space + i*(self.m2_width+self.m2_space)

    def route_wires(self):
        # M4 tracks
        self.din_bar_track = 2
        self.en_track = 0
        self.en_bar_track = 1

        self.route_bitlines()
        self.route_din()
        self.route_din_bar()
        self.route_en()
        self.route_en_bar()

    def route_supplies(self):
        for inst in [self.en_inst, self.din_inst, self.bl_inst, self.br_inst]:
            # Continous vdd rail along with label.
            vdd_pin=inst.get_pin("vdd")
            self.add_layout_pin(text="vdd",
                                layer="m1",
                                offset=vdd_pin.ll().scale(0,1),
                                width=self.width,
                                height=vdd_pin.height())

            # Continous gnd rail along with label.
            gnd_pin=inst.get_pin("gnd")
            self.add_layout_pin(text="gnd",
                                layer="m1",
                                offset=gnd_pin.ll().scale(0,1),
                                width=self.width,
                                height=vdd_pin.height())


    def get_w_en_cin(self):
        """Get the relative capacitance of a single input"""
        # This is approximated from SCMOS. It has roughly 5 3x transistor gates.
        return 5*3
