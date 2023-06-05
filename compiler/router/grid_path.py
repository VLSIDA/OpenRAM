# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from itertools import tee
from openram.base.vector3d import vector3d
from .grid import grid
from .direction import direction


class grid_path:
    """
    A grid path is a list of lists of grid cells.
    It can have a width that is more than one cell.
    All of the sublists will be the same dimension.
    Cells should be continguous.
    It can have a name to define pin shapes as well.
    """

    def __init__(self, items=[], name=""):
        self.name = name
        if items:
            self.pathlist = [items]
        else:
            self.pathlist = []

    def __str__(self):
        p = str(self.pathlist)
        if self.name != "":
            return (str(self.name) + " : " + p)
        return p

    def __setitem__(self, index, value):
        """
        override setitem function
        can set value by pathinstance[index]=value
        """
        self.pathlist[index]=value

    def __getitem__(self, index):
        """
        override getitem function
        can get value by value=pathinstance[index]
        """
        return self.pathlist[index]

    def __contains__(self, key):
        """
        Determine if cell exists in this path
        """
        # FIXME: Could maintain a hash to make in O(1)
        for sublist in self.pathlist:
            for item in sublist:
                if item == key:
                    return True
        else:
            return False

    def __add__(self, items):
        """
        Override add to do append
        """
        return self.pathlist.extend(items)

    def __len__(self):
        return len(self.pathlist)

    def trim_last(self):
        """
        Drop the last item
        """
        if len(self.pathlist)>0:
            self.pathlist.pop()

    def trim_first(self):
        """
        Drop the first item
        """
        if len(self.pathlist)>0:
            self.pathlist.pop(0)

    def append(self,item):
        """
        Append the list of items to the cells
        """
        self.pathlist.append(item)

    def extend(self,item):
        """
        Extend the list of items to the cells
        """
        self.pathlist.extend(item)

    def set_path(self,value=True):
        for sublist in self.pathlist:
            for p in sublist:
                p.path=value

    def set_blocked(self,value=True):
        for sublist in self.pathlist:
            for p in sublist:
                p.blocked=value

    def get_grids(self):
        """
        Return a set of all the grids in this path.
        """
        newset = set()
        for sublist in self.pathlist:
            newset.update(sublist)
        return newset

    def get_wire_grids(self, start_index, end_index):
        """
        Return a set of all the wire grids in this path.
        These are the indices in the wave path in a certain range.
        """
        newset = set()
        for sublist in self.pathlist:
            newset.update(sublist[start_index:end_index])
        return newset

    def cost(self):
        """
        The cost of the path is the length plus a penalty for the number
        of vias. We assume that non-preferred direction is penalized.
        This cost only works with 1 wide tracks.
        """

        # Ignore the source pin layer change, FIXME?
        def pairwise(iterable):
            "s -> (s0,s1), (s1,s2), (s2, s3), ..."
            a, b = tee(iterable)
            next(b, None)
            return zip(a, b)

        plist = list(pairwise(self.pathlist))
        cost = 0
        for p0list,p1list in plist:
            # This is because they are "waves" so pick the first item
            p0=p0list[0]
            p1=p1list[0]

            if p0.z != p1.z: # via
                cost += grid.VIA_COST
            elif p0.x != p1.x and p0.z==1: # horizontal on vertical layer
                cost += grid.NONPREFERRED_COST
            elif p0.y != p1.y and p0.z==0: # vertical on horizontal layer
                cost += grid.NONPREFERRED_COST
            else:
                cost += grid.PREFERRED_COST

        return cost

    def expand_dirs(self):
        """
        Expand from the end in each of the four cardinal directions plus up
        or down but not expanding to blocked cells. Expands in all
        directions regardless of preferred directions.

        If the width is more than one, it can only expand in one direction
        (for now). This is assumed for the supply router for now.

        """
        neighbors = []

        for d in direction.cardinal_directions(True):
            n = self.neighbor(d)
            if n:
                neighbors.append(n)

        return neighbors

    def neighbor(self, d):
        offset = direction.get_offset(d)

        newwave = [point + offset for point in self.pathlist[-1]]

        if newwave in self.pathlist:
            return None
        elif newwave[0].z>1 or newwave[0].z<0:
            return None

        return newwave

    def set_layer(self, zindex):
        new_pathlist = [vector3d(item.x, item.y, zindex) for wave in self.pathlist for item in wave]
        self.pathlist = new_pathlist

    def overlap(self, other):
        """
        Return the overlap waves ignoring different layers
        """

        my_zindex = self.pathlist[0][0].z
        other_flat_cells = [vector3d(item.x,item.y,my_zindex) for wave in other.pathlist for item in wave]
        # This keeps the wave structure of the self layer
        shared_waves = []
        for wave in self.pathlist:
            for item in wave:
                # If any item in the wave is not contained, skip it
                if not item in other_flat_cells:
                    break
            else:
                shared_waves.append(wave)

        if len(shared_waves)>0:
            ll = shared_waves[0][0]
            ur = shared_waves[-1][-1]
            return [ll,ur]
        return None

