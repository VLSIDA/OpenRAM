#!/usr/bin/env python
import struct
from .gdsPrimitives import *

class Gds2reader:
    """Class to read in a file in GDSII format and populate a layout class with it"""
    ## Based on info from http://www.rulabinsky.com/cavd/text/chapc.html
    global offset
    offset=0

    def __init__(self,layoutObject,debugToTerminal = 0):
        self.fileHandle = None
        self.layoutObject = layoutObject
        self.debugToTerminal=debugToTerminal

          #do we dump debug data to the screen

    def print64AsBinary(self,number):
        for index in range(0,64):
            print((number>>(63-index))&0x1,eol='')
        print("\n")

    def stripNonASCII(self,bytestring):
        string = bytestring.decode('utf-8')
        return string

    def ieeeDoubleFromIbmData(self,ibmData):
       #the GDS double is in IBM 370 format like this:
       #(1)sign (7)exponent (56)mantissa
       #exponent is excess 64, mantissa has no implied 1
       #a normal IEEE double is like this:
       #(1)sign (11)exponent (52)mantissa
       data = struct.unpack('>q',ibmData)[0]
       sign = (data >> 63)&0x01
       exponent = (data >> 56) & 0x7f
       mantissa = data<<8 #chop off sign and exponent

       if mantissa == 0:
           newFloat = 0.0
       else:
           exponent = ((exponent-64)*4)+1023 #convert to double exponent
           #re normalize
           while mantissa & 0x8000000000000000 == 0:
               mantissa<<=1
               exponent-=1
           mantissa<<=1  #remove the assumed high bit
           exponent-=1
           #check for underflow error  -- should handle these properly!
           if(exponent<=0):
               print("Underflow Error")
           elif(exponent == 2047):
               print("Overflow Error")
           #re assemble
           newFloat=(sign<<63)|(exponent<<52)|((mantissa>>12)&0xfffffffffffff)
           asciiDouble = struct.pack('>q',newFloat)
           #convert back to double
           newFloat = struct.unpack('>d',asciiDouble)[0]
       return newFloat

    def ieeeFloatCheck(self,aFloat):
        asciiDouble = struct.pack('>d',aFloat)
        data = struct.unpack('>q',asciiDouble)[0]
        sign = data >> 63
        exponent = ((data >> 52) & 0x7ff)-1023
	# BINWU: Cleanup
        #print(exponent+1023)
        mantissa = data << 12 #chop off sign and exponent
	# BINWU: Cleanup
        #self.print64AsBinary((sign<<63)|((exponent+1023)<<52)|(mantissa>>12))
        asciiDouble = struct.pack('>q',(sign<<63)|(exponent+1023<<52)|(mantissa>>12))
        newFloat = struct.unpack('>d',asciiDouble)[0]
        print("Check:"+str(newFloat))

    def readNextRecord(self):
        global offset
        recordLengthAscii = self.fileHandle.read(2) #first 2 bytes tell us the length of the record
        if len(recordLengthAscii)==0:
            return
        recordLength = struct.unpack(">h",recordLengthAscii)  #gives us a tuple with a short int inside
        offset_int = int(recordLength[0])  # extract length
        offset += offset_int  # count offset
        if(self.debugToTerminal==1):
            print("Offset: " + str(offset))  #print out the record numbers for de-bugging
        record = self.fileHandle.read(recordLength[0]-2) #read the rest of it (first 2 bytes were already read)
        return record

    def readHeader(self):
        self.layoutObject.info.clear()
        ##  Header
        record = self.readNextRecord()
        idBits = record[0:2]
        if(idBits==b'\x00\x02' and len(record)==4):
            gdsVersion = struct.unpack(">h",record[2:4])[0]
            self.layoutObject.info["gdsVersion"]=gdsVersion
            if(self.debugToTerminal==1):
                print("GDS II Version "+str(gdsVersion))
        else:
            print("Invalid GDSII Header")
            return -1

        #read records until we hit the UNITS section... this is the last part of the header
        while 1:
            record = self.readNextRecord()
            idBits = record[0:2]
            ## Modified Date
            if idBits==b'\x01\x02' and len(record)==26:
                modYear = struct.unpack(">h",record[2:4])[0]
                modMonth = struct.unpack(">h",record[4:6])[0]
                modDay = struct.unpack(">h",record[6:8])[0]
                modHour = struct.unpack(">h",record[8:10])[0]
                modMinute = struct.unpack(">h",record[10:12])[0]
                modSecond = struct.unpack(">h",record[12:14])[0]
                lastAccessYear = struct.unpack(">h",record[14:16])[0]
                lastAccessMonth = struct.unpack(">h",record[16:18])[0]
                lastAccessDay = struct.unpack(">h",record[18:20])[0]
                lastAccessHour = struct.unpack(">h",record[20:22])[0]
                lastAccessMinute = struct.unpack(">h",record[22:24])[0]
                lastAccessSecond = struct.unpack(">h",record[24:26])[0]
                self.layoutObject.info["dates"]=(modYear,modMonth,modDay,modHour,modMinute,modSecond,\
                                                 lastAccessYear,lastAccessMonth,lastAccessDay,lastAccessHour,lastAccessMinute,lastAccessSecond)
                if(self.debugToTerminal==1):
                    print("Date Modified:"+str(modYear)+","+str(modMonth)+","+str(modDay)+","+str(modHour)+","+str(modMinute)+","+str(modSecond))
                    print("Date Last Accessed:"+str(lastAccessYear)+","+str(lastAccessMonth)+","+str(lastAccessDay)+\
                            ","+str(lastAccessHour)+","+str(lastAccessMinute)+","+str(lastAccessSecond))
            ##  LibraryName
            elif(idBits==b'\x02\x06'):
                libraryName = record[2::].decode("utf-8")
                self.layoutObject.info["libraryName"]=libraryName
                if(self.debugToTerminal==1):
                    print("Library: "+libraryName)
            ## reference libraries
            elif(idBits==b'\x1F\x06'):
                referenceLibraryA = record[2:46]
                referenceLibraryB = record[47:91]
                self.layoutObject.info["referenceLibraries"]=(referenceLibraryA,referenceLibraryB)
                if(self.debugToTerminal==1):
                    print( "Reference Libraries:"+referenceLibraryA+","+referenceLibraryB)
            elif(idBits==b'\x20\x06'):
                fontA = record[2:45]
                fontB = record[46:89]
                fontC = record[90:133]
                fontD = record[134:177]
                self.layoutObject.info["fonts"]=(fontA,fontB,fontC,fontD)
                if(self.debugToTerminal==1):
                    print("Fonts:"+fontA+","+fontB+","+fontC+","+fontD)
            elif(idBits==b'\x23\x06'):
                attributeTable = record[2:45]
                self.layoutObject.info["attributeTable"]=attributeTable
                if(self.debugToTerminal==1):
                    print("Attributes:"+attributeTable)
            elif(idBits==b'\x22\x02'):
                generations = struct.unpack(">h",record[2]+record[3])
                self.layoutObject.info["generations"]=generations
                if(self.debugToTerminal==1):
                    print("Generations:"+generations                )
            elif(idBits==b'\x36\x02'):
                fileFormat = struct.unpack(">h",record[2]+record[3])
                self.layoutObject.info["fileFormat"]=fileFormat
                if(self.debugToTerminal==1):
                    print("File Format:"+fileFormat)
            elif(idBits==b'\x37\x06'):
                mask = record[2::]
                self.layoutObject.info["mask"] = mask
                if(self.debugToTerminal==1):
                    print("Mask: "+mask)
            elif(idBits==b'\x03\x05'):  #this is also wrong b/c python doesn't natively have an 8 byte float
                userUnits=self.ieeeDoubleFromIbmData(record[2:10])
                dbUnits=self.ieeeDoubleFromIbmData(record[10:18])
                self.layoutObject.info["units"] = (userUnits,dbUnits)
                if(self.debugToTerminal==1):
                    print("Units: 1 user unit="+str(userUnits)+" database units, 1 database unit="+str(dbUnits)+" meters.")
                break;
        if(self.debugToTerminal==1):
            print("End of GDSII Header Found")
        return 1

    def readBoundary(self):
        ##reads in a boundary type structure = a filled polygon
        if(self.debugToTerminal==1):
            print("\t\tBeginBoundary")
        thisBoundary=GdsBoundary()
        while 1:
            record = self.readNextRecord()
            idBits = record[0:2]
            if(idBits==b'\x26\x01'):  #ELFLAGS
                elementFlags = struct.unpack(">h",record[2:4])[0]
                thisBoundary.elementFlags=elementFlags
                if(self.debugToTerminal==1):
                    print("\t\tElement Flags: "+str(elementFlags))
            elif(idBits==b'\x2F\x03'):  #PLEX
                plex = struct.unpack(">i",record[2:6])[0]
                thisBoundary.plex=plex
                if(self.debugToTerminal==1):
                    print("\t\tPLEX: "+str(plex))
            elif(idBits==b'\x0D\x02'):  #Layer
                drawingLayer = struct.unpack(">h",record[2:4])[0]
                thisBoundary.drawingLayer=drawingLayer
                if drawingLayer not in self.layoutObject.layerNumbersInUse:
                    self.layoutObject.layerNumbersInUse += [drawingLayer]
                if(self.debugToTerminal==1):
                    print("\t\tDrawing Layer: "+str(drawingLayer))
            elif(idBits==b'\x0E\x02'):  #Purpose DATATYPE
                purposeLayer = struct.unpack(">h",record[2:4])[0]
                thisBoundary.purposeLayer=purposeLayer
                if(self.debugToTerminal==1):
                    print("\t\tPurpose Layer: "+str(purposeLayer))
            elif(idBits==b'\x10\x03'):  #XY Data Points
                numDataPoints = len(record)-2  #packed as XY coordinates 4 bytes each
                thisBoundary.coordinates=[]
                for index in range(2,numDataPoints+2,8):  #incorporate the 2 byte offset
                    x=struct.unpack(">i",record[index:index+4])[0]
                    y=struct.unpack(">i",record[index+4:index+8])[0]
                    thisBoundary.coordinates+=[(x,y)]
                    if(self.debugToTerminal==1):
                        print("\t\t\tXY Point: "+str(x)+","+str(y))
            elif(idBits==b'\x11\x00'):  #End Of Element
                if(self.debugToTerminal==1):
                    print("\t\tEndBoundary")
                break;
        return thisBoundary

    def readPath(self):  #reads in a path structure
        if(self.debugToTerminal==1):
            print("\t\tBeginPath")

        thisPath=GdsPath()
        while 1:
            record = self.readNextRecord()
            idBits = record[0:2]
            if(idBits==b'\x26\x01'):  #ELFLAGS
                elementFlags = struct.unpack(">h",record[2:4])[0]
                thisPath.elementFlags=elementFlags
                if(self.debugToTerminal==1):
                    print("\t\tElement Flags: "+str(elementFlags))
            elif(idBits==b'\x2F\x03'):  #PLEX
                plex = struct.unpack(">i",record[2:6])[0]
                thisPath.plex=plex
                if(self.debugToTerminal==1):
                    print("\t\tPLEX: "+str(plex))
            elif(idBits==b'\x0D\x02'):  #Layer
                drawingLayer = struct.unpack(">h",record[2:4])[0]
                thisPath.drawingLayer=drawingLayer
                if drawingLayer not in self.layoutObject.layerNumbersInUse:
                    self.layoutObject.layerNumbersInUse += [drawingLayer]
                if(self.debugToTerminal==1):
                    print("\t\t\tDrawing Layer: "+str(drawingLayer))
            elif(idBits==b'\x16\x02'):  #Purpose
                purposeLayer = struct.unpack(">h",record[2:4])[0]
                thisPath.purposeLayer=purposeLayer
                if(self.debugToTerminal==1):
                    print("\t\tPurpose Layer: "+str(purposeLayer))
            elif(idBits==b'\x21\x02'):  #Path type
                pathType = struct.unpack(">h",record[2:4])[0]
                thisPath.pathType=pathType
                if(self.debugToTerminal==1):
                    print("\t\t\tPath Type: "+str(pathType))
            elif(idBits==b'\x0E\x02'):  #Data type
                dataType = struct.unpack(">h",record[2:4])[0]
                thisPath.dataType=dataType
                if(self.debugToTerminal==1):
                    print("\t\t\tData Type: "+str(dataType))
            elif(idBits==b'\x0F\x03'):  #Path width
                pathWidth = struct.unpack(">i",record[2:6])[0]
                thisPath.pathWidth=pathWidth
                if(self.debugToTerminal==1):
                    print("\t\t\tPath Width: "+str(pathWidth))
            elif(idBits==b'\x10\x03'):  #XY Data Points
                numDataPoints = len(record)-2  #packed nas XY coordinates 4 bytes each
                thisPath.coordinates=[]
                for index in range(2,numDataPoints+2,8):  #incorporate the 2 byte offset
                    x=struct.unpack(">i",record[index:index+4])[0]
                    y=struct.unpack(">i",record[index+4:index+8])[0]
                    thisPath.coordinates+=[(x,y)]
                    if(self.debugToTerminal==1):
                        print("\t\t\tXY Point: "+str(x)+","+str(y))
            elif(idBits==b'\x11\x00'):  #End Of Element
                if(self.debugToTerminal==1):
                    print("\t\tEndPath")
                break;
        return thisPath

    def readSref(self):  #reads in a reference to another structure
        if(self.debugToTerminal==1):
            print("\t\t\tBeginSref")

        thisSref=GdsSref()
        while 1:
            record = self.readNextRecord()
            idBits = record[0:2]
            if(idBits==b'\x26\x01'):  #ELFLAGS
                elementFlags = struct.unpack(">h",record[2:4])[0]
                thisSref.elementFlags=elementFlags
                if(self.debugToTerminal==1):
                    print("\t\tElement Flags: "+str(elementFlags))
            elif(idBits==b'\x2F\x03'):  #PLEX
                plex = struct.unpack(">i",record[2:6])[0]
                thisSref.plex=plex
                if(self.debugToTerminal==1):
                    print("\t\tPLEX: "+str(plex))
            elif(idBits==b'\x12\x06'):  #Reference Name
                sName = self.stripNonASCII(record[2::])
                thisSref.sName=sName.rstrip()
                if(self.debugToTerminal==1):
                    print("\t\tReference Name:"+sName)
            elif(idBits==b'\x1A\x01'):  #Transformation
                transFlags = struct.unpack(">H",record[2:4])[0]
                mirrorFlag = bool(transFlags&0x8000)   ##these flags are a bit sketchy
                rotateFlag = bool(transFlags&0x0002)
                magnifyFlag = bool(transFlags&0x0004)
                thisSref.transFlags=[mirrorFlag,magnifyFlag,rotateFlag]
                if(self.debugToTerminal==1):
                    print("\t\t\tMirror X:"+str(mirrorFlag))
                    print( "\t\t\tRotate:"+str(rotateFlag))
                    print("\t\t\tMagnify:"+str(magnifyFlag))
            elif(idBits==b'\x1B\x05'):  #Magnify
                magFactor=self.ieeeDoubleFromIbmData(record[2:10])
                thisSref.magFactor=magFactor
                if(self.debugToTerminal==1):
                    print("\t\t\tMagnification:"+str(magFactor))
            elif(idBits==b'\x1C\x05'):  #Rotate Angle
                rotateAngle=self.ieeeDoubleFromIbmData(record[2:10])
                thisSref.rotateAngle=rotateAngle
                if(self.debugToTerminal==1):
                    print("\t\t\tRotate Angle (CCW):"+str(rotateAngle))
            elif(idBits==b'\x10\x03'):  #XY Data Points
                index=2
                x=struct.unpack(">i",record[index:index+4])[0]
                y=struct.unpack(">i",record[index+4:index+8])[0]
                thisSref.coordinates=(x,y)
                if(self.debugToTerminal==1):
                    print("\t\t\tXY Point: "+str(x)+","+str(y))
            elif(idBits==b'\x11\x00'):  #End Of Element
                if(self.debugToTerminal==1):
                    print("\t\t\tEndSref")
                break;
        return thisSref

    def readAref(self):  #an array of references
        if(self.debugToTerminal==1):
            print("\t\t\tBeginAref")

        thisAref = GdsAref()
        while 1:
            record = self.readNextRecord()
            idBits = record[0:2]
            if(idBits==b'\x26\x01'):  #ELFLAGS
                elementFlags = struct.unpack(">h",record[2:4])[0]
                thisAref.elementFlags=elementFlags
                if(self.debugToTerminal==1):
                    print("\t\tElement Flags: "+str(elementFlags))
            elif(idBits==b'\x2F\x03'):  #PLEX
                plex = struct.unpack(">i",record[2:6])[0]
                thisAref.plex=plex
                if(self.debugToTerminal==1):
                    print("\t\tPLEX: "+str(plex))
            elif(idBits==b'\x12\x06'):  #Reference Name
                aName = record[2::]
                thisAref.aName=aName
                if(self.debugToTerminal==1):
                    print("\t\tReference Name:"+aName)
            elif(idBits==b'\x1A\x01'):  #Transformation
                transFlags = struct.unpack(">H",record[2:4])[0]
                mirrorFlag = bool(transFlags&0x8000)   ##these flags are a bit sketchy
                rotateFlag = bool(transFlags&0x0002)
                magnifyFlag = bool(transFlags&0x0004)
                thisAref.transFlags=[mirrorFlag,magnifyFlag,rotateFlag]
                if(self.debugToTerminal==1):
                    print("\t\t\tMirror X:"+str(mirrorFlag))
                    print("\t\t\tRotate:"+str(rotateFlag))
                    print("\t\t\tMagnify:"+str(magnifyFlag))
            elif(idBits==b'\x1B\x05'):  #Magnify
                magFactor=self.ieeeDoubleFromIbmData(record[2:10])
                thisAref.magFactor=magFactor
                if(self.debugToTerminal==1):
                    print("\t\t\tMagnification:"+str(magFactor))
            elif(idBits==b'\x1C\x05'):  #Rotate Angle
                rotateAngle=self.ieeeDoubleFromIbmData(record[2:10])
                thisAref.rotateAngle=rotateAngle
                if(self.debugToTerminal==1):
                    print("\t\t\tRotate Angle (CCW):"+str(rotateAngle))
            elif(idBits==b'\x10\x03'):  #XY Data Points
                index=2
                topLeftX=struct.unpack(">i",record[index:index+4])[0]
                topLeftY=struct.unpack(">i",record[index+4:index+8])[0]
                rightMostX=struct.unpack(">i",record[index+8:index+12])[0]
                bottomMostY=struct.unpack(">i",record[index+12:index+16])[0]
                thisAref.coordinates=[(topLeftX,topLeftY),(rightMostX,topLeftY),(topLeftX,bottomMostY)]
                if(self.debugToTerminal==1):
                    print("\t\t\tTop Left Point: "+str(topLeftX)+","+str(topLeftY))
                    print("\t\t\t\tArray Width: "+str(rightMostX-topLeftX))
                    print("\t\t\t\tArray Height: "+str(topLeftY-bottomMostY))
            elif(idBits==b'\x11\x00'):  #End Of Element
                if(self.debugToTerminal==1):
                    print("\t\t\tEndAref")
                break;
        return thisAref

    def readText(self):
        if(self.debugToTerminal==1):
            print("\t\t\tBeginText")

        thisText=GdsText()
        while 1:
            record = self.readNextRecord()
            idBits = record[0:2]
            if(idBits==b'\x26\x01'):  #ELFLAGS
                elementFlags = struct.unpack(">h",record[2:4])[0]
                thisText.elementFlags=elementFlags
                if(self.debugToTerminal==1):
                    print("\t\tElement Flags: "+str(elementFlags))
            elif(idBits==b'\x2F\x03'):  #PLEX
                plex = struct.unpack(">i",record[2:6])[0]
                thisText.plex=plex
                if(self.debugToTerminal==1):
                    print("\t\tPLEX: "+str(plex))
            elif(idBits==b'\x0D\x02'):  #Layer
                drawingLayer = struct.unpack(">h",record[2:4])[0]
                thisText.drawingLayer=drawingLayer
                if drawingLayer not in self.layoutObject.layerNumbersInUse:
                    self.layoutObject.layerNumbersInUse += [drawingLayer]
                if(self.debugToTerminal==1):
                    print("\t\tDrawing Layer: "+str(drawingLayer))
            elif(idBits==b'\x16\x02'):  #Purpose TEXTTYPE
                purposeLayer = struct.unpack(">h",record[2:4])[0]
                thisText.purposeLayer=purposeLayer
                if(self.debugToTerminal==1):
                    print("\t\tPurpose Layer: "+str(purposeLayer))
            elif(idBits==b'\x1A\x01'):  #Transformation
                transFlags = struct.unpack(">H",record[2:4])[0]
                mirrorFlag = bool(transFlags&0x8000)   ##these flags are a bit sketchy
                rotateFlag = bool(transFlags&0x0002)
                magnifyFlag = bool(transFlags&0x0004)
                thisText.transFlags=[mirrorFlag,magnifyFlag,rotateFlag]
                if(self.debugToTerminal==1):
                    print("\t\t\tMirror X:"+str(mirrorFlag))
                    print("\t\t\tRotate:"+str(rotateFlag))
                    print("\t\t\tMagnify:"+str(magnifyFlag))
            elif(idBits==b'\x1B\x05'):  #Magnify
                magFactor=self.ieeeDoubleFromIbmData(record[2:10])
                thisText.magFactor=magFactor
                if(self.debugToTerminal==1):
                    print("\t\t\tMagnification:"+str(magFactor))
            elif(idBits==b'\x1C\x05'):  #Rotate Angle
                rotateAngle=self.ieeeDoubleFromIbmData(record[2:10])
                thisText.rotateAngle=rotateAngle
                if(self.debugToTerminal==1):
                    print("\t\t\tRotate Angle (CCW):"+str(rotateAngle))
            elif(idBits==b'\x21\x02'):  #Path type
                pathType = struct.unpack(">h",record[2:4])[0]
                thisText.pathType=pathType
                if(self.debugToTerminal==1):
                    print("\t\t\tPath Type: "+str(pathType))
            elif(idBits==b'\x0F\x03'):  #Path width
                pathWidth = struct.unpack(">i",record[2:6])[0]
                thisText.pathWidth=pathWidth
                if(self.debugToTerminal==1):
                    print("\t\t\tPath Width: "+str(pathWidth))
            elif(idBits==b'\x1A\x01'):  #Text Presentation
                presentationFlags = struct.unpack(">H",record[2:4])[0]
                font = (presentationFlags&0x0030)>>4   ##these flags are a bit sketchy
                verticalFlags = (presentationFlags&0x000C)
                horizontalFlags = (presentationFlags&0x0003)
                thisText.presentationFlags=(font,verticalFlags,horizontalFlags)
                if(self.debugToTerminal==1):
                    print("\t\t\tFont:"+str(font))
                if(verticalFlags==0):
                    if(self.debugToTerminal==1):
                        print("\t\t\tVertical: Top")
                elif(verticalFlags==1):
                    if(self.debugToTerminal==1):
                        print("\t\t\tVertical: Middle")
                elif(verticalFlags==2):
                    if(self.debugToTerminal==1):
                        print("\t\t\tVertical: Bottom")
                if(horizontalFlags==0):
                    if(self.debugToTerminal==1):
                        print("\t\t\tHorizontal: Left")
                elif(horizontalFlags==1):
                    if(self.debugToTerminal==1):
                        print("\t\t\tHorizontal: Center")
                elif(horizontalFlags==2):
                    if(self.debugToTerminal==1):
                        print("\t\t\tHorizontal: Right")
            elif(idBits==b'\x10\x03'):  #XY Data Points
                index=2
                x=struct.unpack(">i",record[index:index+4])[0]
                y=struct.unpack(">i",record[index+4:index+8])[0]
                thisText.coordinates=[(x,y)]
                if(self.debugToTerminal==1):
                    print("\t\t\tXY Point: "+str(x)+","+str(y))
            elif(idBits==b'\x19\x06'):  #Text String - also the last record in this element
                textString = record[2::].decode('utf-8')
                thisText.textString=textString
                if(self.debugToTerminal==1):
                    print("\t\t\tText String: "+textString)
            elif(idBits==b'\x11\x00'):  #End Of Element
                if(self.debugToTerminal==1):
                    print("\t\t\tEndText")
                break;
        return thisText

    def readNode(self):
        if(self.debugToTerminal==1):
            print("\t\t\tBeginNode")

        ##reads in a node type structure = an electrical net
        thisNode = GdsNode()
        while 1:
            record = self.readNextRecord()
            idBits = record[0:2]
            if(idBits==b'\x26\x01'):  #ELFLAGS
                elementFlags = struct.unpack(">h",record[2:4])[0]
                thisNode.elementFlags=elementFlags
                if(self.debugToTerminal==1):
                    print("\t\tElement Flags: "+str(elementFlags))
            elif(idBits==b'\x2F\x03'):  #PLEX
                plex = struct.unpack(">i",record[2:6])[0]
                thisNode.plex=plex
                if(self.debugToTerminal==1):
                    print("\t\tPLEX: "+str(plex))
            elif(idBits==b'\x0D\x02'):  #Layer
                drawingLayer = struct.unpack(">h",record[2:4])[0]
                thisNode.drawingLayer=drawingLayer
                if drawingLayer not in self.layoutObject.layerNumbersInUse:
                    self.layoutObject.layerNumbersInUse += [drawingLayer]
                if(self.debugToTerminal==1):
                    print("\t\tDrawing Layer: "+str(drawingLayer))
            elif(idBits==b'\x2A\x02'):  #Node Type
                nodeType = struct.unpack(">h",record[2:4])[0]
                thisNode.nodeType=nodeType
                if(self.debugToTerminal==1):
                    print("\t\tNode Type: "+str(nodeType))
            elif(idBits==b'\x10\x03'):  #XY Data Points
                numDataPoints = len(record)-2  #packed as XY coordinates 4 bytes each
                thisNode.coordinates=[]
                for index in range(2,numDataPoints+2,8):  #incorporate the 2 byte offset
                    x=struct.unpack(">i",record[index:index+4])[0]
                    y=struct.unpack(">i",record[index+4:index+8])[0]
                    thisNode.coordinates+=[(x,y)]
                    if(self.debugToTerminal==1):
                        print("\t\t\tXY Point: "+str(x)+","+str(y))
            elif(idBits==b'\x11\x00'):  #End Of Element
                if(self.debugToTerminal==1):
                    print("\t\t\tEndNode")
                break;
        return thisNode

    def readBox(self):
        if(self.debugToTerminal==1):
            print("\t\t\tBeginBox")

        ##reads in a gds BOX structure
        thisBox = GdsBox()
        while 1:
            record = self.readNextRecord()
            idBits = record[0:2]
            if(idBits==b'\x26\x01'):  #ELFLAGS
                elementFlags = struct.unpack(">h",record[2:4])
                thisBox.elementFlags=elementFlags
                if(self.debugToTerminal==1):
                    print("\t\tElement Flags: "+str(elementFlags))
            elif(idBits==b'\x2F\x03'):  #PLEX
                plex = struct.unpack(">i",record[2:6])[0]
                thisBox.plex=plex
                if(self.debugToTerminal==1):
                    print("\t\tPLEX: "+str(plex))
            elif(idBits==b'\x0D\x02'):  #Layer
                drawingLayer = struct.unpack(">h",record[2:4])[0]
                thisBox.drawingLayer=drawingLayer
                if drawingLayer not in self.layoutObject.layerNumbersInUse:
                    self.layoutObject.layerNumbersInUse += [drawingLayer]
                if(self.debugToTerminal==1):
                    print("\t\tDrawing Layer: "+str(drawingLayer))
            elif(idBits==b'\x16\x02'):  #Purpose TEXTYPE
                purposeLayer = struct.unpack(">h",record[2:4])[0]
                thisBox.purposeLayer=purposeLayer
                if(self.debugToTerminal==1):
                    print("\t\tPurpose Layer: "+str(purposeLayer))
            elif(idBits==b'\x2D\x00'):  #Box
                boxValue = struct.unpack(">h",record[2:4])[0]
                thisBox.boxValue=boxValue
                if(self.debugToTerminal==1):
                    print("\t\tBox Value: "+str(boxValue))
            elif(idBits==b'\x10\x03'):  #XY Data Points that form a closed box
                numDataPoints = len(record)-2  #packed as XY coordinates 4 bytes each
                thisBox.coordinates=[]
                for index in range(2,numDataPoints+2,8):  #incorporate the 2 byte offset
                    x=struct.unpack(">i",record[index:index+4])[0]
                    y=struct.unpack(">i",record[index+4:index+8])[0]
                    thisBox.coordinates+=[(x,y)]
                    if(self.debugToTerminal==1):
                        print("\t\t\tXY Point: "+str(x)+","+str(y))
            elif(idBits==b'\x11\x00'):  #End Of Element
                if(self.debugToTerminal==1):
                    print("\t\t\tEndBox")
                break;
        return thisBox

    def readNextStructure(self):
        thisStructure = GdsStructure()
        record = self.readNextRecord()
        idBits = record[0:2]
        # Begin structure
        if(idBits==b'\x05\x02' and len(record)==26):
            createYear = struct.unpack(">h",record[2:4])[0]
            createMonth = struct.unpack(">h",record[4:6])[0]
            createDay = struct.unpack(">h",record[6:8])[0]
            createHour = struct.unpack(">h",record[8:10])[0]
            createMinute = struct.unpack(">h",record[10:12])[0]
            createSecond = struct.unpack(">h",record[12:14])[0]
            modYear = struct.unpack(">h",record[14:16])[0]
            modMonth = struct.unpack(">h",record[16:18])[0]
            modDay = struct.unpack(">h",record[18:20])[0]
            modHour = struct.unpack(">h",record[20:22])[0]
            modMinute = struct.unpack(">h",record[22:24])[0]
            modSecond = struct.unpack(">h",record[24:26])[0]
            thisStructure.createDate=(createYear,createMonth,createDay,createHour,createMinute,createSecond)
            thisStructure.modDate=(modYear,modMonth,modDay,modHour,modMinute,modSecond)
            if(self.debugToTerminal==1):
                print("Date Created:"+str(createYear)+","+str(createMonth)+","+str(createDay)+\
                      ","+str(createHour)+","+str(createMinute)+","+str(createSecond))
                print("Date Modified:"+str(modYear)+","+str(modMonth)+","+str(modDay)+","+str(modHour)+","+str(modMinute)+","+str(modSecond))
        else:
            #means we have hit the last structure, so return the record
            #to whoever called us to do something with it
            return record
        while 1:
            record = self.readNextRecord()
            idBits = record[0:2]
            if idBits==b'\x07\x00': break; #we've reached the end of the structure
            elif(idBits==b'\x06\x06'):
                structName = self.stripNonASCII(record[2::])
                thisStructure.name = structName
                if(self.debugToTerminal==1):
                    print("\tStructure Name: "+structName)
            elif(idBits==b'\x08\x00'):
                thisStructure.boundaries+=[self.readBoundary()]
            elif(idBits==b'\x09\x00'):
                thisStructure.paths+=[self.readPath()]
            elif(idBits==b'\x0A\x00'):
                thisStructure.srefs+=[self.readSref()]
            elif(idBits==b'\x0B\x00'):
                thisStructure.arefs+=[self.readAref()]
            elif(idBits==b'\x0C\x00'):
                thisStructure.texts+=[self.readText()]
            elif(idBits==b'\x15\x00'):
                thisStructure.nodes+=[self.readNode()]
            elif(idBits==b'\x2E\x02'):
                thisStructure.boxes+=[self.readBox()]
        if(self.debugToTerminal==1):
            print("\tEnd of Structure.")
        self.layoutObject.structures[structName]=thisStructure #add this structure to the layout object
        return 1

    def readGds2(self):
        if(self.readHeader()):  #did the header read ok?
            record = self.readNextStructure()
            while(record == 1):
                record = self.readNextStructure()
            #now we have fallen out of the while, which means we are out of structures
            #so test for end of library
            if(len(record)>1):
                idBits = record[0:2]
                if idBits==b'\x04\x00': #we've reached the end of the library
                    if(self.debugToTerminal==1):
                        print("End of GDS Library.")
            else:
                print("There was an error reading the structure list.")
        else:
            print("There was an error parsing the GDS header.  Aborting...")

    def loadFromFile(self, fileName, special_purposes={}):
        self.fileHandle = open(fileName,"rb")
        self.readGds2()
        self.fileHandle.close()
        self.layoutObject.initialize(special_purposes)

