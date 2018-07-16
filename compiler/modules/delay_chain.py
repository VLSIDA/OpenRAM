import debug
import design
from tech import drc
from pinv import pinv
from contact import contact
from vector import vector
from globals import OPTS

class delay_chain(design.design):
    """
    Generate a delay chain with the given number of stages and fanout.
    This automatically adds an extra inverter with no load on the input.
    Input is a list contains the electrical effort of each stage.
    """

    def __init__(self, fanout_list, name="delay_chain"):
        """init function"""
        design.design.__init__(self, name)
        # FIXME: input should be logic effort value 
        # and there should be functions to get 
        # area efficient inverter stage list 

        for f in fanout_list:
            debug.check(f>0,"Must have non-zero fanouts for each stage.")

        # number of inverters including any fanout loads.
        self.fanout_list = fanout_list
        self.num_inverters = 1 + sum(fanout_list)
        self.num_top_half = round(self.num_inverters / 2.0)
        
        from importlib import reload
        c = reload(__import__(OPTS.bitcell))
        self.mod_bitcell = getattr(c, OPTS.bitcell)
        self.bitcell = self.mod_bitcell()

        self.add_pins()
        self.create_module()
        self.route_inverters()
        self.add_layout_pins()
        self.DRC_LVS()

    def add_pins(self):
        """ Add the pins of the delay chain"""
        self.add_pin("in")
        self.add_pin("out")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def create_module(self):
        """ Add the inverter logical module """

        self.inv = pinv(route_output=False)
        self.add_mod(self.inv)

        # half chain length is the width of the layout 
        # invs are stacked into 2 levels so input/output are close
        # extra metal is for the gnd connection U
        self.height = len(self.fanout_list)*self.inv.height
        self.width = (max(self.fanout_list)+1) * self.inv.width

        self.add_inverters()
        

    def add_inverters(self):
        """ Add the inverters and connect them based on the stage list """
        self.driver_inst_list = []
        self.rightest_load_inst = {}
        self.load_inst_map = {}
        for stage_num,fanout_size in zip(range(len(self.fanout_list)),self.fanout_list):
            if stage_num % 2:
                inv_mirror = "MX"
                inv_offset = vector(0, (stage_num+1)* self.inv.height)
            else:
                inv_mirror = "R0"
                inv_offset = vector(0, stage_num * self.inv.height)                
                
            # Add the inverter
            cur_driver=self.add_inst(name="dinv{}".format(stage_num),
                                  mod=self.inv,
                                  offset=inv_offset,
                                  mirror=inv_mirror)
            # keep track of the inverter instances so we can use them to get the pins
            self.driver_inst_list.append(cur_driver)


            # Hook up the driver
            if stage_num+1==len(self.fanout_list):
                stageout_name = "out"
            else:
                stageout_name = "dout_{}".format(stage_num+1)
            if stage_num == 0:
                stagein_name = "in"
            else:
                stagein_name = "dout_{}".format(stage_num)  
            self.connect_inst([stagein_name, stageout_name, "vdd", "gnd"])
            
            # Now add the dummy loads to the right
            self.load_inst_map[cur_driver]=[]
            for i in range(fanout_size):
                inv_offset += vector(self.inv.width,0)
                cur_load=self.add_inst(name="dload_{0}_{1}".format(stage_num,i),
                                      mod=self.inv,
                                      offset=inv_offset,
                                      mirror=inv_mirror)
                # Fanout stage is always driven by driver and output is disconnected
                disconnect_name = "n_{0}_{1}".format(stage_num,i)  
                self.connect_inst([stageout_name, disconnect_name, "vdd", "gnd"])
            
                # Keep track of all the loads to connect their inputs as a load
                self.load_inst_map[cur_driver].append(cur_load)
            else:
                # Keep track of the last one so we can add the the wire later
                self.rightest_load_inst[cur_driver]=cur_load
                
    def add_route(self, pin1, pin2):
        """ This guarantees that we route from the top to bottom row correctly. """
        pin1_pos = pin1.center()
        pin2_pos = pin2.center()
        if pin1_pos.y == pin2_pos.y:
            self.add_path("metal2", [pin1_pos, pin2_pos])
        else:
            mid_point = vector(pin2_pos.x, 0.5*(pin1_pos.y+pin2_pos.y))
            # Written this way to guarantee it goes right first if we are switching rows
            self.add_path("metal2", [pin1_pos, vector(pin1_pos.x,mid_point.y), mid_point, vector(mid_point.x,pin2_pos.y), pin2_pos])
    
    def route_inverters(self):
        """ Add metal routing for each of the fanout stages """

        for i in range(len(self.driver_inst_list)):
            inv = self.driver_inst_list[i]
            for load in self.load_inst_map[inv]:
                # Drop a via on each A pin
                a_pin = load.get_pin("A")      
                self.add_via_center(layers=("metal1","via1","metal2"),
                                    offset=a_pin.center())
                self.add_via_center(layers=("metal2","via2","metal3"),
                                    offset=a_pin.center())

            # Route an M3 horizontal wire to the furthest
            z_pin = inv.get_pin("Z")
            a_pin = inv.get_pin("A")
            a_max = self.rightest_load_inst[inv].get_pin("A")
            self.add_via_center(layers=("metal1","via1","metal2"),
                                offset=a_pin.center())
            self.add_via_center(layers=("metal1","via1","metal2"),
                                offset=z_pin.center())
            self.add_via_center(layers=("metal2","via2","metal3"),
                                offset=z_pin.center())
            self.add_path("metal3",[z_pin.center(), a_max.center()])

            
            # Route Z to the A of the next stage
            if i+1 < len(self.driver_inst_list):
                z_pin = inv.get_pin("Z")
                next_inv = self.driver_inst_list[i+1]
                next_a_pin = next_inv.get_pin("A")
                y_mid = (z_pin.cy() + next_a_pin.cy())/2
                mid1_point = vector(z_pin.cx(), y_mid)
                mid2_point = vector(next_a_pin.cx(), y_mid)
                self.add_path("metal2",[z_pin.center(), mid1_point, mid2_point, next_a_pin.center()])  
            
                
    def add_layout_pins(self):
        """ Add vdd and gnd rails and the input/output. Connect the gnd rails internally on
        the top end with no input/output to obstruct. """

        for pin_name in ["vdd", "gnd"]:
            for driver in self.driver_inst_list:
                pin = driver.get_pin(pin_name)
                start = pin.lc()
                end = start + vector(self.width,0)
                self.add_power_pin(pin_name, start)
                self.add_power_pin(pin_name, end)
                self.add_rect(layer="metal1",
                              offset=pin.ll(),
                              width=self.width,
                              height=pin.height())

        # input is A pin of first inverter
        a_pin = self.driver_inst_list[0].get_pin("A")
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=a_pin.center())
        self.add_layout_pin(text="in",
                            layer="metal2",
                            offset=a_pin.ll().scale(1,0),
                            height=a_pin.cy())
        

        # output is A pin of last load inverter
        last_driver_inst = self.driver_inst_list[-1]
        a_pin = self.rightest_load_inst[last_driver_inst].get_pin("A")
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=a_pin.center())
        mid_point = vector(a_pin.cx()+3*self.m2_width,a_pin.cy())
        self.add_path("metal2",[a_pin.center(), mid_point, mid_point.scale(1,0)])
        self.add_layout_pin_segment_center(text="out",
                                           layer="metal2",
                                           start=mid_point,
                                           end=mid_point.scale(1,0))

            
