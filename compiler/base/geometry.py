# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
This provides a set of useful generic types for the gdsMill interface.
"""
import debug
from vector import vector
import tech
import math
from globals import OPTS
from utils import round_to_grid


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
        debug.error("__str__ must be overridden by all geometry types.", 1)

    def __repr__(self):
        """ override print function output """
        debug.error("__repr__ must be overridden by all geometry types.", 1)

    # def translate_coords(self, coords, mirr, angle, xyShift):
    #     """Calculate coordinates after flip, rotate, and shift"""
    #     coordinate = []
    #     for item in coords:
    #         x = (item[0]*math.cos(angle)-item[1]*mirr*math.sin(angle)+xyShift[0])
    #         y = (item[0]*math.sin(angle)+item[1]*mirr*math.cos(angle)+xyShift[1])
    #         coordinate += [(x, y)]
    #     return coordinate

    def transform_coords(self, coords, offset, mirr, angle):
        """Calculate coordinates after flip, rotate, and shift"""
        coordinate = []
        for item in coords:
            x = item[0] * math.cos(angle) - item[1] * mirr * math.sin(angle) + offset[0]
            y = item[0] * math.sin(angle) + item[1] * mirr * math.cos(angle) + offset[1]
            coordinate += [[x, y]]
        return coordinate

    def normalize(self):
        """ Re-find the LL and UR points after a transform """
        (first, second) = self.boundary
        ll = vector(min(first[0], second[0]),
                    min(first[1], second[1])).snap_to_grid()
        ur = vector(max(first[0], second[0]),
                    max(first[1], second[1])).snap_to_grid()
        self.boundary = [ll, ur]

    def update_boundary(self):
        """ Update the boundary with a new placement. """
        self.compute_boundary(self.offset, self.mirror, self.rotate)

    def compute_boundary(self, offset=vector(0, 0), mirror="", rotate=0):
        """
        Transform with offset, mirror and rotation to get the absolute pin location.
        We must then re-find the ll and ur. The master is the cell instance.
        """
        if OPTS.netlist_only:
            self.boundary = [vector(0, 0), vector(0, 0)]
            return

        (ll, ur) = [vector(0, 0), vector(self.width, self.height)]

        # Mirroring is performed before rotation
        if mirror == "MX":
            ll = ll.scale(1, -1)
            ur = ur.scale(1, -1)
        elif mirror == "MY":
            ll = ll.scale(-1, 1)
            ur = ur.scale(-1, 1)
        elif mirror == "XY":
            ll = ll.scale(-1, -1)
            ur = ur.scale(-1, -1)
        elif mirror == "" or mirror == "R0":
            pass
        else:
            debug.error("Invalid mirroring: {}".format(mirror), -1)

        if rotate == 0:
            pass
        elif rotate == 90:
            ll = ll.rotate_scale(-1, 1)
            ur = ur.rotate_scale(-1, 1)
        elif rotate == 180:
            ll = ll.scale(-1, -1)
            ur = ur.scale(-1, -1)
        elif rotate == 270:
            ll = ll.rotate_scale(1, -1)
            ur = ur.rotate_scale(1, -1)
        else:
            debug.error("Invalid rotation: {}".format(rotate), -1)

        self.boundary = [offset + ll, offset + ur]
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

    def cx(self):
        """ Return the center x """
        return 0.5 * (self.boundary[0].x + self.boundary[1].x)

    def cy(self):
        """ Return the center y """
        return 0.5 * (self.boundary[0].y + self.boundary[1].y)

    def center(self):
        """ Return the center coordinate """
        return vector(self.cx(), self.cy())
    

class instance(geometry):
    """
    An instance of an instance/module with a specified location and
    rotation
    """
    def __init__(self, name, mod, offset=[0, 0], mirror="R0", rotate=0):
        """Initializes an instance to represent a module"""
        super().__init__()
        debug.check(mirror not in ["R90", "R180", "R270"],
                    "Please use rotation and not mirroring during instantiation.")

        self.name = name
        self.mod = mod
        self.gds = mod.gds
        self.rotate = rotate
        self.offset = vector(offset).snap_to_grid()
        self.mirror = mirror
        if OPTS.netlist_only:
            self.width = 0
            self.height = 0
        else:
            if mirror in ["R90", "R270"] or rotate in [90, 270]:
                self.width = round_to_grid(mod.height)
                self.height = round_to_grid(mod.width)
            else:
                self.width = round_to_grid(mod.width)
                self.height = round_to_grid(mod.height)
        self.compute_boundary(offset, mirror, rotate)

        debug.info(4, "creating instance: " + self.name)

    def get_blockages(self, lpp, top=False):
        """ Retrieve blockages of all modules in this instance.
        Apply the transform of the instance placement to give absolute blockages."""
        angle = math.radians(float(self.rotate))
        mirr = 1
        if self.mirror == "R90":
            angle += math.radians(90.0)
        elif self.mirror == "R180":
            angle += math.radians(180.0)
        elif self.mirror == "R270":
            angle += math.radians(270.0)
        elif self.mirror == "MX":
            mirr = -1
        elif self.mirror == "MY":
            mirr = -1
            angle += math.radians(180.0)
        elif self.mirror == "XY":
            mirr = 1
            angle += math.radians(180.0)

        new_blockages = []
        if self.mod.is_library_cell:
            # Writes library cell blockages as shapes instead of a large metal blockage
            blockages = []
            blockages = self.mod.gds.getBlockages(lpp)
            for b in blockages:
                new_blockages.append(self.transform_coords(b, self.offset, mirr, angle))
        else:
            blockages = self.mod.get_blockages(lpp)
            for b in blockages:
                new_blockages.append(self.transform_coords(b, self.offset, mirr, angle))
        return new_blockages

    def gds_write_file(self, new_layout):
        """Recursively writes all the sub-modules in this instance"""
        debug.info(4, "writing instance: " + self.name)
        # make sure to write out my module/structure
        # (it will only be written the first time though)
        self.mod.gds_write_file(self.gds)
        # now write an instance of my module/structure
        new_layout.addInstance(self.gds,
                               self.mod.name,
                               offsetInMicrons=self.offset,
                               mirror=self.mirror,
                               rotate=self.rotate)

    def place(self, offset, mirror="R0", rotate=0):
        """ This updates the placement of an instance. """
        # Update the placement of an already added instance
        self.offset = vector(offset).snap_to_grid()
        self.mirror = mirror
        self.rotate = rotate
        self.update_boundary()
        debug.info(3, "placing instance {}".format(self))

    def get_pin(self, name, index=-1):
        """ Return an absolute pin that is offset and transformed based on
        this instance location. Index will return one of several pins."""

        import copy
        if index == -1:
            pin = copy.deepcopy(self.mod.get_pin(name))
            pin.transform(self.offset, self.mirror, self.rotate)
            return pin
        else:
            pins = copy.deepcopy(self.mod.get_pin(name))
            pins.transform(self.offset, self.mirror, self.rotate)
            return pin[index]

    def get_num_pins(self, name):
        """ Return the number of pins of a given name """
        return len(self.mod.get_pins(name))

    def get_pins(self, name):
        """ Return an absolute pin that is offset and transformed based on
        this instance location. """

        import copy
        pin = copy.deepcopy(self.mod.get_pins(name))

        new_pins = []
        for p in pin:
            p.transform(self.offset, self.mirror, self.rotate)
            new_pins.append(p)
        return new_pins

    def __str__(self):
        """ override print function output """
        return "( inst: " + self.name + " @" + str(self.offset) + " mod=" + self.mod.name + " " + self.mirror + " R=" + str(self.rotate) + ")"

    def __repr__(self):
        """ override print function output """
        return "( inst: " + self.name + " @" + str(self.offset) + " mod=" + self.mod.name + " " + self.mirror + " R=" + str(self.rotate) + ")"

    
class path(geometry):
    """Represents a Path"""

    def __init__(self, lpp, coordinates, path_width):
        """Initializes a path for the specified layer"""
        super().__init__()
        self.name = "path"
        self.layerNumber = lpp[0]
        self.layerPurpose = lpp[1]
        self.coordinates = map(lambda x: [x[0], x[1]], coordinates)
        self.coordinates = vector(self.coordinates).snap_to_grid()
        self.path_width = path_width

        # FIXME figure out the width/height. This type of path is not
        # supported right now. It might not work in gdsMill.
        assert(0)

    def gds_write_file(self, new_layout):
        """Writes the path to GDS"""
        debug.info(4, "writing path (" + str(self.layerNumber) +  "): " + self.coordinates)
        new_layout.addPath(layerNumber=self.layerNumber,
                           purposeNumber=self.layerPurpose,
                           coordinates=self.coordinates,
                           width=self.path_width)

    def get_blockages(self, layer):
        """ Fail since we don't support paths yet. """
        assert(0)

    def __str__(self):
        """ override print function output """
        return "path: layer=" + self.layerNumber + " purpose=" + str(self.layerPurpose) + " w=" + self.width

    def __repr__(self):
        """ override print function output """
        return "( path: layer=" + self.layerNumber + " purpose=" + str(self.layerPurpose) + " w=" + self.width + " coords=" + str(self.coordinates) + " )"


