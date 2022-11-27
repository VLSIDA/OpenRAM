import math
from datetime import *
import numpy as np
from openram import debug
from .gdsPrimitives import *


class VlsiLayout:
    """Class represent a hierarchical layout"""

    def __init__(self, name=None, units=(0.001,1e-9), libraryName="DEFAULT.DB", gdsVersion=5):
        # keep a list of all the structures in this layout
        self.units = units
        # print(units)
        modDate = datetime.now()
        self.structures=dict()
        self.layerNumbersInUse = []
        self.debug = False
        if name:
            # take the root structure and copy it to a new structure with the new name
            self.rootStructureName=self.padText(name)
            # create the ROOT structure
            self.structures[self.rootStructureName] = GdsStructure()
            self.structures[self.rootStructureName].name = name
            self.structures[self.rootStructureName].createDate = (modDate.year,
                                                                  modDate.month,
                                                                  modDate.day,
                                                                  modDate.hour,
                                                                  modDate.minute,
                                                                  modDate.second)
            self.structures[self.rootStructureName].modDate = (modDate.year,
                                                               modDate.month,
                                                               modDate.day,
                                                               modDate.hour,
                                                               modDate.minute,
                                                               modDate.second)

        self.info = dict()  # information gathered from the GDSII header
        self.info['units']=self.units
        self.info['dates']=(modDate.year,
                            modDate.month,
                            modDate.day,
                            modDate.hour,
                            modDate.minute,
                            modDate.second,
                            modDate.year,
                            modDate.month,
                            modDate.day,
                            modDate.hour,
                            modDate.minute,
                            modDate.second)
        self.info['libraryName']=libraryName
        self.info['gdsVersion']=gdsVersion

        # This will contain a list of all structure names
        # expanded to include srefs / arefs separately.
        # each structure will have an X,Y,offset, and rotate associated
        # with it.  Populate via traverseTheHierarchy method.
        self.xyTree = []

        # temp variables used in delegate functions
        self.tempCoordinates=None
        self.tempPassFail = True

        # This is a dict indexed by the pin labels.
        # It contains a list of list of shapes, one for each occurance of the label.
        # Multiple labels may be disconnected.
        self.pins = {}

    def rotatedCoordinates(self,coordinatesToRotate,rotateAngle):
        # helper method to rotate a list of coordinates
        angle=math.radians(float(0))
        if(rotateAngle):
            angle = math.radians(float(rotateAngle))

        coordinatesRotate = []    # this will hold the rotated values
        for coordinate in coordinatesToRotate:
            # This is the CCW rotation matrix
            newX = coordinate[0]*math.cos(angle) - coordinate[1]*math.sin(angle)
            newY = coordinate[0]*math.sin(angle) + coordinate[1]*math.cos(angle)
            coordinatesRotate.extend((newX,newY))
        return coordinatesRotate

    def uniquify(self, prefix_name=None):
        new_structures = {}
        if self.rootStructureName[-1] == "\x00":
            prefix = self.rootStructureName[0:-1] + "_"
        else:
            prefix = self.rootStructureName + "_"
        for name in self.structures:
            if name[-1] == "\x00":
                base_name = name[0:-1]
            else:
                base_name = name
            # Don't do library cells
            if prefix_name and base_name.startswith(prefix_name):
                new_name = name
            elif name != self.rootStructureName:
                new_name = self.padText(prefix + base_name)
            else:
                new_name = name
            #print("Structure: {0} -> {1}".format(base_name, new_name))

            new_structures[new_name] = self.structures[name]
            new_structures[new_name].name = new_name
            for sref in new_structures[new_name].srefs:
                if sref.sName[-1] == "\x00":
                    base_sref_name = sref.sName[0:-1]
                else:
                    base_sref_name = sref.sName
                # Don't do library cells
                if prefix_name and base_sref_name.startswith(prefix_name):
                    new_sref_name = sref.sName
                else:
                    new_sref_name = self.padText(prefix + base_sref_name)
                sref.sName = new_sref_name
                #print("SREF: {0} -> {1}".format(base_sref_name, new_sref_name))
        self.structures = new_structures

    def rename(self,newName):
        # take the root structure and copy it to a new structure with the new name
        self.structures[newName] = self.structures[self.rootStructureName]
        self.structures[newName].name = self.padText(newName)
        # and delete the old root
        del self.structures[self.rootStructureName]
        self.rootStructureName = newName
        # repopulate the 2d map so drawing occurs correctly
        del self.xyTree[:]
        self.populateCoordinateMap()

    def newLayout(self,newName):
        # if (newName == "" | newName == 0):
        #    print("ERROR: vlsiLayout.py:newLayout  newName is null")

        # make sure the newName is a multiple of 2 characters
        # if(len(newName)%2 == 1):
            # pad with a zero
            # newName = newName + '\x00'
        # take the root structure and copy it to a new structure with the new name
        # self.structures[newName] = self.structures[self.rootStructureName]

        modDate = datetime.now()

        self.structures[newName] = GdsStructure()
        self.structures[newName].name = newName

        self.rootStructureName = newName

        self.rootStructureName=newName

        # create the ROOT structure
        self.structures[self.rootStructureName] = GdsStructure()
        # self.structures[self.rootStructureName].name = name
        self.structures[self.rootStructureName].createDate = (modDate.year,
                                                              modDate.month,
                                                              modDate.day,
                                                              modDate.hour,
                                                              modDate.minute,
                                                              modDate.second)
        self.structures[self.rootStructureName].modDate = (modDate.year,
                                                           modDate.month,
                                                           modDate.day,
                                                           modDate.hour,
                                                           modDate.minute,
                                                           modDate.second)


        #repopulate the 2d map so drawing occurs correctly
        self.prepareForWrite()

    def prepareForWrite(self):
        del self.xyTree[:]
        self.populateCoordinateMap()

    def deduceHierarchy(self):
        """ First, find the root of the tree.
        Then go through and get the name of every structure.
        Then, go through and find which structure is not
        contained by any other structure. this is the root."""
        structureNames=[]
        for name in self.structures:
            structureNames.append(name)
        for name in self.structures:
            if(len(self.structures[name].srefs)>0): #does this structure reference any others?
                for sref in self.structures[name].srefs: #go through each reference
                    if sref.sName in structureNames: #and compare to our list
                        structureNames.remove(sref.sName)

        debug.check(len(structureNames)==1,"Multiple possible root structures in the layout: {}".format(str(structureNames)))
        self.rootStructureName = structureNames[0]

    def traverseTheHierarchy(self, startingStructureName=None, delegateFunction=None,
                             transformPath=[], rotateAngle=0, transFlags=[0, 0, 0], coordinates=(0, 0)):
        # since this is a recursive function, must deal with the default
        # parameters explicitly
        if startingStructureName == None:
            startingStructureName = self.rootStructureName

        # set up the rotation matrix
        if(rotateAngle == None or rotateAngle == ""):
            angle = 0
        else:
            # MRG: Added negative to make CCW rotate 8/29/18
            angle = math.radians(float(rotateAngle))
        mRotate = np.array([[math.cos(angle), -math.sin(angle), 0.0],
                            [math.sin(angle), math.cos(angle), 0.0],
                            [0.0, 0.0, 1.0]])
        # set up the translation matrix
        translateX = float(coordinates[0])
        translateY = float(coordinates[1])
        mTranslate = np.array([[1.0, 0.0, translateX],
                               [0.0, 1.0, translateY],
                               [0.0, 0.0, 1.0]])
        # set up the scale matrix (handles mirror X)
        scaleX = 1.0
        if (transFlags[0]):
            scaleY = -1.0
        else:
            scaleY = 1.0
        mScale = np.array([[scaleX, 0.0, 0.0],
                           [0.0, scaleY, 0.0],
                           [0.0, 0.0, 1.0]])
        # we need to keep track of all transforms in the hierarchy
        # when we add an element to the xy tree, we apply all transforms from the bottom up
        transformPath.append((mRotate,mScale,mTranslate))
        if delegateFunction != None:
            delegateFunction(startingStructureName, transformPath)
        # starting with a particular structure, we will recursively traverse the tree
        # ********might have to set the recursion level deeper for big layouts!
        try:
            if(len(self.structures[startingStructureName].srefs)>0): #does this structure reference any others?
                # if so, go through each and call this function again
                # if not, return back to the caller (caller can be this function)
                for sref in self.structures[startingStructureName].srefs:
                    # here, we are going to modify the sref coordinates based on the parent objects rotation
                    self.traverseTheHierarchy(startingStructureName = sref.sName,
                                              delegateFunction = delegateFunction,
                                              transformPath = transformPath,
                                              rotateAngle = sref.rotateAngle,
                                              transFlags = sref.transFlags,
                                              coordinates = sref.coordinates)
        except KeyError:
            debug.error("Could not find structure {} in GDS file.".format(startingStructureName),-1)

            # MUST HANDLE AREFs HERE AS WELL
        # when we return, drop the last transform from the transformPath
        del transformPath[-1]
        return

    def initialize(self, special_purposes={}):
        self.deduceHierarchy()
        # self.traverseTheHierarchy()
        self.populateCoordinateMap()
        # only ones with text
        for layerNumber in self.layerNumbersInUse:
            # if layerNumber not in no_pin_shape:
            if layerNumber in special_purposes:
                self.processLabelPins((layerNumber, special_purposes[layerNumber]))
            else:
                self.processLabelPins((layerNumber, None))

    def populateCoordinateMap(self):
        def addToXyTree(startingStructureName = None,transformPath = None):
            uVector = np.array([[1.0],[0.0],[0.0]]) #start with normal basis vectors
            vVector = np.array([[0.0],[1.0],[0.0]])
            origin = np.array([[0.0],[0.0],[1.0]]) #and an origin (Z component is 1.0 to indicate position instead of vector)
            #make a copy of all the transforms and reverse it
            reverseTransformPath = transformPath[:]
            if len(reverseTransformPath) > 1:
                reverseTransformPath.reverse()
            #now go through each transform and apply them to our basis and origin in succession
            for transform in reverseTransformPath:
                origin = np.dot(transform[0], origin)  #rotate
                uVector = np.dot(transform[0], uVector)  #rotate
                vVector = np.dot(transform[0], vVector)  #rotate
                origin = np.dot(transform[1], origin)  #scale
                uVector = np.dot(transform[1], uVector)  #scale
                vVector = np.dot(transform[1], vVector)  #scale
                origin = np.dot(transform[2], origin)  #translate
                #we don't need to do a translation on the basis vectors
                #uVector = transform[2] * uVector  #translate
                #vVector = transform[2] * vVector  #translate
            #populate the xyTree with each structureName and coordinate space
            self.xyTree.append((startingStructureName,origin,uVector,vVector))
        self.traverseTheHierarchy(delegateFunction = addToXyTree)

    def microns(self, userUnits):
        """Utility function to convert user units to microns"""
        userUnit = self.units[1]/self.units[0]
        userUnitsPerMicron = userUnit / userunit
        layoutUnitsPerMicron = userUnitsPerMicron / self.units[0]
        return userUnits / layoutUnitsPerMicron

    def userUnits(self, microns):
        """Utility function to convert microns to user units"""
        userUnit = self.units[1]/self.units[0]
        # userUnitsPerMicron = userUnit / 1e-6
        userUnitsPerMicron = userUnit / (userUnit)
        layoutUnitsPerMicron = userUnitsPerMicron / self.units[0]
        # print("userUnit:",userUnit,
        # "userUnitsPerMicron",userUnitsPerMicron,
        # "layoutUnitsPerMicron",layoutUnitsPerMicron,
        # [microns,microns*layoutUnitsPerMicron])
        return round(microns*layoutUnitsPerMicron, 0)

    def changeRoot(self,newRoot, create=False):
        """
        Method to change the root pointer to another layout.
        """

        if self.debug:
            debug.info(0,"DEBUG:  GdsMill vlsiLayout: changeRoot: %s "%newRoot)

        # Determine if newRoot exists
        #  layoutToAdd (default) or nameOfLayout
        if (newRoot == 0 | ((newRoot not in self.structures) & ~create)):
            print("ERROR:  vlsiLayout.changeRoot: Name of new root [%s] not found and create flag is false"%newRoot)
            exit(1)
        else:
            if ((newRoot not in self.structures) & create):
                self.newLayout(newRoot)
            self.rootStructureName = newRoot

    def addInstance(self,layoutToAdd,nameOfLayout=0,offsetInMicrons=(0,0),mirror=None,rotate=None):
        """
        Method to insert one layout into another at a particular offset.
        """
        offsetInLayoutUnits = (self.userUnits(offsetInMicrons[0]),self.userUnits(offsetInMicrons[1]))
        if self.debug:
            debug.info(0,"DEBUG:  GdsMill vlsiLayout: addInstance: type {0}, nameOfLayout {1}".format(type(layoutToAdd),nameOfLayout))
            debug.info(0,"DEBUG: name={0} offset={1} mirror={2} rotate={3}".format(layoutToAdd.rootStructureName,offsetInMicrons, mirror, rotate))



        # Determine if we are instantiating the root design of
        #  layoutToAdd (default) or nameOfLayout
        if nameOfLayout == 0:
            StructureFound = True
            StructureName = layoutToAdd.rootStructureName
        else:
            StructureName = nameOfLayout #layoutToAdd
            StructureFound = False
            for structure in layoutToAdd.structures:
                if StructureName in structure:
                    if self.debug:
                        debug.info(1,"DEBUG:  Structure %s Found"%StructureName)
                    StructureFound = True

        debug.check(StructureFound,"Could not find layout to instantiate {}".format(StructureName))


        # If layoutToAdd is a unique object (not this), then copy hierarchy,
        #  otherwise, if it is a text name of an internal structure, use it.

        if layoutToAdd != self:
            #first, we need to combine the structure dictionaries from both layouts
            for structure in layoutToAdd.structures:
                if structure not in self.structures:
                    self.structures[structure]=layoutToAdd.structures[structure]
            #also combine the "layers in use" list
            for layerNumber in layoutToAdd.layerNumbersInUse:
                if layerNumber not in self.layerNumbersInUse:
                    self.layerNumbersInUse.append(layerNumber)

        #add a reference to the new layout structure in this layout's root
        layoutToAddSref = GdsSref()
        layoutToAddSref.sName = StructureName
        layoutToAddSref.coordinates = offsetInLayoutUnits

        if mirror or rotate:

            layoutToAddSref.transFlags = [0,0,0]
            # transFlags = (mirror around x-axis, magnification, rotation)
            # If magnification or rotation is true, it is the flags are then
            # followed by an amount in the record
            if mirror=="R90":
                rotate = 90.0
            if mirror=="R180":
                rotate = 180.0
            if mirror=="R270":
                rotate = 270.0
            if rotate:
                #layoutToAddSref.transFlags[2] = 1
                layoutToAddSref.rotateAngle = rotate
            if mirror == "x" or mirror == "MX":
                layoutToAddSref.transFlags[0] = 1
            if mirror == "y" or mirror == "MY": #NOTE: "MY" option will override specified rotate angle
                layoutToAddSref.transFlags[0] = 1
                #layoutToAddSref.transFlags[2] = 1
                layoutToAddSref.rotateAngle = 180.0
            if mirror == "xy" or mirror == "XY": #NOTE: "XY" option will override specified rotate angle
                #layoutToAddSref.transFlags[2] = 1
                layoutToAddSref.rotateAngle = 180.0

        #add the sref to the root structure
        self.structures[self.rootStructureName].srefs.append(layoutToAddSref)

    def addBox(self,layerNumber=0, purposeNumber=0, offsetInMicrons=(0,0), width=1.0, height=1.0,center=False):
        """
        Method to add a box to a layout
        """
        offsetInLayoutUnits = (self.userUnits(offsetInMicrons[0]),self.userUnits(offsetInMicrons[1]))
        #print("addBox:offsetInLayoutUnits",offsetInLayoutUnits)
        widthInLayoutUnits = self.userUnits(width)
        heightInLayoutUnits = self.userUnits(height)
        #print("offsetInLayoutUnits",widthInLayoutUnits,"heightInLayoutUnits",heightInLayoutUnits)
        if not center:
            coordinates=[offsetInLayoutUnits,
                         (offsetInLayoutUnits[0]+widthInLayoutUnits,offsetInLayoutUnits[1]),
                         (offsetInLayoutUnits[0]+widthInLayoutUnits,offsetInLayoutUnits[1]+heightInLayoutUnits),
                         (offsetInLayoutUnits[0],offsetInLayoutUnits[1]+heightInLayoutUnits),
                         offsetInLayoutUnits]
        else:
            startPoint = (offsetInLayoutUnits[0]-widthInLayoutUnits/2.0, offsetInLayoutUnits[1]-heightInLayoutUnits/2.0)
            coordinates=[startPoint,
                         (startPoint[0]+widthInLayoutUnits,startPoint[1]),
                         (startPoint[0]+widthInLayoutUnits,startPoint[1]+heightInLayoutUnits),
                         (startPoint[0],startPoint[1]+heightInLayoutUnits),
                         startPoint]

        boundaryToAdd = GdsBoundary()
        boundaryToAdd.drawingLayer = layerNumber
        boundaryToAdd.coordinates = coordinates
        boundaryToAdd.purposeLayer = purposeNumber
        #add the sref to the root structure
        self.structures[self.rootStructureName].boundaries.append(boundaryToAdd)

    def addPath(self, layerNumber=0, purposeNumber=0, coordinates=[(0,0)], width=1.0):
        """
        Method to add a path to a layout
        """
        widthInLayoutUnits = self.userUnits(width)
        layoutUnitCoordinates = []
        #first convert to proper units
        for coordinate in coordinates:
            cX = self.userUnits(coordinate[0])
            cY = self.userUnits(coordinate[1])
            layoutUnitCoordinates.append((cX,cY))
        pathToAdd = GdsPath()
        pathToAdd.drawingLayer = layerNumber
        pathToAdd.purposeLayer = purposeNumber
        pathToAdd.pathWidth = widthInLayoutUnits
        pathToAdd.coordinates = layoutUnitCoordinates
        #add the sref to the root structure
        self.structures[self.rootStructureName].paths.append(pathToAdd)

    def addText(self, text, layerNumber=0, purposeNumber=0, offsetInMicrons=(0,0), magnification=None, rotate=None):
        offsetInLayoutUnits = (self.userUnits(offsetInMicrons[0]),self.userUnits(offsetInMicrons[1]))
        textToAdd = GdsText()
        textToAdd.drawingLayer = layerNumber
        textToAdd.purposeLayer = purposeNumber
        textToAdd.coordinates = [offsetInLayoutUnits]
        textToAdd.transFlags = [0,0,0]
        textToAdd.textString = self.padText(text)
        #textToAdd.transFlags[1] = 1
        if magnification:
            textToAdd.magFactor = magnification
        if rotate:
            #textToAdd.transFlags[2] = 1
            textToAdd.rotateAngle = rotate
        #add the sref to the root structure
        self.structures[self.rootStructureName].texts.append(textToAdd)

    def padText(self, text):
        debug.check(len(text) > 0, "Cannot have zero length text string.")
        if(len(text) % 2 == 1):
            return text + '\x00'
        else:
            return text

    def isBounded(self,testPoint,startPoint,endPoint):
        #these arguments are touples of (x,y) coordinates
        if testPoint == None:
            return 0
        if(testPoint[0]<=max(endPoint[0],startPoint[0]) and \
           testPoint[0]>=min(endPoint[0],startPoint[0]) and \
           testPoint[1]<=max(endPoint[1],startPoint[1]) and \
           testPoint[1]>=min(endPoint[1],startPoint[1])):
            return 1
        else:
            return 0

    def intersectionPoint(self,startPoint1,endPoint1,startPoint2,endPoint2):
        if((endPoint1[0]-startPoint1[0])!=0 and (endPoint2[0]-startPoint2[0])!=0):
            pSlope = (endPoint1[1]-startPoint1[1])/(endPoint1[0]-startPoint1[0])
            pIntercept = startPoint1[1]-pSlope*startPoint1[0]
            qSlope = (endPoint2[1]-startPoint2[1])/(endPoint2[0]-startPoint2[0])
            qIntercept = startPoint2[1]-qSlope*startPoint2[0]
            if(pSlope!=qSlope):
                newX=(qIntercept-pIntercept)/(pSlope-qSlope)
                newY=pSlope*newX+pIntercept
            else:
                #parallel lines can't intersect
                newX=None
                newY=None
        elif((endPoint1[0]-startPoint1[0])==0 and (endPoint2[0]-startPoint2[0])==0):
            #two vertical lines cannot intersect
            newX = None
            newY = None
        elif((endPoint1[0]-startPoint1[0])==0 and (endPoint2[0]-startPoint2[0])!=0):
            qSlope = (endPoint2[1]-startPoint2[1])/(endPoint2[0]-startPoint2[0])
            qIntercept = startPoint2[1]-qSlope*startPoint2[0]
            newX=endPoint1[0]
            newY=qSlope*newX+qIntercept
        elif((endPoint1[0]-startPoint1[0])!=0 and (endPoint2[0]-startPoint2[0])==0):
            pSlope = (endPoint1[1]-startPoint1[1])/(endPoint1[0]-startPoint1[0])
            pIntercept = startPoint1[1]-pSlope*startPoint1[0]
            newX=endPoint2[0]
            newY=pSlope*newX+pIntercept
        return (newX,newY)

    def isCollinear(self,testPoint,point1,point2):
        slope1 = (testPoint[1]-point1[1])/(testPoint[0]-point1[0])
        slope2 = (point2[1]-point1[1])/(point2[0]-point1[0])
        if slope1 == slope2:
            return True
        return False

    def doShapesIntersect(self,shape1Coordinates, shape2Coordinates):
        """
        Utility function to determine if 2 arbitrary shapes intersect.
        We define intersection by taking pairs of points in each shape (assuming they are in order)
        and seeing if any of the lines formed by these pais intersect.
        """
        for shape1Index in range(0,len(shape1Coordinates)-1):
            for shape2Index in range(0,len(shape2Coordinates)-1):
                startPoint1 = shape1Coordinates[shape1Index]
                endPoint1 = shape1Coordinates[shape1Index+1]
                startPoint2 = shape2Coordinates[shape2Index]
                endPoint2 = shape2Coordinates[shape2Index+1]
                intersect = self.intersectionPoint(startPoint1,endPoint1,startPoint2,endPoint2)
                if(self.isBounded(intersect,startPoint1,endPoint1) and self.isBounded(intersect,startPoint2,endPoint2)):
                    return True  #these shapes overlap!
        return False #these shapes are ok

    def isPointInsideOfBox(self,pointCoordinates,boxCoordinates):
        """
        Check if a point is contained in the shape
        """
        debug.check(len(boxCoordinates)==4,"Invalid number of coordinates for box.")
        leftBound = boxCoordinates[0][0]
        rightBound = boxCoordinates[0][0]
        topBound = boxCoordinates[0][1]
        bottomBound = boxCoordinates[0][1]
        for point in boxCoordinates:
            if point[0]<leftBound:
                leftBound = point[0]
            if point[0]>rightBound:
                rightBound = point[0]
            if point[1]<bottomBound:
                bottomBound = point[1]
            if point[1]>topBound:
                topBound = point[1]
        if(pointCoordinates[0]>rightBound or
           pointCoordinates[0]<leftBound or
           pointCoordinates[1]>topBound or
           pointCoordinates[1]<bottomBound):
            return False
        return True

    def isShapeInsideOfBox(self,shapeCoordinates, boxCoordinates):
        """
        Go through every point in the shape to test if they are all inside the box.
        """
        for point in shapeCoordinates:
            if not self.isPointInsideOfBox(point,boxCoordinates):
                return False
        return True


    def fillAreaDensity(self, layerToFill = 0, offsetInMicrons = (0,0), coverageWidth = 100.0, coverageHeight = 100.0, minSpacing = 0.22, blockSize = 1.0):
        effectiveBlock = blockSize+minSpacing
        widthInBlocks = int(coverageWidth/effectiveBlock)
        heightInBlocks = int(coverageHeight/effectiveBlock)
        passFailRecord = []

        print("Filling layer:",layerToFill)
        def isThisBlockOk(startingStructureName,coordinates,rotateAngle=None):
            #go through every boundary and check
            for boundary in self.structures[startingStructureName].boundaries:
                #only test shapes on the same layer
                if(boundary.drawingLayer == layerToFill):
                    #remap coordinates
                    shiftedBoundaryCoordinates = []
                    for shapeCoordinate in boundary.rotatedCoordinates(rotateAngle):
                        shiftedBoundaryCoordinates.append((shapeCoordinate[0]+coordinates[0],shapeCoordinate[1]+coordinates[1]))
                    joint = self.doShapesIntersect(self.tempCoordinates, shiftedBoundaryCoordinates)
                    if joint:
                        self.tempPassFail = False
                    common = self.isShapeInsideOfBox(shiftedBoundaryCoordinates,self.tempCoordinates)
                    if common:
                        self.tempPassFail = False
            for path in self.structures[startingStructureName].paths:
                #only test shapes on the same layer
                if(path.drawingLayer == layerToFill):
                    #remap coordinates
                    shiftedBoundaryCoordinates = []
                    for shapeCoordinate in path.equivalentBoundaryCoordinates(rotateAngle):
                        shiftedBoundaryCoordinates.append((shapeCoordinate[0]+coordinates[0],shapeCoordinate[1]+coordinates[1]))
                    joint = self.doShapesIntersect(self.tempCoordinates, shiftedBoundaryCoordinates)
                    if joint:
                        self.tempPassFail = False
                    common = self.isShapeInsideOfBox(shiftedBoundaryCoordinates,self.tempCoordinates)
                    if common:
                        self.tempPassFail = False

        for yIndex in range(0,heightInBlocks):
            for xIndex in range(0,widthInBlocks):
                percentDone = (float((yIndex*heightInBlocks)+xIndex) / (heightInBlocks*widthInBlocks))*100
                blockX = (xIndex*effectiveBlock)+offsetInMicrons[0]
                blockY = (yIndex*effectiveBlock)+offsetInMicrons[1]
                self.tempCoordinates=[(self.userUnits(blockX-minSpacing),self.userUnits(blockY-minSpacing)),
                    (self.userUnits(blockX-minSpacing),self.userUnits(blockY+effectiveBlock)),
                    (self.userUnits(blockX+effectiveBlock),self.userUnits(blockY+effectiveBlock)),
                    (self.userUnits(blockX+effectiveBlock),self.userUnits(blockY-minSpacing)),
                    (self.userUnits(blockX-minSpacing),self.userUnits(blockY-minSpacing))]
                self.tempPassFail = True
                #go through the hierarchy and see if the block will fit
                self.traverseTheHierarchy(delegateFunction = isThisBlockOk)
                #if its bad, this global tempPassFail will be false
                #if true, we can add the block
                passFailRecord.append(self.tempPassFail)
            print("Percent Complete:"+str(percentDone))


        passFailIndex=0
        for yIndex in range(0,heightInBlocks):
            for xIndex in range(0,widthInBlocks):
                blockX = (xIndex*effectiveBlock)+offsetInMicrons[0]
                blockY = (yIndex*effectiveBlock)+offsetInMicrons[1]
                if passFailRecord[passFailIndex]:
                    self.addBox(layerToFill, (blockX,blockY), width=blockSize, height=blockSize)
                passFailIndex += 1
        print("Done\n\n")

    def getLayoutBorder(self, lpp, structure = ""):
        if structure == "":
            structure = self.rootStructureName
        cellSizeMicron = None

        shapes = self.getAllShapes(lpp)
        if len(shapes) != 1:
            debug.warning("More than one or no boundaries found in cell: {}".format(structure))
        debug.check(len(shapes) != 0,
                    "Error: "+str(structure)+".cell_size information not found yet")
        max_boundary = None
        max_area = 0
        for boundary in shapes:
            new_area = boundaryArea(boundary)
            if not max_boundary or new_area > max_area:
                max_boundary = boundary
                max_area = new_area
        cellSizeMicron = [max_boundary[2], max_boundary[3]]
        return cellSizeMicron

    def measureSize(self, startStructure):
        self.rootStructureName = self.padText(startStructure)
        self.populateCoordinateMap()
        cellBoundary = [None, None, None, None]
        for TreeUnit in self.xyTree:
            cellBoundary = self.measureSizeInStructure(TreeUnit, cellBoundary)
        cellSize = [cellBoundary[2]-cellBoundary[0],
                    cellBoundary[3]-cellBoundary[1]]
        cellSizeMicron = [cellSize[0]*self.units[0],
                          cellSize[1]*self.units[0]]
        return cellSizeMicron

    def measureBoundary(self, startStructure):
        self.rootStructureName = self.padText(startStructure)
        self.populateCoordinateMap()
        cellBoundary = [None, None, None, None]
        for TreeUnit in self.xyTree:
            cellBoundary = self.measureSizeInStructure(TreeUnit, cellBoundary)
        return [[self.units[0]*cellBoundary[0],
                 self.units[0]*cellBoundary[1]],
                [self.units[0]*cellBoundary[2],
                 self.units[0]*cellBoundary[3]]]

    def measureSizeInStructure(self, structure, cellBoundary):
        (structureName, structureOrigin,
         structureuVector, structurevVector) = structure
        for boundary in self.structures[str(structureName)].boundaries:
            left_bottom=boundary.coordinates[0]
            right_top=boundary.coordinates[2]
            thisBoundary=[left_bottom[0],left_bottom[1],right_top[0],right_top[1]]
            thisBoundary=self.transformRectangle(thisBoundary,structureuVector,structurevVector)
            thisBoundary=[thisBoundary[0]+structureOrigin[0],thisBoundary[1]+structureOrigin[1],
            thisBoundary[2]+structureOrigin[0],thisBoundary[3]+structureOrigin[1]]
            cellBoundary=self.updateBoundary(thisBoundary,cellBoundary)
        return cellBoundary

    def updateBoundary(self,thisBoundary,cellBoundary):
        [left_bott_X,left_bott_Y,right_top_X,right_top_Y]=thisBoundary
        # If any are None
        if not (cellBoundary[0] and cellBoundary[1] and cellBoundary[2] and cellBoundary[3]):
            cellBoundary=thisBoundary
        else:
            if cellBoundary[0]>left_bott_X:
                cellBoundary[0]=left_bott_X
            if cellBoundary[1]>left_bott_Y:
                cellBoundary[1]=left_bott_Y
            if cellBoundary[2]<right_top_X:
                cellBoundary[2]=right_top_X
            if cellBoundary[3]<right_top_Y:
                cellBoundary[3]=right_top_Y
        return cellBoundary

    def getTexts(self, lpp):
        """
        Get all of the labels on a given layer only at the root level.
        """
        text_list = []
        for Text in self.structures[self.rootStructureName].texts:
            if sameLPP((Text.drawingLayer, Text.purposeLayer),
                       lpp):
                text_list.append(Text)
        return text_list

    def getPinShape(self, pin_name):
        """
        Search for a pin label and return the largest enclosing rectangle
        on the same layer as the pin label.
        If there are multiple pin lists, return the max of each.
        """
        pin_map = self.pins[pin_name]
        max_pins = []
        for pin_list in pin_map:
            max_pin = None
            max_area = 0
            for pin in pin_list:
                (layer, boundary) = pin
                new_area = boundaryArea(boundary)
                if not max_pin or new_area > max_area:
                    max_pin = pin
                    max_area = new_area
            max_pins.append(max_pin)

        return max_pins

    def getAllPinShapes(self, pin_name):
        """
        Search for a pin label and return ALL the enclosing rectangles on the same layer
        as the pin label.
        """
        shape_list = []
        pin_map = self.pins[pin_name]
        for pin_list in pin_map:
            for pin in pin_list:
                (pin_layer, boundary) = pin
                shape_list.append(pin)

        return shape_list

    def processLabelPins(self, lpp):
        """
        Find all text labels and create a map to a list of shapes that
        they enclose on the given layer.
        """

        # Get the labels on a layer in the root level
        labels = self.getTexts(lpp)

        # Get all of the shapes on the layer at all levels
        # and transform them to the current level
        shapes = self.getAllShapes(lpp)

        for label in labels:
            label_coordinate = label.coordinates[0]
            user_coordinate = [x*self.units[0] for x in label_coordinate]
            pin_shapes = []
            # Remove the padding if it exists
            if label.textString[-1] == "\x00":
                label_text = label.textString[0:-1]
            else:
                label_text = label.textString
            try:
                from openram.tech import layer_override
                if layer_override[label_text]:
                    shapes = self.getAllShapes((layer_override[label_text][0], None))
                    if not shapes:
                        shapes = self.getAllShapes(lpp)
                    else:
                        lpp = layer_override[label_text]



            except:
                pass
            for boundary in shapes:
                if self.labelInRectangle(user_coordinate, boundary):
                    pin_shapes.append((lpp, boundary))

            try:
                self.pins[label_text]
            except KeyError:
                self.pins[label_text] = []
            self.pins[label_text].append(pin_shapes)

    def getBlockages(self, lpp):
        """
        Return all blockages on a given layer in
        [coordinate 1, coordinate 2,...] format and
        user units.
        """
        blockages = []

        shapes = self.getAllShapes(lpp)
        for boundary in shapes:
            vectors = []
            for i in range(0, len(boundary), 2):
                vectors.append((boundary[i], boundary[i+1]))
            blockages.append(vectors)

        return blockages

    def getAllShapes(self, lpp):
        """
        Return all shapes on a given layer in [llx, lly, urx, ury]
        format and user units for rectangles
        and [coordinate 1, coordinate 2,...] format and user
        units for polygons.
        """
        boundaries = set()
        for TreeUnit in self.xyTree:
            # print(TreeUnit[0])
            boundaries.update(self.getShapesInStructure(lpp, TreeUnit))

        # Convert to user units
        user_boundaries = []
        for boundary in boundaries:
            boundaries_list = []
            for i in range(0, len(boundary)):
                boundaries_list.append(boundary[i]*self.units[0])
            user_boundaries.append(boundaries_list)
        return user_boundaries

    def getShapesInStructure(self, lpp, structure):
        """
        Go through all the shapes in a structure and
        return the list of shapes in
        the form [llx, lly, urx, ury] for rectangles
        and [coordinate 1, coordinate 2,...] for polygons.
        """
        (structureName, structureOrigin,
         structureuVector, structurevVector) = structure
        # print(structureName,
        # "u", structureuVector.transpose(),
        # "v",structurevVector.transpose(),
        # "o",structureOrigin.transpose())
        boundaries = []
        for boundary in self.structures[str(structureName)].boundaries:
            if sameLPP((boundary.drawingLayer, boundary.purposeLayer),
                       lpp):
                if len(boundary.coordinates) != 5:
                    # if shape is a polygon (used in DFF)
                    boundaryPolygon = []
                    # Polygon is a list of coordinates going ccw
                    for coord in range(0, len(boundary.coordinates)):
                        boundaryPolygon.append(boundary.coordinates[coord][0])
                        boundaryPolygon.append(boundary.coordinates[coord][1])
                    # perform the rotation
                    boundaryPolygon = self.transformPolygon(boundaryPolygon,
                                                            structureuVector,
                                                            structurevVector)
                    # add the offset
                    polygon = []
                    for i in range(0, len(boundaryPolygon), 2):
                        polygon.append(boundaryPolygon[i] + structureOrigin[0].item())
                        polygon.append(boundaryPolygon[i+1] + structureOrigin[1].item())
                    # make it a tuple
                    polygon = tuple(polygon)
                    boundaries.append(polygon)
                else:
                    # else shape is a rectangle
                    left_bottom = boundary.coordinates[0]
                    right_top = boundary.coordinates[2]
                    # Rectangle is [leftx, bottomy, rightx, topy].
                    boundaryRect = [left_bottom[0], left_bottom[1],
                                    right_top[0], right_top[1]]
                    # perform the rotation
                    boundaryRect = self.transformRectangle(boundaryRect,
                                                           structureuVector,
                                                           structurevVector)
                    # add the offset and make it a tuple
                    boundaryRect = (boundaryRect[0]+structureOrigin[0].item(),
                                    boundaryRect[1]+structureOrigin[1].item(),
                                    boundaryRect[2]+structureOrigin[0].item(),
                                    boundaryRect[3]+structureOrigin[1].item())
                    boundaries.append(boundaryRect)
        return boundaries


    def transformPolygon(self,originalPolygon,uVector,vVector):
        """
        Transforms the coordinates of a polygon in space.
        """
        polygon = []
        newPolygon = []
        for i in range(0,len(originalPolygon),2):
            polygon.append(self.transformCoordinate([originalPolygon[i],originalPolygon[i+1]],uVector,vVector))
            newPolygon.append(polygon[int(i/2)][0])
            newPolygon.append(polygon[int(i/2)][1])
        return newPolygon

    def transformRectangle(self,originalRectangle,uVector,vVector):
        """
        Transforms the four coordinates of a rectangle in space
        and recomputes the left, bottom, right, top values.
        """
        leftBottom=[originalRectangle[0],originalRectangle[1]]
        leftBottom=self.transformCoordinate(leftBottom,uVector,vVector)

        rightTop=[originalRectangle[2],originalRectangle[3]]
        rightTop=self.transformCoordinate(rightTop,uVector,vVector)

        left=min(leftBottom[0],rightTop[0])
        bottom=min(leftBottom[1],rightTop[1])
        right=max(leftBottom[0],rightTop[0])
        top=max(leftBottom[1],rightTop[1])

        newRectangle = [left,bottom,right,top]
        return newRectangle

    def transformCoordinate(self,coordinate,uVector,vVector):
        """
        Rotate a coordinate in space.
        """
        # MRG: 9/3/18 Incorrect matrix multiplication!
        # This is fixed to be:
        # |u[0] v[0]| |x| |x'|
        # |u[1] v[1]|x|y|=|y'|
        x=coordinate[0]*uVector[0][0]+coordinate[1]*vVector[0][0]
        y=coordinate[0]*uVector[1][0]+coordinate[1]*vVector[1][0]
        transformCoordinate=[x,y]

        return transformCoordinate


    def labelInRectangle(self,coordinate,rectangle):
        """
        Checks if a coordinate is within a given rectangle. Rectangle is [leftx, bottomy, rightx, topy].
        """
        coordinate_In_Rectangle_x_range=(coordinate[0]>=rectangle[0])&(coordinate[0]<=rectangle[2])
        coordinate_In_Rectangle_y_range=(coordinate[1]>=rectangle[1])&(coordinate[1]<=rectangle[3])
        if coordinate_In_Rectangle_x_range & coordinate_In_Rectangle_y_range:
            return True
        else:
            return False


def sameLPP(lpp1, lpp2):
    """
    Check if the layers and purposes are the same.
    Ignore if purpose is a None.
    """
    if lpp1[1] == None or lpp2[1] == None:
        return lpp1[0] == lpp2[0]

    if isinstance(lpp1[1], list):
        for i in range(len(lpp1[1])):
            if lpp1[0] == lpp2[0] and lpp1[1][i] == lpp2[1]:
                return True

    if isinstance(lpp2[1], list):
        for i in range(len(lpp2[1])):
            if lpp1[0] == lpp2[0] and lpp1[1] == lpp2[1][i]:
                return True

    return lpp1[0] == lpp2[0] and lpp1[1] == lpp2[1]


def boundaryArea(A):
    """
    Returns boundary area for sorting.
    """
    area_A=(A[2]-A[0])*(A[3]-A[1])
    return area_A
