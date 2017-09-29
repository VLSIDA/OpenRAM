"""
This provides a set of useful generic types for the gdsMill interface. 
"""
import debug
from vector import vector
from tech import GDS

class geometry:
    """
    A specific path, shape, or text geometry. Base class for shared
    items.
    """
    def __init__(self):
        """ By default, everything has no size. """
        self.width = 0
        self.height = 0

    def __str__(self):
        """ override print function output """
        debug.error("__str__ must be overridden by all geometry types.",1)

    def __repr__(self):
        """ override print function output """
        debug.error("__repr__ must be overridden by all geometry types.",1)


class instance(geometry):
    """
    An instance of an instance/module with a specified location and
    rotation
    """
    def __init__(self, name, mod, offset, mirror, rotate):
        """Initializes an instance to represent a module"""
        geometry.__init__(self)
        debug.check(mirror not in ["R90","R180","R270"], "Please use rotation and not mirroring during instantiation.")
        
        self.name = name
        self.mod = mod
        self.gds = mod.gds
        self.rotate = rotate
        self.offset = vector(offset).snap_to_grid()
        self.mirror = mirror
        
        self.compute_boundary(offset,mirror,rotate)
        
        debug.info(4, "creating instance: " + self.name)

    def gds_write_file(self, newLayout):
        """Recursively writes all the sub-modules in this instance"""
        debug.info(4, "writing instance: " + self.name)
        # make sure to write out my module/structure 
        # (it will only be written the first time though)
        self.mod.gds_write_file(self.gds)
        # now write an instance of my module/structure
        newLayout.addInstance(self.gds,
                              offsetInMicrons=self.offset,
                              mirror=self.mirror,
                              rotate=self.rotate)

    def normalize(self):
        """ Re-find the LL and UR points after a transform """
        (first,second)=self.boundary
        ll = vector(min(first[0],second[0]),min(first[1],second[1]))
        ur = vector(max(first[0],second[0]),max(first[1],second[1]))
        self.boundary=[ll,ur]
        
    def compute_boundary(self,offset=vector(0,0),mirror="",rotate=0):
        """ Transform with offset, mirror and rotation to get the absolute pin location. 
        We must then re-find the ll and ur. The master is the cell instance. """
        (ll,ur) = [vector(0,0),vector(self.mod.width,self.mod.height)]
        if mirror=="MX":
            ll=ll.scale(1,-1)
            ur=ur.scale(1,-1)
        elif mirror=="MY":
            ll=ll.scale(-1,1)
            ur=ur.scale(-1,1)
        elif mirror=="XY":
            ll=ll.scale(-1,-1)
            ur=ur.scale(-1,-1)
            
        if rotate==90:
            ll=ll.rotate_scale(-1,1)
            ur=ur.rotate_scale(-1,1)
        elif rotate==180:
            ll=ll.scale(-1,-1)
            ur=ur.scale(-1,-1)
        elif rotate==270:
            ll=ll.rotate_scale(1,-1)
            ur=ur.rotate_scale(1,-1)

        self.boundary=[offset+ll,offset+ur]
        self.normalize()
        
    def ll(self):
        """ Return the lower left corner """
        return self.boundary[0]
    
    def ur(self):
        """ Return the upper right corner """
        return self.boundary[1]
    
    def lr(self):
        """ Return the lower right corner """
        return vector(self.boundary[1].x, self.boundary[0].y)
    
    def ul(self):
        """ Return the upper left corner """
        return vector(self.boundary[0].x, self.boundary[1].y)


    def uy(self):
        """ Return the upper edge """
        return self.boundary[1].y

    def by(self):
        """ Return the bottom edge """
        return self.boundary[0].y

    def lx(self):
        """ Return the left edge """
        return self.boundary[0].x

    def rx(self):
        """ Return the right edge """
        return self.boundary[1].x
    
    def get_pin(self,name):
        """ Return an absolute pin that is offset and transformed based on
        this instance location. """
        
        import copy
        pin = copy.deepcopy(self.mod.get_pin(name))
        pin.transform(self.offset,self.mirror,self.rotate)
        return pin

    def get_pins(self,name):
        """ Return an absolute pin that is offset and transformed based on
        this instance location. """
        
        import copy
        pin = copy.deepcopy(self.mod.get_pins(name))
        
        new_pins = []
        for p in pin:
            p.transform(self.offset,self.mirror,self.rotate)                
            new_pins.append(p)
        return new_pins
        
    def __str__(self):
        """ override print function output """
        return "inst: " + self.name + " mod=" + self.mod.name

    def __repr__(self):
        """ override print function output """
        return "( inst: " + self.name + " @" + str(self.offset) + " mod=" + self.mod.name + " " + self.mirror + " R=" + str(self.rotate) + ")"

