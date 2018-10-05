import sys
import gdsMill
import tech
from contact import contact
import math
import debug
from pin_layout import pin_layout
from vector import vector
from vector3d import vector3d 
from globals import OPTS
from pprint import pformat

class router:
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
        self.cell = design

        # If didn't specify a gds blockage file, write it out to read the gds
        # This isn't efficient, but easy for now
        if not gds_filename:
            gds_filename = OPTS.openram_temp+"temp.gds"
            self.cell.gds_write(gds_filename)
        
        # Load the gds file and read in all the shapes
        self.layout = gdsMill.VlsiLayout(units=tech.GDS["unit"])
        self.reader = gdsMill.Gds2reader(self.layout)
        self.reader.loadFromFile(gds_filename)
        self.top_name = self.layout.rootStructureName

        # Set up layers and track sizes
        self.set_layers(layers)
        
        ### The pin data structures
        # A map of pin names to pin structures
        self.pins = {}
        # This is a set of all pins so that we don't create blockages for these shapes.
        self.all_pins = set()
        # A set of connected pin groups
        self.pin_groups = {}
        # The corresponding sets (components) of grids for each pin
        self.pin_components = {}
        
        ### The blockage data structures
        # A list of pin layout shapes that are blockages
        self.blockages=[]
        # A set of blocked grids
        self.blocked_grids = set()
        # The corresponding set of partially blocked grids for each component.
        # These are blockages for other nets but unblocked for this component.
        #self.pin_component_blockages = {}        
        
        ### The routed data structures
        # A list of paths that have been "routed"
        self.paths = []
        # The list of supply rails that may be routed
        self.supply_rails = []

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
        self.pin_grids = {}
        self.pin_paritals = {}        
        # DO NOT clear the blockages as these don't change
        self.rg.reinit()

        
    def set_top(self,top_name):
        """ If we want to route something besides the top-level cell."""
        self.top_name = top_name

    def get_zindex(self,layer_num):
        if layer_num==self.horiz_layer_number:
            return 0
        else:
            return 1

    def get_layer(self, zindex):
        if zindex==1:
            return self.vert_layer_name
        elif zindex==0:
            return self.horiz_layer_name
        else:
            debug.error("Invalid zindex {}".format(zindex),-1)
        
    def is_wave(self,path):
        """
        Determines if this is a multi-track width wave (True) or a normal route (False)
        """
        return len(path[0])>1
    
    def set_layers(self, layers):
        """
        Allows us to change the layers that we are routing on. First layer
        is always horizontal, middle is via, and last is always
        vertical.
        """
        self.layers = layers
        (self.horiz_layer_name, self.via_layer_name, self.vert_layer_name) = self.layers

        self.vert_layer_minwidth = tech.drc["minwidth_{0}".format(self.vert_layer_name)]
        self.vert_layer_spacing = tech.drc[str(self.vert_layer_name)+"_to_"+str(self.vert_layer_name)] 
        self.vert_layer_number = tech.layer[self.vert_layer_name]
        
        self.horiz_layer_minwidth = tech.drc["minwidth_{0}".format(self.horiz_layer_name)]
        self.horiz_layer_spacing = tech.drc[str(self.horiz_layer_name)+"_to_"+str(self.horiz_layer_name)] 
        self.horiz_layer_number = tech.layer[self.horiz_layer_name]

        # Contacted track spacing.
        via_connect = contact(self.layers, (1, 1))
        self.max_via_size = max(via_connect.width,via_connect.height)
        self.horiz_track_width = self.max_via_size + self.horiz_layer_spacing
        self.vert_track_width = self.max_via_size + self.vert_layer_spacing

        # We'll keep horizontal and vertical tracks the same for simplicity.
        self.track_width = max(self.horiz_track_width,self.vert_track_width)
        debug.info(1,"Track width: "+str(self.track_width))

        self.track_widths = [self.track_width] * 2
        self.track_factor = [1/self.track_width] * 2
        debug.info(1,"Track factor: {0}".format(self.track_factor))

        # When we actually create the routes, make them the width of the track (minus 1/2 spacing on each side)
        self.layer_widths = [self.track_width - self.horiz_layer_spacing, 1, self.track_width - self.vert_layer_spacing]

    def retrieve_pins(self,pin_name):
        """
        Retrieve the pin shapes from the layout.
        """
        shape_list=self.layout.getAllPinShapesByLabel(str(pin_name))
        pin_set = set()
        for shape in shape_list:
            (name,layer,boundary)=shape
            rect = [vector(boundary[0],boundary[1]),vector(boundary[2],boundary[3])]
            pin = pin_layout(pin_name, rect, layer)
            debug.info(2,"Found pin {}".format(str(pin)))
            pin_set.add(pin)

        debug.check(len(pin_set)>0,"Did not find any pin shapes for {0}.".format(str(pin_name)))
        self.pins[pin_name] = pin_set
        self.all_pins.update(pin_set)

        
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
            
        self.convert_blockages()
            
    # # def reinit(self):
    # #     """
    # #     Reset the source and destination pins to start a new routing.
    # #     Convert the source/dest pins to blockages.
    # #     Convert the routed path to blockages.
    # #     Keep the other blockages unchanged.
    # #     """
    # #     self.clear_pins()
    # #     # DO NOT clear the blockages as these don't change
    # #     self.rg.reinit()
        

    def find_pins_and_blockages(self, pin_list):
        """
        Find the pins and blockages in the design 
        """
        # This finds the pin shapes and sorts them into "groups" that are connected
        for pin in pin_list:
            self.find_pins(pin)

        # This will get all shapes as blockages and convert to grid units
        # This ignores shapes that were pins 
        self.find_blockages()
        
        # This will convert the pins to grid units
        # It must be done after blockages to ensure no DRCs between expanded pins and blocked grids
        for pin in pin_list:
            self.convert_pins(pin)

        # Enclose the continguous grid units in a metal rectangle to fix some DRCs
        self.enclose_pins()

    def prepare_blockages(self):
        """
        Reset and add all of the blockages in the design.
        Names is a list of pins to add as a blockage.
        """
        debug.info(1,"Preparing blockages.")
        
        # Start fresh. Not the best for run-time, but simpler.
        self.clear_blockages()
        # This adds the initial blockges of the design
        #print("BLOCKING:",self.blocked_grids)
        self.set_blockages(self.blocked_grids,True)

        # Block all of the supply rails (some will be unblocked if they're a target)
        self.set_supply_rail_blocked(True)
        
        # Block all of the pin components (some will be unblocked if they're a source/target)
        for name in self.pin_components.keys():
            self.set_blockages(self.pin_components[name],True)

        # Block all of the pin component partial blockages 
        #for name in self.pin_component_blockages.keys():
        #    self.set_blockages(self.pin_component_blockages[name],True)
                           
        # These are the paths that have already been routed.
        self.set_path_blockages()
        
    def translate_coordinates(self, coord, mirr, angle, xyShift):
        """
        Calculate coordinates after flip, rotate, and shift
        """
        coordinate = []
        for item in coord:
            x = (item[0]*math.cos(angle)-item[1]*mirr*math.sin(angle)+xyShift[0])
            y = (item[0]*math.sin(angle)+item[1]*mirr*math.cos(angle)+xyShift[1])
            coordinate += [(x, y)]
        return coordinate

    def convert_shape_to_units(self, shape):
        """ 
        Scale a shape (two vector list) to user units 
        """
        unit_factor = [tech.GDS["unit"][0]] * 2
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

        
    def add_path_blockages(self):
        """
        Go through all of the past paths and add them as blockages.
        This is so we don't have to write/reload the GDS.
        """
        for path in self.paths:
            for grid in path:
                self.rg.set_blocked(grid)

    def clear_blockages(self):
        """ 
        Clear all blockages on the grid.
        """
        debug.info(2,"Clearing all blockages")
        self.rg.clear_blockages()
        
    def set_blockages(self, blockages, value=True):
        """ Flag the blockages in the grid """
        self.rg.set_blocked(blockages, value)

    def set_path_blockages(self,value=True):
        """ Flag the paths as blockages """
        # These are the paths that have already been routed.
        # This adds the initial blockges of the design
        for p in self.paths:
            p.set_blocked(value)
        
    def get_blockage_tracks(self, ll, ur, z):
        debug.info(4,"Converting blockage ll={0} ur={1} z={2}".format(str(ll),str(ur),z))

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
            full_rect = self.convert_track_to_pin(coord)
            # Compute the overlap with that rectangle
            overlap_rect=self.compute_overlap(pin.rect,full_rect)
            # Determine the min x or y overlap
            min_overlap = min(overlap_rect)
            if min_overlap>best_overlap:
                best_overlap=min_overlap
                best_coord=coord
            
        return set([best_coord])

        
    def get_layer_width_space(self, zindex):
        """
         Return the width and spacing of a given layer. 
        """
        if zindex==1:
            width = self.vert_layer_minwidth
            spacing = self.vert_layer_spacing
        elif zindex==0:
            width = self.horiz_layer_minwidth
            spacing = self.horiz_layer_spacing
        else:
            debug.error("Invalid zindex for track", -1)

        return (width,spacing)

    def convert_pin_coord_to_tracks(self, pin, coord):
        """ 
        Given a pin and a track coordinate, determine if the pin overlaps enough.
        If it does, add additional metal to make the pin "on grid". 
        If it doesn't, add it to the blocked grid list.
        """

        (width, spacing) = self.get_layer_width_space(coord.z)
            
        # This is the rectangle if we put a pin in the center of the track
        track_rect = self.convert_track_to_pin(coord)
        overlap_width = self.compute_overlap_width(pin.rect, track_rect)
        
        debug.info(3,"Check overlap: {0} {1} . {2} = {3}".format(coord, pin.rect, track_rect, overlap_width))
        # If it overlaps by more than the min width DRC, we can just use the track
        if overlap_width==math.inf or snap_val_to_grid(overlap_width) >= snap_val_to_grid(width):
            debug.info(3,"  Overlap: {0} >? {1}".format(overlap_width,spacing))  
            return (coord, None)
        # Otherwise, keep track of the partial overlap grids in case we need to patch it later.
        else:
            debug.info(3,"  Partial/no overlap: {0} >? {1}".format(overlap_width,spacing))
            return (None, coord)
        


    def compute_overlap(self, r1, r2):
        """ Calculate the rectangular overlap of two rectangles. """
        (r1_ll,r1_ur) = r1
        (r2_ll,r2_ur) = r2

        #ov_ur = vector(min(r1_ur.x,r2_ur.x),min(r1_ur.y,r2_ur.y))
        #ov_ll = vector(max(r1_ll.x,r2_ll.x),max(r1_ll.y,r2_ll.y))

        dy = min(r1_ur.y,r2_ur.y)-max(r1_ll.y,r2_ll.y)
        dx = min(r1_ur.x,r2_ur.x)-max(r1_ll.x,r2_ll.x)

        if dx>0 and dy>0:
            return [dx,dy]
        else:
            return [0,0]

    def compute_overlap_width(self, r1, r2):
        """ 
        Calculate the intersection segment and determine its width.
        """
        intersections = self.compute_overlap_segment(r1,r2)

        if len(intersections)==2:
            (p1,p2) = intersections
            return math.sqrt(pow(p1[0]-p2[0],2) + pow(p1[1]-p2[1],2))
        else:
            # we either have no overlap or complete overlap
            # Compute the width of the overlap of the two rectangles
            overlap_rect=self.compute_overlap(r1, r2)
            # Determine the min x or y overlap
            min_overlap = min(overlap_rect)
            if min_overlap>0:
                return math.inf
            else:
                return 0

    
    def compute_overlap_segment(self, r1, r2):
        """ 
        Calculate the intersection segment of two rectangles 
        (if any)
        """
        (r1_ll,r1_ur) = r1
        (r2_ll,r2_ur) = r2

        # The other corners besides ll and ur
        r1_ul = vector(r1_ll.x, r1_ur.y)
        r1_lr = vector(r1_ur.x, r1_ll.y)
        r2_ul = vector(r2_ll.x, r2_ur.y)
        r2_lr = vector(r2_ur.x, r2_ll.y)

        from itertools import tee
        def pairwise(iterable):
            "s -> (s0,s1), (s1,s2), (s2, s3), ..."
            a, b = tee(iterable)
            next(b, None)
            return zip(a, b)
        
        # R1 edges CW
        r1_cw_points = [r1_ll, r1_ul, r1_ur, r1_lr, r1_ll]
        r1_edges = []
        for (p,q) in pairwise(r1_cw_points):
            r1_edges.append([p,q])
        
        # R2 edges CW
        r2_cw_points = [r2_ll, r2_ul, r2_ur, r2_lr, r2_ll]
        r2_edges = []
        for (p,q) in pairwise(r2_cw_points):
            r2_edges.append([p,q])

        # There are 4 edges on each rectangle
        # so just brute force check intersection of each
        # Two pairs of them should intersect
        intersections = []
        for r1e in r1_edges:
            for r2e in r2_edges:
                i = self.segment_intersection(r1e, r2e)
                if i:
                    intersections.append(i)

        return intersections

    def on_segment(self, p, q, r):
        """
        Given three co-linear points, determine if q lies on segment pr
        """
        if q[0] <= max(p[0], r[0]) and \
           q[0] >= min(p[0], r[0]) and \
           q[1] <= max(p[1], r[1]) and \
           q[1] >= min(p[1], r[1]):
            return True 
        
        return False
    
    def segment_intersection(self, s1, s2):
        """ 
        Determine the intersection point of two segments
        Return the a segment if they overlap.
        Return None if they don't.
        """
        (a,b) = s1
        (c,d) = s2
        # Line AB represented as a1x + b1y = c1
        a1 = b.y - a.y
        b1 = a.x - b.x
        c1 = a1*a.x + b1*a.y
        
        # Line CD represented as a2x + b2y = c2
        a2 = d.y - c.y
        b2 = c.x - d.x
        c2 = a2*c.x + b2*c.y
        
        determinant = a1*b2 - a2*b1

        if determinant!=0:
            x = (b2*c1 - b1*c2)/determinant
            y = (a1*c2 - a2*c1)/determinant
            
            r = [x,y]
            if self.on_segment(a, r, b) and self.on_segment(c, r, d):
                return [x, y]
           
        return None

                                                        

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

        return [ll,ur]

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
        local_debug=False
        # Put each pin in an equivalence class of it's own
        equiv_classes = [set([x]) for x in pin_set]
        if local_debug:
            print("INITIAL\n",equiv_classes)

        def compare_classes(class1, class2):
            """ 
            Determine if two classes should be combined and if so return
            the combined set. Otherwise, return None.
            """
            if local_debug:
                print("CLASS1:\n",class1)
                print("CLASS2:\n",class2)
            # Compare each pin in each class,
            # and if any overlap, return the combined the class 
            for p1 in class1:
                for p2 in class2:
                    if p1.overlaps(p2):
                        combined_class = class1 | class2
                        if local_debug:
                            print("COMBINE:",pformat(combined_class))
                        return combined_class
                        
            if local_debug:
                print("NO COMBINE")
            return None
                        
        
        def combine_classes(equiv_classes):
            """ Recursive function to combine classes. """
            if local_debug:
                print("\nRECURSE:\n",pformat(equiv_classes))
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
            print("FINAL  ",reduced_classes)
        self.pin_groups[pin_name]=reduced_classes
        
    def convert_pins(self, pin_name):
        """ 
        Convert the pin groups into pin tracks and blockage tracks
        """
        try:
            self.pin_components[pin_name]
        except:
            self.pin_components[pin_name] = []

        # try:
        #     self.pin_component_blockages[pin_name]
        # except:
        #     self.pin_component_blockages[pin_name] = []
            
        found_pin = False
        for pg in self.pin_groups[pin_name]:
            #print("PG  ",pg)
            # Keep the same groups for each pin
            pin_set = set()
            blockage_set = set()
            for pin in pg:
                debug.info(2,"  Converting {0}".format(pin))
                # Determine which tracks the pin overlaps 
                pin_in_tracks=self.convert_pin_to_tracks(pin_name, pin)
                pin_set.update(pin_in_tracks)
                # Blockages will be a super-set of pins since it uses the inflated pin shape.
                blockage_in_tracks = self.convert_blockage(pin) 
                blockage_set.update(blockage_in_tracks)

            debug.info(2,"     pins   {}".format(pin_set))
            debug.info(2,"     blocks {}".format(blockage_set))
                       
            # At least one of the groups must have some valid tracks
            if (len(pin_set) == 0):
                self.write_debug_gds()
                debug.error("Unable to find pin on grid.",-1)

            # We need to route each of the components, so don't combine the groups
            self.pin_components[pin_name].append(pin_set | blockage_set)

            # Add all of the blocked grids to the set for the design
            #partial_set = blockage_set - pin_set
            #self.pin_component_blockages[pin_name].append(partial_set)

            # Remove the blockage set from the blockages since these
            # will either be pins or partial pin blockges
            self.blocked_grids.difference_update(blockage_set)            

    def enclose_pin_grids(self, grids):
        """
        This encloses a single pin component with a rectangle. 
        It returns the set of the unenclosed pins.
        """

        # We may have started with an empty set
        if not grids:
            return

        # Start with lowest left element 
        ll = min(grids)
        grids.remove(ll)
        # Start with the ll and make the widest row
        row = [ll]
        # Move right while we can
        while True:
            right = row[-1] + vector3d(1,0,0)
            # Can't move if not in the pin shape or blocked
            if right in grids and right not in self.blocked_grids:
                grids.remove(right)
                row.append(right)
            else:
                break
        # Move up while we can
        while True:
            next_row = [x+vector3d(0,1,0) for x in row]
            for cell in next_row:
                # Can't move if any cell is not in the pin shape or blocked
                if cell not in grids or cell in self.blocked_grids:
                    break
            else:
                grids.difference_update(set(next_row))
                row = next_row
                # Skips the second break
                continue
            # Breaks from the nested break
            break

        # Add a shape from ll to ur
        ur = row[-1]
        self.add_enclosure(ll, ur, ll.z)
        
        # Return the remaining grid set
        return grids
    
    def enclose_pins(self):
        """
        This will find the biggest rectangle enclosing some grid squares and
        put a rectangle over it. It does not enclose grid squares that are blocked
        by other shapes.
        """
        # FIXME: This could be optimized, but we just do a simple greedy biggest shape
        # for now.
        for pin_name in self.pin_components.keys():
            #for pin_set,partial_set in zip(self.pin_components[pin_name],self.pin_component_blockages[pin_name]):
            #    total_pin_grids = pin_set | partial_set
            for pin_grids in self.pin_components[pin_name]:
                # Must duplicate so we don't destroy the original
                total_pin_grids=set(pin_grids)
                while self.enclose_pin_grids(total_pin_grids):
                    pass

        self.write_debug_gds("pin_debug.gds", False)

        
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
        return len(self.pin_components[pin_name])
    
    def add_pin_component_source(self, pin_name, index):
        """ 
        This will mark only the pin tracks from the indexed pin component as a source.
        It also unsets it as a blockage.
        """
        debug.check(index<self.num_pin_components(pin_name),"Pin component index too large.")
        
        pin_in_tracks = self.pin_components[pin_name][index]
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
        debug.check(index<self.num_pin_components(pin_name),"Pin component index too large.")
        
        pin_in_tracks = self.pin_components[pin_name][index]
        debug.info(1,"Set target: " + str(pin_name) + " " + str(pin_in_tracks))
        self.rg.add_target(pin_in_tracks)
            

    def add_supply_rail_target(self, pin_name):
        """
        Add the supply rails of given name as a routing target.
        """
        debug.info(2,"Add supply rail target {}".format(pin_name))
        for rail in self.supply_rails:
            if rail.name != pin_name:
                continue
            for wave_index in range(len(rail)):
                pin_in_tracks = rail[wave_index]
                #debug.info(1,"Set target: " + str(pin_name) + " " + str(pin_in_tracks))
                self.rg.set_target(pin_in_tracks)
                self.rg.set_blocked(pin_in_tracks,False)

    def set_supply_rail_blocked(self, value=True):
        """
        Add the supply rails of given name as a routing target.
        """
        debug.info(2,"Blocking supply rail")        
        for rail in self.supply_rails:
            for wave_index in range(len(rail)):
                pin_in_tracks = rail[wave_index]
                #debug.info(1,"Set target: " + str(pin_name) + " " + str(pin_in_tracks))
                self.rg.set_blocked(pin_in_tracks,value)
                
    def set_component_blockages(self, pin_name, value=True):
        """ 
        Block all of the pin components.
        """
        debug.info(2,"Setting blockages {0} {1}".format(pin_name,value))
        for component in self.pin_components[pin_name]:
            self.set_blockages(component, value)
            

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
        (ll,ur) = self.convert_track_to_pin(track)
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
        
        

    def add_wavepath(self, name, path):
        """ 
        Add the current wave to the given design instance.
        This is a single layer path that is multiple tracks wide.
        """
        path=self.prepare_path(path)

        ll = path[0][0]
        ur = path[-1][-1]
        z = ll.z
        
        pin = self.add_enclosure(ll, ur, z, name)
        
        return pin

    def add_enclosure(self, ll, ur, zindex, name=""):
        """ 
        Enclose the tracks from ll to ur in a single rectangle that meets the track DRC rules.
        If name is supplied, it is added as a pin and not just a rectangle.

        """
        # Get the layer information
        (width, space) = self.get_layer_width_space(zindex)
        layer = self.get_layer(zindex)

        # This finds the pin shape enclosed by the track with DRC spacing on the sides
        (abs_ll,unused) = self.convert_track_to_pin(ll)
        (unused,abs_ur) = self.convert_track_to_pin(ur)
        #print("enclose ll={0} ur={1}".format(ll,ur))
        #print("enclose ll={0} ur={1}".format(abs_ll,abs_ur))
        
        if name:
            pin = self.cell.add_layout_pin(name,
                                           layer=layer,
                                           offset=abs_ll,
                                           width=abs_ur.x-abs_ll.x,
                                           height=abs_ur.y-abs_ll.y)
        else:
            pin = self.cell.add_rect(layer=layer,
                                     offset=abs_ll,
                                     width=abs_ur.x-abs_ll.x,
                                     height=abs_ur.y-abs_ll.y)
        return pin
            

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
    

    def add_path_blockages(self):
        """
        Go through all of the past paths and add them as blockages.
        This is so we don't have to write/reload the GDS.
        """
        for path in self.paths:
            self.rg.block_path(path)
            
    def run_router(self, detour_scale):
        """
        This assumes the blockages, source, and target are all set up. 
        """
        # returns the path in tracks
        (path,cost) = self.rg.route(detour_scale)
        if path:
            debug.info(1,"Found path: cost={0} ".format(cost))
            debug.info(2,str(path))
            self.paths.append(path)
            self.add_route(path)
        else:
            self.write_debug_gds()
            # clean up so we can try a reroute
            self.reinit()
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
            (ll,ur) = self.convert_track_to_pin(coord)
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
        # Only add the debug info to the gds file if we have any debugging on.
        # This is because we may reroute a wire with detours and don't want the debug information.
        if OPTS.debug_level==0: return
        
        self.add_router_info()
        self.cell.gds_write(gds_name)

        if stop_program:
            import sys
            sys.exit(1)
        
    def add_router_info(self):
        """
        Write the routing grid and router cost, blockage, pins on 
        the boundary layer for debugging purposes. This can only be 
        called once or the labels will overlap.
        """
        debug.info(0,"Adding router info")

        if OPTS.debug_level==0:
            # Display the inflated blockage
            for blockage in self.blockages:
                debug.info(1,"Adding {}".format(blockage))
                (ll,ur) = blockage.inflate()
                self.cell.add_rect(layer="text",
                                   offset=ll,
                                   width=ur.x-ll.x,
                                   height=ur.y-ll.y)
        if OPTS.debug_level>1:
            #self.set_blockages(self.blocked_grids,True)
            grid_keys=self.rg.map.keys()
            partial_track=vector(0,self.track_width/6.0)
            for g in grid_keys:
                shape = self.convert_track_to_shape(g)
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

    
# FIXME: This should be replaced with vector.snap_to_grid at some point

def snap_to_grid(offset):
    """
    Changes the coodrinate to match the grid settings
    """
    xoff = snap_val_to_grid(offset[0])
    yoff = snap_val_to_grid(offset[1])    
    return vector(xoff, yoff)

def snap_val_to_grid(x):
    grid = tech.drc["grid"]
    xgrid = int(round(round((x / grid), 2), 0))
    xoff = xgrid * grid
    return xoff
