import gdsMill
import tech
from contact import contact
import math
import debug
from globals import OPTS
import grid
from pin_layout import pin_layout
from vector import vector
from vector3d import vector3d 
from router import router
from direction import direction

class supply_router(router):
    """
    A router class to read an obstruction map from a gds and
    routes a grid to connect the supply on the two layers.
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
        size = self.ur - self.ll
        debug.info(1,"Size: {0} x {1}".format(size.x,size.y))

        import supply_grid
        self.rg = supply_grid.supply_grid(self.ll, self.ur, self.track_width)
    
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

        self.route_supply_rails()
        self.connect_supply_rails()
        #self.route_pins_to_rails()
        
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

    def connect_supply_rails(self):
        """
        Add vias between overlapping supply rails.
        """
        self.connect_supply_rail("vdd")
        self.connect_supply_rail("gnd")
        
    def connect_supply_rail(self, name):
        """
        Add vias between overlapping supply rails.
        """
        paths = [x for x in self.paths if x.name == name]
        
        # Split into horizontal and vertical
        vertical_paths = [x for x in paths if x[0][0].z==1]
        horizontal_paths = [x for x in paths if x[0][0].z==0]

        shared_areas = []
        for v in vertical_paths:
            for h in horizontal_paths:
                overlap = v.overlap(h)
                if overlap:
                    shared_areas.append(overlap)


        for (ll,ur) in shared_areas:
            center = (ll + ur).scale(0.5,0.5,0)
            self.add_via(center,self.rail_track_width)
        

                
    def route_supply_rails(self):
        """
        Add supply rails for vdd and gnd alternating in both layers.
        Connect cross-over points with vias.
        """
        # Width in grid units.
        self.rail_track_width = 2

        # Keep a list of all the rail wavepaths
        self.paths = []
            
        # vdd will be the even grids every 2 widths
        for offset in range(0, self.rg.ur.y, 2*self.rail_track_width):
            # Seed the function at the location with the given width
            wave = [vector3d(0,offset+i,0) for i in range(self.rail_track_width)]
            # While we can keep expanding east
            while wave and wave[0].x < self.rg.ur.x:
                wave = self.route_supply_rail("vdd", wave, direction.EAST)

        # gnd will be the even grids every 2 widths
        for offset in range(self.rail_track_width, self.rg.ur.y, 2*self.rail_track_width):
            # Seed the function at the location with the given width
            wave = [vector3d(0,offset+i,0) for i in range(self.rail_track_width)]
            # While we can keep expanding east
            while wave and wave[0].x < self.rg.ur.x:
                wave = self.route_supply_rail("gnd", wave, direction.EAST)

        # vdd will be the even grids every 2 widths
        for offset in range(0, self.rg.ur.x, 2*self.rail_track_width):
            # Seed the function at the location with the given width
            wave = [vector3d(offset+i,0,1) for i in range(self.rail_track_width)]
            # While we can keep expanding east
            while wave and wave[0].y < self.rg.ur.y:
                wave = self.route_supply_rail("vdd", wave, direction.NORTH)

        # gnd will be the even grids every 2 widths
        for offset in range(self.rail_track_width, self.rg.ur.x, 2*self.rail_track_width):
            # Seed the function at the location with the given width
            wave = [vector3d(offset+i,0,1) for i in range(self.rail_track_width)]
            # While we can keep expanding east
            while wave and wave[0].y < self.rg.ur.y:
                wave = self.route_supply_rail("gnd", wave, direction.NORTH)


    def route_supply_rail(self, name, seed_wave, direct):
        """
        Add supply rails alternating layers.
        Return the final wavefront for seeding the next wave.
        """

        # Sweep to find an initial unblocked valid wave
        start_wave = self.rg.find_start_wave(seed_wave, len(seed_wave), direct)
        if not start_wave:
            return None

        # Expand the wave to the right
        wave_path = self.rg.probe(start_wave, direct)
        if not wave_path:
            return None

        # Filter any path that won't span 2 rails
        # so that we can guarantee it is connected
        if len(wave_path)>=2*self.rail_track_width:
            self.add_wavepath(name, wave_path)
            wave_path.name = name
            self.paths.append(wave_path)

        # seed the next start wave location
        wave_end = wave_path[-1]
        return wave_path.neighbor(direct)
    

                    
                
        
    def route_pins_to_rails(self):
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
    
        
    # def add_route(self,path):
    #     """ 
    #     Add the current wire route to the given design instance.
    #     """
    #     debug.info(3,"Set path: " + str(path))

    #     # Keep track of path for future blockages
    #     self.paths.append(path)
        
    #     # This is marked for debug
    #     self.rg.add_path(path)

    #     # For debugging... if the path failed to route.
    #     if False or path==None:
    #         self.write_debug_gds()

    #     # First, simplify the path for
    #     #debug.info(1,str(self.path))        
    #     contracted_path = self.contract_path(path)
    #     debug.info(1,str(contracted_path))

    #     # convert the path back to absolute units from tracks
    #     abs_path = map(self.convert_point_to_units,contracted_path)
    #     debug.info(1,str(abs_path))
    #     self.cell.add_route(self.layers,abs_path)

    


    
