# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2002-2006 Jörg Lehmann <joergl@users.sourceforge.net>
# Copyright (C) 2002-2004 André Wobst <wobsta@users.sourceforge.net>
#
# This file is part of PyX (http://pyx.sourceforge.net/).
#
# PyX is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PyX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyX; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import math
import unit

#
# classes representing bounding boxes
#

class bbox_pt:

    """class for bounding boxes

    This variant requires points in the constructor, and is used for internal
    purposes.

    A bbox for which llx_pt is None represents an empty bbox, i.e., one containing
    no points.
    """

    def __init__(self, llx_pt, lly_pt, urx_pt, ury_pt):
        self.llx_pt = llx_pt
        self.lly_pt = lly_pt
        self.urx_pt = urx_pt
        self.ury_pt = ury_pt

    def __nonzero__(self):
        return self.llx_pt is not None

    def __add__(self, other):
        """join two bboxes"""
        if self.llx_pt is not None:
            if other.llx_pt is not None:
                return bbox_pt(min(self.llx_pt, other.llx_pt), min(self.lly_pt, other.lly_pt),
                               max(self.urx_pt, other.urx_pt), max(self.ury_pt, other.ury_pt))
            else:
                return bbox_pt(self.llx_pt, self.lly_pt, self.urx_pt, self.ury_pt)
        else:
            return bbox_pt(other.llx_pt, other.lly_pt, other.urx_pt, other.ury_pt)

    def __iadd__(self, other):
        """join two bboxes inplace"""
        if self.llx_pt is not None:
            if other.llx_pt is not None:
                self.llx_pt = min(self.llx_pt, other.llx_pt)
                self.lly_pt = min(self.lly_pt, other.lly_pt)
                self.urx_pt = max(self.urx_pt, other.urx_pt)
                self.ury_pt = max(self.ury_pt, other.ury_pt)
        else:
            self.llx_pt = other.llx_pt
            self.lly_pt = other.lly_pt
            self.urx_pt = other.urx_pt
            self.ury_pt = other.ury_pt
        return self

    def __mul__(self, other):
        """return intersection of two bboxes"""
        if self.llx_pt is not None and other.llx_pt is not None:
            return bbox_pt(max(self.llx_pt, other.llx_pt), max(self.lly_pt, other.lly_pt),
                           min(self.urx_pt, other.urx_pt), min(self.ury_pt, other.ury_pt))
        else:
            return empty()

    def __imul__(self, other):
        """intersect two bboxes in place"""
        if self.llx_pt is not None and other.llx_pt is not None:
            self.llx_pt = max(self.llx_pt, other.llx_pt)
            self.lly_pt = max(self.lly_pt, other.lly_pt)
            self.urx_pt = min(self.urx_pt, other.urx_pt)
            self.ury_pt = min(self.ury_pt, other.ury_pt)
        elif other.llx_pt is None:
            self.llx_pt = None
        return self

    def copy(self):
        return bbox_pt(self.llx_pt, self.lly_pt, self.urx_pt, self.ury_pt)

    def set(self, other):
        self.llx_pt = other.llx_pt
        self.lly_pt = other.lly_pt
        self.urx_pt = other.urx_pt
        self.ury_pt = other.ury_pt

    def lowrestuple_pt(self):
        if self.llx_pt is None:
            raise ValueError("Cannot return low-res tuple for empty bbox")
        return (math.floor(self.llx_pt), math.floor(self.lly_pt),
                math.ceil(self.urx_pt), math.ceil(self.ury_pt))

    def highrestuple_pt(self):
        if self.llx_pt is None:
            raise ValueError("Cannot return high-res tuple for empty bbox")
        return (self.llx_pt, self.lly_pt, self.urx_pt, self.ury_pt)

    def intersects(self, other):
        """check, if two bboxes intersect eachother"""
        if self.llx_pt is None or other.llx_pt is None:
            return 0
        else:
            return not (self.llx_pt > other.urx_pt or
                        self.lly_pt > other.ury_pt or
                        self.urx_pt < other.llx_pt or
                        self.ury_pt < other.lly_pt)

    def includepoint_pt(self, x_pt, y_pt):
        if self.llx_pt is None:
            self.llx_pt = self.urx_pt = x_pt
            self.ury_pt = self.ury_pt = y_pt
        else:
            self.llx_pt = min(self.llx_pt, x_pt)
            self.lly_pt = min(self.lly_pt, y_pt)
            self.urx_pt = max(self.urx_pt, x_pt)
            self.ury_pt = max(self.ury_pt, y_pt)

    def transform(self, trafo):
        """transform bbox in place by trafo"""
        if self.llx_pt is None:
            return
        # we have to transform all four corner points of the bbox
        llx_pt, lly_pt = trafo.apply_pt(self.llx_pt, self.lly_pt)
        lrx_pt, lry_pt = trafo.apply_pt(self.urx_pt, self.lly_pt)
        urx_pt, ury_pt = trafo.apply_pt(self.urx_pt, self.ury_pt)
        ulx_pt, uly_pt = trafo.apply_pt(self.llx_pt, self.ury_pt)

        # Now, by sorting, we obtain the lower left and upper right corner
        # of the new bounding box.
        self.llx_pt = min(llx_pt, lrx_pt, urx_pt, ulx_pt)
        self.lly_pt = min(lly_pt, lry_pt, ury_pt, uly_pt)
        self.urx_pt = max(llx_pt, lrx_pt, urx_pt, ulx_pt)
        self.ury_pt = max(lly_pt, lry_pt, ury_pt, uly_pt)

    def transformed(self, trafo):
        """return bbox transformed by trafo"""
        if self.llx_pt is None:
            return empty()
        # we have to transform all four corner points of the bbox
        llx_pt, lly_pt = trafo.apply_pt(self.llx_pt, self.lly_pt)
        lrx_pt, lry_pt = trafo.apply_pt(self.urx_pt, self.lly_pt)
        urx_pt, ury_pt = trafo.apply_pt(self.urx_pt, self.ury_pt)
        ulx_pt, uly_pt = trafo.apply_pt(self.llx_pt, self.ury_pt)

        # Now, by sorting, we obtain the lower left and upper right corner
        # of the new bounding box.
        return bbox_pt(min(llx_pt, lrx_pt, urx_pt, ulx_pt), min(lly_pt, lry_pt, ury_pt, uly_pt),
                       max(llx_pt, lrx_pt, urx_pt, ulx_pt), max(lly_pt, lry_pt, ury_pt, uly_pt))

    def enlarge_pt(self, all_pt=0, bottom_pt=None, left_pt=None, top_pt=None, right_pt=None):
        """enlarge bbox in place by the given amounts in pts

        all is used, if bottom, left, top and/or right are not given.

        """
        if self.llx_pt is None:
            return
        if bottom_pt is None:
           bottom_pt = all_pt
        if left_pt is None:
           left_pt = all_pt
        if top_pt is None:
           top_pt = all_pt
        if right_pt is None:
           right_pt = all_pt
        self.llx_pt -= left_pt
        self.lly_pt -= bottom_pt
        self.urx_pt += right_pt
        self.ury_pt += top_pt

    def enlarged_pt(self, all_pt=0, bottom_pt=None, left_pt=None, top_pt=None, right_pt=None):
        """return bbox enlarged by the given amounts in pts

        all is used, if bottom, left, top and/or right are not given.

        """
        if self.llx_pt is None:
            return empty()
        if bottom_pt is None:
           bottom_pt = all_pt
        if left_pt is None:
           left_pt = all_pt
        if top_pt is None:
           top_pt = all_pt
        if right_pt is None:
           right_pt = all_pt
        return bbox_pt(self.llx_pt-left_pt, self.lly_pt-bottom_pt, self.urx_pt+right_pt, self.ury_pt+top_pt)

    def enlarge(self, all=0, bottom=None, left=None, top=None, right=None):
        """enlarge bbox in place

        all is used, if bottom, left, top and/or right are not given.

        """
        if self.llx_pt is None:
            return
        bottom_pt = left_pt = top_pt = right_pt = unit.topt(all)
        if bottom is not None:
           bottom_pt = unit.topt(bottom)
        if left is not None:
           left_pt = unit.topt(left)
        if top is not None:
           top_pt = unit.topt(top)
        if right is not None:
           right_pt = unit.topt(right)
        self.llx_pt -= left_pt
        self.lly_pt -= bottom_pt
        self.urx_pt += right_pt
        self.ury_pt += top_pt

    def enlarged(self, all=0, bottom=None, left=None, top=None, right=None):
        """return bbox enlarged

        all is used, if bottom, left, top and/or right are not given.

        """
        if self.llx_pt is None:
            return empty()
        bottom_pt = left_pt = top_pt = right_pt = unit.topt(all)
        if bottom is not None:
           bottom_pt = unit.topt(bottom)
        if left is not None:
           left_pt = unit.topt(left)
        if top is not None:
           top_pt = unit.topt(top)
        if right is not None:
           right_pt = unit.topt(right)
        return bbox_pt(self.llx_pt-left_pt, self.lly_pt-bottom_pt, self.urx_pt+right_pt, self.ury_pt+top_pt)

    def rect(self):
        """return rectangle corresponding to bbox"""
        if self.llx_pt is None:
            raise ValueError("Cannot return path for empty bbox")
        import path
        return path.rect_pt(self.llx_pt, self.lly_pt, self.urx_pt-self.llx_pt, self.ury_pt-self.lly_pt)

    path = rect

    def height_pt(self):
        """return height of bbox in pts"""
        if self.llx_pt is None:
            raise ValueError("Cannot return heigth of empty bbox")
        return self.ury_pt-self.lly_pt

    def width_pt(self):
        """return width of bbox in pts"""
        if self.llx_pt is None:
            raise ValueError("Cannot return width of empty bbox")
        return self.urx_pt-self.llx_pt

    def top_pt(self):
        """return top coordinate of bbox in pts"""
        if self.llx_pt is None:
            raise ValueError("Cannot return top coordinate of empty bbox")
        return self.ury_pt

    def bottom_pt(self):
        """return bottom coordinate of bbox in pts"""
        if self.llx_pt is None:
            raise ValueError("Cannot return bottom coordinate of empty bbox")
        return self.lly_pt

    def left_pt(self):
        """return left coordinate of bbox in pts"""
        if self.llx_pt is None:
            raise ValueError("Cannot return left coordinate of empty bbox")
        return self.llx_pt

    def right_pt(self):
        """return right coordinate of bbox in pts"""
        if self.llx_pt is None:
            raise ValueError("Cannot return right coordinate of empty bbox")
        return self.urx_pt

    def center_pt(self):
        """return coordinates of the center of the bbox in pts"""
        if self.llx_pt is None:
            raise ValueError("Cannot return center coordinates of empty bbox")
        return 0.5 * (self.llx_pt+self.urx_pt), 0.5 * (self.lly_pt+self.ury_pt)

    def height(self):
        """return height of bbox"""
        return self.height_pt() * unit.t_pt

    def width(self):
        """return width of bbox"""
        return self.width_pt() * unit.t_pt

    def top(self):
        """return top coordinate of bbox"""
        return self.ury_pt * unit.t_pt

    def bottom(self):
        """return bottom coordinate of bbox"""
        return self.lly_pt * unit.t_pt

    def left(self):
        """return left coordinate of bbox"""
        return self.llx_pt * unit.t_pt

    def right(self):
        """return right coordinate of bbox"""
        return self.urx_pt * unit.t_pt

    def center(self):
        """return coordinates of the center of the bbox"""
        centerx_pt, centery_pt = self.center_pt()
        return centerx_pt * unit.t_pt, centery_pt * unit.t_pt


class bbox(bbox_pt):

    """class for bounding boxes"""

    def __init__(self, llx_pt, lly_pt, urx_pt, ury_pt):
        llx_pt = unit.topt(llx_pt)
        lly_pt = unit.topt(lly_pt)
        urx_pt = unit.topt(urx_pt)
        ury_pt = unit.topt(ury_pt)
        bbox_pt.__init__(self, llx_pt, lly_pt, urx_pt, ury_pt)


class empty(bbox_pt):

    """empty bounding box, i.e., one containing no point"""
    def __init__(self):
        bbox_pt.__init__(self, None, None, None, None)
