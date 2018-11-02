import sys
import gdsMill
from tech import drc,GDS
import math
import debug
from router_tech import router_tech
from pin_layout import pin_layout
from pin_group import pin_group
from vector import vector
from vector3d import vector3d 
from globals import OPTS
from pprint import pformat
import grid_utils

class router(router_tech):
    """
    A router class to read an obstruction map from a gds and plan a
    route on a given layer. This is limited to two layer routes.
    It populates blockages on a grid class.
    """

    def __init__(self, layers, design, gds_filename=None):
        """
        This will instantiate a copy of the gds file or the module at (0,0) and
        route on top of this. The blockages from the gds/module will be considered.
        """
        router_tech.__init__(self, layers)
        
        self.cell = design

        # If didn't specify a gds blockage file, write it out to read the gds
        # This isn't efficient, but easy for now
        if not gds_filename:
            gds_filename = OPTS.openram_temp+"temp.gds"
            self.cell.gds_write(gds_filename)
        
        # Load the gds file and read in all the shapes
        self.layout = gdsMill.VlsiLayout(units=GDS["unit"])
        self.reader = gdsMill.Gds2reader(self.layout)
        self.reader.loadFromFile(gds_filename)
        self.top_name = self.layout.rootStructureName

        ### The pin data structures
        # A map of pin names to a set of pin_layout structures
        self.pins = {}
        # This is a set of all pins (ignoring names) so that can quickly not create blockages for pins
        # (They will be blocked based on the names we are routing)
        self.all_pins = set()
        
        # A map of pin names to a list of pin groups
        self.pin_groups = {}
        
        ### The blockage data structures
        # A list of metal shapes (using the same pin_layout structure) that are not pins but blockages.
        self.blockages=[]
        # The corresponding set of blocked grids for above pin shapes
        self.blocked_grids = set()
        
        ### The routed data structures
        # A list of paths that have been "routed"
        self.paths = []
        # A list of path blockages (they might be expanded for wide metal DRC)
        self.path_blockages = []

        # The boundary will determine the limits to the size of the routing grid
        self.boundary = self.layout.measureBoundary(self.top_name)
        # These must be un-indexed to get rid of the matrix type
        self.ll = vector(self.boundary[0][0], self.boundary[0][1])
        self.ur = vector(self.boundary[1][0], self.boundary[1][1])

    def clear_pins(self):
        """
        Convert the routed path to blockages.
        Keep the other blockages unchanged.
        """
        self.pins = {}
        self.all_pins = set()
        self.pin_groups = {}        
        # DO NOT clear the blockages as these don't change
        self.rg.reinit()

        
    def set_top(self,top_name):
        """ If we want to route something besides the top-level cell."""
        self.top_name = top_name

        
    def is_wave(self,path):
        """
        Determines if this is a multi-track width wave (True) or a normal route (False)
        """
        return len(path[0])>1
    

    def retrieve_pins(self,pin_name):
        """
        Retrieve the pin shapes from the layout.
        """
        shape_list=self.layout.getAllPinShapesByLabel(str(pin_name))
        pin_set = set()
        for shape in shape_list:
            (name,layer,boundary)=shape
            # GDSMill boundaries are in (left, bottom, right, top) order
            # so repack and snap to the grid
            ll = vector(boundary[0],boundary[1]).snap_to_grid()
            ur = vector(boundary[2],boundary[3]).snap_to_grid()
            rect = [ll,ur]
            pin = pin_layout(pin_name, rect, layer)
            pin_set.add(pin)

        debug.check(len(pin_set)>0,"Did not find any pin shapes for {0}.".format(str(pin_name)))

        self.pins[pin_name] = pin_set
        self.all_pins.update(pin_set)

        for pin in self.pins[pin_name]:
            debug.info(2,"Retrieved pin {}".format(str(pin)))
        

        
    def find_pins(self,pin_name):
        """ 
        Finds the pin shapes and converts to tracks. 
        Pin can either be a label or a location,layer pair: [[x,y],layer].
        """
        self.retrieve_pins(pin_name)
        self.analyze_pins(pin_name)


    def find_blockages(self):
        """
        Iterate through all the layers and write the obstacles to the routing grid.
        This doesn't consider whether the obstacles will be pins or not. They get reset later
        if they are not actually a blockage.
        """
        for layer in [self.vert_layer_number,self.horiz_layer_number]:
            self.retrieve_blockages(layer)
            
            
    def find_pins_and_blockages(self, pin_list):
        """
        Find the pins and blockages in the design 
        """
        # This finds the pin shapes and sorts them into "groups" that are connected
        # This must come before the blockages, so we can not count the pins themselves
        # as blockages.
        for pin in pin_list:
            self.find_pins(pin)

        # This will get all shapes as blockages and convert to grid units
        # This ignores shapes that were pins 
        self.find_blockages()

        # Convert the blockages to grid units
        self.convert_blockages()
        
        # This will convert the pins to grid units
        # It must be done after blockages to ensure no DRCs between expanded pins and blocked grids
        for pin in pin_list:
            self.convert_pins(pin)

        for pin in pin_list:
            self.combine_adjacent_pins(pin)
        #self.write_debug_gds("debug_combine_pins.gds",stop_program=True)

        # Separate any adjacent grids of differing net names to prevent wide metal DRC violations
        # Must be done before enclosing pins
        self.separate_adjacent_pins(self.supply_rail_space_width)
        # For debug
        #self.separate_adjacent_pins(1)
        
        # Enclose the continguous grid units in a metal rectangle to fix some DRCs
        self.enclose_pins()
        #self.write_debug_gds("debug_enclose_pins.gds",stop_program=True)

        
    def combine_adjacent_pins_pass(self, pin_name):
        """
        Find pins that have adjacent routing tracks and merge them into a
        single pin_group.  The pins themselves may not be touching, but 
        enclose_pis in the next step will ensure they are touching.
        """        

        # Make a copy since we are going to add to (and then reduce) this list
        pin_groups = self.pin_groups[pin_name].copy()
        
        # Start as None to signal the first iteration
        remove_indices = set()
            
        for index1,pg1 in enumerate(self.pin_groups[pin_name]):
            # Cannot combine more than once
            if index1 in remove_indices:
                continue
            for index2,pg2 in enumerate(self.pin_groups[pin_name]):
                # Cannot combine with yourself
                if index1==index2:
                    continue
                # Cannot combine more than once
                if index2 in remove_indices:
                    continue

                # Combine if at least 1 grid cell is adjacent
                if pg1.adjacent(pg2):
                    combined = pin_group(pin_name, [], self)
                    combined.combine_groups(pg1, pg2)
                    debug.info(2,"Combining {0} {1} {2}:".format(pin_name, index1, index2))
                    debug.info(2, "     {0}\n  {1}".format(pg1.pins, pg2.pins))
                    debug.info(2,"  --> {0}\n      {1}".format(combined.pins,combined.grids))
                    remove_indices.update([index1,index2])
                    pin_groups.append(combined)
                    break

        # Remove them in decreasing order to not invalidate the indices
        debug.info(2,"Removing {}".format(sorted(remove_indices)))
        for i in sorted(remove_indices, reverse=True):
            del pin_groups[i]

        # Use the new pin group!
        self.pin_groups[pin_name] = pin_groups
        
        removed_pairs = int(len(remove_indices)/2)
        debug.info(1, "Combined {0} pin pairs for {1}".format(removed_pairs,pin_name))
        
        return removed_pairs
            
    def combine_adjacent_pins(self, pin_name):
        """
        Make multiple passes of the combine adjacent pins until we have no
        more combinations or hit an iteration limit.
        """
        
        # Start as None to signal the first iteration
        num_removed_pairs = None

        # Just used in case there's a circular combination or something weird
        for iteration_count in range(10):
            num_removed_pairs = self.combine_adjacent_pins_pass(pin_name)
            if num_removed_pairs==0:
                break
        else:
            debug.warning("Did not converge combining adjacent pins in supply router.")

    def separate_adjacent_pins(self, separation):
        """
        This will try to separate all grid pins by the supplied number of separation 
        tracks (default is to prevent adjacency).
        """
        # Commented out to debug with SCMOS
        #if separation==0:
        #    return
        
        pin_names = self.pin_groups.keys()
        for pin_name1 in pin_names:
            for pin_name2 in pin_names:
                if pin_name1==pin_name2:
                    continue
                self.separate_adjacent_pin(pin_name1, pin_name2, separation)

    def separate_adjacent_pin(self, pin_name1, pin_name2, separation):
        """
        Go through all of the pin groups and check if any other pin group is 
        within a separation of it.
        If so, reduce the pin group grid to not include the adjacent grid.
        Try to do this intelligently to keep th pins enclosed.
        """
        debug.info(1,"Comparing {0} and {1} adjacency".format(pin_name1, pin_name2))
        for index1,pg1 in enumerate(self.pin_groups[pin_name1]):
            for index2,pg2 in enumerate(self.pin_groups[pin_name2]):
                # FIXME: Use separation distance and edge grids only
                grids_g1, grids_g2 = pg1.adjacent_grids(pg2, separation)
                # These should have the same length, so...
                if len(grids_g1)>0:
                    debug.info(1,"Adjacent grids {0} {1} {2} {3}".format(index1,grids_g1,index2,grids_g2))
                    self.remove_adjacent_grid(pg1, grids_g1, pg2, grids_g2)

    def remove_adjacent_grid(self, pg1, grids1, pg2, grids2):
        """
        Remove one of the adjacent grids in a heuristic manner.
        """
        # Determine the bigger and smaller group
        if pg1.size()>pg2.size():
            bigger = pg1
            bigger_grids = grids1
            smaller = pg2
            smaller_grids = grids2
        else:
            bigger = pg2
            bigger_grids = grids2
            smaller = pg1
            smaller_grids = grids1
        
        # First, see if we can remove grids that are in the secondary grids
        # i.e. they aren't necessary to the pin grids
        if bigger_grids.issubset(bigger.secondary_grids):
            debug.info(1,"Removing {} from bigger {}".format(str(bigger_grids), bigger))
            bigger.grids.difference_update(bigger_grids)
            self.blocked_grids.update(bigger_grids)
            return
        elif smaller_grids.issubset(smaller.secondary_grids):
            debug.info(1,"Removing {} from smaller {}".format(str(smaller_grids), smaller))
            smaller.grids.difference_update(smaller_grids)
            self.blocked_grids.update(smaller_grids)
            return
            
        # If that fails, just randomly remove from the bigger one and give a warning.
        # This might fail later.
        debug.warning("Removing arbitrary grids from a pin group {} {}".format(bigger, bigger_grids))
        debug.check(len(bigger.grids)>len(bigger_grids),"Zero size pin group after adjacency removal {} {}".format(bigger, bigger_grids))
        bigger.grids.difference_update(bigger_grids)
        self.blocked_grids.update(bigger_grids)


    
    def prepare_blockages(self, pin_name):
        """
        Reset and add all of the blockages in the design.
        Names is a list of pins to add as a blockage.
        """
        debug.info(3,"Preparing blockages.")
        
        # Start fresh. Not the best for run-time, but simpler.
        self.clear_blockages()
        # This adds the initial blockges of the design
        #print("BLOCKING:",self.blocked_grids)
        self.set_blockages(self.blocked_grids,True)

        # Block all of the supply rails (some will be unblocked if they're a target)
        self.set_supply_rail_blocked(True)
        
        # Block all of the pin components (some will be unblocked if they're a source/target)
        # Also block the previous routes
        for name in self.pin_groups.keys():
            blockage_grids = {y for x in self.pin_groups[name] for y in x.grids}
            self.set_blockages(blockage_grids,True)
            blockage_grids = {y for x in self.pin_groups[name] for y in x.blockages}
            self.set_blockages(blockage_grids,True)

        # FIXME: These duplicate a bit of work
        # These are the paths that have already been routed.
        self.set_path_blockages()

        # Don't mark the other components as targets since we want to route
        # directly to a rail, but unblock all the source components so we can
        # route over them
        blockage_grids = {y for x in self.pin_groups[pin_name] for y in x.grids}
        self.set_blockages(blockage_grids,False)
            
        
    # def translate_coordinates(self, coord, mirr, angle, xyShift):
    #     """
    #     Calculate coordinates after flip, rotate, and shift
    #     """
    #     coordinate = []
    #     for item in coord:
    #         x = (item[0]*math.cos(angle)-item[1]*mirr*math.sin(angle)+xyShift[0])
    #         y = (item[0]*math.sin(angle)+item[1]*mirr*math.cos(angle)+xyShift[1])
    #         coordinate += [(x, y)]
    #     return coordinate

    def convert_shape_to_units(self, shape):
        """ 
        Scale a shape (two vector list) to user units 
        """
        unit_factor = [GDS["unit"][0]] * 2
        ll=shape[0].scale(unit_factor)
        ur=shape[1].scale(unit_factor)
        return [ll,ur]

        
    def min_max_coord(self, coord):
        """ 
        Find the lowest and highest corner of a Rectangle 
        """
        coordinate = []
        minx = min(coord[0][0], coord[1][0], coord[2][0], coord[3][0])
        maxx = max(coord[0][0], coord[1][0], coord[2][0], coord[3][0])
        miny = min(coord[0][1], coord[1][1], coord[2][1], coord[3][1])
        maxy = max(coord[0][1], coord[1][1], coord[2][1], coord[3][1])
        coordinate += [vector(minx, miny)]
        coordinate += [vector(maxx, maxy)]
        return coordinate

    def get_inertia(self,p0,p1):
        """ 
        Sets the direction based on the previous direction we came from. 
        """
        # direction (index) of movement
        if p0.x!=p1.x:
            return 0
        elif p0.y!=p1.y:
            return 1
        else:
            # z direction
            return 2

    def clear_blockages(self):
        """ 
        Clear all blockages on the grid.
        """
        debug.info(3,"Clearing all blockages")
        self.rg.clear_blockages()
        
    def set_blockages(self, blockages, value=True):
        """ Flag the blockages in the grid """
        self.rg.set_blocked(blockages, value)

    def set_path_blockages(self,value=True):
        """ Flag the paths as blockages """
        # These are the paths that have already been routed.
        for path_set in self.path_blockages:
            for c in path_set:
                self.rg.set_blocked(c,value)
        
    def get_blockage_tracks(self, ll, ur, z):
        debug.info(3,"Converting blockage ll={0} ur={1} z={2}".format(str(ll),str(ur),z))

        block_list = []
        for x in range(int(ll[0]),int(ur[0])+1):
            for y in range(int(ll[1]),int(ur[1])+1):
                block_list.append(vector3d(x,y,z))

        return set(block_list)

    def convert_blockage(self, blockage):
        """ 
        Convert a pin layout blockage shape to routing grid tracks. 
        """
        # Inflate the blockage by half a spacing rule
        [ll,ur]=self.convert_blockage_to_tracks(blockage.inflate())
        zlayer = self.get_zindex(blockage.layer_num)
        blockage_tracks = self.get_blockage_tracks(ll, ur, zlayer)
        return blockage_tracks
        
    def convert_blockages(self):
        """ Convert blockages to grid tracks. """
        
        for blockage in self.blockages:
            debug.info(3,"Converting blockage {}".format(str(blockage)))
            blockage_list = self.convert_blockage(blockage)
            self.blocked_grids.update(blockage_list)
        
        
    def retrieve_blockages(self, layer_num): 
        """
        Recursive find boundaries as blockages to the routing grid.
        """

        shapes = self.layout.getAllShapesInStructureList(layer_num)
        for boundary in shapes:
            ll = vector(boundary[0],boundary[1])
            ur = vector(boundary[2],boundary[3])
            rect = [ll,ur]
            new_pin = pin_layout("blockage{}".format(len(self.blockages)),rect,layer_num)
            
            # If there is a rectangle that is the same in the pins, it isn't a blockage!
            if new_pin not in self.all_pins:
                self.blockages.append(new_pin)


    def convert_point_to_units(self, p):
        """ 
        Convert a path set of tracks to center line path.
        """
        pt = vector3d(p)
        pt = pt.scale(self.track_widths[0],self.track_widths[1],1)
        return pt

    def convert_wave_to_units(self, wave):
        """ 
        Convert a wave to a set of center points 
        """
        return [self.convert_point_to_units(i) for i in wave]
    

    def convert_blockage_to_tracks(self, shape):
        """ 
        Convert a rectangular blockage shape into track units.
        """
        (ll,ur) = shape
        ll = snap_to_grid(ll)
        ur = snap_to_grid(ur)

        # to scale coordinates to tracks
        debug.info(3,"Converting [ {0} , {1} ]".format(ll,ur))
        old_ll = ll
        old_ur = ur
        ll=ll.scale(self.track_factor)
        ur=ur.scale(self.track_factor)
        # We can round since we are using inflated shapes
        # and the track points are at the center
        ll = ll.round()
        ur = ur.round()
        # if ll[0]<45 and ll[0]>35 and ll[1]<5 and ll[1]>-5:
        #     debug.info(0,"Converting [ {0} , {1} ]".format(old_ll,old_ur))
        #     debug.info(0,"Converted [ {0} , {1} ]".format(ll,ur))
        #     pin=self.convert_track_to_shape(ll)            
        #     debug.info(0,"Pin {}".format(pin))
        return [ll,ur]

    def convert_pin_to_tracks(self, pin_name, pin):
        """ 
        Convert a rectangular pin shape into a list of track locations,layers.
        If no pins are "on-grid" (i.e. sufficient overlap) it makes the one with most overlap if it is not blocked.
        """
        (ll,ur) = pin.rect
        debug.info(3,"Converting pin [ {0} , {1} ]".format(ll,ur))
        
        # scale the size bigger to include neaby tracks
        ll=ll.scale(self.track_factor).floor()
        ur=ur.scale(self.track_factor).ceil()

        # Keep tabs on tracks with sufficient and insufficient overlap
        sufficient_list = set()
        insufficient_list = set()
        
        zindex=self.get_zindex(pin.layer_num)
        for x in range(int(ll[0]),int(ur[0])+1):
            for y in range(int(ll[1]),int(ur[1])+1):
                debug.info(4,"Converting [ {0} , {1} ]".format(x,y))
                (full_overlap,partial_overlap) = self.convert_pin_coord_to_tracks(pin, vector3d(x,y,zindex))
                if full_overlap:
                    sufficient_list.update([full_overlap])
                if partial_overlap:
                    insufficient_list.update([partial_overlap])

        if len(sufficient_list)>0:
            return sufficient_list
        elif len(insufficient_list)>0:
            # If there wasn't a sufficient grid, find the best and patch it to be on grid.
            return self.get_best_offgrid_pin(pin, insufficient_list)
        else:
            debug.error("Unable to find any overlapping grids.", -1)
            

    def get_best_offgrid_pin(self, pin, insufficient_list):
        """ 
        Given a pin and a list of partial overlap grids:
        1) Find the unblocked grids.
        2) If one, use it.
        3) If not, find the greatest overlap.
        4) Add a pin with the most overlap to make it "on grid"
        that is not blocked.
        """
        #print("INSUFFICIENT LIST",insufficient_list)
        # Find the coordinate with the most overlap
        best_coord = None
        best_overlap = -math.inf
        for coord in insufficient_list:
            full_pin = self.convert_track_to_pin(coord)
            # Compute the overlap with that rectangle
            overlap_rect=pin.compute_overlap(full_pin)
            # Determine the min x or y overlap
            min_overlap = min(overlap_rect)
            if min_overlap>best_overlap:
                best_overlap=min_overlap
                best_coord=coord
            
        return set([best_coord])

        
    def convert_pin_coord_to_tracks(self, pin, coord):
        """ 
        Given a pin and a track coordinate, determine if the pin overlaps enough.
        If it does, add additional metal to make the pin "on grid". 
        If it doesn't, add it to the blocked grid list.
        """

        (width, spacing) = self.get_layer_width_space(coord.z)
            
        # This is the rectangle if we put a pin in the center of the track
        track_pin = self.convert_track_to_pin(coord)
        overlap_length = pin.overlap_length(track_pin)
        
        debug.info(3,"Check overlap: {0} {1} . {2} = {3}".format(coord, pin.rect, track_pin, overlap_length))
        # If it overlaps by more than the min width DRC, we can just use the track
        if overlap_length==math.inf or snap_val_to_grid(overlap_length) >= snap_val_to_grid(width):
            debug.info(3,"  Overlap: {0} >? {1}".format(overlap_length,spacing))  
            return (coord, None)
        # Otherwise, keep track of the partial overlap grids in case we need to patch it later.
        else:
            debug.info(3,"  Partial/no overlap: {0} >? {1}".format(overlap_length,spacing))
            return (None, coord)
        



                                                        

    def convert_track_to_pin(self, track):
        """ 
        Convert a grid point into a rectangle shape that is centered
        track in the track and leaves half a DRC space in each direction.
        """
        # space depends on which layer it is
        if self.get_layer(track[2])==self.horiz_layer_name:
            space = 0.5*self.horiz_layer_spacing
        else:
            space = 0.5*self.vert_layer_spacing
            
        # calculate lower left 
        x = track.x*self.track_width - 0.5*self.track_width + space
        y = track.y*self.track_width - 0.5*self.track_width + space
        ll = snap_to_grid(vector(x,y))
            
        # calculate upper right
        x = track.x*self.track_width + 0.5*self.track_width - space
        y = track.y*self.track_width + 0.5*self.track_width - space
        ur = snap_to_grid(vector(x,y))

        p = pin_layout("", [ll, ur], self.get_layer(track[2]))
        return p

    def convert_track_to_shape(self, track):
        """ 
        Convert a grid point into a rectangle shape that occupies the entire centered
        track.
        """
        # to scale coordinates to tracks
        x = track[0]*self.track_width - 0.5*self.track_width
        y = track[1]*self.track_width - 0.5*self.track_width
        # offset lowest corner object to to (-track halo,-track halo)
        ll = snap_to_grid(vector(x,y))
        ur = snap_to_grid(ll + vector(self.track_width,self.track_width))

        return [ll,ur]
    
    def analyze_pins(self, pin_name):
        """ 
        Analyze the shapes of a pin and combine them into groups which are connected.
        """
        pin_set = self.pins[pin_name]
        local_debug = False

        # Put each pin in an equivalence class of it's own
        equiv_classes = [set([x]) for x in pin_set]
        if local_debug:
            debug.info(0,"INITIAL\n",equiv_classes)

        def compare_classes(class1, class2):
            """ 
            Determine if two classes should be combined and if so return
            the combined set. Otherwise, return None.
            """
            if local_debug:
                debug.info(0,"CLASS1:\n",class1)
                debug.info(0,"CLASS2:\n",class2)
            # Compare each pin in each class,
            # and if any overlap, return the combined the class 
            for p1 in class1:
                for p2 in class2:
                    if p1.overlaps(p2):
                        combined_class = class1 | class2
                        if local_debug:
                            debug.info(0,"COMBINE:",pformat(combined_class))
                        return combined_class
                        
            if local_debug:
                debug.info(0,"NO COMBINE")
            return None
                        
        
        def combine_classes(equiv_classes):
            """ Recursive function to combine classes. """
            local_debug = False

            if local_debug:
                debug.info(0,"\nRECURSE:\n",pformat(equiv_classes))
            if len(equiv_classes)==1:
                return(equiv_classes)
            
            for class1 in equiv_classes:
                for class2 in equiv_classes:
                    if class1 == class2:
                        continue
                    class3 = compare_classes(class1, class2)
                    if class3:
                        new_classes = equiv_classes
                        new_classes.remove(class1)
                        new_classes.remove(class2)
                        new_classes.append(class3)
                        return(combine_classes(new_classes))
            else:
                return(equiv_classes)

        reduced_classes = combine_classes(equiv_classes)
        if local_debug:
            debug.info(0,"FINAL  ",reduced_classes)
        self.pin_groups[pin_name] = [pin_group(name=pin_name, pin_set=x, router=self) for x in reduced_classes]
        
    def convert_pins(self, pin_name):
        """ 
        Convert the pin groups into pin tracks and blockage tracks.
        """
        for pg in self.pin_groups[pin_name]:
            pg.convert_pin()


    
    def enclose_pins(self):
        """
        This will find the biggest rectangle enclosing some grid squares and
        put a rectangle over it. It does not enclose grid squares that are blocked
        by other shapes.
        """
        for pin_name in self.pin_groups.keys():
            debug.info(1,"Enclosing pins for {}".format(pin_name))
            for pg in self.pin_groups[pin_name]:
                pg.enclose_pin()
                pg.add_enclosure(self.cell)

        #self.write_debug_gds("pin_debug.gds", False)
    
    def add_source(self, pin_name):
        """ 
        This will mark the grids for all pin components as a source.
        Marking as source or target also clears blockage status.
        """
        for i in range(self.num_pin_components(pin_name)):
            self.add_pin_component_source(pin_name, i)

    def add_target(self, pin_name):
        """ 
        This will mark the grids for all pin components as a target.
        Marking as source or target also clears blockage status.
        """
        for i in range(self.num_pin_components(pin_name)):
            self.add_pin_component_target(pin_name, i)
            
    def num_pin_components(self, pin_name):
        """ 
        This returns how many disconnected pin components there are.
        """
        return len(self.pin_groups[pin_name])
    
    def add_pin_component_source(self, pin_name, index):
        """ 
        This will mark only the pin tracks from the indexed pin component as a source.
        It also unsets it as a blockage.
        """
        debug.check(index<self.num_pin_components(pin_name),"Pin component index too large.")
        
        pin_in_tracks = self.pin_groups[pin_name][index].grids
        debug.info(1,"Set source: " + str(pin_name) + " " + str(pin_in_tracks))
        self.rg.add_source(pin_in_tracks)

    def add_path_target(self, paths):
        """ 
        Set all of the paths as a target too.
        """
        for p in paths:
            self.rg.set_target(p)
            self.rg.set_blocked(p,False)

    def add_pin_component_target(self, pin_name, index):
        """ 
        This will mark only the pin tracks from the indexed pin component as a target.
        It also unsets it as a blockage.
        """
        debug.check(index<self.num_pin_grids(pin_name),"Pin component index too large.")
        
        pin_in_tracks = self.pin_groups[pin_name][index].grids
        debug.info(1,"Set target: " + str(pin_name) + " " + str(pin_in_tracks))
        self.rg.add_target(pin_in_tracks)
            

    def set_component_blockages(self, pin_name, value=True):
        """ 
        Block all of the pin components.
        """
        debug.info(2,"Setting blockages {0} {1}".format(pin_name,value))
        for pg in self.pin_groups[pin_name]:
            self.set_blockages(pg.grids, value)
            

    def prepare_path(self,path):
        """ 
        Prepare a path or wave for routing ebedding.
        This tracks the path, simplifies the path and marks it as a path for debug output.
        """
        debug.info(4,"Set path: " + str(path))

        # Keep track of path for future blockages
        #path.set_blocked()
        
        # This is marked for debug
        path.set_path()

        # For debugging... if the path failed to route.
        if False or path==None:
            self.write_debug_gds()

        # First, simplify the path for
        #debug.info(1,str(self.path))        
        contracted_path = self.contract_path(path)
        debug.info(3,"Contracted path: " + str(contracted_path))
        
        return contracted_path
        
        
    def add_route(self,path):
        """ 
        Add the current wire route to the given design instance.
        """
        path=self.prepare_path(path)
        
        debug.info(1,"Adding route: {}".format(str(path)))
        # If it is only a square, add an enclosure to the track
        if len(path)==1:
            self.add_single_enclosure(path[0][0])
        else:
            # convert the path back to absolute units from tracks
            # This assumes 1-track wide again
            abs_path = [self.convert_point_to_units(x[0]) for x in path]
            # Otherwise, add the route which includes enclosures
            self.cell.add_route(layers=self.layers,
                                coordinates=abs_path,
                                layer_widths=self.layer_widths)
            
    def add_single_enclosure(self, track):
        """
        Add a metal enclosure that is the size of the routing grid minus a spacing on each side. 
        """
        pin = self.convert_track_to_pin(track)
        (ll,ur) = pin.rect
        self.cell.add_rect(layer=self.get_layer(track.z),
                           offset=ll,
                           width=ur.x-ll.x,
                           height=ur.y-ll.y)
                                  

        
    def add_via(self,loc,size=1):
        """ 
        Add a via centered at the current location
        """
        loc = self.convert_point_to_units(vector3d(loc[0],loc[1],0))
        self.cell.add_via_center(layers=self.layers,
                                 offset=vector(loc.x,loc.y),
                                 size=(size,size))

    def compute_pin_enclosure(self, ll, ur, zindex, name=""):
        """
        Enclose the tracks from ll to ur in a single rectangle that meets
        the track DRC rules. 
        """
        # Get the layer information
        (width, space) = self.get_layer_width_space(zindex)
        layer = self.get_layer(zindex)
        
        # This finds the pin shape enclosed by the track with DRC spacing on the sides
        pin = self.convert_track_to_pin(ll)
        (abs_ll,unused) = pin.rect
        pin = self.convert_track_to_pin(ur)
        (unused,abs_ur) = pin.rect
        #print("enclose ll={0} ur={1}".format(ll,ur))
        #print("enclose ll={0} ur={1}".format(abs_ll,abs_ur))
        
        pin = pin_layout(name, [abs_ll, abs_ur], layer)
        
        return pin
    

    def compute_wide_enclosure(self, ll, ur, zindex, name=""):
        """ 
        Enclose the tracks from ll to ur in a single rectangle that meets the track DRC rules.
        """

        # Find the pin enclosure of the whole track shape (ignoring DRCs)
        (abs_ll,unused) = self.convert_track_to_shape(ll)
        (unused,abs_ur) = self.convert_track_to_shape(ur)
        
        # Get the layer information
        x_distance = abs(abs_ll.x-abs_ur.x)
        y_distance = abs(abs_ll.y-abs_ur.y)
        shape_width = min(x_distance, y_distance)
        shape_length = max(x_distance, y_distance)

        # Get the DRC rule for the grid dimensions
        (width, space) = self.get_layer_width_space(zindex, shape_width, shape_length)
        layer = self.get_layer(zindex)

        if zindex==0:
            spacing = vector(0.5*self.track_width, 0.5*space)
        else:
            spacing = vector(0.5*space, 0.5*self.track_width)
        # Compute the shape offsets with correct spacing
        new_ll = abs_ll + spacing
        new_ur = abs_ur - spacing
        pin = pin_layout(name, [new_ll, new_ur], layer)
        
        return pin
    

    def contract_path(self,path):
        """ 
        Remove intermediate points in a rectilinear path or a wave.
        """
        # Waves are always linear, so just return the first and last.
        if self.is_wave(path):
            return [path[0],path[-1]]

        # Make a list only of points that change inertia of the path
        newpath = [path[0]]
        for i in range(1,len(path)-1):
            prev_inertia=self.get_inertia(path[i-1][0],path[i][0])
            next_inertia=self.get_inertia(path[i][0],path[i+1][0])
            # if we switch directions, add the point, otherwise don't
            if prev_inertia!=next_inertia:
                newpath.append(path[i])

        # always add the last path unless it was a single point
        if len(path)>1:
            newpath.append(path[-1])
        return newpath
    

            
    def run_router(self, detour_scale):
        """
        This assumes the blockages, source, and target are all set up. 
        """
        # returns the path in tracks
        (path,cost) = self.rg.route(detour_scale)
        if path:
            debug.info(2,"Found path: cost={0} ".format(cost))
            debug.info(3,str(path))
            self.paths.append(path)
            path_set = grid_utils.flatten_set(path)
            inflated_path = grid_utils.inflate_set(path_set,self.supply_rail_space_width)
            self.path_blockages.append(inflated_path)
            self.add_route(path)
        else:
            self.write_debug_gds("failed_route.gds")
            # clean up so we can try a reroute
            self.rg.reinit()
            return False
        return True


    def annotate_pin_and_tracks(self, pin, tracks):
        """"
        Annotate some shapes for debug purposes
        """
        debug.info(0,"Annotating\n  pin {0}\n  tracks {1}".format(pin,tracks))
        for coord in tracks:
            (ll,ur) = self.convert_track_to_shape(coord)
            self.cell.add_rect(layer="text",
                               offset=ll,
                               width=ur[0]-ll[0],
                               height=ur[1]-ll[1])
            (ll,ur) = self.convert_track_to_pin(coord).rect
            self.cell.add_rect(layer="boundary",
                               offset=ll,
                               width=ur[0]-ll[0],
                               height=ur[1]-ll[1])
            (ll,ur) = pin.rect
            self.cell.add_rect(layer="text",
                               offset=ll,
                               width=ur[0]-ll[0],
                               height=ur[1]-ll[1])

    def write_debug_gds(self, gds_name="debug_route.gds", stop_program=True):
        """ 
        Write out a GDS file with the routing grid and search information annotated on it.
        """
        self.add_router_info()
        self.cell.gds_write(gds_name)

        if stop_program:
            import sys
            sys.exit(1)

    def annotate_grid(self, g):
        """
        Display grid information in the GDS file for a single grid cell.
        """
        shape = self.convert_track_to_shape(g)
        partial_track=vector(0,self.track_width/6.0)
        self.cell.add_rect(layer="text",
                           offset=shape[0],
                           width=shape[1].x-shape[0].x,
                           height=shape[1].y-shape[0].y)
        t=self.rg.map[g].get_type()
                
        # midpoint offset
        off=vector((shape[1].x+shape[0].x)/2,
                   (shape[1].y+shape[0].y)/2)
        if g[2]==1:
            # Upper layer is upper right label
            type_off=off+partial_track
        else:
            # Lower layer is lower left label
            type_off=off-partial_track
        if t!=None:
            self.cell.add_label(text=str(t),
                                layer="text",
                                offset=type_off)
        self.cell.add_label(text="{0},{1}".format(g[0],g[1]),
                            layer="text",
                            offset=shape[0],
                            zoom=0.05)

    def add_router_info(self):
        """
        Write the routing grid and router cost, blockage, pins on 
        the boundary layer for debugging purposes. This can only be 
        called once or the labels will overlap.
        """
        debug.info(0,"Adding router info")

        show_blockages = True
        show_blockage_grids = True
        show_enclosures = True
        show_all_grids = True
        
        if show_all_grids:
            self.rg.add_all_grids()
            for g in self.rg.map.keys():
                self.annotate_grid(g)
            
        if show_blockages:
            # Display the inflated blockage
            for blockage in self.blockages:
                debug.info(1,"Adding {}".format(blockage))
                (ll,ur) = blockage.inflate()
                self.cell.add_rect(layer="text",
                                   offset=ll,
                                   width=ur.x-ll.x,
                                   height=ur.y-ll.y)
        if show_blockage_grids:
            self.set_blockages(self.blocked_grids,True)
            grid_keys=self.rg.map.keys()
            for g in grid_keys:
                self.annotate_grid(g)

        if show_enclosures:
            for key in self.pin_groups.keys():
                for pg in self.pin_groups[key]:
                    if not pg.enclosed:
                        continue
                    for pin in pg.enclosures:
                        #print("enclosure: ",pin.name,pin.ll(),pin.width(),pin.height())
                        self.cell.add_rect(layer="text",
                                           offset=pin.ll(),
                                           width=pin.width(),
                                           height=pin.height())
    
# FIXME: This should be replaced with vector.snap_to_grid at some point

def snap_to_grid(offset):
    """
    Changes the coodrinate to match the grid settings
    """
    xoff = snap_val_to_grid(offset[0])
    yoff = snap_val_to_grid(offset[1])    
    return vector(xoff, yoff)

def snap_val_to_grid(x):
    grid = drc("grid")
    xgrid = int(round(round((x / grid), 2), 0))
    xoff = xgrid * grid
    return xoff
