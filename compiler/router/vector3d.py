import debug
import math

class vector3d():
    """
    This is the vector3d class to represent a 3D coordinate.
    It needs to override several operators to support
    concise vector3d operations, output, and other more complex
    data structures like lists.
    """
    def __init__(self, x, y=None, z=None):
        """ init function support two init method"""
        # will take single input as a coordinate
        if y==None:
            self.x = x[0]
            self.y = x[1]
            self.z = x[2]
        #will take two inputs as the values of a coordinate
        else:
            self.x = x
            self.y = y
            self.z = z
        self.tpl=(x,y,z)
            
    def __str__(self):
        """ override print function output """
        return "vector3d:["+str(self.x)+", "+str(self.y)+", "+str(self.z)+"]"

    def __repr__(self):
        """ override print function output """
        return "["+str(self.x)+", "+str(self.y)+", "+str(self.z)+"]"

    def __setitem__(self, index, value):
        """ 
        override setitem function 
        can set value by vector3d[index]=value
        """
        if index==0:
            self.x=value
        elif index==1:
            self.y=value
        elif index==2:
            self.z=value
        else:
            self.x=value[0]
            self.y=value[1]
            self.z=value[2] 

    def __getitem__(self, index):
        """
        override getitem function 
        can get value by value=vector3d[index]
        """
        if index==0:
            return self.x
        elif index==1:
            return self.y
        elif index==2:
            return self.z
        else:
            return self                

    def __add__(self, other):
        """
        Override + function (left add)
        Can add by vector3d(x1,y1,z1)+vector(x2,y2,z2)
        """
        return vector3d(self.x + other[0], self.y + other[1], self.z + other[2])


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
        return vector3d(self.x - other[0], self.y - other[1], self.z - other[2])

    def __hash__(self):
        """
        Override - function (hash)
        Note: This assumes that you DON'T CHANGE THE VECTOR or it will
        break things.
        """
        return hash(self.tpl)


    def __rsub__(self, other):
        """
        Override - function (right)
        """
        return vector3d(other[0]- self.x, other[1] - self.y, other[2] - self.z)

    def rotate(self):
        """ pass a copy of rotated vector3d, without altering the vector3d! """
        return vector3d(self.y,self.x,self.z)

    def scale(self, x_factor, y_factor=None,z_factor=None):
        """ pass a copy of scaled vector3d, without altering the vector3d! """
        if y_factor==None:
            z_factor=x_factor[2]
            y_factor=x_factor[1]
            x_factor=x_factor[0]
        return vector3d(self.x*x_factor,self.y*y_factor,self.z*z_factor)

    def rotate_scale(self, x_factor, y_factor=None, z_factor=None):
        """ pass a copy of scaled vector3d, without altering the vector3d! """
        if y_factor==None:
            z_factor=x_factor[2]
            y_factor=x_factor[1]
            x_factor=x_factor[0]
        return vector3d(self.y*x_factor,self.x*y_factor,self.z*z_factor)

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
        return vector3d(max(self.x,other.x),max(self.y,other.y),max(self.z,other.z))

    def min(self, other):
        """ Min of both values """
        return vector3d(min(self.x,other.x),min(self.y,other.y),min(self.z,other.z))

