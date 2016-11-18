import debug
import design
from tech import drc
from pinv import pinv
from contact import contact
from vector import vector
from globals import OPTS

class logic_effort_dc(design.design):
    """
    Generate a logic effort based delay chain.
    Input is a list contains the electrical effort of each stage.
    """

    def __init__(self, name, stage_list):
        """init function"""
        design.design.__init__(self, "delay_chain")
        #fix me: input should be logic effort value 
        # and there should be functions to get 
        # area effecient inverter stage list 

        # chain_length is number of inverters in the load
        # plus 1 for the input
        chain_length = 1 + sum(stage_list)
        # half chain length is the width of the layeout 
        # invs are stacked into 2 levels so input/output are close
        half_length = round(chain_length / 2.0)

        c = reload(__import__(OPTS.config.bitcell))
        self.mod_bitcell = getattr(c, OPTS.config.bitcell)
        self.bitcell_height = self.mod_bitcell.chars["height"]

        self.add_pins()
        self.create_module()
        self.cal_cell_size(half_length)
        self.create_inv_stage_lst(stage_list)
        self.add_inv_lst(chain_length)
        self.route_inv(stage_list)
        self.add_vddgnd_label()
        self.DRC_LVS()

    def add_pins(self):
        """add the pins of the delay chain"""
        self.add_pin("clk_in")
        self.add_pin("clk_out")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def cal_cell_size(self, half_length):
        """ calculate the width and height of the cell"""
        self.width = half_length * self.inv.width
        self.height = 2 * self.bitcell_height

    def create_module(self):
        """add the inverters"""
        self.inv = pinv(name="delay_chain_inv",
                        nmos_width=drc["minwidth_tx"],
                        route_output=False)
        self.add_mod(self.inv)


    def create_inv_stage_lst(self, stage_list):
        """ Generate a list to indicate what stage each inv is in """
        self.inv_stage_lst = [[0, True]]
        stage_num = 0
        for stage in stage_list:
            stage_num = stage_num + 1
            repeat_times = stage
            for i in range(repeat_times):
                if i == repeat_times - 1:
                    # the first one need to connected to the next stage
                    self.inv_stage_lst.append([stage_num, True])
                else:
                    # the rest should not drive any thing
                    self.inv_stage_lst.append([stage_num, False])

    def add_inv_lst(self, chain_length):
        """add the inverter and connect them based on the stage list """
        half_length = round(chain_length / 2.0)
        self.inv_positions = []
        for i in range(chain_length):
            if i < half_length:
                # add top level
                inv_offset = [i * self.inv.width,
                              2 * self.inv.height]
                inv_mirror="MX"
                self.inv_positions.append(inv_offset)
                offset = inv_offset + \
                         self.inv.input_position.scale(1,-1)
                m1m2_via_rotate=270
                if i == 0:
                    self.clk_in_offset = offset
            else:
                # add bottom level
                inv_offset = [(chain_length - i) * self.inv.width,
                              0]
                inv_mirror="MY"
                self.inv_positions.append(inv_offset)
                offset = inv_offset + \
                         self.inv.input_position.scale(-1,1)
                m1m2_via_rotate=90
                if i == chain_length - 1:
                    self.clk_out_offset = inv_offset + \
                                          self.inv.output_position.scale(-1,1)
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=offset,
                         rotate=m1m2_via_rotate)
            self.add_inst(name="inv_chain%d" % i,
                          mod=self.inv,
                          offset=inv_offset,
                          mirror=inv_mirror)

            # connecting spice
            if i == 0:
                self.connect_inst(args=["clk_in", "s" + str(self.inv_stage_lst[i][0] + 1),
                                   "vdd", "gnd"],
                                  check=False)
                spare_node_counter = 1
            elif i == chain_length - 1:
                self.connect_inst(args=["s" + str(self.inv_stage_lst[i][0]), "clk_out", "vdd", "gnd"],
                                  check=False)
            else:
                if self.inv_stage_lst[i][1] == True:
                    self.connect_inst(args=["s" + str(self.inv_stage_lst[i][0]),
                                            "s" + str(self.inv_stage_lst[i][0] + 1), "vdd", "gnd"],
                                      check=False)
                    spare_node_counter = 1
                else:
                    self.connect_inst(args=["s" + str(self.inv_stage_lst[i][0]), "s" \
                                                + str(self.inv_stage_lst[i][0] + 1) + "n" \
                                                + str(spare_node_counter), "vdd", "gnd"],
                                      check=False)
                    spare_node_counter += 1

    def route_inv(self, stage_list):
        """add metal routing based on the stage list """
        half_length = round((sum(stage_list) + 1) / 2.0)
        start_inv = end_inv = 0
        for stage in stage_list:
            # end inv number depends on the fan out number
            end_inv = start_inv + stage
            start_inv_offset = self.inv_positions[start_inv]
            end_inv_offset = self.inv_positions[end_inv]

            if start_inv < half_length:
                start_o_offset =  start_inv_offset + \
                                  self.inv.output_position.scale(1,-1)
                m1m2_via_rotate =270
                m1m2_via_vc = vector(1,-.5)
            else:
                start_o_offset = start_inv_offset + \
                                 self.inv.output_position.scale(-1,1)
                m1m2_via_rotate =90
                m1m2_via_vc = vector(1,.5)
            M2_start = start_o_offset + vector(0,drc["minwidth_metal2"]).scale(m1m2_via_vc)
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=start_o_offset,
                         rotate=m1m2_via_rotate)

            if end_inv < half_length:
                end_i_offset =  end_inv_offset + \
                                self.inv.input_position.scale(1,-1)
                M2_end = end_i_offset - vector(0, 0.5 * drc["minwidth_metal2"])
            else:
                end_i_offset =  end_inv_offset + \
                                self.inv.input_position.scale(-1,1)
                M2_end = end_i_offset + vector(0, 0.5 * drc["minwidth_metal2"])

            if start_inv < half_length and end_inv >= half_length:
                mid = [half_length * self.inv.width \
                       - 0.5 * drc["minwidth_metal2"], M2_start[1]]
                self.add_wire(("metal2", "via2", "metal3"),
                              [M2_start, mid, M2_end])
            else:
                self.add_path(("metal2"), [M2_start, M2_end])
            # set the start of next one after current end
            start_inv = end_inv

    def add_vddgnd_label(self):
        """add vdd and gnd labels"""
        for i in range(3):
            if i % 2:
                self.add_label(text="vdd",
                               layer="metal1",
                               offset=[0, i * self.bitcell_height])
            else:
                self.add_label(text="gnd",
                               layer="metal1",
                               offset=[0, i * self.bitcell_height])
