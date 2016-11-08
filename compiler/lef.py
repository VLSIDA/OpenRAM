import gdsMill
import tech
import globals
import math
import debug
from collections import defaultdict

class lef:
    """
    SRAM LEF Class open GDS file, read pins information, obstruction
    and write them to LEF file
    """
    def __init__(self, gdsName, lefName, sr):
        self.gdsName = gdsName
        self.lef  = open(lefName,"w")
        self.sr = sr
        self.myLayout = gdsMill.VlsiLayout(units=tech.GDS["unit"])
        self.reader = gdsMill.Gds2reader(self.myLayout)
        self.reader.loadFromFile(gdsName)
        self.unit = float(self.myLayout.info['units'][0])
        self.layer = ["metal1", "via1", "metal2", "via2", "metal3"]   
        
        self.create()

        self.lef.close()

    def create(self):
        """Write to LEF file"""
        power_pin_name = self.powerPinName()
        ground_pin_name = self.groundPinName()
        input_pin_name = self.inputPinName()
        inout_pin_name = self.inoutPinName()
        
        self.writeLefHeader() 
        
        for pin in power_pin_name:
          self.writePin(pin, 1)

        for pin in ground_pin_name:
          self.writePin(pin, 2)   
                    
        for pin in inout_pin_name:
          self.writePin(pin, 3)
            
        for pin in input_pin_name:
           self.writePin(pin,4)
            
        self.lef.write("    OBS \n")
        for lay in self.layer:
            self.lef.write("        Layer  {0} ; \n".format(lay))
            self.writeObstruct(self.sr.name, lay, mirr = 1, angle = math.radians(float(0)), xyShift = (0, 0))
        self.lef.write("    END \n")

        self.writeLefFooter()
       
    def coordinatesTranslate(self, coord, mirr, angle, xyShift):
        """Calculate coordinates after flip, rotate, and shift"""
        coordinate = []
        for item in coord:
            x = (item[0]*math.cos(angle)-item[1]*mirr*math.sin(angle)+xyShift[0])
            y = (item[0]*math.sin(angle)+item[1]*mirr*math.cos(angle)+xyShift[1])
            coordinate += [(x, y)]
        return coordinate
                
    def writeObstruct(self, sr, lay, mirr = 1, angle = math.radians(float(0)), xyShift = (0, 0)): 
        """Recursive write boundaries on each Structure in GDS file to LEF"""
        for boundary in self.myLayout.structures[sr].boundaries:
            coordTrans = self.coordinatesTranslate(boundary.coordinates, mirr, angle, xyShift)
            rect = self.minMaxCoord(coordTrans)
            lay_convert = tech.layer[lay]
            if boundary.drawingLayer == lay_convert:
                self.lef.write("        RECT ") 
                for item in rect:
                    self.lef.write(" {0} {1}".format(item[0]*self.unit, item[1]*self.unit))
                self.lef.write(" ;\n")
               
        for sref in self.myLayout.structures[sr].srefs:
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

    def writePinCoord(self, sr, pinName, pinLayer, pinCoord, mirr = 1,
                      angle = math.radians(float(0)), xyShift = (0, 0)): 
        """Write PIN information to LEF"""
        for boundary in self.myLayout.structures[sr].boundaries:
            if (pinLayer == boundary.drawingLayer):
                coordTrans = self.coordinatesTranslate(boundary.coordinates, mirr, angle, xyShift)
                rect = self.minMaxCoord(coordTrans)
                if self.pointInsideRect(pinCoord, rect):
                    self.lef.write("        RECT ") 
                    for item in rect:
                         self.lef.write(" {0} {1}".format(item[0]*self.unit, item[1]*self.unit))
                    self.lef.write(" ;\n")

        for sref in self.myLayout.structures[sr].srefs:
            sMirr = 1
            if sref.transFlags[0] == True:
                sMirr = -1
            sAngle = math.radians(float(0))
            if sref.rotateAngle:
                sAngle = math.radians(float(sref.rotateAngle))
            sAngle += angle
            x = sref.coordinates[0]
            y = sref.coordinates[1]
            newX = (x*math.cos(angle) - mirr*y*math.sin(angle)) + xyShift[0] 
            newY = (x*math.sin(angle) + mirr*y*math.cos(angle)) + xyShift[1] 
            sxyShift = (newX, newY)
            self.writePinCoord(sref.sName, pinName, pinLayer, pinCoord, sMirr, sAngle, sxyShift)
    
    def pinLayerCoord(self, sr, pinName):
        """Get Pin Layer and Coordinates {layer:[coord1, coord2, ...]}"""
        layCoord = defaultdict(list)
        for text in self.myLayout.structures[self.sr.name].texts:
            if text.textString.strip('\x00') == pinName: 
                k = text.drawingLayer
                v = text.coordinates
                d = {k: v}
                layCoord.setdefault(k, []).append(v)
        return layCoord
                    
    def minMaxCoord(self, coordTrans):
        """Find the lowest and highest conner of a Rectangle"""
        coordinate = []
        minx = min(coordTrans[0][0], coordTrans[1][0], coordTrans[2][0], coordTrans[3][0])
        maxx = max(coordTrans[0][0], coordTrans[1][0], coordTrans[2][0], coordTrans[3][0])
        miny = min(coordTrans[0][1], coordTrans[1][1], coordTrans[2][1], coordTrans[3][1])
        maxy = max(coordTrans[0][1], coordTrans[1][1], coordTrans[2][1], coordTrans[3][1])
        coordinate += [(minx, miny)]
        coordinate += [(maxx, maxy)]
        return coordinate

    def pointInsideRect(self, p, rect):
        """Check if a point is inside a rectangle"""
        inside = False
        if ((p[0][0] >= rect[0][0])& (p[0][0] <= rect[1][0])
            & (p[0][1] >= rect[0][1]) &(p[0][1] <= rect[1][1])):
            inside = not inside
        return inside

    def writeLefHeader(self):
        """Heafer of LEF file"""
        coord = self.lowestLeftCorner(self.sr.name, 1, 0.0, (0, 0), [], [], [], [])
        self.lef.write("MACRO {0}\n".format(self.sr.name))
        self.lef.write("    CLASS RING ;\n")
        self.lef.write("    ORIGIN {0} {1} ;\n".format(-coord[0][0]*self.unit, coord[0][1]*self.unit))
        self.lef.write("    FOREIGN  sram {0} {1} ;\n"
                           .format(0.0, 0.0))
        self.lef.write("    SIZE {0} BY {1} ;\n"
                           .format(self.sr.width, self.sr.height))
        self.lef.write("    SYMMETRY X Y R90 ;\n")

    def writeLefFooter(self):
        self.lef.write("END    {0} \n".format(self.sr.name))
        self.lef.write("END    LIBRARY \n")
        
    def powerPinName(self):
        return ["vdd"]

    def groundPinName(self):
        return ["gnd"]
        
    def inputPinName(self):
        input_pin_name = []
        for i in range(self.sr.addr_size + int(math.log(self.sr.num_banks, 2))):
            input_pin_name.append("ADDR[{0}]".format(i))
        input_pin_name.append("CSb")
        input_pin_name.append("OEb")
        input_pin_name.append("WEb")
        input_pin_name.append("clk")
        return input_pin_name
        
    def inoutPinName(self):
        inout_pin_name = []
        for i in range(self.sr.word_size):
            inout_pin_name.append("DATA[{0}]".format(i))
            
        return inout_pin_name
        
    def writePin(self, pinName, typ):
        self.lef.write("    PIN {0} \n".format(pinName))
        if typ == 1:
            self.lef.write("        DIRECTION INOUT ; \n")
            self.lef.write("        USE POWER ; \n")
            self.lef.write("        SHAPE ABUTMENT ; \n")
            self.lef.write("        PORT             \n")
        elif typ == 2:
            self.lef.write("        DIRECTION INOUT ; \n")
            self.lef.write("        USE GROUND ; \n")
            self.lef.write("        SHAPE ABUTMENT ; \n")
            self.lef.write("        PORT             \n")
        elif typ == 3:
            self.lef.write("        DIRECTION INOUT ; \n")
            self.lef.write("        PORT             \n")
        elif typ == 4:
            self.lef.write("        DIRECTION INPUT ; \n")
            self.lef.write("        PORT             \n")
        else:
            debug.error("Invalid pin type on pin {0}".format(pinName))

        pin_layer_coord = self.pinLayerCoord(self.sr.name, pinName)
        for pinLayer in pin_layer_coord:
            lay = [key for key, value in tech.layer.iteritems() if value == pinLayer][0]
            self.lef.write("        Layer {0} ; \n".format(lay))
            for pinCoord in pin_layer_coord[pinLayer]:
                self.writePinCoord(self.sr.name, pinName, pinLayer, pinCoord,
                                   mirr = 1,angle = math.radians(float(0)), xyShift = (0, 0))
        self.lef.write("        END             \n")
        self.lef.write("    END {0} \n".format(pinName))

    def lowestLeftCorner(self, sr, mirr = 1, angle = math.radians(float(0)), xyShift = (0, 0), listMinX = [], listMinY = [], listMaxX = [], listMaxY =[]): 
        """Recursive find a lowest left conner on each Structure in GDS file"""
        for boundary in self.myLayout.structures[sr].boundaries:
            coordTrans = self.coordinatesTranslate(boundary.coordinates, mirr, angle, xyShift)
            minX = min(coordTrans[0][0], coordTrans[1][0], coordTrans[2][0], coordTrans[3][0])
            minY = min(coordTrans[0][1], coordTrans[1][1], coordTrans[2][1], coordTrans[3][1])
            maxX = max(coordTrans[0][0], coordTrans[1][0], coordTrans[2][0], coordTrans[3][0])
            maxY = max(coordTrans[0][1], coordTrans[1][1], coordTrans[2][1], coordTrans[3][1])
            listMinX.append(minX)
            listMinY.append(minY)
            listMaxX.append(maxX)
            listMaxY.append(maxY)

        for sref in self.myLayout.structures[sr].srefs:
            sMirr = 1
            if sref.transFlags[0] == True:
                sMirr = -1
            sAngle = math.radians(float(0))
            if sref.rotateAngle:
                sAngle = math.radians(float(sref.rotateAngle))
            sAngle += angle
            x = sref.coordinates[0]
            y = sref.coordinates[1]
            newX = (x*math.cos(angle) - mirr*y*math.sin(angle)) + xyShift[0] 
            newY = (x*math.sin(angle) + mirr*y*math.cos(angle)) + xyShift[1] 
            sxyShift = (newX, newY)
            self.lowestLeftCorner(sref.sName, sMirr, sAngle, sxyShift, listMinX, listMinY, listMaxX, listMaxY)
        coordinate = []
        lowestX = min(listMinX)
        lowestY = min(float(item) for item in listMinY)
        highestX = max(float(item) for item in listMaxX)
        highestY = max(float(item) for item in listMaxY)
        coordinate.append((lowestX, lowestY))
        coordinate.append((highestX, highestY))
        return coordinate

