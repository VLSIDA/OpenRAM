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
DATASET_CSV_NAME = MODEL_DIR+'datasets.csv'

# Data Collection class
# This module can perform two tasks
#  1) Collect data
#  2) Display data
# Data Collection - 
# A single SRAM simulation will collect 6 datasets: wordline (WL) delays, sense amp enable (SAE) delays,
# WL slews, SAE slews, WL model delays, SAE model delays.
# Each dataset is stored in a separate csv file. Each row of the CSV refers to a different corner simulated on.
# The files names are stored in DATASET_CSV_NAME marked above.
# There are 2 main ways the collection is targeted: looking at different delay chain sizes and looking at different SRAM configurations.
# These are separated by different functions and should not be collected together.
#
# Data display - 
# There are many functions in this file which will search (or told) for data using DATASET_CSV_NAME as a guide.
# Delay chain data is analyzed in analyze_delay_chain_data, graph_delays_and_inp_slews, and graph_inp_slews_and_delay_var
# WL and SAE graphing is done in analyze_sae_data and graph_delays_and_var
#
# Data collection and each analysis can be run independently, but the one you want needs to be commented in/out.

class data_collection(openram_test):

    def runTest(self):
    
        #Uncomment this for model evaluation
        # ratio_data = self.calculate_delay_ratios_of_srams()
        # self.display_data(ratio_data)
        
        self.run_setup()
        
        self.run_delay_chain_analysis()
        #self.run_sae_analysis()
        globals.end_openram()
    
    def run_setup(self):
        """Checks file existence and sets some member variables"""
        if not os.path.isdir(MODEL_DIR):
            os.mkdir(MODEL_DIR)
        
        #File requires names from the delay measurement object.
        #Initialization is delayed until one configuration simulation has occurred.
        self.dataset_initialized=False
        
        #These help mark positions in the csv file for data collection and analysis
        self.config_fields = ['word_size', 'num_words', 'words_per_row', 'dc_resized', 'process', 'voltage', 'temp']
        self.sae_config_fields = ['dc_start_ind', 'dc_end_ind']
        self.other_data_fields = ['sum']

    
    def init_dataset_csv(self, file_fields):
        """Creates csv which holds files names of all available datasets."""
        debug.info(2,'Initializing dataset file and dataframe.')
        self.dataset_file_fields = file_fields 
        self.dataset_file_fields.sort()
        config_fields = ['word_size', 'num_words', 'words_per_row', 'dc_config']
        self.dataset_fields = config_fields+self.dataset_file_fields
        
        if not os.path.exists(DATASET_CSV_NAME):
            debug.info(2,'No dataset file found. Creating dataset file.')
            dataset_csv = open(DATASET_CSV_NAME, 'w')
            csv_writer = csv.writer(dataset_csv, lineterminator = '\n')
            csv_writer.writerow(self.dataset_fields)
            dataset_csv.close()
            self.dataset_initialized=True
        self.datasets_df = pd.read_csv(DATASET_CSV_NAME, encoding='utf-8')
        
    def add_dataset(self, word_size, num_words, words_per_row):
        """Added filenames to DATASET_CSV_NAME"""
        cur_len = len(self.datasets_df)
        #list converted to str as lists as saved as str in the csv file.
        #e.g. list=[2,2] -> csv entry = '[2,2]'
        fanout_str = str(self.delay_obj.get_num_delay_fanout_list())
        file_names = [self.file_name_dict[fname] for fname in self.dataset_file_fields]
        new_df_row = [word_size, num_words, words_per_row,fanout_str]+file_names
        
        df_bool = (self.datasets_df['word_size'] == word_size) & (self.datasets_df['num_words'] == num_words) & (self.datasets_df['words_per_row'] == words_per_row) & (self.datasets_df['dc_config'] == fanout_str)
        if len(self.datasets_df.loc[df_bool]) == 0:
            self.datasets_df = self.datasets_df.append(pd.Series(new_df_row, self.dataset_fields), ignore_index=True)
        else:    
            self.datasets_df.loc[df_bool] = [new_df_row]
                           
    
    def get_filename_by_config(self, data_types, word_size, num_words, words_per_row, fanout_list):
        """Searches the dataset csv for a config match. Extracts the filenames for the desired data."""
        start_fname_ind = 4 # four query items
        
        fanout_str = str(fanout_list)
        datasets_df = pd.read_csv(DATASET_CSV_NAME, encoding='utf-8')
        df_bool = (datasets_df['word_size'] == word_size) & (datasets_df['num_words'] == num_words) & (datasets_df['words_per_row'] == words_per_row) & (datasets_df['dc_config'] == fanout_str)
        df_filtered = datasets_df.loc[df_bool]
        if len(df_filtered) > 1:    
            debug.info(1,"Found more than 1 dataset entry with the same configuration. Using the first found")
        elif len(df_filtered) == 0:
            debug.error("Dataset for configuration not found:\n \
            word_size={}, num_words={}, words_per_row={}, fanout_list={}".format(word_size,
                                                                                 num_words,
                                                                                 words_per_row,
                                                                                 fanout_list), 1)
        df_row = df_filtered.iloc[0]    
        #Check csv header against expected    
        csv_data_types = list(df_filtered)[start_fname_ind:]
        if not set(data_types).issubset(set(csv_data_types)):
            debug.error("Dataset csv header does not match expected:\nExpected={}\nCSV={}".format(data_types,
                                                                                                  csv_data_types),1)
        
        return [df_row[dt] for dt in data_types]
    
    def get_all_filenames(self, data_types):
        """Gets all files from dataset.csv specified by the datatype (model/measure)"""
        start_fname_ind = 4 # four query items
       
        datasets_df = pd.read_csv(DATASET_CSV_NAME, encoding='utf-8')
        csv_data_types = list(datasets_df)[start_fname_ind:]
        if not set(data_types).issubset(set(csv_data_types)):
            debug.error("Dataset csv header does not match expected:\nExpected={}\nCSV={}".format(data_types,
                                                                                                  csv_data_types),1)

        return [list(datasets_df[dt]) for dt in data_types]
    
    def run_sae_analysis(self):
        """Generates sram with different delay chain configs over different corners and 
           analyzes delay average and variation."""
        #config_tuple_list = [(8, 16, 1),(8, 32, 1),(16, 32, 1), (32, 64, 1), (64, 32, 1), (64, 64, 1), (32, 128, 1)]   
        #config_tuple_list = [(1, 16, 1),(4, 16, 1),(16, 16, 1), (32, 32, 1)]
        config_tuple_list = [(1, 16, 1),(4, 16, 1)]
        self.save_sram_data_using_configs(config_tuple_list)
        self.analyze_sae_data() #Uses all available data
        #self.graph_delays_and_var('sae_measures')
        #self.graph_delays_and_var('wl_measures')
        #self.compare_wl_sae_data()
    
    def save_sram_data_using_configs(self, config_list):
        """Get SRAM data for different configurations"""
        for config in config_list:
            word_size, num_words, words_per_row = config
            self.init_data_gen()
            self.save_data_sram_corners(word_size, num_words, words_per_row)
    
    def analyze_sae_data(self):
        """Compare and graph delay chain variations over different configurations."""
        delay_avgs_ratio = []
        delay_vars_ratio = []
        sram_configs = []
        data_types = ["sae_measures"]
        sae_filenames = self.get_all_filenames(data_types)[0]
        sae_dataframes = self.get_csv_data(sae_filenames)
        
        for df in sae_dataframes:
            #Each row in df contains sram config. Only use the first one (they should all be the same)
            config = df[['word_size', 'num_words', 'words_per_row']].values.tolist()[0]
            sram_configs.append(config)
            delay_sums = self.get_sum(df)
            delay_chain_sums = self.get_delay_chain_sums(df)
            delay_avgs_ratio.append(self.get_average(delay_chain_sums)/self.get_average(delay_sums))
            delay_vars_ratio.append(self.get_variance(delay_chain_sums)/self.get_variance(delay_sums))
            debug.info(1,"DC config={}: avg ratio={} var ratio={}".format(sram_configs[-1], 
                                                                          delay_avgs_ratio[-1], 
                                                                          delay_vars_ratio[-1]))
            
        #Sort by the delays then graph
        all_data = zip(delay_avgs_ratio,sram_configs,delay_vars_ratio)
        delay_avgs_ratio,sram_configs,delay_vars_ratio = zip(*sorted(all_data))
        x_ax_label = '[word_size, num_words, words_per_row]'
        y_ax_labels = ['DC/SAE Delay Ratio', 'DC/SAE Var. Ratio']
        self.plot_delay_variance_data_sets(sram_configs, x_ax_label, y_ax_labels, delay_avgs_ratio, delay_vars_ratio)
    
    def compare_wl_sae_data(self):
        """Compare and graph delay chain variations over different configurations."""
        delay_avgs_ratio = []
        delay_vars_ratio = []
        sram_configs = []
        data_types = ["wl_measures","sae_measures"]
        data_filenames = self.get_all_filenames(data_types)
        wl_filenames = data_filenames[0]
        wl_dataframes = self.get_csv_data(wl_filenames)
        sae_filenames = data_filenames[1]
        sae_dataframes = self.get_csv_data(sae_filenames)
        
        #Loop through all configurations found
        for wl_df,sae_df in zip(wl_dataframes,sae_dataframes):
            #Each row in df contains sram config. Only use the first one (they should all be the same)
            config = wl_df[['word_size', 'num_words', 'words_per_row']].values.tolist()[0]
            sram_configs.append(config)
            wl_delays = self.get_sum(wl_df)
            sae_delays = self.get_sum(sae_df)
            delay_avgs_ratio.append(self.get_average(wl_delays)/self.get_average(sae_delays))
            delay_vars_ratio.append(self.get_variance(wl_delays)/self.get_variance(sae_delays))
            debug.info(1,"DC config={}: avg ratio={} var ratio={}".format(sram_configs[-1], 
                                                                          delay_avgs_ratio[-1], 
                                                                          delay_vars_ratio[-1]))
            
        #Sort by the delays then graph
        all_data = zip(delay_avgs_ratio,sram_configs,delay_vars_ratio)
        delay_avgs_ratio,sram_configs,delay_vars_ratio = zip(*sorted(all_data))
        x_ax_label = 'SRAM Config'
        y_ax_labels = ['WL/SAE Delay Ratio', 'WL/SAE Var. Ratio']
        self.plot_delay_variance_data_sets(sram_configs, x_ax_label, y_ax_labels, delay_avgs_ratio, delay_vars_ratio)
    
    def graph_delays_and_var(self, data_type):
        delay_avgs = []
        delay_vars = []
        sram_configs = []
        data_filenames = self.get_all_filenames([data_type])[0]
        dataframes = self.get_csv_data(data_filenames)
        
        #Loop through all configurations found
        for df in dataframes:
            #Each row in df contains sram config. Only use the first one (they should all be the same)
            config = df[['word_size', 'num_words', 'words_per_row']].values.tolist()[0]
            sram_configs.append(config)
            delays = self.get_sum(df)
            delay_avgs.append(self.get_average(delays))
            delay_vars.append(self.get_variance(delays))
            debug.info(1,"DC config={}: avg={}, var={}".format(sram_configs[-1], 
                                                               delay_avgs[-1], 
                                                               delay_vars[-1]))
            
        #Sort by the delays then graph
        all_data = zip(delay_avgs,sram_configs,delay_vars)
        delay_avgs,sram_configs,delay_vars = zip(*sorted(all_data))
        x_ax_label = 'SRAM Config'
        y_ax_labels = ['Avg. Delay', 'Delay Variance']
        self.plot_delay_variance_data_sets(sram_configs, x_ax_label, y_ax_labels, delay_avgs, delay_vars)
        
    def run_delay_chain_analysis(self):
        """Generates sram with different delay chain configs over different corners and 
           analyzes delay average and variation."""
        OPTS.use_tech_delay_chain_size = True
        #Constant sram config for this test   
        word_size, num_words, words_per_row = 1, 16, 1
        #Only change delay chain
        #dc_config_list = [(2,3), (3,3), (3,4), (4,2), (4,3), (4,4), (2,4), (2,5)]
        #dc_config_list = [(2,3), (3,3)]
        
        #fanout_configs = [[3,3], [3,3,3]]
        old_fanout_configs = []
        fanout_configs = [[3,3], [2,3,2,3], [2,4,2,4], [2,2,2,2], [3,3,3,3], [4,4],[4,4,4,4], [5,5], \
                              [2,2], [2,5,2,5], [2,6,2,6], [2,8,2,8], [3,5,3,5], [4,5,4,5], [2,2,2,2,2,2], [3,3,3,3,3,3],\
                              [6,6],[7,7],[8,8],[9,9],[10,10],[11,11],
                              [5,2,5,2], [6,2,6,2], [8,2,8,2], [5,3,5,3], [5,4,5,4], [2,3,4,5], [7,2,7,2]]
        analysis_configs = fanout_configs+old_fanout_configs
        #self.save_delay_chain_data(word_size, num_words, words_per_row, fanout_configs)
        #self.analyze_delay_chain_data(word_size, num_words, words_per_row, analysis_configs)
        #self.graph_delays_and_inp_slews(word_size, num_words, words_per_row, analysis_configs)
        self.graph_inp_slews_and_delay_var(word_size, num_words, words_per_row, analysis_configs)
    
    def save_delay_chain_data(self, word_size, num_words, words_per_row, fanout_configs):
        """Get the delay data by only varying the delay chain size."""
        for fanouts in fanout_configs:
            self.init_data_gen()
            self.set_delay_chain(fanouts)
            self.save_data_sram_corners(word_size, num_words, words_per_row)
    
    def analyze_delay_chain_data(self, word_size, num_words, words_per_row, fanout_configs):
        """Compare and graph delay chain variations over different configurations."""
        if not os.path.exists(DATASET_CSV_NAME):
            debug.error("Could not find dataset CSV. Aborting analysis...",1)
        dc_avgs, dc_vars = [],[]
        rise_avgs, rise_vars = [],[]
        fall_avgs, fall_vars = [],[]
        for fanouts in fanout_configs:
            data_types = ["wl_measures","sae_measures"]
            filenames = self.get_filename_by_config(data_types, word_size, num_words, words_per_row, fanouts)
            wl_dataframe, sae_dataframe = self.get_csv_data(filenames)
            rise_delay, fall_delay = self.get_rise_fall_dc_sum(sae_dataframe)
            delay_sums = self.get_delay_chain_sums(sae_dataframe)
            dc_avgs.append(self.get_average(delay_sums))
            dc_vars.append(self.get_variance(delay_sums))
            
            rise_avgs.append(self.get_average(rise_delay))
            rise_vars.append(self.get_variance(rise_delay))
            
            fall_avgs.append(self.get_average(fall_delay))
            fall_vars.append(self.get_variance(fall_delay))
            debug.info(1,"DC config={}: avg={} variance={}".format(fanouts, dc_avgs[-1], dc_vars[-1]))
            
        #Sort by the delays then graph
        config_copy = list(fanout_configs)
        all_data = zip(dc_avgs,config_copy,dc_vars)
        dc_avgs,config_copy,dc_vars = zip(*sorted(all_data))
        x_ax_label = 'DC Fanouts'
        y_ax_labels = ['Average Delay (ns)', 'Delay Variance (ns)']
        self.plot_delay_variance_data_sets(config_copy, x_ax_label, y_ax_labels, dc_avgs, dc_vars)
        
        config_copy = list(fanout_configs)
        all_data = zip(rise_avgs,config_copy,rise_vars)
        rise_avgs,config_copy,rise_vars = zip(*sorted(all_data))
        x_ax_label = 'DC Fanouts'
        y_ax_labels = ['Average Rise Delay (ns)', 'Rise Delay Variance (ns)']
        self.plot_delay_variance_data_sets(config_copy, x_ax_label, y_ax_labels, rise_avgs, rise_vars)
        
        config_copy = list(fanout_configs)
        all_data = zip(fall_avgs,config_copy,fall_vars)
        fall_avgs,config_copy,fall_vars = zip(*sorted(all_data))
        x_ax_label = 'DC Fanouts'
        y_ax_labels = ['Average Fall Delay (ns)', 'Fall Delay Variance (ns)']
        self.plot_delay_variance_data_sets(config_copy, x_ax_label, y_ax_labels, fall_avgs, fall_vars)
     
    def graph_inp_slews_and_delay_var(self, word_size, num_words, words_per_row, fanout_configs):
        """Compare and graph delay chain variations over different configurations."""
        if not os.path.exists(DATASET_CSV_NAME):
            debug.error("Could not find dataset CSV. Aborting analysis...",1)
        dc_delays_var, dc_slews = [],[]
        rise_delay_var, rise_slew_avgs = [],[]
        fall_delay_var, fall_slew_avgs = [],[]
        for fanouts in fanout_configs:
            data_types = ["sae_measures", "sae_slews"]
            filenames = self.get_filename_by_config(data_types, word_size, num_words, words_per_row, fanouts)
            sae_delay_df, sae_slew_df = self.get_csv_data(filenames)
            
            delay_sums = self.get_delay_chain_sums(sae_delay_df)
            slew_sums = self.get_delay_chain_avg(sae_slew_df)
            dc_delays_var.append(self.get_variance(delay_sums))
            dc_slews.append(self.get_average(slew_sums))
            
            rise_delay, fall_delay = self.get_rise_fall_dc_sum(sae_delay_df)
            rise_delay_var.append(self.get_variance(rise_delay))
            fall_delay_var.append(self.get_variance(fall_delay))
            
            rise_slews, fall_slews = self.get_rise_fall_dc_avg(sae_slew_df)
            rise_slew_avgs.append(self.get_average(rise_slews))
            fall_slew_avgs.append(self.get_average(fall_slews))
            debug.info(1,"DC config={}: slew avg={} delay var={}".format(fanouts, dc_slews[-1], dc_delays_var[-1]))
            
        #Sort by the delays then graph
        config_copy = list(fanout_configs)
        all_data = zip(dc_slews,config_copy,dc_delays_var)
        dc_slews,config_copy,dc_delays_var = zip(*sorted(all_data))
        x_ax_label = 'DC Fanouts'
        y_ax_labels = ['Average Input Slew (ns)', 'Delay Variance (ns)']
        self.plot_delay_variance_data_sets(config_copy, x_ax_label, y_ax_labels, dc_slews, dc_delays_var)
        
        config_copy = list(fanout_configs)
        all_data = zip(rise_slew_avgs,config_copy,rise_delay_var)
        rise_slew_avgs,config_copy,rise_delay_var = zip(*sorted(all_data))
        x_ax_label = 'DC Fanouts'
        y_ax_labels = ['Average Rise Stage Input Slew (ns)', 'Rise Delay Variance (ns)']
        self.plot_delay_variance_data_sets(config_copy, x_ax_label, y_ax_labels, rise_slew_avgs, rise_delay_var)
        
        config_copy = list(fanout_configs)
        all_data = zip(fall_slew_avgs,config_copy,fall_delay_var)
        fall_slew_avgs,config_copy,fall_delay_var = zip(*sorted(all_data))
        x_ax_label = 'DC Fanouts'
        y_ax_labels = ['Average Fall Stage Input Slew (ns)', 'Fall Delay Variance (ns)']
        self.plot_delay_variance_data_sets(config_copy, x_ax_label, y_ax_labels, fall_slew_avgs, fall_delay_var)
    
    def graph_delays_and_inp_slews(self, word_size, num_words, words_per_row, fanout_configs):
        """Compare and graph delay chain variations over different configurations."""
        if not os.path.exists(DATASET_CSV_NAME):
            debug.error("Could not find dataset CSV. Aborting analysis...",1)
        dc_delays, dc_slews = [],[]
        rise_delay_avgs, rise_slew_avgs = [],[]
        fall_delay_avgs, fall_slew_avgs = [],[]
        for fanouts in fanout_configs:
            data_types = ["sae_measures", "sae_slews"]
            filenames = self.get_filename_by_config(data_types, word_size, num_words, words_per_row, fanouts)
            sae_delay_df, sae_slew_df = self.get_csv_data(filenames)
            
            delay_sums = self.get_delay_chain_sums(sae_delay_df)
            slew_sums = self.get_delay_chain_avg(sae_slew_df)
            dc_delays.append(self.get_average(delay_sums))
            dc_slews.append(self.get_average(slew_sums))
            
            rise_delay, fall_delay = self.get_rise_fall_dc_sum(sae_delay_df)
            rise_delay_avgs.append(self.get_average(rise_delay))
            fall_delay_avgs.append(self.get_average(fall_delay))
            
            rise_slews, fall_slews = self.get_rise_fall_dc_avg(sae_slew_df)
            rise_slew_avgs.append(self.get_average(rise_slews))
            fall_slew_avgs.append(self.get_average(fall_slews))
            debug.info(1,"DC config={}: delay avg={} slew avg={}".format(fanouts, dc_delays[-1], dc_slews[-1]))
            
        #Sort by the delays then graph
        config_copy = list(fanout_configs)
        all_data = zip(dc_delays,config_copy,dc_slews)
        dc_delays,config_copy,dc_slews = zip(*sorted(all_data))
        x_ax_label = 'DC Fanouts'
        y_ax_labels = ['Average Delay (ns)', 'Average Input Slew (ns)']
        self.plot_delay_variance_data_sets(config_copy, x_ax_label, y_ax_labels, dc_delays, dc_slews)
        
        config_copy = list(fanout_configs)
        all_data = zip(rise_delay_avgs,config_copy,rise_slew_avgs)
        rise_delay_avgs,config_copy,rise_slew_avgs = zip(*sorted(all_data))
        x_ax_label = 'DC Fanouts'
        y_ax_labels = ['Average Rise Delay (ns)', 'Average Input Slew (ns)']
        self.plot_delay_variance_data_sets(config_copy, x_ax_label, y_ax_labels, rise_delay_avgs, rise_slew_avgs)
        
        config_copy = list(fanout_configs)
        all_data = zip(fall_delay_avgs,config_copy,fall_slew_avgs)
        fall_delay_avgs,config_copy,fall_slew_avgs = zip(*sorted(all_data))
        x_ax_label = 'DC Fanouts'
        y_ax_labels = ['Average Fall Delay (ns)', 'Average Input Slew (ns)']
        self.plot_delay_variance_data_sets(config_copy, x_ax_label, y_ax_labels, fall_delay_avgs, fall_slew_avgs)
    
    
    def get_delay_chain_data(self, sae_dataframe):
        """Get the data of the delay chain over different corners"""
        start_dc_pos = sae_dataframe.columns.get_loc('dc_start_ind')
        end_dc_pos = sae_dataframe.columns.get_loc('dc_end_ind')
        start_data_pos = len(self.config_fields)+len(self.sae_config_fields)+1 #items before this point are configuration related
        delay_data = []
        #Get delay sums over different corners
        for sae_row in sae_dataframe.itertuples():
            start_dc, end_dc = sae_row[start_dc_pos+1], sae_row[end_dc_pos+1]
            dc_delays = sae_row[start_data_pos+start_dc:start_data_pos+end_dc]
            delay_data.append(dc_delays)
        return delay_data
        
    def get_delay_chain_sums(self, sae_dataframe):
        """Calculate the sum of each delay chain for each corner"""
        dc_data = self.get_delay_chain_data(sae_dataframe)
        return [sum(data_list) for data_list in dc_data]
    
    def get_delay_chain_avg(self, sae_dataframe):
        """Calculate the average of each delay chain for each corner"""
        dc_data = self.get_delay_chain_data(sae_dataframe)
        return [sum(data_list)/len(data_list) for data_list in dc_data]
    
    def get_rise_fall_dc_data_per_corner(self,sae_dataframe):
        """Extracts the data from the dataframe which represents the delay chain.
           Delay chain data is marked by indices in the CSV.
        """
        start_dc_pos = sae_dataframe.columns.get_loc('dc_start_ind')
        end_dc_pos = sae_dataframe.columns.get_loc('dc_end_ind')
        start_data_pos = len(self.config_fields)+len(self.sae_config_fields)+1 #items before this point are configuration related
        rise_data = []
        fall_data = []
        #Get delay sums over different corners
        for sae_row in sae_dataframe.itertuples():
            start_dc, end_dc = sae_row[start_dc_pos+1], sae_row[end_dc_pos+1]
            fall_list = sae_row[start_data_pos+start_dc:start_data_pos+end_dc:2]
            rise_list = sae_row[start_data_pos+start_dc+1:start_data_pos+end_dc:2]
            fall_data.append(fall_list)
            rise_data.append(rise_list) 
        return rise_data, fall_data
    
    def get_rise_fall_dc_sum(self,sae_dataframe):
        """Gets the delay/slew sum of the delay chain for every corner"""
        #Get list of lists of delay chain data and reduce to sums
        rise_data, fall_data = self.get_rise_fall_dc_data_per_corner(sae_dataframe)
        rise_sums = [sum(dc_data) for dc_data in rise_data]
        fall_sums = [sum(dc_data) for dc_data in fall_data]
        return rise_sums,fall_sums
    
    def get_rise_fall_dc_avg(self,sae_dataframe):
        """Gets the delay/slew average of the delay chain for every corner"""
        #Get list of lists of delay chain data and reduce to sums
        rise_data, fall_data = self.get_rise_fall_dc_data_per_corner(sae_dataframe)
        rise_avgs = [sum(dc_data)/len(dc_data) for dc_data in rise_data]
        fall_avgs = [sum(dc_data)/len(dc_data) for dc_data in fall_data]
        return rise_avgs,fall_avgs
    
    def get_sum(self, dataframe):
        """Get full delay from csv using the sum field in the df"""
        return list(dataframe['sum'])
    
    def get_variance(self, nums):
        avg = self.get_average(nums)
        delay_variance = sum((xi - avg) ** 2 for xi in nums) / len(nums)
        return delay_variance
        
    def get_average(self,nums):
        return sum(nums) / len(nums)
    
    def plot_data(self, x_labels, y_values):
        """Display a plot using matplot lib. 
           Assumes input x values are just labels and y values are actual data."""
        data_range = [i+1 for i in range(len(x_labels))]
        plt.xticks(data_range, x_labels)
        plt.plot(data_range, y_values, 'ro')
        plt.show()
    
    def plot_delay_variance_data_sets(self, x_labels, x_ax_name, y_labels, y1_delays, y2_vars):
        """Plots two data sets on the same x-axis."""
        data_range = [i for i in range(len(x_labels))]
        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel(str(x_ax_name))
        ax1.set_ylabel(y_labels[0], color=color)
        ax1.plot(data_range, y1_delays, marker='o', color=color, linestyle='')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.tick_params(axis='x', labelrotation=-90)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        #ax2.set_xticks(data_range, x_labels)
        ax2.set_ylabel(y_labels[1], color=color)  # we already handled the x-label with ax1
        ax2.plot(data_range, y2_vars, marker='*', color=color, linestyle='')
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.xticks(data_range, x_labels, rotation=90)
        plt.show()
    
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
        
    def get_csv_data(self, filenames):
        """Returns a dataframe for each file name. Returns as tuple for convenience"""
        dataframes = [pd.read_csv(fname,encoding='utf-8') for fname in filenames]
        return tuple(dataframes)
        
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
        file_list = self.file_name_dict.values()
        wl_meas_df = [pd.read_csv(file_name,encoding='utf-8') for file_name in file_list if "wl_measures" in file_name][0]
        sae_meas_df = [pd.read_csv(file_name,encoding='utf-8') for file_name in file_list if "sae_measures" in file_name][0]
        wl_model_df = [pd.read_csv(file_name,encoding='utf-8') for file_name in file_list if "wl_model" in file_name][0]
        sae_model_df = [pd.read_csv(file_name,encoding='utf-8') for file_name in file_list if "sae_model" in file_name][0]
        
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
        wl_start_data_pos = len(self.config_fields)
        sae_start_data_pos = len(self.config_fields)+len(self.sae_config_fields) 
        error_list = []
        row_count = 0
        for wl_row, sae_row in zip(wl_dataframe.itertuples(), sae_dataframe.itertuples()):             
            debug.info(2, "wl_row:{}".format(wl_row))
            wl_sum = sum(wl_row[wl_start_data_pos+1:])
            debug.info(2, "wl_sum:{}".format(wl_sum))
            sae_sum = sum(sae_row[sae_start_data_pos+1:])
            error_list.append(abs((wl_sum-sae_sum)/wl_sum))
        return error_list
        
    def calculate_delay_variation_error(self, wl_dataframe, sae_dataframe):
        """Measures a base delay from the first corner then the variations from that base"""
        wl_start_data_pos = len(self.config_fields)
        sae_start_data_pos = len(self.config_fields)+len(self.sae_config_fields)
        variation_error_list = []
        count = 0
        for wl_row, sae_row in zip(wl_dataframe.itertuples(), sae_dataframe.itertuples()):
            if count == 0:
                #Create a base delay, variation is defined as the difference between this base
                wl_base = sum(wl_row[wl_start_data_pos+1:])
                debug.info(1, "wl_sum base:{}".format(wl_base))
                sae_base = sum(sae_row[sae_start_data_pos+1:])
                variation_error_list.append(0.0)
            else:
                #Calculate the variation from the respective base and then difference between the variations
                wl_sum = sum(wl_row[wl_start_data_pos+1:])
                wl_base_diff = abs((wl_base-wl_sum)/wl_base)
                sae_sum = sum(sae_row[sae_start_data_pos+1:])
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
        
        #Save file names generated by this run
        if not self.dataset_initialized:
            self.init_dataset_csv(list(sram_data))
        self.add_dataset(word_size, num_words, words_per_row)    
        
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

    def set_delay_chain(self, fanout_list):
        """Force change the parameter in the tech file to specify a delay chain configuration"""
        parameter["static_fanout_list"] = fanout_list
        
    def close_files(self):
        """Closes all files stored in the file dict"""
        #Close the files holding data
        for key,file in self.csv_files.items():
            file.close()
        
        #Write dataframe to the dataset csv
        self.datasets_df.to_csv(DATASET_CSV_NAME, index=False)
   
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
        dc_start_ind, dc_end_ind = self.delay_obj.delay_chain_indices
        sram_specs = [word_size,num_words,words_per_row,dc_resized,*corner]
        sae_specs = [dc_start_ind, dc_end_ind]
        for data_name, data_values in sram_data.items():
            if 'sae' in data_name:
                all_specs = sram_specs+sae_specs
            else:
                all_specs = sram_specs
                
            other_values = self.calculate_other_data_values(data_values)
            self.csv_writers[data_name].writerow(all_specs+sram_data[data_name]+other_values)
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
        self.file_name_dict = {}
        delay_fanout_list = self.delay_obj.get_num_delay_fanout_list()
        fanout_str = '_'.join(str(fanout) for fanout in delay_fanout_list)
        delay_stages = self.delay_obj.get_num_delay_stages()
        delay_stage_fanout = self.delay_obj.get_num_delay_stage_fanout()
        
        for data_name, header_list in header_dict.items():
            file_name = '{}data_{}b_{}word_{}way_dc{}_{}.csv'.format(MODEL_DIR,
                                                                word_size, 
                                                                num_words, 
                                                                words_per_row,
                                                                fanout_str,
                                                                data_name)
            self.file_name_dict[data_name] = file_name
            self.csv_files[data_name] = open(file_name, 'w')
            if 'sae' in data_name:
                fields = (*self.config_fields, *self.sae_config_fields, *header_list, *self.other_data_fields)
            else:
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
