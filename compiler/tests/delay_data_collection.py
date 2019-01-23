#!/usr/bin/env python3
"""
Run a regression test on various srams
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug
import csv
from sram import sram
from sram_config import sram_config

MODEL_DIR = "model_data/"

class data_collection(openram_test):

    def runTest(self):
        self.init_data_gen()
     
        word_size, num_words, words_per_row = 4, 16, 1 
        self.evalulate_sram_on_corners(word_size, num_words, words_per_row)
        globals.end_openram()
    
    def evalulate_sram_on_corners(self, word_size, num_words, words_per_row):
        """Performs corner analysis on a single SRAM configuration"""
        self.create_sram(word_size, num_words, words_per_row)
        #Run on one size to initialize CSV writing (csv names come from return value). Strange, but it is okay for now.
        corner_gen = self.corner_combination_generator()
        init_corner = next(corner_gen)
        sram_data = self.get_sram_data(init_corner)
        self.initialize_csv_file(sram_data, word_size, num_words, words_per_row)
        self.add_sram_data_to_csv(sram_data, word_size, num_words, words_per_row, init_corner) 
        
        #Run openRAM for all corners
        for corner in corner_gen:
            sram_data = self.get_sram_data(corner)
            self.add_sram_data_to_csv(sram_data, word_size, num_words, words_per_row, corner)
            
        self.close_files()
        debug.info(1,"Data Generated")
        
    def init_data_gen(self):
        """Initialization for the data test to run"""
        globals.init_openram("config_data")
        if OPTS.tech_name == "scmos":
            debug.warning("Device models not up to date with scn4m technology.")
        OPTS.spice_name="hspice" #Much faster than ngspice.
        OPTS.trim_netlist = False
        OPTS.netlist_only = True
        OPTS.analytical_delay = False
        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        import characterizer
        reload(characterizer) 

    def close_files(self):
        """Closes all files stored in the file dict"""
        for key,file in self.csv_files.items():
            file.close()
   
    def corner_combination_generator(self):
        """Generates corner using a combination of values from config file"""
        processes = OPTS.process_corners
        voltages = OPTS.supply_voltages
        temperatures = OPTS.temperatures
        for proc in processes:
            for volt in voltages:
                for temp in temperatures:
                    yield (proc, volt, temp)
        
        
    def get_sram_configs(self):
        """Generate lists of wordsizes, number of words, and column mux size (words per row) to be tested."""
        min_word_size = 1
        max_word_size = 16
        min_num_words_log2 = 4
        max_num_words_log2 = 8
        word_sizes = [i for i in range(min_word_size,max_word_size+1)]
        num_words = [2**i for i in range(min_num_words_log2,max_num_words_log2+1)]
        words_per_row = [1]
        return word_sizes, num_words, words_per_row
    
    def add_sram_data_to_csv(self, sram_data, word_size, num_words, words_per_row, corner):
        """Writes data to its respective CSV file. There is a CSV for each measurement target (wordline, sense amp enable, and models)"""
        sram_specs = [word_size,num_words,words_per_row,*corner]
        for data_name, data_values in sram_data.items():
            self.csv_writers[data_name].writerow(sram_specs+sram_data[data_name])
        debug.info(2,"Data Added to CSV file.")
    
    def initialize_csv_file(self, sram_data, word_size, num_words, words_per_row):
        """Opens a CSV file and writer for every data set being written (wl/sae measurements and model values)"""
        #CSV File writing
        header_dict = self.delay_obj.get_all_signal_names()
        self.csv_files = {}
        self.csv_writers = {}
        for data_name, header_list in header_dict.items():
            file_name = '{}data_{}b_{}word_{}way_{}.csv'.format(MODEL_DIR,
                                                                word_size, 
                                                                num_words, 
                                                                words_per_row, 
                                                                data_name)
            self.csv_files[data_name] = open(file_name, 'w')
            fields = ('word_size', 'num_words', 'words_per_row', 'process', 'voltage', 'temp', *header_list)
            self.csv_writers[data_name] = csv.writer(self.csv_files[data_name], lineterminator = '\n')
            self.csv_writers[data_name].writerow(fields)
    
    def create_sram(self, word_size, num_words, words_per_row):
        """Generates the SRAM based on input configuration."""
        c = sram_config(word_size=word_size,
                        num_words=num_words,
                        num_banks=1)
        #minimum 16 rows. Most sizes below 16*16 will try to automatically use less rows unless enforced.
        #if word_size*num_words < 256:
        c.words_per_row=words_per_row #Force no column mux until incorporated into analytical delay.
            
        debug.info(1, "Creating SRAM: {} bit, {} words, with 1 bank".format(word_size, num_words))
        self.sram = sram(c, name="sram_{}ws_{}words".format(word_size, num_words))

        self.sram_spice = OPTS.openram_temp + "temp.sp"
        self.sram.sp_write(self.sram_spice)
        
    def get_sram_data(self, corner):
        """Generates the delay object using the corner and runs a simulation for data."""
        from characterizer import model_check
        self.delay_obj = model_check(self.sram.s, self.sram_spice, corner)
        
        import tech
        #Only 1 at a time
        probe_address = "1" * self.sram.s.addr_size
        probe_data = self.sram.s.word_size - 1
        loads = [tech.spice["msflop_in_cap"]*4]
        slews = [tech.spice["rise_time"]*2]

        sram_data = self.delay_obj.analyze(probe_address,probe_data,slews,loads)
        return sram_data
       
    def remove_lists_from_dict(self, dict):
        """Check all the values in the dict and replaces the list items with its first value."""
       #This is useful because the tests performed here only generate 1 value but a list
       #with 1 item makes writing it to a csv later harder.
        for key in dict.keys():
            if type(dict[key]) is list:
                if len(dict[key]) > 0:
                    dict[key] = dict[key][0]
                else:
                    del dict[key]
                
# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
