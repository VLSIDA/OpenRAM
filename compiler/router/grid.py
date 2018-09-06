import numpy as np
import string
from itertools import tee
import debug
from vector3d import vector3d
from cell import cell
import os

class grid:
    """
    A two layer routing map. Each cell can be blocked in the vertical
    or horizontal layer.
    """

    def __init__(self, ll, ur, track_width):
        """ Initialize the map and define the costs. """

        # costs are relative to a unit grid
        # non-preferred cost allows an off-direction jog of 1 grid
        # rather than 2 vias + preferred direction (cost 5)
        self.VIA_COST = 2
        self.NONPREFERRED_COST = 4
        self.PREFERRED_COST = 1

        # list of the source/target grid coordinates
        self.source = []
        self.target = []

        self.track_width = track_width
        self.track_widths = [self.track_width, self.track_width, 1.0] 
        self.track_factor = [1/self.track_width, 1/self.track_width, 1.0]
        
        # The bounds are in grids for this
        # This is really lower left bottom layer and upper right top layer in 3D.
        self.ll = vector3d(ll.x,ll.y,0).scale(self.track_factor).round()
        self.ur = vector3d(ur.x,ur.y,1).scale(self.track_factor).round()
        
        # let's leave the map sparse, cells are created on demand to reduce memory
        self.map={}

    def set_blocked(self,n,value=True):
        if isinstance(n,list):
            for item in n:
                self.set_blocked(item,value)
        else:
            self.add_map(n)
            self.map[n].blocked=value

    def is_blocked(self,n):
        self.add_map(n)
        return self.map[n].blocked

    def set_path(self,n,value=True):
        if isinstance(n,list):
            for item in n:
                self.set_path(item,value)
        else:
            self.add_map(n)
            self.map[n].path=value

    
    def add_blockage_shape(self,ll,ur,z):
        debug.info(3,"Adding blockage ll={0} ur={1} z={2}".format(str(ll),str(ur),z))

        block_list = []
        for x in range(int(ll[0]),int(ur[0])+1):
            for y in range(int(ll[1]),int(ur[1])+1):
                block_list.append(vector3d(x,y,z))

        self.add_blockage(block_list)

    def add_blockage(self,block_list):
        debug.info(2,"Adding blockage list={0}".format(str(block_list)))
        for n in block_list:
            self.set_blocked(n)

    def set_source(self,n):
        if isinstance(n,list):
            for item in n:
                self.set_source(item)
        else:
            self.add_map(n)
            self.map[n].source=True
            self.source.append(n)
        
    def set_target(self,n):
        if isinstance(n,list):
            for item in n:
                self.set_target(item)
        else:
            self.add_map(n)
            self.map[n].target=True
            self.target.append(n)

        
    def add_source(self,track_list):
        debug.info(2,"Adding source list={0}".format(str(track_list)))
        for n in track_list:
            debug.info(3,"Adding source ={0}".format(str(n)))
            self.set_source(n)


    def add_target(self,track_list):
        debug.info(2,"Adding target list={0}".format(str(track_list)))
        for n in track_list:
            debug.info(3,"Adding target ={0}".format(str(n)))                                
            self.set_target(n)

    def is_target(self,point):
        """
        Point is in the target set, so we are done.
        """
        return point in self.target
            
    def add_map(self,n):
        """
        Add a point to the map if it doesn't exist.
        """
        if isinstance(n,list):
            for item in n:
                self.add_map(item)
        else:
            if n not in self.map.keys():
                self.map[n]=cell()
        
    def add_path(self,path):
        """ 
        Mark the path in the routing grid for visualization
        """
        self.path=path
        for p in path:
            self.set_path(p)

    def block_path(self,path):
        """ 
        Mark the path in the routing grid as blocked. 
        Also unsets the path flag.
        """
        for p in path:
            self.set_path(p,False)
            self.set_blocked(p)
            
    def cost(self,path):
        """ 
        The cost of the path is the length plus a penalty for the number
        of vias. We assume that non-preferred direction is penalized.
        """

        # Ignore the source pin layer change, FIXME?
        def pairwise(iterable):
            "s -> (s0,s1), (s1,s2), (s2, s3), ..."
            a, b = tee(iterable)
            next(b, None)
            return zip(a, b)


        plist = pairwise(path)
        cost = 0
        for p0,p1 in plist:
            if p0.z != p1.z: # via
                cost += self.VIA_COST
            elif p0.x != p1.x: # horizontal
                cost += self.NONPREFERRED_COST if (p0.z == 1) else self.PREFERRED_COST
            elif p0.y != p1.y: # vertical
                cost += self.NONPREFERRED_COST if (p0.z == 0) else self.PREFERRED_COST
            else:
                debug.error("Non-changing direction!")

        return cost
    

        
        
