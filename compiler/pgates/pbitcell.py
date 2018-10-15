import contact
import design
import debug
from tech import drc, parameter, spice
from vector import vector
from ptx import ptx
from globals import OPTS

class pbitcell(design.design):
    """
    This module implements a parametrically sized multi-port bitcell,
    with a variable number of read/write, write, and read ports
    """
    
    def __init__(self, replica_bitcell=False):
        
        self.num_rw_ports = OPTS.num_rw_ports
        self.num_w_ports = OPTS.num_w_ports
        self.num_r_ports = OPTS.num_r_ports
        self.total_ports = self.num_rw_ports + self.num_w_ports + self.num_r_ports
        
        self.replica_bitcell = replica_bitcell
        
        if self.replica_bitcell:
            name = "replica_pbitcell_{0}RW_{1}W_{2}R".format(self.num_rw_ports, self.num_w_ports, self.num_r_ports)
        else:
            name = "pbitcell_{0}RW_{1}W_{2}R".format(self.num_rw_ports, self.num_w_ports, self.num_r_ports)
        # This is not a pgate because pgates depend on the bitcell height!
        design.design.__init__(self, name)
        debug.info(2, "create a multi-port bitcell with {0} rw ports, {1} w ports and {2} r ports".format(self.num_rw_ports,
                                                                                                          self.num_w_ports,
                                                                                                          self.num_r_ports))  

        self.create_netlist()
        # We must always create the bitcell layout because
        # some transistor sizes in the other netlists depend on it
        self.create_layout()
        
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
            self.route_readwrite_access()
        if(self.num_w_ports > 0):
            self.place_write_ports()
            self.route_write_access()
        if(self.num_r_ports > 0):
            self.place_read_ports()
            self.route_read_access()
        self.extend_well()
        
        self.route_wordlines()
        self.route_bitlines()
        self.route_supply()
        
        if self.replica_bitcell:
            self.route_rbc_short()
        
        # in netlist_only mode, calling offset_all_coordinates will not be possible
        # this function is not needed to calculate the dimensions of pbitcell in netlist_only mode though
        if not OPTS.netlist_only:
            self.offset_all_coordinates()
            gnd_overlap = vector(0, 0.5*contact.well.width)
            self.translate_all(gnd_overlap)
        self.DRC_LVS()
    
    def add_pins(self):
        self.rw_bl_names = []
        self.rw_br_names = []
        self.w_bl_names = []
        self.w_br_names = []
        self.r_bl_names = []
        self.r_br_names = []
        self.rw_wl_names = []
        self.w_wl_names = []
        self.r_wl_names = []
        port = 0
    
        for k in range(self.num_rw_ports):
            self.add_pin("bl{}".format(port))
            self.add_pin("br{}".format(port))
            self.rw_bl_names.append("bl{}".format(port))
            self.rw_br_names.append("br{}".format(port))
            port += 1
        for k in range(self.num_w_ports):
            self.add_pin("bl{}".format(port))
            self.add_pin("br{}".format(port))
            self.w_bl_names.append("bl{}".format(port))
            self.w_br_names.append("br{}".format(port))
            port += 1
        for k in range(self.num_r_ports):
            self.add_pin("bl{}".format(port))
            self.add_pin("br{}".format(port))
            self.r_bl_names.append("bl{}".format(port))
            self.r_br_names.append("br{}".format(port))
            port += 1
        
        port = 0
        for k in range(self.num_rw_ports):
            self.add_pin("wl{}".format(port))
            self.rw_wl_names.append("wl{}".format(port))
            port += 1
        for k in range(self.num_w_ports):
            self.add_pin("wl{}".format(port))
            self.w_wl_names.append("wl{}".format(port))
            port += 1
        for k in range(self.num_r_ports):
            self.add_pin("wl{}".format(port))
            self.r_wl_names.append("wl{}".format(port))
            port += 1
            
        self.add_pin("vdd")
        self.add_pin("gnd")
        
        if self.replica_bitcell:
            self.Q_bar = "vdd"
        else:
            self.Q_bar = "Q_bar"
    
    def add_modules(self):
        """
        Determine size of transistors and add ptx modules
        """
        # if there are any read/write ports, then the inverter nmos is sized based the number of read/write ports
        if(self.num_rw_ports > 0):
            inverter_nmos_width = self.num_rw_ports*3*parameter["min_tx_size"]
            inverter_pmos_width = parameter["min_tx_size"]
            readwrite_nmos_width = 1.5*parameter["min_tx_size"]
            write_nmos_width = parameter["min_tx_size"]
            read_nmos_width = 2*parameter["min_tx_size"]
        
        # if there are no read/write ports, then the inverter nmos is statically sized for the dual port case
        else:
            inverter_nmos_width = 2*parameter["min_tx_size"]
            inverter_pmos_width = parameter["min_tx_size"]
            readwrite_nmos_width = 1.5*parameter["min_tx_size"]
            write_nmos_width = parameter["min_tx_size"]
            read_nmos_width = 2*parameter["min_tx_size"]
    
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
        readwrite_nmos_contact_extension = 0.5*(self.readwrite_nmos.active_contact.height - self.readwrite_nmos.active_height)
        write_nmos_contact_extension = 0.5*(self.write_nmos.active_contact.height - self.write_nmos.active_height)
        read_nmos_contact_extension = 0.5*(self.read_nmos.active_contact.height - self.read_nmos.active_height)
        max_contact_extension = max(readwrite_nmos_contact_extension, write_nmos_contact_extension, read_nmos_contact_extension)
        
        # y-offset for the access transistor's gate contact
        self.gate_contact_yoffset = max_contact_extension + self.m2_space + 0.5*max(contact.poly.height, contact.m1m2.height)
        
        # y-position of access transistors
        self.port_ypos = self.m1_space + 0.5*contact.m1m2.height + self.gate_contact_yoffset
        
        # y-position of inverter nmos
        self.inverter_nmos_ypos = self.port_ypos
        
        # spacing between ports
        self.bitline_offset = -self.active_width + 0.5*contact.m1m2.height + self.m2_space + self.m2_width 
        self.port_spacing = self.bitline_offset + self.m2_space
        
        # spacing between cross coupled inverters
        self.inverter_to_inverter_spacing = contact.poly.height + self.m1_space
        
        # calculations related to inverter connections
        inverter_pmos_contact_extension = 0.5*(self.inverter_pmos.active_contact.height - self.inverter_pmos.active_height)
        self.inverter_gap = self.poly_to_active + self.poly_to_polycontact + 2*contact.poly.width + self.m1_space + inverter_pmos_contact_extension
        self.cross_couple_lower_ypos = self.inverter_nmos_ypos + self.inverter_nmos.active_height + self.poly_to_active + 0.5*contact.poly.width
        self.cross_couple_upper_ypos = self.inverter_nmos_ypos + self.inverter_nmos.active_height + self.poly_to_active + self.poly_to_polycontact + 1.5*contact.poly.width
        
        # spacing between wordlines (and gnd)
        self.rowline_spacing = self.m1_space + contact.m1m2.width
        
        # spacing for vdd
        vdd_offset_well_constraint = self.well_enclose_active + 0.5*contact.well.width
        vdd_offset_metal1_constraint = max(inverter_pmos_contact_extension, 0) + self.m1_space + 0.5*contact.well.width
        self.vdd_offset = max(vdd_offset_well_constraint, vdd_offset_metal1_constraint)
        
        # read port dimensions
        width_reduction = self.read_nmos.active_width - self.read_nmos.get_pin("D").cx()
        self.read_port_width = 2*self.read_nmos.active_width - 2*width_reduction
    
    def calculate_postions(self):
        """ 
        Calculate positions that describe the edges and dimensions of the cell 
        """
        self.botmost_ypos = -0.5*self.m1_width - self.total_ports*self.rowline_spacing
        self.topmost_ypos = self.inverter_nmos_ypos + self.inverter_nmos.active_height + self.inverter_gap + self.inverter_pmos.active_height + self.vdd_offset
        
        self.leftmost_xpos = -0.5*self.inverter_to_inverter_spacing - self.inverter_nmos.active_width \
                             - self.num_rw_ports*(self.readwrite_nmos.active_width + self.port_spacing) \
                             - self.num_w_ports*(self.write_nmos.active_width + self.port_spacing) \
                             - self.num_r_ports*(self.read_port_width + self.port_spacing) \
                             - self.bitline_offset - 0.5*self.m2_space
        
        self.width = -2*self.leftmost_xpos
        self.height = self.topmost_ypos - self.botmost_ypos
        
        self.y_center = 0.5*(self.topmost_ypos + self.botmost_ypos)

    def create_storage(self):
        """
        Creates the crossed coupled inverters that act as storage for the bitcell.
        The stored value of the cell is denoted as "Q", and the inverted value as "Q_bar".
        """
        
        # create active for nmos
        self.inverter_nmos_left = self.add_inst(name="inverter_nmos_left",
                                                mod=self.inverter_nmos)
        self.connect_inst(["Q", self.Q_bar, "gnd", "gnd"])
        
        self.inverter_nmos_right = self.add_inst(name="inverter_nmos_right",
                                                 mod=self.inverter_nmos)
        self.connect_inst(["gnd", "Q", self.Q_bar, "gnd"])
        
        # create active for pmos
        self.inverter_pmos_left = self.add_inst(name="inverter_pmos_left",
                                                mod=self.inverter_pmos)
        self.connect_inst(["Q", self.Q_bar, "vdd", "vdd"])
        
        self.inverter_pmos_right = self.add_inst(name="inverter_pmos_right",
                                                 mod=self.inverter_pmos)
        self.connect_inst(["vdd", "Q", self.Q_bar, "vdd"])
        
    def place_storage(self):
        """
        Places the transistors for the crossed coupled inverters in the bitcell
        """
        
        # calculate transistor offsets
        left_inverter_xpos = -0.5*self.inverter_to_inverter_spacing - self.inverter_nmos.active_width
        right_inverter_xpos = 0.5*self.inverter_to_inverter_spacing
        inverter_pmos_ypos = self.inverter_nmos_ypos + self.inverter_nmos.active_height + self.inverter_gap
                
        # create active for nmos
        self.inverter_nmos_left.place([left_inverter_xpos, self.inverter_nmos_ypos])
        self.inverter_nmos_right.place([right_inverter_xpos, self.inverter_nmos_ypos])
        
        # create active for pmos
        self.inverter_pmos_left.place([left_inverter_xpos, inverter_pmos_ypos])
        self.inverter_pmos_right.place([right_inverter_xpos, inverter_pmos_ypos])
        
        self.left_building_edge = left_inverter_xpos
        self.right_building_edge = right_inverter_xpos + self.inverter_nmos.active_width
        
    def route_storage(self):
        """
        Routes inputs and outputs of inverters to cross couple them
        """
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
        
    def route_rails(self):
        """
        Adds gnd and vdd rails and connects them to the inverters
        """
        # Add rails for vdd and gnd
        gnd_ypos = -0.5*self.m1_width - self.total_ports*self.rowline_spacing
        self.gnd_position = vector(0, gnd_ypos)
        self.gnd = self.add_layout_pin_rect_center(text="gnd",
                                                   layer="metal1",
                                                   offset=self.gnd_position,
                                                   width=self.width,
                                                   height=contact.well.second_layer_width)
        
        vdd_ypos = self.inverter_nmos_ypos + self.inverter_nmos.active_height + self.inverter_gap + self.inverter_pmos.active_height + self.vdd_offset
        self.vdd_position = vector(0, vdd_ypos)
        self.vdd = self.add_layout_pin_rect_center(text="vdd",
                                                   layer="metal1",
                                                   offset=self.vdd_position,
                                                   width=self.width,
                                                   height=contact.well.second_layer_width)

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
            self.connect_inst([self.rw_bl_names[k], self.rw_wl_names[k], "Q", "gnd"])
            
            self.readwrite_nmos_right[k] = self.add_inst(name="readwrite_nmos_right{}".format(k),
                                                         mod=self.readwrite_nmos)
            self.connect_inst([self.Q_bar, self.rw_wl_names[k], self.rw_br_names[k], "gnd"])

    def place_readwrite_ports(self):
        """
        Places read/write ports in the bit cell. 
        """
    
        # Define variables relevant to write transistors
        self.rwwl_positions = [None] * self.num_rw_ports
        self.rwbl_positions = [None] * self.num_rw_ports
        self.rwbr_positions = [None] * self.num_rw_ports
        
        # iterate over the number of read/write ports
        for k in range(0,self.num_rw_ports):
            # Add transistors
            # calculate read/write transistor offsets 
            left_readwrite_transistor_xpos = self.left_building_edge \
                                             - (k+1)*self.port_spacing \
                                             - (k+1)*self.readwrite_nmos.active_width
            
            right_readwrite_transistor_xpos = self.right_building_edge \
                                              + (k+1)*self.port_spacing \
                                              + k*self.readwrite_nmos.active_width
            
            # add read/write transistors
            self.readwrite_nmos_left[k].place(offset=[left_readwrite_transistor_xpos, self.port_ypos])
            
            self.readwrite_nmos_right[k].place(offset=[right_readwrite_transistor_xpos, self.port_ypos])
                        
            # Add RWWL lines 
            # calculate RWWL position
            rwwl_ypos = -0.5*self.m1_width - k*self.rowline_spacing
            self.rwwl_positions[k] = vector(0, rwwl_ypos)
            
            # add pin for RWWL
            self.add_layout_pin_rect_center(text=self.rw_wl_names[k],
                                            layer="metal1",
                                            offset=self.rwwl_positions[k],
                                            width=self.width,
                                            height=self.m1_width)
                      
            # add pins for RWBL and RWBL_bar, overlaid on source contacts
            rwbl_xpos = left_readwrite_transistor_xpos - self.bitline_offset + self.m2_width
            self.rwbl_positions[k] = vector(rwbl_xpos, self.y_center)
            self.add_layout_pin_rect_center(text=self.rw_bl_names[k],
                                            layer="metal2",
                                            offset=self.rwbl_positions[k],
                                            width=drc["minwidth_metal2"],
                                            height=self.height)

            rwbr_xpos = right_readwrite_transistor_xpos + self.readwrite_nmos.active_width + self.bitline_offset - self.m2_width
            self.rwbr_positions[k] = vector(rwbr_xpos, self.y_center)
            self.add_layout_pin_rect_center(text=self.rw_br_names[k],
                                            layer="metal2",
                                            offset=self.rwbr_positions[k],
                                            width=drc["minwidth_metal2"],
                                            height=self.height)
        
        # update furthest left and right transistor edges 
        self.left_building_edge = left_readwrite_transistor_xpos
        self.right_building_edge = right_readwrite_transistor_xpos + self.readwrite_nmos.active_width
    
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
            self.connect_inst([self.w_bl_names[k], self.w_wl_names[k], "Q", "gnd"])
            
            self.write_nmos_right[k] = self.add_inst(name="write_nmos_right{}".format(k),
                                                     mod=self.write_nmos)
            self.connect_inst([self.Q_bar, self.w_wl_names[k], self.w_br_names[k], "gnd"])

    def place_write_ports(self):
        """
        Places write ports in the bit cell. 
        """
        # Define variables relevant to write transistors 
        self.wwl_positions = [None] * self.num_w_ports
        self.wbl_positions = [None] * self.num_w_ports
        self.wbr_positions = [None] * self.num_w_ports       

        # define offset correction due to rotation of the ptx module
        write_rotation_correct = self.write_nmos.active_height
        
        # iterate over the number of write ports
        for k in range(0,self.num_w_ports):
            # Add transistors
            # calculate write transistor offsets 
            left_write_transistor_xpos = self.left_building_edge \
                                         - (k+1)*self.port_spacing \
                                         - (k+1)*self.write_nmos.active_width
            
            right_write_transistor_xpos = self.right_building_edge \
                                          + (k+1)*self.port_spacing \
                                          + k*self.write_nmos.active_width
            
            # add write transistors
            self.write_nmos_left[k].place(offset=[left_write_transistor_xpos, self.port_ypos])
            
            self.write_nmos_right[k].place(offset=[right_write_transistor_xpos, self.port_ypos])
                        
            # Add WWL lines 
            # calculate WWL position
            wwl_ypos = rwwl_ypos = -0.5*self.m1_width - self.num_rw_ports*self.rowline_spacing - k*self.rowline_spacing
            self.wwl_positions[k] = vector(0, wwl_ypos)
            
            # add pin for WWL
            self.add_layout_pin_rect_center(text=self.w_wl_names[k],
                                            layer="metal1",
                                            offset=self.wwl_positions[k],
                                            width=self.width,
                                            height=self.m1_width)
                       
            # add pins for WBL and WBL_bar, overlaid on source contacts
            wbl_xpos = left_write_transistor_xpos - self.bitline_offset + self.m2_width
            self.wbl_positions[k] = vector(wbl_xpos, self.y_center)
            self.add_layout_pin_rect_center(text=self.w_bl_names[k],
                                            layer="metal2",
                                            offset=self.wbl_positions[k],
                                            width=drc["minwidth_metal2"],
                                            height=self.height)

            wbr_xpos = right_write_transistor_xpos + self.write_nmos.active_width + self.bitline_offset - self.m2_width
            self.wbr_positions[k] = vector(wbr_xpos, self.y_center)
            self.add_layout_pin_rect_center(text=self.w_br_names[k],
                                            layer="metal2",
                                            offset=self.wbr_positions[k],
                                            width=drc["minwidth_metal2"],
                                            height=self.height)
        
        # update furthest left and right transistor edges 
        self.left_building_edge = left_write_transistor_xpos
        self.right_building_edge = right_write_transistor_xpos + self.write_nmos.active_width
                
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
            self.connect_inst(["RA_to_R_left{}".format(k), self.Q_bar, "gnd", "gnd"])
            
            self.read_access_nmos_right[k] = self.add_inst(name="read_access_nmos_right{}".format(k),
                                                           mod=self.read_nmos)
            self.connect_inst(["gnd", "Q", "RA_to_R_right{}".format(k), "gnd"])
            
            # add read transistors
            self.read_nmos_left[k] = self.add_inst(name="read_nmos_left{}".format(k),
                                                   mod=self.read_nmos)
            self.connect_inst([self.r_bl_names[k], self.r_wl_names[k], "RA_to_R_left{}".format(k), "gnd"])
            
            self.read_nmos_right[k] = self.add_inst(name="read_nmos_right{}".format(k),
                                                    mod=self.read_nmos)
            self.connect_inst(["RA_to_R_right{}".format(k), self.r_wl_names[k], self.r_br_names[k], "gnd"])
                        
    def place_read_ports(self):
        """
        Places the read ports in the bit cell. 
        """
        # Define variables relevant to read transistors
        self.rwl_positions = [None] * self.num_r_ports
        self.rbl_positions = [None] * self.num_r_ports
        self.rbr_positions = [None] * self.num_r_ports
        
        # define offset correction due to rotation of the ptx module
        read_rotation_correct = self.read_nmos.active_height
        
        # calculate offset to overlap the drain of the read-access transistor with the source of the read transistor
        overlap_offset = self.read_nmos.get_pin("D").cx() - self.read_nmos.get_pin("S").cx()
        
        # iterate over the number of read ports
        for k in range(0,self.num_r_ports):
            # Add transistors 
            # calculate transistor offsets
            left_read_transistor_xpos = self.left_building_edge \
                                        - (k+1)*self.port_spacing \
                                        - (k+1)*self.read_port_width
            
            right_read_transistor_xpos = self.right_building_edge \
                                         + (k+1)*self.port_spacing \
                                         + k*self.read_port_width
            
            # add read-access transistors
            self.read_access_nmos_left[k].place(offset=[left_read_transistor_xpos+overlap_offset, self.port_ypos])
            
            self.read_access_nmos_right[k].place(offset=[right_read_transistor_xpos, self.port_ypos])
            
            # add read transistors
            self.read_nmos_left[k].place(offset=[left_read_transistor_xpos, self.port_ypos])
            
            self.read_nmos_right[k].place(offset=[right_read_transistor_xpos+overlap_offset, self.port_ypos])
                        
            # Add RWL lines 
            # calculate RWL position
            rwl_ypos = rwwl_ypos = -0.5*self.m1_width - self.num_rw_ports*self.rowline_spacing - self.num_w_ports*self.rowline_spacing - k*self.rowline_spacing
            self.rwl_positions[k] = vector(0, rwl_ypos)
            
            # add pin for RWL
            self.add_layout_pin_rect_center(text=self.r_wl_names[k],
                                            layer="metal1",
                                            offset=self.rwl_positions[k],
                                            width=self.width,
                                            height=self.m1_width)
            
            # add pins for RBL and RBL_bar, overlaid on drain contacts
            rbl_xpos = left_read_transistor_xpos - self.bitline_offset + self.m2_width
            self.rbl_positions[k] = vector(rbl_xpos, self.y_center)
            self.add_layout_pin_rect_center(text=self.r_bl_names[k],
                                            layer="metal2",
                                            offset=self.rbl_positions[k],
                                            width=drc["minwidth_metal2"],
                                            height=self.height)

            rbr_xpos = right_read_transistor_xpos + self.read_port_width + self.bitline_offset - self.m2_width
            self.rbr_positions[k] = vector(rbr_xpos, self.y_center)
            self.add_layout_pin_rect_center(text=self.r_br_names[k],
                                            layer="metal2",
                                            offset=self.rbr_positions[k],
                                            width=drc["minwidth_metal2"],
                                            height=self.height)
                                            
    def route_wordlines(self):
        """
        Routes gate of transistors to their respective wordlines
        """
        port_transistors = []
        for k in range(self.num_rw_ports):
            port_transistors.append(self.readwrite_nmos_left[k])
            port_transistors.append(self.readwrite_nmos_right[k])
        for k in range(self.num_w_ports):
            port_transistors.append(self.write_nmos_left[k])
            port_transistors.append(self.write_nmos_right[k])
        for k in range(self.num_r_ports):
            port_transistors.append(self.read_nmos_left[k])
            port_transistors.append(self.read_nmos_right[k])
            
        wl_positions = []
        for k in range(self.num_rw_ports):
            wl_positions.append(self.rwwl_positions[k])
            wl_positions.append(self.rwwl_positions[k])
        for k in range(self.num_w_ports):
            wl_positions.append(self.wwl_positions[k])
            wl_positions.append(self.wwl_positions[k])
        for k in range(self.num_r_ports):
            wl_positions.append(self.rwl_positions[k])
            wl_positions.append(self.rwl_positions[k])
        
        
        for k in range(2*self.total_ports):
            gate_offset = port_transistors[k].get_pin("G").bc()
            port_contact_offset = gate_offset + vector(0, -self.gate_contact_yoffset + self.poly_extend_active)
            wl_contact_offset = vector(gate_offset.x, wl_positions[k].y)
           
            if (k == 0) or (k == 1):
                self.add_contact_center(layers=("poly", "contact", "metal1"),
                                        offset=port_contact_offset)
                                        
                self.add_path("poly", [gate_offset, port_contact_offset])                 
                self.add_path("metal1", [port_contact_offset, wl_contact_offset])
                                                 
            else:
                self.add_contact_center(layers=("poly", "contact", "metal1"),
                                        offset=port_contact_offset)            
                self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                        offset=port_contact_offset)
                                        
                self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                        offset=wl_contact_offset,
                                        rotate=90)
                                        
                self.add_path("poly", [gate_offset, port_contact_offset])                 
                self.add_path("metal2", [port_contact_offset, wl_contact_offset])
                
    def route_bitlines(self):
        """ 
        Routes read/write transistors to their respective bitlines
        """
        left_port_transistors = []
        right_port_transistors = []
        for k in range(self.num_rw_ports):
            left_port_transistors.append(self.readwrite_nmos_left[k])
            right_port_transistors.append(self.readwrite_nmos_right[k])
        for k in range(self.num_w_ports):
            left_port_transistors.append(self.write_nmos_left[k])
            right_port_transistors.append(self.write_nmos_right[k])
        for k in range(self.num_r_ports):
            left_port_transistors.append(self.read_nmos_left[k])
            right_port_transistors.append(self.read_nmos_right[k])
            
        bl_positions = []
        br_positions = []
        for k in range(self.num_rw_ports):
            bl_positions.append(self.rwbl_positions[k])
            br_positions.append(self.rwbr_positions[k])
        for k in range(self.num_w_ports):
            bl_positions.append(self.wbl_positions[k])
            br_positions.append(self.wbr_positions[k])
        for k in range(self.num_r_ports):
            bl_positions.append(self.rbl_positions[k])
            br_positions.append(self.rbr_positions[k])
            
        for k in range(self.total_ports):
            port_contact_offest = left_port_transistors[k].get_pin("S").center()
            bl_offset = vector(bl_positions[k].x, port_contact_offest.y)
            
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=port_contact_offest)
                                    
            self.add_path("metal2", [port_contact_offest, bl_offset], width=contact.m1m2.height)
            
        for k in range(self.total_ports):
            port_contact_offest = right_port_transistors[k].get_pin("D").center()
            br_offset = vector(br_positions[k].x, port_contact_offest.y)
            
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=port_contact_offest)
                                    
            self.add_path("metal2", [port_contact_offest, br_offset], width=contact.m1m2.height)
            
    def route_supply(self):
        # route inverter nmos and read-access transistors to gnd
        nmos_contact_positions = []
        nmos_contact_positions.append(self.inverter_nmos_left.get_pin("S").center())
        nmos_contact_positions.append(self.inverter_nmos_right.get_pin("D").center())
        for k in range(self.num_r_ports):
            nmos_contact_positions.append(self.read_access_nmos_left[k].get_pin("D").center())
            nmos_contact_positions.append(self.read_access_nmos_right[k].get_pin("S").center())
            
        for position in nmos_contact_positions:
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=position)
                                    
            supply_offset = vector(position.x, self.gnd_position.y)
            self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                    offset=supply_offset,
                                    rotate=90)
                                    
            self.add_path("metal2", [position, supply_offset])
        
        # route inverter pmos to vdd
        vdd_pos_left = vector(self.inverter_nmos_left.get_pin("S").uc().x, self.vdd_position.y)
        self.add_path("metal1", [self.inverter_pmos_left.get_pin("S").uc(), vdd_pos_left])
        
        vdd_pos_right = vector(self.inverter_nmos_right.get_pin("D").uc().x, self.vdd_position.y)
        self.add_path("metal1", [self.inverter_pmos_right.get_pin("D").uc(), vdd_pos_right])
        
    def route_readwrite_access(self):
        """
        Routes read/write transistors to the storage component of the bitcell
        """
        for k in range(self.num_rw_ports):
            mid = vector(self.readwrite_nmos_left[k].get_pin("D").uc().x, self.cross_couple_lower_ypos)
            Q_pos = vector(self.inverter_nmos_left.get_pin("D").lx(), self.cross_couple_lower_ypos)
            self.add_path("metal1", [self.readwrite_nmos_left[k].get_pin("D").uc(), mid+vector(0,0.5*self.m1_width)], width=contact.poly.second_layer_width)
            self.add_path("metal1", [mid, Q_pos])
            
            mid = vector(self.readwrite_nmos_right[k].get_pin("S").uc().x, self.cross_couple_lower_ypos)
            Q_bar_pos = vector(self.inverter_nmos_right.get_pin("S").rx(), self.cross_couple_lower_ypos)
            self.add_path("metal1", [self.readwrite_nmos_right[k].get_pin("S").uc(), mid+vector(0,0.5*self.m1_width)], width=contact.poly.second_layer_width)
            self.add_path("metal1", [mid, Q_bar_pos])
            
    def route_write_access(self):
        """
        Routes read/write transistors to the storage component of the bitcell
        """
        for k in range(self.num_w_ports):
            mid = vector(self.write_nmos_left[k].get_pin("D").uc().x, self.cross_couple_lower_ypos)
            Q_pos = vector(self.inverter_nmos_left.get_pin("D").lx(), self.cross_couple_lower_ypos)
            self.add_path("metal1", [self.write_nmos_left[k].get_pin("D").uc(), mid+vector(0,0.5*self.m1_width)], width=contact.poly.second_layer_width)
            self.add_path("metal1", [mid, Q_pos])
            
            mid = vector(self.write_nmos_right[k].get_pin("S").uc().x, self.cross_couple_lower_ypos)
            Q_bar_pos = vector(self.inverter_nmos_right.get_pin("S").rx(), self.cross_couple_lower_ypos)
            self.add_path("metal1", [self.write_nmos_right[k].get_pin("S").uc(), mid+vector(0,0.5*self.m1_width)], width=contact.poly.second_layer_width)
            self.add_path("metal1", [mid, Q_bar_pos])
    
    def route_read_access(self):
        """ 
        Routes read access transistors to the storage component of the bitcell
        """
        left_storage_contact =  vector(self.inverter_nmos_left.get_pin("G").lc().x - drc["poly_to_polycontact"] - 0.5*contact.poly.width, self.cross_couple_upper_ypos)
        self.add_contact_center(layers=("poly", "contact", "metal1"),
                                        offset=left_storage_contact,
                                        rotate=90)
        
        right_storage_contact =  vector(self.inverter_nmos_right.get_pin("G").rc().x + drc["poly_to_polycontact"] + 0.5*contact.poly.width, self.cross_couple_upper_ypos)
        self.add_contact_center(layers=("poly", "contact", "metal1"),
                                        offset=right_storage_contact,
                                        rotate=90)
    
        inverter_gate_offset_left = vector(self.inverter_nmos_left.get_pin("G").lc().x, self.cross_couple_upper_ypos)
        self.add_path("poly", [left_storage_contact, inverter_gate_offset_left])
        
        inverter_gate_offset_right = vector(self.inverter_nmos_right.get_pin("G").rc().x, self.cross_couple_upper_ypos)
        self.add_path("poly", [right_storage_contact, inverter_gate_offset_right])
        
        for k in range(self.num_r_ports):
            port_contact_offset = self.read_access_nmos_left[k].get_pin("G").uc() + vector(0, self.gate_contact_yoffset - self.poly_extend_active)

            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=port_contact_offset)
                                    
            self.add_path("poly", [self.read_access_nmos_left[k].get_pin("G").uc(), port_contact_offset])
                                    
            mid = vector(self.read_access_nmos_left[k].get_pin("G").uc().x, self.cross_couple_upper_ypos)
            self.add_path("metal1", [port_contact_offset, mid+vector(0,0.5*self.m1_width)], width=contact.poly.second_layer_width)
            self.add_path("metal1", [mid, left_storage_contact])
            
            port_contact_offset = self.read_access_nmos_right[k].get_pin("G").uc() + vector(0, self.gate_contact_yoffset - self.poly_extend_active)

            self.add_contact_center(layers=("poly", "contact", "metal1"),
                                    offset=port_contact_offset)
                                    
            self.add_path("poly", [self.read_access_nmos_right[k].get_pin("G").uc(), port_contact_offset])
                                    
            mid = vector(self.read_access_nmos_right[k].get_pin("G").uc().x, self.cross_couple_upper_ypos)
            self.add_path("metal1", [port_contact_offset, mid+vector(0,0.5*self.m1_width)], width=contact.poly.second_layer_width)
            self.add_path("metal1", [mid, right_storage_contact])
        
    def extend_well(self):
        """
        Connects wells between ptx modules to avoid drc spacing issues.
        Since the pwell of the read ports rise higher than the nwell of the inverters,
        the well connections must be done piecewise to avoid pwell and nwell overlap.
        """
        
        max_nmos_well_height = max(self.inverter_nmos.cell_well_height,
                              self.readwrite_nmos.cell_well_height,
                              self.write_nmos.cell_well_height,
                              self.read_nmos.cell_well_height)
        
        well_height = max_nmos_well_height + self.port_ypos - self.well_enclose_active - self.gnd_position.y
    
        # extend pwell to encompass entire nmos region of the cell up to the height of the inverter nmos well 
        offset = vector(self.leftmost_xpos, self.botmost_ypos)
        self.add_rect(layer="pwell",
                      offset=offset,
                      width=self.width,
                      height=well_height)        
        
        # extend nwell to encompass inverter_pmos
        # calculate offset of the left pmos well
        inverter_well_xpos = -(self.inverter_nmos.active_width + 0.5*self.inverter_to_inverter_spacing) - drc["well_enclosure_active"]
        inverter_well_ypos = self.inverter_nmos_ypos + self.inverter_nmos.active_height + self.inverter_gap - drc["well_enclosure_active"]
        
        # calculate width of the two combined nwells
        # calculate height to encompass nimplant connected to vdd
        well_width = 2*(self.inverter_nmos.active_width + 0.5*self.inverter_to_inverter_spacing) + 2*drc["well_enclosure_active"]
        well_height = self.vdd_position.y - inverter_well_ypos + drc["well_enclosure_active"] + drc["minwidth_tx"]
        
        offset = [inverter_well_xpos,inverter_well_ypos]
        self.add_rect(layer="nwell",
                      offset=offset,
                      width=well_width,
                      height=well_height)
        
        
        # add well contacts 
        # connect pimplants to gnd
        offset = vector(0, self.gnd_position.y)
        self.add_contact_center(layers=("active", "contact", "metal1"),
                                offset=offset,
                                rotate=90,
                                implant_type="p",
                                well_type="p")
        
        # connect nimplants to vdd
        offset = vector(0, self.vdd_position.y)
        self.add_contact_center(layers=("active", "contact", "metal1"),
                                offset=offset,
                                rotate=90,
                                implant_type="n",
                                well_type="n")  
    
    def list_bitcell_pins(self, col, row):
        """ Creates a list of connections in the bitcell, indexed by column and row, for instance use in bitcell_array """
        bitcell_pins = []
        for port in range(self.total_ports):
            bitcell_pins.append("bl{0}_{1}".format(port,col))
            bitcell_pins.append("br{0}_{1}".format(port,col))
        for port in range(self.total_ports):
            bitcell_pins.append("wl{0}_{1}".format(port,row))
        bitcell_pins.append("vdd")
        bitcell_pins.append("gnd")
        return bitcell_pins
    
    def list_all_wl_names(self):
        """ Creates a list of all wordline pin names """
        wordline_names = self.rw_wl_names + self.w_wl_names + self.r_wl_names
        return wordline_names
    
    def list_all_bitline_names(self):
        """ Creates a list of all bitline pin names (both bl and br) """
        bitline_pins = []
        for port in range(self.total_ports):
            bitline_pins.append("bl{0}".format(port))
            bitline_pins.append("br{0}".format(port))
        return bitline_pins
        
    def list_all_bl_names(self):
        """ Creates a list of all bl pins names """
        bl_pins = self.rw_bl_names + self.w_bl_names + self.r_bl_names    
        return bl_pins
        
    def list_all_br_names(self):
        """ Creates a list of all br pins names """
        br_pins = self.rw_br_names + self.w_br_names + self.r_br_names     
        return br_pins
        
    def list_read_bl_names(self):
        """ Creates a list of bl pin names associated with read ports """
        bl_pins = self.rw_bl_names + self.r_bl_names     
        return bl_pins
        
    def list_read_br_names(self):
        """ Creates a list of br pin names associated with read ports """
        br_pins = self.rw_br_names + self.r_br_names     
        return br_pins
        
    def list_write_bl_names(self):
        """ Creates a list of bl pin names associated with write ports """
        bl_pins = self.rw_bl_names + self.w_bl_names  
        return bl_pins
    
    def list_write_br_names(self):
        """ Creates a list of br pin names asscociated with write ports"""
        br_pins = self.rw_br_names + self.w_br_names  
        return br_pins
        
    def route_rbc_short(self):
        """ route the short from Q_bar to gnd necessary for the replica bitcell """
        Q_bar_pos = self.inverter_pmos_left.get_pin("D").uc()
        vdd_pos = vector(Q_bar_pos.x, self.vdd_position.y)
        
        self.add_path("metal1", [Q_bar_pos, vdd_pos])
        