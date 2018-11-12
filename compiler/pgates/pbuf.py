import debug
import design
from tech import drc
from math import log
from vector import vector
from globals import OPTS
from pinv import pinv

class pbuf(design.design):
    """
    This is a simple buffer used for driving loads. 
    """
    from importlib import reload
    c = reload(__import__(OPTS.bitcell))
    bitcell = getattr(c, OPTS.bitcell)

    unique_id = 1

    def __init__(self, driver_size=4, height=bitcell.height, name=""):

        stage_effort = 4
        # FIXME: Change the number of stages to support high drives.

        if name=="":
            name = "pbuf_{0}_{1}".format(driver_size, pbuf.unique_id)
            pbuf.unique_id += 1

        design.design.__init__(self, name)
        debug.info(1, "Creating {}".format(self.name))

        
        # Shield the cap, but have at least a stage effort of 4
        input_size = max(1,int(driver_size/stage_effort))
        self.inv1 = pinv(size=input_size, height=height) # 1 
        self.add_mod(self.inv)
        
        self.inv2 = pinv(size=driver_size, height=height) # 2
        self.add_mod(self.inv1)

        self.width = self.inv1.width + self.inv2.width
        self.height = self.inv1.height

        self.create_layout()

        #self.offset_all_coordinates()
        
        self.DRC_LVS()

    def create_layout(self):
        self.add_pins()
        self.add_insts()
        self.add_wires()
        self.add_layout_pins()
        
    def add_pins(self):
        self.add_pin("A")
        self.add_pin("Z")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def add_insts(self):
        # Add INV1 to the right 
        self.inv1_inst=self.add_inst(name="buf_inv1",
                                     mod=self.inv1,
                                     offset=vector(0,0))
        self.connect_inst(["A", "zb_int",  "vdd", "gnd"])
        

        # Add INV2 to the right
        self.inv2_inst=self.add_inst(name="buf_inv2",
                                     mod=self.inv2,
                                     offset=vector(self.inv1_inst.rx(),0))
        self.connect_inst(["zb_int", "Z",  "vdd", "gnd"])
        
        
    def add_wires(self):
        # inv1 Z to inv2 A
        z1_pin = self.inv1_inst.get_pin("Z")
        a2_pin = self.inv2_inst.get_pin("A")
        mid_point = vector(z1_pin.cx(), a2_pin.cy())        
        self.add_path("metal1", [z1_pin.center(), mid_point, a2_pin.center()])
        
        
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
            
        z_pin = self.inv2_inst.get_pin("Z")
        self.add_layout_pin_rect_center(text="Z",
                                        layer="metal2",
                                        offset=z_pin.center())
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=z_pin.center())

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
    
    