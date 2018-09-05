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

    def __init__(self, gds_name=None, module=None):
        """Use the gds file for the blockages with the top module topName and
        layers for the layers to route on
        """
        router.__init__(self, gds_name, module)
        
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
        Add power supply rails and connect all pins to these rails.
        """
        debug.info(1,"Running supply router on {0} and {1}...".format(vdd_name, gnd_name))
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
        
        # Now add the blockages (all shapes except the pins)
        self.add_blockages()

        #self.route_supply_rails()

        #self.route_supply_pins()
        
        # source pin will be a specific layout pin
        # target pin will be the rails only
            
        # returns the path in tracks
        # (path,cost) = self.rg.route(detour_scale)
        # if path:
        #     debug.info(1,"Found path: cost={0} ".format(cost))
        #     debug.info(2,str(path))
        #     self.add_route(path)
        #     return True
        # else:
        #     self.write_debug_gds()
        #     # clean up so we can try a reroute
        #     self.clear_pins()
            
        self.write_debug_gds()
        return False

    def route_supply_rails(self):
        """
        Add supply rails for vdd and gnd alternating in both layers.
        Connect cross-over points with vias.
        """
        # vdd will be the even grids
        
        # gnd will be the odd grids


        pass
    
    def route_supply_pins(self, pin):
        """
        This will route all the supply pins to supply rails one at a time.
        After each one, it adds the cells to the blockage list.
        """
        for pin_name in self.pins.keys():
            for pin in self.pins[pin_name]:
                route_supply_pin(pin)
                


    def route_supply_pin(self, pin):
        """
        This will take a single pin and route it to the appropriate supply rail.
        Do not allow other pins to be destinations so that everything is connected 
        to the rails.
        """
        pass
    
        
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

    
    def create_routing_grid(self):
        """ 
        Create a sprase routing grid with A* expansion functions.
        """
        # We will add a halo around the boundary
        # of this many tracks
        size = self.ur - self.ll
        debug.info(1,"Size: {0} x {1}".format(size.x,size.y))

        import supply_grid
        self.rg = supply_grid.supply_grid()


    
