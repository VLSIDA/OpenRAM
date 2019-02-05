#!/usr/bin/env python3
"""
Run a regression test on various srams
"""
import csv,sys,os
import pandas as pd
import matplotlib.pyplot as plt

import unittest
from testutils import header,openram_test
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug
from sram import sram
from sram_config import sram_config

MODEL_DIR = "model_data/"

class data_collection(openram_test):

    def runTest(self):
        ratio_data = self.calculate_delay_ratios_of_srams()
        self.display_data(ratio_data)
        # word_size, num_words, words_per_row = 4, 16, 1 
        # self.init_data_gen()
        # self.set_delay_chain(2,3)
        # self.save_data_sram_corners(word_size, num_words, words_per_row)
        # wl_dataframe, sae_dataframe = self.get_csv_data()
        # self.evaluate_data(wl_dataframe, sae_dataframe)
        
        #Run again but with different delay chain sizes
        # self.init_data_gen() 
        # self.set_delay_chain(4,2)
        # self.save_data_sram_corners(word_size, num_words, words_per_row)
        # wl_dataframe, sae_dataframe = self.get_csv_data()
        # self.evaluate_data(wl_dataframe, sae_dataframe)
        
        # model_delay_ratios, meas_delay_ratios, ratio_error = self.compare_model_to_measure()
        # debug.info(1, "model_delay_ratios={}".format(model_delay_ratios))
        # debug.info(1, "meas_delay_ratios={}".format(meas_delay_ratios))
        # debug.info(1, "ratio_error={}".format(ratio_error))
        # globals.end_openram()
    
    def calculate_delay_ratios_of_srams(self):
        """Runs delay measurements on several sram configurations.
        Computes the delay ratio for each one."""
        delay_ratio_data = {}
        config_tuple_list = [(32, 1024, None)]
        #config_tuple_list = [(1, 16, 1),(4, 16, 1), (16, 16, 1), (32, 32, 1)]
        for sram_config in config_tuple_list:
            word_size, num_words, words_per_row = sram_config
            self.init_data_gen()
            self.save_data_sram_corners(word_size, num_words, words_per_row)
            model_delay_ratios, meas_delay_ratios, ratio_error = self.compare_model_to_measure()
            delay_ratio_data[sram_config] = ratio_error
            debug.info(1, "Ratio percentage error={}".format(ratio_error))
        return delay_ratio_data
        
    def get_csv_data(self):
        """Hardcoded Hack to get the measurement data from the csv into lists. """
        wl_files_name = [file_name for file_name in self.file_names if "wl_measures" in file_name][0]
        sae_files_name = [file_name for file_name in self.file_names if "sae_measures" in file_name][0]
        wl_dataframe = pd.read_csv(wl_files_name,encoding='utf-8')
        sae_dataframe = pd.read_csv(sae_files_name,encoding='utf-8')
        return wl_dataframe,sae_dataframe 
        
    def evaluate_data(self, wl_dataframe, sae_dataframe):
        """Analyze the delay error and variation error"""
        delay_error = self.calculate_delay_error(wl_dataframe, sae_dataframe)
        debug.info(1, "Delay errors:{}".format(delay_error))
        variation_error = self.calculate_delay_variation_error(wl_dataframe, sae_dataframe)
        debug.info(1, "Variation errors:{}".format(variation_error))
    
    def compare_model_to_measure(self):
        """Uses the last 4 recent data sets (wl_meas, sen_meas, wl_model, sen_model)
           and compare the wl-sen delay ratio between model and measured.
        """
        model_delay_ratios = {}
        meas_delay_ratios = {}
        ratio_error = {}
        #The full file name contains unrelated portions, separate them into the four that are needed
        wl_meas_df = [pd.read_csv(file_name,encoding='utf-8') for file_name in self.file_names if "wl_measures" in file_name][0]
        sae_meas_df = [pd.read_csv(file_name,encoding='utf-8') for file_name in self.file_names if "sae_measures" in file_name][0]
        wl_model_df = [pd.read_csv(file_name,encoding='utf-8') for file_name in self.file_names if "wl_model" in file_name][0]
        sae_model_df = [pd.read_csv(file_name,encoding='utf-8') for file_name in self.file_names if "sae_model" in file_name][0]
        
        #Assume each csv has the same corners (and the same row order), use one of the dfs for corners
        proc_pos, volt_pos, temp_pos = wl_meas_df.columns.get_loc('process'), wl_meas_df.columns.get_loc('voltage'), wl_meas_df.columns.get_loc('temp')
        wl_sum_pos = wl_meas_df.columns.get_loc('sum')
        sae_sum_pos = sae_meas_df.columns.get_loc('sum')
        
        df_zip = zip(wl_meas_df.itertuples(),sae_meas_df.itertuples(),wl_model_df.itertuples(),sae_model_df.itertuples())
        for wl_meas,sae_meas,wl_model,sae_model in df_zip:
            #Use previously calculated position to index the df row. 
            corner = (wl_meas[proc_pos+1], wl_meas[volt_pos+1], wl_meas[temp_pos+1])
            meas_delay_ratios[corner] = wl_meas[wl_sum_pos+1]/sae_meas[sae_sum_pos+1]
            model_delay_ratios[corner] = wl_model[wl_sum_pos+1]/sae_model[sae_sum_pos+1]
            #Not using absolute error, positive error means model was larger, negative error means it was smaller.
            ratio_error[corner] = 100*(model_delay_ratios[corner]-meas_delay_ratios[corner])/meas_delay_ratios[corner]
            
        return model_delay_ratios, meas_delay_ratios, ratio_error 
     
    def display_data(self, data):
        """Displays the ratio data using matplotlib (requires graphics)"""
        config_data = []
        xticks = []
        #Organize data
        #First key level if the sram configuration (wordsize, num words, words per row)
        for config,corner_data_dict in data.items():
            #Second level is the corner data for that configuration.
            for corner, corner_data in corner_data_dict.items():
                #Right now I am only testing with a single corner, will not work with more than 1 corner
                config_data.append(corner_data)
            xticks.append("{}b,{}w,{}wpr".format(*config))
        #plot data
        data_range = [i+1 for i in range(len(data))]
        shapes = ['ro', 'bo', 'go', 'co', 'mo']
        plt.xticks(data_range, xticks)
        plt.plot(data_range, config_data, 'ro')
        plt.show()
        
    def calculate_delay_error(self, wl_dataframe, sae_dataframe):
        """Calculates the percentage difference in delays between the wordline and sense amp enable"""
        start_data_pos = len(self.config_fields) #items before this point are configuration related
        error_list = []
        row_count = 0
        for wl_row, sae_row in zip(wl_dataframe.itertuples(), sae_dataframe.itertuples()):             
            debug.info(2, "wl_row:{}".format(wl_row))
            wl_sum = sum(wl_row[start_data_pos+1:])
            debug.info(2, "wl_sum:{}".format(wl_sum))
            sae_sum = sum(sae_row[start_data_pos+1:])
            error_list.append(abs((wl_sum-sae_sum)/wl_sum))
        return error_list
        
    def calculate_delay_variation_error(self, wl_dataframe, sae_dataframe):
        """Measures a base delay from the first corner then the variations from that base"""
        start_data_pos = len(self.config_fields)
        variation_error_list = []
        count = 0
        for wl_row, sae_row in zip(wl_dataframe.itertuples(), sae_dataframe.itertuples()):
            if count == 0:
                #Create a base delay, variation is defined as the difference between this base
                wl_base = sum(wl_row[start_data_pos+1:])
                debug.info(1, "wl_sum base:{}".format(wl_base))
                sae_base = sum(sae_row[start_data_pos+1:])
                variation_error_list.append(0.0)
            else:
                #Calculate the variation from the respective base and then difference between the variations
                wl_sum = sum(wl_row[start_data_pos+1:])
                wl_base_diff = abs((wl_base-wl_sum)/wl_base)
                sae_sum = sum(sae_row[start_data_pos+1:])
                sae_base_diff = abs((sae_base-sae_sum)/sae_base)
                variation_diff = abs((wl_base_diff-sae_base_diff)/wl_base_diff)
                variation_error_list.append(variation_diff)
            count+=1
        return variation_error_list
        
    def save_data_sram_corners(self, word_size, num_words, words_per_row):
        """Performs corner analysis on a single SRAM configuration"""
        self.create_sram(word_size, num_words, words_per_row)
        #Setting to none forces SRAM to determine the value. Must be checked after sram creation
        if not words_per_row: 
            words_per_row = self.sram.s.words_per_row
        #Run on one size to initialize CSV writing (csv names come from return value). Strange, but it is okay for now.
        corner_gen = self.corner_combination_generator()
        init_corner = next(corner_gen)
        sram_data = self.get_sram_data(init_corner)
        dc_resized = self.was_delay_chain_resized()
        self.initialize_csv_file(word_size, num_words, words_per_row)
        self.add_sram_data_to_csv(sram_data, word_size, num_words, words_per_row, dc_resized, init_corner) 
        
        #Run openRAM for all corners
        for corner in corner_gen:
            sram_data = self.get_sram_data(corner)
            self.add_sram_data_to_csv(sram_data, word_size, num_words, words_per_row, dc_resized, corner)
            
        self.close_files()
        debug.info(1,"Data Generated")
        
    def init_data_gen(self):
        """Initialization for the data test to run"""
        globals.init_openram("config_data")
        from tech import parameter
        global parameter
        if OPTS.tech_name == "scmos":
            debug.warning("Device models not up to date with scn4m technology.")
        OPTS.spice_name="hspice" #Much faster than ngspice.
        OPTS.trim_netlist = False
        OPTS.netlist_only = True
        OPTS.analytical_delay = False
        #OPTS.use_tech_delay_chain_size = True
        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        import characterizer
        reload(characterizer) 

    def set_delay_chain(self, stages, fanout):
        """Force change the parameter in the tech file to specify a delay chain configuration"""
        parameter["static_delay_stages"] = stages
        parameter["static_fanout_per_stage"] = fanout
        
    def close_files(self):
        """Closes all files stored in the file dict"""
        for key,file in self.csv_files.items():
            file.close()
   
    def corner_combination_generator(self):
        processes = OPTS.process_corners
        voltages = OPTS.supply_voltages
        temperatures = OPTS.temperatures
        """Generates corner using a combination of values from config file"""
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
    
    def add_sram_data_to_csv(self, sram_data, word_size, num_words, words_per_row, dc_resized, corner):
        """Writes data to its respective CSV file. There is a CSV for each measurement target 
        (wordline, sense amp enable, and models)"""
        sram_specs = [word_size,num_words,words_per_row,dc_resized,*corner]
        for data_name, data_values in sram_data.items():
            other_values = self.calculate_other_data_values(data_values)
            self.csv_writers[data_name].writerow(sram_specs+sram_data[data_name]+other_values)
        debug.info(2,"Data Added to CSV file.")
    
    def calculate_other_data_values(self, sram_data_list):
        """A function to calculate extra values related to the data. Only does the sum for now"""
        data_sum = sum(sram_data_list)
        return [data_sum]
    
    def initialize_csv_file(self, word_size, num_words, words_per_row):
        """Opens a CSV file and writer for every data set being written (wl/sae measurements and model values)"""
        #CSV File writing
        header_dict = self.delay_obj.get_all_signal_names()
        self.csv_files = {}
        self.csv_writers = {}
        self.file_names = []
        delay_stages = self.delay_obj.get_num_delay_stages()
        delay_stage_fanout = self.delay_obj.get_num_delay_stage_fanout()
        
        for data_name, header_list in header_dict.items():
            file_name = '{}data_{}b_{}word_{}way_dc{}x{}_{}.csv'.format(MODEL_DIR,
                                                                word_size, 
                                                                num_words, 
                                                                words_per_row,
                                                                delay_stages,
                                                                delay_stage_fanout,
                                                                data_name)
            self.file_names.append(file_name)
            self.csv_files[data_name] = open(file_name, 'w')
            self.config_fields = ['word_size', 'num_words', 'words_per_row', 'dc_resized', 'process', 'voltage', 'temp']
            self.other_data_fields = ['sum']
            fields = (*self.config_fields, *header_list, *self.other_data_fields)
            self.csv_writers[data_name] = csv.writer(self.csv_files[data_name], lineterminator = '\n')
            self.csv_writers[data_name].writerow(fields)
    
    def create_sram(self, word_size, num_words, words_per_row):
        """Generates the SRAM based on input configuration."""
        c = sram_config(word_size=word_size,
                        num_words=num_words,
                        num_banks=1,
                        words_per_row=words_per_row)
            
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
                    
    def was_delay_chain_resized(self):
        """Accesses the dc resize boolean in the control logic module."""
        #FIXME:assumes read/write port only
        return self.sram.s.control_logic_rw.delay_chain_resized
                
# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
