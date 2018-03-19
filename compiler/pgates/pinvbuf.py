import debug
import design
from tech import drc
from math import log
from vector import vector
from globals import OPTS
from pinv import pinv

class pinvbuf(design.design):
    """
    This is a simple inverter/buffer used for driving loads. It is
    used in the column decoder for 1:2 decoding and as the clock buffer.
    """
    c = reload(__import__(OPTS.bitcell))
    bitcell = getattr(c, OPTS.bitcell)

    def __init__(self, inv1_size=2, inv2_size=4, height=bitcell.height, name=""):

        if name=="":
            name = "pinvbuf_{0}_{1}".format(inv1_size, inv2_size)
        design.design.__init__(self, name)
        debug.info(1, "Creating {}".format(self.name))

        self.inv = pinv(size=1, height=height)
        self.add_mod(self.inv)
        
        self.inv1 = pinv(size=inv1_size, height=height)
        self.add_mod(self.inv1)

        self.inv2 = pinv(size=inv2_size, height=height)
        self.add_mod(self.inv2)

        self.width = 2*self.inv1.width + self.inv2.width
        self.height = 2*self.inv1.height

        self.create_layout()

        self.offset_all_coordinates()
        
        self.DRC_LVS()

    def create_layout(self):
        self.add_pins()
        self.add_insts()
        self.add_wires()
        self.add_layout_pins()
        
    def add_pins(self):
        self.add_pin("A")
        self.add_pin("Zb")
        self.add_pin("Z")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def add_insts(self):
        # Add INV1 to the right (capacitance shield)
        self.inv1_inst=self.add_inst(name="buf_inv1",
                                     mod=self.inv,
                                     offset=vector(0,0))
        self.connect_inst(["A", "zb_int",  "vdd", "gnd"])
        

        # Add INV2 to the right
        self.inv2_inst=self.add_inst(name="buf_inv2",
                                     mod=self.inv1,
                                     offset=vector(self.inv1_inst.rx(),0))
        self.connect_inst(["zb_int", "z_int",  "vdd", "gnd"])
        
        # Add INV3 to the right
        self.inv3_inst=self.add_inst(name="buf_inv3",
                                     mod=self.inv2,
                                     offset=vector(self.inv2_inst.rx(),0))
        self.connect_inst(["z_int", "Zb",  "vdd", "gnd"])

        # Add INV4 to the bottom
        self.inv4_inst=self.add_inst(name="buf_inv4",
                                     mod=self.inv2,
                                     offset=vector(self.inv2_inst.rx(),2*self.inv2.height),
                                     mirror = "MX")
        self.connect_inst(["zb_int", "Z",  "vdd", "gnd"])
        
        
    def add_wires(self):
        # inv1 Z to inv2 A
        z1_pin = self.inv1_inst.get_pin("Z")
        a2_pin = self.inv2_inst.get_pin("A")
        mid_point = vector(z1_pin.cx(), a2_pin.cy())        
        self.add_path("metal1", [z1_pin.center(), mid_point, a2_pin.center()])
        
        # inv2 Z to inv3 A
        z2_pin = self.inv2_inst.get_pin("Z")
        a3_pin = self.inv3_inst.get_pin("A")
        mid_point = vector(z2_pin.cx(), a3_pin.cy())        
        self.add_path("metal1", [z2_pin.center(), mid_point, a3_pin.center()])

        # inv1 Z to inv4 A (up and over)
        z1_pin = self.inv1_inst.get_pin("Z")
        a4_pin = self.inv4_inst.get_pin("A")
        mid_point = vector(z1_pin.cx(), a4_pin.cy())        
        self.add_wire(("metal1","via1","metal2"), [z1_pin.center(), mid_point, a4_pin.center()])
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=z1_pin.center())
        

        
    def add_layout_pins(self):

        # Continous vdd rail along with label.
        vdd_pin=self.inv1_inst.get_pin("vdd")
        self.add_layout_pin(text="vdd",
                            layer="metal1",
                            offset=vdd_pin.ll().scale(0,1),
                            width=self.width,
                            height=vdd_pin.height())

        # Continous vdd rail along with label.
        gnd_pin=self.inv4_inst.get_pin("gnd")
        self.add_layout_pin(text="gnd",
                            layer="metal1",
                            offset=gnd_pin.ll().scale(0,1),
                            width=self.width,
                            height=gnd_pin.height())
        
        # Continous gnd rail along with label.
        gnd_pin=self.inv1_inst.get_pin("gnd")
        self.add_layout_pin(text="gnd",
                            layer="metal1",
                            offset=gnd_pin.ll().scale(0,1),
                            width=self.width,
                            height=vdd_pin.height())
            
        z_pin = self.inv4_inst.get_pin("Z")
        self.add_layout_pin_center_rect(text="Z",
                                        layer="metal2",
                                        offset=z_pin.center())
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=z_pin.center())

        zb_pin = self.inv3_inst.get_pin("Z")
        self.add_layout_pin_center_rect(text="Zb",
                                        layer="metal2",
                                        offset=zb_pin.center())
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=zb_pin.center())
        

        a_pin = self.inv1_inst.get_pin("A")
        self.add_layout_pin_center_rect(text="A",
                                        layer="metal2",
                                        offset=a_pin.center())
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=a_pin.center())
        
        

    def analytical_delay(self, slew, load=0.0):
        """ Calculate the analytical delay of DFF-> INV -> INV """
        inv1_delay = self.inv1.analytical_delay(slew=slew, load=self.inv2.input_load()) 
        inv2_delay = self.inv2.analytical_delay(slew=inv1_delay.slew, load=load)
        return inv1_delay + inv2_delay
            
