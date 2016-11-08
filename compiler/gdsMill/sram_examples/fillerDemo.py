#!/usr/bin/env python
import gdsMill

#we will add the filler at a higher level of hiearchy
#so first, load our top level layout from GDS
myTopLevelLayout = gdsMill.VlsiLayout()
reader = gdsMill.Gds2reader(myTopLevelLayout)
reader.loadFromFile("./gdsFiles/testLayoutA.gds")

#now create a new layout
#be sure to assign a name, since this will be the root object in our hierarchy to which
#all other objects are referenced
filledLayout = gdsMill.VlsiLayout(name="filledLayout")

#now place an instnace of our top level layout into the filled layout
#hierarchy looks like this:
#   filled layout
#       top level layout
#           layout elements
#           layout elements
#           layout elements
#       fill elements
#       fill elements .....
filledLayout.addInstance(myTopLevelLayout,
                                offsetInMicrons = (0,0),
                                mirror = "",
                                rotate = 0.0)

#now actaully add the fill - gds mill will create an array of boxes
# maintaining spacing from existing layout elements
#we'll do it once for two different layers
filledLayout.fillAreaDensity(layerToFill = myTopLevelLayout.layerNumbersInUse[5],
                            offsetInMicrons = (-10.0,-10.0), #this is where to start from
                            coverageWidth = 40.0,  #size of the fill area in microns
                            coverageHeight = 40.0,
                            minSpacing = 0.5,  #distance between fill blocks
                            blockSize = 2.0 #width and height of each filler block in microns
                            )
filledLayout.fillAreaDensity(layerToFill = myTopLevelLayout.layerNumbersInUse[7],
                            offsetInMicrons = (-11.0,-11.0), #this is where to start from
                            coverageWidth = 40.0,  #size of the fill area in microns
                            coverageHeight = 40.0,
                            minSpacing = 0.5,  #distance between fill blocks
                            blockSize = 3.0 #width and height of each filler block in microns
                            )
#and now dump the filled layout to a new GDS file
writer = gdsMill.Gds2writer(filledLayout)
writer.writeToFile("./gdsFiles/filledLayout.gds")
#and strea
streamer = gdsMill.GdsStreamer()
streamer.streamToCadence(cadenceLibraryContainerPath = "~/design/600nmAmi",
                         libraryName = "gdsMillTest",
                         inputPath = "./gdsFiles/filledLayout.gds")
