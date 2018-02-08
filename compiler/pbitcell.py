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
    This module implements a parametrically sized multi-port bitcell
    """

    def __init__(self, num_write=1, num_read=1):
        name = "pbitcell"
        design.design.__init__(self, name)
        debug.info(2, "create a multi-port bitcell with {0} write ports and {1} read ports".format(num_write, num_read))   
        
        self.num_write = num_write
        self.num_read = num_read

        self.create_layout()
        self.DRC_LVS()
    
    def add_pins(self):
        for k in range(0,self.num_write):
            self.add_pin("WROW{}".format(k))
        for k in range(0,self.num_write):
            self.add_pin("WBL{}".format(k))
            self.add_pin("WBL_bar{}".format(k))
        for k in range(0,self.num_read):
            self.add_pin("RROW{}".format(k))
        for k in range(0,self.num_read):
            self.add_pin("RBL{}".format(k))
            self.add_pin("RBL_bar{}".format(k))
        self.add_pin("vdd")
        self.add_pin("gnd")

    def create_layout(self):
        self.create_ptx()
        self.add_storage()
        self.add_rails()
        if(self.num_write > 0):
            self.add_write_transistors()
        if(self.num_read > 0):
            self.add_read_transistors()
        self.extend_well()
        #self.add_fail()
    
    def create_ptx(self):
        """ Create ptx for all transistors. Also define measurements to be used throughout bitcell """
        # create ptx for inverter transistors
        self.i_nmos = ptx(width=2*parameter["min_tx_size"],
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
        self.w_nmos = ptx(width=parameter["min_tx_size"],
                          tx_type="nmos",
                          connect_active=True,
                          connect_poly=True)
        self.add_mod(self.w_nmos)
        
        # create ptx for read transistors
        self.r_nmos = ptx(width=2*parameter["min_tx_size"],
                          mults=2,
                          tx_type="nmos",
                          connect_active=False,
                          connect_poly=False)
        self.add_mod(self.r_nmos)
        
        # determine metal contact extensions
        self.ip_ex = 0.5*(self.i_pmos.active_contact.height - self.i_pmos.active_height)
        self.w_ex = 0.5*(self.w_nmos.active_contact.height - self.w_nmos.active_height)    
        
        # determine global measurements
        w_spacer = drc["minwidth_metal2"] + self.w_ex + contact.poly.width + drc["poly_to_field_poly"] + drc["poly_extend_active"]
        r_spacer = 2*drc["minwidth_poly"] + drc["minwidth_metal1"] + 2*contact.poly.width
        rw_spacer = drc["minwidth_poly"] + drc["poly_to_field_poly"] + drc["minwidth_metal2"] + 2*contact.poly.width + self.w_ex
        
        self.w_tile_width = w_spacer + self.w_nmos.active_height
        self.r_tile_width = r_spacer + self.r_nmos.active_height
        self.inv_gap = drc["poly_to_active"] + drc["poly_to_field_poly"] + 2*contact.poly.width + drc["minwidth_metal1"] + self.ip_ex
        self.cross_heightL = self.i_nmos.active_height + drc["poly_to_active"] + 0.5*contact.poly.width
        self.cross_heightU = self.i_nmos.active_height + drc["poly_to_active"] + drc["poly_to_field_poly"] + 1.5*contact.poly.width
        
        self.leftmost_xpos = -(self.i_nmos.active_width + 1.5*parameter["min_tx_size"]) \
                             - self.num_write*(w_spacer + self.w_nmos.active_height) \
                             - rw_spacer - self.r_nmos.active_height - (self.num_read-1)*self.r_tile_width \
                             - 3*drc["minwidth_metal1"]
        self.botmost_ypos = -2*drc["minwidth_metal1"] - self.num_write*2*drc["minwidth_metal2"] - self.num_read*2*drc["minwidth_metal2"]
        self.topmost_ypos = self.inv_gap + self.i_nmos.active_height + self.i_pmos.active_height + drc["poly_extend_active"] + 2*drc["minwidth_metal1"]
        self.cell_width = -2*self.leftmost_xpos
        self.cell_height = self.topmost_ypos - self.botmost_ypos        

        
    def add_storage(self):
        """
        Creates the crossed coupled inverters that act as storage for the bitcell.
        """
        lit_xpos = -(self.i_nmos.active_width + 1.5*parameter["min_tx_size"])
        rit_xpos = 1.5*parameter["min_tx_size"]
        it_ypos = self.inv_gap + self.i_nmos.active_height
                
        # create active
        self.i_nmosL = self.add_inst(name="i_nmosL",
                                     mod=self.i_nmos,
                                     offset=[lit_xpos,0])
        self.connect_inst(["Q_bar", "Q", "gnd", "gnd"])
        
        self.i_nmosR = self.add_inst(name="i_nmosR",
                                      mod=self.i_nmos,
                                      offset=[rit_xpos,0])
        self.connect_inst(["gnd", "Q_bar", "Q", "gnd"])

        self.i_pmosL = self.add_inst(name="i_pmosL",
                                     mod=self.i_pmos,
                                     offset=[lit_xpos, it_ypos])
        self.connect_inst(["Q_bar", "Q", "vdd", "vdd"])
        
        self.i_pmosR = self.add_inst(name="i_pmosR",
                                     mod=self.i_pmos,
                                     offset=[rit_xpos, it_ypos])
        self.connect_inst(["vdd", "Q_bar", "Q", "vdd"])
        
        # connect poly for inverters
        self.add_path("poly", [self.i_nmosL.get_pin("G").uc(), self.i_pmosL.get_pin("G").bc()])
        self.add_path("poly", [self.i_nmosR.get_pin("G").uc(), self.i_pmosR.get_pin("G").bc()]) 
        
        # connect drains for inverters
        self.add_path("metal1", [self.i_nmosL.get_pin("D").uc(), self.i_pmosL.get_pin("D").bc()])
        self.add_path("metal1", [self.i_nmosR.get_pin("S").uc(), self.i_pmosR.get_pin("S").bc()])
        
        # add contacts to connect gate poly to drain/source metal1 (to connect Q to Q_bar)
        offsetL =  vector(self.i_nmosL.get_pin("G").rc().x + drc["poly_to_field_poly"] + 0.5*contact.poly.width, self.cross_heightU)
        self.add_contact_center(layers=("poly", "contact", "metal1"),
                                        offset=offsetL,
                                        rotate=90)
                                
        offsetR =  vector(self.i_nmosR.get_pin("G").lc().x - drc["poly_to_field_poly"] - 0.5*contact.poly.width, self.cross_heightL)
        self.add_contact_center(layers=("poly", "contact", "metal1"),
                                        offset=offsetR,
                                        rotate=90)
                                           
        # connect contacts to gate poly (cross couple)
        gate_offsetR = vector(self.i_nmosR.get_pin("G").lc().x, offsetL.y)
        self.add_path("poly", [offsetL, gate_offsetR])
        
        gate_offsetL = vector(self.i_nmosL.get_pin("G").rc().x, offsetR.y)
        self.add_path("poly", [offsetR, gate_offsetL])
                      
       
    def add_rails(self):
        """ Add rails for vdd and gnd """
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
        
        """ Connect inverters to rails """
        # connect nmos to gnd        
        gnd_posL = vector(self.i_nmosL.get_pin("S").bc().x, self.gnd_position.y + drc["minwidth_metal1"])
        self.add_path("metal1", [self.i_nmosL.get_pin("S").bc(), gnd_posL])
        
        gnd_posR = vector(self.i_nmosR.get_pin("D").bc().x, self.gnd_position.y + drc["minwidth_metal1"])        
        self.add_path("metal1", [self.i_nmosR.get_pin("D").bc(), gnd_posR])
        
        # connect pmos to vdd
        vdd_posL = vector(self.i_nmosL.get_pin("S").uc().x, self.vdd_position.y)
        self.add_path("metal1", [self.i_pmosL.get_pin("S").uc(), vdd_posL])
        
        vdd_posR = vector(self.i_nmosR.get_pin("D").uc().x, self.vdd_position.y)
        self.add_path("metal1", [self.i_pmosR.get_pin("D").uc(), vdd_posR])


    def add_write_transistors(self):
        """ Define variables relevant to write transistors """
        lit_xpos = -(self.i_nmos.active_width + 1.5*parameter["min_tx_size"])
        rit_xpos = 1.5*parameter["min_tx_size"] + self.i_nmos.active_width
        rot_correct = self.w_nmos.active_height
        
        self.w_nmosL = [None] * self.num_write 
        self.w_nmosR = [None] * self.num_write
        self.wrow_positions = [None] * self.num_write
        self.wbl_positions = [None] * self.num_write
        self.wbl_bar_positions = [None] * self.num_write
        
        
        for k in range(0,self.num_write):
            """ Add transistors and WROW lines """
            # calculate transistor offsets
            w_spacer = drc["minwidth_metal2"] + self.w_ex + contact.poly.width + drc["poly_to_field_poly"] + drc["poly_extend_active"]
            wrow_ypos = self.gnd_position.y - (k+1)*2*drc["minwidth_metal2"]   
            lwt_xpos = lit_xpos - (k+1)*self.w_tile_width  + rot_correct
            rwt_xpos = rit_xpos + w_spacer + k*self.w_tile_width + rot_correct
            
            # add write transistors
            self.w_nmosL[k] = self.add_inst(name="w_nmosL{}".format(k),
                                            mod=self.w_nmos,
                                            offset=[lwt_xpos,0],
                                            rotate=90)
            self.connect_inst(["Q", "WROW{}".format(k), "WBL{}".format(k), "gnd"])
            
            self.w_nmosR[k] = self.add_inst(name="w_nmosR{}".format(k),
                                            mod=self.w_nmos,
                                            offset=[rwt_xpos,0],
                                            rotate=90)
            self.connect_inst(["Q_bar", "WROW{}".format(k), "WBL_bar{}".format(k), "gnd"])
            
            # add WROW lines
            self.wrow_positions[k] = vector(self.leftmost_xpos, wrow_ypos)
            self.add_layout_pin(text="WROW{}".format(k),
                                layer="metal1",
                                offset=self.wrow_positions[k],
                                width=self.cell_width,
                                height=drc["minwidth_metal1"])
            
            
            """ Source/WBL/WBL_bar connections """            
            # add contacts to connect source of wt to WBL or WBL_bar
            offsetL = self.w_nmosL[k].get_pin("S").center()
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=offsetL,
                                    rotate=90)
            
            offsetR = self.w_nmosR[k].get_pin("S").center()
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=offsetR,
                                    rotate=90)
            
            # add WBL and WBL_bar (simultaneously connects to source of wt)
            self.wbl_positions[k] = vector(self.w_nmosL[k].get_pin("S").center().x - 0.5*drc["minwidth_metal2"], self.botmost_ypos)
            self.add_layout_pin(text="WBL{}".format(k),
                                layer="metal2",
                                offset=self.wbl_positions[k],
                                width=drc["minwidth_metal2"],
                                height=self.cell_height)

            self.wbl_bar_positions[k] = vector(self.w_nmosR[k].get_pin("S").center().x - 0.5*drc["minwidth_metal2"], self.botmost_ypos)
            self.add_layout_pin(text="WBL_bar{}".format(k),
                                layer="metal2",
                                offset=self.wbl_bar_positions[k],
                                width=drc["minwidth_metal2"],
                                height=self.cell_height)
            
            
            """ Gate/WROW connections """
            # add contacts to connect gate of wt to WROW (poly to metal2)
            offsetL =  vector(self.w_nmosL[k].get_pin("S").lc().x - drc["minwidth_metal2"] - 0.5*contact.m1m2.width, self.w_nmosL[k].get_pin("D").bc().y - drc["minwidth_metal1"] - 0.5*contact.m1m2.height)
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=offsetL)
            
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=offsetL)
            
            self.add_rect_center(layer="poly",
                                 offset=offsetL,
                                 width=contact.poly.width,
                                 height=contact.poly.height)
            
            offsetR = vector(self.w_nmosR[k].get_pin("S").rc().x + drc["minwidth_metal2"] + 0.5*contact.m1m2.width, self.w_nmosR[k].get_pin("D").bc().y - drc["minwidth_metal1"] - 0.5*contact.m1m2.height)
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=offsetR)
            
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=offsetR)
                            
            self.add_rect_center(layer="poly",
                                 offset=offsetR,
                                 width=contact.poly.width,
                                 height=contact.poly.height) 
            
            # connect gate of wt to contact
            midL = vector(offsetL.x, self.w_nmosL[k].get_pin("G").lc().y)
            self.add_path("poly", [self.w_nmosL[k].get_pin("G").lc(), midL, offsetL])
            
            midR = vector(offsetR.x, self.w_nmosR[k].get_pin("G").rc().y) 
            self.add_path("poly", [self.w_nmosR[k].get_pin("G").rc(), midR, offsetR])
            
            # add contacts to WROW lines
            offset = vector(offsetL.x, self.wrow_positions[k].y + 0.5*drc["minwidth_metal1"])
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                            offset=offset,
                                            rotate=90)
                             
            offset = vector(offsetR.x, self.wrow_positions[k].y + 0.5*drc["minwidth_metal1"])
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                            offset=offset,
                                            rotate=90)
            
            # connect wt gate contacts to WROW contacts
            wrow_offset = vector(offsetL.x, self.wrow_positions[k].y)
            self.add_path("metal2", [offsetL, wrow_offset])
            
            wrow_offset = vector(offsetR.x, self.wrow_positions[k].y)
            self.add_path("metal2", [offsetR, wrow_offset])
            
            
            """ Drain/Storage connections """
            if(k == self.num_write-1):
                # add contacts to connect gate of inverters to drain of wt
                offsetL =  vector(self.i_nmosL.get_pin("G").lc().x - drc["poly_to_field_poly"] - 0.5*contact.poly.width, self.cross_heightL)
                self.add_contact_center(layers=("poly", "contact", "metal1"),
                                                offset=offsetL,
                                                rotate=90)
                
                offsetR =  vector(self.i_nmosR.get_pin("G").rc().x + drc["poly_to_field_poly"] + 0.5*contact.poly.width, self.cross_heightL)
                self.add_contact_center(layers=("poly", "contact", "metal1"),
                                                offset=offsetR,
                                                rotate=90)
                                 
                # connect gate of inverters to contacts
                gate_offsetL = vector(self.i_nmosL.get_pin("G").lc().x, offsetL.y)
                self.add_path("poly", [offsetL, gate_offsetL])
                
                gate_offsetR = vector(self.i_nmosR.get_pin("G").rc().x, offsetR.y)
                self.add_path("poly", [offsetR, gate_offsetR])
                
                # connect contacts to drains of wt
                midL0 = vector(self.i_nmosL.get_pin("S").lc().x - 1.5*drc["minwidth_metal1"], offsetL.y)
                midL1 = vector(self.i_nmosL.get_pin("S").lc().x - 1.5*drc["minwidth_metal1"], self.w_nmosL[k].get_pin("D").lc().y)
                self.add_path("metal1", [offsetL, midL0, midL1, self.w_nmosL[k].get_pin("D").lc()])
                
                midR0 = vector(self.i_nmosR.get_pin("D").rc().x + 1.5*drc["minwidth_metal1"], offsetR.y)
                midR1 = vector(self.i_nmosR.get_pin("D").rc().x + 1.5*drc["minwidth_metal1"], self.w_nmosR[k].get_pin("D").rc().y)
                self.add_path("metal1", [offsetR, midR0, midR1, self.w_nmosR[k].get_pin("D").rc()])

                
    def add_read_transistors(self):
        """ Define variables relevant to read transistors """
        lit_xpos = -(self.i_nmos.active_width + 1.5*parameter["min_tx_size"])
        rit_xpos = 1.5*parameter["min_tx_size"] + self.i_nmos.active_width
        lwt_xpos = lit_xpos - self.num_write*self.w_tile_width
        rwt_xpos = rit_xpos + self.num_write*self.w_tile_width
        wrow_ypos = self.gnd_position.y - self.num_write*2*drc["minwidth_metal2"]  
        
        rot_correct = self.r_nmos.active_height
        r_spacer = 2*drc["minwidth_poly"] + drc["minwidth_metal1"] + 2*contact.poly.width
        rw_spacer = drc["minwidth_poly"] + drc["poly_to_field_poly"] + drc["minwidth_metal2"] + 2*contact.poly.width + self.w_ex     
        
        self.r_nmosL = [None] * self.num_read 
        self.r_nmosR = [None] * self.num_read
        self.rrow_positions = [None] * self.num_read
        self.rbl_positions = [None] * self.num_read
        self.rbl_bar_positions = [None] * self.num_read
        
        
        for k in range(0,self.num_read):
            """ Add transistors and RROW lines """
            # calculate transistor offsets
            lrt_xpos = lwt_xpos - rw_spacer - self.r_nmos.active_height - k*self.r_tile_width + rot_correct
            rrt_xpos = rwt_xpos + rw_spacer + k*self.r_tile_width + rot_correct          
            
            # add read transistors
            self.r_nmosL[k] = self.add_inst(name="r_nmosL",
                                            mod=self.r_nmos,
                                            offset=[lrt_xpos,0],
                                            rotate=90)
            self.connect_inst(["RROW{}".format(k), "Q", "RBL{}".format(k), "gnd"])
            
            self.r_nmosR[k] = self.add_inst(name="r_nmosR",
                                            mod=self.r_nmos,
                                            offset=[rrt_xpos,0],
                                            rotate=90)
            self.connect_inst(["RROW{}".format(k), "Q_bar", "RBL_bar{}".format(k), "gnd"])
            
            # add RROW lines
            rrow_ypos = wrow_ypos - (k+1)*2*drc["minwidth_metal2"]
            self.rrow_positions[k] = vector(self.leftmost_xpos, rrow_ypos)
            self.add_layout_pin(text="RROW{}".format(k),
                                layer="metal1",
                                offset=self.rrow_positions[k],
                                width=self.cell_width,
                                height=drc["minwidth_metal1"])
            
            
            """ Source of RA transistor / GND connection """
            offset = vector(self.r_nmosL[k].get_pins("S")[0].bc().x, self.gnd_position.y)
            self.add_path("metal1", [self.r_nmosL[k].get_pins("S")[0].bc(), offset])
            
            offset = vector(self.r_nmosR[k].get_pins("S")[0].bc().x, self.gnd_position.y)
            self.add_path("metal1", [self.r_nmosR[k].get_pins("S")[0].bc(), offset])
            
            
            """ Source of R transistor / RBL & RBL_bar connection """
            # add contacts to connect source of rt to RBL or RBL_bar
            offsetL = self.r_nmosL[k].get_pins("S")[1].center()
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=offsetL,
                                    rotate=90)
            
            offsetR = self.r_nmosR[k].get_pins("S")[1].center()
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=offsetR,
                                    rotate=90)
            
            # add RBL and RBL_bar (simultaneously connects to source of rt)
            self.rbl_positions[k] = vector(self.r_nmosL[k].get_pins("S")[1].center().x - 0.5*drc["minwidth_metal2"], self.botmost_ypos)
            self.add_layout_pin(text="RBL{}".format(k),
                                layer="metal2",
                                offset=self.rbl_positions[k],
                                width=drc["minwidth_metal2"],
                                height=self.cell_height)

            self.rbl_bar_positions[k] = vector(self.r_nmosR[k].get_pins("S")[1].center().x - 0.5*drc["minwidth_metal2"], self.botmost_ypos)
            self.add_layout_pin(text="RBL_bar{}".format(k),
                                layer="metal2",
                                offset=self.rbl_bar_positions[k],
                                width=drc["minwidth_metal2"],
                                height=self.cell_height)
            
            
            """ Gate of R transistor / RROW connection """
            # add contact to connect gate of rt to RROW (poly to metal2)
            offsetL = vector(lrt_xpos - rot_correct - drc["minwidth_poly"] - 0.5*contact.poly.width, self.r_nmosL[k].get_pins("G")[1].lc().y)
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=offsetL)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=offsetL)
                                    
            offsetR = vector(rrt_xpos + drc["minwidth_poly"] + 0.5*contact.poly.width, self.r_nmosR[k].get_pins("G")[1].rc().y)
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=offsetR)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=offsetR)
            
            # connect gate of rt to contact
            self.add_path("poly", [self.r_nmosL[k].get_pins("G")[1].lc(), offsetL])         
            self.add_path("poly", [self.r_nmosR[k].get_pins("G")[1].rc(), offsetR])
            
            # add contacts to RROW lines
            row_offsetL = vector(self.r_nmosL[k].get_pins("S")[1].lc().x - drc["minwidth_metal2"] - 0.5*contact.m1m2.width, self.rrow_positions[k].y + 0.5*drc["minwidth_metal1"])
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=row_offsetL,
                                    rotate=90)
                                                            
            row_offsetR = vector(self.r_nmosR[k].get_pins("S")[1].rc().x + drc["minwidth_metal2"] + 0.5*contact.m1m2.width, self.rrow_positions[k].y + 0.5*drc["minwidth_metal1"])
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=row_offsetR,
                                    rotate=90)
            
            # connect rt gate contacts to RROW contacts
            self.add_path("metal2", [offsetL, row_offsetL])
            self.add_path("metal2", [offsetR, row_offsetR])
            
            
            """ Gate of RA transistor / storage connection """
            # add contact to connect gate of rat to output of inverters
            offsetL = vector(lrt_xpos + drc["minwidth_poly"] + 0.5*contact.poly.width, self.r_nmosL[k].get_pins("G")[0].rc().y)
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=offsetL)
                        
            offsetR = vector(rrt_xpos - rot_correct - drc["minwidth_poly"] - 0.5*contact.poly.width, self.r_nmosR[k].get_pins("G")[0].lc().y)
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=offsetR)
            
            # connect gate of rat to contact
            self.add_path("poly", [self.r_nmosL[k].get_pins("G")[0].rc(), offsetL])
            self.add_path("poly", [self.r_nmosR[k].get_pins("G")[0].lc(), offsetR])
            
            # connect contact to output of inverters
            midL0 = vector(offsetL.x, self.r_nmosL[k].get_pins("S")[1].uc().y + 1.5*drc["minwidth_metal1"])
            midL1 = vector(self.i_nmosL.get_pin("S").lc().x - 1.5*drc["minwidth_metal1"], self.r_nmosL[0].get_pins("S")[1].uc().y + 1.5*drc["minwidth_metal1"])
            midL2 = vector(self.i_nmosL.get_pin("S").lc().x - 1.5*drc["minwidth_metal1"], self.cross_heightU)
            gate_offsetL = vector(self.i_nmosL.get_pin("D").center().x, self.cross_heightU)
            self.add_path("metal1", [offsetL, midL0, midL1, midL2, gate_offsetL])
            
            midR0 = vector(offsetR.x, self.r_nmosR[k].get_pins("S")[1].uc().y + 1.5*drc["minwidth_metal1"])
            midR1 = vector(self.i_nmosR.get_pin("D").rc().x + 1.5*drc["minwidth_metal1"], self.r_nmosR[k].get_pins("S")[1].uc().y + 1.5*drc["minwidth_metal1"])
            midR2 = vector(self.i_nmosR.get_pin("D").rc().x + 1.5*drc["minwidth_metal1"], self.cross_heightU)
            gate_offsetR = vector(self.i_nmosR.get_pin("S").center().x, self.cross_heightU)
            self.add_path("metal1", [offsetR, midR0, midR1, midR2, gate_offsetR]) 
            

    def extend_well(self):
        """ extend nwell and pwell """
        # extend pwell to encompass i_nmos
        offset = vector(self.leftmost_xpos, self.botmost_ypos)
        well_height = -self.botmost_ypos + self.i_nmos.well_height - drc["well_enclosure_active"]
        self.add_rect(layer="pwell",
                      offset=offset,
                      width=self.cell_width,
                      height=well_height)
                      
        # extend pwell to encompass r_nmos
        r_well_width = self.num_read*self.r_tile_width                      
        r_well_height = self.r_nmos.well_width - drc["well_enclosure_active"]
        offset = vector(self.leftmost_xpos, 0)
        self.add_rect(layer="pwell",
                      offset=offset,
                      width=r_well_width,
                      height=r_well_height)
                      
        offset = vector(-self.leftmost_xpos - r_well_width, 0)
        self.add_rect(layer="pwell",
                      offset=offset,
                      width=r_well_width,
                      height=r_well_height)
                      
        # extend pwell to encompass w_nmos
        lwt_xpos = -(self.i_nmos.active_width + 1.5*parameter["min_tx_size"] + self.w_tile_width - self.w_nmos.active_height - drc["well_enclosure_active"])
        rwt_xpos =  1.5*parameter["min_tx_size"] + self.i_nmos.active_width + self.w_tile_width - self.w_nmos.active_height - drc["well_enclosure_active"]    
        
        w_well_width = -(self.leftmost_xpos - lwt_xpos)                    
        w_well_height = self.w_nmos.well_width - drc["well_enclosure_active"]
        offset = vector(lwt_xpos - w_well_width, 0)
        self.add_rect(layer="pwell",
                      offset=offset,
                      width=w_well_width,
                      height=w_well_height)
                      
        offset = vector(rwt_xpos, 0)
        self.add_rect(layer="pwell",
                      offset=offset,
                      width=w_well_width,
                      height=w_well_height)
        
        # extend nwell to encompass i_pmos
        lit_xpos = -(self.i_nmos.active_width + 1.5*parameter["min_tx_size"] + drc["well_enclosure_active"])
        it_ypos = self.inv_gap + self.i_nmos.active_height - drc["well_enclosure_active"]
        offset = [lit_xpos,it_ypos]
        well_width = 2*self.i_pmos.active_width + 3*parameter["min_tx_size"] + 2*drc["well_enclosure_active"]
        well_height = self.vdd_position.y - it_ypos + drc["well_enclosure_active"] + drc["minwidth_tx"]
        self.add_rect(layer="nwell",
                      offset=offset,
                      width=well_width,
                      height=well_height)
        
        
        """ add well contacts """
        # connect pimplants to gnd
        offset = vector(0, self.gnd_position.y + 0.5*drc["minwidth_metal1"])
        self.add_contact_center(layers=("active", "contact", "metal1"),
                                offset=offset,
                                rotate=90)
        
        self.add_rect_center(layer="pimplant",
                             offset=offset,
                             width=drc["minwidth_tx"],
                             height=drc["minwidth_tx"])
        
        # connect nimplants to vdd
        offset = vector(0, self.vdd_position.y + 0.5*drc["minwidth_metal1"])
        self.add_contact_center(layers=("active", "contact", "metal1"),
                                offset=offset,
                                rotate=90)
                                
        self.add_rect_center(layer="nimplant",
                             offset=offset,
                             width=drc["minwidth_tx"],
                             height=drc["minwidth_tx"])    
        
    
    def add_fail(self):
        # for failing drc
        frail_width = self.well_width = 2*drc["minwidth_metal1"]
        frail_height = self.rail_height = drc["minwidth_metal1"]
        
        fail_position = vector(-25*drc["minwidth_tx"], - 1.5 * drc["minwidth_metal1"] - 0.5 * frail_height)  # for tiling purposes
        self.add_layout_pin(text="gnd",
                            layer="metal1",
                            offset=fail_position,
                            width=frail_width,
                            height=frail_height)

        fail_position2 = vector(-25*drc["minwidth_tx"], - 0.5 * drc["minwidth_metal1"]) 
        self.add_layout_pin(text="gnd2",
                            layer="metal1",
                            offset=fail_position2,
                            width=frail_width,
                            height=frail_height)
