import gdsMill
import tech
from contact import contact
import math
import debug
import grid
from pin_layout import pin_layout
from vector import vector
from vector3d import vector3d 
from globals import OPTS
from router import router

class supply_router(router):
    """
    A router class to read an obstruction map from a gds and
    routes a grid to connect the supply on the two layers.
    """

    def __init__(self, gds_name):
        """Use the gds file for the blockages with the top module topName and
        layers for the layers to route on
        """

        router.__init__(self, gds_name)
        
        self.pins = {}

            
    def clear_pins(self):
        """
        Convert the routed path to blockages.
        Keep the other blockages unchanged.
        """
        self.pins = {}
        self.rg.reinit()
        

    def route(self, cell, layers, vdd_name="vdd", gnd_name="gnd"):
        """ 
        Route a single source-destination net and return
        the simplified rectilinear path. 
        """
        self.cell = cell
        self.pins[vdd_name] = []
        self.pins[gnd_name] = []

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
        self.get_pin(vdd_name)
        self.get_pin(gnd_name)
        
        # Now add the blockages (all shapes except the src/tgt pins)
        self.add_blockages()
        # Add blockages from previous routes
        self.add_path_blockages()        

        # Now add the src/tgt if they are not blocked by other shapes
        self.add_pin(vdd_name,True)
        #self.add_pin()

            
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

    


    ##########################
    # Gridded supply route functions
    ##########################
    def create_grid(self, ll, ur):
        """ Create alternating vdd/gnd lines horizontally """
        
        self.create_horizontal_grid()
        self.create_vertical_grid()


    def create_horizontal_grid(self):
        """ Create alternating vdd/gnd lines horizontally """
        
        pass

    def create_vertical_grid(self):
        """ Create alternating vdd/gnd lines horizontally """
        pass
    
    def route(self):
        #self.create_grid()
        pass
