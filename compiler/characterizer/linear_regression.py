# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

import os
from sklearn.linear_model import LinearRegression
from .analytical_util import *
from globals import OPTS
import debug

relative_data_path = "/sim_data"
delay_data_filename = "data.csv"
power_data_filename = "power_data.csv"
tech_path = os.environ.get('OPENRAM_TECH')
data_dir = tech_path+'/'+OPTS.tech_name+relative_data_path

class linear_regression():

    def __init__(self):
        self.delay_model = None
        self.power_model = None

    def get_predictions(self, model_inputs): 
               
        delay_file_path = data_dir +'/'+delay_data_filename
        power_file_path = data_dir +'/'+power_data_filename
        scaled_inputs = np.asarray([scale_input_datapoint(model_inputs, delay_file_path)])

        predictions = []
        for path, model in zip([delay_file_path, power_file_path], [self.delay_model, self.power_model]):
            features, labels = get_scaled_data(path)
            model = self.generate_model(features, labels)
            scaled_pred = self.model_prediction(model, scaled_inputs)
            pred = unscale_data(scaled_pred.tolist(), path)
            debug.info(1,"Unscaled Prediction = {}".format(pred))
            predictions.append(pred)
        return predictions

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
        