import numpy as np
import string
import debug
from vector3d import vector3d
from grid_cell import grid_cell

class grid:
    """
    A two layer routing map. Each cell can be blocked in the vertical
    or horizontal layer.
    """
    # costs are relative to a unit grid
    # non-preferred cost allows an off-direction jog of 1 grid
    # rather than 2 vias + preferred direction (cost 5)
    VIA_COST = 2 
    NONPREFERRED_COST = 4
    PREFERRED_COST = 1


    def __init__(self, ll, ur, track_width):
        """ Initialize the map and define the costs. """

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
        if isinstance(n,list):
            for item in n:
                if self.is_blocked(item):
                    return True
            else:
                return False
        else:
            self.add_map(n)
            return self.map[n].blocked


    def set_path(self,n,value=True):
        if isinstance(n,list):
            for item in n:
                self.set_path(item,value)
        else:
            self.add_map(n)
            self.map[n].path=value

    def set_blockages(self,block_list,value=True):
        debug.info(3,"Adding blockage list={0}".format(str(block_list)))
        for n in block_list:
            self.set_blocked(n,value)

    def clear_blockages(self):
        debug.info(2,"Clearing all blockages")
        for n in self.map.keys():
            self.set_blocked(n,False)
            
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
        debug.info(3,"Adding source list={0}".format(str(track_list)))
        for n in track_list:
            debug.info(4,"Adding source ={0}".format(str(n)))
            self.set_source(n)
            self.set_blocked(n,False)


    def add_target(self,track_list):
        debug.info(3,"Adding target list={0}".format(str(track_list)))
        for n in track_list:
            debug.info(4,"Adding target ={0}".format(str(n)))                                
            self.set_target(n)
            self.set_blocked(n,False)            

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
                self.map[n]=grid_cell()
        

    def block_path(self,path):
        """ 
        Mark the path in the routing grid as blocked. 
        Also unsets the path flag.
        """
        path.set_path(False)
        path.set_blocked(True)
            
    

        
        
