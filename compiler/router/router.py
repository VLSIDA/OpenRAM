import gdsMill
import tech
from contact import contact
import math
import debug
import grid
from vector import vector
from vector3d import vector3d 
from globals import OPTS

class router:
    """A router class to read an obstruction map from a gds and plan a
    route on a given layer. This is limited to two layer routes.
    """

    def __init__(self, gds_name):
        """Use the gds file for the blockages with the top module topName and
        layers for the layers to route on
        """
        # Load the gds file and read in all the shapes
        self.gds_name = gds_name
        self.layout = gdsMill.VlsiLayout(units=tech.GDS["unit"])
        self.reader = gdsMill.Gds2reader(self.layout)
        self.reader.loadFromFile(gds_name)
        self.top_name = self.layout.rootStructureName

        self.source_pin_shapes = []
        self.source_pin_zindex = None
        self.target_pin_shapes = []
        self.target_pin_zindex = None
        # the list of all blockage shapes
        self.blockages = []
        # all thepaths we've routed so far (to supplement the blockages)
        self.paths = []

        # The boundary will determine the limits to the size of the routing grid
        self.boundary = self.layout.measureBoundary(self.top_name)
        self.ll = vector(self.boundary[0])
        self.ur = vector(self.boundary[1])

    def set_top(self,top_name):
        """ If we want to route something besides the top-level cell."""
        self.top_name = top_name

    def set_layers(self, layers):
        """Allows us to change the layers that we are routing on. First layer
        is always horizontal, middle is via, and last is always
        vertical.
        """
        self.layers = layers
        (horiz_layer, via_layer, vert_layer) = self.layers

        self.vert_layer_name = vert_layer
        self.vert_layer_width = tech.drc["minwidth_{0}".format(vert_layer)]
        self.vert_layer_spacing = tech.drc[str(self.vert_layer_name)+"_to_"+str(self.vert_layer_name)] 
        self.vert_layer_number = tech.layer[vert_layer]
        
        self.horiz_layer_name = horiz_layer
        self.horiz_layer_width = tech.drc["minwidth_{0}".format(horiz_layer)]
        self.horiz_layer_spacing = tech.drc[str(self.horiz_layer_name)+"_to_"+str(self.horiz_layer_name)] 
        self.horiz_layer_number = tech.layer[horiz_layer]

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



    def create_routing_grid(self):
        """ 
        Create a routing grid that spans given area. Wires cannot exist outside region. 
        """
        # We will add a halo around the boundary
        # of this many tracks
        size = self.ur - self.ll
        debug.info(1,"Size: {0} x {1}".format(size.x,size.y))

        self.rg = grid.grid()
        

    def find_pin(self,pin):
        """ 
        Finds the pin shapes and converts to tracks. 
        Pin can either be a label or a location,layer pair: [[x,y],layer].
        """

        if type(pin)==str:
            (pin_name,pin_layer,pin_shapes) = self.layout.getAllPinShapesByLabel(str(pin))
        else:
            (pin_name,pin_layer,pin_shapes) = self.layout.getAllPinShapesByLocLayer(pin[0],pin[1])

        new_pin_shapes = []
        for pin_shape in pin_shapes:
            debug.info(2,"Find pin {0} layer {1} shape {2}".format(pin_name,str(pin_layer),str(pin_shape)))
            # repack the shape as a pair of vectors rather than four values
            new_pin_shapes.append([vector(pin_shape[0],pin_shape[1]),vector(pin_shape[2],pin_shape[3])])
            
        debug.check(len(new_pin_shapes)>0,"Did not find any pin shapes for {0}.".format(str(pin)))
        
        return (pin_layer,new_pin_shapes)

    def find_blockages(self):
        """
        Iterate through all the layers and write the obstacles to the routing grid.
        This doesn't consider whether the obstacles will be pins or not. They get reset later
        if they are not actually a blockage.
        """
        for layer in self.layers:
            self.get_blockages(self.top_name)

            
    def clear_pins(self):
        """
        Reset the source and destination pins to start a new routing.
        Convert the source/dest pins to blockages.
        Convert the routed path to blockages.
        Keep the other blockages unchanged.
        """
        self.source_pin = None
        self.source_pin_shapes = []
        self.source_pin_zindex = None
        self.target_pin = None
        self.target_pin_shapes = []
        self.target_pin_zindex = None
        # DO NOT clear the blockages as these don't change
        self.rg.reinit()
        

    def route(self, cell, layers, src, dest, detour_scale=2):
        """ 
        Route a single source-destination net and return
        the simplified rectilinear path. Cost factor is how sub-optimal to explore for a feasible route. 
        This is used to speed up the routing when there is not much detouring needed.
        """
        self.cell = cell

        # Clear the pins if we have previously routed
        if (hasattr(self,'rg')):
            self.clear_pins()
        else:
            # Set up layers and track sizes
            self.set_layers(layers)
            # Creat a routing grid over the entire area
            # FIXME: This could be created only over the routing region,
            # but this is simplest for now.
            self.create_routing_grid()
            # This will get all shapes as blockages
            self.find_blockages()

        # Get the pin shapes
        self.get_source(src)
        self.get_target(dest)
        
        # Now add the blockages (all shapes except the src/tgt pins)
        self.add_blockages()
        # Add blockages from previous paths
        self.add_path_blockages()        

        # Now add the src/tgt if they are not blocked by other shapes
        self.add_source()
        self.add_target()

            
        # returns the path in tracks
        (path,cost) = self.rg.route(detour_scale)
        if path:
            debug.info(1,"Found path: cost={0} ".format(cost))
            debug.info(2,str(path))
            self.add_route(path)
            return True
        else:
            self.write_debug_gds()
            # clean up so we can try a reroute
            self.clear_pins()
            

        return False

    def write_debug_gds(self,):
        """ 
        Write out a GDS file with the routing grid and search information annotated on it.
        """
        # Only add the debug info to the gds file if we have any debugging on.
        # This is because we may reroute a wire with detours and don't want the debug information.
        if OPTS.debug_level==0: return
        
        self.add_router_info()
        debug.error("Writing debug_route.gds from {0} to {1}".format(self.source_pin,self.target_pin))
        self.cell.gds_write("debug_route.gds")

    def add_router_info(self):
        """
        Write the routing grid and router cost, blockage, pins on 
        the boundary layer for debugging purposes. This can only be 
        called once or the labels will overlap.
        """
        debug.info(0,"Adding router info for {0} to {1}".format(self.source_pin,self.target_pin))
        grid_keys=self.rg.map.keys()
        partial_track=vector(0,self.track_width/6.0)
        for g in grid_keys:
            shape = self.convert_full_track_to_shape(g)
            self.cell.add_rect(layer="boundary",
                               offset=shape[0],
                               width=shape[1].x-shape[0].x,
                               height=shape[1].y-shape[0].y)
            # These are the on grid pins
            #rect = self.convert_track_to_pin(g)
            #self.cell.add_rect(layer="boundary",
            #                   offset=rect[0],
            #                   width=rect[1].x-rect[0].x,
            #                   height=rect[1].y-rect[0].y)
            
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
                                offset=shape[0])
                           
    def add_route(self,path):
        """ 
        Add the current wire route to the given design instance.
        """
        debug.info(3,"Set path: " + str(path))

        # Keep track of path for future blockages
        self.paths.append(path)
        
        # This is marked for debug
        self.rg.add_path(path)

        # For debugging... if the path failed to route.
        if False or path==None:
            self.write_debug_gds()

        if 'Xout_4_1' in [self.source_pin, self.target_pin]:
            self.write_debug_gds()

            
        # First, simplify the path for
        #debug.info(1,str(self.path))        
        contracted_path = self.contract_path(path)
        debug.info(1,str(contracted_path))
        
        # Make sure there's a pin enclosure on the source and dest
        add_src_via = contracted_path[0].z!=self.source_pin_zindex
        self.add_grid_pin(contracted_path[0],add_src_via)
        add_tgt_via = contracted_path[-1].z!=self.target_pin_zindex
        self.add_grid_pin(contracted_path[-1],add_tgt_via)

        # convert the path back to absolute units from tracks
        abs_path = map(self.convert_point_to_units,contracted_path)
        debug.info(1,str(abs_path))
        self.cell.add_route(self.layers,abs_path)

    
    def add_grid_pin(self,point,add_via=False):
        """
        Create a rectangle at the grid 3D point that is 1/2 DRC smaller
        than the routing grid on all sides.
        """
        pin = self.convert_track_to_pin(point)
        self.cell.add_rect(layer=self.layers[2*point.z],
                           offset=pin[0],
                           width=pin[1].x-pin[0].x,
                           height=pin[1].y-pin[0].y)

        if add_via:
            # offset this by 1/2 the via size
            c=contact(self.layers, (1, 1))
            via_offset = vector(-0.5*c.width,-0.5*c.height)
            self.cell.add_via(self.layers,vector(point[0],point[1])+via_offset)

        
    def create_steiner_routes(self,pins):
        """
        Find a set of steiner points and then return the list of
        point-to-point routes.
        """
        pass

    def find_steiner_points(self,pins):
        """ 
        Find the set of steiner points and return them.
        """
        pass

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

        
    def contract_path(self,path):
        """ 
        Remove intermediate points in a rectilinear path. 
        """
        newpath = [path[0]]
        for i in range(1,len(path)-1):
            prev_inertia=self.get_inertia(path[i-1],path[i])
            next_inertia=self.get_inertia(path[i],path[i+1])
            # if we switch directions, add the point, otherwise don't
            if prev_inertia!=next_inertia:
                newpath.append(path[i])

        # always add the last path
        newpath.append(path[-1])
        return newpath
    

    def add_path_blockages(self):
        """
        Go through all of the past paths and add them as blockages.
        This is so we don't have to write/reload the GDS.
        """
        for path in self.paths:
            for grid in path:
                self.rg.set_blocked(grid)
        

    def get_source(self,pin):
        """ 
        Gets the source pin shapes only. Doesn't add to grid.
        """
        self.source_pin = pin        
        (self.source_pin_layer,self.source_pin_shapes) = self.find_pin(pin)
        zindex = 0 if self.source_pin_layer==self.horiz_layer_number else 1
        self.source_pin_zindex = zindex

    def add_source(self):
        """ 
        Mark the grids that are in the pin rectangle ranges to have the source property. 
        pin can be a location or a label.
        """

        found_pin = False
        for shape in self.source_pin_shapes:
            (pin_in_tracks,blockage_in_tracks)=self.convert_pin_to_tracks(shape,self.source_pin_zindex,self.source_pin)
            if (len(pin_in_tracks)>0): found_pin=True
            debug.info(1,"Set source: " + str(self.source_pin) + " " + str(pin_in_tracks) + " z=" + str(self.source_pin_zindex))
            self.rg.add_source(pin_in_tracks)
            self.rg.add_blockage(blockage_in_tracks)
            
        if not found_pin:
            self.write_debug_gds()
        debug.check(found_pin,"Unable to find source pin on grid.")

    def get_target(self,pin):
        """ 
        Gets the target pin shapes only. Doesn't add to grid.
        """
        self.target_pin = pin
        (self.target_pin_layer,self.target_pin_shapes) = self.find_pin(pin)
        zindex = 0 if self.target_pin_layer==self.horiz_layer_number else 1
        self.target_pin_zindex = zindex
        
    def add_target(self):
        """ 
        Mark the grids that are in the pin rectangle ranges to have the target property. 
        pin can be a location or a label.
        """
        found_pin=False
        for shape in self.target_pin_shapes:
            (pin_in_tracks,blockage_in_tracks)=self.convert_pin_to_tracks(shape,self.target_pin_zindex,self.target_pin)
            if (len(pin_in_tracks)>0): found_pin=True
            debug.info(1,"Set target: " + str(self.target_pin) + " " + str(pin_in_tracks) + " z=" + str(self.target_pin_zindex))
            self.rg.add_target(pin_in_tracks)
            self.rg.add_blockage(blockage_in_tracks)            

        if not found_pin:
            self.write_debug_gds()
        debug.check(found_pin,"Unable to find target pin on grid.")            

    def add_blockages(self):
        """ Add the blockages except the pin shapes """
        for blockage in self.blockages:
            (shape,zlayer) = blockage
            # Skip source pin shapes
            if zlayer==self.source_pin_zindex and shape in self.source_pin_shapes:
                continue
            # Skip target pin shapes
            if zlayer==self.target_pin_zindex and shape in self.target_pin_shapes:
                continue
            [ll,ur]=self.convert_blockage_to_tracks(shape)
            self.rg.add_blockage_shape(ll,ur,zlayer)

        
    def get_blockages(self, sref, mirr = 1, angle = math.radians(float(0)), xyShift = (0, 0)): 
        """
        Recursive find boundaries as blockages to the routing grid.
        Recurses for each Structure in GDS.
        """
        for boundary in self.layout.structures[sref].boundaries:
            coord_trans = self.translate_coordinates(boundary.coordinates, mirr, angle, xyShift)
            shape_coords = self.min_max_coord(coord_trans)
            shape = self.convert_shape_to_units(shape_coords)

            # only consider the two layers that we are routing on
            if boundary.drawingLayer in [self.vert_layer_number,self.horiz_layer_number]:
                zlayer = 0 if boundary.drawingLayer==self.horiz_layer_number else 1
                self.blockages.append((shape,zlayer))
                

        # recurse given the mirror, angle, etc.
        for cur_sref in self.layout.structures[sref].srefs:
            sMirr = 1
            if cur_sref.transFlags[0] == True:
                sMirr = -1
            sAngle = math.radians(float(0))
            if cur_sref.rotateAngle:
                sAngle = math.radians(float(cur_sref.rotateAngle))
            sAngle += angle
            x = cur_sref.coordinates[0]
            y = cur_sref.coordinates[1]
            newX = (x)*math.cos(angle) - mirr*(y)*math.sin(angle) + xyShift[0] 
            newY = (x)*math.sin(angle) + mirr*(y)*math.cos(angle) + xyShift[1] 
            sxyShift = (newX, newY)
            
            self.get_blockages(cur_sref.sName, sMirr, sAngle, sxyShift)

    def convert_point_to_units(self,p):
        """ 
        Convert a path set of tracks to center line path.
        """
        pt = vector3d(p)
        pt=pt.scale(self.track_widths[0],self.track_widths[1],1)
        return pt

    def convert_blockage_to_tracks(self,shape,round_bigger=False):
        """ 
        Convert a rectangular blockage shape into track units.
        """
        [ll,ur] = shape
        ll = snap_to_grid(ll)
        ur = snap_to_grid(ur)

        # to scale coordinates to tracks
        #debug.info(1,"Converting [ {0} , {1} ]".format(ll,ur))
        ll=ll.scale(self.track_factor)
        ur=ur.scale(self.track_factor)
        ll = ll.floor() if round_bigger else ll.round()
        ur = ur.ceil() if round_bigger else ur.round()
        #debug.info(1,"Converted [ {0} , {1} ]".format(ll,ur))
        return [ll,ur]

    def convert_pin_to_tracks(self,shape,zindex,pin):
        """ 
        Convert a rectangular pin shape into a list of track locations,layers.
        If no on-grid pins are found, it searches for the nearest off-grid pin(s).
        If a pin has insufficent overlap, it returns the blockage list to avoid it.
        """
        [ll,ur] = shape
        ll = snap_to_grid(ll)
        ur = snap_to_grid(ur)

        #debug.info(1,"Converting [ {0} , {1} ]".format(ll,ur))
        
        # scale the size bigger to include neaby tracks
        ll=ll.scale(self.track_factor).floor()
        ur=ur.scale(self.track_factor).ceil()

        # width depends on which layer it is
        if zindex==0:
            width = self.horiz_layer_width
        else:
            width = self.vert_layer_width            

        track_list = []
        block_list = []
        # include +- 1 so when a shape is less than one grid
        for x in range(ll[0]-1,ur[0]+1):
            for y in range(ll[1]-1,ur[1]+1):
                #debug.info(1,"Converting [ {0} , {1} ]".format(x,y))
                # get the rectangular pin at a track location
                # if dimension of overlap is greater than min width in any dimension,
                # it will be an on-grid pin
                rect = self.convert_track_to_pin(vector3d(x,y,zindex))
                max_overlap=max(self.compute_overlap(shape,rect))

                # however, if there is not enough overlap, then if there is any overlap at all,
                # we need to block it to prevent routes coming in on that grid
                full_rect = self.convert_full_track_to_shape(vector3d(x,y,zindex))
                full_overlap=max(self.compute_overlap(shape,full_rect))
                
                #debug.info(1,"Check overlap: {0} {1} max={2}".format(shape,rect,max_overlap))
                if max_overlap >= width:
                    track_list.append(vector3d(x,y,zindex))
                elif full_overlap>0:
                    block_list.append(vector3d(x,y,zindex))
                else:
                    debug.info(1,"No overlap: {0} {1} max={2}".format(shape,rect,max_overlap))

        #debug.warning("Off-grid pin for {0}.".format(str(pin)))
        #debug.info(1,"Converted [ {0} , {1} ]".format(ll,ur))
        return (track_list,block_list)

    def compute_overlap(self,r1,r2):
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
            

    def convert_track_to_pin(self,track):
        """ 
        Convert a grid point into a rectangle shape that is centered
        track in the track and leaves half a DRC space in each direction.
        """
        # space depends on which layer it is
        if track[2]==0:
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

    def convert_full_track_to_shape(self,track):
        """ 
        Convert a grid point into a rectangle shape that occupies the entire centered
        track.
        """
        # to scale coordinates to tracks
        x = track.x*self.track_width - 0.5*self.track_width
        y = track.y*self.track_width - 0.5*self.track_width
        # offset lowest corner object to to (-track halo,-track halo)
        ll = snap_to_grid(vector(x,y))
        ur = snap_to_grid(ll + vector(self.track_width,self.track_width))

        return [ll,ur]
    

# FIXME: This should be replaced with vector.snap_to_grid at some point

def snap_to_grid(offset):
    """
    Changes the coodrinate to match the grid settings
    """
    grid = tech.drc["grid"]  
    x = offset[0]
    y = offset[1]
    # this gets the nearest integer value
    xgrid = int(round(round((x / grid), 2), 0))
    ygrid = int(round(round((y / grid), 2), 0))
    xoff = xgrid * grid
    yoff = ygrid * grid
    return vector(xoff, yoff)

