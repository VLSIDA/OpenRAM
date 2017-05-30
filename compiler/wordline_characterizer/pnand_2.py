import contact
import design
import debug
from tech import drc
from ptx import ptx
from vector import vector
from globals import OPTS
from nand_2 import nand_2

class pnand_2(design.design):
    """
    This module generates gds of a parametrically sized 2_input nand.
    This model use ptx to generate a 2_input nand within a cetrain height.
    The 2_input nand's cell_height should be the same as the 6t library cell
    This module doesn't generate multi_finger 2_input nand gate, 
    It generate only the minimum size 2_input nand gate.
    Creates a pcell for a simple 2_input nand
    """

    c = reload(__import__(OPTS.config.bitcell))
    bitcell = getattr(c, OPTS.config.bitcell)

    def __init__(self, name, nmos_width=1, height=bitcell.chars["height"]):
        """ Constructor """
        design.design.__init__(self, name)
        debug.info(2, "create nand_2 strcuture {0} with size of {1}".format(
            name, nmos_width))

        self.nmos_width = nmos_width

        self.mults = int(self.nmos_width/(2.0*drc["minwidth_tx"])) 
        self.height = height

        self.add_pins()
        self.create_unit()
        self.add_nand()
        if self.mults >1:
            self.connect_A()
            self.connect_B()
            self.connect_Z()
        self.A_position = self.nand_2_sub.A_position
        self.B_position = self.nand_2_sub.B_position
        self.Z_position = vector((self.mults-1)* self.nand_2_sub.width,0) + self.nand_2_sub.Z_position
        self.vdd_position = self.nand_2_sub.vdd_position
        self.gnd_position = self.nand_2_sub.gnd_position
        self.width = self.mults * self.nand_2_sub.width
        self.height = self.nand_2_sub.height
        self.DRC_LVS()

    def add_pins(self):
        """ Add pins """
        self.add_pin_list(["A", "B", "Z", "vdd", "gnd"])

    def create_unit(self):
        self.nand_2_sub = nand_2(name="pnand2_sub",
                           nmos_width=2 *drc["minwidth_tx"])
        self.add_mod(self.nand_2_sub)

    def add_nand(self):
        for  i in range(self.mults):
            nand2_offset_i = vector(self.nand_2_sub.width*i,0)   
            self.add_inst(name=self.name+"sub"+str(i),
                          mod=self.nand_2_sub,
                          offset=nand2_offset_i)
            self.connect_inst(["A", "B", "Z", "vdd", "gnd"])

    def connect_A(self):
        for i in range(self.mults):
            offset = self.nand_2_sub.A_position + vector(i* self.nand_2_sub.width,0)
            self.add_contact(layers=("metal1", "via1", "metal2"),
                             offset=offset,
                             rotate = 90,
                             mirror = "MX")
        start = self.nand_2_sub.A_position
        end = start + vector((self.mults-1)* self.nand_2_sub.width,0)
        self.add_rect(layer="metal2",
                      offset = start,
                      width = (self.mults-1)* self.nand_2_sub.width,
                      height = drc["minwidth_metal2"])


    def connect_B(self):
        for i in range(self.mults):
            offset = self.nand_2_sub.B_position + vector(i* self.nand_2_sub.width,0)
            self.add_contact(layers=("metal1", "via1", "metal2"),
                             offset=offset,
                             rotate = 270,
                             mirror = "MY")
        start = self.nand_2_sub.B_position
        end = start + vector((self.mults-1)* self.nand_2_sub.width,0)
        self.add_rect(layer="metal2",
                      offset = start,
                      width = (self.mults-1)* self.nand_2_sub.width,
                      height = drc["minwidth_metal2"])


    def connect_Z(self):
        start = self.nand_2_sub.Z_position
        end = start + vector((self.mults-1)* self.nand_2_sub.width,0)
        self.add_rect(layer="metal1",
                      offset = start,
                      width = (self.mults-1)* self.nand_2_sub.width,
                      height = drc["minwidth_metal1"])
