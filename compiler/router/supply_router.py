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

        # Power rail width in grid units.
        self.rail_track_width = 2
        

        
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
        self.vdd_name = vdd_name
        self.gnd_name = gnd_name

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
        self.find_pins(vdd_name)
        self.find_pins(gnd_name)
        

        self.add_blockages()
        self.add_pin_blockages(vdd_name)
        self.route_supply_rails(gnd_name,0)
        self.connect_supply_rail(gnd_name)
        self.route_pins_to_rails(gnd_name)

        # Start fresh. Not the best for run-time, but simpler.
        self.clear_blockages()
        
        self.add_blockages()
        self.add_pin_blockages(gnd_name)
        self.route_supply_rails(vdd_name,1)
        self.connect_supply_rail(vdd_name)
        self.route_pins_to_rails(vdd_name)
        
        self.write_debug_gds()
        return False

        
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
        

                
    def route_supply_rails(self, name, supply_number):
        """
        Route the horizontal and vertical supply rails across the entire design.
        """

        start_offset = supply_number*self.rail_track_width
        max_yoffset = self.rg.ur.y
        max_xoffset = self.rg.ur.x
        step_offset = 2*self.rail_track_width

        # Horizontal supply rails
        for offset in range(start_offset, max_yoffset, step_offset):
            # Seed the function at the location with the given width
            wave = [vector3d(0,offset+i,0) for i in range(self.rail_track_width)]
            # While we can keep expanding east in this horizontal track
            while wave and wave[0].x < max_xoffset:
                wave = self.route_supply_rail(name, wave, direction.EAST)


        # Vertical supply rails
        max_offset = self.rg.ur.x
        for offset in range(start_offset, max_xoffset, step_offset):
            # Seed the function at the location with the given width
            wave = [vector3d(offset+i,0,1) for i in range(self.rail_track_width)]
            # While we can keep expanding north in this vertical track
            while wave and wave[0].y < max_yoffset:
                wave = self.route_supply_rail(name, wave, direction.NORTH)

        # Remember index of path size which is how many rails we had at the start
        self.num_rails = len(self.paths)

    def route_supply_rail(self, name, seed_wave, direct):
        """
        This finds the first valid starting location and routes a supply rail
        in the given direction.
        It returns the space after the end of the rail to seed another call for multiple
        supply rails in the same "track" when there is a blockage.
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
    

                    
                
        
    def route_pins_to_rails(self,pin_name):
        """
        This will route each of the pin components to the supply rails. 
        After it is done, the cells are added to the pin blockage list.
        """

        # For every component
        for index in range(self.num_pin_components(pin_name)):
            
            # Block all the pin components first
            self.add_component_blockages(pin_name)
            
            # Add the single component of the pin as the source
            # which unmarks it as a blockage too
            self.add_pin_component(pin_name,index,is_source=True)
            
            # Add all of the rails as targets
            # Don't add the other pins, but we could?
            self.add_supply_rail_target(pin_name)

            # Actually run the A* router
            self.run_router(detour_scale=5)
            

            

                
    

    


    
