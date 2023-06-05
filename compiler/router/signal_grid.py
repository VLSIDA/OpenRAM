# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from copy import deepcopy
from heapq import heappush,heappop
from openram import debug
from openram.base.vector3d import vector3d
from .grid import grid
from .grid_path import grid_path


class signal_grid(grid):
    """
    Expand the two layer grid to include A* search functions for a source and target.
    """

    def __init__(self, ll, ur, track_factor):
        """ Create a routing map of width x height cells and 2 in the z-axis. """
        grid.__init__(self, ll, ur, track_factor)

    def reinit(self):
        """ Reinitialize everything for a new route. """

        # Reset all the cells in the map
        for p in self.map.values():
            p.reset()

        self.clear_source()
        self.clear_target()

    def init_queue(self):
        """
        Populate the queue with all the source pins with cost
        to the target. Each item is a path of the grid cells.
        We will use an A* search, so this cost must be pessimistic.
        Cost so far will be the length of the path.
        """
        # Counter is used to not require data comparison in Python 3.x
        # Items will be returned in order they are added during cost ties
        self.q = []
        self.counter = 0
        for s in self.source:
            cost = self.cost_to_target(s)
            debug.info(3, "Init: cost=" + str(cost) + " " + str([s]))
            heappush(self.q, (cost, self.counter, grid_path([vector3d(s)])))
            self.counter += 1

    def route(self, detour_scale):
        """
        This does the A* maze routing with preferred direction routing.
        This only works for 1 track wide routes!
        """

        # We set a cost bound of the HPWL for run-time. This can be
        # over-ridden if the route fails due to pruning a feasible solution.
        any_source_element = next(iter(self.source))
        cost_bound = detour_scale * self.cost_to_target(any_source_element) * grid.PREFERRED_COST

        # Check if something in the queue is already a source and a target!
        for s in self.source:
            if self.is_target(s):
                return((grid_path([vector3d(s)]), 0))

        # Put the source items into the queue
        self.init_queue()

        # Keep expanding and adding to the priority queue until we are done
        while len(self.q)>0:
            # should we keep the path in the queue as well or just the final node?
            (cost, count, curpath) = heappop(self.q)
            debug.info(3, "Queue size: size=" + str(len(self.q)) + " " + str(cost))
            debug.info(4, "Expanding: cost=" + str(cost) + " " + str(curpath))

            # expand the last element
            neighbors =  self.expand_dirs(curpath)
            debug.info(4, "Neighbors: " + str(neighbors))

            for n in neighbors:
                # make a new copy of the path to not update the old ones
                newpath = deepcopy(curpath)
                # node is added to the map by the expand routine
                newpath.append(n)
                # check if we hit the target and are done
                if self.is_target(n[0]): # This uses the [0] item because we are assuming 1-track wide
                    return (newpath, newpath.cost())
                else:
                    # current path cost + predicted cost
                    current_cost = newpath.cost()
                    target_cost = self.cost_to_target(n[0])
                    predicted_cost = current_cost +  target_cost
                    # only add the cost if it is less than our bound
                    if (predicted_cost < cost_bound):
                        if (self.map[n[0]].min_cost==-1 or predicted_cost<self.map[n[0]].min_cost):
                            self.map[n[0]].min_path = newpath
                            self.map[n[0]].min_cost = predicted_cost
                            debug.info(4, "Enqueuing: cost=" + str(current_cost) + "+" + str(target_cost) + " " + str(newpath))
                            # add the cost to get to this point if we haven't reached it yet
                            heappush(self.q, (predicted_cost, self.counter, newpath))
                            self.counter += 1
                        #else:
                        #    print("Better previous cost.")
                    #else:
                    #    print("Cost bounded")

        return (None, None)

    def expand_dirs(self, curpath):
        """
        Expand each of the four cardinal directions plus up or down
        but not expanding to blocked cells. Expands in all directions
        regardless of preferred directions.
        """

        # Expand all directions.
        neighbors = curpath.expand_dirs()

        # Filter the out of region ones
        # Filter the blocked ones
        valid_neighbors = [x for x in neighbors if self.is_inside(x) and not self.is_blocked(x)]

        return valid_neighbors

    def hpwl(self, src, dest):
        """
        Return half perimeter wire length from point to another.
        Either point can have positive or negative coordinates.
        Include the via penalty if there is one.
        """
        hpwl = abs(src.x - dest.x)
        hpwl += abs(src.y - dest.y)
        if src.x!=dest.x and src.y!=dest.y:
            hpwl += grid.VIA_COST
        return hpwl

    def cost_to_target(self, source):
        """
        Find the cheapest HPWL distance to any target point ignoring
        blockages for A* search.
        """
        any_target_element = next(iter(self.target))
        cost = self.hpwl(source, any_target_element)
        for t in self.target:
            cost = min(self.hpwl(source, t), cost)

        return cost

    def get_inertia(self, p0, p1):
        """
        Sets the direction based on the previous direction we came from.
        """
        # direction (index) of movement
        if p0.x==p1.x:
            return 1
        elif p0.y==p1.y:
            return 0
        else:
            # z direction
            return 2



