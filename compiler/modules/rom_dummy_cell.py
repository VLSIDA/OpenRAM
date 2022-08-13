# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#



from base import design
from base import vector
from globals import OPTS
from sram_factory import factory
from tech import drc


class rom_dummy_cell(design):

    def __init__(self, name="", cell_name=None, source_contact=False, drain_contact=False):
        super().__init__(name, cell_name)
        self.route_layer = "m1"
        self.source_contact=source_contact
        self.drain_contact=drain_contact
        self.create_netlist()
        self.create_layout()

    def create_netlist(self):
        #creates nmos for layout dimensions
        self.add_nmos()


        #set height and width such that the cell will tile perfectly by only ofsetting in the array by its width and height
        
        

    def create_layout(self):
        
        
        self.setup_drc_offsets()
        
        self.add_boundary()
        self.add_poly()
        self.add_metal()
        #poly_offset = 
        #           vector(0.5 * self.nmos.active_contact.width +  0.5 * self.nmos.poly_width + self.nmos.active_contact_to_gate, 0)
                     
        #self.add_rect(  layer="poly",
        #                offset=poly_offset,
        #                height=self.nmos.height + self.nmos.poly_extend_active,
        #                width=self.nmos.poly_width
        #            )   
        self.add_label("0,0", self.route_layer)
        #self.add_wire(  layers=self.route_layer)
        #self.add_rect(  layer=self.route_layer)



    # Calculates offsets of cell width and height so that tiling of cells does not violate any drc rules
    def setup_drc_offsets(self):
    
        #nmos contact to gate distance
        self.contact_to_gate = 0.5 * (self.nmos.width - 2 * self.nmos.contact_width - self.nmos.poly_width - 2 * self.active_enclose_contact) 

        #height offset to account for active-to-active spacing between adjacent bitlines
        self.poly_extend_active_spacing = abs( 2 * self.nmos.poly_extend_active - drc("active_to_active") )

        #contact to contact distance, minimum cell width before drc offsets 
        self.base_width = self.nmos.width - 2 * self.active_enclose_contact - self.nmos.contact_width

        #width offset to account for active-to-active spacing between cells on the same bitline
        #this is calculated as a negative value
        self.cell_diffusion_offset = ((self.base_width - 2 * self.active_enclose_contact - self.nmos.contact_width) - drc("active_to_active")) * 0.5

        
        # width offset to account for poly-active spacing between base and dummy cells on the same bitline
        self.poly_active_offset = 0.5 * (self.base_width - 2 * self.cell_diffusion_offset - (self.poly_width + 2 * self.active_enclose_contact + self.nmos.contact_width)) - self.poly_to_active


    def add_boundary(self):

        #cell height with offsets applied
        self.height = self.nmos.height + self.poly_extend_active_spacing + 2 * self.nmos.poly_extend_active

        # cell width with offsets applied, if the offsets are positive (greater than 0) they are not applied
        self.width = self.base_width - min(self.cell_diffusion_offset, 0) - min(self.poly_active_offset, 0)

        super().add_boundary()

        

    def add_poly(self):

        poly_x = 0.5 * self.nmos.contact_width + self.contact_to_gate

        self.add_rect("poly", vector(poly_x, 0), self.poly_width, self.height)

    def add_metal(self):

        wire_x =  min(self.cell_diffusion_offset, 0) + min(self.poly_active_offset, 0)
        wire_y = 0.5 * (self.height - self.poly_extend_active_spacing)

        wire_start = vector( wire_x, wire_y )
        wire_end = vector(self.width, wire_y)

        if self.route_layer == 'm1':

            if self.drain_contact:
                self.add_via_center(self.li_stack, [wire_x, wire_y])
            if self.source_contact:
                self.add_via_center(self.li_stack, [self.width, wire_y])

        self.add_path(self.route_layer, [wire_start, wire_end])   
        
            
            
            

    def add_nmos(self):
        #used only for layout constants
        self.nmos  = factory.create(module_type="ptx",
                                    tx_type="nmos"
                                    )
        
    
