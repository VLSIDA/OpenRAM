from PIL import ImageColor

class cell:
    """
    A single cell that can be occupied in a given layer, blocked,
    visited, etc.
    """
    scale=1
    
    def __init__(self):
        self.visited = 0

        self.blocked = False

        self.is_source = False
        self.is_target = False


    def get_color(self):

        # Blues are horizontal
        if self.blocked:
            return ImageColor.getrgb("Blue")
        # Reds are source/sink    
        if self.is_source or self.is_target:
            return ImageColor.getrgb("Red")

        if self.visited>0:
            return [255-min(int(self.visited/cell.scale * 255),255)] * 3

        return [255,255,255]
            
            
