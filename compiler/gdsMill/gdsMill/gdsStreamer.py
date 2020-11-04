import os

class GdsStreamer:
    """
    This class is used to stream GDS files in and out of the Cadence toolsuite.
    """
    def __init__(self, workingDirectory = "."):
        self.workingDirectory = os.path.abspath(workingDirectory)

    def createStreamOutTemplate(self, sourceLibraryName, sourceCellName, gdsDestinationPath):
        templateFile = open(self.workingDirectory+"/partStreamOut.tmpl","w")
        templateFile.write("streamOutKeys = list(nil\n")
        templateFile.write("'runDir			\".\"\n")
        templateFile.write("'libName		\""+sourceLibraryName+"\"\n")
        templateFile.write("'primaryCell		\""+sourceCellName+"\"\n")
        templateFile.write("'viewName		\"layout\"\n")
        templateFile.write("'outFile		\""+gdsDestinationPath+"/"+sourceCellName+".gds\"\n")
        templateFile.write("'scale			0.001000\n")
        templateFile.write("'units			\"micron\"\n")
        templateFile.write("'compression		\"none\"\n")
        templateFile.write("'hierDepth		32\n")
        templateFile.write("'convertToGeo		nil\n")
        templateFile.write("'maxVertices		200\n")
        templateFile.write("'refLib			nil\n")
        templateFile.write("'libVersion		\"5.0\"\n")
        templateFile.write("'checkPolygon		nil\n")
        templateFile.write("'snapToGrid		nil\n")
        templateFile.write("'simMosaicToArray	t\n")
        templateFile.write("'caseSensitivity	\"preserve\"\n")
        templateFile.write("'lineToZeroPath		\"path\"\n")
        templateFile.write("'convertDot	\"ignore\"\n")
        templateFile.write("'rectToBox		nil\n")
        templateFile.write("'convertPathToPoly	nil\n")
        templateFile.write("'keepPcell	nil\n")
        templateFile.write("'replaceBusBitChar	nil\n")
        templateFile.write("'useParentXYforText	nil\n")
        templateFile.write("'reportPrecision	nil\n")
        templateFile.write("'runQuiet		nil\n")
        templateFile.write("'comprehensiveLog		nil\n")
        templateFile.write("'ignorePcellEvalFail		nil\n")
        templateFile.write("'errFile		\"PIPO.LOG\"\n")
        templateFile.write("'NOUnmappingLayerWarning		nil\n")
        templateFile.write("'techFileChoice		nil\n")
        templateFile.write("'pcellSuffix		\"DbId\"\n")
        templateFile.write("'respectGDSIILimits		nil\n")
        templateFile.write("'dumpPcellInfo		nil\n")
        templateFile.write("'genListHier		nil\n")
        templateFile.write("'cellMapTable		\"\"\n")
        templateFile.write("'layerTable		\"\"\n")
        templateFile.write("'textFontTable		\"\"\n")
        templateFile.write("'convertPin		\"geometry\"\n")
        templateFile.write("'pinInfo		0\n")
        templateFile.write("'pinTextMapTable	\"\"\n")
        templateFile.write("'propMapTable		\"\"\n")
        templateFile.write("'propSeparator		\",\"\n")
        templateFile.write("'userSkillFile		\"\"\n")
        templateFile.write("'rodDir			\"\"\n")
        templateFile.write("'refLibList		\"\"\n")
        templateFile.write(")\n")
        templateFile.close()

    def createStreamInTemplate(self, sourceLibraryName = None,inputGdsPath = None, retainReferenceLibraries = True):
        # retainReferenceLibraries added to tell PIPO whether it should import all SREFS as new cellviews or to
        #look inside of existing libraries for cellviews with the same name.
        templateParameters = dict()
        if retainReferenceLibraries:
            templateParameters["ref"] = "t"
        else:
            templateParameters["ref"] = "nil"
        templateFile = open(self.workingDirectory+"/partStreamIn.tmpl","w")
        templateFile.write("streamInKeys = list(nil\n")
        templateFile.write("'runDir			\".\"\n")
        templateFile.write("'inFile		\""+inputGdsPath+"\"\n")
        templateFile.write("'primaryCell		\"\"\n")
        templateFile.write("'libName		\""+sourceLibraryName+"\"\n")
        templateFile.write("'techFileName		\"\"\n")
        templateFile.write("'scale			0.001000\n")
        templateFile.write("'units			\"micron\"\n")
        templateFile.write("'errFile		\"PIPO.LOG\"\n")
        templateFile.write("'refLib			"+templateParameters["ref"]+"\n")
        templateFile.write("'hierDepth		32\n")
        templateFile.write("'maxVertices		1024\n")
        templateFile.write("'checkPolygon		nil\n")
        templateFile.write("'snapToGrid		nil\n")
        templateFile.write("'arrayToSimMosaic	t\n")
        templateFile.write("'caseSensitivity	\"preserve\"\n")
        templateFile.write("'zeroPathToLine		\"path\"\n")
        templateFile.write("'convertNode	\"ignore\"\n")
        templateFile.write("'keepPcell	nil\n")
        templateFile.write("'replaceBusBitChar	nil\n")
        templateFile.write("'skipUndefinedLPP	nil\n")
        templateFile.write("'ignoreBox	        nil\n")
        templateFile.write("'mergeUndefPurposToDrawing	nil\n")
        templateFile.write("'reportPrecision	nil\n")
        templateFile.write("'keepStreamCells		nil\n")
        templateFile.write("'attachTechfileOfLib		\"\"\n")
        templateFile.write("'runQuiet		nil\n")
        templateFile.write("'noWriteExistCell		nil\n")
        templateFile.write("'NOUnmappingLayerWarning		nil\n")
        templateFile.write("'comprehensiveLog		nil\n")
        templateFile.write("'ignorePcellEvalFail		nil\n")
        templateFile.write("'appendDB		nil\n")
        templateFile.write("'genListHier		nil\n")
        templateFile.write("'cellMapTable		\"\"\n")
        templateFile.write("'layerTable		\"\"\n")
        templateFile.write("'textFontTable		\"\"\n")
        templateFile.write("'restorePin		0\n")
        templateFile.write("'propMapTable		\"\"\n")
        templateFile.write("'propSeparator		\",\"\n")
        templateFile.write("'userSkillFile		\"\"\n")
        templateFile.write("'rodDir			\"\"\n")
        templateFile.write("'refLibOrder			\"\"\n")
        templateFile.write(")\n")
        templateFile.close()

    def streamFromCadence(self, cadenceLibraryContainerPath, libraryName, cellName, outputPath):
        #change into the cadence directory
        outputPath = os.path.abspath(outputPath)
        currentPath = os.path.abspath(".")
        os.chdir(cadenceLibraryContainerPath)
        self.createStreamOutTemplate(libraryName,cellName,outputPath)
        #stream the gds out from cadence
        worker = os.popen("pipo strmout "+self.workingDirectory+"/partStreamOut.tmpl")
        #dump the outputs to the screen line by line
        print("Streaming Out From Cadence......")
        while 1:
            line = worker.readline()
            if not line: break  #this means sim is finished so jump out
            #else: print(line)   #for debug only
        worker.close()
        #now remove the template file
        os.remove(self.workingDirectory+"/partStreamOut.tmpl")
        #and go back to whever it was we started from
        os.chdir(currentPath)

    def streamToCadence(self,cadenceLibraryContainerPath, libraryName, inputPath):
        #change into the cadence directory
        inputPath = os.path.abspath(inputPath)
        currentPath = os.path.abspath(".")
        os.chdir(cadenceLibraryContainerPath)
        self.createStreamInTemplate(libraryName,inputPath)
        #stream the gds out from cadence
        worker = os.popen("pipo strmin "+self.workingDirectory+"/partStreamIn.tmpl")
        #dump the outputs to the screen line by line
        print("Streaming In To Cadence......")
        while 1:
            line = worker.readline()
            if not line: break  #this means sim is finished so jump out
            #else: print(line)   #for debug only
        worker.close()
        #now remove the template file
        os.remove(self.workingDirectory+"/partStreamIn.tmpl")
        #and go back to whever it was we started from
        os.chdir(currentPath)