class path(geometry):
    """Represents a Path"""

    def __init__(self, layerNumber, coordinates, path_width):
        """Initializes a path for the specified layer"""
        geometry.__init__(self)
        self.name = "path"
        self.layerNumber = layerNumber
        self.coordinates = map(lambda x: [x[0], x[1]], coordinates)
        self.coordinates = vector(self.coordinates).snap_to_grid()
        self.path_width = path_width

        # FIXME figure out the width/height. This type of path is not
        # supported right now. It might not work in gdsMill.
        assert(0)

    def gds_write_file(self, newLayout):
        """Writes the path to GDS"""
        debug.info(4, "writing path (" + str(self.layerNumber) +  "): " + self.coordinates)
        newLayout.addPath(layerNumber=self.layerNumber,
                          purposeNumber=0,
                          coordinates=self.coordinates,
                          width=self.path_width)

    def __str__(self):
        """ override print function output """
        return "path: layer=" + self.layerNumber + " w=" + self.width

    def __repr__(self):
        """ override print function output """
        return "( path: layer=" + self.layerNumber + " w=" + self.width + " coords=" + str(self.coordinates) + " )"


class label(geometry):
    """Represents a text label"""

    def __init__(self, text, layerNumber, offset, zoom=-1):
        """Initializes a text label for specified layer"""
        geometry.__init__(self)
        self.name = "label"
        self.text = text
        self.layerNumber = layerNumber
        self.offset = vector(offset).snap_to_grid()
        if zoom<0:
            self.zoom = GDS["zoom"]
        else:
            self.zoom = zoom


        self.size = 0

        debug.info(4,"creating label " + self.text + " " + str(self.layerNumber) + " " + str(self.offset))

    def gds_write_file(self, newLayout):
        """Writes the text label to GDS"""
        debug.info(4, "writing label (" + str(self.layerNumber) + "): " + self.text)
        newLayout.addText(text=self.text,
                          layerNumber=self.layerNumber,
                          purposeNumber=0,
                          offsetInMicrons=self.offset,
                          magnification=self.zoom,
                          rotate=None)

    def __str__(self):
        """ override print function output """
        return "label: " + self.text + " layer=" + str(self.layerNumber)

    def __repr__(self):
        """ override print function output """
        return "( label: " + self.text + " @" + str(self.offset) + " layer=" + self.layerNumber + " )"

class rectangle(geometry):
    """Represents a rectangular shape"""

    def __init__(self, layerNumber, offset, width, height):
        """Initializes a rectangular shape for specified layer"""
        geometry.__init__(self)
        self.name = "rect"
        self.layerNumber = layerNumber
        self.offset = vector(offset).snap_to_grid()
        self.size = vector(width, height).snap_to_grid()
        self.width = self.size.x
        self.height = self.size.y

        debug.info(4, "creating rectangle (" + str(self.layerNumber) + "): " 
                   + str(self.width) + "x" + str(self.height) + " @ " + str(self.offset))


    def gds_write_file(self, newLayout):
        """Writes the rectangular shape to GDS"""
        debug.info(4, "writing rectangle (" + str(self.layerNumber) + "):" 
                   + str(self.width) + "x" + str(self.height) + " @ " + str(self.offset))
        newLayout.addBox(layerNumber=self.layerNumber,
                         purposeNumber=0,
                         offsetInMicrons=self.offset,
                         width=self.width,
                         height=self.height,
                         center=False)

    def __str__(self):
        """ override print function output """
        return "rect: @" + str(self.offset) + " " + str(self.width) + "x" + str(self.height) + " layer=" +str(self.layerNumber)

    def __repr__(self):
        """ override print function output """
        return "( rect: @" + str(self.offset) + " " + str(self.width) + "x" + str(self.height) + " layer=" + str(self.layerNumber) + " )"
