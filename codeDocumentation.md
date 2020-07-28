# Configuration file

The configuration file is the starting point, it is the highest level of the OpenRAM, which the used uses to initialize all the variables needed for the compiler. For more information about the configuration file and the options please look at the Documentation README file provided in the repository.

# Compiler

## openram.py

openram.py is the first file that initializes the compiler with the variables that the user set in the configuration file, outputs the compilation information in runtime. This module then calls the sram class with the options it took from the configuration files.

## globals.py

This is one of the most important modules in the OpenRAM as it is responsible for setting up the OpenRAM, it parses all the options, sets the technology (default technology is the scmos technology that can be overridden from the configuration file). This module also run checks for the required tools and their versions, for the project dependencies please check out the README file. Determines the correct custom or parameterized bitcell for the design. It also reads the configuration file, *This will only actually get read the first time. Subsequent reads will just restore the previous copy*. There's also a function for overriding the configuration file from the command line, except for the technology. There are 2 functions for cleaning up the openram, which is ``` end_openram() ``` and  ```cleanup_paths() ```, the cleanup_paths function deletes the output files from the temp directory. 

If the user specifies a write mask size, it needs to be less than or equal to half the word size and a multiple of the word size. If the user specified the write size mask equal to the word size the compiler will print an error, this error is just to let the user know that the mask specified is equal to the word size and that the whole word will be written at once, but the compiler won't abort, it will continue compiling.

## sram class

The sram class instantiates the sram design and the top module creates and prints the output files, so it has the lvs, gds, sp, lef and verilog writers. 

### sram_bank1 & sram_bank2

This class is specific for producing sram for the specified banks, these classes adds the modules and busses needed in the top-level module to connect the banks. The function ``` add_lvs_correspondence_points(self) ``` is a function for easing the debugging process, where it adds bus names to the lvs, but this should be turned off by default, as these additions will be extracted in the netlist as ports.

### sram_base

Dynamically generated SRAM by connecting banks to control logic. 

## Verify Class

This is a module that will import the correct DRC/LVS/PEX module based on what tools are found. It is a layer of indirection to enable multiple verification tool support.
The verify class will use the tools appropriate to each technology, tools supported are magic, netgen, calibre and assura. These tools can be overwritten in the configuration file, so if you want the compiler to use one specific tool from these 4, you can do it in the configuration file.

## Tests Class

This class has all the tests that you would need, starting from code format check all the way to tools and technology tests. This is a great class for debugging, as you can run specific tests on parts that you are unsure about or to run the regress.py test which will automatically run all tests. Disclaimer, if you don't have all the tools that OpenRAM supports some tests specific for these tools will fail. 

## Router Class

A router class to read an obstruction map from a gds and plan a route on a given layer. This is limited to two-layer routes. It populates blockages on a grid class. The class imports the gds files and starts overwriting some layers in order to make paths and pins on the layout needed for connecting the sram modules together. This class would be useful when debugging if you have a pin or path misplaced, this would be where to look.

## pagtes

This class is the one that generates gds and spice models to the nmos and pmos. It is the class that determines the gates' widths. This would only be useful if you have an issue with running the lvs tests and there is an error with the gates' widths, other than that this wouldn't be as useful for developers as it is already set. The other modules in this class is building the smallest building blocks in the sram, like the pmos and nmos, the single level column multiplexer, pnand, etc. 

## modules & custom

The modules class is actually one of the most important classes in the OpenRAM compiler, it is the class that the sram class takes all the building blocks from, and one module in this class is the bank.py, which generates the whole bank including bitcell array, hierarchical_decoder, precharge, (optional column_mux and column decoder), write driver and sense amplifiers. These modules that the bank uses are also defined in the same class, so this takes the pgates' small building blocks and builds bigger building blocks all the way to a single bank or multibanks. This class would actually be the best class for a developer to debug LVS and DRC errors, because each module defines a different building block. The custom has some more modules that might be used in the sram, and different configurations to the decoder, for example using and not nand gates.

## GgsMill

GdsMill is a python library that the compiler uses in order to import and manipulate gds files, this library can do anything from drawing different layers to importing and building an array of gds files and then writing it to a bigger gds file. This library is used in other projects as well but in the OpenRAM it is modified in order to support some OpenRAM attributes. For the GdsMill manual [click here](http://michaelwieckowski.com/software/). 

## drc

This class defines the design rules that the user gives the compiler using the technology, it builds a lookup table full of design rules Each element is a tuple with the last value being the rule. It searches through backwards until all of the key values are met and returns the rule value. For example, the key values can be width and length, and it would return the rule for a wire of at least a given width and length. A dimension can be ignored by passing inf.

## datasheet

The datasheet class parses the output files and put the values in a .html file that can be viewed on your browser, this is a clean and easy way for the user to see the value output without having to go through the output files. 

## characterizer

The characterizer is extremely important for anyone that's using OpenRAM, it is the class that reads the output spice files using ngspice, and does some tests on them, and then outputs some measurements like the setup hold times and delays, which is extremely important when experimenting on the OpenRAM to monitor the behavior of the sram, and see if it does what you want it to do. Moreover, this class modifies the output netlists by removing the redundant parts of it in order to optimize the performance.

## bitcells

This class is where the bit cells and defined, or the building blocks of the memory cells. It takes 6T, 8T, etc. bitcells. These bitcells are actually blackboxed so that it doesn't get tested by the drc and lvs, so if you have a warning from these cells don't worry about it.

# Technology

The technology files should be added by the user but the OpenRAM has 3 default technologies that are fully compatible with the OpenRAM. For more information of how to introduce more technologies to the OpenRAM please read the README file.

It has the technolgy files that define the layers, datatypes and design rules needed. It should also include gds, lvs and sp files that describes some building blocks that the compiler will work with.
