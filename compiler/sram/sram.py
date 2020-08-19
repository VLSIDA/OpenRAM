# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import datetime
import debug
from globals import OPTS, print_time


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
    
    def sp_write(self, name):
        self.s.sp_write(name)

    def lvs_write(self, name):
        self.s.lvs_write(name)
        
    def lef_write(self, name):
        self.s.lef_write(name)

    def gds_write(self, name):
        self.s.gds_write(name)

    def verilog_write(self, name):
        self.s.verilog_write(name)

    def save(self):
        """ Save all the output files while reporting time to do it as well. """

        if not OPTS.netlist_only:
            # Create a LEF physical model
            start_time = datetime.datetime.now()
            lefname = OPTS.output_path + self.s.name + ".lef"
            debug.print_raw("LEF: Writing to {0}".format(lefname))
            self.lef_write(lefname)
            print_time("LEF", datetime.datetime.now(), start_time)

            # Write the layout
            start_time = datetime.datetime.now()
            gdsname = OPTS.output_path + self.s.name + ".gds"
            debug.print_raw("GDS: Writing to {0}".format(gdsname))
            self.gds_write(gdsname)
            print_time("GDS", datetime.datetime.now(), start_time)

        # Save the spice file
        start_time = datetime.datetime.now()
        spname = OPTS.output_path + self.s.name + ".sp"
        debug.print_raw("SP: Writing to {0}".format(spname))
        self.sp_write(spname)
        print_time("Spice writing", datetime.datetime.now(), start_time)

        # Save the LVS file
        start_time = datetime.datetime.now()
        lvsname = OPTS.output_path + self.s.name + ".lvs.sp"
        debug.print_raw("LVS: Writing to {0}".format(lvsname))
        self.lvs_write(lvsname)
        print_time("LVS writing", datetime.datetime.now(), start_time)
        
        # Save the extracted spice file
        if OPTS.use_pex:
            import verify
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
