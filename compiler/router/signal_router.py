import gdsMill
import tech
from contact import contact
import math
import debug
from pin_layout import pin_layout
from vector import vector
from vector3d import vector3d 
from globals import OPTS
from router import router

class signal_router(router):
    """A router class to read an obstruction map from a gds and plan a
    route on a given layer. This is limited to two layer routes.
    """

    def __init__(self, gds_name=None, module=None):
        """Use the gds file for the blockages with the top module topName and
        layers for the layers to route on
        """
        router.__init__(self, gds_name, module)

        # all the paths we've routed so far (to supplement the blockages)
        self.paths = []


    def create_routing_grid(self):
        """ 
        Create a sprase routing grid with A* expansion functions.
        """
        # We will add a halo around the boundary
        # of this many tracks
        size = self.ur - self.ll
        debug.info(1,"Size: {0} x {1}".format(size.x,size.y))

        import astar_grid
        self.rg = astar_grid.astar_grid()
        

    def route(self, cell, layers, src, dest, detour_scale=5):
        """ 
        Route a single source-destination net and return
        the simplified rectilinear path. Cost factor is how sub-optimal to explore for a feasible route. 
        This is used to speed up the routing when there is not much detouring needed.
        """
        debug.info(1,"Running signal router from {0} to {1}...".format(src,dest))
        self.cell = cell
        self.source_pin_name = src
        self.target_pin_name = dest

        # Clear the pins if we have previously routed
        if (hasattr(self,'rg')):
            self.clear_pins()
        else:
            # Set up layers and track sizes
            self.set_layers(layers)
            # Creat a routing grid over the entire area
            # FIXME: This could be created only over the routing region,
            # but this is simplest for now.
            self.create_routing_grid()
            # This will get all shapes as blockages
            self.find_blockages()

        # Get the pin shapes
        self.get_pin(src)
        self.get_pin(dest)
        
        # Now add the blockages (all shapes except the src/tgt pins)
        self.add_blockages()
        # Add blockages from previous paths
        self.add_path_blockages()        

        # Now add the src/tgt if they are not blocked by other shapes
        self.add_pin(src,True)
        self.add_pin(dest,False)

            
        # returns the path in tracks
        (path,cost) = self.rg.route(detour_scale)
        if path:
            debug.info(1,"Found path: cost={0} ".format(cost))
            debug.info(2,str(path))
            self.add_route(path)
            return True
        else:
            self.write_debug_gds()
            # clean up so we can try a reroute
            self.clear_pins()
            

        return False

                           
    def add_route(self,path):
        """ 
        Add the current wire route to the given design instance.
        """
        debug.info(3,"Set path: " + str(path))

        # Keep track of path for future blockages
        self.paths.append(path)
        
        # This is marked for debug
        self.rg.add_path(path)

        # For debugging... if the path failed to route.
        if False or path==None:
            self.write_debug_gds()

            
        # First, simplify the path for
        #debug.info(1,str(self.path))        
        contracted_path = self.contract_path(path)
        debug.info(1,str(contracted_path))

        # convert the path back to absolute units from tracks
        abs_path = map(self.convert_point_to_units,contracted_path)
        debug.info(1,str(abs_path))
        self.cell.add_route(self.layers,abs_path)


    def get_inertia(self,p0,p1):
        """ 
        Sets the direction based on the previous direction we came from. 
        """
        # direction (index) of movement
        if p0.x!=p1.x:
            return 0
        elif p0.y!=p1.y:
            return 1
        else:
            # z direction
            return 2

    def contract_path(self,path):
        """ 
        Remove intermediate points in a rectilinear path. 
        """
        newpath = [path[0]]
        for i in range(1,len(path)-1):
            prev_inertia=self.get_inertia(path[i-1],path[i])
            next_inertia=self.get_inertia(path[i],path[i+1])
            # if we switch directions, add the point, otherwise don't
            if prev_inertia!=next_inertia:
                newpath.append(path[i])

        # always add the last path
        newpath.append(path[-1])
        return newpath
    

    def add_path_blockages(self):
        """
        Go through all of the past paths and add them as blockages.
        This is so we don't have to write/reload the GDS.
        """
        for path in self.paths:
            for grid in path:
                self.rg.set_blocked(grid)
        



