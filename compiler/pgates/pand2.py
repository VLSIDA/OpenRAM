import debug
import design
from tech import drc
from math import log
from vector import vector
from globals import OPTS
from pnand2 import pnand2
from pinv import pinv

class pand2(design.design):
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
            name = "pand2_{0}_{1}".format(driver_size, pand2.unique_id)
            pand2.unique_id += 1

        design.design.__init__(self, name)
        debug.info(1, "Creating {}".format(self.name))

        
        # Shield the cap, but have at least a stage effort of 4
        self.nand = pnand2(height=height) 
        self.add_mod(self.nand)
        
        self.inv = pinv(size=driver_size, height=height)
        self.add_mod(self.inv)

        self.width = self.nand.width + self.inv.width
        self.height = self.inv.height

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
        self.add_pin("B")
        self.add_pin("Z")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def add_insts(self):
        # Add NAND to the right 
        self.nand_inst=self.add_inst(name="pand2_nand",
                                     mod=self.nand,
                                     offset=vector(0,0))
        self.connect_inst(["A", "B", "zb_int",  "vdd", "gnd"])
        

        # Add INV to the right
        self.inv_inst=self.add_inst(name="pand2_inv",
                                    mod=self.inv,
                                    offset=vector(self.nand_inst.rx(),0))
        self.connect_inst(["zb_int", "Z",  "vdd", "gnd"])
        
        
    def add_wires(self):
        # nand Z to inv A
        z1_pin = self.nand_inst.get_pin("Z")
        a2_pin = self.inv_inst.get_pin("A")
        mid1_point = vector(0.5*(z1_pin.cx()+a2_pin.cx()), z1_pin.cy())
        mid2_point = vector(mid1_point, a2_pin.cy())
        self.add_path("metal1", [z1_pin.center(), mid1_point, mid2_point, a2_pin.center()])
        
        
    def add_layout_pins(self):
        # Continous vdd rail along with label.
        vdd_pin=self.inv_inst.get_pin("vdd")
        self.add_layout_pin(text="vdd",
                            layer="metal1",
                            offset=vdd_pin.ll().scale(0,1),
                            width=self.width,
                            height=vdd_pin.height())
        
        # Continous gnd rail along with label.
        gnd_pin=self.inv_inst.get_pin("gnd")
        self.add_layout_pin(text="gnd",
                            layer="metal1",
                            offset=gnd_pin.ll().scale(0,1),
                            width=self.width,
                            height=vdd_pin.height())
            
        z_pin = self.inv_inst.get_pin("Z")
        self.add_layout_pin_rect_center(text="Z",
                                        layer="metal2",
                                        offset=z_pin.center())
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=z_pin.center())

        for pin_name in ["A","B"]:
            pin = self.nand_inst.get_pin(pin_name)
            self.add_layout_pin_rect_center(text=pin_name,
                                            layer="metal2",
                                            offset=pin.center())
            self.add_via_center(layers=("metal1","via1","metal2"),
                                offset=pin.center())
        
        

    def analytical_delay(self, slew, load=0.0):
        """ Calculate the analytical delay of DFF-> INV -> INV """
        nand_delay = selfnand.analytical_delay(slew=slew, load=self.inv.input_load()) 
        inv_delay = self.inv.analytical_delay(slew=nand_delay.slew, load=load)
        return nand_delay + inv_delay
    
    
