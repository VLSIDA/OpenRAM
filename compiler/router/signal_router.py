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
    """
    A router class to read an obstruction map from a gds and plan a
    route on a given layer. This is limited to two layer routes.
    """

    def __init__(self, gds_name=None, module=None):
        """
        Use the gds file for the blockages with the top module topName and
        layers for the layers to route on
        """
        router.__init__(self, gds_name, module)


    def create_routing_grid(self):
        """ 
        Create a sprase routing grid with A* expansion functions.
        """
        # We will add a halo around the boundary
        # of this many tracks
        size = self.ur - self.ll
        debug.info(1,"Size: {0} x {1}".format(size.x,size.y))

        import signal_grid
        self.rg = signal_grid.signal_grid(self.ll, self.ur, self.track_width)
        

    def route(self, cell, layers, src, dest, detour_scale=5):
        """ 
        Route a single source-destination net and return
        the simplified rectilinear path. Cost factor is how sub-optimal to explore for a feasible route. 
        This is used to speed up the routing when there is not much detouring needed.
        """
        debug.info(1,"Running signal router from {0} to {1}...".format(src,dest))
        self.cell = cell

        self.pins[src] = []
        self.pins[dest] = []
        
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

        # Now add the blockages (all shapes except the pins)
        self.get_pin(src)
        self.get_pin(dest)
        
        # Now add the blockages
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

                           
        



