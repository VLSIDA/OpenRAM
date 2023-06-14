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
from openram import rom_config as config
from openram import OPTS, print_time


class rom():
    """
    This is not a design module, but contains an ROM design instance.
    """
    def __init__(self, rom_config=None, name=None):

        # Create default configs if custom config isn't provided
        if rom_config is None:
            rom_config = config(rom_data=OPTS.rom_data,
                                word_size=OPTS.word_size,
                                words_per_row=OPTS.words_per_row,
                                rom_endian=OPTS.rom_endian,
                                scramble_bits=OPTS.scramble_bits,
                                strap_spacing=OPTS.strap_spacing,
                                data_type=OPTS.data_type)

        if name is None:
            name = OPTS.output_name

        rom_config.set_local_config(self)

        # reset the static duplicate name checker for unit tests
        # in case we create more than one ROM
        from openram.base import design
        design.name_map=[]

        debug.print_raw("create rom of word size {0} with {1} num of words".format(self.word_size,
                                                                                       self.num_words))
        start_time = datetime.datetime.now()

        self.name = name

        import openram.modules.rom_bank as rom

        self.r = rom(name, rom_config)

        self.r.create_netlist()
        if not OPTS.netlist_only:
            self.r.create_layout()

        if not OPTS.is_unit_test:
            print_time("ROM creation", datetime.datetime.now(), start_time)

    def sp_write(self, name, lvs=False, trim=False):
        self.r.sp_write(name, lvs, trim)

    def gds_write(self, name):
        self.r.gds_write(name)

    def verilog_write(self, name):
        self.r.verilog_write(name)

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

        # Save the spice file
        start_time = datetime.datetime.now()
        spname = OPTS.output_path + self.r.name + ".sp"
        debug.print_raw("SP: Writing to {0}".format(spname))
        self.sp_write(spname)

        print_time("Spice writing", datetime.datetime.now(), start_time)

        if not OPTS.netlist_only:
            # Write the layout
            start_time = datetime.datetime.now()
            gdsname = OPTS.output_path + self.r.name + ".gds"
            debug.print_raw("GDS: Writing to {0}".format(gdsname))
            self.gds_write(gdsname)
            if OPTS.check_lvsdrc:
                verify.write_drc_script(cell_name=self.r.name,
                                        gds_name=os.path.basename(gdsname),
                                        extract=True,
                                        final_verification=True,
                                        output_path=OPTS.output_path)
            print_time("GDS", datetime.datetime.now(), start_time)

        # Save the LVS file
        start_time = datetime.datetime.now()
        lvsname = OPTS.output_path + self.r.name + ".lvs.sp"
        debug.print_raw("LVS: Writing to {0}".format(lvsname))
        self.sp_write(lvsname, lvs=True)
        if not OPTS.netlist_only and OPTS.check_lvsdrc:
            verify.write_lvs_script(cell_name=self.r.name,
                                    gds_name=os.path.basename(gdsname),
                                    sp_name=os.path.basename(lvsname),
                                    final_verification=True,
                                    output_path=OPTS.output_path)
        print_time("LVS writing", datetime.datetime.now(), start_time)

        # Save the extracted spice file
        if OPTS.use_pex:
            start_time = datetime.datetime.now()
            # Output the extracted design if requested
            pexname = OPTS.output_path + self.r.name + ".pex.sp"
            spname = OPTS.output_path + self.r.name + ".sp"
            verify.run_pex(self.r.name, gdsname, spname, output=pexname)
            sp_file = pexname
            print_time("Extraction", datetime.datetime.now(), start_time)
        else:
            # Use generated spice file for characterization
            sp_file = spname

        # Save a functional simulation file

        # TODO: Characterize the design


        # Write the config file
        # Should also save the provided data file
        start_time = datetime.datetime.now()
        from shutil import copyfile
        copyfile(OPTS.config_file, OPTS.output_path + OPTS.output_name + '.py')
        copyfile(self.rom_data, OPTS.output_path + self.rom_data)
        debug.print_raw("Config: Writing to {0}".format(OPTS.output_path + OPTS.output_name + '.py'))
        print_time("Config", datetime.datetime.now(), start_time)

        # TODO: Write the datasheet

        #Write a verilog model
        start_time = datetime.datetime.now()
        vname = OPTS.output_path + self.r.name + '.v'
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
