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
from characterizer import functional, delay
from base import timing_graph
from globals import OPTS, print_time
import shutil


class sram():
    """
    This is not a design module, but contains an SRAM design instance.
    It could later try options of number of banks and oganization to compare
    results.
    We can later add visualizer and other high-level functions as needed.
    """
    def __init__(self, name, sram_config):

        self.name = name
        self.config = sram_config
        sram_config.setup_multiport_constants()
        sram_config.set_local_config(self)

        self.sp_name = OPTS.output_path + self.name + ".sp"
        self.lvs_name = OPTS.output_path + self.name + ".lvs.sp"
        self.pex_name = OPTS.output_path + self.name + ".pex.sp"
        self.gds_name = OPTS.output_path + self.name + ".gds"
        self.lef_name = OPTS.output_path + self.name + ".lef"
        self.v_name = OPTS.output_path + self.name + ".v"

        # reset the static duplicate name checker for unit tests
        # in case we create more than one SRAM
        from base import design
        design.name_map=[]

        self.create()

    def create(self):
        debug.info(2, "create sram of size {0} with {1} num of words {2} banks".format(self.word_size,
                                                                                       self.num_words,
                                                                                       self.num_banks))
        start_time = datetime.datetime.now()

        from .sram_1bank import sram_1bank as sram

        self.s = sram(self.name, self.config)

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
            from .sram_multibank import sram_multibank
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
        import verify

        # Save the spice file
        start_time = datetime.datetime.now()
        debug.print_raw("SP: Writing to {0}".format(self.sp_name))
        self.sp_write(self.sp_name)

        # Save a functional simulation file with default period
        functional(self.s,
                   os.path.basename(self.sp_name),
                   cycles=200,
                   output_path=OPTS.output_path)
        print_time("Spice writing", datetime.datetime.now(), start_time)

        # Save stimulus and measurement file
        start_time = datetime.datetime.now()
        debug.print_raw("DELAY: Writing stimulus...")
        d = delay(self.s, self.get_sp_name(), ("TT", 5, 25), output_path=OPTS.output_path)
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
            debug.print_raw("GDS: Writing to {0}".format(self.gds_name))
            self.gds_write(self.gds_name)
            if OPTS.check_lvsdrc:
                verify.write_drc_script(cell_name=self.s.name,
                                        gds_name=os.path.basename(self.gds_name),
                                        extract=True,
                                        final_verification=True,
                                        output_path=OPTS.output_path)
            print_time("GDS", datetime.datetime.now(), start_time)

            # Create a LEF physical model
            start_time = datetime.datetime.now()
            debug.print_raw("LEF: Writing to {0}".format(self.lef_name))
            self.lef_write(self.lef_name)
            print_time("LEF", datetime.datetime.now(), start_time)

        # Save the LVS file
        start_time = datetime.datetime.now()
        debug.print_raw("LVS: Writing to {0}".format(self.lvs_name))
        self.sp_write(self.lvs_name, lvs=True)
        if not OPTS.netlist_only and OPTS.check_lvsdrc:
            verify.write_lvs_script(cell_name=self.s.name,
                                    gds_name=os.path.basename(self.gds_name),
                                    sp_name=os.path.basename(self.lvs_name),
                                    final_verification=True,
                                    output_path=OPTS.output_path)
        print_time("LVS writing", datetime.datetime.now(), start_time)

        # Save the extracted spice file
        if OPTS.use_pex:
            start_time = datetime.datetime.now()
            # Output the extracted design if requested
            verify.run_pex(self.s.name, self.gds_name, self.sp_name, output=self.pex_name)
            print_time("Extraction", datetime.datetime.now(), start_time)

        # Characterize the design
        start_time = datetime.datetime.now()
        from characterizer import delay
        debug.print_raw("LIB: Writing Analysis File... ")
        d = delay(self, self.get_sp_name(), ("TT", 5, 25))
        if (self.sram.num_spare_rows == 0):
            probe_address = "1" * self.sram.addr_size
        else:
            probe_address = "0" + "1" * (self.sram.addr_size - 1)
        d.analysis_init(probe_address, probe_data)
        print_time("Characterization", datetime.datetime.now(), start_time)

        # Write the config file
        start_time = datetime.datetime.now()
        from shutil import copyfile
        copyfile(OPTS.config_file, OPTS.output_path + OPTS.output_name + '.py')
        debug.print_raw("Config: Writing to {0}".format(OPTS.output_path + OPTS.output_name + '.py'))
        print_time("Config", datetime.datetime.now(), start_time)

        # Write the datasheet
        start_time = datetime.datetime.now()
        from datasheet import datasheet_gen
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
