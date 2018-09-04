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
    This module implements a parametrically sized multi-port bitcell,
    with a variable number of read/write, write, and read ports
    """

    width = None
    height = None
    
    def __init__(self):
        
        self.num_rw_ports = OPTS.num_rw_ports
        self.num_w_ports = OPTS.num_w_ports
        self.num_r_ports = OPTS.num_r_ports
        
        name = "pbitcell_{0}RW_{1}W_{2}R".format(self.num_rw_ports, self.num_w_ports, self.num_r_ports)
        pgate.pgate.__init__(self, name)
        debug.info(2, "create a multi-port bitcell with {0} rw ports, {1} w ports and {2} r ports".format(self.num_rw_ports,
                                                                                                          self.num_w_ports,
                                                                                                          self.num_r_ports))  

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

        # FIXME: Why is this static set here?
        pbitcell.width = self.width
        pbitcell.height = self.height
        
    def create_netlist(self):
        self.add_pins()
        self.add_modules()
        self.create_storage()
        
        if(self.num_rw_ports > 0):
            self.create_readwrite_ports()
        if(self.num_w_ports > 0):
            self.create_write_ports()
        if(self.num_r_ports > 0):
            self.create_read_ports()
        
    def create_layout(self):
        self.calculate_spacing()
        self.calculate_postions()
        
        self.place_storage()
        self.route_storage()
        self.route_rails()
        
        if(self.num_rw_ports > 0):
            self.place_readwrite_ports()
        if(self.num_w_ports > 0):
            self.place_write_ports()
        if(self.num_r_ports > 0):
            self.place_read_ports()
        self.extend_well()
        
        self.offset_all_coordinates()
        self.DRC_LVS()
    
    def add_pins(self):
        for k in range(self.num_rw_ports):
            self.add_pin("rwbl{}".format(k))
            self.add_pin("rwbl_bar{}".format(k))
        for k in range(self.num_w_ports):
            self.add_pin("wbl{}".format(k))
            self.add_pin("wbl_bar{}".format(k))
        for k in range(self.num_r_ports):
            self.add_pin("rbl{}".format(k))
            self.add_pin("rbl_bar{}".format(k))
        
        for k in range(self.num_rw_ports):
            self.add_pin("rwwl{}".format(k))
        for k in range(self.num_w_ports):
            self.add_pin("wwl{}".format(k))
        for k in range(self.num_r_ports):
            self.add_pin("rwl{}".format(k))
            
        self.add_pin("vdd")
        self.add_pin("gnd")
    
    def add_modules(self):
        # if there are any read/write ports, then the inverter nmos is sized based the number of them
        if(self.num_rw_ports > 0):
            inverter_nmos_width = self.num_rw_ports*3*parameter["min_tx_size"]
            inverter_pmos_width = parameter["min_tx_size"]
            readwrite_nmos_width = 1.5*parameter["min_tx_size"]
            write_nmos_width = parameter["min_tx_size"]
            read_nmos_width = 2*parameter["min_tx_size"]
        
        # if there are no read/write ports, then the inverter nmos is sized for the dual port case
        else:
            inverter_nmos_width = 2*parameter["min_tx_size"]
            inverter_pmos_width = parameter["min_tx_size"]
            readwrite_nmos_width = 1.5*parameter["min_tx_size"]
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
        
        # create ptx for readwrite transitors
        self.readwrite_nmos = ptx(width=readwrite_nmos_width,
                              tx_type="nmos")
        self.add_mod(self.readwrite_nmos)
        
        # create ptx for write transitors
        self.write_nmos = ptx(width=write_nmos_width,
                              tx_type="nmos")
        self.add_mod(self.write_nmos)
        
        # create ptx for read transistors
        self.read_nmos = ptx(width=read_nmos_width,
                             tx_type="nmos")
        self.add_mod(self.read_nmos)
    
    def calculate_spacing(self):        
        """ Calculate transistor spacings """
        
        # calculate metal contact extensions over transistor active
        self.inverter_pmos_contact_extension = 0.5*(self.inverter_pmos.active_contact.height - self.inverter_pmos.active_height)
        self.readwrite_nmos_contact_extension = 0.5*(self.readwrite_nmos.active_contact.height - self.readwrite_nmos.active_height)
        self.write_nmos_contact_extension = 0.5*(self.write_nmos.active_contact.height - self.write_nmos.active_height)
        self.read_nmos_contact_extension = 0.5*(self.read_nmos.active_contact.height - self.read_nmos.active_height)
        
        # calculate the distance threshold for different gate contact spacings
        self.gate_contact_thres = drc["poly_to_active"] - drc["minwidth_metal2"]
        
        #calculations for horizontal transistor to tansistor spacing
        # inverter spacings
        self.inverter_to_inverter_spacing = contact.poly.height + drc["minwidth_metal1"]
        self.inverter_to_write_spacing = drc["pwell_to_nwell"] + 2*drc["well_enclosure_active"]
        
        # readwrite to readwrite transistor spacing (also acts as readwrite to write transistor spacing)
        if(self.readwrite_nmos_contact_extension > self.gate_contact_thres):
            self.readwrite_to_readwrite_spacing = drc["minwidth_metal2"] + self.readwrite_nmos_contact_extension + contact.poly.width + drc["poly_to_polycontact"] + drc["poly_extend_active"]
        else:
            self.readwrite_to_readwrite_spacing = drc["poly_to_active"] + contact.poly.width + drc["poly_to_polycontact"] + drc["poly_extend_active"]
        
        # write to write transistor spacing
        if(self.write_nmos_contact_extension > self.gate_contact_thres):
            self.write_to_write_spacing = drc["minwidth_metal2"] + self.write_nmos_contact_extension + contact.poly.width + drc["poly_to_polycontact"] + drc["poly_extend_active"]
        else:
            self.write_to_write_spacing = drc["poly_to_active"] + contact.poly.width + drc["poly_to_polycontact"] + drc["poly_extend_active"]
        
        # read to read transistor spacing
        if(self.read_nmos_contact_extension > self.gate_contact_thres):
            self.read_to_read_spacing = 2*(drc["minwidth_metal2"] + self.read_nmos_contact_extension) + drc["minwidth_metal1"] + 2*contact.poly.width
        else:
            self.read_to_read_spacing = 2*drc["poly_to_active"] + drc["minwidth_metal1"] + 2*contact.poly.width
        
        # write to read transistor spacing (also acts as readwrite to read transistor spacing)
        # calculation is dependent on whether the read transistor is adjacent to a write transistor or a readwrite transistor
        if(self.num_w_ports > 0):
            if(self.write_nmos_contact_extension > self.gate_contact_thres):
                write_portion = drc["minwidth_metal2"] + self.write_nmos_contact_extension
            else:
                write_portion = drc["poly_to_active"]
        else:
            if(self.readwrite_nmos_contact_extension > self.gate_contact_thres):
                write_portion = drc["minwidth_metal2"] + self.readwrite_nmos_contact_extension
            else:
                write_portion = drc["poly_to_active"]
        
        if(self.read_nmos_contact_extension > self.gate_contact_thres):
            read_portion = drc["minwidth_metal2"] + self.read_nmos_contact_extension
        else:
            read_portion = drc["poly_to_active"]
            
        self.write_to_read_spacing = write_portion + read_portion + 2*contact.poly.width + drc["poly_to_polycontact"]
        
        """ calculations for transistor tiling (transistor + spacing) """
        self.inverter_tile_width = self.inverter_nmos.active_width + 0.5*self.inverter_to_inverter_spacing
        self.readwrite_tile_width = self.readwrite_to_readwrite_spacing + self.readwrite_nmos.active_height
        self.write_tile_width = self.write_to_write_spacing + self.write_nmos.active_height
        self.read_tile_width = self.read_to_read_spacing + self.read_nmos.active_height
        
        """ calculation for row line tiling """
        self.rail_tile_height = drc["active_to_body_active"] + contact.well.width #0.5*(drc["minwidth_tx"] - drc["minwidth_metal1"]) + drc["minwidth_metal1"]
        self.rowline_tile_height = drc["minwidth_metal1"] + contact.m1m2.width
        
        """ calculations related to inverter connections """
        self.inverter_gap = drc["poly_to_active"] + drc["poly_to_polycontact"] + 2*contact.poly.width + drc["minwidth_metal1"] + self.inverter_pmos_contact_extension
        self.cross_couple_lower_ypos = self.inverter_nmos.active_height + drc["poly_to_active"] + 0.5*contact.poly.width
        self.cross_couple_upper_ypos = self.inverter_nmos.active_height + drc["poly_to_active"] + drc["poly_to_polycontact"] + 1.5*contact.poly.width
        
    
    def calculate_postions(self):
        """ 
        Calculate positions that describe the edges of the cell 
        """
        # create flags for excluding readwrite, write, or read port calculations if they are not included in the bitcell
        if(self.num_rw_ports > 0):
            self.readwrite_port_flag = True
        else:
            self.readwrite_port_flag = False
        
        if(self.num_w_ports > 0):
            self.write_port_flag = True
        else:
            self.write_port_flag = False
            
        if(self.num_r_ports > 0):
            self.read_port_flag = True
        else:
            self.read_port_flag = False
            
        # determine the distance of the leftmost/rightmost transistor gate connection
        if (self.num_r_ports > 0):
            if(self.read_nmos_contact_extension > self.gate_contact_thres):
                end_connection = drc["minwidth_metal2"] + self.read_nmos_contact_extension + contact.m1m2.height
            else:
                end_connection = drc["poly_to_active"] + contact.m1m2.height
        else:
            if(self.readwrite_nmos_contact_extension > self.gate_contact_thres):
                end_connection = drc["minwidth_metal2"] + self.readwrite_nmos_contact_extension + contact.m1m2.height
            else:
                end_connection = drc["poly_to_active"] + contact.m1m2.height
            
        # leftmost position = storage width + read/write ports width + write ports width + read ports width + end transistor gate connections + metal spacing necessary for tiling the bitcell
        self.leftmost_xpos = -self.inverter_tile_width \
                             - self.inverter_to_write_spacing \
                             - self.readwrite_port_flag*(self.readwrite_nmos.active_height + (self.num_rw_ports-1)*self.readwrite_tile_width) \
                             - self.write_port_flag*self.readwrite_port_flag*self.write_to_write_spacing \
                             - self.write_port_flag*(self.write_nmos.active_height + (self.num_w_ports-1)*self.write_tile_width) \
                             - self.read_port_flag*self.write_to_read_spacing \
                             - self.read_port_flag*(self.read_nmos.active_height + (self.num_r_ports-1)*self.read_tile_width) \
                             - end_connection \
                             - 0.5*drc["poly_to_polycontact"]
                             
        self.rightmost_xpos = -self.leftmost_xpos
        
        # bottommost position = gnd height + rwwl height + wwl height + rwl height + space needed between tiled bitcells
        array_tiling_offset = 0.5*drc["minwidth_metal2"]
        self.botmost_ypos = -self.rail_tile_height \
                            - self.num_rw_ports*self.rowline_tile_height \
                            - self.num_w_ports*self.rowline_tile_height \
                            - self.num_r_ports*self.rowline_tile_height \
                            - array_tiling_offset
                            
        # topmost position = height of the inverter + height of vdd
        self.topmost_ypos = self.inverter_nmos.active_height + self.inverter_gap + self.inverter_pmos.active_height \
                            + self.rail_tile_height
        
        # calculations for the cell dimensions
        array_vdd_overlap = 0.5*contact.well.width
        self.width = -2*self.leftmost_xpos
        self.height = self.topmost_ypos - self.botmost_ypos - array_vdd_overlap


    def create_storage(self):
        """
        Creates the crossed coupled inverters that act as storage for the bitcell.
        The stored value of the cell is denoted as "Q", and the inverted value as "Q_bar".
        """
        
        # create active for nmos
        self.inverter_nmos_left = self.add_inst(name="inverter_nmos_left",
                                                mod=self.inverter_nmos)
        self.connect_inst(["Q_bar", "Q", "gnd", "gnd"])
        
        self.inverter_nmos_right = self.add_inst(name="inverter_nmos_right",
                                                 mod=self.inverter_nmos)
        self.connect_inst(["gnd", "Q_bar", "Q", "gnd"])
        
        # create active for pmos
        self.inverter_pmos_left = self.add_inst(name="inverter_pmos_left",
                                                mod=self.inverter_pmos)
        self.connect_inst(["Q_bar", "Q", "vdd", "vdd"])
        
        self.inverter_pmos_right = self.add_inst(name="inverter_pmos_right",
                                                 mod=self.inverter_pmos)
        self.connect_inst(["vdd", "Q_bar", "Q", "vdd"])
        
        
    def place_storage(self):
        """
        Places the crossed coupled inverters that act as storage for the bitcell.
        The stored value of the cell is denoted as "Q", and the inverted value as "Q_bar".
        """
        
        # calculate transistor offsets
        left_inverter_xpos = -0.5*self.inverter_to_inverter_spacing - self.inverter_nmos.active_width
        right_inverter_xpos = 0.5*self.inverter_to_inverter_spacing
        inverter_pmos_ypos = self.inverter_nmos.active_height + self.inverter_gap
                
        # create active for nmos
        self.inverter_nmos_left.place([left_inverter_xpos,0])
        self.inverter_nmos_right.place([right_inverter_xpos,0])
        
        # create active for pmos
        self.inverter_pmos_left.place([left_inverter_xpos, inverter_pmos_ypos])
        self.inverter_pmos_right.place([right_inverter_xpos, inverter_pmos_ypos])

    def route_storage(self):
        
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
                                           
        # connect contacts to gate poly (cross couple connections)
        gate_offset_right = vector(self.inverter_nmos_right.get_pin("G").lc().x, contact_offset_left.y)
        self.add_path("poly", [contact_offset_left, gate_offset_right])
        
        gate_offset_left = vector(self.inverter_nmos_left.get_pin("G").rc().x, contact_offset_right.y)
        self.add_path("poly", [contact_offset_right, gate_offset_left])
        
        # update furthest left and right transistor edges (this will propagate to further transistor offset calculations)
        self.left_building_edge = -self.inverter_tile_width
        self.right_building_edge = self.inverter_tile_width
        
        
    def route_rails(self):
        """
        Add gnd and vdd rails and connects them to the inverters
        """
        
        # Add rails for vdd and gnd
        self.gnd_position = vector(self.leftmost_xpos, -self.rail_tile_height)
        self.gnd = self.add_layout_pin(text="gnd",
                                       layer="metal1",
                                       offset=self.gnd_position,
                                       width=self.width,
                                       height=contact.well.second_layer_width)
        
        vdd_ypos = self.inverter_nmos.active_height + self.inverter_gap + self.inverter_pmos.active_height \
                   + drc["active_to_body_active"] + 0.5*(drc["minwidth_tx"] - drc["minwidth_metal1"])
        self.vdd_position = vector(self.leftmost_xpos, vdd_ypos)
        self.vdd = self.add_layout_pin(text="vdd",
                                       layer="metal1",
                                       offset=self.vdd_position,
                                       width=self.width,
                                       height=drc["minwidth_metal1"])
                
        # Connect inverters to rails 
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


    def create_readwrite_ports(self):
        """
        Creates read/write ports to the bit cell. A differential pair of transistor can both read and write, like in a 6T cell.
        A read or write is enabled by setting a Read-Write-Wordline (RWWL) high, subsequently turning on the transistor.
        The transistor is connected between a Read-Write-Bitline (RWBL) and the storage component of the cell (Q). 
        In a write operation, driving RWBL high or low sets the value of the cell.
        In a read operation, RWBL is precharged, then is either remains high or is discharged depending on the value of the cell.
        This is a differential design, so each write port has a mirrored port that connects RWBL_bar to Q_bar.
        """
    
        # define write transistor variables as empty arrays based on the number of write ports
        self.readwrite_nmos_left = [None] * self.num_rw_ports 
        self.readwrite_nmos_right = [None] * self.num_rw_ports
        
        # iterate over the number of read/write ports
        for k in range(0,self.num_rw_ports):
            # add read/write transistors
            self.readwrite_nmos_left[k] = self.add_inst(name="readwrite_nmos_left{}".format(k),
                                                        mod=self.readwrite_nmos)
            self.connect_inst(["Q", "rwwl{}".format(k), "rwbl{}".format(k), "gnd"])
            
            self.readwrite_nmos_right[k] = self.add_inst(name="readwrite_nmos_right{}".format(k),
                                                         mod=self.readwrite_nmos)
            self.connect_inst(["Q_bar", "rwwl{}".format(k), "rwbl_bar{}".format(k), "gnd"])
                        

    def place_readwrite_ports(self):
        """
        Places read/write ports in the bit cell. 
        """
    
        # Define variables relevant to write transistors
        self.rwwl_positions = [None] * self.num_rw_ports
        self.rwbl_positions = [None] * self.num_rw_ports
        self.rwbl_bar_positions = [None] * self.num_rw_ports    
        
        # define offset correction due to rotation of the ptx module
        readwrite_rotation_correct = self.readwrite_nmos.active_height
        
        # iterate over the number of read/write ports
        for k in range(0,self.num_rw_ports):
            # Add transistors
            # calculate read/write transistor offsets 
            left_readwrite_transistor_xpos = self.left_building_edge \
                                             - self.inverter_to_write_spacing \
                                             - self.readwrite_nmos.active_height - k*self.readwrite_tile_width \
                                             + readwrite_rotation_correct
            
            right_readwrite_transistor_xpos = self.right_building_edge \
                                              + self.inverter_to_write_spacing \
                                              + k*self.readwrite_tile_width \
                                              + readwrite_rotation_correct
            
            # add read/write transistors
            self.readwrite_nmos_left[k].place(offset=[left_readwrite_transistor_xpos,0],
                                              rotate=90)
            
            self.readwrite_nmos_right[k].place(offset=[right_readwrite_transistor_xpos,0],
                                               rotate=90)
                        
            # Add RWWL lines 
            # calculate RWWL position
            rwwl_ypos = self.gnd_position.y - (k+1)*self.rowline_tile_height 
            self.rwwl_positions[k] = vector(self.leftmost_xpos, rwwl_ypos)
            
            # add pin for RWWL
            self.add_layout_pin(text="rwwl{}".format(k),
                                layer="metal1",
                                offset=self.rwwl_positions[k],
                                width=self.width,
                                height=contact.m1m2.width)
                       
            # Source/RWBL/RWBL_bar connections 
            # add metal1-to-metal2 contacts on top of read/write transistor source pins for connection to WBL and WBL_bar
            offset_left = self.readwrite_nmos_left[k].get_pin("S").center()
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=offset_left,
                                    rotate=90)
            
            offset_right = self.readwrite_nmos_right[k].get_pin("S").center()
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=offset_right,
                                    rotate=90)
            
            # add pins for RWBL and RWBL_bar, overlaid on source contacts
            self.rwbl_positions[k] = vector(self.readwrite_nmos_left[k].get_pin("S").center().x - 0.5*drc["minwidth_metal2"], self.botmost_ypos)
            self.add_layout_pin(text="rwbl{}".format(k),
                                layer="metal2",
                                offset=self.rwbl_positions[k],
                                width=drc["minwidth_metal2"],
                                height=self.height)

            self.rwbl_bar_positions[k] = vector(self.readwrite_nmos_right[k].get_pin("S").center().x - 0.5*drc["minwidth_metal2"], self.botmost_ypos)
            self.add_layout_pin(text="rwbl_bar{}".format(k),
                                layer="metal2",
                                offset=self.rwbl_bar_positions[k],
                                width=drc["minwidth_metal2"],
                                height=self.height)
                        
            # Gate/RWWL connections 
            # add poly-to-meltal2 contacts to connect gate of read/write transistors to RWWL (contact next to gate)
            # contact must be placed a metal1 width below the source pin to avoid drc from source pin routings
            if(self.readwrite_nmos_contact_extension > self.gate_contact_thres):
                contact_xpos = self.readwrite_nmos_left[k].get_pin("S").lc().x - drc["minwidth_metal2"] - 0.5*contact.m1m2.width
            else:
                contact_xpos = left_readwrite_transistor_xpos - self.readwrite_nmos.active_height - drc["poly_to_active"] - 0.5*contact.poly.width
            contact_ypos = self.readwrite_nmos_left[k].get_pin("D").bc().y - drc["minwidth_metal1"] - 0.5*contact.m1m2.height
            left_gate_contact =  vector(contact_xpos, contact_ypos)
            
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=left_gate_contact)            
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=left_gate_contact)            
            
            if(self.readwrite_nmos_contact_extension > self.gate_contact_thres):
                contact_xpos = self.readwrite_nmos_right[k].get_pin("S").rc().x + drc["minwidth_metal2"] + 0.5*contact.m1m2.width
            else:
                contact_xpos = right_readwrite_transistor_xpos + drc["poly_to_active"] + 0.5*contact.poly.width
            contact_ypos = self.readwrite_nmos_right[k].get_pin("D").bc().y - drc["minwidth_metal1"] - 0.5*contact.m1m2.height
            right_gate_contact = vector(contact_xpos, contact_ypos)
            
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=right_gate_contact)            
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=right_gate_contact)
            
            # connect gate of read/write transistor to contact (poly path)
            midL = vector(left_gate_contact.x, self.readwrite_nmos_left[k].get_pin("G").lc().y)
            self.add_path("poly", [self.readwrite_nmos_left[k].get_pin("G").lc(), midL, left_gate_contact], width=contact.poly.width)
            
            midR = vector(right_gate_contact.x, self.readwrite_nmos_right[k].get_pin("G").rc().y) 
            self.add_path("poly", [self.readwrite_nmos_right[k].get_pin("G").rc(), midR, right_gate_contact], width=contact.poly.width)
            
            # add metal1-to-metal2 contacts to RWWL lines
            left_rwwl_contact = vector(left_gate_contact.x, self.rwwl_positions[k].y + 0.5*contact.m1m2.width)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                            offset=left_rwwl_contact,
                                            rotate=90)
                             
            right_rwwl_contact = vector(right_gate_contact.x, self.rwwl_positions[k].y + 0.5*contact.m1m2.width)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                            offset=right_rwwl_contact,
                                            rotate=90)
            
            # connect read/write transistor gate contacts to RWWL contacts (metal2 path)
            self.add_path("metal2", [left_gate_contact, left_rwwl_contact])
            self.add_path("metal2", [right_gate_contact, right_rwwl_contact])
                       
            # Drain/Storage connections 
            # this path only needs to be drawn once on the last iteration of the loop
            if(k == self.num_rw_ports-1):
                # add contacts to connect gate of inverters to drain of read/write transistors
                left_storage_contact =  vector(self.inverter_nmos_left.get_pin("G").lc().x - drc["poly_to_polycontact"] - 0.5*contact.poly.width, self.cross_couple_lower_ypos)
                self.add_contact_center(layers=("poly", "contact", "metal1"),
                                                offset=left_storage_contact,
                                                rotate=90)
                
                right_storage_contact =  vector(self.inverter_nmos_right.get_pin("G").rc().x + drc["poly_to_polycontact"] + 0.5*contact.poly.width, self.cross_couple_lower_ypos)
                self.add_contact_center(layers=("poly", "contact", "metal1"),
                                                offset=right_storage_contact,
                                                rotate=90)
                                 
                # connect gate of inverters to contacts (poly path)
                inverter_gate_offset_left = vector(self.inverter_nmos_left.get_pin("G").lc().x, self.cross_couple_lower_ypos)
                self.add_path("poly", [left_storage_contact, inverter_gate_offset_left])
                
                inverter_gate_offset_right = vector(self.inverter_nmos_right.get_pin("G").rc().x, self.cross_couple_lower_ypos)
                self.add_path("poly", [right_storage_contact, inverter_gate_offset_right])
                
                # connect contacts to drains of read/write transistors (metal1 path)
                midL0 = vector(self.inverter_nmos_left.get_pin("S").lc().x - 1.5*drc["minwidth_metal1"], left_storage_contact.y)
                midL1 = vector(self.inverter_nmos_left.get_pin("S").lc().x - 1.5*drc["minwidth_metal1"], self.readwrite_nmos_left[k].get_pin("D").lc().y)
                self.add_path("metal1", [left_storage_contact, midL0], width=contact.poly.second_layer_width) # width needed to avoid drc error
                self.add_path("metal1", [midL0+vector(0,0.5*contact.poly.second_layer_width), midL1, self.readwrite_nmos_left[k].get_pin("D").lc()])
                
                midR0 = vector(self.inverter_nmos_right.get_pin("D").rc().x + 1.5*drc["minwidth_metal1"], right_storage_contact.y)
                midR1 = vector(self.inverter_nmos_right.get_pin("D").rc().x + 1.5*drc["minwidth_metal1"], self.readwrite_nmos_right[k].get_pin("D").rc().y)
                self.add_path("metal1", [right_storage_contact, midR0], width=contact.poly.second_layer_width)
                self.add_path("metal1", [midR0+vector(0,0.5*contact.poly.second_layer_width), midR1, self.readwrite_nmos_right[k].get_pin("D").rc()])
            # end if
        # end for
        
        # update furthest left and right transistor edges 
        self.left_building_edge = left_readwrite_transistor_xpos - self.readwrite_nmos.active_height
        self.right_building_edge = right_readwrite_transistor_xpos
        
    
    def create_write_ports(self):
        """
        Creates write ports in the bit cell. A differential pair of transistors can write only.
        A write is enabled by setting a Write-Rowline (WWL) high, subsequently turning on the transistor.
        The transistor is connected between a Write-Bitline (WBL) and the storage component of the cell (Q). 
        In a write operation, driving WBL high or low sets the value of the cell.
        This is a differential design, so each write port has a mirrored port that connects WBL_bar to Q_bar.
        """
    
        # Define variables relevant to write transistors
        # define offset correction due to rotation of the ptx module
        write_rotation_correct = self.write_nmos.active_height
        
        # define write transistor variables as empty arrays based on the number of write ports
        self.write_nmos_left = [None] * self.num_w_ports 
        self.write_nmos_right = [None] * self.num_w_ports
        
        # iterate over the number of write ports
        for k in range(0,self.num_w_ports):
            # add write transistors
            self.write_nmos_left[k] = self.add_inst(name="write_nmos_left{}".format(k),
                                                    mod=self.write_nmos)
            self.connect_inst(["Q", "wwl{}".format(k), "wbl{}".format(k), "gnd"])
            
            self.write_nmos_right[k] = self.add_inst(name="write_nmos_right{}".format(k),
                                                     mod=self.write_nmos)
            self.connect_inst(["Q_bar", "wwl{}".format(k), "wbl_bar{}".format(k), "gnd"])
                        

    def place_write_ports(self):
        """
        Places write ports in the bit cell. 
        """
    
        # Define variables relevant to write transistors 
        self.wwl_positions = [None] * self.num_w_ports
        self.wbl_positions = [None] * self.num_w_ports
        self.wbl_bar_positions = [None] * self.num_w_ports       

        # define offset correction due to rotation of the ptx module
        write_rotation_correct = self.write_nmos.active_height
        
        # iterate over the number of write ports
        for k in range(0,self.num_w_ports):
            # Add transistors
            # calculate write transistor offsets 
            left_write_transistor_xpos = self.left_building_edge \
                                         - (not self.readwrite_port_flag)*self.inverter_to_write_spacing \
                                         - (self.readwrite_port_flag)*self.readwrite_to_readwrite_spacing \
                                         - self.write_nmos.active_height - k*self.write_tile_width \
                                         + write_rotation_correct
            
            right_write_transistor_xpos = self.right_building_edge \
                                          + (not self.readwrite_port_flag)*self.inverter_to_write_spacing \
                                          + (self.readwrite_port_flag)*self.readwrite_to_readwrite_spacing \
                                          + k*self.write_tile_width \
                                          + write_rotation_correct
            
            # add write transistors
            self.write_nmos_left[k].place(offset=[left_write_transistor_xpos,0],
                                          rotate=90)
            
            self.write_nmos_right[k].place(offset=[right_write_transistor_xpos,0],
                                           rotate=90)
                        
            # Add WWL lines 
            # calculate WWL position
            wwl_ypos = self.gnd_position.y \
                       - self.num_rw_ports*self.rowline_tile_height \
                       - (k+1)*self.rowline_tile_height 
            self.wwl_positions[k] = vector(self.leftmost_xpos, wwl_ypos)
            
            # add pin for WWL
            self.add_layout_pin(text="wwl{}".format(k),
                                layer="metal1",
                                offset=self.wwl_positions[k],
                                width=self.width,
                                height=contact.m1m2.width)
                       
            # Source/WBL/WBL_bar connections 
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
                        
            # Gate/WWL connections
            # add poly-to-meltal2 contacts to connect gate of write transistors to WWL (contact next to gate)
            # contact must be placed a metal width below the source pin to avoid drc from source pin routings
            if(self.write_nmos_contact_extension > self.gate_contact_thres):
                contact_xpos = self.write_nmos_left[k].get_pin("S").lc().x - drc["minwidth_metal2"] - 0.5*contact.m1m2.width
            else:
                contact_xpos = left_write_transistor_xpos - self.write_nmos.active_height - drc["poly_to_active"] - 0.5*contact.poly.width
            contact_ypos = self.write_nmos_left[k].get_pin("D").bc().y - drc["minwidth_metal1"] - 0.5*contact.m1m2.height
            left_gate_contact =  vector(contact_xpos, contact_ypos)
            
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=left_gate_contact)            
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=left_gate_contact)            
            
            if(self.write_nmos_contact_extension > self.gate_contact_thres):
                contact_xpos = self.write_nmos_right[k].get_pin("S").rc().x + drc["minwidth_metal2"] + 0.5*contact.m1m2.width
            else:
                contact_xpos = right_write_transistor_xpos + drc["poly_to_active"] + 0.5*contact.poly.width
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
            
            # add metal1-to-metal2 contacts to WWL lines
            left_wwl_contact = vector(left_gate_contact.x, self.wwl_positions[k].y + 0.5*contact.m1m2.width)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                            offset=left_wwl_contact,
                                            rotate=90)
                             
            right_wwl_contact = vector(right_gate_contact.x, self.wwl_positions[k].y + 0.5*contact.m1m2.width)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                            offset=right_wwl_contact,
                                            rotate=90)
            
            # connect write transistor gate contacts to WWL contacts (metal2 path)
            self.add_path("metal2", [left_gate_contact, left_wwl_contact])
            self.add_path("metal2", [right_gate_contact, right_wwl_contact])
                       
            # Drain/Storage connections 
            # this path only needs to be drawn once on the last iteration of the loop
            if(k == self.num_w_ports-1):
                # add contacts to connect gate of inverters to drain of write transistors
                left_storage_contact =  vector(self.inverter_nmos_left.get_pin("G").lc().x - drc["poly_to_polycontact"] - 0.5*contact.poly.width, self.cross_couple_lower_ypos)
                self.add_contact_center(layers=("poly", "contact", "metal1"),
                                                offset=left_storage_contact,
                                                rotate=90)
                
                right_storage_contact =  vector(self.inverter_nmos_right.get_pin("G").rc().x + drc["poly_to_polycontact"] + 0.5*contact.poly.width, self.cross_couple_lower_ypos)
                self.add_contact_center(layers=("poly", "contact", "metal1"),
                                                offset=right_storage_contact,
                                                rotate=90)
                                 
                # connect gate of inverters to contacts (poly path)
                inverter_gate_offset_left = vector(self.inverter_nmos_left.get_pin("G").lc().x, self.cross_couple_lower_ypos)
                self.add_path("poly", [left_storage_contact, inverter_gate_offset_left])
                
                inverter_gate_offset_right = vector(self.inverter_nmos_right.get_pin("G").rc().x, self.cross_couple_lower_ypos)
                self.add_path("poly", [right_storage_contact, inverter_gate_offset_right])
                
                # connect contacts to drains of write transistors (metal1 path)
                midL0 = vector(self.inverter_nmos_left.get_pin("S").lc().x - 1.5*drc["minwidth_metal1"], left_storage_contact.y)
                midL1 = vector(self.inverter_nmos_left.get_pin("S").lc().x - 1.5*drc["minwidth_metal1"], self.write_nmos_left[k].get_pin("D").lc().y)
                self.add_path("metal1", [left_storage_contact, midL0], width=contact.poly.second_layer_width) # width needed to avoid drc error
                self.add_path("metal1", [midL0+vector(0,0.5*contact.poly.second_layer_width), midL1, self.write_nmos_left[k].get_pin("D").lc()])
                
                midR0 = vector(self.inverter_nmos_right.get_pin("D").rc().x + 1.5*drc["minwidth_metal1"], right_storage_contact.y)
                midR1 = vector(self.inverter_nmos_right.get_pin("D").rc().x + 1.5*drc["minwidth_metal1"], self.write_nmos_right[k].get_pin("D").rc().y)
                self.add_path("metal1", [right_storage_contact, midR0], width=contact.poly.second_layer_width)
                self.add_path("metal1", [midR0+vector(0,0.5*contact.poly.second_layer_width), midR1, self.write_nmos_right[k].get_pin("D").rc()])
        
        # update furthest left and right transistor edges 
        self.left_building_edge = left_write_transistor_xpos - self.write_nmos.active_height
        self.right_building_edge = right_write_transistor_xpos

                
    def create_read_ports(self):
        """
        Creates read ports in the bit cell. A differential pair of ports can read only. 
        Two transistors function as a read port, denoted as the "read transistor" and the "read-access transistor".
        The read transistor is connected to RWL (gate), RBL (drain), and the read-access transistor (source).
        The read-access transistor is connected to Q_bar (gate), gnd (source), and the read transistor (drain).
        A read is enabled by setting a Read-Rowline (RWL) high, subsequently turning on the read transistor.
        The Read-Bitline (RBL) is precharged to high, and when the value of Q_bar is high, the read-access transistor
        is turned on, creating a connection between RBL and gnd. RBL subsequently discharges allowing for a differential read
        using sense amps. This is a differential design, so each read port has a mirrored port that connects RBL_bar to Q.
        """
        
        # define read transistor variables as empty arrays based on the number of read ports
        self.read_nmos_left = [None] * self.num_r_ports 
        self.read_nmos_right = [None] * self.num_r_ports
        self.read_access_nmos_left = [None] * self.num_r_ports 
        self.read_access_nmos_right = [None] * self.num_r_ports
        
        # iterate over the number of read ports
        for k in range(0,self.num_r_ports):
            # add read-access transistors
            self.read_access_nmos_left[k] = self.add_inst(name="read_access_nmos_left{}".format(k),
                                                          mod=self.read_nmos)
            self.connect_inst(["RA_to_R_left{}".format(k), " Q_bar", "gnd", "gnd"])
            
            self.read_access_nmos_right[k] = self.add_inst(name="read_access_nmos_right{}".format(k),
                                                           mod=self.read_nmos)
            self.connect_inst(["RA_to_R_right{}".format(k), "Q", "gnd", "gnd"])
            
            # add read transistors
            self.read_nmos_left[k] = self.add_inst(name="read_nmos_left{}".format(k),
                                                   mod=self.read_nmos)
            self.connect_inst(["rbl{}".format(k), "rwl{}".format(k), "RA_to_R_left{}".format(k), "gnd"])
            
            self.read_nmos_right[k] = self.add_inst(name="read_nmos_right{}".format(k),
                                                    mod=self.read_nmos)
            self.connect_inst(["rbl_bar{}".format(k), "rwl{}".format(k), "RA_to_R_right{}".format(k), "gnd"])
                        
    def place_read_ports(self):
        """
        Places the read ports in the bit cell. 
        """
        
        # Define variables relevant to read transistors
        self.rwl_positions = [None] * self.num_r_ports
        self.rbl_positions = [None] * self.num_r_ports
        self.rbl_bar_positions = [None] * self.num_r_ports
        
        # define offset correction due to rotation of the ptx module
        read_rotation_correct = self.read_nmos.active_height
        
        # calculate offset to overlap the drain of the read-access transistor with the source of the read transistor
        overlap_offset = self.read_nmos.get_pin("D").ll() - self.read_nmos.get_pin("S").ll()
        
        # iterate over the number of read ports
        for k in range(0,self.num_r_ports):
            # Add transistors 
            # calculate transistor offsets
            left_read_transistor_xpos = self.left_building_edge \
                                        - self.write_to_read_spacing \
                                        - self.read_nmos.active_height - k*self.read_tile_width \
                                        + read_rotation_correct
                       
            right_read_transistor_xpos = self.right_building_edge \
                                         + self.write_to_read_spacing \
                                         + k*self.read_tile_width \
                                         + read_rotation_correct          
            
            # add read-access transistors
            self.read_access_nmos_left[k].place(offset=[left_read_transistor_xpos,0],
                                                rotate=90)
            
            self.read_access_nmos_right[k].place(offset=[right_read_transistor_xpos,0],
                                                 rotate=90)
            
            # add read transistors
            self.read_nmos_left[k].place(offset=[left_read_transistor_xpos,overlap_offset.x],
                                         rotate=90)
            
            self.read_nmos_right[k].place(offset=[right_read_transistor_xpos,overlap_offset.x],
                                          rotate=90)
                        
            # Add RWL lines 
            # calculate RWL position
            rwl_ypos = self.gnd_position.y \
                        - self.num_rw_ports*self.rowline_tile_height \
                        - self.num_w_ports*self.rowline_tile_height \
                        - (k+1)*self.rowline_tile_height            
            self.rwl_positions[k] = vector(self.leftmost_xpos, rwl_ypos)
            
            # add pin for RWL
            self.add_layout_pin(text="rwl{}".format(k),
                                layer="metal1",
                                offset=self.rwl_positions[k],
                                width=self.width,
                                height=contact.m1m2.width)
                       
            # Drain of read transistor / RBL & RBL_bar connection 
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
                       
            # Gate of read transistor / RWL connection 
            # add poly-to-meltal2 contacts to connect gate of read transistors to RWL (contact next to gate)
            if(self.read_nmos_contact_extension > self.gate_contact_thres):
                contact_xpos = self.read_nmos_left[k].get_pin("S").lc().x - drc["minwidth_metal2"] - 0.5*contact.m1m2.width
            else:
                contact_xpos = left_read_transistor_xpos - self.read_nmos.active_height - drc["poly_to_active"] - 0.5*contact.poly.width
            contact_ypos = self.read_nmos_left[k].get_pin("G").lc().y
            left_gate_contact = vector(contact_xpos, contact_ypos)
            
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=left_gate_contact)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=left_gate_contact)
            
            if(self.read_nmos_contact_extension > self.gate_contact_thres):
                contact_xpos = self.read_nmos_right[k].get_pin("S").rc().x + drc["minwidth_metal2"] + 0.5*contact.m1m2.width
            else:
                contact_xpos = right_read_transistor_xpos + drc["poly_to_active"] + 0.5*contact.poly.width
            contact_ypos = self.read_nmos_right[k].get_pin("G").rc().y
            right_gate_contact = vector(contact_xpos, contact_ypos)
            
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=right_gate_contact)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=right_gate_contact)
            
            # connect gate of read transistor to contact (poly path)
            self.add_path("poly", [self.read_nmos_left[k].get_pin("G").lc(), left_gate_contact])         
            self.add_path("poly", [self.read_nmos_right[k].get_pin("G").rc(), right_gate_contact])
            
            # add metal1-to-metal2 contacts to RWL lines
            left_rwl_contact = vector(left_gate_contact.x, self.rwl_positions[k].y + 0.5*contact.poly.width)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=left_rwl_contact,
                                    rotate=90)
                                                            
            right_rwl_contact = vector(right_gate_contact.x, self.rwl_positions[k].y + 0.5*contact.poly.width)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=right_rwl_contact,
                                    rotate=90)
            
            # connect read transistor gate contacts to RWL contacts (metal2 path)
            self.add_path("metal2", [left_gate_contact, left_rwl_contact])
            self.add_path("metal2", [right_gate_contact, right_rwl_contact])
            
            # Source of read-access transistor / GND connection 
            # connect source of read-access transistor to GND (metal1 path)
            gnd_offset_left = vector(self.read_access_nmos_left[k].get_pin("S").bc().x, self.gnd_position.y)
            self.add_path("metal1", [self.read_access_nmos_left[k].get_pin("S").bc(), gnd_offset_left])
            
            gnd_offset_right = vector(self.read_access_nmos_right[k].get_pin("S").bc().x, self.gnd_position.y)
            self.add_path("metal1", [self.read_access_nmos_right[k].get_pin("S").bc(), gnd_offset_right])
            
            # Gate of read-access transistor / storage connection 
            # add poly-to-metal1 contacts to connect gate of read-access transistors to output of inverters (contact next to gate)
            if(self.read_nmos_contact_extension > self.gate_contact_thres):
                contact_xpos = self.read_nmos_left[k].get_pin("S").rc().x + drc["minwidth_metal2"] + 0.5*contact.m1m2.width
            else:
                contact_xpos = left_read_transistor_xpos + drc["poly_to_active"] + 0.5*contact.poly.width
            contact_ypos = self.read_access_nmos_left[k].get_pin("G").rc().y
            left_gate_contact = vector(contact_xpos, contact_ypos)
            
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=left_gate_contact)
            
            if(self.read_nmos_contact_extension > self.gate_contact_thres):
                contact_xpos = self.read_nmos_right[k].get_pin("S").lc().x - drc["minwidth_metal2"] - 0.5*contact.m1m2.width
            else:
                contact_xpos = right_read_transistor_xpos - self.read_nmos.active_height - drc["poly_to_active"] - 0.5*contact.poly.width
            contact_ypos = self.read_access_nmos_right[k].get_pin("G").lc().y
            right_gate_contact = vector(contact_xpos, contact_ypos)
            
            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=right_gate_contact)
            
            # connect gate of read-access transistor to contact (poly path)
            self.add_path("poly", [self.read_access_nmos_left[k].get_pin("G").rc(), left_gate_contact])
            self.add_path("poly", [self.read_access_nmos_right[k].get_pin("G").lc(), right_gate_contact])
            
            # save the positions of the first gate contacts for use in later iterations
            if(k == 0):
                left_gate_contact0 = left_gate_contact
                right_gate_contact0 = right_gate_contact
            
            # connect contact to output of inverters (metal1 path)
            # mid0: metal1 path must route over the read transistors (above drain of read transistor)
            # mid1: continue metal1 path horizontally until at first read access gate contact
            # mid2: route up or down to be level with inverter output
            # endpoint at drain/source of inverter
            midL0 = vector(left_gate_contact.x, self.read_nmos_left[k].get_pin("D").uc().y + 1.5*drc["minwidth_metal1"])
            midL1 = vector(left_gate_contact0.x, self.read_nmos_left[0].get_pin("D").uc().y + 1.5*drc["minwidth_metal1"])
            midL2 = vector(left_gate_contact0.x, self.cross_couple_upper_ypos)
            left_inverter_offset = vector(self.inverter_nmos_left.get_pin("D").center().x, self.cross_couple_upper_ypos)
            self.add_path("metal1", [left_gate_contact, midL0, midL1, midL2, left_inverter_offset])
            
            midR0 = vector(right_gate_contact.x, self.read_nmos_right[k].get_pin("D").uc().y + 1.5*drc["minwidth_metal1"])
            midR1 = vector(right_gate_contact0.x, self.read_nmos_right[k].get_pin("D").uc().y + 1.5*drc["minwidth_metal1"])
            midR2 = vector(right_gate_contact0.x, self.cross_couple_upper_ypos)
            right_inverter_offset = vector(self.inverter_nmos_right.get_pin("S").center().x, self.cross_couple_upper_ypos)
            self.add_path("metal1", [right_gate_contact, midR0, midR1, midR2, right_inverter_offset])
        # end for
            
        
    def extend_well(self):
        """
        Connects wells between ptx modules to avoid drc spacing issues.
        Since the pwell of the read ports rise higher than the nwell of the inverters,
        the well connections must be done piecewise to avoid pwell and nwell overlap.
        """
    
        # extend pwell to encompass entire nmos region of the cell up to the height of the inverter nmos well 
        offset = vector(self.leftmost_xpos, self.botmost_ypos)
        well_height = -self.botmost_ypos + self.inverter_nmos.cell_well_height - drc["well_enclosure_active"]
        self.add_rect(layer="pwell",
                      offset=offset,
                      width=self.width,
                      height=well_height)        
        
        # extend pwell over read/write and write transistors to the
        # height of the write transistor well (read/write and write
        # transistors are the same height) 
        if(self.num_w_ports > 0):
            # calculate the edge of the write transistor well closest to the center
            left_write_well_xpos = self.write_nmos_left[0].offset.x + drc["well_enclosure_active"]
            right_write_well_xpos =  self.write_nmos_right[0].offset.x - self.write_nmos.active_height - drc["well_enclosure_active"]
        else:
            # calculate the edge of the read/write transistor well closest to the center
            left_write_well_xpos = self.readwrite_nmos_left[0].offset.x + drc["well_enclosure_active"]
            right_write_well_xpos =  self.readwrite_nmos_right[0].offset.x - self.readwrite_nmos.active_height - drc["well_enclosure_active"]    
            
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
                     
        # extend pwell over the read transistors to the height of the bitcell 
        if(self.num_r_ports > 0):
            # calculate the edge of the read transistor well clostest to the center
            left_read_well_xpos = self.read_nmos_left[0].offset.x + drc["well_enclosure_active"]
            right_read_well_xpos =  self.read_nmos_right[0].offset.x - self.read_nmos.active_height - drc["well_enclosure_active"] 
        
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
        
        # extend nwell to encompass inverter_pmos
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
        
        
        # add well contacts 
        # connect pimplants to gnd
        offset = vector(0, self.gnd_position.y + 0.5*contact.well.second_layer_width)
        self.add_contact_center(layers=("active", "contact", "metal1"),
                                offset=offset,
                                rotate=90,
                                implant_type="p",
                                well_type="p")
        
        # connect nimplants to vdd
        offset = vector(0, self.vdd_position.y + 0.5*drc["minwidth_metal1"])
        self.add_contact_center(layers=("active", "contact", "metal1"),
                                offset=offset,
                                rotate=90,
                                implant_type="n",
                                well_type="n")  
    
    
    def list_bitcell_pins(self, col, row):
        """ Creates a list of connections in the bitcell, indexed by column and row, for instance use in bitcell_array """
        bitcell_pins = []
        for k in range(self.num_rw_ports):
            bitcell_pins.append("rwbl{0}[{1}]".format(k,col))
            bitcell_pins.append("rwbl_bar{0}[{1}]".format(k,col))
        for k in range(self.num_w_ports):
            bitcell_pins.append("wbl{0}[{1}]".format(k,col))
            bitcell_pins.append("wbl_bar{0}[{1}]".format(k,col))
        for k in range(self.num_r_ports):
            bitcell_pins.append("rbl{0}[{1}]".format(k,col))
            bitcell_pins.append("rbl_bar{0}[{1}]".format(k,col))
        for k in range(self.num_rw_ports):
            bitcell_pins.append("rwwl{0}[{1}]".format(k,row))
        for k in range(self.num_w_ports):
            bitcell_pins.append("wwl{0}[{1}]".format(k,row))
        for k in range(self.num_r_ports):
            bitcell_pins.append("rwl{0}[{1}]".format(k,row))
        bitcell_pins.append("vdd")
        bitcell_pins.append("gnd")
        
        return bitcell_pins
    
    def list_all_wl_names(self):
        """ Creates a list of all wordline pin names """
        row_pins = []
        for k in range(self.num_rw_ports):
            row_pins.append("rwwl{0}".format(k))
        for k in range(self.num_w_ports):
            row_pins.append("wwl{0}".format(k))
        for k in range(self.num_r_ports):
            row_pins.append("rwl{0}".format(k))
            
        return row_pins
    
    def list_read_wl_names(self):
        """ Creates a list of wordline pin names associated with read ports """
        row_pins = []
        for k in range(self.num_rw_ports):
            row_pins.append("rwwl{0}".format(k))
        for k in range(self.num_r_ports):
            row_pins.append("rwl{0}".format(k))
            
        return row_pins
    
    def list_write_wl_names(self):
        """ Creates a list of wordline pin names associated with write ports """
        row_pins = []
        for k in range(self.num_rw_ports):
            row_pins.append("rwwl{0}".format(k))
        for k in range(self.num_w_ports):
            row_pins.append("wwl{0}".format(k))
            
        return row_pins
    
    
    def list_all_bitline_names(self):
        """ Creates a list of all bitline pin names (both bl and br) """
        column_pins = []
        for k in range(self.num_rw_ports):
            column_pins.append("rwbl{0}".format(k))
            column_pins.append("rwbl_bar{0}".format(k))
        for k in range(self.num_w_ports):
            column_pins.append("wbl{0}".format(k))
            column_pins.append("wbl_bar{0}".format(k))
        for k in range(self.num_r_ports):
            column_pins.append("rbl{0}".format(k))
            column_pins.append("rbl_bar{0}".format(k))
            
        return column_pins
        
    def list_all_bl_names(self):
        """ Creates a list of all bl pins names """
        column_pins = []
        for k in range(self.num_rw_ports):
            column_pins.append("rwbl{0}".format(k))
        for k in range(self.num_w_ports):
            column_pins.append("wbl{0}".format(k))
        for k in range(self.num_r_ports):
            column_pins.append("rbl{0}".format(k))
            
        return column_pins
        
    def list_all_br_names(self):
        """ Creates a list of all br pins names """
        column_pins = []
        for k in range(self.num_rw_ports):
            column_pins.append("rwbl_bar{0}".format(k))
        for k in range(self.num_w_ports):
            column_pins.append("wbl_bar{0}".format(k))
        for k in range(self.num_r_ports):
            column_pins.append("rbl_bar{0}".format(k))
            
        return column_pins
        
    def list_read_bl_names(self):
        """ Creates a list of bl pin names associated with read ports """
        column_pins = []
        for k in range(self.num_rw_ports):
            column_pins.append("rwbl{0}".format(k))
        for k in range(self.num_r_ports):
            column_pins.append("rbl{0}".format(k))
            
        return column_pins
        
    def list_read_br_names(self):
        """ Creates a list of br pin names associated with read ports """
        column_pins = []
        for k in range(self.num_rw_ports):
            column_pins.append("rwbl_bar{0}".format(k))
        for k in range(self.num_r_ports):
            column_pins.append("rbl_bar{0}".format(k))
            
        return column_pins
        
    def list_write_bl_names(self):
        """ Creates a list of bl pin names associated with write ports """
        column_pins = []
        for k in range(self.num_rw_ports):
            column_pins.append("rwbl{0}".format(k))
        for k in range(self.num_w_ports):
            column_pins.append("wbl{0}".format(k))
            
        return column_pins
    
    def list_write_br_names(self):
        """ Creates a list of br pin names asscociated with write ports"""
        column_pins = []
        for k in range(self.num_rw_ports):
            column_pins.append("rwbl_bar{0}".format(k))
        for k in range(self.num_w_ports):
            column_pins.append("wbl_bar{0}".format(k))
            
        return column_pins
