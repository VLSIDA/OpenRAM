import debug
import pgate
import math
from tech import drc
from math import log
from vector import vector
from globals import OPTS
from sram_factory import factory

class pdriver(pgate.pgate):
    """
    This instantiates an even or odd number of inverters sized for driving a load.
    """
    def __init__(self, name, neg_polarity=False, fanout=0, size_list=None, height=None):

        self.stage_effort = 3
        self.height = height 
        self.neg_polarity = neg_polarity
        self.size_list = size_list
        self.fanout = fanout

        if self.size_list and (self.fanout != 0 or self.neg_polarity):
            debug.error("Cannot specify both size_list and neg_polarity or fanout.", -1)
 
        pgate.pgate.__init__(self, name, height) 
        debug.info(1, "Creating {}".format(self.name))
        
        self.compute_sizes()

        self.add_comment("sizes: {}".format(str(self.size_list)))
        
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def compute_sizes(self):
        # size_list specified
        if self.size_list:
            if not len(self.size_list) % 2:
                neg_polarity = True
            self.num_inv = len(self.size_list)
        else:
            # find the number of stages
            #fanout is a unit inverter fanout, not a capacitance so c_in=1
            num_stages = max(1,int(round(log(self.fanout)/log(4))))

            # find inv_num and compute sizes
            if self.neg_polarity:
                if (num_stages % 2 == 0):   # if num_stages is even
                    self.diff_polarity(num_stages=num_stages)
                else:                       # if num_stages is odd
                    self.same_polarity(num_stages=num_stages)  
            else: # positive polarity
                if (num_stages % 2 == 0):        
                    self.same_polarity(num_stages=num_stages)
                else:
                    self.diff_polarity(num_stages=num_stages)


    def same_polarity(self, num_stages):
        self.size_list = []
        self.num_inv = num_stages
        # compute sizes
        fanout_prev = self.fanout
        for x in range(self.num_inv-1,-1,-1):
            fanout_prev = max(round(fanout_prev/self.stage_effort),1)
            self.size_list.append(fanout_prev)
        self.size_list.reverse()


    def diff_polarity(self, num_stages):
        self.size_list = []
        # find which delay is smaller
        if (num_stages > 1):
            delay_below = ((num_stages-1)*(self.fanout**(1/num_stages-1))) + num_stages-1
            delay_above = ((num_stages+1)*(self.fanout**(1/num_stages+1))) + num_stages+1
            if (delay_above < delay_below):
                # recompute stage_effort for this delay
                self.num_inv = num_stages+1
                polarity_stage_effort = self.fanout**(1/self.num_inv)
            else:
                self.num_inv = num_stages-1
                polarity_stage_effort = self.fanout**(1/self.num_inv)
        else: # num_stages is 1, can't go to 0
            self.num_inv = num_stages+1
            polarity_stage_effort = self.fanout**(1/self.num_inv)

        
        fanout_prev = self.fanout
        for x in range(self.num_inv-1,-1,-1):
            fanout_prev = round(fanout_prev/polarity_stage_effort)
            self.size_list.append(fanout_prev)
        self.size_list.reverse()

    def create_netlist(self):
        inv_list = []

        self.add_pins()
        self.add_modules()
        self.create_insts()

    def create_layout(self):
        self.place_modules()
        self.route_wires()
        self.add_layout_pins()

        self.width = self.inv_inst_list[-1].rx()
        self.height = self.inv_inst_list[0].height
        
        self.DRC_LVS()
        
    def add_pins(self):
        self.add_pin("A")
        self.add_pin("Z")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def add_modules(self):     
        self.inv_list = []
        for size in self.size_list:
            temp_inv = factory.create(module_type="pinv", size=size, height=self.height)
            self.inv_list.append(temp_inv)
            self.add_mod(temp_inv)
    
    
    def create_insts(self):
        self.inv_inst_list = []
        for x in range(1,self.num_inv+1):
            # Create first inverter
            if x == 1:
                zbx_int = "Zb{}_int".format(x);
                self.inv_inst_list.append(self.add_inst(name="buf_inv{}".format(x),
                                                        mod=self.inv_list[x-1]))
                if self.num_inv == 1:
                    self.connect_inst(["A", "Z", "vdd", "gnd"])
                else:
                    self.connect_inst(["A", zbx_int, "vdd", "gnd"])
            
            # Create last inverter
            elif x == self.num_inv:
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
        # Add the first inverter at the origin
        self.inv_inst_list[0].place(vector(0,0))

        # Add inverters to the right of the previous inverter
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
        """Calculate the analytical delay of INV1 -> ... -> INVn"""
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


    def get_stage_efforts(self, external_cout, inp_is_rise=False):
        """Get the stage efforts of the A -> Z path"""

        cout_list = {}
        for prev_inv,inv in zip(self.inv_list, self.inv_list[1:]):
            cout_list[prev_inv]=inv.get_cin()
            
        cout_list[self.inv_list[-1]]=external_cout
        
        stage_effort_list = []
        last_inp_is_rise = inp_is_rise
        for inv in self.inv_list:
            stage = inv.get_stage_effort(cout_list[inv], last_inp_is_rise)
            stage_effort_list.append(stage)
            last_inp_is_rise = stage.is_rise
            
        return stage_effort_list

    def get_cin(self):
        """Returns the relative capacitance of the input"""
        return self.inv_list[0].get_cin()
