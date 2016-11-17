import numpy as np
from PIL import Image
import debug
from vector3d import vector3d

from cell import cell
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
        
    
class grid:
    """A two layer routing map. Each cell can be blocked in the vertical
    or horizontal layer.

    """

    def __init__(self, width, height):
        """ Create a routing map of width x height cells and 2 in the z-axis. """
        self.width=width
        self.height=height
        self.source = []
        self.target = []
        self.blocked = []
        self.map={}
        for x in range(width):
            for y in range(height):
                for z in range(2):
                    self.map[vector3d(x,y,z)]=cell()

        # priority queue for the maze routing
        self.q = Q.PriorityQueue()
        
                    

    def view(self):
        """
        View the data by creating an RGB array and mapping the data
        structure to the RGB color palette.
        """

        v_map = np.zeros((self.width,self.height,3), 'uint8')
        mid_map = np.ones((25,self.height,3), 'uint8')
        h_map = np.ones((self.width,self.height,3), 'uint8')        

        # We shouldn't have a path greater than 50% the HPWL
        # so scale all visited indices by this value for colorization
        for x in range(self.width):
            for y in range(self.height):
                h_map[x,y] = self.map[vector3d(x,y,0)].get_color()
                v_map[x,y] = self.map[vector3d(x,y,1)].get_color()
                # This is just for scale
                if x==0 and y==0:
                    h_map[x,y] = [0,0,0]
                    v_map[x,y] = [0,0,0]
        
        v_img = Image.fromarray(v_map, 'RGB').rotate(90)
        #v_img.show()
        mid_img = Image.fromarray(mid_map, 'RGB').rotate(90)        
        h_img = Image.fromarray(h_map, 'RGB').rotate(90)
        #h_img.show()
        
        # concatenate them into a plot with the two layers
        img = Image.new('RGB', (2*self.width+25, self.height))
        img.paste(h_img, (0,0))
        img.paste(mid_img, (self.width,0))        
        img.paste(v_img, (self.width+25,0))
        img.show()
        img.save("test.png")

    def set_property(self,ll,ur,z,name,value=True):
        assert(ur[1] >= ll[1] and ur[0] >= ll[0])
        assert(ll[0]<self.width and ll[0]>=0)
        assert(ll[1]<self.height and ll[1]>=0)
        assert(ur[0]<self.width and ur[0]>=0)
        assert(ur[1]<self.height and ur[1]>=0)
        for x in range(int(ll[0]),int(ur[0])+1):
            for y in range(int(ll[1]),int(ur[1])+1):
                debug.info(3,"  Adding {3} x={0} y={1} z={2}".format(str(ll),str(ur),z,name))
                setattr (self.map[vector3d(x,y,z)], name, True)
                getattr (self, name).append(vector3d(x,y,z))

    def add_blockage(self,ll,ur,z):
        debug.info(2,"Adding blockage ll={0} ur={1} z={2}".format(str(ll),str(ur),z))
        self.set_property(ll,ur,z,"blocked")

    def set_source(self,ll,ur,z):
        debug.info(1,"Adding source ll={0} ur={1} z={2}".format(str(ll),str(ur),z))
        self.set_property(ll,ur,z,"source")


    def set_target(self,ll,ur,z):
        debug.info(1,"Adding target ll={0} ur={1} z={2}".format(str(ll),str(ur),z))
        self.set_property(ll,ur,z,"target")

    def set_path(self,path):
        """ 
        Mark the path in the routing grid for visualization
        """
        for p in path:
            self.map[p].path=True
        
    def route(self):
        """
        This does the A* maze routing.
        """
        
        # Make sure the queue is empty if we run another route
        while not self.q.empty():
            self.q.get()

        # Put the source items into the queue
        self.init_queue()
        cheapest_path = None
        cheapest_cost = None
        
        # Keep expanding and adding to the priority queue until we are done
        while not self.q.empty():
            (cost,path) = self.q.get()
            debug.info(2,"Expanding: cost=" + str(cost))
            debug.info(3,str(path))
            
            # expand the last element
            neighbors =  self.expand_dirs(path)
            debug.info(2,"Neighbors: " + str(neighbors))
            
            for n in neighbors:
                newpath = path + [n]
                self.map[n].visited=True

                # check if we hit the target and are done
                if self.is_target(n):
                    return newpath
                else:
                    # path cost + predicted cost
                    cost = len(newpath) +  self.cost_to_target(n) 
                    self.q.put((cost,newpath))

        self.view()
        debug.error("Unable to route path. Expand area?",-1)

    def is_target(self,point):
        """
        Point is in the target set, so we are done.
        """
        return point in self.target
            
    def expand_dirs(self,path):
        """
        Expand each of the four cardinal directions plus up or down
        but not expanding to blocked cells. Always follow horizontal/vertical
        routing layer requirements. Extend in the future if not routable?
        """
        # expand from the last point
        point = path[-1]

        neighbors = []
        # check z layer for enforced direction routing
        if point.z==0:
            east = point + vector3d(1,0,0)
            west= point + vector3d(-1,0,0)
            if east.x<self.width and not self.map[east].blocked and not self.map[east].visited:
                neighbors.append(east)
            if west.x>=0 and not self.map[west].blocked and not self.map[west].visited:
                neighbors.append(west)

            up = point + vector3d(0,0,1)
            if not self.map[up].blocked and not self.map[up].visited:
                neighbors.append(up)
        elif point.z==1:
            north = point + vector3d(0,1,0)
            south = point + vector3d(0,-1,0)
            if north.y<self.height and not self.map[north].blocked and not self.map[north].visited:
                neighbors.append(north)
            if south.y>=0 and not self.map[south].blocked and not self.map[south].visited:
                neighbors.append(south)
                
            down = point + vector3d(0,0,-1)
            if not self.map[down].blocked and not self.map[down].visited:
                neighbors.append(down)

            

        return neighbors
        
        
    def init_queue(self):
        """
        Populate the queue with all the source pins with cost
        to the target. Each item is a path of the grid cells.
        We will use an A* search, so this cost must be pessimistic.
        Cost so far will be the length of the path.
        """
        debug.info(0,"Initializing queue.")
        for s in self.source:
            cost = self.cost_to_target(s)
            debug.info(2,"Init: cost=" + str(cost) + " " + str([s]))
            self.q.put((cost,[s]))

    def cost_to_target(self,source):
        """
        Find the cheapest HPWL distance to any target point
        """
        cost = source.hpwl(self.target[0])
        for t in self.target:
            cost = min(source.hpwl(t),cost)
        return cost
