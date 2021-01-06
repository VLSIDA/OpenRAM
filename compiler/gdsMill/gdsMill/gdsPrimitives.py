

class GdsStructure:
    """Class represent a GDS Structure Object"""
    def __init__(self):
        self.name=""
        self.createDate=()
        self.modDate=()
        #these are the primitives defined in GDS2, and we will maintain lists of them all
        self.boundaries=[]
        self.paths=[]
        self.srefs=[]
        self.arefs=[]
        self.texts=[]
        self.nodes=[]
        self.boxes=[]

        
class GdsBoundary:
    """Class represent a GDS Boundary Object"""
    def __init__(self):
        self.elementFlags=""
        self.plex=""
        self.drawingLayer=""
        self.purposeLayer=0
        self.coordinates=""

        
class GdsPath:
    """Class represent a GDS Path Object"""
    def __init__(self):
        self.elementFlags=""
        self.plex=""
        self.drawingLayer=""
        self.purposeLayer=0
        self.pathType=""
        self.dataType=None
        self.pathWidth=""
        self.coordinates=""

    def equivalentBoundaryCoordinates(self):
        """Convert the path to a set of boundary coordinates that define it"""
        halfWidth = (self.pathWidth/2)
        lastX = lastY = None  #start of the path
        #go through every point
        #always draw on the "left side of the line"
        #this way, we can append two copies of the coordinates and just trace in order
        # i.e. coordinates are (A,B,C,D) - we just make a new array (A,B,C,D,C,B,A) and trace with a fixed offset to the "left"
        coordinatesCopy = self.coordinates[:]
        coordinatesCopy.reverse()
        coordinates=self.coordinates[:]+coordinatesCopy
        boundaryEquivalent = []
        #create the first point
        x=(coordinates[0][0])
        y=(coordinates[0][1])
        boundaryEquivalent += [(x, y)]
        for index in range(0,len(coordinates)):
            x=(coordinates[index][0])
            y=(coordinates[index][1])
            if index < len(coordinates)-1:
                nextX=(coordinates[index+1][0])
                nextY=(coordinates[index+1][1])
            else: #end of the path b/c no next points
                nextX = None;
                nextY = None;
            if lastX==None:   #start of the path
                if nextX>x:#moving right
                    boundaryEquivalent+=[(x,y+halfWidth)]
                if nextX<x:#moving left
                    boundaryEquivalent+=[(x,y-halfWidth)]
                if nextY>y:#moving up
                    boundaryEquivalent+=[(x-halfWidth,y)]
                if nextY<y:#moving down
                    boundaryEquivalent+=[(x+halfWidth,y)]
            if (nextX != None) and (lastX!=None): #somewhere in the middle
                if (x == lastX and nextX == x) and ((lastY < y) or (nextY > y)):  #vertical line up
                    boundaryEquivalent+=[(x-halfWidth,y)]
                if (x == lastX and nextX == x) and ((lastY > y) or (nextY < y)):  #vertical line down
                    boundaryEquivalent+=[(x+halfWidth,y)]
                if (y == lastY and nextY == y) and ((lastX < x) or (nextX > x)):  #horizontal line right
                    boundaryEquivalent+=[(x,y+halfWidth)]
                if (y == lastY and nextY == y) and ((lastX > x) or (nextX < x)):  #horizontal line left
                    boundaryEquivalent+=[(x,y-halfWidth)]
                ###### TAKE CARE OF THE CORNERS / BENDS HERE - there are 8 types of corners (4 angles * 2 directions)
                if(y < nextY and x < lastX):
                    boundaryEquivalent+=[(x-halfWidth,y-halfWidth)]
                if(y < lastY and x < nextX):
                    boundaryEquivalent+=[(x+halfWidth,y+halfWidth)]
                if(y > nextY and x < lastX):
                    boundaryEquivalent+=[(x+halfWidth,y-halfWidth)]
                if(y > lastY and x < nextX):
                    boundaryEquivalent+=[(x-halfWidth,y+halfWidth)]
                if(y > nextY and x > lastX):
                    boundaryEquivalent+=[(x+halfWidth,y+halfWidth)]
                if(y > lastY and x > nextX):
                    boundaryEquivalent+=[(x-halfWidth,y-halfWidth)]
                if(y < nextY and x > lastX):
                    boundaryEquivalent+=[(x-halfWidth,y+halfWidth)]
                if(y < lastY and x > nextX):
                    boundaryEquivalent+=[(x+halfWidth,y-halfWidth)]

            if nextX == None:   #end of path, put in the last 2 points
                if lastX<x:#moving right
                    boundaryEquivalent+=[(x,y+halfWidth)]
                if lastX>x:#moving left
                    boundaryEquivalent+=[(x,y-halfWidth)]
                if lastY<y:#moving up
                    boundaryEquivalent+=[(x-halfWidth,y)]
                if lastY>y:#moving down
                    boundaryEquivalent+=[(x+halfWidth,y)]
                #return to beginning
                boundaryEquivalent+=[(x,y)]
            lastX = x
            lastY = y
        return boundaryEquivalent

    
class GdsSref:
    """Class represent a GDS structure reference Object"""
    def __init__(self):
        self.elementFlags=""
        self.plex=""
        self.sName=""
        self.transFlags=[0,0,0]
        self.magFactor=""
        self.rotateAngle=""
        self.coordinates=""

        
class GdsAref:
    """Class represent a GDS array reference Object"""
    def __init__(self):
        self.elementFlags=""
        self.plex=""
        self.aName=""
        self.transFlags=[0,0,0]
        self.magFactor=""
        self.rotateAngle=""
        self.coordinates=""

        
class GdsText:
    """Class represent a GDS text Object"""
    def __init__(self):
        self.elementFlags=""
        self.plex=""
        self.drawingLayer=""
        self.purposeLayer=0
        self.transFlags=[0,0,0]
        self.magFactor=""
        self.rotateAngle=""
        self.pathType=""
        self.pathWidth=""
        self.presentationFlags=""
        self.coordinates=""
        self.textString = ""

        
class GdsNode:
    """Class represent a GDS Node Object"""
    def __init__(self):
        self.elementFlags=""
        self.plex=""
        self.drawingLayer=""
        self.nodeType=""
        self.coordinates=""

        
class GdsBox:
    """Class represent a GDS Box Object"""
    def __init__(self):
        self.elementFlags=""
        self.plex=""
        self.drawingLayer=""
        self.purposeLayer=0
        self.boxValue=""
        self.coordinates=""
