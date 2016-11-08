#!/usr/bin/env python
import gdsMill
#we are going to make an array of instances of an existing layout
#assume that we designed the "base cell" in cadence
#step 1 is to stream it out of cadence into a GDS to work with
#   creater a streamer object to interact with the cadence libraries
streamer = gdsMill.GdsStreamer()

#   use the streamer to take a cadence layout, and convert it to GDS 2 for us to work with
#   the GDS will be named testLayoutA.gds
#streamer.streamFromCadence(cadenceLibraryContainerPath = "~/design/600nmAmi",
#                           libraryName = "gdsMillTest",
#                           cellName = "testLayoutA",
#                           outputPath = "./gdsFiles")

#next, load our base cell layout from the GDS generated above
arrayCellLayout = gdsMill.VlsiLayout()
reader = gdsMill.Gds2reader(arrayCellLayout)
reader.loadFromFile("./gdsFiles/testLayoutA.gds")

##since we will be streaming into the same library that testLayout came from
#let's rename it here so that we don't overwrite accidentally later
arrayCellLayout.rename("arrayCell")

#now create a new layout
#be sure to assign a name, since this will be the root object in our hierarchy to which
#all other objects are referenced
newLayout = gdsMill.VlsiLayout(name="arrayExample")

#now place an instnace of our top level layout into the filled layout
#hierarchy looks like this:
#   array example
#       array cell layout
#           layout elements
#           layout elements
#           layout elements
#       cell instance
#       cell instance
#       cell instance
#       connection elements .....

#now create the array of instances
for xIndex in range(0,10):
    for yIndex in range(0,10):
        if(yIndex%2 == 0):
            mirror = "MX"
        else:
            mirror = "R0"
        newLayout.addInstance(arrayCellLayout,
                              offsetInMicrons = (xIndex*10.0,yIndex*15.0),
                              mirror = mirror,
                              rotate = 0.0)

#add a "wire" that in a real example might be a power rail, data bus, etc.
newLayout.addPath(layerNumber = newLayout.layerNumbersInUse[7],
                  coordinates = [(-20.0,0.0),(25.0,0),(25.0,10.0)],
                  width = 1.0)

#add some text that in a real example might be an I/O pin
newLayout.addText(text = "Hello",
                  layerNumber = newLayout.layerNumbersInUse[5],
                  offsetInMicrons = (0,0),
                  magnification = 1,
                  rotate = None)


newLayout.prepareForWrite()

#and now dump the filled layout to a new GDS file
writer = gdsMill.Gds2writer(newLayout)
writer.writeToFile("./gdsFiles/arrayLayout.gds")
#and stream it into cadence
#streamer.streamToCadence(cadenceLibraryContainerPath = "~/design/600nmAmi",
#                         libraryName = "gdsMillTest",
#                         inputPath = "./gdsFiles/arrayLayout.gds")
