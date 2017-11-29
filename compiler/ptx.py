import design
import debug
from tech import drc, info, spice
from vector import vector
from contact import contact
import path
import re

class ptx(design.design):
    """
    This module generates gds and spice of a parametrically NMOS or
    PMOS sized transistor.  Pins are accessed as D, G, S, B.  Width is
    the transistor width. Mults is the number of transistors of the
    given width. Total width is therefore mults*width.  Options allow
    you to connect the fingered gates and active for parallel devices.

    """
    def __init__(self, width=drc["minwidth_tx"], mults=1, tx_type="nmos", connect_active=False, connect_poly=False, num_contacts=None):
        # We need to keep unique names because outputting to GDSII
        # will use the last record with a given name. I.e., you will
        # over-write a design in GDS if one has and the other doesn't
        # have poly connected, for example.
        name = "{0}_m{1}_w{2}".format(tx_type, mults, width)
        if connect_active:
            name += "_a"
        if connect_poly:
            name += "_p"
        if num_contacts:
            name += "_c{}".format(num_contacts)
        # replace periods with underscore for newer spice compatibility
        name=re.sub('\.','_',name)

        design.design.__init__(self, name)
        debug.info(3, "create ptx2 structure {0}".format(name))

        self.tx_type = tx_type
        self.mults = mults
        self.tx_width = width
        self.connect_active = connect_active
        self.connect_poly = connect_poly
        self.num_contacts = num_contacts

        self.add_pins()
        self.create_spice()
        self.create_layout()
        # for run-time, we won't check every transitor DRC independently
        # but this may be uncommented for debug purposes
        #self.DRC()

    def add_pins(self):
        self.add_pin_list(["D", "G", "S", "B"])

    def create_layout(self):
        self.setup_layout_constants()
        self.add_active()
        self.add_well_implant()  
        self.add_poly()
        self.add_active_contacts()

        # offset this BEFORE we add the active/poly connections
        #self.offset_all_coordinates()
        
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
        
    # def offset_all_coordinates(self):
    #     offset = self.find_lowest_coords()
    #     self.offset_attributes(offset)
    #     self.translate_all(offset)

    #     # We can do this in ptx because we have offset all modules it uses.
    #     # Is this really true considering the paths that connect the src/drain?
    #     self.height = max(max(obj.offset.y + obj.height for obj in self.objs),
    #                               max(inst.offset.y + inst.mod.height for inst in self.insts))
    #     self.width = max(max(obj.offset.x + obj.width for obj in self.objs),
    #                              max(inst.offset.x + inst.mod.width for inst in self.insts))

    def create_spice(self):
        self.spice.append("\n.SUBCKT {0} {1}".format(self.name,
                                                     " ".join(self.pins)))
        self.spice.append("M{0} {1} {2} m={3} w={4}u l={5}u".format(self.tx_type,
                                                                    " ".join(self.pins),
                                                                    spice[self.tx_type],
                                                                    self.mults,
                                                                    self.tx_width,
                                                                    drc["minwidth_poly"]))
        self.spice.append(".ENDS {0}".format(self.name))

    def setup_layout_constants(self):
        """
        Pre-compute some handy layout parameters.
        """

        if self.num_contacts==None:
            self.num_contacts=self.calculate_num_contacts()
        
        # This is not actually instantiated but used for calculations
        self.active_contact = contact(layer_stack=("active", "contact", "metal1"),
                                      dimensions=(1, self.num_contacts))

        # Standard DRC rules
        self.active_width = drc["minwidth_active"]
        self.contact_width = drc["minwidth_contact"]
        self.poly_width = drc["minwidth_poly"]
        self.poly_to_active = drc["poly_to_active"]
        self.poly_extend_active = drc["poly_extend_active"]
        
        # The contacted poly pitch (or uncontacted in an odd technology)
        self.poly_pitch = max(2*drc["contact_to_poly"] + self.contact_width + self.poly_width,
                              drc["poly_to_poly"])

        # The contacted poly pitch (or uncontacted in an odd technology)
        self.contact_pitch = 2*drc["contact_to_poly"] + self.contact_width + self.poly_width
        
        # The enclosure of an active contact. Not sure about second term.
        active_enclose_contact = max(drc["active_enclosure_contact"],
                                     (self.active_width - self.contact_width)/2)
        # This is the distance from the edge of poly to the contacted end of active
        self.end_to_poly = active_enclose_contact + self.contact_width + drc["contact_to_poly"]
        

        # Active width is determined by enclosure on both ends and contacted pitch,
        # at least one poly and n-1 poly pitches
        self.active_width = 2*self.end_to_poly + self.poly_width + (self.mults - 1)*self.poly_pitch

        # Active height is just the transistor width
        self.active_height = self.tx_width

        # Poly height must include poly extension over active
        self.poly_height = self.tx_width + 2*self.poly_extend_active

        # Well enclosure of active, ensure minwidth as well
        self.well_width = max(self.active_width + 2*drc["well_enclosure_active"],
                              drc["minwidth_well"])
        self.well_height = max(self.tx_width + 2*drc["well_enclosure_active"],
                               drc["minwidth_well"])

        # The active offset is due to the well extension
        self.active_offset = vector([drc["well_enclosure_active"]]*2)

        # This is the center of the first active contact offset (centered vertically)
        self.contact_offset = self.active_offset + vector(active_enclose_contact + 0.5*self.contact_width,
                                                          0.5*self.active_height)
                                     
        
        # Min area results are just flagged for now.
        debug.check(self.active_width*self.active_height>=drc["minarea_active"],"Minimum active area violated.")
        # We do not want to increase the poly dimensions to fix an area problem as it would cause an LVS issue.
        debug.check(self.poly_width*self.poly_height>=drc["minarea_poly"],"Minimum poly area violated.")

    def connect_fingered_poly(self, poly_positions):
        """
        Connect together the poly gates and create the single gate pin.
        The poly positions are the center of the poly gates
        and we will add a single horizontal connection.
        """
        # Nothing to do if there's one poly gate
        if len(poly_positions) == 1:
            return

        # The width of the poly is from the left-most to right-most poly gate
        poly_width = poly_positions[-1].x - poly_positions[0].x + self.poly_width
        # This can be limited by poly to active spacing or the poly extension
        distance_below_active = self.poly_width + max(self.poly_to_active,0.5*self.poly_height)
        poly_offset = poly_positions[0] - vector(0.5*self.poly_width, distance_below_active)

        # Remove the old pin and add the new one
        self.remove_layout_pin("G") # only keep the main pin
        self.add_layout_pin(text="G",
                            layer="poly",
                            offset=poly_offset,
                            width=poly_width,
                            height=drc["minwidth_poly"])


            

    def pairwise(self, iterable):
        """
        Create an iterable set of pairs from a set:
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        """
        from itertools import tee, izip
        a, b = tee(iterable)
        next(b, None)
        return izip(a, b)


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

        return source_positions

    def determine_drain_wire(self, contact_positions):
        drain_positions = []
        drain_contact_pos = contact_positions[1:][::2]  # odd indexes
        for c, d in self.pairwise(drain_contact_pos):
            correct = vector(0.5*(self.active_contact.width 
                                  - drc["minwidth_metal1"] + drc["minwidth_contact"]),
                             0.5*(self.active_contact.height - drc["minwidth_contact"])
                               - drc["metal1_extend_contact"])
            connected = vector(d.x + drc["minwidth_metal1"], c.y - drc["metal1_to_metal1"])
            self.drain_positions.append(vector(c + correct))
            self.drain_positions.append(vector(c.x + correct.x, connected.y))
            self.drain_positions.append(vector(d.x + correct.x,
                                               connected.y - 0.5 * drc["minwidth_metal1"]))
            self.drain_positions.append(vector(d + correct))

        return drain_positions

            
    def connect_fingered_active(self, drain_positions, source_positions):
        """
        Connect each contact  up/down to a source or drain pin
        """
        
        # This is the distance that we must route up or down from the center
        # of the contacts to avoid DRC violations to the other contacts
        pin_offset = vector(0, 0.5*self.active_contact.second_layer_height \
                            + drc["metal1_to_metal1"] + 0.5*drc["minwidth_metal1"])
        # This is the width of a contact to extend the ends of the pin
        end_offset = vector(self.active_contact.second_layer_width/2,0)
        
        if source_positions: # if not an empty set
            self.remove_layout_pin("S") # remove the individual connections
            # Add each vertical segment
            for a in source_positions:
                self.add_path(("metal1"), [a,a+pin_offset])
            # Add a single horizontal pin
            self.add_center_layout_pin_segment(text="S",
                                               layer="metal1",
                                               start=source_positions[0]+pin_offset-end_offset,
                                               end=source_positions[-1]+pin_offset+end_offset)

        if drain_positions: # if not an empty set
            self.remove_layout_pin("D") # remove the individual connections
            # Add each vertical segment
            for a in drain_positions:
                self.add_path(("metal1"), [a,a-pin_offset])
            # Add a single horizontal pin
            self.add_center_layout_pin_segment(text="D",
                                               layer="metal1",
                                               start=drain_positions[0]-pin_offset-end_offset,
                                               end=drain_positions[-1]-pin_offset+end_offset)
            
    def add_poly(self):
        """
        Add the poly gates(s) and (optionally) connect them.
        """
        # poly is one contacted spacing from the end and down an extension
        poly_offset = vector(self.active_offset.x + self.end_to_poly + 0.5*self.poly_width,0.5*self.poly_height)

        # poly_positions are the bottom center of the poly gates
        poly_positions = []
        
        for i in range(0, self.mults):
            if self.connect_poly:
                # Add the rectangle in case we remove the pin when joining fingers
                self.add_center_rect(layer="poly",
                                     offset=poly_offset,
                                     height=self.poly_height,
                                     width=self.poly_width)
            else:
                self.add_center_layout_pin_rect(text="G",
                                                layer="poly",
                                                offset=poly_offset,
                                                height=self.poly_height,
                                                width=self.poly_width)
            poly_positions.append(poly_offset)
            poly_offset = poly_offset + vector(self.poly_pitch,0)

        if self.connect_poly:
            self.connect_fingered_poly(poly_positions)
            
    def add_active(self):
        """ 
        Adding the diffusion (active region = diffusion region) 
        """
        self.add_rect(layer="active",
                      offset=self.active_offset,
                      width=self.active_width,
                      height=self.active_height)

    def add_well_implant(self):
        """
        Add an (optional) well and implant for the type of transistor.
        """
        if self.tx_type == "nmos":
            implant_type = "n"
            well_type = "p"
        elif self.tx_type == "pmos":
            implant_type = "p"
            well_type = "n"
        else:
            self.error("Invalid transitor type.",-1)
            
        if info["has_{}well".format(well_type)]:
            self.add_rect(layer="{}well".format(well_type),
                          offset=(0,0),
                          width=self.well_width,
                          height=self.well_height)
            self.add_rect(layer="vtg",
                          offset=(0,0),
                          width=self.well_width,
                          height=self.well_height)
        self.add_rect(layer="{}implant".format(implant_type),
                      offset=self.active_offset,
                      width=self.active_width,
                      height=self.active_height)


    def calculate_num_contacts(self):
        """ 
        Calculates the possible number of source/drain contacts in a finger.
        For now, it is hard set as 1.
        """
        return 1


    def get_contact_positions(self):
        """
        Create a list of the centers of drain and source contact positions.
        """
        # The first one will always be a source
        source_positions = [self.contact_offset]
        drain_positions = []

        # For all but the last finger...
        for i in range(self.mults-1):
            if i%2:
                # It's a source... so offset from previous drain.
                source_positions.append(drain_positions[-1] + vector(self.contact_pitch,0))
            else:
                # It's a drain... so offset from previous source.
                drain_positions.append(source_positions[-1] + vector(self.contact_pitch,0))

        # The last one will always be a drain
        drain_positions.append(source_positions[-1] + vector(self.contact_pitch,0))            

        return [source_positions,drain_positions]
        
    def add_active_contacts(self):
        """
        Add the active contacts to the transistor.
        """

        [source_positions,drain_positions] = self.get_contact_positions()

        for pos in source_positions:
            contact=self.add_center_contact(layers=("active", "contact", "metal1"),
                                            offset=pos,
                                            size=(1, self.num_contacts))
            if self.connect_active:
                # Add this in case the pins get removed when fingers joined
                self.add_center_rect(layer="metal1",
                                     offset=pos,
                                     width=contact.second_layer_width,
                                     height=contact.second_layer_height)
            else:
                self.add_center_layout_pin_rect(text="S",
                                                layer="metal1",
                                                offset=pos,
                                                width=contact.second_layer_width,
                                                height=contact.second_layer_height)

                
        for pos in drain_positions:
            contact=self.add_center_contact(layers=("active", "contact", "metal1"),
                                            offset=pos,
                                            size=(1, self.num_contacts))
            if self.connect_active:
                # Add this in case the pins get removed when fingers joined
                self.add_center_rect(layer="metal1",
                                     offset=pos,
                                     width=contact.second_layer_width,
                                     height=contact.second_layer_height)
            else:
                self.add_center_layout_pin_rect(text="D",
                                                layer="metal1",
                                                offset=pos,
                                                width=contact.second_layer_width,
                                                height=contact.second_layer_height)
                
        if self.connect_active:
            self.connect_fingered_active(drain_positions, source_positions)

        

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
