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

        self.pins = {}
        # the list of all blockage shapes
        self.blockages = []
        # all the paths we've routed so far (to supplement the blockages)
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




    def find_pin(self,pin):
        """ 
        Finds the pin shapes and converts to tracks. 
        Pin can either be a label or a location,layer pair: [[x,y],layer].
        """

        label_list=self.layout.getPinShapeByLabel(str(pin))
        pin_list = []
        for label in label_list:
            (name,layer,boundary)=label
            rect = [vector(boundary[0],boundary[1]),vector(boundary[2],boundary[3])]
            # this is a list because other cells/designs may have must-connect pins
            pin_list.append(pin_layout(pin, rect, layer))

        debug.check(len(pin_list)>0,"Did not find any pin shapes for {0}.".format(str(pin)))

        return pin_list


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
        """ Add the blockages except the pin shapes """
        for blockage in self.blockages:
            # Skip pin shapes
            all_pins = [x[0] for x in list(self.pins.values())]
            for pin in all_pins:
                if blockage.overlaps(pin):
                    break
            else:
                [ll,ur]=self.convert_blockage_to_tracks(blockage.rect)
                zlayer = 0 if blockage.layer_num==self.horiz_layer_number else 1
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
                # store the blockages as pin layouts so they are easy to compare etc.
                self.blockages.append(pin_layout("blockage",shape,boundary.drawingLayer))
                

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

    def convert_pin_to_tracks(self, pin):
        """ 
        Convert a rectangular pin shape into a list of track locations,layers.
        If no on-grid pins are found, it searches for the nearest off-grid pin(s).
        If a pin has insufficent overlap, it returns the blockage list to avoid it.
        """
        [ll,ur] = pin.rect
        ll = snap_to_grid(ll)
        ur = snap_to_grid(ur)

        #debug.info(1,"Converting [ {0} , {1} ]".format(ll,ur))
        
        # scale the size bigger to include neaby tracks
        ll=ll.scale(self.track_factor).floor()
        ur=ur.scale(self.track_factor).ceil()

        # width depends on which layer it is
        zindex = 0 if pin.layer_num==self.horiz_layer_number else 1
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
                max_overlap=max(self.compute_overlap(pin.rect,rect))

                # however, if there is not enough overlap, then if there is any overlap at all,
                # we need to block it to prevent routes coming in on that grid
                full_rect = self.convert_full_track_to_shape(vector3d(x,y,zindex))
                full_overlap=max(self.compute_overlap(pin.rect,full_rect))
                
                #debug.info(1,"Check overlap: {0} {1} max={2}".format(shape,rect,max_overlap))
                if max_overlap >= width:
                    track_list.append(vector3d(x,y,zindex))
                elif full_overlap>0:
                    block_list.append(vector3d(x,y,zindex))
                else:
                    debug.info(4,"No overlap: {0} {1} max={2}".format(pin.rect,rect,max_overlap))

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

