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

    def __init__(self, layers, design, gds_filename=None):
        """
        This will route on layers in design. It will get the blockages from
        either the gds file name or the design itself (by saving to a gds file).
        """
        router.__init__(self, layers, design, gds_filename)
        
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
    
    def route(self, vdd_name="vdd", gnd_name="gnd"):
        """ 
        Add power supply rails and connect all pins to these rails.
        """
        debug.info(1,"Running supply router on {0} and {1}...".format(vdd_name, gnd_name))
        self.vdd_name = vdd_name
        self.gnd_name = gnd_name

        # Clear the pins if we have previously routed
        if (hasattr(self,'rg')):
            self.clear_pins()
        else:
            # Creat a routing grid over the entire area
            # FIXME: This could be created only over the routing region,
            # but this is simplest for now.
            self.create_routing_grid()

        # Get the pin shapes
        self.find_pins_and_blockages([self.vdd_name, self.gnd_name])
        
        # Add the supply rails in a mesh network and connect H/V with vias
        # Block everything
        self.prepare_blockages(self.gnd_name)
        # Determine the rail locations
        self.route_supply_rails(self.gnd_name,0)
        
        # Block everything
        self.prepare_blockages(self.vdd_name)
        # Determine the rail locations
        self.route_supply_rails(self.vdd_name,1)
        
        #self.write_debug_gds("pre_pin_debug.gds",stop_program=True)
        
        # Route the supply pins to the supply rails
        self.route_pins_to_rails(gnd_name)
        self.route_pins_to_rails(vdd_name)
        
        #self.write_debug_gds("post_pin_debug.gds",stop_program=False)
        
        return True

        
    def connect_supply_rails(self, name):
        """
        Determine which supply rails overlap and can accomodate a via.
        Remove any supply rails that do not have a via since they are disconnected.
        NOTE: It is still possible though unlikely that there are disconnected groups of rails.
        """
            
        # Split into horizontal and vertical paths
        vertical_rails = [x for x in self.supply_rails if x[0][0].z==1 and x.name==name]
        horizontal_rails = [x for x in self.supply_rails if x[0][0].z==0 and x.name==name]
        
        # Flag to see if each supply rail has at least one via (i.e. it is "connected")
        vertical_flags = [False] * len(vertical_rails)
        horizontal_flags = [False] * len(horizontal_rails)
        
        # Compute a list of "shared areas" that are bigger than a via
        via_areas = []
        for vindex,v in enumerate(vertical_rails):
            for hindex,h in enumerate(horizontal_rails):
                # Compute the overlap of the two paths, None if no overlap
                overlap = v.overlap(h)
                if overlap:
                    (ll,ur) = overlap
                    # We can add a via only if it is a full track width in each dimension
                    if ur.x-ll.x >= self.rail_track_width-1 and ur.y-ll.y >= self.rail_track_width-1:
                        vertical_flags[vindex]=True
                        horizontal_flags[hindex]=True
                        via_areas.append(overlap)

        # Go through and add the vias at the center of the intersection
        for (ll,ur) in via_areas:
            center = (ll + ur).scale(0.5,0.5,0)
            self.add_via(center,self.rail_track_width)

        # Retrieve the original indices into supply_rails for removal
        remove_hrails = [rail for flag,rail in zip(horizontal_flags,horizontal_rails) if not flag]
        remove_vrails = [rail for flag,rail in zip(vertical_flags,vertical_rails) if not flag]
        for rail in remove_hrails + remove_vrails:
            debug.info(1,"Removing disconnected supply rail {}".format(rail))
            self.supply_rails.remove(rail)
        
    def add_supply_rails(self, name):
        """
        Add the shapes that represent the routed supply rails.
        This is after the paths have been pruned and only include rails that are
        connected with vias.
        """
        for wave_path in self.supply_rails:
            if wave_path.name == name:
                self.add_wavepath(name, wave_path)


                
    def route_supply_rails(self, name, supply_number):
        """
        Route the horizontal and vertical supply rails across the entire design.
        Must be done with lower left at 0,0
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
                wave = self.find_supply_rail(name, wave, direction.EAST)


        # Vertical supply rails
        max_offset = self.rg.ur.x
        for offset in range(start_offset, max_xoffset, step_offset):
            # Seed the function at the location with the given width
            wave = [vector3d(offset+i,0,1) for i in range(self.rail_track_width)]
            # While we can keep expanding north in this vertical track
            while wave and wave[0].y < max_yoffset:
                wave = self.find_supply_rail(name, wave, direction.NORTH)

        # Add the supply rail vias (and prune disconnected rails)
        self.connect_supply_rails(name)
        
        # Add the rails themselves
        self.add_supply_rails(name)

    def find_supply_rail(self, name, seed_wave, direct):
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

        # We must have at least 2 tracks to drop plus 2 tracks for a via
        if len(wave_path)>=4*self.rail_track_width:
            # drop the first and last steps to leave escape routing room
            # around the blockage that stopped the probe
            # except, don't drop the first if it is the first in a row/column
            if (direct==direction.NORTH and seed_wave[0].y>0):
                wave_path.trim_first()
            elif (direct == direction.EAST and seed_wave[0].x>0):
                wave_path.trim_first()
                
            wave_path.trim_last()
            wave_path.name = name
            self.supply_rails.append(wave_path)

        # seed the next start wave location
        wave_end = wave_path[-1]
        return wave_path.neighbor(direct)
    

                    
                
        
    def route_pins_to_rails(self, pin_name):
        """
        This will route each of the pin components to the supply rails. 
        After it is done, the cells are added to the pin blockage list.
        """


        num_components = self.num_pin_components(pin_name)
        debug.info(1,"Pin {0} has {1} components to route.".format(pin_name, num_components))

        recent_paths = []
        # For every component
        for index in range(num_components):
            debug.info(2,"Routing component {0} {1}".format(pin_name, index))
            
            self.rg.reinit()
            
            self.prepare_blockages(pin_name)
            
            # Add the single component of the pin as the source
            # which unmarks it as a blockage too
            self.add_pin_component_source(pin_name,index)

            # Add all of the rails as targets
            # Don't add the other pins, but we could?
            self.add_supply_rail_target(pin_name)

            # Add the previous paths as targets too
            #self.add_path_target(recent_paths)

            
            # Actually run the A* router
            if not self.run_router(detour_scale=5):
                self.write_debug_gds()
            
            recent_paths.append(self.paths[-1])

                
    

    


    
