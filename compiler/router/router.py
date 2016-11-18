import gdsMill
import tech
from contact import contact
import math
import debug
from vector import vector
import grid

 


class router:
    """A router class to read an obstruction map from a gds and plan a
    route on a given layer. This is limited to two layer routes.

    """
    def __init__(self, gds_name):
        """Use the gds file for the blockages with the top module topName and
        layers for the layers to route on

        """
        self.gds_name = gds_name
        self.layout = gdsMill.VlsiLayout(units=tech.GDS["unit"])
        self.reader = gdsMill.Gds2reader(self.layout)
        self.reader.loadFromFile(gds_name)
        self.top_name = self.layout.rootStructureName

        self.pin_names = []
        self.pin_shapes = {}
        # Used to track which shapes should not become blockages
        self.all_pin_shapes = []
        self.pin_layers = {}
        
        self.boundary = self.layout.measureBoundary(self.top_name)
        self.ll = vector(self.boundary[0])
        self.ur = vector(self.boundary[1])
        self.size = self.ur - self.ll


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

        # contacted track spacing
        via_connect = contact(self.layers, (1, 1))
        self.horiz_track_width = tech.drc[str(self.horiz_layer_name)+"_to_"+str(self.horiz_layer_name)] + via_connect.width
        self.vert_track_width = tech.drc[str(self.vert_layer_name)+"_to_"+str(self.vert_layer_name)] + via_connect.width

        # This is so we can use a single resolution grid for both layers
        self.track_width = max(self.horiz_track_width,self.vert_track_width)
        debug.info(1,"Track width:"+str(self.track_width))



    def create_routing_grid(self):
        """ Create a routing grid that spans given area. Wires cannot exist outside region. """
        # We will add a halo around the boundary
        # of this many tracks
        track_halo = 2
        # We will offset so ll is at (-track_halo*track_width,-track_halo*track_width)
        track_width_offset = vector([track_halo*self.track_width]*2)
        self.offset = self.ll - track_width_offset
        debug.info(1,"Offset: "+str(self.offset))
        width = self.size.x
        height = self.size.y
        debug.info(1,"Size: {0} x {1}".format(width,height))

        # pad the tracks on each side by the halo as well
        self.width_in_tracks = int(math.ceil(width/self.track_width)) + 2*track_halo
        self.height_in_tracks = int(math.ceil(height/self.track_width)) + 2*track_halo

        debug.info(1,"Size (in tracks): {0} x {1}".format(self.width_in_tracks, self.height_in_tracks))
        
        self.rg = grid.grid(self.width_in_tracks,self.height_in_tracks)
        

    def find_pin(self,pin):
        """ Finds the pin shapes and converts to tracks """
        (pin_name,pin_layer,pin_shapes) = self.layout.readAllPin(str(pin))

        self.pin_shapes[str(pin)]=[]
        self.pin_names.append(pin_name)
        
        for pin_shape in pin_shapes:
            debug.info(3,"Find pin {0} layer {1} shape {2}".format(pin_name,str(pin_layer),str(pin_shape)))
            # repack the shape as a pair of vectors rather than four values
            shape=[vector(pin_shape[0],pin_shape[1]),vector(pin_shape[2],pin_shape[3])]
            new_shape = self.convert_shape_to_tracks(shape,round_bigger=False)
            self.pin_shapes[str(pin)].append(new_shape)
            self.all_pin_shapes.append(new_shape)            
            self.pin_layers[str(pin)] = pin_layer
            
        return self.pin_shapes[str(pin)]

    def find_blockages(self):
        if len(self.pin_names)!=2:
            debug.error("Must set pins before creating blockages.",-1)
            
        for layer in self.layers:
            self.write_obstacle(self.top_name)

    def clear_pins(self):
        self.source = []
        self.dest = []

    def route(self, layers, src, dest):
        """ 
        Route a single source-destination net and return
        the simplified rectilinear path.
        """
        self.clear_pins()
        self.set_layers(layers)
        self.create_routing_grid()
        self.set_source(src)
        self.set_target(dest)
        
        self.find_blockages()
        # returns the path in tracks
        path = self.rg.route()
        debug.info(1,"Found path. ")
        debug.info(2,str(path))
        self.set_path(path)
        # First, simplify the path.
        contracted_path = self.contract_path(path)
        debug.info(1,str(contracted_path))                
        # convert the path back to absolute units from tracks
        abs_path = self.convert_path_to_units(contracted_path)
        debug.info(1,str(abs_path))        
        return abs_path
    
    def create_steiner_routes(self,pins):
        """Find a set of steiner points and then return the list of
        point-to-point routes."""
        pass

    def find_steiner_points(self,pins):
        """ Find the set of steiner points and return them."""
        pass

    def translate_coordinates(self, coord, mirr, angle, xyShift):
        """Calculate coordinates after flip, rotate, and shift"""
        coordinate = []
        for item in coord:
            x = (item[0]*math.cos(angle)-item[1]*mirr*math.sin(angle)+xyShift[0])
            y = (item[0]*math.sin(angle)+item[1]*mirr*math.cos(angle)+xyShift[1])
            coordinate += [(x, y)]
        return coordinate

    def convert_shape_to_units(self, shape):
        """ Scale a shape (two vector list) to user units """
        unit_factor = [tech.GDS["unit"][0]] * 2
        ll=shape[0].scale(unit_factor)
        ur=shape[1].scale(unit_factor)
        return [ll,ur]

        
    def min_max_coord(self, coord):
        """Find the lowest and highest corner of a Rectangle"""
        coordinate = []
        minx = min(coord[0][0], coord[1][0], coord[2][0], coord[3][0])
        maxx = max(coord[0][0], coord[1][0], coord[2][0], coord[3][0])
        miny = min(coord[0][1], coord[1][1], coord[2][1], coord[3][1])
        maxy = max(coord[0][1], coord[1][1], coord[2][1], coord[3][1])
        coordinate += [vector(minx, miny)]
        coordinate += [vector(maxx, maxy)]
        return coordinate

    def get_inertia(self,p0,p1):
        # direction (index) of movement
        if p0.x==p1.x:
            inertia = 1
        elif p0.y==p1.y:
            inertia = 0
        else:
            inertia = 2
        return inertia
        
    def contract_path(self,path):
        """ 
        Remove intermediate points in a rectilinear path.
        """
        newpath = [path[0]]
        for i in range(len(path)-1):
            if i==0:
                continue
            prev_inertia=self.get_inertia(path[i-1],path[i])
            next_inertia=self.get_inertia(path[i],path[i+1])

            if prev_inertia!=next_inertia:
                newpath.append(path[i])
            else:
                continue

        newpath.append(path[-1])

        return newpath
    
    def set_path(self,path):
        debug.info(3,"Set path: " + str(path))        
        self.rg.set_path(path)

    def set_source(self,name):
        shapes = self.find_pin(name)
        zindex = 0 if self.pin_layers[name]==self.horiz_layer_number else 1
        for shape in shapes:
            debug.info(1,"Set source: " + str(name) + " " + str(shape) + " z=" + str(zindex))
            self.rg.set_source(shape[0],shape[1],zindex)


    def set_target(self,name):
        shapes = self.find_pin(name)
        zindex = 0 if self.pin_layers[name]==self.horiz_layer_number else 1
        for shape in shapes:
            debug.info(1,"Set target: " + str(name) + " " + str(shape) + " z=" + str(zindex))
            self.rg.set_target(shape[0],shape[1],zindex)
        
    def write_obstacle(self, sref, mirr = 1, angle = math.radians(float(0)), xyShift = (0, 0)): 
        """Recursive write boundaries on each Structure in GDS file to LEF"""

        for boundary in self.layout.structures[sref].boundaries:
            coord_trans = self.translate_coordinates(boundary.coordinates, mirr, angle, xyShift)
            shape_coords = self.min_max_coord(coord_trans)
            shape = self.convert_shape_to_units(shape_coords)

            if boundary.drawingLayer in [self.vert_layer_number,self.horiz_layer_number]:
                # We round the pins down, so we must do this to skip them
                pin_shape_tracks=self.convert_shape_to_tracks(shape,round_bigger=False)

                # don't add a blockage if this shape was a pin shape
                if pin_shape_tracks not in self.all_pin_shapes:
                    # inflate the ll and ur by 1 track in each direction
                    [ll,ur]=self.convert_shape_to_tracks(shape)
                    zlayer = 0 if boundary.drawingLayer==self.horiz_layer_number else 1
                    self.rg.add_blockage(ll,ur,zlayer)
                else:
                    debug.info(2,"Skip: "+str(pin_shape_tracks))
                

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

    def convert_path_to_units(self,path):
        """ 
        Convert a path set of tracks to center line path.
        """
        newpath = []
        track_factor = [self.track_width] * 2        
        for p in path:
            # we can ignore the layers here
            # add_wire will filter out duplicates
            pt = vector(p[0],p[1])
            pt=pt.scale(track_factor)
            pt=snap_to_grid(pt+self.offset)
            newpath.append(pt)
        return newpath

    def convert_shape_to_tracks(self,shape,round_bigger=True):
        """ 
        Convert a rectangular shape into track units.
        """
        [ll,ur] = shape

        # offset lowest corner object to to (-track halo,-track halo)
        ll = snap_to_grid(ll-self.offset)
        ur = snap_to_grid(ur-self.offset)

        # to scale coordinates to tracks
        track_factor = [1/self.track_width] * 2


        # Always round blockage shapes up.
        if round_bigger:
            ll = ll.scale(track_factor).floor()
            ur = ur.scale(track_factor).ceil()
        # Always round pin shapes down
        else:
            ll = ll.scale(track_factor).ceil()
            ur = ur.scale(track_factor).floor()
            # if they were within one grid, we must
            # not let it round away the pin
            if ur.x<ll.x:
                ur.x=ll.x
            if ur.y<ll.y:
                ur.y=ll.y

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
            
