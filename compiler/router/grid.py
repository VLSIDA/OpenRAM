import numpy as np
from PIL import Image
from itertools import tee
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

        # let's leave this sparse, create cells on demand
        # for x in range(width):
        #     for y in range(height):
        #         for z in range(2):
        #             self.map[vector3d(x,y,z)]=cell()

        # priority queue for the maze routing
        self.q = Q.PriorityQueue()
        
                    

    # def view(self,filename="test.png"):
    #     """
    #     View the data by creating an RGB array and mapping the data
    #     structure to the RGB color palette.
    #     """

    #     v_map = np.zeros((self.width,self.height,3), 'uint8')
    #     mid_map = np.ones((10,self.height,3), 'uint8')
    #     h_map = np.ones((self.width,self.height,3), 'uint8')        

    #     # We shouldn't have a path greater than 50% the HPWL
    #     # so scale all visited indices by this value for colorization
    #     for x in range(self.width):
    #         for y in range(self.height):
    #             h_map[x,y] = self.map[vector3d(x,y,0)].get_color()
    #             v_map[x,y] = self.map[vector3d(x,y,1)].get_color()
    #             # This is just for scale
    #             if x==0 and y==0:
    #                 h_map[x,y] = [0,0,0]
    #                 v_map[x,y] = [0,0,0]
        
    #     v_img = Image.fromarray(v_map, 'RGB').rotate(90)
    #     #v_img.show()
    #     mid_img = Image.fromarray(mid_map, 'RGB').rotate(90)        
    #     h_img = Image.fromarray(h_map, 'RGB').rotate(90)
    #     #h_img.show()
        
    #     # concatenate them into a plot with the two layers
    #     img = Image.new('RGB', (2*self.width+10, self.height))
    #     img.paste(h_img, (0,0))
    #     img.paste(mid_img, (self.width,0))        
    #     img.paste(v_img, (self.width+10,0))
    #     #img.show()
    #     img.save(filename)

    def set_property(self,ll,ur,z,name,value=True):
        assert(ur[1] >= ll[1] and ur[0] >= ll[0])
        assert(ll[0]<self.width and ll[0]>=0)
        assert(ll[1]<self.height and ll[1]>=0)
        assert(ur[0]<self.width and ur[0]>=0)
        assert(ur[1]<self.height and ur[1]>=0)
        for x in range(int(ll[0]),int(ur[0])+1):
            for y in range(int(ll[1]),int(ur[1])+1):
                n = vector3d(x,y,z)
                self.add_map(n)
                setattr (self.map[n], name, True)
                if n not in getattr(self, name):
                    getattr(self, name).append(n)

    def add_blockage(self,ll,ur,z):
        debug.info(3,"Adding blockage ll={0} ur={1} z={2}".format(str(ll),str(ur),z))
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
        
    def route(self,cost_bound=0):
        """
        This does the A* maze routing with preferred direction routing.
        """

        # We set a cost bound of 2.5 x the HPWL for run-time. This can be 
        # over-ridden if the route fails due to pruning a feasible solution.
        if (cost_bound==0):
            cost_bound = 2.5*self.cost_to_target(self.source[0])
            
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
            debug.info(2,"Expanding: cost=" + str(cost) + " " + str(path))
            
            # expand the last element
            neighbors =  self.expand_dirs(path)
            debug.info(4,"Neighbors: " + str(neighbors))
            
            for n in neighbors:
                newpath = path + [n]
                if n not in self.map.keys():
                    self.map[n]=cell()
                self.map[n].visited=True

                # check if we hit the target and are done
                if self.is_target(n):
                    return (newpath,self.cost(newpath))
                else:
                    # potential path cost + predicted cost
                    cost = self.cost(newpath) +  self.cost_to_target(n)
                    # only add the cost if it is less than our bound
                    if (cost < cost_bound):
                        self.q.put((cost,newpath))

        debug.error("Unable to route path. Expand area?",-1)

    def is_target(self,point):
        """
        Point is in the target set, so we are done.
        """
        return point in self.target
            
    def expand_dirs(self,path):
        """
        Expand each of the four cardinal directions plus up or down
        but not expanding to blocked cells. Expands in all directions
        regardless of preferred directions.
        """
        # expand from the last point
        point = path[-1]

        neighbors = []
        
        east = point + vector3d(1,0,0)
        self.add_map(east)
        if not self.map[east].blocked and not east in path:                
            neighbors.append(east)
        
        west= point + vector3d(-1,0,0)
        self.add_map(west)
        if not self.map[west].blocked and not west in path:                
            neighbors.append(west)

        up = point + vector3d(0,0,1)
        self.add_map(up)
        if up.z<2 and not self.map[up].blocked and not up in path:
                neighbors.append(up)

        north = point + vector3d(0,1,0)
        self.add_map(north)
        if not self.map[north].blocked and not north in path:                
            neighbors.append(north)

        south = point + vector3d(0,-1,0)
        self.add_map(south)
        if not self.map[south].blocked and not south in path:                
            neighbors.append(south)
                
        down = point + vector3d(0,0,-1)
        self.add_map(down)            
        if down.z>=0 and not self.map[down].blocked and not down in path:
            neighbors.append(down)

            

        return neighbors

    def add_map(self,p):
        """
        Add a point to the map if it doesn't exist.
        """
        if p not in self.map.keys():
            self.map[p]=cell()
        
    def init_queue(self):
        """
        Populate the queue with all the source pins with cost
        to the target. Each item is a path of the grid cells.
        We will use an A* search, so this cost must be pessimistic.
        Cost so far will be the length of the path.
        """
        debug.info(4,"Initializing queue.")
        for s in self.source:
            cost = self.cost_to_target(s)
            debug.info(4,"Init: cost=" + str(cost) + " " + str([s]))
            self.q.put((cost,[s]))

    def cost_to_target(self,source):
        """
        Find the cheapest HPWL distance to any target point
        """
        cost = source.hpwl(self.target[0])
        for t in self.target:
            cost = min(source.hpwl(t),cost)
        return cost


    

    def cost(self,path):
        """ 
        The cost of the path is the length plus a penalty for the number
        of vias.
        We assume that non-preferred direction is penalized 2x.
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
                cost += 2
            elif p0.x != p1.x: # horizontal
                cost += 2 if (p0.z == 1) else 1
            elif p0.y != p1.y: # vertical
                cost += 2 if (p0.z == 0) else 1
            else:
                debug.error("Non-changing direction!")
        
        # for p in path:
        #     if p.z != prev_p.z:
        #         via_cost += 2 # we count a via as 2x a wire track
        #         prev_layer = p.z
        #     prev_p = p
        #
        #return len(path)+via_cost
        return cost
    
    def get_inertia(self,p0,p1):
        """ 
        Sets the direction based on the previous direction we came from. 
        """
        # direction (index) of movement
        if p0.x==p1.x:
            return 1
        elif p0.y==p1.y:
            return 0
        else:
            # z direction
            return 2
