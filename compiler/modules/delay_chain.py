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
        
        c = reload(__import__(OPTS.bitcell))
        self.mod_bitcell = getattr(c, OPTS.bitcell)
        self.bitcell = self.mod_bitcell()

        self.add_pins()
        self.create_module()
        self.route_inv()
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

        self.create_inv_list()

        self.inv = pinv(route_output=False)
        self.add_mod(self.inv)

        # half chain length is the width of the layout 
        # invs are stacked into 2 levels so input/output are close
        # extra metal is for the gnd connection U
        self.width = self.num_top_half * self.inv.width + 2*drc["metal1_to_metal1"] + 0.5*drc["minwidth_metal1"]
        self.height = 2 * self.inv.height

        self.add_inv_list()
        
    def create_inv_list(self):
        """ 
        Generate a list of inverters. Each inverter has a stage
        number and a flag indicating if it is a dummy load. This is 
        the order that they will get placed too.
        """
        # First stage is always 0 and is not a dummy load
        self.inv_list=[[0,False]]
        for stage_num,fanout_size in zip(range(len(self.fanout_list)),self.fanout_list):
            for i in range(fanout_size-1):
                # Add the dummy loads
                self.inv_list.append([stage_num+1, True])
                
            # Add the gate to drive the next stage
            self.inv_list.append([stage_num+1, False])

    def add_inv_list(self):
        """ Add the inverters and connect them based on the stage list """
        dummy_load_counter = 1
        self.inv_inst_list = []
        for i in range(self.num_inverters):
            # First place the gates
            if i < self.num_top_half:
                # add top level that is upside down
                inv_offset = vector(i * self.inv.width, 2 * self.inv.height)
                inv_mirror="MX"
            else:
                # add bottom level from right to left
                inv_offset = vector((self.num_inverters - i) * self.inv.width, 0)
                inv_mirror="MY"

            cur_inv=self.add_inst(name="dinv{}".format(i),
                                  mod=self.inv,
                                  offset=inv_offset,
                                  mirror=inv_mirror)
            # keep track of the inverter instances so we can use them to get the pins
            self.inv_inst_list.append(cur_inv)

            # Second connect them logically
            cur_stage = self.inv_list[i][0]
            next_stage = self.inv_list[i][0]+1
            if i == 0:
                input = "in"
            else:
                input = "s{}".format(cur_stage)
            if i == self.num_inverters-1:
                output = "out"
            else:                
                output = "s{}".format(next_stage)

            # if the gate is a dummy load don't connect the output
            # else reset the counter
            if self.inv_list[i][1]: 
                output = output+"n{0}".format(dummy_load_counter)
                dummy_load_counter += 1
            else:
                dummy_load_counter = 1
                    
            self.connect_inst(args=[input, output, "vdd", "gnd"])

            if i != 0:
                self.add_via_center(layers=("metal1", "via1", "metal2"),
                                    offset=cur_inv.get_pin("A").center())
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
    
    def route_inv(self):
        """ Add metal routing for each of the fanout stages """
        start_inv = end_inv = 0
        for fanout in self.fanout_list:
            # end inv number depends on the fan out number
            end_inv = start_inv + fanout
            start_inv_inst = self.inv_inst_list[start_inv]
            
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=start_inv_inst.get_pin("Z").center()),

            # route from output to first load
            start_inv_pin = start_inv_inst.get_pin("Z")
            load_inst = self.inv_inst_list[start_inv+1]
            load_pin = load_inst.get_pin("A")
            self.add_route(start_inv_pin, load_pin)
            
            next_inv = start_inv+2
            while next_inv <= end_inv:
                prev_load_inst = self.inv_inst_list[next_inv-1]
                prev_load_pin = prev_load_inst.get_pin("A")
                load_inst = self.inv_inst_list[next_inv]
                load_pin = load_inst.get_pin("A")
                self.add_route(prev_load_pin, load_pin)
                next_inv += 1
            # set the start of next one after current end
            start_inv = end_inv

    def add_layout_pins(self):
        """ Add vdd and gnd rails and the input/output. Connect the gnd rails internally on
        the top end with no input/output to obstruct. """
        vdd_pin = self.inv.get_pin("vdd")
        gnd_pin = self.inv.get_pin("gnd")
        for i in range(3):
            (offset,y_dir)=self.get_gate_offset(0, self.inv.height, i)
            rail_width = self.num_top_half * self.inv.width
            if i % 2:
                self.add_layout_pin(text="vdd",
                                    layer="metal1",
                                    offset=offset + vdd_pin.ll().scale(1,y_dir),
                                    width=rail_width,
                                    height=drc["minwidth_metal1"])
            else:
                self.add_layout_pin(text="gnd",
                                    layer="metal1",
                                    offset=offset + gnd_pin.ll().scale(1,y_dir),
                                    width=rail_width,
                                    height=drc["minwidth_metal1"])

        # Use the right most parts of the gnd rails and add a U connector
        # We still have the two gnd pins, but it is an either-or connect
        gnd_pins = self.get_pins("gnd")
        gnd_start = gnd_pins[0].rc()
        gnd_mid1 = gnd_start + vector(2*drc["metal1_to_metal1"],0)
        gnd_end = gnd_pins[1].rc()
        gnd_mid2 = gnd_end + vector(2*drc["metal1_to_metal1"],0)
        #self.add_wire(("metal1","via1","metal2"), [gnd_start, gnd_mid1, gnd_mid2, gnd_end])
        self.add_path("metal1", [gnd_start, gnd_mid1, gnd_mid2, gnd_end])                
        
        # input is A pin of first inverter
        a_pin = self.inv_inst_list[0].get_pin("A")
        self.add_layout_pin(text="in",
                            layer="metal1",
                            offset=a_pin.ll(),
                            width=a_pin.width(),
                            height=a_pin.height())


        # output is Z pin of last inverter
        z_pin = self.inv_inst_list[-1].get_pin("Z")
        self.add_layout_pin(text="out",
                            layer="metal1",
                            offset=z_pin.ll().scale(0,1),
                            width=z_pin.lx())

            
