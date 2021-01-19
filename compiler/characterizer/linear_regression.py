# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

from .analytical_util import *
from .simulation import simulation
from globals import OPTS
import debug

import os
from sklearn.linear_model import LinearRegression
import math

relative_data_path = "/sim_data"
data_fnames = ["rise_delay.csv",
               "fall_delay.csv",
               "rise_slew.csv",
               "fall_slew.csv",
               "write1_power.csv",
               "write0_power.csv",
               "read1_power.csv",
               "read0_power.csv",
               "leakage_data.csv"]
# Positions must correspond to data_fname list               
lib_dnames = ["delay_lh",
              "delay_hl",
              "slew_lh",
              "slew_hl",
              "write1_power",
              "write0_power",
              "read1_power",
              "read0_power",
              "leakage_power"]             
data_dir = OPTS.openram_tech+relative_data_path
data_paths = {dname:data_dir +'/'+fname for dname, fname in zip(lib_dnames, data_fnames)}

class linear_regression(simulation):

    def __init__(self, sram, spfile, corner):
        super().__init__(sram, spfile, corner)
        self.set_corner(corner)

    def get_lib_values(self, slews, loads):
        """
        A model and prediction is created for each output needed for the LIB 
        """

        log_num_words = math.log(OPTS.num_words, 2)
        debug.info(1, "OPTS.words_per_row={}".format(OPTS.words_per_row))
        model_inputs = [log_num_words, 
                        OPTS.word_size, 
                        OPTS.words_per_row, 
                        self.sram.width * self.sram.height,
                        process_transform[self.process], 
                        self.vdd_voltage, 
                        self.temperature]  

        self.create_measurement_names()
        models = self.train_models()

        # Set delay/power for slews and loads
        port_data = self.get_empty_measure_data_dict()
        debug.info(1, 'Slew, Load, Delay(ns), Slew(ns)')
        max_delay = 0.0
        for slew in slews:
            for load in loads:
                # List returned with value order being delay, power, leakage, slew
                sram_vals = self.get_predictions(model_inputs+[slew, load], models)
                # Delay is only calculated on a single port and replicated for now.
                for port in self.all_ports:
                    port_data[port]['delay_lh'].append(sram_vals['delay_lh'])
                    port_data[port]['delay_hl'].append(sram_vals['delay_hl'])
                    port_data[port]['slew_lh'].append(sram_vals['slew_lh'])
                    port_data[port]['slew_hl'].append(sram_vals['slew_hl'])
                    
                    port_data[port]['write1_power'].append(sram_vals['write1_power'])
                    port_data[port]['write0_power'].append(sram_vals['write0_power'])
                    port_data[port]['read1_power'].append(sram_vals['read1_power'])
                    port_data[port]['read0_power'].append(sram_vals['read0_power'])
                    
                    # Disabled power not modeled. Copied from other power predictions
                    port_data[port]['disabled_write1_power'].append(sram_vals['write1_power'])
                    port_data[port]['disabled_write0_power'].append(sram_vals['write0_power'])
                    port_data[port]['disabled_read1_power'].append(sram_vals['read1_power'])
                    port_data[port]['disabled_read0_power'].append(sram_vals['read0_power'])
                        

        # Estimate the period as double the delay with margin
        period_margin = 0.1
        sram_data = {"min_period": sram_vals['delay_lh'] * 2,
                     "leakage_power": sram_vals["leakage_power"]}

        debug.info(2, "SRAM Data:\n{}".format(sram_data))
        debug.info(2, "Port Data:\n{}".format(port_data))

        return (sram_data, port_data)

    def get_predictions(self, model_inputs, models): 
        """
        Generate a model and prediction for LIB output
        """
        
        #Scaled the inputs using first data file as a reference
        data_name = lib_dnames[0]       
        scaled_inputs = np.asarray([scale_input_datapoint(model_inputs, data_paths[data_name])])

        predictions = {}
        for dname in data_paths.keys():
            path = data_paths[dname]
            m = models[dname]
        
            features, labels = get_scaled_data(path)
            scaled_pred = self.model_prediction(m, scaled_inputs)
            pred = unscale_data(scaled_pred.tolist(), path)
            debug.info(1,"Unscaled Prediction = {}".format(pred))
            predictions[dname] = pred[0][0]
        return predictions

    def train_models(self):
        """
        Generate and return models
        """
        models = {}
        for dname, dpath in data_paths.items():
            features, labels = get_scaled_data(dpath)
            model = self.generate_model(features, labels)
            models[dname] = model
        return models


    def generate_model(self, features, labels):
        """
        Supervised training of model.
        """
        
        model = LinearRegression()
        model.fit(features, labels)
        return model
        
    def model_prediction(self, model, features):    
        """
        Have the model perform a prediction and unscale the prediction
        as the model is trained with scaled values.
        """
        
        pred = model.predict(features)
        return pred
        