class label(geometry):
    """Represents a text label"""

    def __init__(self, text, lpp, offset, zoom=-1):
        """Initializes a text label for specified layer"""
        super().__init__()
        self.name = "label"
        self.text = text
        self.layerNumber = lpp[0]
        self.layerPurpose = lpp[1]
        self.offset = vector(offset).snap_to_grid()

        if zoom<0:
            self.zoom = tech.GDS["zoom"]
        else:
            self.zoom = zoom

        self.size = 0

        debug.info(4, "creating label " + self.text + " " + str(self.layerNumber) + " " + str(self.offset))

    def gds_write_file(self, new_layout):
        """Writes the text label to GDS"""
        debug.info(4, "writing label (" + str(self.layerNumber) + "): " + self.text)
        new_layout.addText(text=self.text,
                           layerNumber=self.layerNumber,
                           purposeNumber=self.layerPurpose,
                           offsetInMicrons=self.offset,
                           magnification=self.zoom,
                           rotate=None)

    def get_blockages(self, layer):
        """ Returns an empty list since text cannot be blockages. """
        return []

    def __str__(self):
        """ override print function output """
        return "label: " + self.text + " layer=" + str(self.layerNumber) + " purpose=" + str(self.layerPurpose)

    def __repr__(self):
        """ override print function output """
        return "( label: " + self.text + " @" + str(self.offset) + " layer=" + str(self.layerNumber) + " purpose=" + str(self.layerPurpose) + " )"


