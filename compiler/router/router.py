import gdsMill
import tech
from contact import contact
import math
import debug
import grid
from vector import vector
from vector3d import vector3d 


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

        # The boundary will determine the limits to the size of the routing grid
        self.boundary = self.layout.measureBoundary(self.top_name)
        self.ll = vector(self.boundary[0])
        self.ur = vector(self.boundary[1])


    def set_top(self,top_name):
        """ If we want to route something besides the top-level cell."""
        self.top_name = top_name

    def set_layers(self, layers):
        """ Allows us to change the layers that we are routing on. """
        self.layers = layers
        (horiz_layer, via_layer, vert_layer) = self.layers

        self.vert_layer_name = vert_layer
        self.vert_layer_width = tech.drc["minwidth_{0}".format(vert_layer)]
        self.vert_layer_number = tech.layer[vert_layer]
        
        self.horiz_layer_name = horiz_layer
        self.horiz_layer_width = tech.drc["minwidth_{0}".format(horiz_layer)]
        self.horiz_layer_number = tech.layer[horiz_layer]

        # Contacted track spacing.
        via_connect = contact(self.layers, (1, 1))
        max_via_size = max(via_connect.width,via_connect.height)
        horiz_layer_spacing = tech.drc[str(self.horiz_layer_name)+"_to_"+str(self.horiz_layer_name)] 
        vert_layer_spacing = tech.drc[str(self.vert_layer_name)+"_to_"+str(self.vert_layer_name)] 
        self.horiz_track_width = max_via_size + horiz_layer_spacing
        self.vert_track_width = max_via_size + vert_layer_spacing

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
            
        return (pin_layer,new_pin_shapes)

    def find_blockages(self):
        """
        Iterate through all the layers and write the obstacles to the routing grid.
        This doesn't consider whether the obstacles will be pins or not. They get reset later
        if they are not actually a blockage.
        """
        for layer in self.layers:
            self.write_obstacle(self.top_name)

            
    def clear_pins(self):
        """
        Reset the source and destination pins to start a new routing.
        Convert the source/dest pins to blockages.
        Convert the routed path to blockages.
        Keep the other blockages unchanged.
        """
        self.source_pin_shapes = []
        self.source_pin_zindex = None
        self.target_pin_shapes = []
        self.target_pin_zindex = None
        self.rg.reinit()
        

    def route(self, layers, src, dest, cost_bound_scale=1):
        """ 
        Route a single source-destination net and return
        the simplified rectilinear path. Cost factor is how sub-optimal to explore for a feasible route. 
        This is used to speed up the routing when there is not much detouring needed.
        """
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
            # This will write all shapes as blockages, but setting pins will
            # clear the blockage attribute
            self.find_blockages()

        self.set_source(src)

        self.set_target(dest)

        # View the initial route pins and blockages for debugging
        #self.rg.view()
        
        # returns the path in tracks
        (self.path,cost) = self.rg.route(cost_bound_scale)
        debug.info(1,"Found path: cost={0} ".format(cost))
        debug.info(2,str(self.path))
        self.set_path(self.path)
        # View the final route for debugging
        #self.rg.view()        
        
        return 

    def add_route(self,cell):
        """ 
        Add the current wire route to the given design instance.
        """
        # First, simplify the path for
        #debug.info(1,str(self.path))        
        contracted_path = self.contract_path(self.path)
        debug.info(1,str(contracted_path))
        
        # Make sure there's a pin enclosure on the source and dest
        src_shape = self.convert_track_to_shape(contracted_path[0])
        cell.add_rect(layer=self.layers[2*contracted_path[0].z],
                      offset=src_shape[0],
                      width=src_shape[1].x-src_shape[0].x,
                      height=src_shape[1].y-src_shape[0].y)

        dest_shape = self.convert_track_to_shape(contracted_path[-1])
        cell.add_rect(layer=self.layers[2*contracted_path[-1].z],
                      offset=dest_shape[0],
                      width=dest_shape[1].x-dest_shape[0].x,
                      height=dest_shape[1].y-dest_shape[0].y)


        # convert the path back to absolute units from tracks
        abs_path = map(self.convert_point_to_units,contracted_path)
        debug.info(1,str(abs_path))
        cell.add_route(self.layers,abs_path)

        # Check if a via is needed at the start point
        if (contracted_path[0].z!=self.source_pin_zindex):
            # offset this by 1/2 the via size
            c=contact(self.layers, (1, 1))
            via_offset = vector(-0.5*c.width,-0.5*c.height)
            cell.add_via(self.layers,abs_path[0]+via_offset)

        # Check if a via is needed at the end point
        if (contracted_path[-1].z!=self.target_pin_zindex):
            # offset this by 1/2 the via size
            c=contact(self.layers, (1, 1))
            via_offset = vector(-0.5*c.width,-0.5*c.height)
            cell.add_via(self.layers,abs_path[-1]+via_offset)

        
    
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
    
    def set_path(self,path):
        """
        Mark the path in the routing grid.
        """
        debug.info(3,"Set path: " + str(path))        
        self.rg.set_path(path)

    def set_source(self,src):
        """ 
        Mark the grids that are in the pin rectangle ranges to have the source property. 
        """
        (pin_layer,self.source_pin_shapes) = self.find_pin(src)
        zindex = 0 if pin_layer==self.horiz_layer_number else 1
        self.source_pin_zindex = zindex
        for shape in self.source_pin_shapes:
            shape_in_tracks=self.convert_shape_to_tracks(shape)
            debug.info(1,"Set source: " + str(src) + " " + str(shape_in_tracks) + " z=" + str(zindex))
            self.rg.set_source(shape_in_tracks[0],shape_in_tracks[1],zindex)


    def set_target(self,src):
        """ 
        Mark the grids that are in the pin rectangle ranges to have the target property. 
        """
        (pin_layer,self.target_pin_shapes) = self.find_pin(src)
        zindex = 0 if pin_layer==self.horiz_layer_number else 1
        self.target_pin_zindex = zindex
        for shape in self.target_pin_shapes:
            shape_in_tracks=self.convert_shape_to_tracks(shape)  
            debug.info(1,"Set target: " + str(src) + " " + str(shape_in_tracks) + " z=" + str(zindex))
            self.rg.set_target(shape_in_tracks[0],shape_in_tracks[1],zindex)
        
    def write_obstacle(self, sref, mirr = 1, angle = math.radians(float(0)), xyShift = (0, 0)): 
        """
        Recursive write boundaries as blockages to the routing grid.
        Recurses for each Structure in GDS.
        """
        for boundary in self.layout.structures[sref].boundaries:
            coord_trans = self.translate_coordinates(boundary.coordinates, mirr, angle, xyShift)
            shape_coords = self.min_max_coord(coord_trans)
            shape = self.convert_shape_to_units(shape_coords)

            # only consider the two layers that we are routing on
            if boundary.drawingLayer in [self.vert_layer_number,self.horiz_layer_number]:
                zlayer = 0 if boundary.drawingLayer==self.horiz_layer_number else 1
                [ll,ur]=self.convert_shape_to_tracks(shape)
                self.rg.add_blockage(ll,ur,zlayer)
                

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
            
            self.write_obstacle(cur_sref.sName, sMirr, sAngle, sxyShift)

    def convert_point_to_units(self,p):
        """ 
        Convert a path set of tracks to center line path.
        """
        pt = vector3d(p)
        pt=pt.scale(self.track_widths[0],self.track_widths[1],1)
        return pt

    def convert_shape_to_tracks(self,shape,round_bigger=False):
        """ 
        Convert a rectangular shape into track units.
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


    def convert_track_to_shape(self,track):
        """ 
        Convert a grid point into a rectangle shape that occupies the centered
        track.
        """
        # to scale coordinates to tracks
        # FIXME: should be the metal width no the track width?
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

