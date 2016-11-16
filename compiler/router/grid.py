import numpy as np
from PIL import Image
import debug

from cell import cell
    
class grid:
    """A two layer routing map. Each cell can be blocked in the vertical
    or horizontal layer.

    """

    def __init__(self, width, height):
        """ Create a routing map of width x height cells and 2 in the z-axis. """
        self.width=width
        self.height=height
        self.map={}
        for x in range(width):
            for y in range(height):
                for z in range(2):
                    self.map[x,y,z]=cell()

    def view(self,):
        """
        View the data by creating an RGB array and mapping the data
        structure to the RGB color palette.
        """

        v_map = np.zeros((self.width,self.height,3), 'uint8')
        mid_map = np.ones((25,self.height,3), 'uint8')        
        h_map = np.ones((self.width,self.height,3), 'uint8')        

        # We shouldn't have a path greater than 50% the HPWL
        # so scale all visited indices by this value for colorization
        cell.scale = 1.5 * (self.width+self.height)
        for x in range(self.width):
            for y in range(self.height):
                h_map[x,y] = self.map[x,y,0].get_color()
                v_map[x,y] = self.map[x,y,1].get_color()
        
        v_img = Image.fromarray(v_map, 'RGB').rotate(90)
        mid_img = Image.fromarray(mid_map, 'RGB').rotate(90)
        h_img = Image.fromarray(h_map, 'RGB').rotate(90)

        # concatenate them into a plot with the two layers
        img = Image.new('RGB', (2*self.width+25, self.height))
        img.paste(h_img, (0,0))
        img.paste(mid_img, (self.width,0))        
        img.paste(v_img, (self.width+25,0))
        img.show()

    def set_property(self,ll,ur,z,name,value=True):
        for x in range(int(ll[0]),int(ur[0])):
            for y in range(int(ll[1]),int(ur[1])):
                setattr (self.map[x,y,z], name, True)            

    def add_blockage(self,ll,ur,z):
        debug.info(1,"Adding blockage ll={0} ur={1} z={2}".format(str(ll),str(ur),z))
        self.set_property(ll,ur,z,"blocked")

    def set_source(self,ll,ur,z):
        debug.info(1,"Adding source ll={0} ur={1} z={2}".format(str(ll),str(ur),z))
        self.set_property(ll,ur,z,"is_source")

    def set_target(self,ll,ur,z):
        debug.info(1,"Adding target ll={0} ur={1} z={2}".format(str(ll),str(ur),z))
        self.set_property(ll,ur,z,"is_target")
        