class rectangle(geometry):
    """Represents a rectangular shape"""

    def __init__(self, lpp, offset, width, height):
        """Initializes a rectangular shape for specified layer"""
        super().__init__()
        self.name = "rect"
        self.layerNumber = lpp[0]
        self.layerPurpose = lpp[1]
        self.offset = vector(offset).snap_to_grid()
        self.size = vector(width, height).snap_to_grid()
        self.width = round_to_grid(self.size.x)
        self.height = round_to_grid(self.size.y)
        self.compute_boundary(offset, "", 0)

        debug.info(4, "creating rectangle (" + str(self.layerNumber) + "): "
                   + str(self.width) + "x" + str(self.height) + " @ " + str(self.offset))

    def get_blockages(self, layer):
        """ Returns a list of one rectangle if it is on this layer"""
        if self.layerNumber == layer:
            return [[self.offset,
                     vector(self.offset.x + self.width,
                            self.offset.y + self.height)]]
        else:
            return []

    def gds_write_file(self, new_layout):
        """Writes the rectangular shape to GDS"""
        debug.info(4, "writing rectangle (" + str(self.layerNumber) + "):"
                   + str(self.width) + "x" + str(self.height) + " @ " + str(self.offset))
        new_layout.addBox(layerNumber=self.layerNumber,
                          purposeNumber=self.layerPurpose,
                          offsetInMicrons=self.offset,
                          width=self.width,
                          height=self.height,
                          center=False)

    def __str__(self):
        """ override print function output """
        return self.__repr__()

    def __repr__(self):
        """ override print function output """
        return "( rect: @" + str(self.offset) + " WxH=" + str(self.width) + "x" + str(self.height) + " layer=" + str(self.layerNumber) + " purpose=" + str(self.layerPurpose) + " )"
