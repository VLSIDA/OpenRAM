from gdsPrimitives import *
from datetime import *
import mpmath
import gdsPrimitives

class VlsiLayout:
    """Class represent a hierarchical layout"""

    def __init__(self, name=None, units=(0.001,1e-9), libraryName = "DEFAULT.DB", gdsVersion=5):
        #keep a list of all the structures in this layout
        self.units = units
        #print units
        modDate = datetime.now()
        self.structures=dict()
        self.layerNumbersInUse = []
        self.debug = False
        if name:
            self.rootStructureName=name
            #create the ROOT structure
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
        
        self.info = dict()  #information gathered from the GDSII header
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
        
        self.xyTree = [] #This will contain a list of all structure names
                        #expanded to include srefs / arefs separately.
                        #each structure will have an X,Y,offset, and rotate associated
                        #with it.  Populate via traverseTheHierarchy method.
        
        #temp variables used in delegate functions
        self.tempCoordinates=None
        self.tempPassFail = True

    def rotatedCoordinates(self,coordinatesToRotate,rotateAngle):
        #helper method to rotate a list of coordinates
        angle=math.radians(float(0))
        if(rotateAngle):
            angle = math.radians(float(repr(rotateAngle)))        

        coordinatesRotate = []    #this will hold the rotated values        
        for coordinate in coordinatesToRotate:
            newX = coordinate[0]*math.cos(angle) - coordinate[1]*math.sin(angle)
            newY = coordinate[0]*math.sin(angle) + coordinate[1]*math.cos(angle)
            coordinatesRotate += [(newX,newY)]       
        return coordinatesRotate
    
    def rename(self,newName):
        #make sure the newName is a multiple of 2 characters
        if(len(newName)%2 == 1):
            #pad with a zero
            newName = newName + '\x00'
        #take the root structure and copy it to a new structure with the new name
        self.structures[newName] = self.structures[self.rootStructureName]
        self.structures[newName].name = newName
        #and delete the old root
        del self.structures[self.rootStructureName]
        self.rootStructureName = newName
        #repopulate the 2d map so drawing occurs correctly
        del self.xyTree[:]
        self.populateCoordinateMap()

    def newLayout(self,newName):
        #if (newName == "" | newName == 0):
    #   print("ERROR: vlsiLayout.py:newLayout  newName is null")

        #make sure the newName is a multiple of 2 characters
        #if(len(newName)%2 == 1):
            #pad with a zero
            #newName = newName + '\x00'
        #take the root structure and copy it to a new structure with the new name
        #self.structures[newName] = self.structures[self.rootStructureName]

        modDate = datetime.now()

        self.structures[newName] = GdsStructure()
        self.structures[newName].name = newName



        self.rootStructureName = newName

        self.rootStructureName=newName

        #create the ROOT structure
        self.structures[self.rootStructureName] = GdsStructure()
        #self.structures[self.rootStructureName].name = name
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
        #first, find the root of the tree.
        #go through and get the name of every structure.
        #then, go through and find which structure is not
        #contained by any other structure. this is the root.
        structureNames=[]
        for name in self.structures:
            #print "deduceHierarchy: structure.name[%s]",name //FIXME: Added By Tom G.
            structureNames+=[name]
            
        for name in self.structures:
            if(len(self.structures[name].srefs)>0): #does this structure reference any others?
                for sref in self.structures[name].srefs: #go through each reference
                    if sref.sName in structureNames: #and compare to our list
                        structureNames.remove(sref.sName)
        
        self.rootStructureName = structureNames[0]

    def traverseTheHierarchy(self, startingStructureName=None, delegateFunction = None, 
                             transformPath = [], rotateAngle = 0, transFlags = (0,0,0), coordinates = (0,0)):
        #since this is a recursive function, must deal with the default
        #parameters explicitly        
        if startingStructureName == None:
            startingStructureName = self.rootStructureName            

        #set up the rotation matrix        
        if(rotateAngle == None or rotateAngle == ""):
            rotateAngle = 0
        else:
            rotateAngle = math.radians(float(rotateAngle))
        mRotate = mpmath.matrix([[math.cos(rotateAngle),-math.sin(rotateAngle),0.0],
                                 [math.sin(rotateAngle),math.cos(rotateAngle),0.0],[0.0,0.0,1.0],])
        #set up the translation matrix
        translateX = float(coordinates[0])
        translateY = float(coordinates[1])
        mTranslate = mpmath.matrix([[1.0,0.0,translateX],[0.0,1.0,translateY],[0.0,0.0,1.0]])
        #set up the scale matrix (handles mirror X)
        scaleX = 1.0
        if(transFlags[0]):
            scaleY = -1.0
        else:
            scaleY = 1.0
        mScale = mpmath.matrix([[scaleX,0.0,0.0],[0.0,scaleY,0.0],[0.0,0.0,1.0]])
        
        #we need to keep track of all transforms in the hierarchy
        #when we add an element to the xy tree, we apply all transforms from the bottom up
        transformPath += [(mRotate,mScale,mTranslate)]
        if delegateFunction != None:
            delegateFunction(startingStructureName, transformPath)
        #starting with a particular structure, we will recursively traverse the tree
        #********might have to set the recursion level deeper for big layouts!
        if(len(self.structures[startingStructureName].srefs)>0): #does this structure reference any others?
            #if so, go through each and call this function again
            #if not, return back to the caller (caller can be this function)            
            for sref in self.structures[startingStructureName].srefs:
                #here, we are going to modify the sref coordinates based on the parent objects rotation                
