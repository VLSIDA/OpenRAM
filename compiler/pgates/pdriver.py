import debug
import design
import math
from tech import drc
from math import log
from vector import vector
from globals import OPTS
from pinv import pinv

class pdriver(design.design):
    """
    This instantiates an even or odd number of inverters sized for driving a load. 
    """
    unique_id = 1
    inv_list = []
    inv_inst_list = []

    def __init__(self, driver_size=4, height=None, name="", neg_polarity=False, c_load=8, size_list = []):

        self.stage_effort = 4
        self.row_height = height
        # FIXME: Change the number of stages to support high drives.
        
        # stage effort of 4 or less
        self.driver_size = driver_size
        self.neg_polarity = neg_polarity
        self.size_list = size_list
        self.c_load = c_load

        if len(self.size_list) > 0 and (self.c_load != 8 or self.neg_polarity):
            raise Exception("Cannot specify both size_list and neg_polarity or c_load.")

        # size_list specified
        if len(self.size_list) > 0:
            if not len(self.size_list) % 2:
                neg_polarity = True
            self.inv_num = len(self.size_list)
        else:
            # with pinv = i
            rho = 3.59
            N = max(1, int(math.log1p(self.stage_effort)/math.log1p(rho)))
            if self.neg_polarity:
                if (N % 2 == 0):            # if N is even
                    self.inv_num = int(N)+1
                else:                       # if N is odd
                    self.inv_num = int(N)
            else: # positive polarity
                if (N % 2 == 0):        
                    self.inv_num = int(N)
                else:
                    self.inv_num = int(N)+1

        if name=="":
            name = "pdriver_{0}_{1}_{2}".format(self.driver_size, self.inv_num, 
                                                pdriver.unique_id)
            pdriver.unique_id += 1

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

        self.width = self.inv_num * self.inv_list[0].width
        self.height = self.inv_list[0].height
        
        self.place_modules()
        self.route_wires()
        self.add_layout_pins()
                
        self.DRC_LVS()
        
    def add_pins(self):
        self.add_pin("A")
        self.add_pin("Z")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def add_modules(self):           
        if len(self.size_list) > 0: # size list specified
            for x in range(len(self.size_list)):
                self.inv_list.append(pinv(size=self.size_list[x], height=self.row_height))
                self.add_mod(self.inv_list[x])
        else: # find inv sizes
            # shield the cap, but have at least a stage effort of 4
            input_size = max(1,int(self.driver_size/self.stage_effort))
            self.inv_list.append(pinv(size=input_size, height=self.row_height))
            self.add_mod(self.inv_list[0])
            
            # work backwards
            for x in range(self.inv_num-1, 0, -1):
                c_in = max(input_size, int(round(self.c_load/self.stage_effort ,0)))
                self.c_load = c_in
                self.inv_list.append(pinv(size=c_in, height=self.row_height))
                self.add_mod(self.inv_list[x])

    def create_insts(self):
        for x in range(1,self.inv_num+1):
            # Create first inverter
            if x == 1:
                zbx_int = "Zb{}_int".format(x);
                self.inv_inst_list.append(self.add_inst(name="buf_inv{}".format(x),
                                                        mod=self.inv_list[x-1]))
                if self.inv_num == 1:
                    self.connect_inst(["A", "Z", "vdd", "gnd"])
                else:
                    self.connect_inst(["A", zbx_int, "vdd", "gnd"])
            # Create last inverter
            elif x == self.inv_num:
                zbn_int = "Zb{}_int".format(x-1);
                self.inv_inst_list.append(self.add_inst(name="buf_inv{}".format(x),
                                                        mod=self.inv_list[x-1]))
                self.connect_inst([zbn_int, "Z", "vdd", "gnd"])

            # Create middle inverters
            else:
                zbx_int = "Zb{}_int".format(x-1);
                zbn_int = "Zb{}_int".format(x);
                self.inv_inst_list.append(self.add_inst(name="buf_inv{}".format(x),
                                                        mod=self.inv_list[x-1]))
                self.connect_inst([zbx_int, zbn_int, "vdd", "gnd"])
        

    def place_modules(self):
        # Add INV1 to the left 
        self.inv_inst_list[0].place(vector(0,0))

        # Add inverters to the right of INV1
        for x in range(1,len(self.inv_inst_list)):
            self.inv_inst_list[x].place(vector(self.inv_inst_list[x-1].rx(),0))
                
        
    def route_wires(self):
        z_inst_list = []
        a_inst_list = []
        # inv_current Z to inv_next A
        for x in range(0,len(self.inv_inst_list)-1):
            z_inst_list.append(self.inv_inst_list[x].get_pin("Z"))
            a_inst_list.append(self.inv_inst_list[x+1].get_pin("A"))
            mid_point = vector(z_inst_list[x].cx(), a_inst_list[x].cy()) 
            self.add_path("metal1", [z_inst_list[x].center(), mid_point, a_inst_list[x].center()])

             
    def add_layout_pins(self):
        # Continous vdd rail along with label.
        vdd_pin=self.inv_inst_list[0].get_pin("vdd")
        self.add_layout_pin(text="vdd",
                            layer="metal1",
                            offset=vdd_pin.ll().scale(0,1),
                            width=self.width,
                            height=vdd_pin.height())
        
        # Continous gnd rail along with label.
        gnd_pin=self.inv_inst_list[0].get_pin("gnd")
        self.add_layout_pin(text="gnd",
                            layer="metal1",
                            offset=gnd_pin.ll().scale(0,1),
                            width=self.width,
                            height=vdd_pin.height())

        z_pin = self.inv_inst_list[len(self.inv_inst_list)-1].get_pin("Z")
        self.add_layout_pin_rect_center(text="Z",
                                        layer=z_pin.layer,
                                        offset=z_pin.center(),
                                        width = z_pin.width(),
                                        height = z_pin.height())

        a_pin = self.inv_inst_list[0].get_pin("A")
        self.add_layout_pin_rect_center(text="A",
                                        layer=a_pin.layer,
                                        offset=a_pin.center(),
                                        width = a_pin.width(),
                                        height = a_pin.height())
        
    def analytical_delay(self, slew, load=0.0):
        """Calculate the analytical delay of DFF -> INV -> ... -> INV"""
        delay = 0;
        if len(self.inv_inst_list) == 1:
            delay = self.inv_inst_list[x].analytical_delay(slew=slew);
        else:
            for x in range(len(self.inv_inst_list-1)):
                load_next = 0.0
                for n in range(x,len(self.inv_inst_list+1)):
                    load_next += self.inv_inst_list[x+1]
                if x == 1:
                    delay += self.inv_inst_list[x].analytical_delay(slew=slew, 
                                                                load=load_next)
                else:
                    delay += self.inv_inst_list[x+1].analytical_delay(slew=delay.slew, 
                                                                  load=load_next)
        return delay


