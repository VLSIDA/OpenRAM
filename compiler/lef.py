import gdsMill
import tech
import globals
import math
import debug
import datetime
from collections import defaultdict

class lef:
    """
    SRAM LEF Class open GDS file, read pins information, obstruction
    and write them to LEF file
    """
    def __init__(self,layers):
        # LEF db units per micron
        self.lef_units = 1000
        # These are the layers of the obstructions
        self.lef_layers = layers

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

        self.lef.write("SITE  MacroSite\n")
        self.indent += "   "
        self.lef.write("{0}CLASS Core ;\n".format(self.indent))
        self.lef.write("{0}SIZE {1} by {2} ;\n".format(self.indent,
                                                       self.lef_units*self.width,
                                                       self.lef_units*self.height))
        self.indent = self.indent[:-3]
        self.lef.write("END  MacroSite\n")
        
        self.lef.write("{0}MACRO {1}\n".format(self.indent,self.name))
        self.indent += "   "
        self.lef.write("{0}CLASS BLOCK ;\n".format(self.indent))
        self.lef.write("{0}SIZE {1} BY {2} ;\n" .format(self.indent,
                                                        self.lef_units*self.width,
                                                        self.lef_units*self.height))
        self.lef.write("{0}SYMMETRY X Y R90 ;\n".format(self.indent))
        self.lef.write("{0}SITE MacroSite ;\n".format(self.indent))

        
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
            self.lef_write_rect(pin.rect)
            
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
            blockages = self.get_blockages(layer,True)
            for b in blockages:
                self.lef_write_rect(b)
            self.indent = self.indent[:-3]
        self.lef.write("{0}END\n".format(self.indent))

    def lef_write_rect(self, rect):
        """ Write a LEF rectangle """
        self.lef.write("{0}RECT ".format(self.indent)) 
        for item in rect:
            self.lef.write(" {0} {1}".format(self.lef_units*item[0], self.lef_units*item[1]))
        self.lef.write(" ;\n")
