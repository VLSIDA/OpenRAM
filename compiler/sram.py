# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os
import shutil
import datetime
from openram import debug
from openram import sram_config as config
from openram import OPTS, print_time


class sram():
    """
    This is not a design module, but contains an SRAM design instance.
    It could later try options of number of banks and organization to compare
    results.
    We can later add visualizer and other high-level functions as needed.
    """
    def __init__(self, sram_config=None, name=None):

        # Create default configs if custom config isn't provided
        if sram_config is None:
            sram_config = config(word_size=OPTS.word_size,
                                 num_words=OPTS.num_words,
                                 write_size=OPTS.write_size,
                                 num_banks=OPTS.num_banks,
                                 words_per_row=OPTS.words_per_row,
                                 num_spare_rows=OPTS.num_spare_rows,
                                 num_spare_cols=OPTS.num_spare_cols)

        if name is None:
            name = OPTS.output_name

        sram_config.set_local_config(self)

        # reset the static duplicate name checker for unit tests
        # in case we create more than one SRAM
        from openram.base import design
        design.name_map=[]

        debug.info(2, "create sram of size {0} with {1} num of words {2} banks".format(self.word_size,
                                                                                       self.num_words,
                                                                                       self.num_banks))
        start_time = datetime.datetime.now()

        self.name = name

        from openram.modules.sram_1bank import sram_1bank as sram

        self.s = sram(name, sram_config)

        self.s.create_netlist()
        if not OPTS.netlist_only:
            self.s.create_layout()

        if not OPTS.is_unit_test:
            print_time("SRAM creation", datetime.datetime.now(), start_time)

    def get_sp_name(self):
        if OPTS.use_pex:
            # Use the extracted spice file
            return self.pex_name
        else:
            # Use generated spice file for characterization
            return self.sp_name

    def sp_write(self, name, lvs=False, trim=False):
        self.s.sp_write(name, lvs, trim)

    def lef_write(self, name):
        self.s.lef_write(name)

    def gds_write(self, name):
        self.s.gds_write(name)

    def verilog_write(self, name):
        self.s.verilog_write(name)
        if self.num_banks != 1:
            from openram.modules.sram_multibank import sram_multibank
            mb = sram_multibank(self.s)
            mb.verilog_write(name[:-2] + '_top.v')

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

        # Import this at the last minute so that the proper tech file
        # is loaded and the right tools are selected
        from openram import verify
        from openram.characterizer import functional
        from openram.characterizer import delay

        # Save the spice file
        start_time = datetime.datetime.now()
        spname = OPTS.output_path + self.s.name + ".sp"
        debug.print_raw("SP: Writing to {0}".format(spname))
        self.sp_write(spname)

        # Save a functional simulation file with default period
        functional(self.s,
                   spname,
                   cycles=200,
                   output_path=OPTS.output_path)
        print_time("Spice writing", datetime.datetime.now(), start_time)

        # Save stimulus and measurement file
        start_time = datetime.datetime.now()
        debug.print_raw("DELAY: Writing stimulus...")
        d = delay(self.s, spname, ("TT", 5, 25), output_path=OPTS.output_path)
        if (self.s.num_spare_rows == 0):
            probe_address = "1" * self.s.addr_size
        else:
            probe_address = "0" + "1" * (self.s.addr_size - 1)
        probe_data = self.s.word_size - 1
        d.analysis_init(probe_address, probe_data)
        d.targ_read_ports.extend(self.s.read_ports)
        d.targ_write_ports = [self.s.write_ports[0]]
        d.write_delay_stimulus()
        print_time("DELAY", datetime.datetime.now(), start_time)

        # Save trimmed spice file
        temp_trim_sp = "{0}trimmed.sp".format(OPTS.output_path)
        self.sp_write(temp_trim_sp, lvs=False, trim=True)

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

        # Characterize the design
        start_time = datetime.datetime.now()
        from openram.characterizer import lib
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
        from openram.datasheet import datasheet_gen
        dname = OPTS.output_path + self.s.name + ".html"
        debug.print_raw("Datasheet: Writing to {0}".format(dname))
        datasheet_gen.datasheet_write(dname)
        print_time("Datasheet", datetime.datetime.now(), start_time)

        # Write a verilog model
        start_time = datetime.datetime.now()
        vname = OPTS.output_path + self.s.name + '.v'
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
