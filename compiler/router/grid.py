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

    def __init__(self):
        """ Initialize the map and define the costs. """

        # costs are relative to a unit grid
        # non-preferred cost allows an off-direction jog of 1 grid
        # rather than 2 vias + preferred direction (cost 5)
        self.VIA_COST = 2
        self.NONPREFERRED_COST = 4
        self.PREFERRED_COST = 1

        # let's leave the map sparse, cells are created on demand to reduce memory
        self.map={}

    def set_blocked(self,n):
        self.add_map(n)
        self.map[n].blocked=True

    def is_blocked(self,n):
        self.add_map(n)
        return self.map[n].blocked

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

    def add_map(self,p):
        """
        Add a point to the map if it doesn't exist.
        """
        if p not in self.map.keys():
            self.map[p]=cell()
        
    def add_path(self,path):
        """ 
        Mark the path in the routing grid for visualization
        """
        self.path=path
        for p in path:
            self.map[p].path=True

    def block_path(self,path):
        """ 
        Mark the path in the routing grid as blocked. 
        Also unsets the path flag.
        """
        for p in path:
            self.map[p].path=False
            self.map[p].blocked=True
            
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
    

        
        
