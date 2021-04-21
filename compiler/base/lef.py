# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
from tech import layer_names
import os
import shutil
from globals import OPTS
from vector import vector
from pin_layout import pin_layout


class lef:
    """
    SRAM LEF Class open GDS file, read pins information, obstruction
    and write them to LEF file.
    This is inherited by the sram_base class.
    """
    def __init__(self, layers):
        # LEF db units per micron
        self.lef_units = 2000
        # These are the layers of the obstructions
        self.lef_layers = layers
        # Round to ensure float values are divisible by 0.0025 (the manufacturing grid)
        self.round_grid = 4

    def magic_lef_write(self, lef_name):
        """ Use a magic script to perform LEF creation. """
        debug.info(3, "Writing abstracted LEF to {0}".format(lef_name))

        # Copy .magicrc file into the output directory
        magic_file = OPTS.openram_tech + "tech/.magicrc"
        if os.path.exists(magic_file):
            shutil.copy(magic_file, OPTS.openram_temp)
        else:
            debug.warning("Could not locate .magicrc file: {}".format(magic_file))

        gds_name = OPTS.openram_temp + "{}.gds".format(self.name)
        self.gds_write(gds_name)

        run_file = OPTS.openram_temp + "run_lef.sh"
        f = open(run_file, "w")
        f.write("#!/bin/sh\n")
        f.write('export OPENRAM_TECH="{}"\n'.format(os.environ['OPENRAM_TECH']))
        f.write('echo "$(date): Starting GDS to MAG using Magic {}"\n'.format(OPTS.drc_exe[1]))
        f.write('\n')
        f.write("{} -dnull -noconsole << EOF\n".format(OPTS.drc_exe[1]))
        f.write("drc off\n")
        f.write("gds polygon subcell true\n")
        f.write("gds warning default\n")
        f.write("gds flatten true\n")
        f.write("gds ordering true\n")
        f.write("gds readonly true\n")
        f.write("gds read {}\n".format(gds_name))
        f.write('puts "Finished reading gds {}"\n'.format(gds_name))
        f.write("load {}\n".format(self.name))
        f.write('puts "Finished loading cell {}"\n'.format(self.name))
        f.write("cellname delete \\(UNNAMED\\)\n")
        f.write("lef write {} -hide\n".format(lef_name))
        f.write('puts "Finished writing LEF cell {}"\n'.format(self.name))
        f.close()
        os.system("chmod u+x {}".format(run_file))
        from run_script import run_script
        (outfile, errfile, resultsfile) = run_script(self.name, "lef")

    def lef_write(self, lef_name):
        """ Write the entire lef of the object to the file. """

        if OPTS.detailed_lef:
            debug.info(3, "Writing detailed LEF to {0}".format(lef_name))
            self.detailed_lef_write(lef_name)
        else:
            debug.info(3, "Writing abstract LEF to {0}".format(lef_name))
            # Can possibly use magic lef write to create the LEF
            # if OPTS.drc_exe and OPTS.drc_exe[0] == "magic":
            #     self.magic_lef_write(lef_name)
            #     return
            self.abstract_lef_write(lef_name)

    def abstract_lef_write(self, lef_name):
        # To maintain the indent level easily
        self.indent = "" 

        self.lef  = open(lef_name, "w")
        self.lef_write_header()

        # Start with blockages on all layers the size of the block
        # minus the pin escape margin (hard coded to 4 x m3 pitch)
        # These are a pin_layout to use their geometric functions
        perimeter_margin = self.m3_pitch
        self.blockages = {}
        for layer_name in self.lef_layers:
            self.blockages[layer_name]=[]
        for layer_name in self.lef_layers:
            ll = vector(perimeter_margin, perimeter_margin)
            ur = vector(self.width - perimeter_margin, self.height - perimeter_margin)
            self.blockages[layer_name].append(pin_layout("",
                                                         [ll, ur],
                                                         layer_name))

        # For each pin, remove the blockage and add the pin
        for pin_name in self.pins:
            pin = self.get_pin(pin_name)
            inflated_pin = pin.inflated_pin(multiple=1)
            for blockage in self.blockages[pin.layer]:
                if blockage.overlaps(inflated_pin):
                    intersection_shape = blockage.intersection(inflated_pin)
                    # If it is zero area, don't add the pin
                    if intersection_shape[0][0]==intersection_shape[1][0] or intersection_shape[0][1]==intersection_shape[1][1]:
                        continue
                    # Remove the old blockage and add the new ones
                    self.blockages[pin.layer].remove(blockage)
                    intersection_pin = pin_layout("", intersection_shape, inflated_pin.layer)
                    new_blockages = blockage.cut(intersection_pin)
                    self.blockages[pin.layer].extend(new_blockages)

            self.lef_write_pin(pin_name)

        self.lef_write_obstructions(abstracted=True)
        self.lef_write_footer()
        self.lef.close()

    def detailed_lef_write(self, lef_name):
        # To maintain the indent level easily
        self.indent = ""

        self.lef  = open(lef_name, "w")
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

        self.lef.write("{0}MACRO {1}\n".format(self.indent, self.name))
        self.indent += "   "
        self.lef.write("{0}CLASS BLOCK ;\n".format(self.indent))
        self.lef.write("{0}SIZE {1} BY {2} ;\n" .format(self.indent,
                                                        round(self.width, self.round_grid),
                                                        round(self.height, self.round_grid)))
        self.lef.write("{0}SYMMETRY X Y R90 ;\n".format(self.indent))

    def lef_write_footer(self):
        self.lef.write("{0}END    {1}\n".format(self.indent, self.name))
        self.indent = self.indent[:-3]
        self.lef.write("END    LIBRARY\n")

    def lef_write_pin(self, name):
        pin_dir = self.get_pin_dir(name)
        pin_type = self.get_pin_type(name)
        self.lef.write("{0}PIN {1}\n".format(self.indent, name))
        self.indent += "   "

        self.lef.write("{0}DIRECTION {1} ;\n".format(self.indent, pin_dir))

        if pin_type in ["POWER", "GROUND"]:
            self.lef.write("{0}USE {1} ; \n".format(self.indent, pin_type))
            self.lef.write("{0}SHAPE ABUTMENT ; \n".format(self.indent))

        self.lef.write("{0}PORT\n".format(self.indent))
        self.indent += "   "

        # We could sort these together to minimize different layer sections, but meh.
        pin_list = self.get_pins(name)
        for pin in pin_list:
            self.lef.write("{0}LAYER {1} ;\n".format(self.indent, layer_names[pin.layer]))
            self.lef_write_shape(pin.rect)

        # End the PORT
        self.indent = self.indent[:-3]
        self.lef.write("{0}END\n".format(self.indent))

        # End the PIN
        self.indent = self.indent[:-3]
        self.lef.write("{0}END {1}\n".format(self.indent, name))

    def lef_write_obstructions(self, abstracted=False):
        """ Write all the obstructions on each layer """
        self.lef.write("{0}OBS\n".format(self.indent))
        for layer in self.lef_layers:
            self.lef.write("{0}LAYER  {1} ;\n".format(self.indent, layer_names[layer]))
            self.indent += "   "
            if abstracted:
                blockages = self.blockages[layer]
                for b in blockages:
                    self.lef_write_shape(b.rect)
            else:
                blockages = self.get_blockages(layer, True)
                for b in blockages:
                    self.lef_write_shape(b)
            self.indent = self.indent[:-3]
        self.lef.write("{0}END\n".format(self.indent))

    def lef_write_shape(self, obj):
        if len(obj) == 2:
            """ Write a LEF rectangle """
            self.lef.write("{0}RECT ".format(self.indent))
            for item in obj:
                # print(obj)
                self.lef.write(" {0} {1}".format(round(item[0],
                                                       self.round_grid),
                                                 round(item[1],
                                                       self.round_grid)))
            self.lef.write(" ;\n")
        else:
            """ Write a LEF polygon """
            self.lef.write("{0}POLYGON ".format(self.indent))
            for item in obj:
                self.lef.write(" {0} {1}".format(round(item[0],
                                                       self.round_grid),
                                                 round(item[1],
                                                       self.round_grid)))
            self.lef.write(" ;\n")

