# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from .signal_grid import signal_grid
from .grid_path import grid_path


class supply_grid(signal_grid):
    """
    This routes a supply grid. It is derived from a signal grid because it still
    routes the pins to the supply rails using the same routines.
    It has a few extra routines to support "waves" which are multiple track wide
    directional routes (no bends).
    """

    def __init__(self, ll, ur, track_width):
        """ Create a routing map of width x height cells and 2 in the z-axis. """
        signal_grid.__init__(self, ll, ur, track_width)

    def reinit(self):
        """ Reinitialize everything for a new route. """

        self.source = set()
        self.target = set()

        # Reset all the cells in the map
        for p in self.map.values():
            p.reset()

    def find_start_wave(self, wave, direct):
        """
        Finds the first loc  starting at loc and up that is open.
        Returns None if it reaches max size first.
        """
        # Don't expand outside the bounding box
        if wave[0].x > self.ur.x:
            return None
        if wave[-1].y > self.ur.y:
            return None

        while wave and self.is_wave_blocked(wave):
            wf = grid_path(wave)
            wave = wf.neighbor(direct)
            # Bail out if we couldn't increment futher
            if wave[0].x > self.ur.x or wave[-1].y > self.ur.y:
                return None
            # Return a start if it isn't blocked
            if not self.is_wave_blocked(wave):
                return wave

        return wave

    def is_wave_blocked(self, wave):
        """
        Checks if any of the locations are blocked
        """
        for v in wave:
            if self.is_blocked(v):
                return True
        else:
            return False

    def probe(self, wave, direct):
        """
        Expand the wave until there is a blockage and return
        the wave path.
        """
        wave_path = grid_path()
        while wave and not self.is_wave_blocked(wave):
            if wave[0].x > self.ur.x or wave[-1].y > self.ur.y:
                break
            wave_path.append(wave)
            wave = wave_path.neighbor(direct)

        return wave_path
