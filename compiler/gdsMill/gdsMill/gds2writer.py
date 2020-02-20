#!/usr/bin/env python
import struct
from .gdsPrimitives import *

class Gds2writer:
    """Class to take a populated layout class and write it to a file in GDSII format"""
    ## Based on info from http://www.rulabinsky.com/cavd/text/chapc.html

    def __init__(self,layoutObject):
        self.fileHandle = 0
        self.layoutObject = layoutObject
        self.debugToTerminal=0  #do we dump debug data to the screen

    def print64AsBinary(self,number):
        #debugging method for binary inspection
        for index in range(0,64):
            print((number>>(63-index))&0x1,eol='')
        print("\n")

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

    def ibmDataFromIeeeDouble(self,ieeeDouble):
        asciiDouble = struct.pack('>d',ieeeDouble)
        data = struct.unpack('>q',asciiDouble)[0]
        sign = (data >> 63) & 0x01
        exponent = ((data >> 52) & 0x7ff)-1023
        mantissa = data << 12 #chop off sign and exponent
        if(ieeeDouble == 0):
            mantissa = 0
            exponent = 0
            sign = 0
        else:
            #add back the assumed digit
            mantissa >>= 1
            mantissa = mantissa|0x8000000000000000
            exponent += 1
            #convert the exponent
            #need to do this in a loop to prevent sign extension!
            for index in range (0,-exponent&3):
                mantissa >>= 1
                mantissa = mantissa & 0x7fffffffffffffff

            exponent = (exponent+3) >> 2
            exponent+=64

        newFloat =(sign<<63)|(exponent<<56)|((mantissa>>8)&0xffffffffffffff)
        asciiDouble = struct.pack('>q',newFloat)
        return asciiDouble

    def ieeeFloatCheck(self,aFloat):
        #debugging method for float construction
        asciiDouble = struct.pack('>d',aFloat)
        data = struct.unpack('>q',asciiDouble)[0]
        sign = data >> 63
        exponent = ((data >> 52) & 0x7ff)-1023
        print(exponent+1023)
        mantissa = data << 12 #chop off sign and exponent
        #self.print64AsBinary((sign<<63)|((exponent+1023)<<52)|(mantissa>>12))
        asciiDouble = struct.pack('>q',(sign<<63)|(exponent+1023<<52)|(mantissa>>12))
        newFloat = struct.unpack('>d',asciiDouble)[0]
        print("Check:"+str(newFloat))

    def writeRecord(self,record):
        recordLength = len(record)+2  #make sure to include this in the length
        recordLengthAscii=struct.pack(">h",recordLength)
        self.fileHandle.write(recordLengthAscii+record)

    def writeHeader(self):
        ##  Header
        if("gdsVersion" in self.layoutObject.info):
            idBits=b'\x00\x02'
            gdsVersion = struct.pack(">h",self.layoutObject.info["gdsVersion"])
            self.writeRecord(idBits+gdsVersion)
        ## Modified Date
        if("dates" in self.layoutObject.info):
            idBits=b'\x01\x02'
            modYear = struct.pack(">h",self.layoutObject.info["dates"][0])
            modMonth = struct.pack(">h",self.layoutObject.info["dates"][1])
            modDay = struct.pack(">h",self.layoutObject.info["dates"][2])
            modHour = struct.pack(">h",self.layoutObject.info["dates"][3])
            modMinute = struct.pack(">h",self.layoutObject.info["dates"][4])
            modSecond = struct.pack(">h",self.layoutObject.info["dates"][5])
            lastAccessYear = struct.pack(">h",self.layoutObject.info["dates"][6])
            lastAccessMonth = struct.pack(">h",self.layoutObject.info["dates"][7])
            lastAccessDay = struct.pack(">h",self.layoutObject.info["dates"][8])
            lastAccessHour = struct.pack(">h",self.layoutObject.info["dates"][9])
            lastAccessMinute = struct.pack(">h",self.layoutObject.info["dates"][10])
            lastAccessSecond = struct.pack(">h",self.layoutObject.info["dates"][11])
            self.writeRecord(idBits+modYear+modMonth+modDay+modHour+modMinute+modSecond+\
                             lastAccessYear+lastAccessMonth+lastAccessDay+lastAccessHour+\
                             lastAccessMinute+lastAccessSecond)
        ##  LibraryName
        if("libraryName" in self.layoutObject.info):
            idBits=b'\x02\x06'
            if (len(self.layoutObject.info["libraryName"]) % 2 != 0):
                libraryName = self.layoutObject.info["libraryName"].encode() + "\0"
            else:
                libraryName = self.layoutObject.info["libraryName"].encode()
            self.writeRecord(idBits+libraryName)
        ## reference libraries
        if("referenceLibraries" in self.layoutObject.info):
            idBits=b'\x1F\x06'
            referenceLibraryA = self.layoutObject.info["referenceLibraries"][0]
            referenceLibraryB = self.layoutObject.info["referenceLibraries"][1]
            self.writeRecord(idBits+referenceLibraryA+referenceLibraryB)
        if("fonts" in self.layoutObject.info):
            idBits=b'\x20\x06'
            fontA = self.layoutObject.info["fonts"][0]
            fontB = self.layoutObject.info["fonts"][1]
            fontC = self.layoutObject.info["fonts"][2]
            fontD = self.layoutObject.info["fonts"][3]
            self.writeRecord(idBits+fontA+fontB+fontC+fontD)
        if("attributeTable" in self.layoutObject.info):
            idBits=b'\x23\x06'
            attributeTable = self.layoutObject.info["attributeTable"]
            self.writeRecord(idBits+attributeTable)
        if("generations" in self.layoutObject.info):
            idBits=b'\x22\x02'
            generations = struct.pack(">h",self.layoutObject.info["generations"])
            self.writeRecord(idBits+generations)
        if("fileFormat" in self.layoutObject.info):
            idBits=b'\x36\x02'
            fileFormat = struct.pack(">h",self.layoutObject.info["fileFormat"])
            self.writeRecord(idBits+fileFormat)
        if("mask" in self.layoutObject.info):
            idBits=b'\x37\x06'
            mask = self.layoutObject.info["mask"]
            self.writeRecord(idBits+mask)
        if("units" in self.layoutObject.info):
            idBits=b'\x03\x05'
            userUnits=self.ibmDataFromIeeeDouble(self.layoutObject.info["units"][0])
            dbUnits=self.ibmDataFromIeeeDouble((self.layoutObject.info["units"][0]*1e-6/self.layoutObject.info["units"][1])*self.layoutObject.info["units"][1])

            #User Units are hardcoded, since the floating point implementation of gdsMill is not adequate,
		#resulting in a different value being written in output stream.  Hardcoded to sram compiler's outputed gds units.
	    #db="39225c17d04dad2a"
	    #uu="3e20c49ba5e353f8"

            #userUnits="3e20c49ba5e353f8".decode("hex")
            #dbUnits="39225c17d04dad2a".decode("hex")

            #dbUnits="39225c17d04dad2a".decode("hex")
	    #db=39225c17d04dad2a


            self.writeRecord(idBits+userUnits+dbUnits)
        if(self.debugToTerminal==1):
            print("writer: userUnits %s"%(userUnits.encode("hex")))
            print("writer: dbUnits   %s"%(dbUnits.encode("hex")))
	    #self.ieeeFloatCheck(1.3e-6)

            print("End of GDSII Header Written")
        return 1

    def writeBoundary(self,thisBoundary):
        idBits=b'\x08\x00'  #record Type
        self.writeRecord(idBits)
        if(thisBoundary.elementFlags!=""):
            idBits=b'\x26\x01' # ELFLAGS
            elementFlags = struct.pack(">h",thisBoundary.elementFlags)
            self.writeRecord(idBits+elementFlags)
        if(thisBoundary.plex!=""):
            idBits=b'\x2F\x03'  # PLEX
            plex = struct.pack(">i",thisBoundary.plex)
            self.writeRecord(idBits+plex)
        if(thisBoundary.drawingLayer!=""):
            idBits=b'\x0D\x02' # drawing layer
            drawingLayer = struct.pack(">h",thisBoundary.drawingLayer)
            self.writeRecord(idBits+drawingLayer)
        if(thisBoundary.purposeLayer!=""):
            idBits=b'\x0E\x02' # DataType
            if type(thisBoundary.purposeLayer)!=int:
                import pdb; pdb.set_trace()
            dataType = struct.pack(">h",thisBoundary.purposeLayer)
            self.writeRecord(idBits+dataType)
        if(thisBoundary.coordinates!=""):
            idBits=b'\x10\x03' # XY Data Points
            coordinateRecord = idBits
            for coordinate in thisBoundary.coordinates:
                x=struct.pack(">i",int(coordinate[0]))
                y=struct.pack(">i",int(coordinate[1]))
                coordinateRecord+=x
                coordinateRecord+=y
            self.writeRecord(coordinateRecord)
        idBits=b'\x11\x00' #End Of Element
        coordinateRecord = idBits
        self.writeRecord(coordinateRecord)

    def writePath(self,thisPath):  #writes out a path structure
        idBits=b'\x09\x00'  #record Type
        self.writeRecord(idBits)
        if(thisPath.elementFlags != ""):
            idBits=b'\x26\x01' #ELFLAGS
            elementFlags = struct.pack(">h",thisPath.elementFlags)
            self.writeRecord(idBits+elementFlags)
        if(thisPath.plex!=""):
            idBits=b'\x2F\x03'  #PLEX
            plex = struct.pack(">i",thisPath.plex)
            self.writeRecord(idBits+plex)
        if(thisPath.drawingLayer):
            idBits=b'\x0D\x02' #drawig layer
            drawingLayer = struct.pack(">h",thisPath.drawingLayer)
            self.writeRecord(idBits+drawingLayer)
        if(thisPath.purposeLayer):
            idBits=b'\x16\x02' #purpose layer
            purposeLayer = struct.pack(">h",thisPath.purposeLayer)
            self.writeRecord(idBits+purposeLayer)
        if(thisPath.dataType is not None):
            idBits=b'\x0E\x02'  #Data type
            dataType = struct.pack(">h",thisPath.dataType)
            self.writeRecord(idBits+dataType)
        if(thisPath.pathType):
            idBits=b'\x21\x02'  #Path type
            pathType = struct.pack(">h",thisPath.pathType)
            self.writeRecord(idBits+pathType)
        if(thisPath.pathWidth):
            idBits=b'\x0F\x03'
            pathWidth = struct.pack(">i",thisPath.pathWidth)
            self.writeRecord(idBits+pathWidth)
        if(thisPath.coordinates):
            idBits=b'\x10\x03' #XY Data Points
            coordinateRecord = idBits
            for coordinate in thisPath.coordinates:
                x=struct.pack(">i",int(coordinate[0]))
                y=struct.pack(">i",int(coordinate[1]))
                coordinateRecord+=x
                coordinateRecord+=y
            self.writeRecord(coordinateRecord)
        idBits=b'\x11\x00' #End Of Element
        coordinateRecord = idBits
        self.writeRecord(coordinateRecord)

    def writeSref(self,thisSref):  #reads in a reference to another structure
        idBits=b'\x0A\x00'  #record Type
        self.writeRecord(idBits)
        if(thisSref.elementFlags != ""):
            idBits=b'\x26\x01' #ELFLAGS
            elementFlags = struct.pack(">h",thisSref.elementFlags)
            self.writeRecord(idBits+elementFlags)
        if(thisSref.plex!=""):
            idBits=b'\x2F\x03'  #PLEX
            plex = struct.pack(">i",thisSref.plex)
            self.writeRecord(idBits+plex)
        if(thisSref.sName!=""):
            idBits=b'\x12\x06'
            if (len(thisSref.sName) % 2 != 0):
                sName = thisSref.sName+"\0"
            else:
                sName = thisSref.sName
            self.writeRecord(idBits+sName.encode())
        if(thisSref.transFlags!=""):
            idBits=b'\x1A\x01'
            mirrorFlag = int(thisSref.transFlags[0])<<15
            # The rotate and magnify flags specify "absolute" rotate and magnify.
            # It is unclear what that is (ignore all further rotates/mags in the
            # hierarchy? But anyway, calibre doesn't support it.
            rotateFlag=0
            magnifyFlag = 0
            #rotateFlag = int(thisSref.transFlags[2])<<1
            #magnifyFlag = int(thisSref.transFlags[1])<<2
            transFlags = struct.pack(">H",mirrorFlag|rotateFlag|magnifyFlag)
            self.writeRecord(idBits+transFlags)
        if(thisSref.magFactor!=""):
            idBits=b'\x1B\x05'
            magFactor=self.ibmDataFromIeeeDouble(thisSref.magFactor)
            self.writeRecord(idBits+magFactor)
        if(thisSref.rotateAngle!=""):
            idBits=b'\x1C\x05'
            rotateAngle=self.ibmDataFromIeeeDouble(thisSref.rotateAngle)
            self.writeRecord(idBits+rotateAngle)
        if(thisSref.coordinates!=""):
            idBits=b'\x10\x03' #XY Data Points
            coordinateRecord = idBits
            coordinate = thisSref.coordinates
            x=struct.pack(">i",int(coordinate[0]))
            y=struct.pack(">i",int(coordinate[1]))
            coordinateRecord+=x
            coordinateRecord+=y
	    #print(thisSref.coordinates)
            self.writeRecord(coordinateRecord)
        idBits=b'\x11\x00' #End Of Element
        coordinateRecord = idBits
        self.writeRecord(coordinateRecord)

    def writeAref(self,thisAref):  #an array of references
        idBits=b'\x0B\x00'  #record Type
        self.writeRecord(idBits)
        if(thisAref.elementFlags!=""):
            idBits=b'\x26\x01' #ELFLAGS
            elementFlags = struct.pack(">h",thisAref.elementFlags)
            self.writeRecord(idBits+elementFlags)
        if(thisAref.plex):
            idBits=b'\x2F\x03'  #PLEX
            plex = struct.pack(">i",thisAref.plex)
            self.writeRecord(idBits+plex)
        if(thisAref.aName):
            idBits=b'\x12\x06'
            if (len(thisAref.aName) % 2 != 0):
                aName = thisAref.aName+"\0"
            else:
                aName = thisAref.aName
            self.writeRecord(idBits+aName)
        if(thisAref.transFlags):
            idBits=b'\x1A\x01'
            mirrorFlag = int(thisAref.transFlags[0])<<15
            # The rotate and magnify flags specify "absolute" rotate and magnify.
            # It is unclear what that is (ignore all further rotates/mags in the
            # hierarchy? But anyway, calibre doesn't support it.
            rotateFlag=0
            magnifyFlag = 0
            #rotateFlag = int(thisAref.transFlags[2])<<1
            #magnifyFlag = int(thisAref.transFlags[1])<<2
            transFlags = struct.pack(">H",mirrorFlag|rotateFlag|magnifyFlag)
            self.writeRecord(idBits+transFlags)
        if(thisAref.magFactor!=""):
            idBits=b'\x1B\x05'
            magFactor=self.ibmDataFromIeeeDouble(thisAref.magFactor)
            self.writeRecord(idBits+magFactor)
        if(thisAref.rotateAngle!=""):
            idBits=b'\x1C\x05'
            rotateAngle=self.ibmDataFromIeeeDouble(thisAref.rotateAngle)
            self.writeRecord(idBits+rotateAngle)
        if(thisAref.coordinates):
            idBits=b'\x10\x03' #XY Data Points
            coordinateRecord = idBits
            for coordinate in thisAref.coordinates:
                x=struct.pack(">i",coordinate[0])
                y=struct.pack(">i",coordinate[1])
                coordinateRecord+=x
                coordinateRecord+=y
            self.writeRecord(coordinateRecord)
        idBits=b'\x11\x00' #End Of Element
        coordinateRecord = idBits
        self.writeRecord(coordinateRecord)

    def writeText(self,thisText):
        idBits=b'\x0C\x00'  #record Type
        self.writeRecord(idBits)
        if(thisText.elementFlags!=""):
            idBits=b'\x26\x01' #ELFLAGS
            elementFlags = struct.pack(">h",thisText.elementFlags)
            self.writeRecord(idBits+elementFlags)
        if(thisText.plex !=""):
            idBits=b'\x2F\x03'  #PLEX
            plex = struct.pack(">i",thisText.plex)
            self.writeRecord(idBits+plex)
        if(thisText.drawingLayer != ""):
            idBits=b'\x0D\x02' #drawing layer
            drawingLayer = struct.pack(">h",thisText.drawingLayer)
            self.writeRecord(idBits+drawingLayer)
            idBits=b'\x16\x02' #purpose layer TEXTTYPE
            purposeLayer = struct.pack(">h",thisText.purposeLayer)
            self.writeRecord(idBits+purposeLayer)
        if(thisText.transFlags != ""):
            idBits=b'\x1A\x01'
            mirrorFlag = int(thisText.transFlags[0])<<15
            # The rotate and magnify flags specify "absolute" rotate and magnify.
            # It is unclear what that is (ignore all further rotates/mags in the
            # hierarchy? But anyway, calibre doesn't support it.
            rotateFlag=0
            magnifyFlag = 0
            #rotateFlag = int(thisText.transFlags[2])<<1
            #magnifyFlag = int(thisText.transFlags[1])<<2
            transFlags = struct.pack(">H",mirrorFlag|rotateFlag|magnifyFlag)
            self.writeRecord(idBits+transFlags)
        if(thisText.magFactor!=""):
            idBits=b'\x1B\x05'
            magFactor=self.ibmDataFromIeeeDouble(thisText.magFactor)
            self.writeRecord(idBits+magFactor)
        if(thisText.rotateAngle!=""):
            idBits=b'\x1C\x05'
            rotateAngle=self.ibmDataFromIeeeDouble(thisText.rotateAngle)
            self.writeRecord(idBits+rotateAngle)
        if(thisText.pathType !=""):
            idBits=b'\x21\x02'  #Path type
            pathType = struct.pack(">h",thisText.pathType)
            self.writeRecord(idBits+pathType)
        if(thisText.pathWidth != ""):
            idBits=b'\x0F\x03'
            pathWidth = struct.pack(">i",thisText.pathWidth)
            self.writeRecord(idBits+pathWidth)
        if(thisText.presentationFlags!=""):
            idBits=b'\x1A\x01'
            font = thisText.presentationFlags[0]<<4
            verticalFlags = int(thisText.presentationFlags[1])<<2
            horizontalFlags = int(thisText.presentationFlags[2])
            presentationFlags = struct.pack(">H",font|verticalFlags|horizontalFlags)
            self.writeRecord(idBits+transFlags)
        if(thisText.coordinates!=""):
            idBits=b'\x10\x03' #XY Data Points
            coordinateRecord = idBits
            for coordinate in thisText.coordinates:
                x=struct.pack(">i",int(coordinate[0]))
                y=struct.pack(">i",int(coordinate[1]))
                coordinateRecord+=x
                coordinateRecord+=y
            self.writeRecord(coordinateRecord)
        if(thisText.textString):
            idBits=b'\x19\x06'
            textString = thisText.textString
            self.writeRecord(idBits+textString.encode())

        idBits=b'\x11\x00' #End Of Element
        coordinateRecord = idBits
        self.writeRecord(coordinateRecord)

    def writeNode(self,thisNode):
        idBits=b'\x15\x00'  #record Type
        self.writeRecord(idBits)
        if(thisNode.elementFlags!=""):
            idBits=b'\x26\x01' #ELFLAGS
            elementFlags = struct.pack(">h",thisNode.elementFlags)
            self.writeRecord(idBits+elementFlags)
        if(thisNode.plex!=""):
            idBits=b'\x2F\x03'  #PLEX
            plex = struct.pack(">i",thisNode.plex)
            self.writeRecord(idBits+plex)
        if(thisNode.drawingLayer!=""):
            idBits=b'\x0D\x02' #drawig layer
            drawingLayer = struct.pack(">h",thisNode.drawingLayer)
            self.writeRecord(idBits+drawingLayer)
        if(thisNode.nodeType!=""):
            idBits=b'\x2A\x02'
            nodeType = struct.pack(">h",thisNode.nodeType)
            self.writeRecord(idBits+nodeType)
        if(thisText.coordinates!=""):
            idBits=b'\x10\x03' #XY Data Points
            coordinateRecord = idBits
            for coordinate in thisText.coordinates:
                x=struct.pack(">i",int(coordinate[0]))
                y=struct.pack(">i",int(coordinate[1]))
                coordinateRecord+=x
                coordinateRecord+=y
            self.writeRecord(coordinateRecord)

        idBits=b'\x11\x00' #End Of Element
        coordinateRecord = idBits
        self.writeRecord(coordinateRecord)

    def writeBox(self,thisBox):
        idBits=b'\x2E\x02'  #record Type
        self.writeRecord(idBits)
        if(thisBox.elementFlags!=""):
            idBits=b'\x26\x01' #ELFLAGS
            elementFlags = struct.pack(">h",thisBox.elementFlags)
            self.writeRecord(idBits+elementFlags)
        if(thisBox.plex!=""):
            idBits=b'\x2F\x03'  #PLEX
            plex = struct.pack(">i",thisBox.plex)
            self.writeRecord(idBits+plex)
        if(thisBox.drawingLayer!=""):
            idBits=b'\x0D\x02' #drawig layer
            drawingLayer = struct.pack(">h",thisBox.drawingLayer)
            self.writeRecord(idBits+drawingLayer)
        if(thisBox.purposeLayer):
            idBits=b'\x16\x02' #purpose layer
            purposeLayer = struct.pack(">h",thisBox.purposeLayer)
            self.writeRecord(idBits+purposeLayer)
        if(thisBox.boxValue!=""):
            idBits=b'\x2D\x00'
            boxValue = struct.pack(">h",thisBox.boxValue)
            self.writeRecord(idBits+boxValue)
        if(thisBox.coordinates!=""):
            idBits=b'\x10\x03' #XY Data Points
            coordinateRecord = idBits
            for coordinate in thisBox.coordinates:
                x=struct.pack(">i",int(coordinate[0]))
                y=struct.pack(">i",int(coordinate[1]))
                coordinateRecord+=x
                coordinateRecord+=y
            self.writeRecord(coordinateRecord)

        idBits=b'\x11\x00' #End Of Element
        coordinateRecord = idBits
        self.writeRecord(coordinateRecord)

    def writeNextStructure(self,structureName):
        #first put in the structure head
        thisStructure = self.layoutObject.structures[structureName]
        idBits=b'\x05\x02'
        createYear = struct.pack(">h",thisStructure.createDate[0])
        createMonth = struct.pack(">h",thisStructure.createDate[1])
        createDay = struct.pack(">h",thisStructure.createDate[2])
        createHour = struct.pack(">h",thisStructure.createDate[3])
        createMinute = struct.pack(">h",thisStructure.createDate[4])
        createSecond = struct.pack(">h",thisStructure.createDate[5])
        modYear = struct.pack(">h",thisStructure.modDate[0])
        modMonth = struct.pack(">h",thisStructure.modDate[1])
        modDay = struct.pack(">h",thisStructure.modDate[2])
        modHour = struct.pack(">h",thisStructure.modDate[3])
        modMinute = struct.pack(">h",thisStructure.modDate[4])
        modSecond = struct.pack(">h",thisStructure.modDate[5])
        self.writeRecord(idBits+createYear+createMonth+createDay+createHour+createMinute+createSecond\
                         +modYear+modMonth+modDay+modHour+modMinute+modSecond)
        #now the structure name
        idBits=b'\x06\x06'
        ##caveat: the name needs to be an EVEN number of characters
        if(len(structureName)%2 == 1):
            #pad with a zero
            structureName = structureName + '\x00'
        self.writeRecord(idBits+structureName.encode())
        #now go through all the structure elements and write them in

        for boundary in thisStructure.boundaries:
            self.writeBoundary(boundary)
        for path in thisStructure.paths:
            self.writePath(path)
        for sref in thisStructure.srefs:
            self.writeSref(sref)
        for aref in thisStructure.arefs:
            self.writeAref(aref)
        for text in thisStructure.texts:
            self.writeText(text)
        for node in thisStructure.nodes:
            self.writeNode(node)
        for box in thisStructure.boxes:
            self.writeBox(box)
        #put in the structure tail
        idBits=b'\x07\x00'
        self.writeRecord(idBits)

    def writeGds2(self):
        self.writeHeader();  #first, put the header in
        #go through each structure in the layout and write it to the file
        for structureName in self.layoutObject.structures:
            self.writeNextStructure(structureName)
        #at the end, put in the END LIB record
        idBits=b'\x04\x00'
        self.writeRecord(idBits)

    def writeToFile(self,fileName):
        self.fileHandle = open(fileName,"wb")
        self.writeGds2()
        self.fileHandle.close()
