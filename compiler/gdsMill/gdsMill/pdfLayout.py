import math
import random
from numpy import matrix
from openram.gdsMill import pyx
from .gdsPrimitives import *

class pdfLayout:
    """Class representing a view for a layout as a PDF"""
    def __init__(self,theLayout):
        self.canvas = pyx.canvas.canvas()
        self.layout = theLayout
        self.layerColors=dict()
        self.scale = 1.0

    def setScale(self,newScale):
        self.scale = float(newScale)

    def hexToRgb(self,hexColor):
        """
        Takes a hexadecimal color string i.e. "#219E1C" and converts it to an rgb float triplet ranging 0->1
        """
        red = int(hexColor[1:3],16)
        green = int(hexColor[3:5],16)
        blue = int(hexColor[5:7],16)
        return (float(red)/255,float(green)/255,float(blue)/255)

    def randomHexColor(self):
        """
        Generates a random color in hex using the format #ABC123
        """
        red = hex(random.randint(0,255)).lstrip("0x")
        green = hex(random.randint(0,255)).lstrip("0x")
        blue = hex(random.randint(0,255)).lstrip("0x")
        return "#"+red+green+blue

    def transformCoordinates(self,uvCoordinates,origin,uVector,vVector):
        """
        This helper method will convert coordinates from a UV space to the cartesian XY space
        """
        xyCoordinates = []
        #setup a translation matrix
        tMatrix = matrix([[1.0,0.0,origin[0]],[0.0,1.0,origin[1]],[0.0,0.0,1.0]])
        #and a rotation matrix
        rMatrix = matrix([[uVector[0],vVector[0],0.0],[uVector[1],vVector[1],0.0],[0.0,0.0,1.0]])
        for coordinate in uvCoordinates:
            #grab the point in UV space
            uvPoint = matrix([coordinate[0],coordinate[1],1.0])
            #now rotate and translate it back to XY space
            xyPoint = rMatrix * uvPoint
            xyPoint = tMatrix * xyPoint
            xyCoordinates += [(xyPoint[0],xyPoint[1])]
        return xyCoordinates

    def drawBoundary(self,boundary,origin,uVector,vVector):
        #get the coordinates in the correct coordinate space
        coordinates = self.transformCoordinates(boundary.coordinates,origin,uVector,vVector)
        #method to draw a boundary with an XY offset
        x=(coordinates[0][0])/self.scale
        y=(coordinates[0][1])/self.scale
        shape = pyx.path.path(pyx.path.moveto(x, y))
        for index in range(1,len(coordinates)):
            x=(coordinates[index][0])/self.scale
            y=(coordinates[index][1])/self.scale
            shape.append(pyx.path.lineto(x,y))
        self.canvas.stroke(shape, [pyx.style.linewidth.thick])
        if(boundary.drawingLayer in self.layerColors):
            layerColor = self.hexToRgb(self.layerColors[boundary.drawingLayer])
            self.canvas.fill(shape, [pyx.color.rgb(layerColor[0],layerColor[1],layerColor[2]), pyx.color.transparency(0.5)])

    def drawPath(self,path,origin,uVector,vVector):
        #method to draw a path with an XY offset
        boundaryCoordinates = self.transformCoordinates(path.equivalentBoundaryCoordinates(),origin,uVector,vVector)
        shape = pyx.path.path(pyx.path.moveto((boundaryCoordinates[0][0])/self.scale,(boundaryCoordinates[0][1])/self.scale))
        for coordinate in boundaryCoordinates[1::]:
            shape.append(pyx.path.lineto((coordinate[0])/self.scale,(coordinate[1])/self.scale))
        self.canvas.stroke(shape, [pyx.style.linewidth.thick])
        if(path.drawingLayer in self.layerColors):
            layerColor = self.hexToRgb(self.layerColors[path.drawingLayer])
            self.canvas.fill(shape, [pyx.color.rgb(layerColor[0],layerColor[1],layerColor[2]), pyx.color.transparency(0.5)])

    def drawLayout(self):
        #use the layout xyTree and structureList
        #to draw ONLY the geometry in each structure
        #SREFS and AREFS are handled in the tree
        for element in self.layout.xyTree:
            #each element is (name,offsetTuple,rotate)
            structureToDraw = self.layout.structures[element[0]]
            for boundary in structureToDraw.boundaries:
                self.drawBoundary(boundary,element[1],element[2], element[3])
            for path in structureToDraw.paths:
                self.drawPath(path,element[1],element[2], element[3])

    def writeToFile(self,filename):
        self.canvas.writePDFfile(filename)
