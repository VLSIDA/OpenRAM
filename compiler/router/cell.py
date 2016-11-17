from PIL import ImageColor

class cell:
    """
    A single cell that can be occupied in a given layer, blocked,
    visited, etc.
    """
    def __init__(self):
        self.visited = False
        self.path = False
        self.blocked = False
        self.source = False
        self.target = False


    def get_color(self):
        r=g=b=0
        count=0
        # Blues are horizontal
        if self.blocked:
            [r1,g1,b1] = ImageColor.getrgb("Green")
            r+=r1
            g+=g1
            b+=b1
            count+=1

            if self.source or self.target:
            [r1,g1,b1] = ImageColor.getrgb("Red")
            r+=r1
            g+=g1
            b+=b1
            count+=1

        if self.path:
            [r1,g1,b1] = ImageColor.getrgb("Blue")
            r+=r1
            g+=g1
            b+=b1
            count+=1

        if count>0:
            return [int(r/count),int(g/count),int(b/count)]
        else:
            return [255,255,255]
            
            
