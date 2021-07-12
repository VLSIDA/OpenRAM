# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import datetime
import os
import debug
import verify
from characterizer import functional
from globals import OPTS, print_time
import shutil


class sram():
    """
    This is not a design module, but contains an SRAM design instance.
    It could later try options of number of banks and oganization to compare
    results.
    We can later add visualizer and other high-level functions as needed.
    """
    def __init__(self, sram_config, name):

        sram_config.set_local_config(self)

        # reset the static duplicate name checker for unit tests
        # in case we create more than one SRAM
        from design import design
        design.name_map=[]

        debug.info(2, "create sram of size {0} with {1} num of words {2} banks".format(self.word_size,
                                                                                       self.num_words,
                                                                                       self.num_banks))
        start_time = datetime.datetime.now()

        self.name = name

        if self.num_banks == 1:
            from sram_1bank import sram_1bank as sram
        elif self.num_banks == 2:
            from sram_2bank import sram_2bank as sram
        else:
            debug.error("Invalid number of banks.", -1)

        self.s = sram(name, sram_config)
        self.s.create_netlist()
        if not OPTS.netlist_only:
            self.s.create_layout()

        if not OPTS.is_unit_test:
            print_time("SRAM creation", datetime.datetime.now(), start_time)

    def sp_write(self, name, lvs=False, trim=False):
        self.s.sp_write(name, lvs, trim)

    def lef_write(self, name):
        self.s.lef_write(name)

    def gds_write(self, name):
        self.s.gds_write(name)

        # This addresses problems with flat GDS namespaces when we
        # want to merge this SRAM with other SRAMs.
        if OPTS.uniquify:
            import gdsMill
            gds = gdsMill.VlsiLayout()
            reader = gdsMill.Gds2reader(gds)
            reader.loadFromFile(name)

            # Uniquify but skip the library cells since they are hard coded
            try:
                from tech import library_prefix_name
            except ImportError:
                library_prefix_name = None
            gds.uniquify(library_prefix_name)

            writer = gdsMill.Gds2writer(gds)
            unique_name = name.replace(".gds", "_unique.gds")
            writer.writeToFile(unique_name)
            shutil.move(unique_name, name)

    def verilog_write(self, name):
        self.s.verilog_write(name)

    def extended_config_write(self, name):
        """Dump config file with all options.
           Include defaults and anything changed by input config."""
        f = open(name, "w")
        var_dict = dict((name, getattr(OPTS, name)) for name in dir(OPTS) if not name.startswith('__') and not callable(getattr(OPTS, name)))
        for var_name, var_value in var_dict.items():
            if isinstance(var_value, str):
                f.write(str(var_name) + " = " + "\"" + str(var_value) + "\"\n")
            else:
                f.write(str(var_name) + " = " + str(var_value)+ "\n")
        f.close()

    def save(self):
        """ Save all the output files while reporting time to do it as well. """

        # Save the spice file
        start_time = datetime.datetime.now()
        spname = OPTS.output_path + self.s.name + ".sp"
        debug.print_raw("SP: Writing to {0}".format(spname))
        self.sp_write(spname)
        functional(self.s,
                   os.path.basename(spname),
                   cycles=200,
                   output_path=OPTS.output_path)
        print_time("Spice writing", datetime.datetime.now(), start_time)

        if not OPTS.netlist_only:
            # Write the layout
            start_time = datetime.datetime.now()
            gdsname = OPTS.output_path + self.s.name + ".gds"
            debug.print_raw("GDS: Writing to {0}".format(gdsname))
            self.gds_write(gdsname)
            if OPTS.check_lvsdrc:
                verify.write_drc_script(cell_name=self.s.name,
                                        gds_name=os.path.basename(gdsname),
                                        extract=True,
                                        final_verification=True,
                                        output_path=OPTS.output_path)
            print_time("GDS", datetime.datetime.now(), start_time)

            # Create a LEF physical model
            start_time = datetime.datetime.now()
            lefname = OPTS.output_path + self.s.name + ".lef"
            debug.print_raw("LEF: Writing to {0}".format(lefname))
            self.lef_write(lefname)
            print_time("LEF", datetime.datetime.now(), start_time)

        # Save the LVS file
        start_time = datetime.datetime.now()
        lvsname = OPTS.output_path + self.s.name + ".lvs.sp"
        debug.print_raw("LVS: Writing to {0}".format(lvsname))
        self.sp_write(lvsname, lvs=True)
        if not OPTS.netlist_only and OPTS.check_lvsdrc:
            verify.write_lvs_script(cell_name=self.s.name,
                                    gds_name=os.path.basename(gdsname),
                                    sp_name=os.path.basename(lvsname),
                                    final_verification=True,
                                    output_path=OPTS.output_path)
        print_time("LVS writing", datetime.datetime.now(), start_time)

        # Save the extracted spice file
        if OPTS.use_pex:
            start_time = datetime.datetime.now()
            # Output the extracted design if requested
            pexname = OPTS.output_path + self.s.name + ".pex.sp"
            spname = OPTS.output_path + self.s.name + ".sp"
            verify.run_pex(self.s.name, gdsname, spname, output=pexname)
            sp_file = pexname
            print_time("Extraction", datetime.datetime.now(), start_time)
        else:
            # Use generated spice file for characterization
            sp_file = spname

        # Save a functional simulation file

        # Characterize the design
        start_time = datetime.datetime.now()
        from characterizer import lib
        debug.print_raw("LIB: Characterizing... ")
        lib(out_dir=OPTS.output_path, sram=self.s, sp_file=sp_file)
        print_time("Characterization", datetime.datetime.now(), start_time)

        # Write the config file
        start_time = datetime.datetime.now()
        from shutil import copyfile
        copyfile(OPTS.config_file, OPTS.output_path + OPTS.output_name + '.py')
        debug.print_raw("Config: Writing to {0}".format(OPTS.output_path + OPTS.output_name + '.py'))
        print_time("Config", datetime.datetime.now(), start_time)

        # Write the datasheet
        start_time = datetime.datetime.now()
        from datasheet_gen import datasheet_gen
        dname = OPTS.output_path + self.s.name + ".html"
        debug.print_raw("Datasheet: Writing to {0}".format(dname))
        datasheet_gen.datasheet_write(dname)
        print_time("Datasheet", datetime.datetime.now(), start_time)

        # Write a verilog model
        start_time = datetime.datetime.now()
        vname = OPTS.output_path + self.s.name + ".v"
        debug.print_raw("Verilog: Writing to {0}".format(vname))
        self.verilog_write(vname)
        print_time("Verilog", datetime.datetime.now(), start_time)

        # Write out options if specified
        if OPTS.output_extended_config:
            start_time = datetime.datetime.now()
            oname = OPTS.output_path + OPTS.output_name + "_extended.py"
            debug.print_raw("Extended Config: Writing to {0}".format(oname))
            self.extended_config_write(oname)
            print_time("Extended Config", datetime.datetime.now(), start_time)
