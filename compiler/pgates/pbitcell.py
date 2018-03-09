import contact
import pgate
import design
import debug
from tech import drc, parameter, spice
from vector import vector
from ptx import ptx
from globals import OPTS

class pbitcell(pgate.pgate):
    """
    This module implements a parametrically sized multi-port bitcell
    """

    def __init__(self, num_write=1, num_read=1):
        name = "pbitcell_{0}W_{1}R".format(num_write, num_read)
        pgate.pgate.__init__(self, name)
        debug.info(2, "create a multi-port bitcell with {0} write ports and {1} read ports".format(num_write, num_read))  
        
        self.num_write = num_write
        self.num_read = num_read

        self.add_pins()
        self.create_layout()
        self.DRC_LVS()
    
    
    def add_pins(self):
        
        for k in range(self.num_write):
            self.add_pin("wbl{}".format(k))
            self.add_pin("wbl_bar{}".format(k))
        for k in range(self.num_read):
            self.add_pin("rbl{}".format(k))
            self.add_pin("rbl_bar{}".format(k))
            
        for k in range(self.num_write):
            self.add_pin("wrow{}".format(k))
        for k in range(self.num_read):
            self.add_pin("rrow{}".format(k))
            
        self.add_pin("vdd")
        self.add_pin("gnd")

        
    def create_layout(self):
        self.create_ptx()
        self.add_globals()
        self.add_storage()
        self.add_rails()
        self.add_write_ports()
        if(self.num_read > 0):
            self.add_read_ports()
        self.extend_well()
        self.offset_all_coordinates()
        #offset = vector(0, -0.5*drc["minwidth_metal2"])
        #self.translate_all(offset)
        #self.add_fail()
    
    def create_ptx(self):
        """ Calculate transistor sizes """
        # if there are no read ports then write transistors are being used as read/write ports, like in a 6T cell
        if(self.num_read == 0):
            inverter_nmos_width = 3*parameter["min_tx_size"]
            inverter_pmos_width = parameter["min_tx_size"]
            write_nmos_width = 1.5*parameter["min_tx_size"]
            read_nmos_width = parameter["min_tx_size"] # read transistor not necessary but included as to not generate errors in the code when referenced
            
        # used for the dual port case where there are separate write and read ports
        else:
            inverter_nmos_width = 2*parameter["min_tx_size"]
            inverter_pmos_width = parameter["min_tx_size"]
            write_nmos_width = parameter["min_tx_size"]
            read_nmos_width = 2*parameter["min_tx_size"]
    
        """ Create ptx for all transistors """
        # create ptx for inverter transistors
        self.inverter_nmos = ptx(width=inverter_nmos_width,
                                 tx_type="nmos")
        self.add_mod(self.inverter_nmos)

        self.inverter_pmos = ptx(width=inverter_pmos_width,
                                 tx_type="pmos")
        self.add_mod(self.inverter_pmos)
        
        # create ptx for write transitors
        self.write_nmos = ptx(width=write_nmos_width,
                              tx_type="nmos")
        self.add_mod(self.write_nmos)
        
        # create ptx for read transistors
        self.read_nmos = ptx(width=read_nmos_width,
                             tx_type="nmos")
        self.add_mod(self.read_nmos)
    
    
    def add_globals(self):        
        """ Define pbitcell global variables """
        # calculate metal contact extensions over transistor active
        self.inverter_pmos_contact_extension = 0.5*(self.inverter_pmos.active_contact.height - self.inverter_pmos.active_height)
        self.write_nmos_contact_extension = 0.5*(self.write_nmos.active_contact.height - self.write_nmos.active_height)    
        
        # calculation for transistor spacing (exact solutions)
        self.inverter_to_inverter_spacing = contact.poly.height + drc["minwidth_metal1"]
        self.inverter_to_write_spacing = drc["pwell_to_nwell"] + 2*drc["well_enclosure_active"]
        self.write_to_write_spacing = drc["minwidth_metal2"] + self.write_nmos_contact_extension + contact.poly.width + drc["poly_to_field_poly"] + drc["poly_extend_active"]
        self.write_to_read_spacing = drc["minwidth_poly"] + drc["poly_to_field_poly"] + drc["minwidth_metal2"] + 2*contact.poly.width + self.write_nmos_contact_extension
        self.read_to_read_spacing = 2*drc["minwidth_poly"] + drc["minwidth_metal1"] + 2*contact.poly.width
        
        # calculation for transistor spacing (symmetric solutions)
        #self.inverter_to_inverter_spacing = 3*parameter["min_tx_size"]
        #self.inverter_to_write_spacing = need to calculate
        #spacing_option1 = contact.poly.width + 2*drc["poly_to_field_poly"] + 2*drc["poly_extend_active"]
        #spacing_option2 = contact.poly.width + 2*drc["minwidth_metal2"] + 2*self.write_nmos_contact_extension
        #self.write_to_write_spacing = max(spacing_option1, spacing_option2)
        #self.write_to_read_spacing = drc["poly_to_field_poly"] + 2*contact.poly.width + 2*drc["minwidth_metal2"] + 2*self.write_nmos_contact_extension
        #self.read_to_read_spacing = drc["minwidth_metal1"] + 2*contact.poly.width + 2*drc["minwidth_poly"]
        
        # calculations for transistor tiling (includes transistor and spacing)
        self.inverter_tile_width = self.inverter_nmos.active_width + 0.5*self.inverter_to_inverter_spacing
        self.write_tile_width = self.write_to_write_spacing + self.write_nmos.active_height
        self.read_tile_width = self.read_to_read_spacing + self.read_nmos.active_height
        
        # calculation for row line tiling
        self.rail_tile_height = drc["active_to_body_active"] + 0.5*(drc["minwidth_tx"] - drc["minwidth_metal1"]) + drc["minwidth_metal1"]
        self.rowline_tile_height = drc["minwidth_metal1"] + contact.m1m2.width
        
        # calculations related to inverter connections
        self.inverter_gap = drc["poly_to_active"] + drc["poly_to_field_poly"] + 2*contact.poly.width + drc["minwidth_metal1"] + self.inverter_pmos_contact_extension
        self.cross_couple_lower_ypos = self.inverter_nmos.active_height + drc["poly_to_active"] + 0.5*contact.poly.width
        self.cross_couple_upper_ypos = self.inverter_nmos.active_height + drc["poly_to_active"] + drc["poly_to_field_poly"] + 1.5*contact.poly.width
        
        """ Calculations for the edges of the cell """
        # create a flag for excluding read port calculations if they are not included in the bitcell
        if(self.num_read > 0):
            read_port_flag = 1
        else:
            read_port_flag = 0
            
        # leftmost position = storage width + write ports width + read ports width + read transistor gate connections + metal spacing necessary for tiling the bitcell
        self.leftmost_xpos = -self.inverter_tile_width \
                             - self.inverter_to_write_spacing - self.write_nmos.active_height - (self.num_write-1)*self.write_tile_width \
                             - read_port_flag*(self.write_to_read_spacing + self.read_nmos.active_height + (self.num_read-1)*self.read_tile_width) \
                             - drc["minwidth_poly"] - contact.m1m2.height \
                             - 0.5*drc["minwidth_metal2"]
                             
        self.rightmost_xpos = -self.leftmost_xpos
        
        # bottommost position = gnd height + wrow height + rrow height
        self.botmost_ypos = -self.rail_tile_height \
                            - self.num_write*self.rowline_tile_height \
                            - read_port_flag*(self.num_read*self.rowline_tile_height)
                            
        # topmost position = height of the inverter + height of vdd
        self.topmost_ypos = self.inverter_nmos.active_height + self.inverter_gap + self.inverter_pmos.active_height \
                            + self.rail_tile_height
        
        # calculations for the cell dimensions
        self.width = -2*self.leftmost_xpos
        self.height = self.topmost_ypos - self.botmost_ypos + 0.5*drc["minwidth_metal2"] - 0.5*drc["minwidth_metal1"]

        
    def add_storage(self):
        """
        Creates the crossed coupled inverters that act as storage for the bitcell.
        The stored value of the cell is denoted as "Q", and the inverted value as "Q_bar".
        """
        
        # calculate transistor offsets
        left_inverter_xpos = -0.5*self.inverter_to_inverter_spacing - self.inverter_nmos.active_width
        right_inverter_xpos = 0.5*self.inverter_to_inverter_spacing
        inverter_pmos_ypos = self.inverter_nmos.active_height + self.inverter_gap
                
        # create active for nmos
        self.inverter_nmos_left = self.add_inst(name="inverter_nmos_left",
                                                mod=self.inverter_nmos,
                                                offset=[left_inverter_xpos,0])
        self.connect_inst(["Q_bar", "Q", "gnd", "gnd"])
        
        self.inverter_nmos_right = self.add_inst(name="inverter_nmos_right",
                                                 mod=self.inverter_nmos,
                                                 offset=[right_inverter_xpos,0])
        self.connect_inst(["gnd", "Q_bar", "Q", "gnd"])
        
        # create active for pmos
        self.inverter_pmos_left = self.add_inst(name="inverter_pmos_left",
                                                mod=self.inverter_pmos,
                                                offset=[left_inverter_xpos, inverter_pmos_ypos])
        self.connect_inst(["Q_bar", "Q", "vdd", "vdd"])
        
        self.inverter_pmos_right = self.add_inst(name="inverter_pmos_right",
                                                 mod=self.inverter_pmos,
                                                 offset=[right_inverter_xpos, inverter_pmos_ypos])
        self.connect_inst(["vdd", "Q_bar", "Q", "vdd"])
        
        # connect input (gate) of inverters
        self.add_path("poly", [self.inverter_nmos_left.get_pin("G").uc(), self.inverter_pmos_left.get_pin("G").bc()])
        self.add_path("poly", [self.inverter_nmos_right.get_pin("G").uc(), self.inverter_pmos_right.get_pin("G").bc()]) 
        
        # connect output (drain/source) of inverters
        self.add_path("metal1", [self.inverter_nmos_left.get_pin("D").uc(), self.inverter_pmos_left.get_pin("D").bc()], width=contact.well.second_layer_width)
        self.add_path("metal1", [self.inverter_nmos_right.get_pin("S").uc(), self.inverter_pmos_right.get_pin("S").bc()], width=contact.well.second_layer_width)
        
        # add contacts to connect gate poly to drain/source metal1 (to connect Q to Q_bar)
        contact_offset_left =  vector(self.inverter_nmos_left.get_pin("D").rc().x + 0.5*contact.poly.height, self.cross_couple_upper_ypos)
        self.add_contact_center(layers=("poly", "contact", "metal1"),
                                        offset=contact_offset_left,
                                        rotate=90)
                                
        contact_offset_right =  vector(self.inverter_nmos_right.get_pin("S").lc().x - 0.5*contact.poly.height, self.cross_couple_lower_ypos)
        self.add_contact_center(layers=("poly", "contact", "metal1"),
                                        offset=contact_offset_right,
                                        rotate=90)
                                           
        # connect contacts to gate poly (cross couple)
        gate_offset_right = vector(self.inverter_nmos_right.get_pin("G").lc().x, contact_offset_left.y)
        self.add_path("poly", [contact_offset_left, gate_offset_right])
        
        gate_offset_left = vector(self.inverter_nmos_left.get_pin("G").rc().x, contact_offset_right.y)
        self.add_path("poly", [contact_offset_right, gate_offset_left])
        
       
    def add_rails(self):
        """
        Add gnd and vdd rails and connects them to the inverters
        """
        
        """ Add rails for vdd and gnd """
        self.gnd_position = vector(self.leftmost_xpos, -self.rail_tile_height)
        self.gnd = self.add_layout_pin(text="gnd",
                                       layer="metal1",
                                       offset=self.gnd_position,
                                       width=self.width,
                                       height=contact.well.second_layer_width)
        
        vdd_ypos = self.inverter_nmos.active_height + self.inverter_gap + self.inverter_pmos.active_height \
                   + drc["active_to_body_active"] + 0.5*(drc["minwidth_tx"] - drc["minwidth_metal1"])
        #vdd_ypos = self.inverter_pmos_left.get_pin("S").uc().y + drc["minwidth_metal1"]
        self.vdd_position = vector(self.leftmost_xpos, vdd_ypos)
        self.vdd = self.add_layout_pin(text="vdd",
                                       layer="metal1",
                                       offset=self.vdd_position,
                                       width=self.width,
                                       height=drc["minwidth_metal1"])
                
        """ Connect inverters to rails """
        # connect inverter nmos to gnd        
        gnd_pos_left = vector(self.inverter_nmos_left.get_pin("S").bc().x, self.gnd_position.y)
        self.add_path("metal1", [self.inverter_nmos_left.get_pin("S").bc(), gnd_pos_left])
        
        gnd_pos_right = vector(self.inverter_nmos_right.get_pin("D").bc().x, self.gnd_position.y)        
        self.add_path("metal1", [self.inverter_nmos_right.get_pin("D").bc(), gnd_pos_right])
        
        # connect inverter pmos to vdd
        vdd_pos_left = vector(self.inverter_nmos_left.get_pin("S").uc().x, self.vdd_position.y)
        self.add_path("metal1", [self.inverter_pmos_left.get_pin("S").uc(), vdd_pos_left])
        
        vdd_pos_right = vector(self.inverter_nmos_right.get_pin("D").uc().x, self.vdd_position.y)
        self.add_path("metal1", [self.inverter_pmos_right.get_pin("D").uc(), vdd_pos_right])


    def add_write_ports(self):
        """
        Adds write ports to the bit cell. A single transistor acts as the write port.
        A write is enabled by setting a Write-Rowline (WROW) high, subsequently turning on the transistor.
        The transistor is connected between a Write-Bitline (WBL) and the storage component of the cell (Q). 
        Driving WBL high or low sets the value of the cell.
        This is a differential design, so each write port has a mirrored port that connects WBL_bar to Q_bar.
        """
    
        """ Define variables relevant to write transistors """
        # define offset correction due to rotation of the ptx cell
        write_rotation_correct = self.write_nmos.active_height
        
        # define write transistor variables as empty arrays based on the number of write ports
        self.write_nmos_left = [None] * self.num_write 
        self.write_nmos_right = [None] * self.num_write
        self.wrow_positions = [None] * self.num_write
        self.wbl_positions = [None] * self.num_write
        self.wbl_bar_positions = [None] * self.num_write       
        
        # iterate over the number of write ports
        for k in range(0,self.num_write):
            """ Add transistors """
            # calculate write transistor offsets 
            left_write_transistor_xpos = -self.inverter_tile_width \
                                         - self.inverter_to_write_spacing - self.write_nmos.active_height - k*self.write_tile_width \
                                         + write_rotation_correct
            
            right_write_transistor_xpos = self.inverter_tile_width \
                                          + self.inverter_to_write_spacing + k*self.write_tile_width \
                                          + write_rotation_correct
            
            # add write transistors
            self.write_nmos_left[k] = self.add_inst(name="write_nmos_left{}".format(k),
                                                    mod=self.write_nmos,
                                                    offset=[left_write_transistor_xpos,0],
                                                    rotate=90)
            self.connect_inst(["Q", "wrow{}".format(k), "wbl{}".format(k), "gnd"])
            
            self.write_nmos_right[k] = self.add_inst(name="write_nmos_right{}".format(k),
                                                     mod=self.write_nmos,
                                                     offset=[right_write_transistor_xpos,0],
                                                     rotate=90)
            self.connect_inst(["Q_bar", "wrow{}".format(k), "wbl_bar{}".format(k), "gnd"])
                        
            """ Add WROW lines """
            # calculate WROW position
            wrow_ypos = self.gnd_position.y - (k+1)*self.rowline_tile_height 
            self.wrow_positions[k] = vector(self.leftmost_xpos, wrow_ypos)
            
            # add pin for WROW
            self.add_layout_pin(text="wrow{}".format(k),
                                layer="metal1",
                                offset=self.wrow_positions[k],
                                width=self.width,
                                height=contact.m1m2.width)
                       
            """ Source/WBL/WBL_bar connections """            
            # add metal1-to-metal2 contacts on top of write transistor source pins for connection to WBL and WBL_bar
            offset_left = self.write_nmos_left[k].get_pin("S").center()
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=offset_left,
                                    rotate=90)
            
            offset_right = self.write_nmos_right[k].get_pin("S").center()
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=offset_right,
                                    rotate=90)
            
            # add pins for WBL and WBL_bar, overlaid on source contacts
            self.wbl_positions[k] = vector(self.write_nmos_left[k].get_pin("S").center().x - 0.5*drc["minwidth_metal2"], self.botmost_ypos)
            self.add_layout_pin(text="wbl{}".format(k),
                                layer="metal2",
                                offset=self.wbl_positions[k],
                                width=drc["minwidth_metal2"],
                                height=self.height)

            self.wbl_bar_positions[k] = vector(self.write_nmos_right[k].get_pin("S").center().x - 0.5*drc["minwidth_metal2"], self.botmost_ypos)
            self.add_layout_pin(text="wbl_bar{}".format(k),
                                layer="metal2",
                                offset=self.wbl_bar_positions[k],
                                width=drc["minwidth_metal2"],
                                height=self.height)
                        
            """ Gate/WROW connections """
            # add poly-to-meltal2 contacts to connect gate of write transistors to WROW (contact next to gate)
            # contact must be placed a metal width below the source pin to avoid drc from routing to the source pins
            contact_xpos = self.write_nmos_left[k].get_pin("S").lc().x - drc["minwidth_metal2"] - 0.5*contact.m1m2.width
            contact_ypos = self.write_nmos_left[k].get_pin("D").bc().y - drc["minwidth_metal1"] - 0.5*contact.m1m2.height
            left_gate_contact =  vector(contact_xpos, contact_ypos)
            
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=left_gate_contact)            
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=left_gate_contact)            
            
            contact_xpos = self.write_nmos_right[k].get_pin("S").rc().x + drc["minwidth_metal2"] + 0.5*contact.m1m2.width
            contact_ypos = self.write_nmos_right[k].get_pin("D").bc().y - drc["minwidth_metal1"] - 0.5*contact.m1m2.height
            right_gate_contact = vector(contact_xpos, contact_ypos)
            
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=right_gate_contact)            
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=right_gate_contact)
            
            # connect gate of write transistor to contact (poly path)
            midL = vector(left_gate_contact.x, self.write_nmos_left[k].get_pin("G").lc().y)
            self.add_path("poly", [self.write_nmos_left[k].get_pin("G").lc(), midL, left_gate_contact], width=contact.poly.width)
            
            midR = vector(right_gate_contact.x, self.write_nmos_right[k].get_pin("G").rc().y) 
            self.add_path("poly", [self.write_nmos_right[k].get_pin("G").rc(), midR, right_gate_contact], width=contact.poly.width)
            
            # add metal1-to-metal2 contacts to WROW lines
            left_wrow_contact = vector(left_gate_contact.x, self.wrow_positions[k].y + 0.5*contact.m1m2.width)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                            offset=left_wrow_contact,
                                            rotate=90)
                             
            right_wrow_contact = vector(right_gate_contact.x, self.wrow_positions[k].y + 0.5*contact.m1m2.width)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                            offset=right_wrow_contact,
                                            rotate=90)
            
            # connect write transistor gate contacts to WROW contacts (metal2 path)
            self.add_path("metal2", [left_gate_contact, left_wrow_contact])
            self.add_path("metal2", [right_gate_contact, right_wrow_contact])
                       
            """ Drain/Storage connections """
            # this path only needs to be drawn once on the last iteration of the loop
            if(k == self.num_write-1):
                # add contacts to connect gate of inverters to drain of write transistors
                left_storage_contact =  vector(self.inverter_nmos_left.get_pin("G").lc().x - drc["poly_to_field_poly"] - 0.5*contact.poly.width, self.cross_couple_lower_ypos)
                self.add_contact_center(layers=("poly", "contact", "metal1"),
                                                offset=left_storage_contact,
                                                rotate=90)
                
                right_storage_contact =  vector(self.inverter_nmos_right.get_pin("G").rc().x + drc["poly_to_field_poly"] + 0.5*contact.poly.width, self.cross_couple_lower_ypos)
                self.add_contact_center(layers=("poly", "contact", "metal1"),
                                                offset=right_storage_contact,
                                                rotate=90)
                                 
                # connect gate of inverters to contacts (poly path)
                inverter_gate_offset_left = vector(self.inverter_nmos_left.get_pin("G").lc().x, self.cross_couple_lower_ypos)
                self.add_path("poly", [left_storage_contact, inverter_gate_offset_left])
                
                inverter_gate_offset_right = vector(self.inverter_nmos_right.get_pin("G").rc().x, self.cross_couple_lower_ypos)
                self.add_path("poly", [right_storage_contact, inverter_gate_offset_right])
                
                # connect contacts to drains of write transistors (metal1 path)
                midL0 = vector(left_storage_contact.x - 0.5*contact.poly.height - 1.5*drc["minwidth_metal1"], left_storage_contact.y)
                midL1 = vector(left_storage_contact.x - 0.5*contact.poly.height - 1.5*drc["minwidth_metal1"], self.write_nmos_left[k].get_pin("D").lc().y)
                self.add_path("metal1", [left_storage_contact, midL0, midL1, self.write_nmos_left[k].get_pin("D").lc()])
                
                midR0 = vector(right_storage_contact.x + 0.5*contact.poly.height + 1.5*drc["minwidth_metal1"], right_storage_contact.y)
                midR1 = vector(right_storage_contact.x + 0.5*contact.poly.height + 1.5*drc["minwidth_metal1"], self.write_nmos_right[k].get_pin("D").rc().y)
                self.add_path("metal1", [right_storage_contact, midR0, midR1, self.write_nmos_right[k].get_pin("D").rc()])

                
    def add_read_ports(self):
        """
        Adds read ports to the bit cell. Two transistors function as a read port.
        The two transistors in the port are denoted as the "read transistor" and the "read-access transistor".
        The read transistor is connected to RROW (gate), RBL (drain), and the read-access transistor (source).
        The read-access transistor is connected to Q_bar (gate), gnd (source), and the read transistor (drain).
        A read is enabled by setting a Read-Rowline (RROW) high, subsequently turning on the read transistor.
        The Read-Bitline (RBL) is precharged to high, and when the value of Q_bar is high, the read-access transistor
        is turned on, creating a connection between RBL and gnd. RBL subsequently discharges allowing for a differential read
        using sense amps. This is a differential design, so each read port has a mirrored port that connects RBL_bar to Q.
        """
        
        """ Define variables relevant to read transistors """ 
        # define offset correction due to rotation of the ptx cell
        read_rotation_correct = self.read_nmos.active_height
        
        # calculate offset to overlap the drain of the read-access transistor with the source of the read transistor
        overlap_offset = self.read_nmos.get_pin("D").ll() - self.read_nmos.get_pin("S").ll()
        
        # define read transistor variables as empty arrays based on the number of read ports
        self.read_nmos_left = [None] * self.num_read 
        self.read_nmos_right = [None] * self.num_read
        self.read_access_nmos_left = [None] * self.num_read 
        self.read_access_nmos_right = [None] * self.num_read
        self.rrow_positions = [None] * self.num_read
        self.rbl_positions = [None] * self.num_read
        self.rbl_bar_positions = [None] * self.num_read
        
        # iterate over the number of read ports
        for k in range(0,self.num_read):
            """ Add transistors """
            # calculate transistor offsets
            left_read_transistor_xpos = -self.inverter_tile_width \
                                        - self.inverter_to_write_spacing - self.write_nmos.active_height - (self.num_write-1)*self.write_tile_width \
                                        - self.write_to_read_spacing - self.read_nmos.active_height - k*self.read_tile_width \
                                        + read_rotation_correct
                       
            right_read_transistor_xpos = self.inverter_tile_width \
                                         + self.inverter_to_write_spacing + self.write_nmos.active_height + (self.num_write-1)*self.write_tile_width \
                                         + self.write_to_read_spacing + k*self.read_tile_width \
                                         + read_rotation_correct          
            
            # add read-access transistors
            self.read_access_nmos_left[k] = self.add_inst(name="read_access_nmos_left",
                                                          mod=self.read_nmos,
                                                          offset=[left_read_transistor_xpos,0],
                                                          rotate=90)
            self.connect_inst(["RA_to_R_left{}".format(k), " Q_bar", "gnd", "gnd"])
            
            self.read_access_nmos_right[k] = self.add_inst(name="read_access_nmos_right",
                                                           mod=self.read_nmos,
                                                           offset=[right_read_transistor_xpos,0],
                                                           rotate=90)
            self.connect_inst(["RA_to_R_right{}".format(k), "Q", "gnd", "gnd"])
            
            # add read transistors
            self.read_nmos_left[k] = self.add_inst(name="read_nmos_left",
                                                   mod=self.read_nmos,
                                                   offset=[left_read_transistor_xpos,overlap_offset.x],
                                                   rotate=90)
            self.connect_inst(["rbl{}".format(k), "rrow{}".format(k), "RA_to_R_left{}".format(k), "gnd"])
            
            self.read_nmos_right[k] = self.add_inst(name="read_nmos_right",
                                                    mod=self.read_nmos,
                                                    offset=[right_read_transistor_xpos,overlap_offset.x],
                                                    rotate=90)
            self.connect_inst(["rbl_bar{}".format(k), "rrow{}".format(k), "RA_to_R_right{}".format(k), "gnd"])
                        
            """ Add RROW lines """
            # calculate RROW position
            rrow_ypos = self.gnd_position.y \
                        - self.num_write*self.rowline_tile_height \
                        - (k+1)*self.rowline_tile_height            
            self.rrow_positions[k] = vector(self.leftmost_xpos, rrow_ypos)
            
            # add pin for RROW
            self.add_layout_pin(text="rrow{}".format(k),
                                layer="metal1",
                                offset=self.rrow_positions[k],
                                width=self.width,
                                height=contact.m1m2.width)
                       
            """ Drain of read transistor / RBL & RBL_bar connection """
            # add metal1-to-metal2 contacts on top of read transistor drain pins for connection to RBL and RBL_bar
            offset_left = self.read_nmos_left[k].get_pin("D").center()
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=offset_left,
                                    rotate=90)
            
            offset_right = self.read_nmos_right[k].get_pin("D").center()
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=offset_right,
                                    rotate=90)
            
            # add pins for RBL and RBL_bar, overlaid on drain contacts
            self.rbl_positions[k] = vector(self.read_nmos_left[k].get_pin("D").center().x - 0.5*drc["minwidth_metal2"], self.botmost_ypos)
            self.add_layout_pin(text="rbl{}".format(k),
                                layer="metal2",
                                offset=self.rbl_positions[k],
                                width=drc["minwidth_metal2"],
                                height=self.height)

            self.rbl_bar_positions[k] = vector(self.read_nmos_right[k].get_pin("D").center().x - 0.5*drc["minwidth_metal2"], self.botmost_ypos)
            self.add_layout_pin(text="rbl_bar{}".format(k),
                                layer="metal2",
                                offset=self.rbl_bar_positions[k],
                                width=drc["minwidth_metal2"],
                                height=self.height)
                       
            """ Gate of read transistor / RROW connection """
            # add poly-to-meltal2 contacts to connect gate of read transistors to RROW (contact next to gate)
            contact_xpos = left_read_transistor_xpos - self.read_nmos.active_height - drc["minwidth_poly"] - 0.5*contact.poly.width
            contact_ypos = self.read_nmos_left[k].get_pin("G").lc().y
            left_gate_contact = vector(contact_xpos, contact_ypos)
            
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=left_gate_contact)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=left_gate_contact)
            
            contact_xpos = right_read_transistor_xpos + drc["minwidth_poly"] + 0.5*contact.poly.width
            contact_ypos = self.read_nmos_right[k].get_pin("G").rc().y
            right_gate_contact = vector(contact_xpos, contact_ypos)
            
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=right_gate_contact)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=right_gate_contact)
            
            # connect gate of read transistor to contact (poly path)
            self.add_path("poly", [self.read_nmos_left[k].get_pin("G").lc(), left_gate_contact])         
            self.add_path("poly", [self.read_nmos_right[k].get_pin("G").rc(), right_gate_contact])
            
            # add metal1-to-metal2 contacts to RROW lines
            left_rrow_contact = vector(left_gate_contact.x, self.rrow_positions[k].y + 0.5*contact.m1m2.width)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=left_rrow_contact,
                                    rotate=90)
                                                            
            right_rrow_contact = vector(right_gate_contact.x, self.rrow_positions[k].y + 0.5*contact.m1m2.width)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=right_rrow_contact,
                                    rotate=90)
            
            # connect read transistor gate contacts to RROW contacts (metal2 path)
            self.add_path("metal2", [left_gate_contact, left_rrow_contact])
            self.add_path("metal2", [right_gate_contact, right_rrow_contact])
            
            """ Source of read-access transistor / GND connection """
            # connect source of read-access transistor to GND (metal1 path)
            gnd_offset_left = vector(self.read_access_nmos_left[k].get_pin("S").bc().x, self.gnd_position.y)
            self.add_path("metal1", [self.read_access_nmos_left[k].get_pin("S").bc(), gnd_offset_left])
            
            gnd_offset_right = vector(self.read_access_nmos_right[k].get_pin("S").bc().x, self.gnd_position.y)
            self.add_path("metal1", [self.read_access_nmos_right[k].get_pin("S").bc(), gnd_offset_right])
            
            """ Gate of read-access transistor / storage connection """
            # add poly-to-metal1 contacts to connect gate of read-access transistors to output of inverters (contact next to gate)
            contact_xpos = left_read_transistor_xpos + drc["minwidth_poly"] + 0.5*contact.poly.width
            contact_ypos = self.read_access_nmos_left[k].get_pin("G").rc().y
            left_gate_contact = vector(contact_xpos, contact_ypos)
            
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=left_gate_contact)
            
            contact_xpos = right_read_transistor_xpos - self.read_nmos.active_height - drc["minwidth_poly"] - 0.5*contact.poly.width
            contact_ypos = self.read_access_nmos_right[k].get_pin("G").lc().y
            right_gate_contact = vector(contact_xpos, contact_ypos)
            
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=right_gate_contact)
            
            # connect gate of read-access transistor to contact (poly path)
            self.add_path("poly", [self.read_access_nmos_left[k].get_pin("G").rc(), left_gate_contact])
            self.add_path("poly", [self.read_access_nmos_right[k].get_pin("G").lc(), right_gate_contact])
            
            # connect contact to output of inverters (metal1 path)
            # mid0: metal1 path must route over the read transistors (above drain of read transistor)
            # mid1: continue metal1 path horizontally until at inverter
            # mid2: route down to be level with inverter output
            # endpoint at drain/source of inverter
            midL0 = vector(left_gate_contact.x, self.read_nmos_left[k].get_pin("D").uc().y + 1.5*drc["minwidth_metal1"])
            midL1 = vector(self.inverter_nmos_left.get_pin("S").lc().x - 1.5*drc["minwidth_metal1"], self.read_nmos_left[0].get_pin("D").uc().y + 1.5*drc["minwidth_metal1"])
            midL2 = vector(self.inverter_nmos_left.get_pin("S").lc().x - 1.5*drc["minwidth_metal1"], self.cross_couple_upper_ypos)
            left_inverter_offset = vector(self.inverter_nmos_left.get_pin("D").center().x, self.cross_couple_upper_ypos)
            self.add_path("metal1", [left_gate_contact, midL0, midL1, midL2, left_inverter_offset])
            
            midR0 = vector(right_gate_contact.x, self.read_nmos_right[k].get_pin("D").uc().y + 1.5*drc["minwidth_metal1"])
            midR1 = vector(self.inverter_nmos_right.get_pin("D").rc().x + 1.5*drc["minwidth_metal1"], self.read_nmos_right[k].get_pin("D").uc().y + 1.5*drc["minwidth_metal1"])
            midR2 = vector(self.inverter_nmos_right.get_pin("D").rc().x + 1.5*drc["minwidth_metal1"], self.cross_couple_upper_ypos)
            right_inverter_offset = vector(self.inverter_nmos_right.get_pin("S").center().x, self.cross_couple_upper_ypos)
            self.add_path("metal1", [right_gate_contact, midR0, midR1, midR2, right_inverter_offset]) 
            

    def extend_well(self):
        """
        Connects wells between ptx cells to avoid drc spacing issues.
        Since the pwell of the read ports rise higher than the pmos of the inverters,
        the well connections must be done piecewise to avoid pwell and nwell overlap.
        """
    
        cell_well_tiling_offset = 0.5*drc["minwidth_metal2"]
        """ extend pwell to encompass entire nmos region of the cell up to the height of the inverter nmos well """
        offset = vector(self.leftmost_xpos, self.botmost_ypos - cell_well_tiling_offset)
        well_height = -self.botmost_ypos + self.inverter_nmos.cell_well_height - drc["well_enclosure_active"] + cell_well_tiling_offset
        self.add_rect(layer="pwell",
                      offset=offset,
                      width=self.width,
                      height=well_height)
                      
        """ extend pwell over write transistors to the height of the write transistor well """
        # calculate the edge of the write transistor well closest to the center
        left_write_well_xpos = -(self.inverter_tile_width + self.write_to_write_spacing - drc["well_enclosure_active"])
        right_write_well_xpos =  self.inverter_tile_width + self.write_to_write_spacing - drc["well_enclosure_active"]    
        
        # calculate a width that will halt at the edge of the write transistors
        write_well_width = -(self.leftmost_xpos - left_write_well_xpos)                    
        write_well_height = self.write_nmos.cell_well_width - drc["well_enclosure_active"]
        
        offset = vector(left_write_well_xpos - write_well_width, 0)
        self.add_rect(layer="pwell",
                      offset=offset,
                      width=write_well_width,
                      height=write_well_height)
                      
        offset = vector(right_write_well_xpos, 0)
        self.add_rect(layer="pwell",
                      offset=offset,
                      width=write_well_width,
                      height=write_well_height)
                     
        """ extend pwell over the read transistors to the height of the bitcell """
        if(self.num_read > 0):
            # calculate the edge of the read transistor well clostest to the center
            left_read_well_xpos = -(self.inverter_tile_width + self.num_write*self.write_tile_width + self.write_to_read_spacing - drc["well_enclosure_active"])
            right_read_well_xpos =  self.inverter_tile_width + self.num_write*self.write_tile_width + self.write_to_read_spacing - drc["well_enclosure_active"] 
        
            # calculate a width that will halt at the edge of the read transistors
            read_well_width = -(self.leftmost_xpos - left_read_well_xpos)               
            read_well_height = self.topmost_ypos
            
            offset = vector(self.leftmost_xpos, 0)
            self.add_rect(layer="pwell",
                          offset=offset,
                          width=read_well_width,
                          height=read_well_height)
                          
            offset = vector(right_read_well_xpos, 0)
            self.add_rect(layer="pwell",
                          offset=offset,
                          width=read_well_width,
                          height=read_well_height)
        
        """ extend nwell to encompass inverter_pmos """
        # calculate offset of the left pmos well
        inverter_well_xpos = -self.inverter_tile_width - drc["well_enclosure_active"]
        inverter_well_ypos = self.inverter_nmos.active_height + self.inverter_gap - drc["well_enclosure_active"]
        
        # calculate width of the two combined nwells
        # calculate height to encompass nimplant connected to vdd
        well_width = 2*self.inverter_tile_width + 2*drc["well_enclosure_active"]
        well_height = self.vdd_position.y - inverter_well_ypos + drc["well_enclosure_active"] + drc["minwidth_tx"]
        
        offset = [inverter_well_xpos,inverter_well_ypos]
        self.add_rect(layer="nwell",
                      offset=offset,
                      width=well_width,
                      height=well_height)
        
        
        """ add well contacts """
        # connect pimplants to gnd
        offset = vector(0, self.gnd_position.y + 0.5*contact.well.second_layer_width)
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
        # for failing drc when I want to observe the gds layout       
        fail_position = vector(-4*drc["minwidth_metal1"], 0)  # for tiling purposes
        self.add_layout_pin(text="fail1",
                            layer="metal1",
                            offset=fail_position,
                            width=drc["minwidth_metal1"],
                            height=drc["minwidth_metal1"])

        fail_position2 = vector(-4*drc["minwidth_metal1"], -1.5*drc["minwidth_metal1"]) 
        self.add_layout_pin(text="fail2",
                            layer="metal1",
                            offset=fail_position2,
                            width=drc["minwidth_metal1"],
                            height=drc["minwidth_metal1"])
