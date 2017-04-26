import debug
import design
from tech import drc
from pinv import pinv
from contact import contact
from bitcell_array import bitcell_array
from nor_2 import nor_2
from ptx import ptx
from vector import vector
from globals import OPTS

class replica_bitline(design.design):
    """
    Generate a module that simulate the delay of control logic 
    and bit line charging.
    Used for memory timing control
    """

    def __init__(self, name, rows):
        design.design.__init__(self, "replica_bitline")

        g = reload(__import__(OPTS.config.delay_chain))
        self.mod_delay_chain = getattr(g, OPTS.config.delay_chain)

        g = reload(__import__(OPTS.config.replica_bitcell))
        self.mod_replica_bitcell = getattr(g, OPTS.config.replica_bitcell)

        c = reload(__import__(OPTS.config.bitcell))
        self.mod_bitcell = getattr(c, OPTS.config.bitcell)
        self.bitcell_chars = self.mod_bitcell.chars

        for pin in ["en", "out", "vdd", "gnd"]:
            self.add_pin(pin)
        self.rows = rows

        self.create_modules()
        self.cal_modules_offset()
        self.add_modules()
        self.route()
        self.offset_all_coordinates()

        self.DRC_LVS()

    def cal_modules_offset(self):
        pinv_error_offset = 0.025
        # leave some room for metal1 routing
        margin = 3 * drc["minwidth_metal1"]
        # witdth + min_spacing of M1 & M2  
        m1rail_space = drc["minwidth_metal1"] + drc["metal1_to_metal1"]
        m2rail_space = drc["minwidth_metal2"] + drc["metal2_to_metal2"]
        # leave some margin as bit cell layout exceeds its own orgin
        route_margin = 8 * m2rail_space
        well_margin = 2 * drc["pwell_enclose_nwell"]
        bitcell_array_spacing = max(route_margin, well_margin)
        # now extra space for BL and WL of RBC
        gnd_route_margin = 5 * m2rail_space

        y_off = (self.inv.height * 2 + pinv_error_offset
                     + max(drc["pwell_enclose_nwell"],
                           m1rail_space * 4))       
        self.delay_chain_offset = vector(self.delay_chain.height,y_off)
        self.en_input_offset = vector(0, y_off - m2rail_space)
        self.en_nor_offset = vector(self.nor.width + margin,
                                    self.inv.height * 2)
        self.BL_inv_offset = vector(self.en_nor_offset.x - self.inv.width, 0)
        self.access_tx_offset = vector(self.en_nor_offset.x - self.nor.width
                                           + self.access_tx.height + margin,
                                       self.inv.height * 0.5)
        self.replica_bitline_offset = vector(self.delay_chain_offset.x
                                                 + bitcell_array_spacing,
                                             self.bitcell_chars["height"] 
                                                 + gnd_route_margin)
        self.delay_inv_offset = vector(self.delay_chain_offset.x - self.inv.width,
                                       self.inv.height * 2)

        self.height = m1rail_space + max(self.delay_chain_offset.y + self.inv.height,
                                         self.replica_bitline_offset.y 
                                             + self.bitline_load.height 
                                             + 0.5 * self.bitcell_chars["height"]) 
        self.width = (self.replica_bitline_offset.x + self.replica_bitcell.width)


    def create_modules(self):
        """ create module """
        self.replica_bitcell = self.mod_replica_bitcell()
        self.add_mod(self.replica_bitcell)

        # This is the replica bitline load column that is the same height as our array
        self.bitline_load = bitcell_array(name="bitline_load",
                                          cols=1,
                                          rows=self.rows)
        self.add_mod(self.bitline_load)

        # FIXME: This just creates 3 1x inverters 
        self.delay_chain = self.mod_delay_chain("delay_chain",
                                                [1, 1, 1])
        self.add_mod(self.delay_chain)

        self.inv = pinv(name="RBL_inv",
                        nmos_width=drc["minwidth_tx"])
        self.add_mod(self.inv)

        # These aren't for instantiating, but we use them to get the dimensions
        self.poly_contact = contact(layer_stack=("poly", "contact", "metal1"))
        self.m1m2_via = contact(layer_stack=("metal1", "via1", "metal2"))
        self.m2m3_via = contact(layer_stack=("metal2", "via2", "metal3"))

        self.nor = nor_2(name="replica_bitline_nor2",
                         nmos_width=drc["minwidth_tx"])
        self.add_mod(self.nor)

        self.access_tx = ptx(width=drc["minwidth_tx"],
                             mults=1,
                             tx_type="pmos")
        self.add_mod(self.access_tx)

    def add_modules(self):
        """add mod instance in layout """
        self.add_inst(name="BL_inv",
                      mod=self.inv,
                      offset=self.BL_inv_offset)
        self.connect_inst(["bl[0]", "out", "vdd", "gnd"])

        self.add_inst(name="BL_access_tx",
                      mod=self.access_tx,
                      offset=self.access_tx_offset,
                      rotate=90)
        # D, G, S, B
        self.connect_inst(["vdd", "delayed_en", "bl[0]", "vdd"])

        self.add_inst(name="delay_chain",
                      mod=self.delay_chain,
                      offset=self.delay_chain_offset,
                      rotate=90)
        self.connect_inst(["en", "delayed_en", "vdd", "gnd"])

        self.add_inst(name="bitcell",
                      mod=self.replica_bitcell,
                      offset=self.replica_bitline_offset,
                      mirror="MX")
        self.connect_inst(["bl[0]", "br[0]", "delayed_en", "vdd", "gnd"])

        self.add_loads()
        self.expan_the_well_to_BL_inv()

    def expan_the_well_to_BL_inv(self):
        width = self.BL_inv_offset.x - self.access_tx_offset.x + self.inv.width
        well_offset = self.access_tx_offset - vector(self.access_tx.width, 0)
        for layer in ["nwell", "vtg"]:
            self.add_rect(layer=layer,
                          offset=well_offset,
                          width=width,
                          height= 2*self.access_tx.width)

    def add_loads(self):
        self.add_inst(name="load",
                      mod=self.bitline_load,
                      offset=self.replica_bitline_offset)
        temp = []
        for i in range(1):
            temp.append("bl[{0}]".format(i))
            temp.append("br[{0}]".format(i))
        for j in range(self.rows):
            temp.append("gnd".format(j))
        temp = temp + ["vdd", "gnd"]
        self.connect_inst(temp)

    def route(self):
        """connect modules together"""
        # calculate pin offset
        correct = vector(0, 0.5 * drc["minwidth_metal1"])
        self.out_offset = self.BL_inv_offset + self.inv.Z_position + correct
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=self.out_offset)
        m1_pin_offset = self.out_offset - correct
        self.add_rect(layer="metal1",
                      offset=m1_pin_offset,
                      width=self.m1m2_via.width,
                      height=self.m1m2_via.height)
        self.add_rect(layer="metal2",
                      offset=m1_pin_offset,
                      width=self.m2m3_via.width,
                      height=self.m2m3_via.height)

        BL_inv_in = self.BL_inv_offset + self.inv.A_position + correct
        BL_offset = self.replica_bitline_offset + vector(1,0).scale(self.bitcell_chars["BL"])
        pin_offset = self.delay_chain.clk_out_offset.rotate_scale(-1,1)
        delay_chain_output = self.delay_chain_offset + pin_offset
        vdd_offset = vector(self.delay_chain_offset.x + 9 * drc["minwidth_metal2"], 
                            self.height)
        self.create_input()

        self.route_BL_t_BL_inv(BL_offset, BL_inv_in)
        self.route_access_tx(delay_chain_output, BL_inv_in, vdd_offset)
        self.route_vdd()
        self.route_gnd()
        # route loads after gnd and vdd created
        self.route_loads(vdd_offset)
        self.route_RC(vdd_offset)

    def create_input(self):
        # create routing module based on module offset
        correct = vector(0.5 * drc["minwidth_metal1"], 0)
        pin_offset = self.delay_chain.clk_in_offset.rotate_scale(-1,1)
        input_offset = self.delay_chain_offset + pin_offset + correct
        mid1 = [input_offset.x, self.en_input_offset.y]
        self.add_path("metal1", [self.en_input_offset, mid1, input_offset])

        self.add_label(text="en",
                       layer="metal1",
                       offset=self.en_input_offset)

    def route_BL_t_BL_inv(self, BL_offset, BL_inv_in):
        # BL_inv input to M3
        mid1 = BL_inv_in - vector(0,  
                                  drc["metal2_to_metal2"] + self.m1m2_via.width)
        mid2 = vector(self.en_nor_offset.x + 3 * drc["metal1_to_metal1"],
                      mid1.y)
        mid3 = vector(mid2.x,
                      self.replica_bitline_offset.y - self.replica_bitcell.height
                          - 0.5 * (self.m1m2_via.height + drc["metal1_to_metal1"])
                          - 2 * drc["metal1_to_metal1"])
        self.add_wire(layers=("metal2", "via1", "metal1"),
                      coordinates=[BL_inv_in, mid1, mid2, mid3])

        # need to fix the mid point as this is done with two wire
        # this seems to cover the metal1 error of the wire
        offset = mid3 - vector( [0.5 * drc["minwidth_metal1"]] * 2)
        self.add_rect(layer="metal1",
                      offset=offset,
                      width=drc["minwidth_metal1"],
                      height=drc["minwidth_metal1"])

        mid4 = [BL_offset.x, mid3.y]
        self.add_wire(layers=("metal1", "via1", "metal2"),
                      coordinates=[BL_offset, mid4, mid3])

    def route_access_tx(self, delay_chain_output, BL_inv_in, vdd_offset):
        self.route_tx_gate(delay_chain_output)
        self.route_tx_drain(vdd_offset)
        self.route_tx_source(BL_inv_in)

    def route_tx_gate(self, delay_chain_output):
        # gate input for access tx
        offset = (self.access_tx.poly_positions[0].rotate_scale(0,1)
                      + self.access_tx_offset)
        width = -6 * drc["minwidth_metal1"]
        self.add_rect(layer="poly",
                      offset=offset,
                      width=width,
                      height=drc["minwidth_poly"])
        y_off = 0.5 * (drc["minwidth_poly"] - self.poly_contact.height)
        offset = offset + vector(width, y_off)
        self.add_contact(layers=("poly", "contact", "metal1"),
                         offset=offset)
        # route gate to delay_chain output
        gate_offset = offset + vector(0.5 * drc["minwidth_metal1"],
                                      0.5 * self.poly_contact.width)
        self.route_access_tx_t_delay_chain(gate_offset, delay_chain_output)
        self.route_access_tx_t_WL(gate_offset)

    def route_access_tx_t_delay_chain(self, offset, delay_chain_output):
        m2rail_space = (drc["minwidth_metal2"] + drc["metal2_to_metal2"]) 
        mid1 = vector(offset.x, self.delay_chain_offset.y - 3 * m2rail_space)
        mid2 = [delay_chain_output.x, mid1.y]
        # Note the inverted wire stack
        self.add_wire(layers=("metal1", "via1", "metal2"),
                      coordinates=[offset, mid1, mid2, delay_chain_output])
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=delay_chain_output,
                     mirror="MX")

    def route_access_tx_t_WL(self, offset):
        m1m2_via_offset = offset - vector(0.5 * self.m1m2_via.width,
                                          0.5 * self.m1m2_via.height)
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=m1m2_via_offset)
        # route gate to RC WL
        RC_WL = self.replica_bitline_offset - vector(0,1).scale(self.bitcell_chars["WL"])
        mid1 = vector(offset.x, 0)
        mid2 = vector(self.en_nor_offset.x + 3 * drc["metal1_to_metal1"], 
                      mid1.y)
        mid3 = vector(RC_WL.x - drc["minwidth_metal1"] - self.m1m2_via.height,
                      mid1.y)
        mid4 = vector(mid3.x, RC_WL.y)
        self.add_path("metal2", [offset, mid1, mid2, mid3, mid4])

        offset = mid4 - vector([0.5 * drc["minwidth_metal1"]] * 2)
        width = RC_WL.x - offset.x
        # enter the bit line array with metal1
        via_offset = [mid4.x - 0.5 * self.m1m2_via.width,
                      offset.y 
                          - 0.5 * (self.m1m2_via.height 
                                             - drc["minwidth_metal1"])]
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=via_offset)
        self.add_rect(layer="metal1",
                      offset=offset,
                      width=width,
                      height=drc["minwidth_metal1"])

    def route_tx_drain(self,vdd_offset):
        # route drain to Vdd
        active_offset = self.access_tx.active_contact_positions[1].rotate_scale(-1,1)
        correct = vector(-0.5 * drc["minwidth_metal1"], 
                         0.5 * self.access_tx.active_contact.width)
        drain_offset = self.access_tx_offset + active_offset + correct
        close_Vdd_offset = self.BL_inv_offset + vector(0, self.inv.height)
        self.add_path("metal1", [drain_offset, close_Vdd_offset])

        mid = [vdd_offset.x, close_Vdd_offset.y]
        self.add_wire(layers=("metal1", "via1", "metal2"),
                      coordinates=[close_Vdd_offset, mid, vdd_offset])

    def route_tx_source(self, BL_inv_in):
        # route source to BL inv input which is connected to BL
        active_offset = self.access_tx.active_contact_positions[0].rotate_scale(-1,1)
        correct = vector(-0.5 * drc["minwidth_metal1"], 
                         0.5 * self.access_tx.active_contact.width)
        source_offset = self.access_tx_offset + active_offset + correct
        self.add_path("metal1", [source_offset, BL_inv_in])

    def route_vdd(self):
        vdd_offset = vector(0, self.height)
        self.add_layout_pin(text="vdd",
                      layer="metal1",
                      offset=vdd_offset,
                      width=self.width,
                      height=drc["minwidth_metal1"])
        # delay chain vdd to vertical vdd  rail and
        start = self.delay_chain_offset - vector(0.5 * self.delay_chain.height, 0)
        m1rail_space = (drc["minwidth_metal1"] + drc["metal1_to_metal1"])
        mid1 = start - vector(0, m1rail_space)
        mid2 = vector(self.delay_chain_offset.x + 9 * drc["minwidth_metal2"],
                      mid1.y)
        end = [mid2.x, vdd_offset.y]
        self.add_path(layer=("metal1"), 
                      coordinates=[start, mid1, mid2])
        self.add_wire(layers=("metal1", "via1", "metal2"), 
                      coordinates=[mid1, mid2, end])

    def route_gnd(self):
        """route gnd of delay chain, en_nor, en_inv and BL_inv"""
        # route delay chain gnd to BL_inv gnd
        # gnd Node between BL_inv access tx and delay chain, and is below
        # en_input
        self.gnd_position = self.delay_chain_offset
        BL_gnd_offset = self.BL_inv_offset 
        mid1 = vector(0, self.BL_inv_offset.y)
        rail2_space = drc["minwidth_metal2"] + drc["metal2_to_metal2"]
        y_off = self.gnd_position.y + self.delay_chain.width + rail2_space
        mid2 = vector(mid1.x, y_off)
        share_gnd = vector(self.gnd_position.x, mid2.y)
        # Note the inverted stacks
        lst = [BL_gnd_offset, mid1, mid2, share_gnd, self.gnd_position]
        self.add_wire(layers=("metal1", "via1", "metal2"),
                      coordinates=lst)
        self.add_label(text="gnd",
                       layer="metal1",
                       offset=self.gnd_position)
        # connect to the metal1 gnd of delay chain
        offset = mid2 - vector(0.5 * drc["minwidth_metal1"], 0)
        self.add_rect(layer="metal1",
                      offset=offset,
                      width=drc["minwidth_metal1"],
                      height=-self.delay_chain.width)
        offset = [offset.x + self.delay_chain.height,
                  mid2.y]
        self.add_rect(layer="metal1",
                      offset=offset,
                      width=drc["minwidth_metal1"],
                      height=-self.delay_chain.width)

    def route_loads(self,vdd_offset):
        """connect all the loads word line to gnd"""
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=vdd_offset,
                     mirror="MX")
        gnd_offset = (self.delay_chain_offset 
                          + vector([drc["minwidth_metal1"]] * 2).scale(-.5,.5))
        for i in range(self.rows):
            WL_offset = (self.replica_bitline_offset                         
                             + self.bitline_load.WL_positions[i].scale(0,1))
            mid = [self.delay_chain_offset.x  + 6 * drc["minwidth_metal2"],
                   gnd_offset.y]
            self.add_wire(layers=("metal1", "via1", "metal2"), 
                          coordinates=[gnd_offset, mid, WL_offset])
            if i % 2 == 0:
                load_vdd_offset = (self.replica_bitline_offset
                                       + self.bitline_load.vdd_positions[i])
                mid = [vdd_offset.x, load_vdd_offset.y]
                self.add_wire(layers=("metal1", "via1", "metal2"), 
                              coordinates=[vdd_offset, mid, load_vdd_offset])

    def route_RC(self,vdd_offset):
        """route vdd gnd to the replica cell """
        # connect vdd
        RC_vdd = self.replica_bitline_offset + vector(1,-1).scale(self.bitcell_chars["vdd"])
        mid = [vdd_offset.x, RC_vdd.y]
        # Note the inverted stacks
        self.add_wire(layers=("metal1", "via1", "metal2"), 
                      coordinates=[vdd_offset, mid, RC_vdd])

        gnd_offset = self.BL_inv_offset - vector(self.inv.width, 0)
        load_gnd = self.replica_bitline_offset + vector(self.bitcell_chars["gnd"][0], 
                                                        self.bitline_load.height)
        mid = [load_gnd.x, gnd_offset.y]
        self.add_wire(layers=("metal1", "via1", "metal2"), 
                      coordinates=[gnd_offset, mid, load_gnd])

        load_gnd = self.replica_bitline_offset + vector(0, 
                                                        self.bitline_load.height)
        mid = [load_gnd.x, gnd_offset.y]
        self.add_wire(("metal1", "via1", "metal2"), [gnd_offset, mid, load_gnd])
