import debug
import design
from tech import drc
from math import log
from vector import vector
from globals import OPTS
from pinv import pinv

class dff_buf(design.design):
    """
    This is a simple buffered DFF. The output is buffered
    with two inverters, of variable size, to provide q
    and qbar. This is to enable driving large fanout loads.
    """

    def __init__(self, inv1_size=2, inv2_size=4, name=""):

        if name=="":
            name = "dff_buf_{0}_{1}".format(inv1_size, inv2_size)
        design.design.__init__(self, name)
        debug.info(1, "Creating {}".format(self.name))

        from importlib import reload
        c = reload(__import__(OPTS.dff))
        self.mod_dff = getattr(c, OPTS.dff)
        self.dff = self.mod_dff("dff")
        self.add_mod(self.dff)

        self.inv1 = pinv(size=inv1_size,height=self.dff.height)
        self.add_mod(self.inv1)

        self.inv2 = pinv(size=inv2_size,height=self.dff.height)
        self.add_mod(self.inv2)

        self.width = self.dff.width + self.inv1.width + self.inv2.width
        self.height = self.dff.height

        self.create_layout()

    def create_layout(self):
        self.add_pins()
        self.add_insts()
        self.add_wires()
        self.add_layout_pins()
        self.DRC_LVS()
        
    def add_pins(self):
        self.add_pin("D")
        self.add_pin("Q")
        self.add_pin("Qb")
        self.add_pin("clk")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def add_insts(self):
        # Add the DFF
        self.dff_inst=self.add_inst(name="dff_buf_dff",
                                    mod=self.dff,
                                    offset=vector(0,0))
        self.connect_inst(["D", "qint", "clk", "vdd", "gnd"])

        # Add INV1 to the right
        self.inv1_inst=self.add_inst(name="dff_buf_inv1",
                                     mod=self.inv1,
                                     offset=vector(self.dff_inst.rx(),0))
        self.connect_inst(["qint", "Qb",  "vdd", "gnd"])
        
        # Add INV2 to the right
        self.inv2_inst=self.add_inst(name="dff_buf_inv2",
                                     mod=self.inv2,
                                     offset=vector(self.inv1_inst.rx(),0))
        self.connect_inst(["Qb", "Q",  "vdd", "gnd"])
        
    def add_wires(self):
        # Route dff q to inv1 a
        q_pin = self.dff_inst.get_pin("Q")
        a1_pin = self.inv1_inst.get_pin("A")
        mid_x_offset = 0.5*(a1_pin.cx() + q_pin.cx())
        mid1 = vector(mid_x_offset, q_pin.cy())
        mid2 = vector(mid_x_offset, a1_pin.cy())
        self.add_path("metal3",
                      [q_pin.center(), mid1, mid2, a1_pin.center()])
        self.add_via_center(layers=("metal2","via2","metal3"),
                            offset=q_pin.center())
        self.add_via_center(layers=("metal2","via2","metal3"),
                            offset=a1_pin.center())
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=a1_pin.center())

        # Route inv1 z to inv2 a
        z1_pin = self.inv1_inst.get_pin("Z")
        a2_pin = self.inv2_inst.get_pin("A")
        mid_point = vector(z1_pin.cx(), a2_pin.cy())        
        self.add_path("metal1", [z1_pin.center(), mid_point, a2_pin.center()])
        
    def add_layout_pins(self):

        # Continous vdd rail along with label.
        vdd_pin=self.dff_inst.get_pin("vdd")
        self.add_layout_pin(text="vdd",
                            layer="metal1",
                            offset=vdd_pin.ll(),
                            width=self.width,
                            height=vdd_pin.height())

        # Continous gnd rail along with label.
        gnd_pin=self.dff_inst.get_pin("gnd")
        self.add_layout_pin(text="gnd",
                            layer="metal1",
                            offset=gnd_pin.ll(),
                            width=self.width,
                            height=vdd_pin.height())
            
        clk_pin = self.dff_inst.get_pin("clk")
        self.add_layout_pin(text="clk",
                            layer=clk_pin.layer,
                            offset=clk_pin.ll(),
                            width=clk_pin.width(),
                            height=clk_pin.height())

        din_pin = self.dff_inst.get_pin("D")
        self.add_layout_pin(text="D",
                            layer=din_pin.layer,
                            offset=din_pin.ll(),
                            width=din_pin.width(),
                            height=din_pin.height())

        dout_pin = self.inv2_inst.get_pin("Z")
        self.add_layout_pin_rect_center(text="Q",
                                        layer="metal2",
                                        offset=dout_pin.center())
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=dout_pin.center())

        dout_pin = self.inv2_inst.get_pin("A")
        self.add_layout_pin_rect_center(text="Qb",
                                        layer="metal2",
                                        offset=dout_pin.center())
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=dout_pin.center())
        
        

    def analytical_delay(self, slew, load=0.0):
        """ Calculate the analytical delay of DFF-> INV -> INV """
        dff_delay=self.dff.analytical_delay(slew=slew, load=self.inv1.input_load())
        inv1_delay = self.inv1.analytical_delay(slew=dff_delay.slew, load=self.inv2.input_load()) 
        inv2_delay = self.inv2.analytical_delay(slew=inv1_delay.slew, load=load)
        return dff_delay + inv1_delay + inv2_delay
            