##############################################

    def findStruct(self,fileName,findStructName):
	#print("find struct")
        self.fileHandle = open(fileName,"rb")
        self.debugToTerminal=0
        if(self.readHeader()):  #did the header read ok?
            record = self.findStruct_readNextStruct(findStructName)
            while(record == 1):
                record = self.findStruct_readNextStruct(findStructName)
            #now we have fallen out of the while, which means we are out of structures
            #so test for end of library
        else:
            print("There was an error parsing the GDS header.  Aborting...")
        self.fileHandle.close()
	#print("End the search of",findStructName)
        #self.layoutObject.initialize()
        return record

    def findStruct_readNextStruct(self,findStructName):
        self.debugToTerminal=0
        thisStructure = GdsStructure()
        record = self.readNextRecord()
        idBits = record[0:2]
        if(idBits==('\x05','\x02') and len(record)==26):
            createYear = struct.unpack(">h",record[2]+record[3])[0]
            createMonth = struct.unpack(">h",record[4]+record[5])[0]
            createDay = struct.unpack(">h",record[6]+record[7])[0]
            createHour = struct.unpack(">h",record[8]+record[9])[0]
            createMinute = struct.unpack(">h",record[10]+record[11])[0]
            createSecond = struct.unpack(">h",record[12]+record[13])[0]
            modYear = struct.unpack(">h",record[14]+record[15])[0]
            modMonth = struct.unpack(">h",record[16]+record[17])[0]
            modDay = struct.unpack(">h",record[18]+record[19])[0]
            modHour = struct.unpack(">h",record[20]+record[21])[0]
            modMinute = struct.unpack(">h",record[22]+record[23])[0]
            modSecond = struct.unpack(">h",record[24]+record[25])[0]
            thisStructure.createDate=(createYear,createMonth,createDay,createHour,createMinute,createSecond)
            thisStructure.modDate=(modYear,modMonth,modDay,modHour,modMinute,modSecond)
        else:
            #means we have hit the last structure, so return the record
            #to whoever called us to do something with it
            return record
        wantedStruct=0
        while 1:
            record = self.readNextRecord()
            idBits = record[0:2]
            if idBits==('\x07','\x00'): break; #we've reached the end of the structure
            elif(idBits==('\x06','\x06')):
                structName = self.stripNonASCII(record[2::]) #(record[2:1] + record[1::]).rstrip()
                thisStructure.name = structName
                if(findStructName==thisStructure.name):
                    wantedStruct=1
                if(self.debugToTerminal==1):
                    print("\tStructure Name: "+structName)
            elif(idBits==('\x08','\x00')):
                thisStructure.boundaries+=[self.readBoundary()]
            elif(idBits==('\x09','\x00')):
                thisStructure.paths+=[self.readPath()]
            elif(idBits==('\x0A','\x00')):
                thisStructure.srefs+=[self.readSref()]
            elif(idBits==('\x0B','\x00')):
                thisStructure.arefs+=[self.readAref()]
            elif(idBits==('\x0C','\x00')):
                thisStructure.texts+=[self.readText()]
            elif(idBits==('\x15','\x00')):
                thisStructure.nodes+=[self.readNode()]
            elif(idBits==('\x2E','\x02')):
                thisStructure.boxes+=[self.readBox()]
        if(self.debugToTerminal==1):
            print("\tEnd of Structure.")
        self.layoutObject.structures[structName]=thisStructure #add this structure to the layout object
        if(wantedStruct == 0):
            return 1
        else:
	    #print("\tDone with collectting bound. Return")
            return [0,thisStructure.boundaries]

    def findLabel(self,fileName,findLabelName):
	#print("find Label")
        self.fileHandle = open(fileName,"rb")
        self.debugToTerminal=0
        if(self.readHeader()):  #did the header read ok?
            record = self.findLabel_readNextStruct(findLabelName)
            while(record == 1):
                record = self.findLabel_readNextStruct(findLabelName)
            #now we have fallen out of the while, which means we are out of structures
            #so test for end of library
        else:
            print("There was an error parsing the GDS header.  Aborting...")
        self.fileHandle.close()
	#print("End the search of",findStructName)
        #self.layoutObject.initialize()
        return record

    def findLabel_readNextStruct(self,findLabelName):
        self.debugToTerminal=0
        thisStructure = GdsStructure()
        record = self.readNextRecord()
        idBits = record[0:2]
        if(idBits==('\x05','\x02') and len(record)==26):
            createYear = struct.unpack(">h",record[2]+record[3])[0]
            createMonth = struct.unpack(">h",record[4]+record[5])[0]
            createDay = struct.unpack(">h",record[6]+record[7])[0]
            createHour = struct.unpack(">h",record[8]+record[9])[0]
            createMinute = struct.unpack(">h",record[10]+record[11])[0]
            createSecond = struct.unpack(">h",record[12]+record[13])[0]
            modYear = struct.unpack(">h",record[14]+record[15])[0]
            modMonth = struct.unpack(">h",record[16]+record[17])[0]
            modDay = struct.unpack(">h",record[18]+record[19])[0]
            modHour = struct.unpack(">h",record[20]+record[21])[0]
            modMinute = struct.unpack(">h",record[22]+record[23])[0]
            modSecond = struct.unpack(">h",record[24]+record[25])[0]
            thisStructure.createDate=(createYear,createMonth,createDay,createHour,createMinute,createSecond)
            thisStructure.modDate=(modYear,modMonth,modDay,modHour,modMinute,modSecond)
        else:
            #means we have hit the last structure, so return the record
            #to whoever called us to do something with it
            return record
        wantedLabel=0
        wantedtexts=[GdsText()]
        while 1:
            record = self.readNextRecord()
            idBits = record[0:2]
            if idBits==('\x07','\x00'): break; #we've reached the end of the structure
            elif(idBits==('\x06','\x06')):
                structName = self.stripNonASCII(record[2::]) #(record[2:1] + record[1::]).rstrip()
                thisStructure.name = structName
                if(self.debugToTerminal==1):
                    print("\tStructure Name: "+structName)
            elif(idBits==('\x08','\x00')):
                thisStructure.boundaries+=[self.readBoundary()]
            elif(idBits==('\x09','\x00')):
                thisStructure.paths+=[self.readPath()]
            elif(idBits==('\x0A','\x00')):
                thisStructure.srefs+=[self.readSref()]
            elif(idBits==('\x0B','\x00')):
                thisStructure.arefs+=[self.readAref()]
            elif(idBits==('\x0C','\x00')):
                label=self.readText()
		#Be careful: label.textString contains one space string in it. Delete that one before use it
                if( findLabelName == label.textString[0:(len(label.textString)-1)] ):
                    wantedLabel=1
                    wantedtexts+=[label]
                thisStructure.texts+=[label]
                if(self.debugToTerminal == 1):
                    print(label.textString[0:(len(label.textString)-1)],findLabelName,( findLabelName == label.textString[0:(len(label.textString)-1)] ))
            elif(idBits==('\x15','\x00')):
                thisStructure.nodes+=[self.readNode()]
            elif(idBits==('\x2E','\x02')):
                thisStructure.boxes+=[self.readBox()]
        if(self.debugToTerminal==1):
            print("\tEnd of Structure.")
        self.layoutObject.structures[structName]=thisStructure #add this structure to the layout object
        if(wantedLabel == 0):
            return 1
        else:
            #print("\tDone with collectting bound. Return")
            return [0,wantedtexts]
