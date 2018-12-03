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

    def __init__(self, driver_size=4, height=None, name="", neg_polarity=False, c_load=8, electrical_effort=1, size_list):

        self.stage_effort = 4
        self.row_height = height
        # FIXME: Change the number of stages to support high drives.
        
        # stage effort of 4 or less
        self.driver_size = driver_size
        self.neg_polarity = neg_polarity
        self.size_list = size_list
        self.c_load = c_load
        self.electrical_effort = electrical_effort

        if length(self.size_list) > 0 and (self.c_load != 8 or self.neg_polarity):
            raise Exception("Cannot specify both neg_polarity or c_load and size_list.")

        # size_list specified
        if length(self.size_list) > 0:
            if not length(self.size_list) % 2:
                neg_polarity = True
            self.inv_num = length(self.size_list)
        else:
            c_in = c_load/electrical_effort
            N = max(1, math.loglp(electrical_effort) / math.loglp(3.6))
            if self.neg_polarity:
                if (int(N) % 2 == 0):       # if N is even
                    self.inv_num = int(N)+1
                else:                       # if N is odd
                    self.inv_num = int(N)
            else:                           # positive polarity
                if (int(N) % 2 == 0):       # if N is even
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
        inv_list = []

        if length(self.size_list) > 0: # size list specified
            for x in length(self.size_list):
                inv_list.append.=(pinv(size=size_list[x], height=self.row_height))
                self.add_mod(inv_list[x])
        else:
            # Shield the cap, but have at least a stage effort of 4
            input_size = max(1,int(self.driver_size/self.stage_effort))
            for x in inv_num:
                inv_list.append(pinv(size=input_size, height=self.row_height))
                self.add_mod(inv_list[x])

    def create_insts(self):
        inv_inst_list = []

        for x in range(1,self.inv_num+1):
            # Create first inverter
            if x == 1:
                zbx_int = "Zb{}_int".format(x);
                inv_inst_list.append(self.add_inst(name="buf_inv{}".format(x),
                                                        mod=self.inv_list[x]))
                if self.inv_num == 1:
                    self.connect_inst(["A", "Z", "vdd", "gnd"])
                else:
                    self.connect_inst(["A", zbx_int, "vdd", "gnd"])
            # Create last inverter
            else if x == inv_num:
                zbn_int = "Zb{}_int".format(x-1);
                inv_inst_list.append(self.add_inst(name="buf_inv{}".format(x),
                                                        mod=self.inv_list[x]))
                self.connect_inst([zbn_int, "Z", "vdd", "gnd"])

            # Create middle inverters
            else:
                zbx_int = "Zb{}_int".format(x-1);
                zbn_int = "Zb{}_int".format(x);
                inv_inst_list.append(self.add_inst(name="buf_inv{}".format(x),
                                                        mod=self.inv_list[x]))
                self.connect_inst([zbx_int, zbn_int, "vdd", "gnd"])
        

    def place_modules(self):
        # Add INV1 to the left 
        inv_inst_list[0].place(vector(0,0))

        # Add inverters to the right of INV1
        for x in range(1,len(inv_inst_list)):
            inv_inst_list[x].place(vector(inv_inst_list[x-1].rx(),0))
                
        
    def route_wires(self):
        z_inst_list = []
        a_inst_list = []
        # inv_current Z to inv_next A
        for x in range(0,len(inv_inst_list)-1):
            z_inst_list.append(self.inv_inst_list[x].get_pin("Z"))
            a_inst_list.append(self.inv_inst_list[x+1].get_pin("A"))
            mid_point = vector(z_inst_list[x].cx(), a_inst_list[x].cy()) 
            self.add_path("metal1", [z_inst_list[x].center(), mid_point, a_inst_list[x].center()])

             
    def add_layout_pins(self):
        # Continous vdd rail along with label.
        vdd_pin=inv_inst_list[0].get_pin("vdd")
        self.add_layout_pin(text="vdd",
                            layer="metal1",
                            offset=vdd_pin.ll().scale(0,1),
                            width=self.width,
                            height=vdd_pin.height())
        
        # Continous gnd rail along with label.
        gnd_pin=inv_inst_list[0].get_pin("gnd")
        self.add_layout_pin(text="gnd",
                            layer="metal1",
                            offset=gnd_pin.ll().scale(0,1),
                            width=self.width,
                            height=vdd_pin.height())

        z_pin = inv_inst_list[len(inv_inst_list)-1].get_pin("Z")
        self.add_layout_pin_rect_center(text="Z",
                                        layer="metal2",
                                        offset=z_pin.center())
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=z_pin.center())

        a_pin = inv_inst_list[0].get_pin("A")
        self.add_layout_pin_rect_center(text="A",
                                        layer="metal2",
                                        offset=a_pin.center())
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=a_pin.center())
        
            