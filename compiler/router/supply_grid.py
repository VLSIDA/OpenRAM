import debug
from vector3d import vector3d
import grid


class supply_grid(grid.grid):
    """
    A two layer routing map. Each cell can be blocked in the vertical
    or horizontal layer.
    """

    def __init__(self):
        """ Create a routing map of width x height cells and 2 in the z-axis. """
        grid.grid.__init__(self)
        
        # list of the vdd/gnd rail cells
        self.vdd_rails = []
        self.gnd_rails = []

    def reinit(self):
        """ Reinitialize everything for a new route. """

        # Reset all the cells in the map
        for p in self.map.values():
            p.reset()
        

