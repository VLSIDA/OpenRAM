# See LICENSE for licensing information.
#
#Copyright (c) 2016-2019 Regents of the University of California and The Board
#of Regents for the Oklahoma Agricultural and Mechanical College
#(acting for and on behalf of Oklahoma State University)
#All rights reserved.
#
import gdsMill
import tech
import math
import debug
from globals import OPTS,print_time
from contact import contact
from pin_group import pin_group
from pin_layout import pin_layout
from vector3d import vector3d 
from router import router
from direction import direction
from datetime import datetime
import grid
import grid_utils

class supply_tree_router(router):
    """
    A router class to read an obstruction map from a gds and
    routes a grid to connect the supply on the two layers.
    """

    def __init__(self, layers, design, gds_filename=None):
        """
        This will route on layers in design. It will get the blockages from
        either the gds file name or the design itself (by saving to a gds file).
        """
        # Power rail width in minimum wire widths
        self.rail_track_width = 3
        
        router.__init__(self, layers, design, gds_filename, self.rail_track_width)

        
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
        Route the two nets in a single layer)
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
        start_time = datetime.now()
        self.find_pins_and_blockages([self.vdd_name, self.gnd_name])
        print_time("Finding pins and blockages",datetime.now(), start_time, 3)

        # Add the supply rails in a mesh network and connect H/V with vias
        start_time = datetime.now()
        # Block everything
        self.prepare_blockages(self.gnd_name)
        self.prepare_blockages(self.vdd_name)

        # Route the supply pins to the supply rails
        # Route vdd first since we want it to be shorter
        start_time = datetime.now()
        self.route_pins(vdd_name)
        self.route_pins(gnd_name)
        print_time("Maze routing supplies",datetime.now(), start_time, 3)

        #self.write_debug_gds("final.gds",False)  

        # Did we route everything??
        if not self.check_all_routed(vdd_name):
            return False
        if not self.check_all_routed(gnd_name):
            return False
        
        return True


    def check_all_routed(self, pin_name):
        """ 
        Check that all pin groups are routed.
        """
        for pg in self.pin_groups[pin_name]:
            if not pg.is_routed():
                return False

    def prepare_blockages(self, pin_name):
        """
        Reset and add all of the blockages in the design.
        Names is a list of pins to add as a blockage.
        """
        debug.info(3,"Preparing blockages.")
        
        # Start fresh. Not the best for run-time, but simpler.
        self.clear_blockages()
        # This adds the initial blockges of the design
        #print("BLOCKING:",self.blocked_grids)
        self.set_blockages(self.blocked_grids,True)

        # Block all of the pin components (some will be unblocked if they're a source/target)
        # Also block the previous routes
        for name in self.pin_groups:
            blockage_grids = {y for x in self.pin_groups[name] for y in x.grids}
            self.set_blockages(blockage_grids,True)
            blockage_grids = {y for x in self.pin_groups[name] for y in x.blockages}
            self.set_blockages(blockage_grids,True)

        # FIXME: These duplicate a bit of work
        # These are the paths that have already been routed.
        self.set_blockages(self.path_blockages)

        # Don't mark the other components as targets since we want to route
        # directly to a rail, but unblock all the source components so we can
        # route over them
        blockage_grids = {y for x in self.pin_groups[pin_name] for y in x.grids}
        self.set_blockages(blockage_grids,False)
            

        
    def route_pins(self, pin_name):
        """
        This will route each of the remaining pin components to the other pins.
        After it is done, the cells are added to the pin blockage list.
        """

        remaining_components = sum(not x.is_routed() for x in self.pin_groups[pin_name])
        debug.info(1,"Maze routing {0} with {1} pin components to connect.".format(pin_name,
                                                                                   remaining_components))

        for index,pg in enumerate(self.pin_groups[pin_name]):
            if pg.is_routed():
                continue
            
            debug.info(1,"Routing component {0} {1}".format(pin_name, index))

            # Clear everything in the routing grid.
            self.rg.reinit()

            # This is inefficient since it is non-incremental, but it was
            # easier to debug.
            self.prepare_blockages(pin_name)
            
            # Add the single component of the pin as the source
            # which unmarks it as a blockage too
            self.add_pin_component_source(pin_name,index)
            
            # Marks all pin components except index as target
            self.add_pin_component_target_except(pin_name,index)
            # Add the prevous paths as a target too
            self.add_path_target(self.paths)

            print("SOURCE: ")
            for k,v in self.rg.map.items():
                if v.source:
                    print(k)

            print("TARGET: ")
            for k,v in self.rg.map.items():
                if v.target:
                    print(k)

            import pdb; pdb.set_trace()
            if index==1:
                self.write_debug_gds("debug{}.gds".format(pin_name),False)
                
            # Actually run the A* router
            if not self.run_router(detour_scale=5):
                self.write_debug_gds("debug_route.gds",True)
                
            #if index==3 and pin_name=="vdd":
            #    self.write_debug_gds("route.gds",False)

    

                
                
