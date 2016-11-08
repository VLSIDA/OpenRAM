from gdsPrimitives import *
from datetime import *
import mpmath
import gdsPrimitives
import debug
debug_level=4

class VlsiLayout:
    """Class represent a hierarchical layout"""

    def __init__(self, name=None, units=(0.001,1e-9), libraryName = "DEFAULT.DB", gdsVersion=5):
        #keep a list of all the structures in this layout
        self.units = units
        #print units
        modDate = datetime.now()
        self.structures=dict()
        self.layerNumbersInUse = []
        self.debug = debug
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

    def strip_non_ascii(string):
        ''' Returns the string without non ASCII characters'''
        stripped = (c for c in string if 0 < ord(c) < 127)
        return ''.join(stripped)

    
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

        #if self.debug: print "DEBUG:  GdsMill vlsiLayout: changeRoot: %s "%newRoot
        debug.info(debug_level,"DEBUG:  GdsMill vlsiLayout: changeRoot: %s "%newRoot)
    
        # Determine if newRoot exists
        #  layoutToAdd (default) or nameOfLayout
        if (newRoot == 0 | ((newRoot not in self.structures) & ~create)):
            #print "ERROR:  vlsiLayout.changeRoot: Name of new root [%s] not found and create flag is false"%newRoot
            debug.error(debug_level,"ERROR:  vlsiLayout.changeRoot: Name of new root [%s] not found and create flag is false"+str(newRoot))
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
        #print "addInstance:offsetInLayoutUnits",offsetInLayoutUnits
        #offsetInLayoutUnits = ((offsetInMicrons[0]),(offsetInMicrons[1]))
        #print "DEBUG: addInstance offsetInLayoutUnits: %f, %f"%(self.userUnits(offsetInMicrons[0]), self.userUnits(offsetInMicrons[1]))
        #if self.debug==1: 
        #   print "DEBUG:  GdsMill vlsiLayout: addInstance: type %s, nameOfLayout "%type(layoutToAdd),nameOfLayout
        #   print offsetInMicrons       
        #   print offsetInLayoutUnits
        debug.info(debug_level,"DEBUG:  GdsMill vlsiLayout: addInstance: type "+str(layoutToAdd.rootStructureName))
        debug.info(debug_level,"offset In Microns:"+str(offsetInMicrons)+"offset In LayoutUnits:"+str(offsetInLayoutUnits))



        # Determine if we are instantiating the root design of 
        #  layoutToAdd (default) or nameOfLayout
        if nameOfLayout == 0:
            StructureFound = True
            StructureName = layoutToAdd.rootStructureName
        else:
            StructureName = nameOfLayout #layoutToAdd
            StructureFound = False
            for structure in layoutToAdd.structures:
        #       if self.debug: print structure, "N","N"
                if StructureName in structure: 
                    debug.info(debug_level,"DEBUG:  Structure %s Found"+str(StructureName))
                    #if self.debug: print "DEBUG:  Structure %s Found"%StructureName
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

        debug.info(debug_level,"Filling layer:"+str(layerToFill))        
        #print "Filling layer:",layerToFill
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
            debug.info(debug_level,"Percent Complete:"+str(percentDone)) 

                
        passFailIndex=0
        for yIndex in range(0,heightInBlocks):
            for xIndex in range(0,widthInBlocks):
                blockX = (xIndex*effectiveBlock)+offsetInMicrons[0]
                blockY = (yIndex*effectiveBlock)+offsetInMicrons[1]
                if passFailRecord[passFailIndex]:
                    self.addBox(layerToFill, (blockX,blockY), width=blockSize, height=blockSize)
                passFailIndex+=1
        debug.info(debug_level,"Done\n\n")

    def readLayoutBorder(self,borderlayer):
        for boundary in self.structures[self.rootStructureName].boundaries:
            if boundary.drawingLayer==borderlayer:
                debug.info(debug_level,"Find border "+str(boundary.coordinates))
                left_button=boundary.coordinates[0]
                right_top=boundary.coordinates[2]
                cellSize=[right_top[0]-left_button[0],right_top[1]-left_button[1]]
                cellSizeMicron=[cellSize[0]*self.units[0],cellSize[1]*self.units[0]]
        if not(cellSizeMicron):
            debug.error("Error: "+str(self.rootStructureName)+".cell_size information not found yet")
        return cellSizeMicron

    def measureSize(self,startStructure):
        self.rootStructureName=startStructure
        self.populateCoordinateMap()
        cellBoundary = [None, None, None, None]
        for TreeUnit in self.xyTree:
            cellBoundary=self.measureSizeInStruture(TreeUnit,cellBoundary)
        cellSize=[cellBoundary[2]-cellBoundary[0],cellBoundary[3]-cellBoundary[1]]
        cellSizeMicron=[cellSize[0]*self.units[0],cellSize[1]*self.units[0]]
        return cellSizeMicron

    def measureSizeInStruture(self,Struture,cellBoundary):
        StrutureName=Struture[0]
        StrutureOrgin=[Struture[1][0],Struture[1][1]]
        StrutureuVector=[Struture[2][0],Struture[2][1],Struture[2][2]]
        StruturevVector=[Struture[3][0],Struture[3][1],Struture[3][2]]
        debug.info(debug_level,"Checking Structure: "+str(StrutureName))
        debug.info(debug_level,"-Structure Struture Orgin:"+str(StrutureOrgin))
        debug.info(debug_level,"-Structure direction: uVector["+str(StrutureuVector)+"]")
        debug.info(debug_level,"-Structure direction: vVector["+str(StruturevVector)+"]")
        
        for boundary in self.structures[str(StrutureName)].boundaries:
            left_button=boundary.coordinates[0]
            right_top=boundary.coordinates[2]
            thisBoundary=[left_button[0],left_button[1],right_top[0],right_top[1]]
            thisBoundary=self.tranformRectangle(thisBoundary,StrutureuVector,StruturevVector)
            thisBoundary=[thisBoundary[0]+StrutureOrgin[0],thisBoundary[1]+StrutureOrgin[1],
            thisBoundary[2]+StrutureOrgin[0],thisBoundary[3]+StrutureOrgin[1]]
            cellBoundary=self.update_boundary(thisBoundary,cellBoundary)
        return cellBoundary
        
    def update_boundary(self,thisBoundary,cellBoundary):   
        [left_butt_X,left_butt_Y,right_top_X,right_top_Y]=thisBoundary
        if cellBoundary==[None,None,None,None]:
            cellBoundary=thisBoundary
        else:
            if cellBoundary[0]>left_butt_X:
                cellBoundary[0]=left_butt_X
            if cellBoundary[1]>left_butt_Y:
                cellBoundary[1]=left_butt_Y
            if cellBoundary[2]<right_top_X:
                cellBoundary[2]=right_top_X
            if cellBoundary[3]<right_top_Y:
                cellBoundary[3]=right_top_Y
        return cellBoundary
        
    def readPin(self,label_name,mod="offset"):
        label_layer = None
        label_coordinate = [None, None]

        for Text in self.structures[self.rootStructureName].texts:
            debug.info(debug_level,"Check Text object "+str(Text.textString)+" in "+str(self.rootStructureName))
            debug.info(debug_level,"Length of text object: "+str(len(Text.textString)))
            if Text.textString == label_name or Text.textString == label_name+"\x00":
                label_layer = Text.drawingLayer
                label_coordinate = Text.coordinates
                debug.info(debug_level,"Find label "+str(Text.textString)+" at "+str(Text.coordinates))

        pin_boundary=self.readPinInStructureList(label_coordinate, label_layer)
        debug.info(debug_level, "Find pin covers "+str(label_name)+" at "+str(pin_boundary))

        pin_boundary=[pin_boundary[0]*self.units[0],pin_boundary[1]*self.units[0],pin_boundary[2]*self.units[0],pin_boundary[3]*self.units[0]]
        return [label_name, label_layer, pin_boundary]

    def readPinInStructureList(self,label_coordinates,layer):
        label_boundary = [None,None,None,None]
        for TreeUnit in self.xyTree:
            label_boundary=self.readPinInStruture(label_coordinates,layer,TreeUnit,label_boundary)
        return label_boundary


    def readPinInStruture(self,label_coordinates,layer,Struture,label_boundary):
        StrutureName=Struture[0]
        StrutureOrgin=[Struture[1][0],Struture[1][1]]
        StrutureuVector=[Struture[2][0],Struture[2][1],Struture[2][2]]
        StruturevVector=[Struture[3][0],Struture[3][1],Struture[3][2]]
        debug.info(debug_level,"Checking Structure: "+str(StrutureName))
        debug.info(debug_level,"-Structure Struture Orgin:"+str(StrutureOrgin))
        debug.info(debug_level,"-Structure direction: uVector["+str(StrutureuVector)+"]")
        debug.info(debug_level,"-Structure direction: vVector["+str(StruturevVector)+"]")

        for boundary in self.structures[str(StrutureName)].boundaries:
            if layer==boundary.drawingLayer:
                left_button=boundary.coordinates[0]
                right_top=boundary.coordinates[2]
                MetalBoundary=[left_button[0],left_button[1],right_top[0],right_top[1]]
                MetalBoundary=self.tranformRectangle(MetalBoundary,StrutureuVector,StruturevVector)
                MetalBoundary=[MetalBoundary[0]+StrutureOrgin[0],MetalBoundary[1]+StrutureOrgin[1],
                MetalBoundary[2]+StrutureOrgin[0],MetalBoundary[3]+StrutureOrgin[1]]

                result = self.labelInRectangle(label_coordinates[0],MetalBoundary)
                if (result):
                    debug.info(debug_level,"Rectangle(layer"+str(layer)+") at "+str(MetalBoundary))
                    debug.info(debug_level,"covers label (offset"+str(label_coordinates)+")")
                    label_boundary=self.returnBiggerBoundary(MetalBoundary,label_boundary)
        return label_boundary

    def tranformRectangle(self,orignalRectangle,uVector,vVector):
        LeftButton=mpmath.matrix([orignalRectangle[0],orignalRectangle[1]])
        LeftButton=self.tranformCoordinate(LeftButton,uVector,vVector)

        RightUp=mpmath.matrix([orignalRectangle[2],orignalRectangle[3]])
        RightUp=self.tranformCoordinate(RightUp,uVector,vVector)

        Left=min(LeftButton[0],RightUp[0])
        Button=min(LeftButton[1],RightUp[1])
        Right=max(LeftButton[0],RightUp[0])
        Up=max(LeftButton[1],RightUp[1])

        return [Left,Button,Right,Up]

    def tranformCoordinate(self,Coordinate,uVector,vVector):
        x=Coordinate[0]*uVector[0]+Coordinate[1]*uVector[1]
        y=Coordinate[1]*vVector[1]+Coordinate[0]*vVector[0]
        tranformCoordinate=[x,y]
        return tranformCoordinate


    def labelInRectangle(self,label_coordinate,Rectangle):
        coordinate_In_Rectangle_x_range=(label_coordinate[0]>=int(Rectangle[0]))&(label_coordinate[0]<=int(Rectangle[2]))
        coordinate_In_Rectangle_y_range=(label_coordinate[1]>=int(Rectangle[1]))&(label_coordinate[1]<=int(Rectangle[3]))
        if coordinate_In_Rectangle_x_range & coordinate_In_Rectangle_y_range:
            return True
        else:
            return False

    def returnBiggerBoundary(self,comparedRectangle,label_boundary):
        if label_boundary[0]== None:
            label_boundary=comparedRectangle
            debug.info(debug_level,"The label_boundary is initialized to "+str(label_boundary))
        else:
            area_label_boundary=(label_boundary[2]-label_boundary[0])*(label_boundary[3]-label_boundary[1])
            area_comparedRectangle=(comparedRectangle[2]-comparedRectangle[0])*(comparedRectangle[3]-comparedRectangle[1])
            if area_label_boundary<=area_comparedRectangle:
                label_boundary = comparedRectangle
                debug.info(debug_level,"The label_boundary is updated to "+str(label_boundary))
        return label_boundary

