import design
import debug
from tech import drc, info, spice
from vector import vector
from contact import contact
import path
import re

class ptx(design.design):
    """
    This module generates gds and spice of a parametrically NMOS or PMOS sized transistor. 
    Creates a simple MOS transistor. poly_positions are the ll of the poly gate. active_contact_positions
    is an array of the positions of the ll of active contacts (left to right)
    """
    def __init__(self, width=drc["minwidth_tx"], mults=1, tx_type="nmos", connect_active=False, connect_poly=False, num_contacts=None):
        name = "{0}_m{1}_w{2}".format(tx_type, mults, width)
        if connect_active:
            name += "_a"
        if connect_poly:
            name += "_p"
        if num_contacts:
            name += "_c{}".format(num_contacts)
        name=re.sub('\.','_',name) # remove periods for newer spice compatibility

        design.design.__init__(self, name)
        debug.info(3, "create ptx structure {0}".format(name))

        self.tx_type = tx_type
        self.mults = mults
        self.gate_width = width
        self.connect_active = connect_active
        self.connect_poly = connect_poly
        self.num_contacts = num_contacts

        self.add_pins()
        self.create_layout()
        self.create_spice()
        # for run-time, we won't check every transitor DRC independently
        #self.DRC()

    def add_pins(self):
        self.add_pin_list(["D", "G", "S", "B"])

    def create_layout(self):
        self.setup_layout_constants()

        if self.num_contacts==None:
            self.num_contacts=self.calculate_num_contacts()
        
        # This is not actually instantiated but used for calculations
        self.active_contact = contact(layer_stack=("active", "contact", "metal1"),
                                      dimensions=(1, self.num_contacts))
        
        self.add_active()
        self.add_implants()  
        self.add_poly()
        self.add_active_contacts()

        # offset this BEFORE we add the active/poly connections
        self.offset_all_coordinates()
        
        if self.connect_active:
            self.connect_fingered_active()
        if self.connect_poly:
            self.connect_fingered_poly()

    def offset_attributes(self, coordinate):
        """Translates all stored 2d cartesian coordinates within the
        attr dictionary"""
        # FIXME: This is dangerous. I think we should not do this, but explicitly
        # offset the necessary coordinates. It is only used in ptx for now!

        for attr_key in dir(self):
            attr_val = getattr(self,attr_key)

            # skip the list of things as these will be offset separately
            if (attr_key in ['objs','insts','mods','pins','conns','name_map']): continue

            # if is a list
            if isinstance(attr_val, list):
                
                for i in range(len(attr_val)):
                    # each unit in the list is a list coordinates
                    if isinstance(attr_val[i], (list,vector)):
                        attr_val[i] = vector(attr_val[i] - coordinate)
                    # the list itself is a coordinate
                    else:
                        if len(attr_val)!=2: continue
                        for val in attr_val:
                            if not isinstance(val, (int, long, float)): continue
                        setattr(self,attr_key, vector(attr_val - coordinate))
                        break

            # if is a vector coordinate
            if isinstance(attr_val, vector):
                setattr(self, attr_key, vector(attr_val - coordinate))
        
    def offset_all_coordinates(self):
        offset = self.find_lowest_coords()
        self.offset_attributes(offset)
        self.translate_all(offset)

        # We can do this in ptx because we have offset all modules it uses.
        # Is this really true considering the paths that connect the src/drain?
        self.height = max(max(obj.offset.y + obj.height for obj in self.objs),
                                  max(inst.offset.y + inst.mod.height for inst in self.insts))
        self.width = max(max(obj.offset.x + obj.width for obj in self.objs),
                                 max(inst.offset.x + inst.mod.width for inst in self.insts))

    def create_spice(self):
        self.spice.append("\n.SUBCKT {0} {1}".format(self.name,
                                                     " ".join(self.pins)))
        self.spice.append("M{0} {1} {2} m={3} w={4}u l={5}u".format(self.tx_type,
                                                                    " ".join(self.pins),
                                                                    spice[self.tx_type],
                                                                    self.mults,
                                                                    self.gate_width,
                                                                    drc["minwidth_poly"]))
        self.spice.append(".ENDS {0}".format(self.name))

    def setup_layout_constants(self):
        # usually contacted poly will limit the spacing, but it could be poly
        # spacing in some weird technology.
        self.mults_poly_to_poly = max(2 * drc["contact_to_poly"] + drc["minwidth_contact"],
                                      drc["poly_to_poly"])
        outeractive_to_contact = max(drc["active_enclosure_contact"],
                                    (drc["minwidth_active"] - drc["minwidth_contact"]) / 2)
        self.active_width = (2 * (outeractive_to_contact + drc["minwidth_contact"] 
                                     + drc["contact_to_poly"])
                                 + drc["minwidth_poly"]
                                 + (self.mults - 1) * (self.mults_poly_to_poly 
                                                           + drc["minwidth_poly"]))
        self.active_height = max(drc["minarea_active"] / self.active_width,
                                 self.gate_width)
        self.poly_width = drc["minwidth_poly"]  # horizontal
        self.poly_height = max(drc["minarea_poly"] / self.poly_width,
                               self.gate_width 
                                   + 2 * drc["poly_extend_active"])  # vertical
        self.well_width = (self.active_width
                               + 2 * (drc["well_enclosure_active"]))
        self.well_height = max(self.gate_width + 2 * (drc["well_enclosure_active"]),
                               drc["minwidth_well"])


    def connect_fingered_poly(self):
        poly_connect_length = self.poly_positions[-1].x + self.poly_width \
                              - self.poly_positions[0].x
        poly_connect_position = self.poly_positions[0] - vector(0, self.poly_width)
        if len(self.poly_positions) > 1:
            self.remove_layout_pin("G") # only keep the main pin
            self.add_layout_pin(text="G",
                                layer="poly",
                                offset=poly_connect_position,
                                width=poly_connect_length,
                                height=drc["minwidth_poly"])

            self.poly_connect_index = len(self.objs) - 1

            

    def pairwise(self, iterable):
        #"s -> (s0,s1), (s1,s2), (s2, s3), ..."
        from itertools import tee, izip
        a, b = tee(iterable)
        next(b, None)
        return izip(a, b)

    def determine_active_wire_location(self):
        self.determine_source_wire()
        self.determine_drain_wire()

    def determine_source_wire(self):
        self.source_positions = []
        source_contact_pos = self.active_contact_positions[0:][::2]  # even indexes
        for a, b in self.pairwise(source_contact_pos):
            correct=vector(0.5 * (self.active_contact.width - 
                                  drc["minwidth_metal1"] + drc["minwidth_contact"]),
                           0.5 * (self.active_contact.height - drc["minwidth_contact"]) 
                               - drc["metal1_extend_contact"])
            connected=vector(b.x + drc["minwidth_metal1"],
                             a.y + self.active_contact.height + drc["metal1_to_metal1"])  
            self.source_positions.append(a + correct)
            self.source_positions.append(vector(a.x + correct.x, connected.y))
            self.source_positions.append(vector(b.x + correct.x,
                                                connected.y + 0.5 * drc["minwidth_metal2"]))
            self.source_positions.append(b + correct)

    def determine_drain_wire(self):
        self.drain_positions = []
        drain_contact_pos = self.active_contact_positions[1:][::2]  # odd indexes
        for c, d in self.pairwise(drain_contact_pos):
            correct = vector(0.5*(self.active_contact.width 
                                  - drc["minwidth_metal1"] 
                                  + drc["minwidth_contact"]),
                             0.5*(self.active_contact.height - drc["minwidth_contact"])
                               - drc["metal1_extend_contact"])
            connected = vector(d.x + drc["minwidth_metal1"], c.y - drc["metal1_to_metal1"])
            self.drain_positions.append(vector(c + correct))
            self.drain_positions.append(vector(c.x + correct.x, connected.y))
            self.drain_positions.append(vector(d.x + correct.x,
                                               connected.y - 0.5 * drc["minwidth_metal1"]))
            self.drain_positions.append(vector(d + correct))

    def connect_fingered_active(self):
        self.determine_active_wire_location()
        # allows one to connect the source and drains
        self.source_connect_index = None
        if self.source_positions:
            self.remove_layout_pin("S") # remove the individual connections
            self.source_positions = path.create_rectilinear_route(self.source_positions)
            self.add_path(("metal1"), self.source_positions)
            # The source positions are odd since the second one is always redundant
            # so we must use the THIRD one
            self.add_center_layout_pin(text="S",
                                       layer="metal1",
                                       start=self.source_positions[2]-vector(0.5*drc["minwidth_metal1"],0),
                                       end=self.source_positions[-2]+vector(0.5*drc["minwidth_metal1"],0))
            self.source_connect_index = len(self.insts) - 1
        self.drain_connect_index = None
        if self.drain_positions:
            self.remove_layout_pin("D") # remove the individual connections
            self.drain_positions = path.create_rectilinear_route(self.drain_positions)
            self.add_path(("metal1"), self.drain_positions)
            # The source positions are odd since the second one is always redundant            
            # so we must use the THIRD one
            self.add_center_layout_pin(text="D",
                                       layer="metal1",
                                       start=self.drain_positions[2]-vector(0.5*drc["minwidth_metal1"],0),
                                       end=self.drain_positions[-2]+vector(0.5*drc["minwidth_metal1"],0))
            self.drain_connect_index = len(self.insts) - 1
            
    def add_poly(self):
        # left_most poly
        poly_xoffset = self.active_contact.via_layer_position.x \
                       + drc["minwidth_contact"] + drc["contact_to_poly"]
        poly_yoffset = -drc["poly_extend_active"]
        self.poly_positions = []
        # following poly(s)
        for i in range(0, self.mults):
            if self.connect_poly:
                # Add the rectangle in case we remove the pin when joining fingers
                self.add_rect(layer="poly",
                              offset=[poly_xoffset, poly_yoffset],
                              width=self.poly_width,
                              height=self.poly_height)
            else:
                self.add_layout_pin(text="G",
                                    layer="poly",
                                    offset=[poly_xoffset, poly_yoffset],
                                    width=self.poly_width,
                                    height=self.poly_height)
            self.poly_positions.append(vector(poly_xoffset, poly_yoffset))
            poly_xoffset += self.mults_poly_to_poly + drc["minwidth_poly"]

    def add_active(self):
        """Adding the diffusion (active region = diffusion region)"""
        offset = self.active_position = [0, 0]
        self.add_rect(layer="active",
                      offset=offset,
                      width=self.active_width,
                      height=self.active_height)

    def add_implants(self):
        if self.tx_type == "nmos":
            self.add_nmos_implants()
        elif self.tx_type == "pmos":
            self.add_pmos_implants()

    def add_nmos_implants(self):
        offset = self.pwell_position = [-drc["well_enclosure_active"], -drc["well_enclosure_active"]]
        if info["has_pwell"]:
            self.add_rect(layer="pwell",
                          offset=offset,
                          width=self.well_width,
                          height=self.well_height)
            self.add_rect(layer="vtg",
                          offset=offset,
                          width=self.well_width,
                          height=self.well_height)
        xlength = self.active_width
        ylength = self.active_height
        self.add_rect(layer="nimplant",
                      offset=self.active_position,
                      width=xlength,
                      height=ylength)

    def add_pmos_implants(self):
        offset = self.nwell_position = [-drc["well_enclosure_active"], -drc["well_enclosure_active"]]
        if info["has_nwell"]:
            self.add_rect(layer="nwell",
                          offset=offset,
                          width=self.well_width,
                          height=self.well_height)
            self.add_rect(layer="vtg",
                          offset=offset,
                          width=self.well_width,
                          height=self.well_height)
        xlength = self.active_width
        ylength = self.active_height
        self.add_rect(layer="pimplant",
                      offset=self.active_position,
                      width=xlength,
                      height=ylength)

    def calculate_num_contacts(self):
        """ Calculates the possible number of source/drain contacts in a column """
        # Used for over-riding the contact dimensions
        possible_length = self.active_height - 2 * drc["active_extend_contact"]
        y = 1
        while True:
            temp_length = (y * drc["minwidth_contact"]) + ((y - 1) * drc["contact_to_contact"])
            if round(possible_length - temp_length, 6) < 0:
                return y - 1
            y += 1

    def add_active_contacts(self):
        self.active_contact_positions = []

        # left_most contact column
        contact_xoffset = 0
        contact_yoffset = (self.active_height - self.active_contact.height) / 2
        offset = vector(contact_xoffset, contact_yoffset)
        contact=self.add_contact(layers=("active", "contact", "metal1"),
                                 offset=offset,
                                 size=(1, self.num_contacts))
        # source are even
        if self.connect_active:
            # Add this in case the pins get removed when fingers joined
            self.add_rect(layer="metal1",
                          offset=offset+contact.second_layer_position,
                          width=contact.second_layer_width,
                          height=contact.second_layer_height)
        else:
            self.add_layout_pin(text="S",
                                layer="metal1",
                                offset=offset+contact.second_layer_position,
                                width=contact.second_layer_width,
                                height=contact.second_layer_height)
        self.active_contact_positions.append(offset)

        # middle contact columns
        for i in range(self.mults - 1):
            contact_xoffset = self.poly_positions[i].x + self.poly_width \
                              + (self.mults_poly_to_poly / 2) \
                              - (drc["minwidth_contact"] / 2) - \
                              self.active_contact.via_layer_position.x
            offset = vector(contact_xoffset, contact_yoffset)
            contact=self.add_contact(layers=("active", "contact", "metal1"),
                                     offset=offset,
                                     size=(1, self.num_contacts))
            # source are even, drain are odd
            if self.connect_active:
                # Add this in case the pins get removed when fingers joined
                self.add_rect(layer="metal1",
                              offset=offset+contact.second_layer_position,
                              width=contact.second_layer_width,
                              height=contact.second_layer_height)
            else:
                name = "S" if i%2==1 else "D"
                self.add_layout_pin(text=name,
                                    layer="metal1",
                                    offset=offset+contact.second_layer_position,
                                    width=contact.second_layer_width,
                                    height=contact.second_layer_height)

            self.active_contact_positions.append(offset)

        # right_most contact column
        contact_xoffset = self.poly_positions[-1].x \
                          + self.poly_width + drc["contact_to_poly"] - \
                          self.active_contact.via_layer_position.x
        offset = vector(contact_xoffset, contact_yoffset)
        contact=self.add_contact(layers=("active", "contact", "metal1"),
                                 offset=offset,
                                 size=(1, self.num_contacts))
        # source are even, drain are odd
        if self.connect_active:
            self.add_rect(layer="metal1",
                          offset=offset+contact.second_layer_position,
                          width=contact.second_layer_width,
                          height=contact.second_layer_height)
        else:
            name = "D" if self.mults%2==1 else "S" 
            self.add_layout_pin(text=name,
                                layer="metal1",
                                offset=offset+contact.second_layer_position,
                                width=contact.second_layer_width,
                                height=contact.second_layer_height)
        # Add this in case the pins get removed when fingers joined
        self.active_contact_positions.append(offset)


    # def remove_drain_connect(self):
    #     debug.info(3,"Removing drain on {}".format(self.name))
    #     # FIXME: This is horrible exception handling!
    #     try:
    #         del self.insts[self.drain_connect_index]
    #         del self.drain_connect_index
    #         self.offset_all_coordinates()
    #         # change the name so it is unique
    #         self.name = self.name + "_rd"
    #     except:
    #         pass

    # def remove_source_connect(self):
    #     debug.info(3,"Removing source on {}".format(self.name))
    #     # FIXME: This is horrible exception handling!
    #     try:
    #         del self.insts[self.source_connect_index]
    #         del self.source_connect_index
    #         if isinstance(self.drain_connect_index, int):
    #             self.drain_connect_index -= 1
    #         self.offset_all_coordinates()
    #         # change the name so it is unique
    #         self.name = self.name + "_rs"
    #     except:
    #         pass

    # def remove_poly_connect(self):
    #     # FIXME: This is horrible exception handling!
    #     try:
    #         del self.objs[self.poly_connect_index]
    #         self.offset_all_coordinates()
    #         # change the name so it is unique
    #         self.name = self.name + "_rp"
    #     except:
    #         pass
