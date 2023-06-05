# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import math
from openram import debug
from openram.tech import GDS, drc
from openram.tech import layer, layer_indices
from .vector import vector


class pin_layout:
    """
    A class to represent a rectangular design pin. It is limited to a
    single shape.
    """

    def __init__(self, name, rect, layer_name_pp):
        self.name = name
        # repack the rect as a vector, just in case
        if type(rect[0]) == vector:
            self._rect = rect
        else:
            self._rect = [vector(rect[0]), vector(rect[1])]
        # snap the rect to the grid
        self._rect = [x.snap_to_grid() for x in self.rect]

        debug.check(self.width() > 0, "Zero width pin.")
        debug.check(self.height() > 0, "Zero height pin.")

        # These are the valid pin layers
        valid_layers = {x: layer[x] for x in layer_indices.keys()}

        # if it's a string, use the name
        if type(layer_name_pp) == str:
            self._layer = layer_name_pp
        # else it is required to be a lpp
        else:
            for (layer_name, lpp) in valid_layers.items():
                if not lpp:
                    continue
                if self.same_lpp(layer_name_pp, lpp):
                    self._layer = layer_name
                    break

            else:
                try:
                    from openram.tech import layer_override
                    from openram.tech import layer_override_name
                    if layer_override[name]:
                       self.lpp = layer_override[name]
                       self.layer = "pwellp"
                       self._recompute_hash()
                       return
                except:
                    debug.error("Layer {} is not a valid routing layer in the tech file.".format(layer_name_pp), -1)

        self.lpp = layer[self.layer]
        self._recompute_hash()

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, l):
        self._layer = l
        self._recompute_hash()

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, r):
        self._rect = r
        self._recompute_hash()

    def _recompute_hash(self):
        """ Recompute the hash for our hash cache """
        self._hash = hash(repr(self))

    def __str__(self):
        """ override print function output """
        return "({} layer={} ll={} ur={})".format(self.name,
                                                  self.layer,
                                                  self.rect[0],
                                                  self.rect[1])

    def __repr__(self):
        """
        override repr function output (don't include
        name since pin shapes could have same shape but diff name e.g. blockage vs A)
        """
        return "(layer={} ll={} ur={})".format(self.layer,
                                               self.rect[0],
                                               self.rect[1])

    def __hash__(self):
        """
        Implement the hash function for sets etc. We only return a cached
        value, that is updated when either 'rect' or 'layer' are changed. This
        is a major speedup, if pin_layout is used as a key for dicts.
        """
        return self._hash

    def __lt__(self, other):
        """ Provide a function for ordering items by the ll point """
        (ll, ur) = self.rect
        (oll, our) = other.rect

        if ll.x < oll.x and ll.y < oll.y:
            return True

        return False

    def __eq__(self, other):
        """ Check if these are the same pins for duplicate checks """
        if isinstance(other, self.__class__):
            return (self.lpp == other.lpp and self.rect == other.rect)
        else:
            return False

    def bbox(self, pin_list):
        """
        Given a list of layout pins, create a bounding box layout.
        """
        (ll, ur) = self.rect
        min_x = ll.x
        max_x = ur.x
        min_y = ll.y
        max_y = ur.y

        for pin in pin_list:
            min_x = min(min_x, pin.ll().x)
            max_x = max(max_x, pin.ur().x)
            min_y = min(min_y, pin.ll().y)
            max_y = max(max_y, pin.ur().y)

        self.rect = [vector(min_x, min_y), vector(max_x, max_y)]

    def fix_minarea(self):
        """
        Try to fix minimum area rule.
        """
        min_area = drc("{}_minarea".format(self.layer))
        pass

    def inflate(self, spacing=None, multiple=0.5):
        """
        Inflate the rectangle by the spacing (or other rule)
        and return the new rectangle.
        """
        if not spacing:
            spacing = multiple*drc("{0}_to_{0}".format(self.layer))

        (ll, ur) = self.rect
        spacing = vector(spacing, spacing)
        newll = ll - spacing
        newur = ur + spacing

        return (newll, newur)

    def inflated_pin(self, spacing=None, multiple=0.5):
        """
        Inflate the rectangle by the spacing (or other rule)
        and return the new rectangle.
        """
        inflated_area = self.inflate(spacing, multiple)
        return pin_layout(self.name, inflated_area, self.layer)

    def intersection(self, other):
        """ Check if a shape overlaps with a rectangle  """

        if not self.overlaps(other):
            return None

        (ll, ur) = self.rect
        (oll, our) = other.rect

        min_x = max(ll.x, oll.x)
        max_x = min(ur.x, our.x)
        min_y = max(ll.y, oll.y)
        max_y = min(ur.y, our.y)

        if max_x - min_x == 0 or max_y - min_y == 0:
            return None

        return pin_layout("", [vector(min_x, min_y), vector(max_x, max_y)], self.layer)

    def xoverlaps(self, other):
        """ Check if shape has x overlap """
        (ll, ur) = self.rect
        (oll, our) = other.rect
        x_overlaps = False
        # check if self is within other x range
        if (ll.x >= oll.x and ll.x <= our.x) or (ur.x >= oll.x and ur.x <= our.x):
            x_overlaps = True
        # check if other is within self x range
        if (oll.x >= ll.x and oll.x <= ur.x) or (our.x >= ll.x and our.x <= ur.x):
            x_overlaps = True

        return x_overlaps

    def yoverlaps(self, other):
        """ Check if shape has x overlap """
        (ll, ur) = self.rect
        (oll, our) = other.rect
        y_overlaps = False

        # check if self is within other y range
        if (ll.y >= oll.y and ll.y <= our.y) or (ur.y >= oll.y and ur.y <= our.y):
            y_overlaps = True
        # check if other is within self y range
        if (oll.y >= ll.y and oll.y <= ur.y) or (our.y >= ll.y and our.y <= ur.y):
            y_overlaps = True

        return y_overlaps

    def xcontains(self, other):
        """ Check if shape contains the x overlap """
        (ll, ur) = self.rect
        (oll, our) = other.rect

        return (oll.x >= ll.x and our.x <= ur.x)

    def ycontains(self, other):
        """ Check if shape contains the y overlap """
        (ll, ur) = self.rect
        (oll, our) = other.rect

        return (oll.y >= ll.y and our.y <= ur.y)

    def contains(self, other):
        """ Check if a shape contains another rectangle  """
        # If it is the same shape entirely, it is contained!
        if self == other:
            return True

        # Can only overlap on the same layer
        if not self.same_lpp(self.lpp, other.lpp):
            return False

        if not self.xcontains(other):
            return False

        if not self.ycontains(other):
            return False

        return True

    def contained_by_any(self, shape_list):
        """ Checks if shape is contained by any in the list """
        for shape in shape_list:
            if shape.contains(self):
                return True
        return False

    def overlaps(self, other):
        """ Check if a shape overlaps with a rectangle  """
        # Can only overlap on the same layer
        if not self.same_lpp(self.lpp, other.lpp):
            return False

        x_overlaps = self.xoverlaps(other)
        y_overlaps = self.yoverlaps(other)

        return x_overlaps and y_overlaps

    def area(self):
        """ Return the area. """
        return self.height()*self.width()

    def height(self):
        """ Return height. Abs is for pre-normalized value."""
        return abs(self.rect[1].y-self.rect[0].y)

    def width(self):
        """ Return width. Abs is for pre-normalized value."""
        return abs(self.rect[1].x-self.rect[0].x)

    def normalize(self):
        """ Re-find the LL and UR points after a transform """
        (first, second) = self.rect
        ll = vector(min(first[0], second[0]), min(first[1], second[1]))
        ur = vector(max(first[0], second[0]), max(first[1], second[1]))
        self.rect=[ll, ur]

    def transform(self, offset, mirror, rotate):
        """
        Transform with offset, mirror and rotation
        to get the absolute pin location.
        We must then re-find the ll and ur.
        The master is the cell instance.
        """
        (ll, ur) = self.rect
        if mirror == "MX":
            ll = ll.scale(1, -1)
            ur = ur.scale(1, -1)
        elif mirror == "MY":
            ll = ll.scale(-1, 1)
            ur = ur.scale(-1, 1)
        elif mirror == "XY":
            ll = ll.scale(-1, -1)
            ur = ur.scale(-1, -1)

        if rotate == 90:
            ll = ll.rotate_scale(-1, 1)
            ur = ur.rotate_scale(-1, 1)
        elif rotate == 180:
            ll = ll.scale(-1, -1)
            ur = ur.scale(-1, -1)
        elif rotate == 270:
            ll = ll.rotate_scale(1, -1)
            ur = ur.rotate_scale(1, -1)

        self.rect = [offset + ll, offset + ur]
        self.normalize()

    def center(self):
        return vector(0.5*(self.rect[0].x+self.rect[1].x),
                      0.5*(self.rect[0].y+self.rect[1].y))

    def cx(self):
        """ Center x """
        return 0.5*(self.rect[0].x+self.rect[1].x)

    def cy(self):
        """ Center y """
        return 0.5*(self.rect[0].y+self.rect[1].y)

    # The four possible corners
    def ll(self):
        """ Lower left point """
        return self.rect[0]

    def ul(self):
        """ Upper left point """
        return vector(self.rect[0].x, self.rect[1].y)

    def lr(self):
        """ Lower right point """
        return vector(self.rect[1].x, self.rect[0].y)

    def ur(self):
        """ Upper right point """
        return self.rect[1]

    # The possible y edge values
    def uy(self):
        """ Upper y value """
        return self.rect[1].y

    def by(self):
        """ Bottom y value """
        return self.rect[0].y

    # The possible x edge values

    def lx(self):
        """ Left x value """
        return self.rect[0].x

    def rx(self):
        """ Right x value """
        return self.rect[1].x

    # The edge centers
    def rc(self):
        """ Right center point """
        return vector(self.rect[1].x,
                      0.5*(self.rect[0].y+self.rect[1].y))

    def lc(self):
        """ Left center point """
        return vector(self.rect[0].x,
                      0.5*(self.rect[0].y+self.rect[1].y))

    def uc(self):
        """ Upper center point """
        return vector(0.5*(self.rect[0].x+self.rect[1].x),
                      self.rect[1].y)

    def bc(self):
        """ Bottom center point """
        return vector(0.5*(self.rect[0].x+self.rect[1].x),
                      self.rect[0].y)

    def gds_write_file(self, newLayout):
        """Writes the pin shape and label to GDS"""
        debug.info(4, "writing pin (" + str(self.layer) + "):"
                   + str(self.width()) + "x"
                   + str(self.height()) + " @ " + str(self.ll()))

        # Try to use the pin layer if it exists, otherwise
        # use the regular layer
        try:
            (pin_layer_num, pin_purpose) = layer[self.layer + "p"]
        except KeyError:
            (pin_layer_num, pin_purpose) = layer[self.layer]
        (layer_num, purpose) = layer[self.layer]

        # Try to use a global pin purpose if it exists,
        # otherwise, use the regular purpose
        try:
            from openram.tech import pin_purpose as global_pin_purpose
            pin_purpose = global_pin_purpose
        except ImportError:
            pass

        try:
            from openram.tech import label_purpose
            try:
                from openram.tech import layer_override_purpose
                if pin_layer_num in layer_override_purpose:
                    layer_num = layer_override_purpose[pin_layer_num][0]
                    label_purpose = layer_override_purpose[pin_layer_num][1]
            except:
                pass
        except ImportError:
            label_purpose = purpose

        newLayout.addBox(layerNumber=layer_num,
                         purposeNumber=purpose,
                         offsetInMicrons=self.ll(),
                         width=self.width(),
                         height=self.height(),
                         center=False)
        # Draw a second pin shape too if it is different
        if not self.same_lpp((pin_layer_num, pin_purpose), (layer_num, purpose)):
            newLayout.addBox(layerNumber=pin_layer_num,
                             purposeNumber=pin_purpose,
                             offsetInMicrons=self.ll(),
                             width=self.width(),
                             height=self.height(),
                             center=False)
        # Add the text in the middle of the pin.
        # This fixes some pin label offsetting when GDS gets
        # imported into Magic.
        try:
            zoom = GDS["zoom"]
        except KeyError:
            zoom = None
        newLayout.addText(text=self.name,
                          layerNumber=layer_num,
                          purposeNumber=label_purpose,
                          magnification=zoom,
                          offsetInMicrons=self.center())

    def compute_overlap(self, other):
        """ Calculate the rectangular overlap of two rectangles. """
        (r1_ll, r1_ur) = self.rect
        (r2_ll, r2_ur) = other.rect

        # ov_ur = vector(min(r1_ur.x,r2_ur.x),min(r1_ur.y,r2_ur.y))
        # ov_ll = vector(max(r1_ll.x,r2_ll.x),max(r1_ll.y,r2_ll.y))

        dy = min(r1_ur.y, r2_ur.y) - max(r1_ll.y, r2_ll.y)
        dx = min(r1_ur.x, r2_ur.x) - max(r1_ll.x, r2_ll.x)

        if dx >= 0 and dy >= 0:
            return [dx, dy]
        else:
            return [0, 0]

    def distance(self, other):
        """
        Calculate the distance to another pin layout.
        """
        (r1_ll, r1_ur) = self.rect
        (r2_ll, r2_ur) = other.rect

        def dist(x1, y1, x2, y2):
            return math.sqrt((x2-x1)**2 + (y2-y1)**2)

        left = r2_ur.x < r1_ll.x
        right = r1_ur.x < r2_ll.x
        bottom = r2_ur.y < r1_ll.y
        top = r1_ur.y < r2_ll.y

        if top and left:
            return dist(r1_ll.x, r1_ur.y, r2_ur.x, r2_ll.y)
        elif left and bottom:
            return dist(r1_ll.x, r1_ll.y, r2_ur.x, r2_ur.y)
        elif bottom and right:
            return dist(r1_ur.x, r1_ll.y, r2_ll.x, r2_ur.y)
        elif right and top:
            return dist(r1_ur.x, r1_ur.y, r2_ll.x, r2_ll.y)
        elif left:
            return r1_ll.x - r2_ur.x
        elif right:
            return r2_ll.x - r1_ur.x
        elif bottom:
            return r1_ll.y - r2_ur.y
        elif top:
            return r2_ll.y - r1_ur.y
        else:
            # rectangles intersect
            return 0

    def overlap_length(self, other):
        """
        Calculate the intersection segment and determine its length
        """

        if self.contains(other):
            return math.inf
        elif other.contains(self):
            return math.inf
        else:
            intersections = set(self.compute_overlap_segment(other))
            # This is the common case where two pairs of edges overlap
            # at two points, so just find the distance between those two points
            if len(intersections) == 2:
                (p1, p2) = intersections
                return math.sqrt(pow(p1[0]-p2[0], 2) + pow(p1[1]-p2[1], 2))
            # If we have a rectangular overlap region
            elif len(intersections) == 4:
                points = intersections
                ll = vector(min(p.x for p in points), min(p.y for p in points))
                ur = vector(max(p.x for p in points), max(p.y for p in points))
                new_shape = pin_layout("", [ll, ur], self.lpp)
                return max(new_shape.height(), new_shape.width())
            else:
                # This is where we had a corner intersection or none
                return 0


    def compute_overlap_segment(self, other):
        """
        Calculate the intersection segment of two rectangles
        (if any)
        """
        (r1_ll, r1_ur) = self.rect
        (r2_ll, r2_ur) = other.rect

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
        for (p, q) in pairwise(r1_cw_points):
            r1_edges.append([p, q])

        # R2 edges CW
        r2_cw_points = [r2_ll, r2_ul, r2_ur, r2_lr, r2_ll]
        r2_edges = []
        for (p, q) in pairwise(r2_cw_points):
            r2_edges.append([p, q])

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
        if q.x <= max(p.x, r.x) and \
           q.x >= min(p.x, r.x) and \
           q.y <= max(p.y, r.y) and \
           q.y >= min(p.y, r.y):
            return True

        return False

    def segment_intersection(self, s1, s2):
        """
        Determine the intersection point of two segments
        Return the a segment if they overlap.
        Return None if they don't.
        """
        (a, b) = s1
        (c, d) = s2
        # Line AB represented as a1x + b1y = c1
        a1 = b.y - a.y
        b1 = a.x - b.x
        c1 = a1*a.x + b1*a.y

        # Line CD represented as a2x + b2y = c2
        a2 = d.y - c.y
        b2 = c.x - d.x
        c2 = a2*c.x + b2*c.y

        determinant = a1*b2 - a2*b1

        if determinant != 0:
            x = (b2*c1 - b1*c2)/determinant
            y = (a1*c2 - a2*c1)/determinant

            r = vector(x, y).snap_to_grid()
            if self.on_segment(a, r, b) and self.on_segment(c, r, d):
                return r

        return None

    def cut(self, shape):
        """
        Return a set of shapes that are this shape minus the argument shape.
        """
        # Make the unique coordinates in X and Y directions
        x_offsets = sorted([self.lx(), self.rx(), shape.lx(), shape.rx()])
        y_offsets = sorted([self.by(), self.uy(), shape.by(), shape.uy()])

        new_shapes = []
        # Create all of the shapes
        for x1, x2 in zip(x_offsets[0:], x_offsets[1:]):
            if x1==x2:
                continue
            for y1, y2 in zip(y_offsets[0:], y_offsets[1:]):
                if y1==y2:
                    continue
                new_shape = pin_layout("", [vector(x1, y1), vector(x2, y2)], self.lpp)
                # Don't add the existing shape in if it overlaps the pin shape
                if new_shape.contains(shape):
                    continue
                # Only add non-zero shapes
                if new_shape.area() > 0:
                    new_shapes.append(new_shape)

        return new_shapes

    def same_lpp(self, lpp1, lpp2):
        """
        Check if the layers and purposes are the same.
        Ignore if purpose is a None.
        """
        if lpp1[1] == None or lpp2[1] == None:
            return lpp1[0] == lpp2[0]

        return lpp1[0] == lpp2[0] and lpp1[1] == lpp2[1]
