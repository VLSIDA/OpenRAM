# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import math
from openram import tech


class vector():
    """
    This is the vector class to represent the coordinate
    vector. It makes the coordinate operations easy and short
    so the code is concise.
    It needs to override several operators to support
    concise vector operations, output, and other more complex
    data structures like lists.
    """
    def __init__(self, x, y=0):
        """ init function support two init method"""
        # will take single input as a coordinate
        if isinstance(x, (list,tuple,vector)):
            self.x = float(x[0])
            self.y = float(x[1])
        #will take two inputs as the values of a coordinate
        else:
            self.x = float(x)
            self.y = float(y)
        self._hash = hash((self.x,self.y))

    def __str__(self):
        """ override print function output """
        return "v["+str(self.x)+","+str(self.y)+"]"

    def __repr__(self):
        """ override print function output """
        return "v["+str(self.x)+","+str(self.y)+"]"

    def __setitem__(self, index, value):
        """
        override setitem function
        can set value by vector[index]=value
        """
        if index==0:
            self.x=float(value)
        elif index==1:
            self.y=float(value)
        else:
            self.x=float(value[0])
            self.y=float(value[1])
        self._hash = hash((self.x,self.y))

    def __getitem__(self, index):
        """
        override getitem function
        can get value by value=vector[index]
        """
        if index==0:
            return self.x
        elif index==1:
            return self.y
        else:
            return self

    def __add__(self, other):
        """
        Override + function (left add)
        Can add by vector(x1,y1)+vector(x2,y2)
        """
        return vector(self.x + other[0], self.y + other[1])


    def __radd__(self, other):
        """
        Override + function (right add)
        """
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__(self, other):
        """
        Override - function (left)
        """
        return vector(self.x - other[0], self.y - other[1])

    def __rsub__(self, other):
        """
        Override - function (right)
        """
        return vector(other[0]- self.x, other[1] - self.y)

    def __hash__(self):
        """
        Override - function (hash)
        Note: This assumes that you DON'T CHANGE THE VECTOR or it will
        break things.
        """
        return self._hash

    def snap_to_grid(self):
        self.x = self.snap_offset_to_grid(self.x)
        self.y = self.snap_offset_to_grid(self.y)
        self._hash = hash((self.x,self.y))
        return self

    def snap_offset_to_grid(self, offset):
        """
        Changes the coodrinate to match the grid settings
        """
        grid = tech.drc["grid"]
        # this gets the nearest integer value
        off_in_grid = int(round(round((offset / grid), 2), 0))
        offset = off_in_grid * grid
        return offset

    def rotate(self):
        """ pass a copy of rotated vector, without altering the vector! """
        return vector(self.y,self.x)

    def scale(self, x_factor, y_factor=None):
        """ pass a copy of scaled vector, without altering the vector! """
        if y_factor==None:
            y_factor=x_factor[1]
            x_factor=x_factor[0]
        return vector(self.x*x_factor,self.y*y_factor)

    def rotate_scale(self, x_factor, y_factor=None):
        """ pass a copy of scaled vector, without altering the vector! """
        if y_factor==None:
            y_factor=x_factor[1]
            x_factor=x_factor[0]
        return vector(self.y*x_factor,self.x*y_factor)

    def floor(self):
        """
        Override floor function
        """
        return vector(int(math.floor(self.x)),int(math.floor(self.y)))

    def ceil(self):
        """
        Override ceil function
        """
        return vector(int(math.ceil(self.x)),int(math.ceil(self.y)))

    def round(self):
        """
        Override round function
        """
        return vector(int(round(self.x)),int(round(self.y)))


    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """Override the default non-equality behavior"""
        return not self.__eq__(other)

    def max(self, other):
        """ Max of both values """
        return vector(max(self.x,other.x),max(self.y,other.y))

    def min(self, other):
        """ Min of both values """
        return vector(min(self.x,other.x),min(self.y,other.y))
