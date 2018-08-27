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
    from importlib import reload
    c = reload(__import__(OPTS.bitcell))
    bitcell = getattr(c, OPTS.bitcell)

    unique_id = 1

    def __init__(self, driver_size=4, height=bitcell.height, name=""):

        self.stage_effort = 4
        self.row_height = height
        # FIXME: Change the number of stages to support high drives.
        
        # stage effort of 4 or less
        # The pinvbuf has a FO of 2 for the first stage, so the second stage
        # should be sized "half" to prevent loading of the first stage
        self.driver_size = driver_size
        self.predriver_size = max(int(self.driver_size/(self.stage_effort/2)),1)
        if name=="":
            name = "pinvbuf_{0}_{1}_{2}".format(self.predriver_size, self.driver_size, pinvbuf.unique_id)
            pinvbuf.unique_id += 1

        design.design.__init__(self, name)
        debug.info(1, "Creating {}".format(self.name))

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()


    def create_netlist(self):
        self.add_pins()
        self.add_modules()
        self.create_insts()

    def create_layout(self):

        self.width = 2*self.inv1.width + self.inv2.width
        self.height = 2*self.inv1.height
        
        self.place_insts()
        self.route_wires()
        self.add_layout_pins()
        
        self.offset_all_coordinates()
        
        self.DRC_LVS()
        
    def add_pins(self):
        self.add_pin("A")
        self.add_pin("Zb")
        self.add_pin("Z")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def add_modules(self):
                
        # Shield the cap, but have at least a stage effort of 4
        input_size = max(1,int(self.predriver_size/self.stage_effort))
        self.inv = pinv(size=input_size, height=self.row_height)
        self.add_mod(self.inv)
        
        self.inv1 = pinv(size=self.predriver_size, height=self.row_height)
        self.add_mod(self.inv1)

        self.inv2 = pinv(size=self.driver_size, height=self.row_height)
        self.add_mod(self.inv2)

    def create_insts(self):
        # Create INV1 (capacitance shield)
        self.inv1_inst=self.add_inst(name="buf_inv1",
                                     mod=self.inv)
        self.connect_inst(["A", "zb_int",  "vdd", "gnd"])
        

        self.inv2_inst=self.add_inst(name="buf_inv2",
                                     mod=self.inv1)
        self.connect_inst(["zb_int", "z_int",  "vdd", "gnd"])
        
        self.inv3_inst=self.add_inst(name="buf_inv3",
                                     mod=self.inv2)
        self.connect_inst(["z_int", "Zb",  "vdd", "gnd"])

        self.inv4_inst=self.add_inst(name="buf_inv4",
                                     mod=self.inv2)
        self.connect_inst(["zb_int", "Z",  "vdd", "gnd"])

    def place_insts(self):
        # Add INV1 to the right (capacitance shield)
        self.place_inst(name="buf_inv1",
                        offset=vector(0,0))

        # Add INV2 to the right
        self.place_inst(name="buf_inv2",
                        offset=vector(self.inv1_inst.rx(),0))
        
        # Add INV3 to the right
        self.place_inst(name="buf_inv3",
                        offset=vector(self.inv2_inst.rx(),0))

        # Add INV4 to the bottom
        self.place_inst(name="buf_inv4",
                        offset=vector(self.inv2_inst.rx(),2*self.inv2.height),
                        mirror = "MX")
        
        
    def route_wires(self):
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
        self.add_layout_pin_rect_center(text="Z",
                                        layer="metal2",
                                        offset=z_pin.center())
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=z_pin.center())

        zb_pin = self.inv3_inst.get_pin("Z")
        self.add_layout_pin_rect_center(text="Zb",
                                        layer="metal2",
                                        offset=zb_pin.center())
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=zb_pin.center())
        

        a_pin = self.inv1_inst.get_pin("A")
        self.add_layout_pin_rect_center(text="A",
                                        layer="metal2",
                                        offset=a_pin.center())
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=a_pin.center())
        
        

    def analytical_delay(self, slew, load=0.0):
        """ Calculate the analytical delay of DFF-> INV -> INV """
        inv1_delay = self.inv1.analytical_delay(slew=slew, load=self.inv2.input_load()) 
        inv2_delay = self.inv2.analytical_delay(slew=inv1_delay.slew, load=load)
        return inv1_delay + inv2_delay
            
