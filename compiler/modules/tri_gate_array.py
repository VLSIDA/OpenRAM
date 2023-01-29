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
from openram.tech import drc
from openram import OPTS

class tri_gate_array(design):
    """
    Dynamically generated tri gate array of all bitlines.  words_per_row
    """

    def __init__(self, columns, word_size, name):
        """Intial function of tri gate array """
        super().__init__(name)
        debug.info(1, "Creating {0}".format(self.name))

        self.columns = columns
        self.word_size = word_size
        self.words_per_row = int(self.columns / self.word_size)

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_array()

    def create_layout(self):
        self.width = (self.columns / self.words_per_row) * self.tri.width
        self.height = self.tri.height

        self.place_array()
        self.add_layout_pins()
        self.add_boundary()
        self.DRC_LVS()

    def add_modules(self):
        self.tri = factory.create(module_type="tri_gate")

    def add_pins(self):
        """create the name of pins depend on the word size"""
        for i in range(self.word_size):
            self.add_pin("in_{0}".format(i))
        for i in range(self.word_size):
            self.add_pin("out_{0}".format(i))
        for pin in ["en", "en_bar", "vdd", "gnd"]:
            self.add_pin(pin)

    def create_array(self):
        """add tri gate to the array """
        self.tri_inst = {}
        for i in range(0,self.columns,self.words_per_row):
            name = "Xtri_gate{0}".format(i)
            self.tri_inst[i]=self.add_inst(name=name,
                                           mod=self.tri)
            index = int(i/self.words_per_row)
            self.connect_inst(["in_{0}".format(index),
                               "out_{0}".format(index),
                               "en", "en_bar", "vdd", "gnd"])

    def place_array(self):
        """ Place the tri gate to the array """
        for i in range(0,self.columns,self.words_per_row):
            base = vector(i*self.tri.width, 0)
            self.tri_inst[i].place(base)


    def add_layout_pins(self):

        for i in range(0,self.columns,self.words_per_row):
            index = int(i/self.words_per_row)

            in_pin = self.tri_inst[i].get_pin("in")
            self.add_layout_pin(text="in_{0}".format(index),
                                layer="m2",
                                offset=in_pin.ll(),
                                width=in_pin.width(),
                                height=in_pin.height())

            out_pin = self.tri_inst[i].get_pin("out")
            self.add_layout_pin(text="out_{0}".format(index),
                                layer="m2",
                                offset=out_pin.ll(),
                                width=out_pin.width(),
                                height=out_pin.height())


            # Route both supplies
            for n in ["vdd", "gnd"]:
                for supply_pin in self.tri_inst[i].get_pins(n):
                    pin_pos = supply_pin.center()
                    self.add_via_center(layers=self.m2_stack,
                                        offset=pin_pos)
                    self.add_layout_pin_rect_center(text=n,
                                                    layer="m3",
                                                    offset=pin_pos)


        width = self.tri.width * self.columns - (self.words_per_row - 1) * self.tri.width
        en_pin = self.tri_inst[0].get_pin("en")
        self.add_layout_pin(text="en",
                            layer="m1",
                            offset=en_pin.ll().scale(0, 1),
                            width=width,
                            height=drc("minwidth_m1"))

        enbar_pin = self.tri_inst[0].get_pin("en_bar")
        self.add_layout_pin(text="en_bar",
                            layer="m1",
                            offset=enbar_pin.ll().scale(0, 1),
                            width=width,
                            height=drc("minwidth_m1"))
