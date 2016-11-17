from PIL import ImageColor

class cell:
    """
    A single cell that can be occupied in a given layer, blocked,
    visited, etc.
    """
    def __init__(self):
        self.path = False

        self.blocked = False

        self.source = False
        self.target = False


    def get_color(self):

        # Blues are horizontal
        if self.blocked:
            return ImageColor.getrgb("Green")
        # Reds are source/sink    
        if self.source or self.target:
            return ImageColor.getrgb("Red")

        if self.path:
            return ImageColor.getrgb("Blue")

        return [255,255,255]
            
            
