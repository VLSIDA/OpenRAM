import gdsMill
import tech
from contact import contact
import math
import debug
from globals import OPTS
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
        

        # The list of supply rails that may be routed
        self.supply_rails = []
        # This is the same as above but the sets of pins
        self.supply_rail_tracks = {}
        self.supply_rail_wire_tracks = {}        
        
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

        #self.write_debug_gds("pin_enclosures.gds",stop_program=True)

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
        remaining_vdd_pin_indices = self.route_simple_overlaps(vdd_name)
        remaining_gnd_pin_indices = self.route_simple_overlaps(gnd_name)
        
        # Route the supply pins to the supply rails
        # Route vdd first since we want it to be shorter
        self.route_pins_to_rails(vdd_name, remaining_vdd_pin_indices)
        self.route_pins_to_rails(gnd_name, remaining_gnd_pin_indices)
        
        self.write_debug_gds("post_pin_debug.gds",stop_program=False)
        
        return True


                
                
    
    def route_simple_overlaps(self, pin_name):
        """
        This checks for simple cases where a pin component already overlaps a supply rail.
        It will add an enclosure to ensure the overlap in wide DRC rule cases.
        """
        num_components = self.num_pin_components(pin_name)
        remaining_pins = []
        supply_tracks = self.supply_rail_tracks[pin_name]

        for index in range(num_components):
            pin_in_tracks = self.pin_grids[pin_name][index]
            common_set = supply_tracks & pin_in_tracks

            if len(common_set)==0:
                # if no overlap, add it to the complex route pins
                remaining_pins.append(index)
            else:
                print("Overlap!",index)
                self.create_simple_overlap_enclosure(pin_name, common_set)
            
        return remaining_pins

    def recurse_simple_overlap_enclosure(self, pin_name, start_set, direct):
        """
        Recursive function to return set of tracks that connects to
        the actual supply rail wire in a given direction (or terminating
        when any track is no longer in the supply rail.
        """
        import grid_utils
        next_set = grid_utils.expand_border(start_set, direct)

        supply_tracks = self.supply_rail_tracks[pin_name]
        supply_wire_tracks = self.supply_rail_wire_tracks[pin_name]
        
        supply_overlap = next_set & supply_tracks
        wire_overlap = next_set & supply_wire_tracks

        print("EXAMINING: ",start_set,len(start_set),len(supply_overlap),len(wire_overlap),direct)
        # If the rail overlap is the same, we are done, since we connected to the actual wire
        if len(wire_overlap)==len(start_set):
            print("HIT RAIL", wire_overlap)
            new_set = start_set | wire_overlap
        # If the supply overlap is the same, keep expanding unti we hit the wire or move out of the rail region
        elif len(supply_overlap)==len(start_set):
            print("RECURSE", supply_overlap)
            recurse_set = self.recurse_simple_overlap_enclosure(pin_name, supply_overlap, direct)
            new_set = start_set | supply_overlap | recurse_set
        else:
            # If we got no next set, we are done, can't expand!
            print("NO MORE OVERLAP", supply_overlap)
            new_set = set()
            
        return new_set
            
    def create_simple_overlap_enclosure(self, pin_name, start_set):
        """
        This takes a set of tracks that overlap a supply rail and creates an enclosure
        that is ensured to overlap the supply rail wire.
        It then adds rectangle(s) for the enclosure.
        """
        import grid_utils

        additional_set = set()
        # Check the layer of any element in the pin to determine which direction to route it
        e = next(iter(start_set))
        new_set = start_set.copy()
        if e.z==0:
            new_set = self.recurse_simple_overlap_enclosure(pin_name, start_set, direction.NORTH)
            if not new_set:
                new_set = self.recurse_simple_overlap_enclosure(pin_name, start_set, direction.SOUTH)
        else:
            new_set = self.recurse_simple_overlap_enclosure(pin_name, start_set, direction.EAST)
            if not new_set:
                new_set = self.recurse_simple_overlap_enclosure(pin_name, start_set, direction.WEST)

        enclosure_list = self.compute_enclosures(new_set)
        for pin in enclosure_list:
            debug.info(2,"Adding simple overlap enclosure {0} {1}".format(pin_name, pin))
            self.cell.add_rect(layer=pin.layer,
                               offset=pin.ll(),
                               width=pin.width(),
                               height=pin.height())



    
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
            debug.info(1,"Removing disconnected supply rail {0} .. {1}".format(rail[0][0],rail[-1][-1]))
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

    def compute_supply_rail_dimensions(self):
        """
        Compute the supply rail dimensions including wide metal spacing rules.
        """
        
        self.max_yoffset = self.rg.ur.y
        self.max_xoffset = self.rg.ur.x

        # Longest length is conservative
        rail_length = max(self.max_yoffset,self.max_xoffset)
        # Convert the number of tracks to dimensions to get the design rule spacing
        rail_width = self.track_width*self.rail_track_width

        # Get the conservative width and spacing of the top rails
        (horizontal_width, horizontal_space) = self.get_layer_width_space(0, rail_width, rail_length)
        (vertical_width, vertical_space) = self.get_layer_width_space(1, rail_width, rail_length)
        width = max(horizontal_width, vertical_width)
        space = max(horizontal_space, vertical_space)
        
        # This is the supply rail pitch in terms of routing grids
        # i.e. a rail of self.rail_track_width needs this many tracks including
        # space
        track_pitch = self.rail_track_width*width + space

        # Determine the pitch (in tracks) of the rail wire + spacing
        self.supply_rail_width = math.ceil(track_pitch/self.track_width)
        debug.info(1,"Rail step: {}".format(self.supply_rail_width))
        
        # Conservatively determine the number of tracks that the rail actually occupies
        space_tracks = math.ceil(space/self.track_width)
        self.supply_rail_wire_width = self.supply_rail_width - space_tracks
        debug.info(1,"Rail wire tracks: {}".format(self.supply_rail_wire_width))
        total_space = self.supply_rail_width - self.supply_rail_wire_width
        debug.check(total_space % 2 == 0, "Asymmetric wire track spacing...")
        self.supply_rail_space_width = int(0.5*total_space)
        debug.info(1,"Rail space tracks: {} (on both sides)".format(self.supply_rail_space_width))


    def compute_supply_rails(self, name, supply_number):
        """
        Compute the unblocked locations for the horizontal and vertical supply rails.
        Go in a raster order from bottom to the top (for horizontal) and left to right
        (for vertical). Start with an initial start_offset in x and y direction.
        """
        start_offset = supply_number*self.supply_rail_width

        # Horizontal supply rails
        for offset in range(start_offset, self.max_yoffset, 2*self.supply_rail_width):
            # Seed the function at the location with the given width
            wave = [vector3d(0,offset+i,0) for i in range(self.supply_rail_width)]
            # While we can keep expanding east in this horizontal track
            while wave and wave[0].x < self.max_xoffset:
                wave = self.find_supply_rail(name, wave, direction.EAST)


        # Vertical supply rails
        max_offset = self.rg.ur.x
        for offset in range(start_offset, self.max_xoffset, 2*self.supply_rail_width):
            # Seed the function at the location with the given width
            wave = [vector3d(offset+i,0,1) for i in range(self.supply_rail_width)]
            # While we can keep expanding north in this vertical track
            while wave and wave[0].y < self.max_yoffset:
                wave = self.find_supply_rail(name, wave, direction.NORTH)

                
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
    

                    
                
    def route_supply_rails(self, name, supply_number):
        """
        Route the horizontal and vertical supply rails across the entire design.
        Must be done with lower left at 0,0
        """

        # Compute the grid dimensions
        self.compute_supply_rail_dimensions()
        
        # Compute the grid locations of the supply rails
        self.compute_supply_rails(name, supply_number)
        
        # Add the supply rail vias (and prune disconnected rails)
        self.connect_supply_rails(name)
        
        # Add the rails themselves
        self.add_supply_rails(name)

        # Make the supply rails into a big giant set of grids
        self.create_supply_track_set(name)
        

    def create_supply_track_set(self, pin_name):
        """
        Take the remaining supply rails and put the middle grids into a set.
        The middle grids will be guaranteed to have the wire.
        FIXME: Do this instead with the supply_rail_pitch and width
        """
        rail_set = set()
        wire_set = set()
        for rail in self.supply_rails:
            if rail.name != pin_name:
                continue
            # FIXME: Select based on self.supply_rail_wire_width and self.supply_rail_width
            start_wire_index = self.supply_rail_space_width
            end_wire_index = self.supply_rail_width - self.supply_rail_space_width 
            for wave_index in range(len(rail)):
                rail_set.update(rail[wave_index])
                wire_set.update(rail[wave_index][start_wire_index:end_wire_index])

        self.supply_rail_tracks[pin_name] = rail_set
        self.supply_rail_wire_tracks[pin_name] = wire_set

                
        
    def route_pins_to_rails(self, pin_name, remaining_component_indices):
        """
        This will route each of the remaining pin components to the supply rails. 
        After it is done, the cells are added to the pin blockage list.
        """

        
        debug.info(1,"Pin {0} has {1} remaining components to route.".format(pin_name,
                                                                             len(remaining_component_indices)))

        recent_paths = []
        # For every component
        for index in remaining_component_indices:
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

            #print(self.rg.target)
            
            # Actually run the A* router
            if not self.run_router(detour_scale=5):
                self.write_debug_gds()
            
            recent_paths.append(self.paths[-1])

    
    def add_supply_rail_target(self, pin_name):
        """
        Add the supply rails of given name as a routing target.
        """
        debug.info(2,"Add supply rail target {}".format(pin_name))
        for rail in self.supply_rails:
            if rail.name != pin_name:
                continue
            # Set the middle track only as the target since wide metal
            # spacings may mean the other grids are actually empty space
            middle_index = math.floor(len(rail[0])/2)
            for wave_index in range(len(rail)):
                pin_in_tracks = rail[wave_index]
                #debug.info(1,"Set target: " + str(pin_name) + " " + str(pin_in_tracks))
                self.rg.set_target(pin_in_tracks[middle_index])
                self.rg.set_blocked(pin_in_tracks,False)

                
    def set_supply_rail_blocked(self, value=True):
        """
        Add the supply rails of given name as a routing target.
        """
        debug.info(3,"Blocking supply rail")        
        for rail in self.supply_rails:
            for wave_index in range(len(rail)):
                pin_in_tracks = rail[wave_index]
                #debug.info(1,"Set target: " + str(pin_name) + " " + str(pin_in_tracks))
                self.rg.set_blocked(pin_in_tracks,value)
                
