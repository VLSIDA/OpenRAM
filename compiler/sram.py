import sys
import datetime
import getpass
import debug
from globals import OPTS, print_time

    
class sram():
    """
    This is not a design module, but contains an SRAM design instance.
    It could later try options of number of banks and oganization to compare
    results.
    We can later add visualizer and other high-level functions as needed.
    """
    def __init__(self, word_size, num_words, num_banks, name):

        # reset the static duplicate name checker for unit tests
        # in case we create more than one SRAM
        from design import design
        design.name_map=[]

        debug.info(2, "create sram of size {0} with {1} num of words".format(word_size, 
                                                                             num_words))
        start_time = datetime.datetime.now()

        if num_banks == 1:
            from sram_1bank import sram_1bank
            sram=sram_1bank(word_size, num_words, name)
        elif num_banks == 2:
            from sram_2bank import sram_2bank
            sram=sram_2bank(word_size, num_words, name)            
        elif num_banks == 4:
            from sram_4bank import sram_4bank
            sram=sram_4bank(word_size, num_words, name)                        
        else:
            debug.error("Invalid number of banks.",-1)

        sram.compute_sizes()
        sram.create_modules()
        sram.add_pins()
        sram.create_layout()
        
        # Can remove the following, but it helps for debug!
        sram.add_lvs_correspondence_points()
        
        sram.offset_all_coordinates()
        (sram.width, sram.height) = sram.find_highest_coords()
        
        sram.DRC_LVS(final_verification=True)

        if not OPTS.is_unit_test:
            print_time("SRAM creation", datetime.datetime.now(), start_time)

        self.save()

    def save(self):
        """ Save all the output files while reporting time to do it as well. """

        # Save the spice file
        start_time = datetime.datetime.now()
        spname = OPTS.output_path + sram.name + ".sp"
        print("SP: Writing to {0}".format(spname))
        sram.sp_write(spname)
        print_time("Spice writing", datetime.datetime.now(), start_time)

        # Save the extracted spice file
        if OPTS.use_pex:
            start_time = datetime.datetime.now()
            # Output the extracted design if requested
            sp_file = OPTS.output_path + "temp_pex.sp"
            verify.run_pex(sram.name, gdsname, spname, output=sp_file)
            print_time("Extraction", datetime.datetime.now(), start_time)
        else:
            # Use generated spice file for characterization
            sp_file = spname
        print(sys.path)
        # Characterize the design
        start_time = datetime.datetime.now()
        from characterizer import lib
        print("LIB: Characterizing... ")
        if OPTS.analytical_delay:
            print("Using analytical delay models (no characterization)")
        else:
            if OPTS.spice_name!="":
                print("Performing simulation-based characterization with {}".format(OPTS.spice_name))
            if OPTS.trim_netlist:
                print("Trimming netlist to speed up characterization.")
        lib(out_dir=OPTS.output_path, sram=self, sp_file=sp_file)
        print_time("Characterization", datetime.datetime.now(), start_time)

        # Write the layout
        start_time = datetime.datetime.now()
        gdsname = OPTS.output_path + sram.name + ".gds"
        print("GDS: Writing to {0}".format(gdsname))
        sram.gds_write(gdsname)
        print_time("GDS", datetime.datetime.now(), start_time)

        # Create a LEF physical model
        start_time = datetime.datetime.now()
        lefname = OPTS.output_path + sram.name + ".lef"
        print("LEF: Writing to {0}".format(lefname))
        sram.lef_write(lefname)
        print_time("LEF", datetime.datetime.now(), start_time)

        # Write a verilog model
        start_time = datetime.datetime.now()
        vname = OPTS.output_path + sram.name + ".v"
        print("Verilog: Writing to {0}".format(vname))
        sram.verilog_write(vname)
        print_time("Verilog", datetime.datetime.now(), start_time)
