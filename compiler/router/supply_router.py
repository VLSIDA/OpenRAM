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
        self.prepare_blockages()
        # Clear the rail we're routing
        self.set_blockages(self.pin_components[self.gnd_name],False)
        # Determine the rail locations
        self.route_supply_rails(self.gnd_name,0)
        
        # Block everything
        self.prepare_blockages()
        # Clear the rail we're routing
        self.set_blockages(self.pin_components[self.vdd_name],False)
        # Determine the rail locations
        self.route_supply_rails(self.vdd_name,1)


        # Route the supply pins to the supply rails
        self.route_pins_to_rails(gnd_name)
        self.route_pins_to_rails(vdd_name)
        
        self.write_debug_gds(stop_program=False)
        return True

        
    def connect_supply_rails(self, name):
        """
        Determine which supply rails overlap and can accomodate a via.
        Remove any paths that do not have a via since they are disconnected.
        """
            
        # Split into horizontal and vertical
        vertical_paths = [(i,x) for i,x in enumerate(self.supply_rails) if x[0][0].z==1 and x.name==name]
        horizontal_paths = [(i,x) for i,x in enumerate(self.supply_rails) if x[0][0].z==0 and x.name==name]
        
        # Flag to see if the paths have a via
        via_flag = [False] * len(self.supply_rails)
        # Ignore the other nets that we aren't considering
        for i,p in enumerate(self.supply_rails):
            if p.name != name:
                via_flag[i]=True
        
        # Compute a list of "shared areas" that are bigger than a via
        via_areas = []
        for vindex,v in vertical_paths:
            for hindex,h in horizontal_paths:
                # Compute the overlap of the two paths, None if no overlap
                overlap = v.overlap(h)
                if overlap:
                    (ll,ur) = overlap
                    # We can add a via only if it is a full track width in each dimension
                    if ur.x-ll.x >= self.rail_track_width-1 and ur.y-ll.y >= self.rail_track_width-1:
                        via_flag[vindex]=True
                        via_flag[hindex]=True
                        via_areas.append(overlap)


        # Go through and add the vias at the center of the intersection
        for (ll,ur) in via_areas:
            center = (ll + ur).scale(0.5,0.5,0)
            self.add_via(center,self.rail_track_width)

        # Remove the paths that have not been connected by any via
        remove_indices = [i for i,x in enumerate(via_flag) if not x]
        for index in remove_indices:
            debug.info(1,"Removing disconnected supply rail {}".format(self.supply_rails[index]))
            del self.supply_rails[index]
        
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

        if len(wave_path)>=2*self.rail_track_width:
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
        
        # For every component
        for index in range(num_components):
            debug.info(2,"Routing component {0} {1}".format(pin_name, index))
            
            self.rg.reinit()
            
            self.prepare_blockages()

            # Add the single component of the pin as the source
            # which unmarks it as a blockage too
            self.add_pin_component_source(pin_name,index)

            # Add all of the rails as targets
            # Don't add the other pins, but we could?
            self.add_supply_rail_target(pin_name)
            
            # Actually run the A* router
            if not self.run_router(detour_scale=5):
                self.write_debug_gds()
            

                
    

    


    
