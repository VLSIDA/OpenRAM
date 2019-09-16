# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import gdsMill
import tech
import globals
import math
import debug
import datetime
from collections import defaultdict
import pdb

class lef:
    """
    SRAM LEF Class open GDS file, read pins information, obstruction
    and write them to LEF file.
    This is inherited by the sram_base class.
    """
    def __init__(self,layers):
        # LEF db units per micron
        self.lef_units = 2000
        # These are the layers of the obstructions
        self.lef_layers = layers
        # Round to ensure float values are divisible by 0.0025 (the manufacturing grid)
        self.round_grid = 4;

    def lef_write(self, lef_name):
        """Write the entire lef of the object to the file."""
        debug.info(3, "Writing to {0}".format(lef_name))

        self.indent = "" # To maintain the indent level easily

        self.lef  = open(lef_name,"w")
        self.lef_write_header()
        for pin in self.pins:
            self.lef_write_pin(pin)
        self.lef_write_obstructions()
        self.lef_write_footer()
        self.lef.close()
        
    def lef_write_header(self):
        """ Header of LEF file """
        self.lef.write("VERSION 5.4 ;\n")
        self.lef.write("NAMESCASESENSITIVE ON ;\n")
        self.lef.write("BUSBITCHARS \"[]\" ;\n")
        self.lef.write("DIVIDERCHAR \"/\" ;\n")
        self.lef.write("UNITS\n")
        self.lef.write("  DATABASE MICRONS {0} ;\n".format(self.lef_units))
        self.lef.write("END UNITS\n")
        
        self.lef.write("{0}MACRO {1}\n".format(self.indent,self.name))
        self.indent += "   "
        self.lef.write("{0}CLASS BLOCK ;\n".format(self.indent))
        self.lef.write("{0}SIZE {1} BY {2} ;\n" .format(self.indent,
                                                        round(self.width,self.round_grid),
                                                        round(self.height,self.round_grid)))
        self.lef.write("{0}SYMMETRY X Y R90 ;\n".format(self.indent))
        
    def lef_write_footer(self):
        self.lef.write("{0}END    {1}\n".format(self.indent,self.name))
        self.indent = self.indent[:-3]
        self.lef.write("END    LIBRARY\n")
        
        
    def lef_write_pin(self, name):
        pin_dir = self.get_pin_dir(name)
        pin_type = self.get_pin_type(name)
        self.lef.write("{0}PIN {1}\n".format(self.indent,name))
        self.indent += "   "
        
        self.lef.write("{0}DIRECTION {1} ;\n".format(self.indent,pin_dir))
        
        if pin_type in ["POWER","GROUND"]:
            self.lef.write("{0}USE {1} ; \n".format(self.indent,pin_type))
            self.lef.write("{0}SHAPE ABUTMENT ; \n".format(self.indent))
            
        self.lef.write("{0}PORT\n".format(self.indent))
        self.indent += "   "

        # We could sort these together to minimize different layer sections, but meh.
        pin_list = self.get_pins(name)
        for pin in pin_list:
            self.lef.write("{0}LAYER {1} ;\n".format(self.indent,pin.layer))
            self.lef_write_shape(pin.rect)
            
        # End the PORT
        self.indent = self.indent[:-3]
        self.lef.write("{0}END\n".format(self.indent))

        # End the PIN
        self.indent = self.indent[:-3]
        self.lef.write("{0}END {1}\n".format(self.indent,name))
            
    def lef_write_obstructions(self):
        """ Write all the obstructions on each layer """
        self.lef.write("{0}OBS\n".format(self.indent))
        for layer in self.lef_layers:
            self.lef.write("{0}LAYER  {1} ;\n".format(self.indent,layer))
            self.indent += "   "
            # pdb.set_trace()
            blockages = self.get_blockages(layer,True)
            for b in blockages:
                # if len(b) > 2:
                #     print(b)
                self.lef_write_shape(b)
            self.indent = self.indent[:-3]
        self.lef.write("{0}END\n".format(self.indent))

    def lef_write_shape(self, rect):
        if len(rect) == 2: 
            """ Write a LEF rectangle """
            self.lef.write("{0}RECT ".format(self.indent)) 
            for item in rect:
                # print(rect)
                self.lef.write(" {0} {1}".format(round(item[0],self.round_grid), round(item[1],self.round_grid)))
            self.lef.write(" ;\n")
        else:            
            """ Write a LEF polygon """
            self.lef.write("{0}POLYGON ".format(self.indent)) 
            for item in rect:
                self.lef.write(" {0} {1}".format(round(item[0],self.round_grid), round(item[1],self.round_grid)))
            # for i in range(0,len(rect)):
                # self.lef.write(" {0} {1}".format(round(rect[i][0],self.round_grid), round(rect[i][1],self.round_grid)))
            self.lef.write(" ;\n")

