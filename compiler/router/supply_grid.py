import debug
from vector3d import vector3d
import grid


class supply_grid(grid.grid):
    """
    A two layer routing map. Each cell can be blocked in the vertical
    or horizontal layer.
    """

    def __init__(self, ll, ur, track_width):
        """ Create a routing map of width x height cells and 2 in the z-axis. """
        grid.grid.__init__(self, ll, ur, track_width)
        
        # Current rail
        self.rail = []

    def reinit(self):
        """ Reinitialize everything for a new route. """

        # Reset all the cells in the map
        for p in self.map.values():
            p.reset()
        

    def find_horizontal_start_wave(self, loc, width):
        """ 
        Finds the first loc  starting at loc and to the right that is open.
        Returns None if it reaches max size first.
        """
        wave = [loc+vector3d(0,i,0) for i in range(width)]
        self.width = width

        # Don't expand outside the bounding box
        if wave[0].y > self.ur.y:
            return None

        # Increment while the wave is blocked
        if self.is_wave_blocked(wave):
            while wave:
                wave=self.increment_east_wave(wave)
                if not self.is_wave_blocked(wave):
                    return wave
                
        # This may return None
        return wave

    def find_vertical_start_wave(self, loc, width):
        """ 
        Finds the first loc  starting at loc and up that is open.
        Returns None if it reaches max size first.
        """
        wave = [loc+vector3d(i,0,1) for i in range(width)]
        self.width = width

        # Don't expand outside the bounding box
        if wave[0].x > self.ur.x:
            return None

        # Increment while the wave is blocked
        if self.is_wave_blocked(wave):
            while wave:
                wave=self.increment_up_wave(wave)
                if not self.is_wave_blocked(wave):
                    return wave
                
        # This may return None
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


    
    def increment_east_wave(self, wave):
        """ 
        Increment the head by moving one step right. Return
        new wave if successful.
        """
        new_wave = [v+vector3d(1,0,0) for v in wave]

        # Don't expand outside the bounding box
        if new_wave[0].x>self.ur.x:
            return None
        
        return new_wave

    def increment_up_wave(self, wave):
        """ 
        Increment the head by moving one step up. Return
        new wave if successful.
        """
        new_wave = [v+vector3d(0,1,0) for v in wave]

        # Don't expand outside the bounding box
        if new_wave[0].y>self.ur.y:
            return None
        
        return new_wave
    
    def probe_east_wave(self, wave):
        """
        Expand the wave until there is a blockage and return
        the wave path.
        """
        wave_path = []
        while wave and not self.is_wave_blocked(wave):
            wave_path.append(wave)
            wave = self.increment_east_wave(wave)

        return wave_path

    def probe_up_wave(self, wave):
        """
        Expand the wave until there is a blockage and return
        the wave path.
        """
        wave_path = []
        while wave and not self.is_wave_blocked(wave):
            wave_path.append(wave)
            wave = self.increment_up_wave(wave)

        return wave_path
    
