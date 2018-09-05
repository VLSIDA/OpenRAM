import gdsMill
import tech
from contact import contact
import math
import debug
from pin_layout import pin_layout
from vector import vector
from vector3d import vector3d 
from globals import OPTS

class router:
    """
    A router class to read an obstruction map from a gds and plan a
    route on a given layer. This is limited to two layer routes.
    It populates blockages on a grid class.
    """

    def __init__(self, gds_name=None, module=None):
        """Use the gds file or the cell for the blockages with the top module topName and
        layers for the layers to route on
        """
        self.gds_name = gds_name
        self.module = module
        debug.check(not (gds_name and module), "Specify only a GDS file or module")

        # If we specified a module instead, write it out to read the gds
        # This isn't efficient, but easy for now
        if module:
            gds_name = OPTS.openram_temp+"temp.gds"
            module.gds_write(gds_name)
        
        # Load the gds file and read in all the shapes
        self.layout = gdsMill.VlsiLayout(units=tech.GDS["unit"])
        self.reader = gdsMill.Gds2reader(self.layout)
        self.reader.loadFromFile(gds_name)
        self.top_name = self.layout.rootStructureName

        self.pins = {}
        self.blockages=[]
        # all the paths we've routed so far (to supplement the blockages)
        self.paths = []

        # The boundary will determine the limits to the size of the routing grid
        self.boundary = self.layout.measureBoundary(self.top_name)
        self.ll = vector(self.boundary[0])
        self.ur = vector(self.boundary[1])

    def set_top(self,top_name):
        """ If we want to route something besides the top-level cell."""
        self.top_name = top_name

    def get_zindex(self,layer_num):
        if layer_num==self.horiz_layer_number:
            return 0
        else:
            return 1

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




    def find_pin(self,pin_name):
        """ 
        Finds the pin shapes and converts to tracks. 
        Pin can either be a label or a location,layer pair: [[x,y],layer].
        """

        shape_list=self.layout.getAllPinShapesByLabel(str(pin_name))
        pin_list = []
        for shape in shape_list:
            (name,layer,boundary)=shape
            rect = [vector(boundary[0],boundary[1]),vector(boundary[2],boundary[3])]
            pin = pin_layout(pin_name, rect, layer)
            debug.info(2,"Found pin {}".format(str(pin)))
            pin_list.append(pin)

        debug.check(len(pin_list)>0,"Did not find any pin shapes for {0}.".format(str(pin)))

        return pin_list


    def find_blockages(self):
        """
        Iterate through all the layers and write the obstacles to the routing grid.
        This doesn't consider whether the obstacles will be pins or not. They get reset later
        if they are not actually a blockage.
        """
        #for layer in [self.vert_layer_number,self.horiz_layer_number]:
        #    self.get_blockages(layer)
        self.get_blockages(self.horiz_layer_number)
            
    def clear_pins(self):
        """
        Reset the source and destination pins to start a new routing.
        Convert the source/dest pins to blockages.
        Convert the routed path to blockages.
        Keep the other blockages unchanged.
        """
        self.pins = {}
        # DO NOT clear the blockages as these don't change
        self.rg.reinit()
        

    
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
        

    def add_blockages(self):
        """ Add the blockages except the pin shapes. Also remove the pin shapes from the blockages list. """
        # Join all the pin shapes into one big list
        all_pins = [item for sublist in list(self.pins.values()) for item in sublist]

        # Do an n^2 check to see if any shapes are the same, otherwise add them
        # FIXME: Make faster, but number of pins won't be *that* large
        real_blockages = []
        for blockage in self.blockages:
            for pin in all_pins:
                # If the blockage overlaps the pin and is on the same layer,
                # it must be connected, so skip it.
                if blockage.overlaps(pin):
                    debug.info(1,"Removing blockage for pin {}".format(str(pin)))
                    break
            else:
                debug.info(2,"Adding blockage {}".format(str(blockage)))
                # Inflate the blockage by spacing rule
                [ll,ur]=self.convert_blockage_to_tracks(blockage.inflate())
                zlayer = self.get_zindex(blockage.layer_num)
                self.rg.add_blockage_shape(ll,ur,zlayer)
                real_blockages.append(blockage)

        # Remember the filtered blockages
        self.blockages = real_blockages

        
    def get_blockages(self, layer_num): 
        """
        Recursive find boundaries as blockages to the routing grid.
        """

        shapes = self.layout.getAllShapesInStructureList(layer_num)
        for boundary in shapes:
            ll = vector(boundary[0],boundary[1])
            ur = vector(boundary[2],boundary[3])
            rect = [ll,ur]
            new_pin = pin_layout("blockage{}".format(len(self.blockages)),rect,layer_num)
            self.blockages.append(new_pin)


    def convert_point_to_units(self,p):
        """ 
        Convert a path set of tracks to center line path.
        """
        pt = vector3d(p)
        pt=pt.scale(self.track_widths[0],self.track_widths[1],1)
        return pt

    def convert_blockage_to_tracks(self,shape):
        """ 
        Convert a rectangular blockage shape into track units.
        """
        (ll,ur) = shape
        # ll = snap_to_grid(ll)
        # ur = snap_to_grid(ur)

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

    def convert_pin_to_tracks(self, pin):
        """ 
        Convert a rectangular pin shape into a list of track locations,layers.
        If no on-grid pins are found, it searches for the nearest off-grid pin(s).
        If a pin has insufficent overlap, it returns the blockage list to avoid it.
        """
        (ll,ur) = pin.rect
        debug.info(1,"Converting [ {0} , {1} ]".format(ll,ur))
        
        # scale the size bigger to include neaby tracks
        ll=ll.scale(self.track_factor).floor()
        ur=ur.scale(self.track_factor).ceil()

        # width depends on which layer it is
        zindex=self.get_zindex(pin.layer_num)
        if zindex:
            width = self.vert_layer_width            
        else:
            width = self.horiz_layer_width

        track_list = []
        block_list = []

        for x in range(ll[0],ur[0]):
            for y in range(ll[1],ur[1]):
                debug.info(1,"Converting [ {0} , {1} ]".format(x,y))

                # however, if there is not enough overlap, then if there is any overlap at all,
                # we need to block it to prevent routes coming in on that grid
                full_rect = self.convert_track_to_shape(vector3d(x,y,zindex))
                track_area = (full_rect[1].x-full_rect[0].x)*(full_rect[1].y-full_rect[0].y)
                overlap_rect=self.compute_overlap(pin.rect,full_rect)
                overlap_area = overlap_rect[0]*overlap_rect[1]
                debug.info(1,"Check overlap: {0} {1} max={2}".format(pin.rect,overlap_rect,overlap_area))
                
                # Assume if more than half the area, it is occupied
                overlap_ratio = overlap_area/track_area
                if overlap_ratio > 0.25:
                    track_list.append(vector3d(x,y,zindex))
                # otherwise, the pin may not be accessible, so block it
                elif overlap_ratio > 0:
                    block_list.append(vector3d(x,y,zindex))
                else:
                    debug.info(4,"No overlap: {0} {1} max={2}".format(pin.rect,overlap_rect,overlap_area))
                # print("H:",x,y)
                # if x>38 and x<42 and y>42 and y<45:
                #     print(pin)
                #     print(full_rect, overlap_rect, overlap_ratio)
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

    def convert_track_to_shape(self,track):
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
    

    def get_pin(self,pin_name):
        """ 
        Gets the pin shapes only. Doesn't add to grid.
        """
        self.pins[pin_name] = self.find_pin(pin_name)

    def add_pin(self,pin_name,is_source=False):
        """ 
        Mark the grids that are in the pin rectangle ranges to have the pin property. 
        pin can be a location or a label.
        """

        found_pin = False
        for pin in self.pins[pin_name]:
            (pin_in_tracks,blockage_in_tracks)=self.convert_pin_to_tracks(pin)
            if (len(pin_in_tracks)>0):
                found_pin=True
            if is_source:
                debug.info(1,"Set source: " + str(pin_name) + " " + str(pin_in_tracks))
                self.rg.add_source(pin_in_tracks)
            else:
                debug.info(1,"Set target: " + str(pin_name) + " " + str(pin_in_tracks))
                self.rg.add_target(pin_in_tracks)
            self.rg.add_blockage(blockage_in_tracks)
            
        if not found_pin:
            self.write_debug_gds()
        debug.check(found_pin,"Unable to find pin on grid.")

    def write_debug_gds(self):
        """ 
        Write out a GDS file with the routing grid and search information annotated on it.
        """
        # Only add the debug info to the gds file if we have any debugging on.
        # This is because we may reroute a wire with detours and don't want the debug information.
        if OPTS.debug_level==0: return
        
        self.add_router_info()
        debug.error("Writing debug_route.gds")
        self.cell.gds_write("debug_route.gds")

    def add_router_info(self):
        """
        Write the routing grid and router cost, blockage, pins on 
        the boundary layer for debugging purposes. This can only be 
        called once or the labels will overlap.
        """
        debug.info(0,"Adding router info")
        grid_keys=self.rg.map.keys()
        partial_track=vector(0,self.track_width/6.0)
        for g in grid_keys:
            shape = self.convert_track_to_shape(g)
            self.cell.add_rect(layer="text",
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
                                offset=shape[0],
                                zoom=0.05)

        for blockage in self.blockages:
            # Display the inflated blockage
            (ll,ur) = blockage.inflate()
            self.cell.add_rect(layer="blockage",
                               offset=ll,
                               width=ur.x-ll.x,
                               height=ur.y-ll.y)


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

            
        # First, simplify the path for
        #debug.info(1,str(self.path))        
        contracted_path = self.contract_path(path)
        debug.info(1,str(contracted_path))

        # convert the path back to absolute units from tracks
        abs_path = map(self.convert_point_to_units,contracted_path)
        debug.info(1,str(abs_path))
        self.cell.add_route(self.layers,abs_path)


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
            self.rg.block_path(path)
            

        
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

