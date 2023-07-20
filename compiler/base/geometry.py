# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
This provides a set of useful generic types for the gdsMill interface.
"""
import math
import copy
import numpy as np
from openram import debug
from openram import tech
from openram import OPTS
from .utils import round_to_grid
from .vector import vector


class geometry:
    """
    A specific path, shape, or text geometry. Base class for shared
    items.
    """
    def __init__(self, lpp=None):
        """ By default, everything has no size. """
        self.width = 0
        self.height = 0
        if lpp:
            self.lpp = lpp
            self.layerNumber = lpp[0]
            self.layerPurpose = lpp[1]

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
    An instance of a module with a specified location, rotation,
    spice pins, and spice nets
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
        # track if the instance's spice pin connections have been made
        self.connected = False

        # deepcopy because this instance needs to
        # change attributes in these spice objects
        self.spice_pins = copy.deepcopy(self.mod.pins)
        self.spice_nets = copy.deepcopy(self.mod.nets)
        for pin in self.spice_pins.values():
            pin.set_inst(self)
        for net in self.spice_nets.values():
            net.set_inst(self)

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
                               self.mod.cell_name,
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

        pin = copy.deepcopy(self.mod.get_pins(name))

        new_pins = []
        for p in pin:
            p.transform(self.offset, self.mirror, self.rotate)
            new_pins.append(p)
        return new_pins

    def connect_spice_pins(self, nets_list):
        """
        add the connection between instance pins and module nets
        to both of their respective objects
        nets_list must be the same length as self.spice_pins
        """
        if len(nets_list) == 0 and len(self.spice_pins) == 0:
            # this is the only valid case to skip the following debug check
            # because this with no pins are often connected arbitrarily
            self.connected = True
            return
        debug.check(not self.connected,
                    "instance {} has already been connected".format(self.name))
        debug.check(len(self.spice_pins) == len(nets_list),
            "must provide list of nets the same length as pin list\
             when connecting an instance")
        for pin in self.spice_pins.values():
            net = nets_list.pop(0)
            pin.set_inst_net(net)
            net.connect_pin(pin)
        self.connected = True

    def get_connections(self):
        conns = []
        for pin in self.spice_pins.values():
            conns.append(pin.inst_net.name)
        return conns

    def calculate_transform(self, node):
        #set up the rotation matrix
        angle = math.radians(float(node.rotate))
        mRotate = np.array([[math.cos(angle), -math.sin(angle), 0.0],
                            [math.sin(angle), math.cos(angle), 0.0],
                            [0.0, 0.0, 1.0]])

        #set up translation matrix
        translateX = float(node.offset[0])
        translateY = float(node.offset[1])
        mTranslate = np.array([[1.0, 0.0, translateX],
                                [0.0, 1.0, translateY],
                                [0.0, 0.0, 1.0]])

        #set up the scale matrix (handles mirror X)
        scaleX = 1.0
        if(node.mirror == 'MX'):
            scaleY = -1.0
        else:
            scaleY = 1.0
        mScale = np.array([[scaleX, 0.0, 0.0],
                            [0.0, scaleY, 0.0],
                            [0.0, 0.0, 1.0]])

        return (mRotate, mScale, mTranslate)

    def apply_transform(self, mtransforms, uVector, vVector, origin):
        origin = np.dot(mtransforms[0], origin)    # rotate
        uVector = np.dot(mtransforms[0], uVector)  # rotate
        vVector = np.dot(mtransforms[0], vVector)  # rotate
        origin = np.dot(mtransforms[1], origin)    # scale
        uVector = np.dot(mtransforms[1], uVector)  # scale
        vVector = np.dot(mtransforms[1], vVector)  # scale
        origin = np.dot(mtransforms[2], origin)

        return(uVector, vVector, origin)

    def apply_path_transform(self, path):
        uVector = np.array([[1.0], [0.0], [0.0]])
        vVector = np.array([[0.0], [1.0], [0.0]])
        origin = np.array([[0.0], [0.0], [1.0]])

        while(path):
            instance = path.pop(-1)
            mtransforms = self.calculate_transform(instance)
            (uVector, vVector, origin) = self.apply_transform(mtransforms, uVector, vVector, origin)

        return (uVector, vVector, origin)

    def reverse_transformation_bitcell(self, cell_name):
        path = [] # path currently follwed in bitcell search
        cell_paths = [] # saved paths to bitcells
        origin_offsets = [] # cell to bank offset
        Q_offsets = [] # Q to cell offet
        Q_bar_offsets = [] # Q_bar to cell offset
        bl_offsets = [] # bl to cell offset
        br_offsets = [] # br to cell offset
        bl_meta = [] # bl offset metadata (row,col,name)
        br_meta  = [] # br offset metadata (row,col,name)

        def walk_subtree(node):
            path.append(node)

            if node.mod.name == cell_name:
                cell_paths.append(copy.copy(path))

                # get the row and col names from the path
                row = int(path[-1].name.split('_')[-2][1:])
                col = int(path[-1].name.split('_')[-1][1:])

                cell_bl_meta = []
                cell_br_meta = []

                normalized_storage_nets = node.mod.get_normalized_storage_nets_offset()
                (normalized_bl_offsets, normalized_br_offsets, bl_names, br_names) = node.mod.get_normalized_bitline_offset()

                for offset in range(len(normalized_bl_offsets)):
                    for port in range(len(bl_names)):
                        cell_bl_meta.append([bl_names[offset], row, col, port])

                for offset in range(len(normalized_br_offsets)):
                    for port in range(len(br_names)):
                        cell_br_meta.append([br_names[offset], row, col, port])

                if normalized_storage_nets == []:
                    debug.error("normalized storage nets should not be empty! Check if the GDS labels Q and Q_bar are correctly set on M1 of the cell",1)
                Q_x = normalized_storage_nets[0][0]
                Q_y = normalized_storage_nets[0][1]

                Q_bar_x = normalized_storage_nets[1][0]
                Q_bar_y = normalized_storage_nets[1][1]

                if node.mirror == 'MX':
                    Q_y = -1 * Q_y
                    Q_bar_y = -1 * Q_bar_y

                    for pair in range(len(normalized_bl_offsets)):
                        normalized_bl_offsets[pair] = (normalized_bl_offsets[pair][0],
                                                       -1 * normalized_bl_offsets[pair][1])

                    for pair in range(len(normalized_br_offsets)):
                        normalized_br_offsets[pair] = (normalized_br_offsets[pair][0],
                                                       -1 * normalized_br_offsets[pair][1])

                Q_offsets.append([Q_x, Q_y])
                Q_bar_offsets.append([Q_bar_x, Q_bar_y])

                bl_offsets.append(normalized_bl_offsets)
                br_offsets.append(normalized_br_offsets)

                bl_meta.append(cell_bl_meta)
                br_meta.append(cell_br_meta)

            elif node.mod.insts is not []:
                for instance in node.mod.insts:
                    walk_subtree(instance)
            path.pop(-1)

        walk_subtree(self)
        for path in cell_paths:
            vector_spaces = self.apply_path_transform(path)
            origin = vector_spaces[2]
            origin_offsets.append([origin[0], origin[1]])

        return(origin_offsets, Q_offsets, Q_bar_offsets, bl_offsets, br_offsets, bl_meta, br_meta)

    def __str__(self):
        """ override print function output """
        return "( inst: " + self.name + " @" + str(self.offset) + " mod=" + self.mod.cell_name + " " + self.mirror + " R=" + str(self.rotate) + ")"

    def __repr__(self):
        """ override print function output """
        return "( inst: " + self.name + " @" + str(self.offset) + " mod=" + self.mod.cell_name + " " + self.mirror + " R=" + str(self.rotate) + ")"


class path(geometry):
    """Represents a Path"""

    def __init__(self, lpp, coordinates, path_width):
        """Initializes a path for the specified layer"""
        super().__init__(lpp)
        self.name = "path"
        self.coordinates = map(lambda x: [x[0], x[1]], coordinates)
        self.coordinates = vector(self.coordinates).snap_to_grid()
        self.path_width = path_width

        # FIXME figure out the width/height. This type of path is not
        # supported right now. It might not work in gdsMill.
        assert(0)

    def gds_write_file(self, new_layout):
        """Writes the path to GDS"""
        debug.info(4, "writing path (" + str(self.layerNumber) + "): " + self.coordinates)
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

    def __init__(self, text, lpp, offset, zoom=None):
        """Initializes a text label for specified layer"""
        super().__init__(lpp)
        self.name = "label"
        self.text = text
        self.offset = vector(offset).snap_to_grid()

        if not zoom:
            try:
                self.zoom = tech.GDS["zoom"]
            except:
                self.zoom = None
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
        super().__init__(lpp)
        self.name = "rect"
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
