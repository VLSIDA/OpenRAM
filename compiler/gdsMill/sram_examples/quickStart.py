#!/usr/bin/env python
import gdsMill

gds_file = "sram_lib2.gds" #"gds_sram_tgate2.gds"
#creater a streamer object to interact with the cadence libraries
#streamer = gdsMill.GdsStreamer()

#use the streamer to take a cadence layout, and convert it to GDS 2 for us to work with
#the GDS will be named testLayoutA.gds
#streamer.streamFromCadence(cadenceLibraryContainerPath = "~/design/600nmAmi",
#                           libraryName = "gdsMillTest",
#                          cellName = "testLayoutA",
#                          outputPath = "./gdsFiles")

#create a layout object - this object represents all of the elements within the layout
myLayout = gdsMill.VlsiLayout()

#give our layout object to a gds reader object.  The gds reader will look at the binary gds 2 file and
#populate the layout object with the file's contents
reader = gdsMill.Gds2reader(myLayout)

#tell the reader object to process the gds file that we streamed in above
#un-comment the next line to see some details about the gds contents
#reader.debugToTerminal=1
reader.loadFromFile(gds_file)

#our layout object now contains all of the elements of the layout
#let add a box to the layout
#myLayout.addBox(layerNumber = myLayout.layerNumbersInUse[0],    #pick some layer
#                offsetInMicrons = (-10,0),  #location
#                width = 1.0,   #units are microns
#                height = 2.0,
#                updateInternalMap = True, #This is important for visualization - see note 1 below
#                center = True)  #origin is in the center or the bottom left corner
#Note 1:the layout object keeps track of its elements in a 2D map (no hiearachy)
#this makes visualization more efficient.  Therefore, to do a PDF output or some other
#flat output, you need to "update the internal map" of the layout object.  Only do this
# ONE TIME after all the objects you are manipulating are fixed

#let's take out new layout and stream it back into a cadence library
#first, create a new GDS
#we change the root structure name (this will be the cellview name upon stream in)
myLayout.rename("testLayoutB")
writer = gdsMill.Gds2writer(myLayout)
writer.writeToFile("testLayoutB.gds")

streamer.streamToCadence(cadenceLibraryContainerPath = "~/design/600nmAmi",
                         libraryName = "gdsMillTest",
                         inputPath = "./gdsFiles/testLayoutB.gds")

#let's create a PDF view of the layout object
#first, create the object to represent the visual output
visualizer = gdsMill.PdfLayout(myLayout)

#since we have no knowledge of what the layer numbers mean for this particular technology
#we need to assign some colors to them

#uncomment the following line if you want to actually see the layout numbers in use
#print myLayout.layerNumbersInUse

#for each layer number used in the layout, we will asign it a layer color as a RGB Hex
visualizer.layerColors[myLayout.layerNumbersInUse[0]]="#219E1C"
visualizer.layerColors[myLayout.layerNumbersInUse[1]]="#271C9E"
visualizer.layerColors[myLayout.layerNumbersInUse[2]]="#CC54C8"
visualizer.layerColors[myLayout.layerNumbersInUse[3]]="#E9C514"
visualizer.layerColors[myLayout.layerNumbersInUse[4]]="#856F00"
#visualizer.layerColors[myLayout.layerNumbersInUse[5]]="#BD1444"
#visualizer.layerColors[myLayout.layerNumbersInUse[6]]="#FD1444"
#visualizer.layerColors[myLayout.layerNumbersInUse[7]]="#FD1414"

#set the scale so that our PDF isn't enormous
visualizer.setScale(500)
#tell the pdf layout object to draw everything in our layout
visualizer.drawLayout()
#and finally, dump it out to a file
visualizer.writeToFile("./gdsFiles/gdsOut.pdf")

