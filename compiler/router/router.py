import gdsMill
import tech
import math
import debug
from collections import defaultdict

class router:
    """A router class to read an obstruction map from a gds and plan a
    route on a given layer.

    """
    def __init__(self, gdsName, topName, layers):
        """Use the gds file for the blockages with the top module topName and
        layers for the layers to route on

        """
        self.topName = topName
        self.gdsName = gdsName
        self.layout = gdsMill.VlsiLayout(units=tech.GDS["unit"])
        self.reader = gdsMill.Gds2reader(self.layout)
        self.reader.loadFromFile(gdsName)
        self.unit = float(self.layout.info['units'][0])
        self.layers = layers

        self.find_blockages()
    def create_map(self):
        pass

    def find_blockages(self):
        for layer in self.layer:
            debug.info("Layer: " + layer)
            self.writeObstruct(self.topName, layer)

    
    def add_route(self,start, end, layerstack):
        """ Add a wire route from the start to the end point"""

        pass

    def create_steiner_routes(self,pins):
        """Find a set of steiner points and then return the list of
        point-to-point routes."""
        pass

    def find_steiner_points(self,pins):
        """ Find the set of steiner points and return them."""
        pass

        
    def writeObstruct(self, sr, lay, mirr = 1, angle = math.radians(float(0)), xyShift = (0, 0)): 
        """Recursive write boundaries on each Structure in GDS file to LEF"""
        for boundary in self.layout.structures[sr].boundaries:
            coordTrans = self.coordinatesTranslate(boundary.coordinates, mirr, angle, xyShift)
            rect = self.minMaxCoord(coordTrans)
            lay_convert = tech.layer[lay]
            if boundary.drawingLayer == lay_convert:
                text = " RECT "
                for item in rect:
                    text += " {0} {1}".format(item[0]*self.unit, item[1]*self.unit)
                debug.info(text)
               
        for sref in self.layout.structures[sr].srefs:
            sMirr = 1
            if sref.transFlags[0] == True:
                sMirr = -1
            sAngle = math.radians(float(0))
            if sref.rotateAngle:
                sAngle = math.radians(float(sref.rotateAngle))
            sAngle += angle
            x = sref.coordinates[0]
            y = sref.coordinates[1]
            newX = (x)*math.cos(angle) - mirr*(y)*math.sin(angle) + xyShift[0] 
            newY = (x)*math.sin(angle) + mirr*(y)*math.cos(angle) + xyShift[1] 
            sxyShift = (newX, newY)
            self.writeObstruct(sref.sName, lay,sMirr, sAngle, sxyShift)
