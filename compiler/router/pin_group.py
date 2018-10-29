from pin_layout import pin_layout
from vector3d import vector3d
from vector import vector
from tech import drc
import debug

class pin_group:
    """
    A class to represent a group of rectangular design pin. 
    It requires a router to define the track widths and blockages which 
    determine how pin shapes get mapped to tracks. 
    """
    def __init__(self, name, pin_shapes, router):
        self.name = name
        # Flag for when it is routed
        self.routed = False
        # This is a list because we can have a pin group of disconnected sets of pins
        # and these are represented by separate lists
        if pin_shapes:
            self.pins = [pin_shapes]
        else:
            self.pins = []
    
        self.router = router
        # These are the corresponding pin grids for each pin group.
        self.grids = set()
        # The corresponding set of partially blocked grids for each pin group.
        # These are blockages for other nets but unblocked for routing this group.
        self.blockages = set()

    def set_routed(self, value=True):
        self.routed = value

    def is_routed(self):
        return self.routed
        
    def pins_enclosed(self):
        """
        Check if all of the pin shapes are enclosed.
        Does not check if the DRC is correct, but just touching.
        """
        for pin_list in self.pins:
            pin_is_enclosed=False
            for pin in pin_list:
                if pin_is_enclosed:
                    break
                for encosure in self.enclosures:
                    if pin.overlaps(enclosure):
                        pin_is_enclosed=True
                        break
            else:
                return False
            
        return True
        
    def remove_redundant_shapes(self, pin_list):
        """
        Remove any pin layout that is contained within another.
        """
        local_debug = True
        if local_debug:
            debug.info(0,"INITIAL: {}".format(pin_list))
        
        # Make a copy of the list to start
        new_pin_list = pin_list.copy()

        remove_indices = set()
        # This is n^2, but the number is small
        for index1,pin1 in enumerate(pin_list):
            if index1 in remove_indices:
                continue
            
            for index2,pin2 in enumerate(pin_list):
                # Can't contain yourself
                if pin1 == pin2:
                    continue
                if index2 in remove_indices:
                    continue
                
                if pin2.contains(pin1):
                    if local_debug:
                        debug.info(0,"{0} contains {1}".format(pin1,pin2))
                        remove_indices.add(index2)
        # Remove them in decreasing order to not invalidate the indices
        for i in sorted(remove_indices, reverse=True):
            del new_pin_list[i]
                        
        if local_debug:
            debug.info(0,"FINAL  : {}".format(new_pin_list))
            
        return new_pin_list

    # FIXME: This relies on some technology parameters from router which is not clean.
    def compute_enclosures(self):
        """
        Find the minimum rectangle enclosures of the given tracks.
        """
        # Enumerate every possible enclosure
        pin_list = []
        for seed in self.grids:
            (ll, ur) = self.enclose_pin_grids(seed)
            enclosure = self.router.compute_pin_enclosure(ll, ur, ll.z)
            pin_list.append(enclosure)

        return self.remove_redundant_shapes(pin_list)
        
    def compute_enclosure(self, pin, enclosure):
        """ 
        Compute an enclosure to connect the pin to the enclosure shape. 
        This assumes the shape will be the dimension of the pin.
        """
        if pin.xoverlaps(enclosure):
            # Is it vertical overlap, extend pin shape to enclosure
            plc = pin.lc()
            prc = pin.rc()
            elc = enclosure.lc()
            erc = enclosure.rc()
            ymin = min(plc.y,elc.y)
            ymax = max(plc.y,elc.y)
            ll = vector(plc.x, ymin)
            ur = vector(prc.x, ymax)
            print(pin,enclosure,ll,ur)
            p = pin_layout(pin.name, [ll, ur], pin.layer) 
        elif pin.yoverlaps(enclosure):
            # Is it horizontal overlap, extend pin shape to enclosure
            pbc = pin.bc()
            puc = pin.uc()
            ebc = enclosure.bc()
            euc = enclosure.uc()
            xmin = min(pbc.x,ebc.x)
            xmax = max(pbc.x,ebc.x)
            ll = vector(xmin, pbc.y)
            ur = vector(xmax, puc.y)
            p = pin_layout(pin.name, [ll, ur], pin.layer)
        else:
            # Neither, so we must do a corner-to corner
            pc = pin.center()
            ec = enclosure.center()
            xmin = min(pc.x, ec.x)
            xmax = max(pc.x, ec.x)
            ymin = min(pc.y, ec.y)
            ymax = max(pc.y, ec.y)
            ll = vector(xmin, ymin)
            ur = vector(xmax, ymax)
            p = pin_layout(pin.name, [ll, ur], pin.layer)

        return p

    def find_smallest_connector(self, enclosure_list):
        """
        Compute all of the connectors between non-overlapping pins and enclosures.
        Return the smallest.
        """
        smallest = None
        for pin_list in self.pins:
            for pin in pin_list:
                for enclosure in enclosure_list:
                    new_enclosure = self.compute_enclosure(pin, enclosure)
                    if smallest == None or new_enclosure.area()<smallest.area():
                        smallest = new_enclosure
                    
        return smallest

    def find_smallest_overlapping(self, pin_list, shape_list):
        """
        Find the smallest area shape in shape_list that overlaps with any 
        pin in pin_list by a min width.
        """

        smallest_shape = None
        for pin in pin_list:
            overlap_shape = self.find_smallest_overlapping_pin(pin,shape_list)
            if overlap_shape:
                overlap_length = pin.overlap_length(overlap_shape)
                if smallest_shape == None or overlap_shape.area()<smallest_shape.area():
                    smallest_shape = overlap_shape
                        
        return smallest_shape


    def find_smallest_overlapping_pin(self, pin, shape_list):
        """
        Find the smallest area shape in shape_list that overlaps with any 
        pin in pin_list by a min width.
        """

        smallest_shape = None
        zindex=self.router.get_zindex(pin.layer_num)
        (min_width,min_space) = self.router.get_layer_width_space(zindex)

        # Now compare it with every other shape to check how much they overlap
        for other in shape_list:
            overlap_length = pin.overlap_length(other)
            if overlap_length > min_width:
                if smallest_shape == None or other.area()<smallest_shape.area():
                    smallest_shape = other
                        
        return smallest_shape
    
    def overlap_any_shape(self, pin_list, shape_list):
        """
        Does the given pin overlap any of the shapes in the pin list.
        """
        for pin in pin_list:
            for other in shape_list:
                if pin.overlaps(other):
                    return True

        return False

    
    def max_pin_layout(self, pin_list):
        """ 
        Return the max area pin_layout
        """
        biggest = pin_list[0]
        for pin in pin_list:
            if pin.area() > biggest.area():
                biggest = pin
                
        return pin

    def enclose_pin_grids(self, ll):
        """
        This encloses a single pin component with a rectangle
        starting with the seed and expanding right until blocked
        and then up until blocked.
        """

        # We may have started with an empty set
        if not self.grids:
            return None

        # Start with the ll and make the widest row
        row = [ll]
        # Move right while we can
        while True:
            right = row[-1] + vector3d(1,0,0)
            # Can't move if not in the pin shape 
            if right in self.grids and right not in self.router.blocked_grids:
                row.append(right)
            else:
                break
        # Move up while we can
        while True:
            next_row = [x+vector3d(0,1,0) for x in row]
            for cell in next_row:
                # Can't move if any cell is not in the pin shape 
                if cell not in self.grids or cell in self.router.blocked_grids:
                    break
            else:
                row = next_row
                # Skips the second break
                continue
            # Breaks from the nested break
            break

        # Add a shape from ll to ur
        ur = row[-1]
        return (ll,ur)

    
    def enclose_pin(self):
        """
        If there is one set of connected pin shapes, 
        this will find the smallest rectangle enclosure that overlaps with any pin.
        If there is not, it simply returns all the enclosures.
        """
        # Compute the enclosure pin_layout list of the set of tracks
        enclosure_list = self.compute_enclosures()

        # A single set of connected pins is easy, so use the optimized set
        if len(self.pins)==1:
            smallest = self.find_smallest_overlapping(self.pins[0],enclosure_list)
            if smallest:
                self.enclosures=[smallest]
            # else:
            #     connector=self.find_smallest_connector(enclosure_list)
            #     if connector:
            #         self.enclosures=[connector]
            #     else:
            #         debug.error("Unable to enclose pin {}".format(self.pins),-1)
        else:
            # Multiple pins is hard, so just use all of the enclosure shapes!
            # At least none of these are redundant shapes though.
            self.enclosures = enclosure_list
            
        debug.info(2,"Computed enclosure(s) {0}\n  {1}\n  {2}\n  {3}".format(self.name, self.pins, self.grids, self.enclosures))

            
    def add_enclosure(self, cell):
        """
        Add the enclosure shape to the given cell.
        """
        for enclosure in self.enclosures:
            debug.info(2,"Adding enclosure {0} {1}".format(self.name, enclosure))  
            cell.add_rect(layer=enclosure.layer,
                          offset=enclosure.ll(),
                          width=enclosure.width(),
                          height=enclosure.height())
        

    
    
    def adjacent(self, other):
        """ 
        Chck if the two pin groups have at least one adjacent pin grid.
        """
        # We could optimize this to just check the boundaries
        for g1 in self.grids:
            for g2 in other.grids:
                if g1.adjacent(g2):
                    return True

        return False

    def convert_pin(self, router):
        #print("PG  ",pg)
        # Keep the same groups for each pin
        pin_set = set()
        blockage_set = set()
        print("PINLIST:",self.pins)
        for pin_list in self.pins:
            for pin in pin_list:
                debug.info(2,"  Converting {0}".format(pin))
                # Determine which tracks the pin overlaps 
                pin_in_tracks=router.convert_pin_to_tracks(self.name, pin)
                pin_set.update(pin_in_tracks)
                # Blockages will be a super-set of pins since it uses the inflated pin shape.
                blockage_in_tracks = router.convert_blockage(pin) 
                blockage_set.update(blockage_in_tracks)

        # If we have a blockage, we must remove the grids
        # Remember, this excludes the pin blockages already
        shared_set = pin_set & router.blocked_grids
        if len(shared_set)>0:
            debug.info(2,"Removing pins {}".format(shared_set))
        shared_set = blockage_set & router.blocked_grids
        if len(shared_set)>0:
            debug.info(2,"Removing blocks {}".format(shared_set))
        pin_set.difference_update(router.blocked_grids)
        blockage_set.difference_update(router.blocked_grids)
        debug.info(2,"     pins   {}".format(pin_set))
        debug.info(2,"     blocks {}".format(blockage_set))
                       
        # At least one of the groups must have some valid tracks
        if (len(pin_set)==0 and len(blockage_set)==0):
            self.write_debug_gds("blocked_pin.gds")
            debug.error("Unable to find unblocked pin on grid.")

        # We need to route each of the components, so don't combine the groups
        self.grids = pin_set | blockage_set

        # Add all of the partial blocked grids to the set for the design
        # if they are not blocked by other metal
        #partial_set = blockage_set - pin_set
        #self.blockages = partial_set

        # We should not have added the pins to the blockages,
        # but remove them just in case
        # Partial set may still be in the blockages if there were
        # other shapes disconnected from the pins that were also overlapping
        #route.blocked_grids.difference_update(pin_set)
