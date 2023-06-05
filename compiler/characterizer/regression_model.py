# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import math
from openram import debug
from openram import OPTS
from .analytical_util import *
from .simulation import simulation


relative_data_path = "sim_data"
data_file = "sim_data.csv"
data_fnames = ["rise_delay.csv",
               "fall_delay.csv",
               "rise_slew.csv",
               "fall_slew.csv",
               "write1_power.csv",
               "write0_power.csv",
               "read1_power.csv",
               "read0_power.csv",
               "leakage_data.csv",
               "sim_time.csv"]
# Positions must correspond to data_fname list
lib_dnames = ["delay_lh",
              "delay_hl",
              "slew_lh",
              "slew_hl",
              "write1_power",
              "write0_power",
              "read1_power",
              "read0_power",
              "leakage_power",
              "sim_time"]
# Check if another data dir was specified
if OPTS.sim_data_path == None:
    data_dir = OPTS.openram_tech+relative_data_path
else:
    data_dir = OPTS.sim_data_path

data_path = data_dir + '/' + data_file

class regression_model(simulation):

    def __init__(self, sram, spfile, corner):
        super().__init__(sram, spfile, corner)
        self.set_corner(corner)

    def get_lib_values(self, load_slews):
        """
        A model and prediction is created for each output needed for the LIB
        """

        debug.info(1, "Characterizing SRAM using regression models.")
        log_num_words = math.log(OPTS.num_words, 2)
        model_inputs = [log_num_words,
                        OPTS.word_size,
                        OPTS.words_per_row,
                        OPTS.local_array_size,
                        process_transform[self.process],
                        self.vdd_voltage,
                        self.temperature]
                        # Area removed for now
                        # self.sram.width * self.sram.height,
        # Include above inputs, plus load and slew which are added below
        self.num_inputs = len(model_inputs)+2

        self.create_measurement_names()
        models = self.train_models()

        # Set delay/power for slews and loads
        port_data = self.get_empty_measure_data_dict()
        debug.info(1, 'Slew, Load, Port, Delay(ns), Slew(ns)')
        max_delay = 0.0
        for load, slew in load_slews:
            # List returned with value order being delay, power, leakage, slew
            sram_vals = self.get_predictions(model_inputs+[slew, load], models)
            # Delay is only calculated on a single port and replicated for now.
            for port in self.all_ports:
                port_data[port]['delay_lh'].append(sram_vals['rise_delay'])
                port_data[port]['delay_hl'].append(sram_vals['fall_delay'])
                port_data[port]['slew_lh'].append(sram_vals['rise_slew'])
                port_data[port]['slew_hl'].append(sram_vals['fall_slew'])

                port_data[port]['write1_power'].append(sram_vals['write1_power'])
                port_data[port]['write0_power'].append(sram_vals['write0_power'])
                port_data[port]['read1_power'].append(sram_vals['read1_power'])
                port_data[port]['read0_power'].append(sram_vals['read0_power'])

                # Disabled power not modeled. Copied from other power predictions
                port_data[port]['disabled_write1_power'].append(sram_vals['write1_power'])
                port_data[port]['disabled_write0_power'].append(sram_vals['write0_power'])
                port_data[port]['disabled_read1_power'].append(sram_vals['read1_power'])
                port_data[port]['disabled_read0_power'].append(sram_vals['read0_power'])

                debug.info(1, '{}, {}, {}, {}, {}'.format(slew,
                                                          load,
                                                          port,
                                                          sram_vals['rise_delay'],
                                                          sram_vals['rise_slew']))
        # Estimate the period as double the delay with margin
        period_margin = 0.1
        sram_data = {"min_period": sram_vals['rise_delay'] * 2,
                     "leakage_power": sram_vals["leakage_power"]}

        debug.info(2, "SRAM Data:\n{}".format(sram_data))
        debug.info(2, "Port Data:\n{}".format(port_data))

        return (sram_data, port_data)

    def get_predictions(self, model_inputs, models):
        """
        Generate a model and prediction for LIB output
        """

        #Scaled the inputs using first data file as a reference
        scaled_inputs = np.asarray([scale_input_datapoint(model_inputs, data_path)])

        predictions = {}
        out_pos = 0
        for dname in self.output_names:
            m = models[dname]

            scaled_pred = self.model_prediction(m, scaled_inputs)
            pred = unscale_data(scaled_pred.tolist(), data_path, pos=self.num_inputs+out_pos)
            debug.info(2,"Unscaled Prediction = {}".format(pred))
            predictions[dname] = pred[0]
            out_pos+=1
        return predictions

    def train_models(self):
        """
        Generate and return models
        """
        self.output_names = get_data_names(data_path)[self.num_inputs:]
        data = get_scaled_data(data_path)
        features, labels = data[:, :self.num_inputs], data[:,self.num_inputs:]

        output_num = 0
        models = {}
        for o_name in self.output_names:
            output_label = labels[:,output_num]
            model = self.generate_model(features, output_label)
            models[o_name] = model
            output_num+=1

        return models

    def score_model(self):
        num_inputs = 9 #FIXME - should be defined somewhere else
        self.output_names = get_data_names(data_path)[num_inputs:]
        data = get_scaled_data(data_path)
        features, labels = data[:, :num_inputs], data[:,num_inputs:]

        output_num = 0
        models = {}
        debug.info(1, "Output name, score")
        for o_name in self.output_names:
            output_label = labels[:,output_num]
            model = self.generate_model(features, output_label)
            scr = model.score(features, output_label)
            debug.info(1, "{}, {}".format(o_name, scr))
            output_num+=1


    def cross_validation(self, test_only=None):
        """Wrapper for sklean cross validation function for OpenRAM regression models.
           Returns the mean accuracy for each model/output."""

        from sklearn.model_selection import cross_val_score
        untrained_model = self.get_model()

        num_inputs = 9 #FIXME - should be defined somewhere else
        self.output_names = get_data_names(data_path)[num_inputs:]
        data = get_scaled_data(data_path)
        features, labels = data[:, :num_inputs], data[:,num_inputs:]

        output_num = 0
        models = {}
        debug.info(1, "Output name, mean_accuracy, std_dev")
        model_scores = {}
        if test_only != None:
            test_outputs = test_only
        else:
            test_outputs = self.output_names
        for o_name in test_outputs:
            output_label = labels[:,output_num]
            scores = cross_val_score(untrained_model, features, output_label, cv=10)
            debug.info(1, "{}, {}, {}".format(o_name, scores.mean(), scores.std()))
            model_scores[o_name] = scores.mean()
            output_num+=1

        return model_scores

    # Fixme - only will work for sklearn regression models
    def save_model(self, model_name, model):
        try:
            OPTS.model_dict
        except AttributeError:
            OPTS.model_dict = {}
        OPTS.model_dict[model_name+"_coef"] = list(model.coef_[0])
        debug.info(1,"Coefs of {}:{}".format(model_name,OPTS.model_dict[model_name+"_coef"]))
        OPTS.model_dict[model_name+"_intercept"] = float(model.intercept_)
