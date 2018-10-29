"""
Some utility functions for sets of grid cells.
"""

import debug
from direction import direction
from vector3d import vector3d


def increment_set(curset, direct):
        """
        Return the cells incremented in given direction
        """
        offset = direction.get_offset(direct)

        newset = set()
        for c in curset:
            newc = c+offset
            newset.add(newc)

        return newset

def remove_border(curset, direct):
    """ 
    Remove the cells on a given border.
    """
    border = get_border(curset, direct)
    curset.difference_update(border)


def get_upper_right(curset):
    ur = None
    for p in curset:
        if ur == None or (p.x>=ur.x and p.y>=ur.y):
            ur = p
    return ur

def get_lower_left(curset):
    ll = None
    for p in curset:
        if ll == None or (p.x<=ll.x and p.y<=ll.y):
            ll = p
    return ll

def get_border( curset, direct):
        """
        Return the furthest cell(s) in a given direction.
        """
        
        # find direction-most cell(s)
        maxc = []
        if direct==direction.NORTH:
            for c in curset:
                if len(maxc)==0 or c.y>maxc[0].y:
                    maxc = [c]
                elif c.y==maxc[0].y:
                    maxc.append(c)
        elif direct==direct.SOUTH:
            for c in curset:
                if len(maxc)==0 or c.y<maxc[0].y:
                    maxc = [c]
                elif c.y==maxc[0].y:
                    maxc.append(c)
        elif direct==direct.EAST:
            for c in curset:
                if len(maxc)==0 or c.x>maxc[0].x:
                    maxc = [c]
                elif c.x==maxc[0].x:
                    maxc.append(c)
        elif direct==direct.WEST:
            for c in curset:
                if len(maxc)==0 or c.x<maxc[0].x:
                    maxc = [c]
                elif c.x==maxc[0].x:
                    maxc.append(c)

        newset = set(maxc)
        return newset

def expand_border(curset, direct):
        """
        Expand the current set of sells in a given direction.
        Only return the contiguous cells.
        """
        border_set = get_border(curset, direct)
        next_border_set = increment_set(border_set, direct)
        return next_border_set
    
def expand_borders(curset):
    """
    Return the expansions in planar directions.
    """
    north_set=expand_border(curset,direction.NORTH)
    south_set=expand_border(curset,direction.SOUTH)
    east_set=expand_border(curset,direction.EAST)
    west_set=expand_border(curset,direction.WEST)

    return(north_set, east_set, south_set, west_set)

