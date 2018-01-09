import design
import debug
from tech import drc, parameter, spice
from vector import vector
import contact
from math import ceil
from ptx import ptx
from globals import OPTS

class pbitcell(design.design):
    """
    This module implements a parametrically sized multi-port bitcell.
    """

    def __init__(self):
        name = "pbitcell"
        design.design.__init__(self, name)
        debug.info(2, "create a multi-port bitcell")   
        
        self.num_write = 2
        self.num_read = 2

        self.create_layout()
        self.DRC_LVS()
    
    def add_pins(self):
        self.add_pin("WROW")
        self.add_pin("WBL")
        self.add_pin("WBL_bar")
        for k in range(0,self.num_read):
            self.add_pin("RROW{}".format(k))
            self.add_pin("RBL{}".format(k))
            self.add_pin("RBL_bar{}".format(k))
        self.add_pin("vdd")
        self.add_pin("gnd")

    def create_layout(self):
        self.create_ptx()
        self.add_storage()
        self.add_rails()        
        self.add_write_transistors()
        self.add_read_transistors()
        self.extend_well()
        #self.add_fail()
    
    def create_ptx(self):
        """
        Create ptx all transistors. Also define measurements to be used throughout bitcell.
        """
        self.i_nmos = ptx(width=2.3*parameter["min_tx_size"],
                        tx_type="nmos",
                        connect_active=True,
                        connect_poly=True)
        self.add_mod(self.i_nmos)

        self.i_pmos = ptx(width=parameter["min_tx_size"],
                        tx_type="pmos",
                        connect_active=True,
                        connect_poly=True)
        self.add_mod(self.i_pmos)
        
        # create ptx for write transitors
        self.w_nmos = ptx(width=1.5*parameter["min_tx_size"],
                        tx_type="nmos",
                        connect_active=True,
                        connect_poly=True)
        self.add_mod(self.w_nmos)
        
        # create ptx for read transistors
        self.r_nmos = ptx(width=parameter["min_tx_size"],
                        tx_type="nmos",
                        connect_active=True,
                        connect_poly=True)
        self.add_mod(self.r_nmos)
        
        # determine metal contact extentions
        self.in_ex = 0.5*(self.i_nmos.active_contact.height - self.i_nmos.active_height)
        self.ip_ex = 0.5*(self.i_pmos.active_contact.height - self.i_pmos.active_height)
        self.w_ex = 0.5*(self.w_nmos.active_contact.height - self.w_nmos.active_height)
        self.r_ex = 0.5*(self.r_nmos.active_contact.height - self.r_nmos.active_height)     
        
        # determine global measurements
        spacer = 5*drc["minwidth_metal2"] + self.w_ex + self.r_ex
        
        self.w_tile_width = 3*parameter["min_tx_size"] + self.w_nmos.active_height
        self.r_tile_width = 3*parameter["min_tx_size"] + self.r_nmos.active_height
        self.inv_gap = 5*contact.poly.width
        self.leftmost_xpos = -(self.i_nmos.active_width + 1.5*parameter["min_tx_size"] + drc["well_enclosure_active"]) \
                             - self.num_write*(3*parameter["min_tx_size"] + self.w_nmos.active_height) \
                             - (self.num_read-1)*(3*parameter["min_tx_size"] + self.r_nmos.active_height) - spacer - self.r_nmos.active_height
        self.botmost_ypos = -2*drc["minwidth_metal1"] - self.num_write*2*drc["minwidth_metal2"] - self.num_read*2*drc["minwidth_metal2"]
        self.topmost_ypos = self.inv_gap + self.i_nmos.active_height + self.i_pmos.active_height + drc["poly_extend_active"] + 2*drc["minwidth_metal1"]
        self.cell_width = -2*self.leftmost_xpos
        self.cell_height = self.topmost_ypos - self.botmost_ypos        
 
 
    def add_rails(self):
        """
        Adds rails for vdd and gnd.      
        """
        self.gnd_position = vector(self.leftmost_xpos, -2*drc["minwidth_metal1"])
        self.gnd = self.add_layout_pin(text="gnd",
                                       layer="metal1",
                                       offset=self.gnd_position,
                                       width=self.cell_width,
                                       height=drc["minwidth_metal1"])
        
        self.vdd_position = vector(self.leftmost_xpos, self.i_pmosL.get_pin("S").uc().y + drc["minwidth_metal1"])
        self.vdd = self.add_layout_pin(text="vdd",
                                       layer="metal1",
                                       offset=self.vdd_position,
                                       width=self.cell_width,
                                       height=drc["minwidth_metal1"])
                                       
        # connect sources to rails
        # connect nmos to gnd
        i_nmosL_source = self.i_nmosL.get_pin("S").bc()        
        gnd_posL = vector(self.i_nmosL.get_pin("S").bc().x, self.gnd_position.y + drc["minwidth_metal1"])
        self.add_path("metal1", [i_nmosL_source, gnd_posL])
        
        i_nmosR_drain = self.i_nmosR.get_pin("D").bc()
        gnd_posR = vector(self.i_nmosR.get_pin("D").bc().x, self.gnd_position.y + drc["minwidth_metal1"])        
        self.add_path("metal1", [i_nmosR_drain, gnd_posR])
        
        # connect pmos to vdd
        i_pmosL_source = self.i_pmosL.get_pin("S").uc()
        vdd_posL = vector(self.i_nmosL.get_pin("S").uc().x, self.vdd_position.y)
        self.add_path("metal1", [i_pmosL_source, vdd_posL])
        
        i_pmosR_drain = self.i_pmosR.get_pin("D").uc()
        vdd_posR = vector(self.i_nmosR.get_pin("D").uc().x, self.vdd_position.y)
        self.add_path("metal1", [i_pmosR_drain, vdd_posR])

        
    def add_storage(self):
        """
        Creates the crossed coupled inverters that act as storage for the bitcell.
        """
        # calculate offsets 
        lit_xpos = -(self.i_nmos.active_width + 1.5*parameter["min_tx_size"])
        rit_xpos = 1.5*parameter["min_tx_size"]
        it_ypos = self.inv_gap + self.i_nmos.active_height
        
        
        # create active
        self.i_nmosL = self.add_inst(name="i_nmosL",
                                     mod=self.i_nmos,
                                     offset=[lit_xpos,0])
        self.connect_inst(["IR", "IL", "gnd", "gnd"])
        
        self.i_nmosR = self.add_inst(name="i_nmosR",
                                      mod=self.i_nmos,
                                      offset=[rit_xpos,0])
        self.connect_inst(["IL", "IR", "gnd", "gnd"])

        self.i_pmosL = self.add_inst(name="i_pmosL",
                                     mod=self.i_pmos,
                                     offset=[lit_xpos, it_ypos])
        self.connect_inst(["IL", "IR", "vdd", "vdd"])
        
        self.i_pmosR = self.add_inst(name="i_pmosR",
                                     mod=self.i_pmos,
                                     offset=[rit_xpos, it_ypos])
        self.connect_inst(["IL", "IR", "vdd", "vdd"])
        
        
        # connect poly for inverters
        i_nmosL_poly = self.i_nmosL.get_pin("G").uc()
        i_pmosL_poly = self.i_pmosL.get_pin("G").bc()
        self.add_path("poly", [i_nmosL_poly, i_pmosL_poly])
        
        i_nmosR_poly = self.i_nmosR.get_pin("G").uc()
        i_pmosR_poly = self.i_pmosR.get_pin("G").bc()
        self.add_path("poly", [i_nmosR_poly, i_pmosR_poly])
        
        
        # connect drains for inverters
        i_nmosL_drain = self.i_nmosL.get_pin("D").uc()
        i_pmosL_drain = self.i_pmosL.get_pin("D").bc()
        self.add_path("metal1", [i_nmosL_drain, i_pmosL_drain])
        
        i_nmosR_source = self.i_nmosR.get_pin("S").uc()
        i_pmosR_source = self.i_pmosR.get_pin("S").bc()
        self.add_path("metal1", [i_nmosR_source, i_pmosR_source])
        
        # add cross couple vias
        offset =  vector(self.i_nmosL.get_pin("D").ur().x + contact.poly.height, self.i_nmos.active_height + 0.6*self.inv_gap)
        self.icl = self.add_contact(layers=("poly", "contact", "metal1"),
                                           offset=offset,
                                           rotate=90)
                                
        offset =  vector(self.i_nmosR.get_pin("S").ul().x, self.i_nmos.active_height + 0.2*self.inv_gap)
        self.icr = self.add_contact(layers=("poly", "contact", "metal1"),
                                           offset=offset,
                                           rotate=90)
                                           
        
        # connect vias to poly (cross couple)
        correct = 0.5*(self.i_nmos.active_contact.width - drc["minwidth_metal1"])
        cross_width = 0.5*self.i_nmos.active_width - 0.5*drc["minwidth_poly"] + 3*parameter["min_tx_size"] + correct
        offset = vector(self.i_nmosL.get_pin("G").ur().x, self.i_nmos.active_height + 0.2*self.inv_gap)
        self.add_rect(layer="poly",
                      offset=offset,
                      width=cross_width,
                      height=contact.poly.width)
        
        offset = vector(self.i_nmosL.get_pin("D").ur().x, self.i_nmos.active_height + 0.6*self.inv_gap)
        self.add_rect(layer="poly",
                      offset=offset,
                      width=cross_width,
                      height=contact.poly.width)
                      
       
    def add_write_transistors(self):
        """
        Define variables relevant to write transistors
        """
        lit_xpos = -(self.i_nmos.active_width + 1.5*parameter["min_tx_size"])
        rit_xpos = 1.5*parameter["min_tx_size"]
        rot_correct = self.w_nmos.active_height
        
        self.w_nmosL = [None] * self.num_write 
        self.w_nmosR = [None] * self.num_write
        self.wrow_positions = [None] * self.num_write
        self.wbl_positions = [None] * self.num_write
        self.wbl_bar_positions = [None] * self.num_write
        
        for k in range(0,self.num_write):
            """
            Add transistors and WROW lines
            """
            wrow_ypos = -2*drc["minwidth_metal1"] - (k+1)*2*drc["minwidth_metal2"]   
            lwt_xpos = lit_xpos + rot_correct - (k+1)*self.w_tile_width
            rwt_xpos = rit_xpos + self.i_nmos.active_width + 3*parameter["min_tx_size"] + rot_correct + k*self.w_tile_width
            
            self.w_nmosL[k] = self.add_inst(name="w_nmosL{}".format(k),
                                            mod=self.w_nmos,
                                            offset=[lwt_xpos,0],
                                            rotate=90)
            self.connect_inst(["IR", "WROW{}".format(k), "WBL{}".format(k), "gnd"])
            
            self.w_nmosR[k] = self.add_inst(name="w_nmosR{}".format(k),
                                            mod=self.w_nmos,
                                            offset=[rwt_xpos,0],
                                            rotate=90)
            self.connect_inst(["IL", "WROW{}".format(k), "WBL_bar{}".format(k), "gnd"])
            
            
            # add WROW lines
            self.wrow_positions[k] = vector(self.leftmost_xpos, wrow_ypos)
            self.add_layout_pin(text="WROW{}".format(k),
                                layer="metal1",
                                offset=self.wrow_positions[k],
                                width=self.cell_width,
                                height=drc["minwidth_metal1"])
            
            """
            Source/WBL/WBL_bar connections
            """
            # connect sources to WBL and WBL_bar
            self.wbl_positions[k] = vector(lwt_xpos - drc["minwidth_metal2"],self.botmost_ypos)
            self.add_layout_pin(text="WBL{}".format(k),
                                layer="metal2",
                                offset=self.wbl_positions[k],
                                width=drc["minwidth_metal2"],
                                height=self.cell_height)

            self.wbl_bar_positions[k] = vector(rwt_xpos - rot_correct,self.botmost_ypos)
            self.add_layout_pin(text="WBL_bar{}".format(k),
                                layer="metal2",
                                offset=self.wbl_bar_positions[k],
                                width=drc["minwidth_metal2"],
                                height=self.cell_height)
            
            # add vias to connect source of wt to WBL and WBL_bar
            offset = self.w_nmosL[k].get_pin("S").ll() + vector(self.w_nmos.active_height, 0)
            self.add_contact(layers=("metal1", "via1", "metal2"),
                             offset=offset,
                             rotate=90)
            
            offset = self.w_nmosR[k].get_pin("S").ll() + vector(self.w_nmos.active_height, 0)
            self.add_contact(layers=("metal1", "via1", "metal2"),
                             offset=offset,
                             rotate=90)
            
            """
            Gate/WROW connections
            """
            # add vias to connect wt gate to WROW
            correct = vector(0.5*(drc["minwidth_metal2"] - drc["minwidth_metal1"]),0)
            offset = self.w_nmosL[k].get_pin("S").ll() - vector(drc["minwidth_metal2"] + contact.poly.width, 0)
            self.add_contact(layers=("poly", "contact", "metal1"),
                             offset=offset)
            
            self.add_contact(layers=("metal1", "via1", "metal2"),
                             offset=offset+correct)
            
            via_offsetL = offset + vector(0.5*contact.poly.width, 0)
            gate_offsetL = vector(offset.x + 0.5*contact.poly.width, self.w_nmosL[k].get_pin("G").ul().y)
            self.add_path("poly", [via_offsetL, gate_offsetL], width=contact.poly.width)
            self.add_path("poly", [gate_offsetL, self.w_nmosL[k].get_pin("G").lc()])
            
            offset = self.w_nmosR[k].get_pin("S").lr() + vector(drc["minwidth_metal2"], 0)
            self.add_contact(layers=("poly", "contact", "metal1"),
                             offset=offset)
            
            self.add_contact(layers=("metal1", "via1", "metal2"),
                             offset=offset+correct)
            
            via_offsetR = offset + vector(0.5*contact.poly.width, 0)
            gate_offsetR = vector(offset.x + 0.5*contact.poly.width, self.w_nmosR[k].get_pin("G").ur().y)
            self.add_path("poly", [via_offsetR, gate_offsetR], width=contact.poly.width)
            self.add_path("poly", [gate_offsetR, self.w_nmosR[k].get_pin("G").rc()])
            
            # add vias to WROW lines
            offset = vector(via_offsetL.x + contact.m1m2.height - 0.5*drc["minwidth_metal2"],self.wrow_positions[k].y)
            self.add_contact(layers=("metal1", "via1", "metal2"),
                             offset=offset,
                             rotate=90)
            
            wrow_offset = vector(via_offsetL.x, self.wrow_positions[k].y)
            self.add_path("metal2", [via_offsetL, wrow_offset])
                             
            offset = vector(via_offsetR.x + 0.5*drc["minwidth_metal2"], self.wrow_positions[k].y)
            self.add_contact(layers=("metal1", "via1", "metal2"),
                             offset=offset,
                             rotate=90)
            
            wrow_offset = vector(via_offsetR.x, self.wrow_positions[k].y)
            self.add_path("metal2", [via_offsetR, wrow_offset])
            
            
            """
            Drain/Storage connections
            """
            if(k == self.num_write-1):
                # add vias to connect input of inverters to drain of wt
                offset = vector(lit_xpos - drc["minwidth_metal1"], self.i_nmos.active_height + 0.2*self.inv_gap)
                self.add_contact(layers=("poly", "contact", "metal1"),
                                 offset=offset,
                                 rotate=90)
                
                offset = vector(rit_xpos + self.i_nmos.active_width + drc["minwidth_metal1"] + contact.poly.height, self.i_nmos.active_height + 0.2*self.inv_gap)
                self.add_contact(layers=("poly", "contact", "metal1"),
                                 offset=offset,
                                 rotate=90)
                                 
                # connect drains of wt to input of inverters
                correct = 0.5*(contact.poly.width - drc["minwidth_metal1"])
                w_nmosL_drain = self.w_nmosL[k].get_pin("D").rc()
                via_offsetLB = vector(lit_xpos - drc["minwidth_metal1"] - contact.poly.height, self.w_nmosL[k].get_pin("D").rc().y)
                via_offsetLT = vector(lit_xpos - drc["minwidth_metal1"] - contact.poly.height, self.i_nmos.active_height + 0.2*self.inv_gap + contact.poly.width - correct)
                self.add_path("metal1", [w_nmosL_drain, via_offsetLB, via_offsetLT])
                
                w_nmosR_drain = self.w_nmosR[k].get_pin("D").lc()
                via_offsetRB = vector(rit_xpos + self.i_nmos.active_width + drc["minwidth_metal1"] + contact.poly.height, self.w_nmosR[k].get_pin("D").lc().y)
                via_offsetRT = vector(rit_xpos + self.i_nmos.active_width + drc["minwidth_metal1"] + contact.poly.height, self.i_nmos.active_height + 0.2*self.inv_gap + contact.poly.width - correct)
                self.add_path("metal1", [w_nmosR_drain, via_offsetRB, via_offsetRT])
                
                via_offsetL = vector(lit_xpos - drc["minwidth_metal1"] - contact.poly.height, self.i_nmos.active_height + 0.2*self.inv_gap + 0.5*contact.poly.width)
                gate_offsetL = vector(self.i_nmosL.get_pin("G").ll().x, self.i_nmos.active_height + 0.2*self.inv_gap + 0.5*contact.poly.width)
                self.add_path("poly", [via_offsetL, gate_offsetL], width=contact.poly.width)
                
                via_offsetR = vector(rit_xpos + self.i_nmos.active_width + drc["minwidth_metal1"] + contact.poly.height, self.i_nmos.active_height + 0.2*self.inv_gap + 0.5*contact.poly.width)
                gate_offsetR = vector(self.i_nmosR.get_pin("G").lr().x, self.i_nmos.active_height + 0.2*self.inv_gap + 0.5*contact.poly.width)
                self.add_path("poly", [via_offsetR, gate_offsetR], width=contact.poly.width)

                
    def add_read_transistors(self):
        """
        Define variables relevant to read transistors
        """
        lit_xpos = -(self.i_nmos.active_width + 1.5*parameter["min_tx_size"])
        rit_xpos = 1.5*parameter["min_tx_size"]
        wrow_ypos = -2*drc["minwidth_metal1"] - self.num_write*2*drc["minwidth_metal2"]  
        lwt_xpos = lit_xpos - self.num_write*self.w_tile_width
        rwt_xpos = rit_xpos + self.i_nmos.active_width + self.num_write*self.w_tile_width
        
        rot_correct = self.r_nmos.active_height
        spacer = 5*drc["minwidth_metal2"]      
        
        self.r_nmosL = [None] * self.num_read 
        self.r_nmosR = [None] * self.num_read
        self.rrow_positions = [None] * self.num_read
        self.rbl_positions = [None] * self.num_read
        self.rbl_bar_positions = [None] * self.num_read
        
        
        for k in range(0,self.num_read):
            """
            Add transistors and RROW lines
            """
            lrt_xpos = lwt_xpos - spacer - self.r_nmos.active_height + rot_correct - k*self.r_tile_width
            rrt_xpos = rwt_xpos + spacer + rot_correct + k*self.r_tile_width            
            
            self.r_nmosL[k] = self.add_inst(name="r_nmosL",
                                            mod=self.r_nmos,
                                            offset=[lrt_xpos,0],
                                            rotate=90)
            self.connect_inst(["RROW{}".format(k), "IL", "RBL{}".format(k), "gnd"])
            
            self.r_nmosR[k] = self.add_inst(name="r_nmosR",
                                            mod=self.r_nmos,
                                            offset=[rrt_xpos,0],
                                            rotate=90)
            self.connect_inst(["RROW{}".format(k), "IR", "RBL_bar{}".format(k), "gnd"])
            
            
            # add RROW lines
            rrow_ypos = wrow_ypos - (k+1)*2*drc["minwidth_metal2"]
            self.rrow_positions[k] = vector(self.leftmost_xpos, rrow_ypos)
            self.add_layout_pin(text="RROW{}".format(k),
                                layer="metal1",
                                offset=self.rrow_positions[k],
                                width=self.cell_width,
                                height=drc["minwidth_metal1"])
                                
            """
            Drain/RBL/RBL_bar connections
            """
            # connect drains to RBL and RBL_bar
            self.rbl_positions[k] = vector(self.r_nmosL[k].get_pin("D").rc().x + drc["minwidth_metal2"],self.botmost_ypos)
            self.add_layout_pin(text="RBL{}".format(k),
                                layer="metal2",
                                offset=self.rbl_positions[k],
                                width=drc["minwidth_metal2"],
                                height=self.cell_height)

            self.rbl_bar_positions[k] = vector(self.r_nmosR[k].get_pin("D").lc().x - 2*drc["minwidth_metal2"],self.botmost_ypos)
            self.add_layout_pin(text="RBL_bar{}".format(k),
                                layer="metal2",
                                offset=self.rbl_bar_positions[k],
                                width=drc["minwidth_metal2"],
                                height=self.cell_height)
            
            # add vias to connect drain of rt to RBL and RBL_bar
            offset = self.r_nmosL[k].get_pin("D").ll() + vector(contact.m1m2.height, 0)
            self.add_contact(layers=("metal1", "via1", "metal2"),
                             offset=offset,
                             rotate=90)
            
            offset = self.r_nmosR[k].get_pin("D").ll() + vector(contact.m1m2.height, 0)
            self.add_contact(layers=("metal1", "via1", "metal2"),
                             offset=offset,
                             rotate=90)
                             
            # connect drain of rt to RBL and RBL_bar
            rbl_offset = vector(self.rbl_positions[k].x, self.r_nmosL[k].get_pin("D").lc().y)
            self.add_path("metal2", [self.r_nmosL[k].get_pin("D").lc(), rbl_offset])
            
            rbl_bar_offset = vector(self.rbl_bar_positions[k].x, self.r_nmosR[k].get_pin("D").rc().y)
            self.add_path("metal2", [self.r_nmosR[k].get_pin("D").rc(), rbl_bar_offset])

            """
            Source/RROW connections
            """
            # add vias on rt sources
            offset = self.r_nmosL[k].get_pin("S").ll() + vector(contact.m1m2.height, 0)
            self.add_contact(layers=("metal1", "via1", "metal2"),
                             offset=offset,
                             rotate=90)
            
            offset = self.r_nmosR[k].get_pin("S").ll() + vector(contact.m1m2.height, 0)
            self.add_contact(layers=("metal1", "via1", "metal2"),
                             offset=offset,
                             rotate=90)
            
            # add vias on rrows
            offset =  vector(self.r_nmosL[k].get_pin("S").ll().x + contact.m1m2.height, self.rrow_positions[k].y)
            self.add_contact(layers=("metal1", "via1", "metal2"),
                             offset=offset,
                             rotate=90)
            
            offset =  vector(self.r_nmosR[k].get_pin("S").ll().x + contact.m1m2.height, self.rrow_positions[k].y)
            self.add_contact(layers=("metal1", "via1", "metal2"),
                             offset=offset,
                             rotate=90)
            
            # connect sources of rt to rrows
            rrow_offset = vector(self.r_nmosL[k].get_pin("S").bc().x, self.rrow_positions[k].y)
            self.add_path("metal2", [self.r_nmosL[k].get_pin("S").bc(), rrow_offset])
            
            rrow_offset = vector(self.r_nmosR[k].get_pin("S").bc().x, self.rrow_positions[k].y)
            self.add_path("metal2", [self.r_nmosR[k].get_pin("S").bc(), rrow_offset])
            
            """
            Gate/inverter connections
            """
            # add vias to connect to gate of rt
            offsetL =  vector(self.r_nmosL[k].get_pin("D").lr().x + drc["minwidth_metal1"], self.r_nmosL[k].get_pin("G").lr().y)
            self.add_contact(layers=("poly", "contact", "metal1"),
                             offset=offsetL)
            
            offsetR =  vector(self.r_nmosR[k].get_pin("D").ll().x - drc["minwidth_metal1"] - contact.poly.width, self.r_nmosR[k].get_pin("G").ll().y)
            self.add_contact(layers=("poly", "contact", "metal1"),
                             offset=offsetR)
            
            # add metal1 path between gate vias and inverter inputs
            midL = vector(offsetL.x + 0.5*contact.poly.width, self.i_nmos.active_height + 0.6*self.inv_gap + 0.5*drc["minwidth_metal1"])
            gate_offsetL = vector(self.i_nmosL.get_pin("D").ll().x, self.i_nmos.active_height + 0.6*self.inv_gap + 0.5*drc["minwidth_metal1"])
            self.add_path("metal1", [offsetL+vector(0.5*contact.poly.width,0), midL, gate_offsetL])
            
            midR = vector(offsetR.x + 0.5*contact.poly.width, self.i_nmos.active_height + 0.6*self.inv_gap + 0.5*drc["minwidth_metal1"])
            gate_offsetR = vector(self.i_nmosR.get_pin("S").lr().x, self.i_nmos.active_height + 0.6*self.inv_gap + 0.5*drc["minwidth_metal1"])
            self.add_path("metal1", [offsetR+vector(0.5*contact.poly.width,0), midR, gate_offsetR])
            
            

    def extend_well(self):
        offset = vector(self.leftmost_xpos, -2*drc["minwidth_metal1"])
        well_height = self.w_nmos.well_width + 2*drc["minwidth_metal1"]
        self.add_rect(layer="pwell",
                      offset=offset,
                      width=self.cell_width,
                      height=well_height)
        
        lit_xpos = -(self.i_nmos.active_width + 1.5*parameter["min_tx_size"] + drc["well_enclosure_active"])
        it_ypos = self.inv_gap + self.i_nmos.active_height - drc["well_enclosure_active"]
        offset = [lit_xpos,it_ypos]
        well_width = 2*self.i_pmos.active_width + 3*parameter["min_tx_size"] + 2*drc["well_enclosure_active"]
        well_height = self.i_pmos.well_height + 2*drc["minwidth_metal1"]
        self.add_rect(layer="nwell",
                      offset=offset,
                      width=well_width,
                      height=well_height)
        
        
    
    def add_fail(self):
        # for failing drc
        frail_width = self.well_width = 10*drc["minwidth_tx"]
        frail_height = self.rail_height = drc["minwidth_metal1"]
        
        self.gnd_position = vector(-25*drc["minwidth_tx"], - 1.5 * drc["minwidth_metal1"] - 0.5 * frail_height)  # for tiling purposes
        self.add_layout_pin(text="gnd",
                            layer="metal1",
                            offset=self.gnd_position,
                            width=frail_width,
                            height=frail_height)

        self.gnd_position2 = vector(-25*drc["minwidth_tx"], - 0.5 * drc["minwidth_metal1"]) 
        self.add_layout_pin(text="gnd2",
                            layer="metal1",
                            offset=self.gnd_position2,
                            width=frail_width,
                            height=frail_height)