#                if (sref.sName.count("via") == 0): 
                self.traverseTheHierarchy(startingStructureName = sref.sName,                                    
                                          delegateFunction = delegateFunction,
                                          transformPath = transformPath,
                                          rotateAngle = sref.rotateAngle,
                                          transFlags = sref.transFlags,
                                          coordinates = sref.coordinates)
#            else:
#                print "WARNING: via encountered, ignoring:", sref.sName
            #MUST HANDLE AREFs HERE AS WELL
        #when we return, drop the last transform from the transformPath
        del transformPath[-1]
        return
    
    def initialize(self):
        self.deduceHierarchy()
        #self.traverseTheHierarchy()
        self.populateCoordinateMap()    
    
    def populateCoordinateMap(self):
        def addToXyTree(startingStructureName = None,transformPath = None):
        #print"populateCoordinateMap"            
            uVector = mpmath.matrix([1.0,0.0,0.0])  #start with normal basis vectors
            vVector = mpmath.matrix([0.0,1.0,0.0])
            origin = mpmath.matrix([0.0,0.0,1.0]) #and an origin (Z component is 1.0 to indicate position instead of vector)
            #make a copy of all the transforms and reverse it            
            reverseTransformPath = transformPath[:]
            if len(reverseTransformPath) > 1:
                reverseTransformPath.reverse()               
            #now go through each transform and apply them to our basis and origin in succession
            for transform in reverseTransformPath:
                origin = transform[0] * origin  #rotate
                uVector = transform[0] * uVector  #rotate
                vVector = transform[0] * vVector  #rotate
                origin = transform[1] * origin  #scale
                uVector = transform[1] * uVector  #rotate
                vVector = transform[1] * vVector  #rotate
                origin = transform[2] * origin  #translate
                #we don't need to do a translation on the basis vectors            
            self.xyTree+=[(startingStructureName,origin,uVector,vVector)]  #populate the xyTree with each
                                                                            #structureName and coordinate space
        self.traverseTheHierarchy(delegateFunction = addToXyTree)
        
    def microns(self,userUnits):
        """Utility function to convert user units to microns"""
        userUnit = self.units[1]/self.units[0]
        userUnitsPerMicron = userUnit / (userunit)
        layoutUnitsPerMicron = userUnitsPerMicron / self.units[0]
        return userUnits / layoutUnitsPerMicron
        
    def userUnits(self,microns):
        """Utility function to convert microns to user units"""
        userUnit = self.units[1]/self.units[0]
        #userUnitsPerMicron = userUnit / 1e-6
        userUnitsPerMicron = userUnit / (userUnit)
        layoutUnitsPerMicron = userUnitsPerMicron / self.units[0]
        #print "userUnit:",userUnit,"userUnitsPerMicron",userUnitsPerMicron,"layoutUnitsPerMicron",layoutUnitsPerMicron,[microns,microns*layoutUnitsPerMicron]
        return round(microns*layoutUnitsPerMicron,0)

    def changeRoot(self,newRoot, create=False):
        """
        Method to change the root pointer to another layout.
        """

        if self.debug: print "DEBUG:  GdsMill vlsiLayout: changeRoot: %s "%newRoot
    
        # Determine if newRoot exists
        #  layoutToAdd (default) or nameOfLayout
        if (newRoot == 0 | ((newRoot not in self.structures) & ~create)):
            print "ERROR:  vlsiLayout.changeRoot: Name of new root [%s] not found and create flag is false"%newRoot
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
        if self.debug==1: 
            print "DEBUG:  GdsMill vlsiLayout: addInstance: type %s, nameOfLayout "%type(layoutToAdd),nameOfLayout



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
                    if self.debug: print "DEBUG:  Structure %s Found"%StructureName
                    StructureFound = True



        # If layoutToAdd is a unique object (not this), then copy heirarchy, 
        #  otherwise, if it is a text name of an internal structure, use it.

        if layoutToAdd != self:
            #first, we need to combine the structure dictionaries from both layouts
            for structure in layoutToAdd.structures:
                if structure not in self.structures:
                    self.structures[structure]=layoutToAdd.structures[structure]
            #also combine the "layers in use" list
            for layerNumber in layoutToAdd.layerNumbersInUse:
                if layerNumber not in self.layerNumbersInUse:
                    self.layerNumbersInUse += [layerNumber]
            #Also, check if the user units / microns is the same as this Layout
            #if (layoutToAdd.units != self.units):
            #print "WARNING:  VlsiLayout: Units from design to be added do not match target Layout"

    #   if debug: print "DEBUG: vlsilayout: Using %d layers"

        # If we can't find the structure, error
        #if StructureFound == False:
            #print "ERROR:  vlsiLayout.addInstance: [%s] Name not found in local structures, "%(nameOfLayout)
            #return #FIXME: remove!
            #exit(1)


        #add a reference to the new layout structure in this layout's root
        layoutToAddSref = GdsSref()
        layoutToAddSref.sName = StructureName
        layoutToAddSref.coordinates = offsetInLayoutUnits

        if mirror or rotate:
        ########flags = (mirror around x-axis, absolute rotation, absolute magnification) 
            layoutToAddSref.transFlags = (False,False,False)
        #Below angles are angular angles(relative), not absolute
            if mirror=="R90":
                rotate = 90.0
            if mirror=="R180":
                rotate = 180.0
            if mirror=="R270":
                rotate = 270.0
            if rotate:
                layoutToAddSref.rotateAngle = rotate
            if mirror == "x" or mirror == "MX":
                layoutToAddSref.transFlags = (True,False,False)
            if mirror == "y" or mirror == "MY": #NOTE: "MY" option will override specified rotate angle
                layoutToAddSref.transFlags = (True,False,False)
                layoutToAddSref.rotateAngle = 180.0
            if mirror == "xy" or mirror == "XY": #NOTE: "XY" option will override specified rotate angle
                layoutToAddSref.transFlags = (False,False,False)
                layoutToAddSref.rotateAngle = 180.0

        #add the sref to the root structure
        self.structures[self.rootStructureName].srefs+=[layoutToAddSref]        
        
    def addBox(self,layerNumber=0, purposeNumber=None, offsetInMicrons=(0,0), width=1.0, height=1.0,center=False):
        """
        Method to add a box to a layout
        """
        offsetInLayoutUnits = (self.userUnits(offsetInMicrons[0]),self.userUnits(offsetInMicrons[1]))
        #print "addBox:offsetInLayoutUnits",offsetInLayoutUnits
        widthInLayoutUnits = self.userUnits(width)
        heightInLayoutUnits = self.userUnits(height)
        #print "offsetInLayoutUnits",widthInLayoutUnits,"heightInLayoutUnits",heightInLayoutUnits
        if not center:
            coordinates=[offsetInLayoutUnits,
                         (offsetInLayoutUnits[0]+widthInLayoutUnits,offsetInLayoutUnits[1]),
                         (offsetInLayoutUnits[0]+widthInLayoutUnits,offsetInLayoutUnits[1]+heightInLayoutUnits),
                         (offsetInLayoutUnits[0],offsetInLayoutUnits[1]+heightInLayoutUnits),
                         offsetInLayoutUnits]
        else:
            
            #is there where gdsmill is halving the coordinates???
            #if you printGDS of temp.gds, the header says 1 user unit = .0005 database units.  By default user units = .001. 
            #something to do with the ieeedouble in gdswriter.py???? 
            startPoint = (offsetInLayoutUnits[0]-widthInLayoutUnits/2, offsetInLayoutUnits[1]-heightInLayoutUnits/2) #width/2 height/2
            coordinates=[startPoint,
                         (startPoint[0]+widthInLayoutUnits,startPoint[1]),
                         (startPoint[0]+widthInLayoutUnits,startPoint[1]+heightInLayoutUnits),
                         (startPoint[0],startPoint[1]+heightInLayoutUnits),
                         startPoint]

        boundaryToAdd = GdsBoundary()
        boundaryToAdd.drawingLayer = layerNumber
        boundaryToAdd.dataType = 0
        boundaryToAdd.coordinates = coordinates
        boundaryToAdd.purposeLayer = purposeNumber
        #add the sref to the root structure
        self.structures[self.rootStructureName].boundaries+=[boundaryToAdd]
    
    def addPath(self, layerNumber=0, purposeNumber = None, coordinates=[(0,0)], width=1.0):
        """
        Method to add a path to a layout
        """
        widthInLayoutUnits = self.userUnits(width)
        layoutUnitCoordinates = []
        #first convert to proper units
        for coordinate in coordinates:
            cX = self.userUnits(coordinate[0])
            cY = self.userUnits(coordinate[1])
            layoutUnitCoordinates += [(cX,cY)]
        pathToAdd = GdsPath()
        pathToAdd.drawingLayer=layerNumber
        pathToAdd.purposeLayer = purposeNumber
        pathToAdd.pathWidth=widthInLayoutUnits
        pathToAdd.coordinates=layoutUnitCoordinates
        #add the sref to the root structure
        self.structures[self.rootStructureName].paths+=[pathToAdd]
        
    def addText(self, text, layerNumber=0, purposeNumber = None, offsetInMicrons=(0,0), magnification=0.1, rotate = None):
        offsetInLayoutUnits = (self.userUnits(offsetInMicrons[0]),self.userUnits(offsetInMicrons[1]))
        textToAdd = GdsText()
        textToAdd.drawingLayer = layerNumber
        textToAdd.purposeLayer = purposeNumber
        textToAdd.dataType = 0
        textToAdd.coordinates = [offsetInLayoutUnits]
        if(len(text)%2 == 1):
            #pad with a zero
            text = text + '\x00'
        textToAdd.textString = text
        textToAdd.transFlags = (False,False,True)
        textToAdd.magFactor = magnification
        if rotate:
            textToAdd.transFlags = (False,True,True)
            textToAdd.rotateAngle = rotate
        #add the sref to the root structure
        self.structures[self.rootStructureName].texts+=[textToAdd]
            
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
        #go through every point in the shape to test if they are all inside the box
        for point in shapeCoordinates:
            if not self.isPointInsideOfBox(point,boxCoordinates):
                return False
        return True
        
                
    def fillAreaDensity(self, layerToFill = 0, offsetInMicrons = (0,0), coverageWidth = 100.0, coverageHeight = 100.0,
                        minSpacing = 0.22, blockSize = 1.0):
        effectiveBlock = blockSize+minSpacing
        widthInBlocks = int(coverageWidth/effectiveBlock)
        heightInBlocks = int(coverageHeight/effectiveBlock)
        passFailRecord = []

        print "Filling layer:",layerToFill
        def isThisBlockOk(startingStructureName,coordinates,rotateAngle=None):
            #go through every boundary and check
            for boundary in self.structures[startingStructureName].boundaries:
                #only test shapes on the same layer
                if(boundary.drawingLayer == layerToFill):
                    #remap coordinates
                    shiftedBoundaryCoordinates = []
                    for shapeCoordinate in boundary.rotatedCoordinates(rotateAngle):
                        shiftedBoundaryCoordinates+=[(shapeCoordinate[0]+coordinates[0],shapeCoordinate[1]+coordinates[1])]
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
                        shiftedBoundaryCoordinates+=[(shapeCoordinate[0]+coordinates[0],shapeCoordinate[1]+coordinates[1])]
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
                passFailRecord+=[self.tempPassFail]
            print "Percent Complete:"+str(percentDone)

                
        passFailIndex=0
        for yIndex in range(0,heightInBlocks):
            for xIndex in range(0,widthInBlocks):
                blockX = (xIndex*effectiveBlock)+offsetInMicrons[0]
                blockY = (yIndex*effectiveBlock)+offsetInMicrons[1]
                if passFailRecord[passFailIndex]:
                    self.addBox(layerToFill, (blockX,blockY), width=blockSize, height=blockSize)
                passFailIndex+=1
        print "Done\n\n"

    def getLayoutBorder(self,borderlayer):
        for boundary in self.structures[self.rootStructureName].boundaries:
            if boundary.drawingLayer==borderlayer:
                if self.debug: print "Find border "+str(boundary.coordinates)
                left_bottom=boundary.coordinates[0]
                right_top=boundary.coordinates[2]
                cellSize=[right_top[0]-left_bottom[0],right_top[1]-left_bottom[1]]
                cellSizeMicron=[cellSize[0]*self.units[0],cellSize[1]*self.units[0]]
        if not(cellSizeMicron):
            print "Error: "+str(self.rootStructureName)+".cell_size information not found yet"
        return cellSizeMicron

    def measureSize(self,startStructure):
        self.rootStructureName=startStructure
        self.populateCoordinateMap()
        cellBoundary = [None, None, None, None]
        for TreeUnit in self.xyTree:
            cellBoundary=self.measureSizeInStructure(TreeUnit,cellBoundary)
        cellSize=[cellBoundary[2]-cellBoundary[0],cellBoundary[3]-cellBoundary[1]]
        cellSizeMicron=[cellSize[0]*self.units[0],cellSize[1]*self.units[0]]
        return cellSizeMicron

    def measureBoundary(self,startStructure):
        self.rootStructureName=startStructure
        self.populateCoordinateMap()
        cellBoundary = [None, None, None, None]
        for TreeUnit in self.xyTree:
            cellBoundary=self.measureSizeInStructure(TreeUnit,cellBoundary)
        return [[self.units[0]*cellBoundary[0],self.units[0]*cellBoundary[1]],
                [self.units[0]*cellBoundary[2],self.units[0]*cellBoundary[3]]]
    
    def measureSizeInStructure(self,Structure,cellBoundary):
        StructureName=Structure[0]
        StructureOrigin=[Structure[1][0],Structure[1][1]]
        StructureuVector=[Structure[2][0],Structure[2][1],Structure[2][2]]
        StructurevVector=[Structure[3][0],Structure[3][1],Structure[3][2]]
        #debug.info(debug_level,"Checking Structure: "+str(StructureName))
        #debug.info(debug_level,"-Structure Structure Origin:"+str(StructureOrigin))
        #debug.info(debug_level,"-Structure direction: uVector["+str(StructureuVector)+"]")
        #debug.info(debug_level,"-Structure direction: vVector["+str(StructurevVector)+"]")
        
        for boundary in self.structures[str(StructureName)].boundaries:
            left_bottom=boundary.coordinates[0]
            right_top=boundary.coordinates[2]
            thisBoundary=[left_bottom[0],left_bottom[1],right_top[0],right_top[1]]
            thisBoundary=self.transformRectangle(thisBoundary,StructureuVector,StructurevVector)
            thisBoundary=[thisBoundary[0]+StructureOrigin[0],thisBoundary[1]+StructureOrigin[1],
            thisBoundary[2]+StructureOrigin[0],thisBoundary[3]+StructureOrigin[1]]
            cellBoundary=self.updateBoundary(thisBoundary,cellBoundary)
        return cellBoundary
        
    def updateBoundary(self,thisBoundary,cellBoundary):
        [left_bott_X,left_bott_Y,right_top_X,right_top_Y]=thisBoundary
        if cellBoundary==[None,None,None,None]:
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


    def getLabelDBInfo(self,label_name):
        """
        Return the coordinates in DB units and layer of a label
        """
        label_layer = None
        label_coordinate = [None, None]

        # Why must this be the last one found? It breaks if we return the first.
        for Text in self.structures[self.rootStructureName].texts:
            if Text.textString == label_name or Text.textString == label_name+"\x00":
                label_layer = Text.drawingLayer
                label_coordinate = Text.coordinates[0]

        return (label_coordinate, label_layer)


    def getLabelInfo(self,label_name):
        """
        Return the coordinates in USER units and layer of a label
        """
        (label_coordinate,label_layer)=self.getLabelDBInfo(label_name)
        user_coordinates = [x*self.units[0] for x in label_coordinate]
        return (user_coordinates,label_layer)
    
    def getPinShapeByLocLayer(self, coordinate, layer):
        """
        Return the largest enclosing rectangle on a layer and at a location.
        Coordinates should be in USER units.
        """
        db_coordinate = [x/self.units[0] for x in coordinate]
        return self.getPinShapeByDBLocLayer(db_coordinate, layer)

    def getPinShapeByDBLocLayer(self, coordinate, layer):
        """
        Return the largest enclosing rectangle on a layer and at a location.
        Coordinates should be in DB units.
        """
        pin_boundaries=self.getAllPinShapesInStructureList(coordinate, layer)

        # sort the boundaries, return the max area pin boundary
        pin_boundaries.sort(cmpBoundaryAreas,reverse=True)
        pin_boundary=pin_boundaries[0]

        # Convert to USER units
        pin_boundary=[pin_boundary[0]*self.units[0],pin_boundary[1]*self.units[0],
                      pin_boundary[2]*self.units[0],pin_boundary[3]*self.units[0]]
        
        # Make a name if we don't have the pin name
        return ["p"+str(coordinate)+"_"+str(layer), layer, pin_boundary]

    def getAllPinShapesByLocLayer(self, coordinate, layer):
        """
        Return ALL the enclosing rectangles on the same layer
        at the given coordinate. Coordinates should be in USER units.
        """
        db_coordinate = [int(x/self.units[0]) for x in coordinate]
        return self.getAllPinShapesByDBLocLayer(db_coordinate, layer)

    def getAllPinShapesByDBLocLayer(self, coordinate, layer):
        """
        Return ALL the enclosing rectangles on the same layer
        at the given coordinate. Coordinates should be in DB units.
        """
        pin_boundaries=self.getAllPinShapesInStructureList(coordinate, layer)

        # Convert to user units
        new_boundaries = []
        for pin_boundary in pin_boundaries:
            new_boundaries.append([pin_boundary[0]*self.units[0],pin_boundary[1]*self.units[0],
                                   pin_boundary[2]*self.units[0],pin_boundary[3]*self.units[0]])

        # Make a name if we don't have the pin name
        return ["p"+str(coordinate)+"_"+str(layer), layer, new_boundaries]
    
    def getPinShapeByLabel(self,label_name):
        """
        Search for a pin label and return the largest enclosing rectangle
        on the same layer as the pin label.
        """
        (label_coordinate,label_layer)=self.getLabelDBInfo(label_name)
        return self.getPinShapeByDBLocLayer(label_coordinate, label_layer)

    def getAllPinShapesByLabel(self,label_name):
        """
        Search for a pin label and return ALL the enclosing rectangles on the same layer
        as the pin label.
        """
        (label_coordinate,label_layer)=self.getLabelDBInfo(label_name)
        return self.getAllPinShapesByDBLocLayer(label_coordinate, label_layer)
    
    def getAllPinShapesInStructureList(self,coordinates,layer):
        """
        Given a coordinate, search for enclosing structures on the given layer.
        Return all pin shapes.
        """
        boundaries = []

        for TreeUnit in self.xyTree:
            boundaries += self.getPinInStructure(coordinates,layer,TreeUnit)

        return boundaries


    def getPinInStructure(self,coordinates,layer,Structure):
        """ 
        Go through all the shapes in a structure and return the list of shapes
        that the label coordinates are inside.
        """
        StructureName=Structure[0]
        StructureOrigin=[Structure[1][0],Structure[1][1]]
        StructureuVector=[Structure[2][0],Structure[2][1],Structure[2][2]]
        StructurevVector=[Structure[3][0],Structure[3][1],Structure[3][2]]

        boundaries = []
        
        for boundary in self.structures[str(StructureName)].boundaries:
            if layer==boundary.drawingLayer:
                left_bottom=boundary.coordinates[0]
                right_top=boundary.coordinates[2]
                MetalBoundary=[left_bottom[0],left_bottom[1],right_top[0],right_top[1]]
                MetalBoundary=self.transformRectangle(MetalBoundary,StructureuVector,StructurevVector)
                MetalBoundary=[MetalBoundary[0]+StructureOrigin[0],MetalBoundary[1]+StructureOrigin[1],
                MetalBoundary[2]+StructureOrigin[0],MetalBoundary[3]+StructureOrigin[1]]

                if self.labelInRectangle(coordinates,MetalBoundary):
                    boundaries.append(MetalBoundary)
                    
        return boundaries

    def transformRectangle(self,orignalRectangle,uVector,vVector):
        """
        Transforms the four coordinates of a rectangle in space
        and recomputes the left, bottom, right, top values.
        """
        leftBottom=mpmath.matrix([orignalRectangle[0],orignalRectangle[1]])
        leftBottom=self.transformCoordinate(leftBottom,uVector,vVector)

        rightTop=mpmath.matrix([orignalRectangle[2],orignalRectangle[3]])
        rightTop=self.transformCoordinate(rightTop,uVector,vVector)

        left=min(leftBottom[0],rightTop[0])
        bottom=min(leftBottom[1],rightTop[1])
        right=max(leftBottom[0],rightTop[0])
        top=max(leftBottom[1],rightTop[1])

        return [left,bottom,right,top]

    def transformCoordinate(self,coordinate,uVector,vVector):
        """
        Rotate a coordinate in space.
        """
        x=coordinate[0]*uVector[0]+coordinate[1]*uVector[1]
        y=coordinate[1]*vVector[1]+coordinate[0]*vVector[0]
        transformCoordinate=[x,y]

        return transformCoordinate


    def labelInRectangle(self,coordinate,rectangle):
        """
        Checks if a coordinate is within a given rectangle.
        """
        coordinate_In_Rectangle_x_range=(coordinate[0]>=int(rectangle[0]))&(coordinate[0]<=int(rectangle[2]))
        coordinate_In_Rectangle_y_range=(coordinate[1]>=int(rectangle[1]))&(coordinate[1]<=int(rectangle[3]))
        if coordinate_In_Rectangle_x_range & coordinate_In_Rectangle_y_range:
            return True
        else:
            return False

def cmpBoundaryAreas(A,B):
    """
    Compares two rectangles and return true if Area(A)>Area(B).
    """
    area_A=(A[2]-A[0])*(A[3]-A[1])
    area_B=(B[2]-B[0])*(B[3]-B[1])
    if area_A>area_B:
        return 1
    elif area_A==area_B:
        return 0
    else:
        return -1


    
