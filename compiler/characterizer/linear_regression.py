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
               
data_dir = OPTS.openram_tech+relative_data_path
data_paths = [data_dir +'/'+fname for fname in data_fnames]

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
                # FIXME: make order less hard coded
                sram_vals = self.get_predictions(model_inputs+[slew, load], models)
                # Delay is only calculated on a single port and replicated for now.
                for port in self.all_ports:
                    port_data[port]['delay_lh'].append(sram_vals[0][0][0])
                    port_data[port]['delay_hl'].append(sram_vals[1][0][0])
                    port_data[port]['slew_lh'].append(sram_vals[2][0][0])
                    port_data[port]['slew_hl'].append(sram_vals[3][0][0])
                    
                    port_data[port]['write1_power'].append(sram_vals[4][0][0])
                    port_data[port]['write0_power'].append(sram_vals[5][0][0])
                    port_data[port]['read1_power'].append(sram_vals[6][0][0])
                    port_data[port]['read0_power'].append(sram_vals[7][0][0])
                    
                    # Disabled power not modeled. Copied from other power predictions
                    port_data[port]['disabled_write1_power'].append(sram_vals[4][0][0])
                    port_data[port]['disabled_write0_power'].append(sram_vals[5][0][0])
                    port_data[port]['disabled_read1_power'].append(sram_vals[6][0][0])
                    port_data[port]['disabled_read0_power'].append(sram_vals[7][0][0])
                        

        # Estimate the period as double the delay with margin
        period_margin = 0.1
        sram_data = {"min_period": sram_vals[0][0][0] * 2,
                     "leakage_power": sram_vals[8][0][0]}

        debug.info(2, "SRAM Data:\n{}".format(sram_data))
        debug.info(2, "Port Data:\n{}".format(port_data))

        return (sram_data, port_data)

    def get_predictions(self, model_inputs, models): 
        """
        Generate a model and prediction for LIB output
        """
               
        scaled_inputs = np.asarray([scale_input_datapoint(model_inputs, data_paths[0])])

        predictions = []
        for m, path in zip(models, data_paths):
            features, labels = get_scaled_data(path)
            scaled_pred = self.model_prediction(m, scaled_inputs)
            pred = unscale_data(scaled_pred.tolist(), path)
            debug.info(1,"Unscaled Prediction = {}".format(pred))
            predictions.append(pred)
        return predictions

    def train_models(self):
        """
        Generate and return models
        """
        models = []
        for path in data_paths:
            features, labels = get_scaled_data(path)
            model = self.generate_model(features, labels)
            models.append(model)
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
        