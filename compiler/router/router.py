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
        self.layout = gdsMill.VlsiLayout()
        self.reader = gdsMill.Gds2reader(self.layout)
        self.reader.loadFromFile(gds_name)
        self.top_name = self.layout.rootStructureName
        self.unit = float(self.layout.info['units'][0])
        print "Units:",self.unit

        self.pin_names = []
        self.pin_shapes = {}
        self.pin_layers = {}
        
        self.boundary = self.layout.measureBoundary(self.top_name)
        self.ll = vector(self.boundary[0])
        self.ur = vector(self.boundary[1])
        self.size = self.ur - self.ll
        self.width = self.size.x
        self.height = self.size.y
        
        print "Boundary: ",self.boundary
        print "Size: ", self.width,self.height
        
        # to scale coordinates by units
        self.unit_factor = [self.unit] * 2
        
        # We will offset so ll is at (0,0)
        self.offset = self.ll 
        print "Offset: ",self.offset
        

    def set_top(self,top_name):
        """ If we want to route something besides the top-level cell."""
        self.top_name = top_name


    def set_layers(self, layers):
        """ Allows us to change the layers that we are routing on. """
        self.layers = layers
        (horiz_layer, via_layer, vert_layer) = self.layers
        if (via_layer != None):
            self.via_layer_name = via_layer
        else:
            self.via_layer_name = None

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
        print "Track width:",self.track_width

        # to scale coordinates to tracks
        self.track_factor = [1/self.track_width] * 2



    def create_routing_grid(self):
        """ Create a routing grid that spans given area. Wires cannot exist outside region. """

        self.width_in_tracks = int(math.ceil(self.width/self.track_width))
        self.height_in_tracks = int(math.ceil(self.height/self.track_width))

        print "Size (in tracks): ", self.width_in_tracks, self.height_in_tracks
        
        self.rg = grid.grid(self.width_in_tracks,self.height_in_tracks)
        

    def find_pin(self,pin):
        """ Finds the offsets to the gds pins """
        (pin_name,pin_layer,pin_shape) = self.layout.readPin(str(pin))
        # repack the shape as a pair of vectors rather than four values
        new_shape = self.convert_to_tracks([vector(pin_shape[0],pin_shape[1]),vector(pin_shape[2],pin_shape[3])])
        self.pin_names.append(pin_name)
        self.pin_shapes[str(pin)] = new_shape
        self.pin_layers[str(pin)] = pin_layer
        return new_shape

    def find_blockages(self):
        if len(self.pin_names)!=2:
            debug.error("Must set pins before creating blockages.",-1)
            
        for layer in self.layers:
            self.write_obstacle(self.top_name)

            
    
    def add_route(self,start, end, layerstack):
        """ Add a wire route from the start to the end point"""
        pass

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

    def min_max_coord(self, coordTrans):
        """Find the lowest and highest conner of a Rectangle"""
        coordinate = []
        minx = min(coordTrans[0][0], coordTrans[1][0], coordTrans[2][0], coordTrans[3][0])
        maxx = max(coordTrans[0][0], coordTrans[1][0], coordTrans[2][0], coordTrans[3][0])
        miny = min(coordTrans[0][1], coordTrans[1][1], coordTrans[2][1], coordTrans[3][1])
        maxy = max(coordTrans[0][1], coordTrans[1][1], coordTrans[2][1], coordTrans[3][1])
        coordinate += [vector(minx, miny)]
        coordinate += [vector(maxx, maxy)]
        return coordinate

    def set_source(self,name):
        shape = self.find_pin(name)
        zindex = 0 if self.pin_layers[name]==self.horiz_layer_number else 1
        debug.info(0,"Set source: " + str(name) + " " + str(shape) + " z=" + str(zindex))
        self.rg.set_source(shape[0],shape[1],zindex)

    def set_target(self,name):
        shape = self.find_pin(name)
        zindex = 0 if self.pin_layers[name]==self.horiz_layer_number else 1        
        debug.info(0,"Set target: " + str(name) + " " + str(shape) + " z=" + str(zindex))
        self.rg.set_target(shape[0],shape[1],zindex)
        
    def write_obstacle(self, sref, mirr = 1, angle = math.radians(float(0)), xyShift = (0, 0)): 
        """Recursive write boundaries on each Structure in GDS file to LEF"""

        for boundary in self.layout.structures[sref].boundaries:
            coordTrans = self.translate_coordinates(boundary.coordinates, mirr, angle, xyShift)
            shape = self.min_max_coord(coordTrans)

            if boundary.drawingLayer in [self.vert_layer_number,self.horiz_layer_number]:
                ll_microns=shape[0].scale(self.unit_factor)
                ur_microns=shape[1].scale(self.unit_factor)
                
                shape_tracks=self.convert_to_tracks([ll_microns,ur_microns])

                if shape_tracks not in self.pin_shapes.values():
                    # inflate the ll and ur by 1 track in each direction
                    [ll,ur]=shape_tracks
                    ll = vector(0,0).max(ll + vector(-1,-1))
                    ur = vector(self.width_in_tracks-1,self.height_in_tracks-1).min(ur + vector(1,1))
                    zlayer = 0 if boundary.drawingLayer==self.horiz_layer_number else 1
                    debug.info(1,"Blockage: "+str([ll,ur])+" z="+str(zlayer))
                    self.rg.add_blockage(ll,ur,zlayer)
                else:
                    debug.info(2,"Skip: "+str(shape_tracks))
                


        # recurse given the mirror, angle, etc.
        for cur_sref in self.layout.structures[sref].srefs:
            sMirr = 1
            if sref.transFlags[0] == True:
                sMirr = -1
            sAngle = math.radians(float(0))
            if sref.rotateAngle:
                sAngle = math.radians(float(cur_sref.rotateAngle))
            sAngle += angle
            x = cur_sref.coordinates[0]
            y = cur_sref.coordinates[1]
            newX = (x)*math.cos(angle) - mirr*(y)*math.sin(angle) + xyShift[0] 
            newY = (x)*math.sin(angle) + mirr*(y)*math.cos(angle) + xyShift[1] 
            sxyShift = (newX, newY)
            
            self.write_obstacle(cur_sref.sName, layer,sMirr, sAngle, sxyShift)

    def inflate_obstacle(self,shape):
        # TODO: inflate by the layer design rules
        return shape
        
    def convert_to_tracks(self,shape):
        """ 
        Convert a rectangular shape into track units.
        """
        [ll,ur] = shape

        # fix offset
        ll = snap_to_grid(ll-self.offset)
        ur = snap_to_grid(ur-self.offset)

        # always round down, because we will add a track
        # to inflate each object later
        ll = ll.scale(self.track_factor).ceil()
        ur = ur.scale(self.track_factor).floor()

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
            
