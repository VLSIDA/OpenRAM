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
data_filename = "data.csv"
tech_path = os.environ.get('OPENRAM_TECH')
data_dir = tech_path+'/'+OPTS.tech_name+relative_data_path

class linear_regression():

    def __init__(self):
        self.model = None

    def get_prediction(self, model_inputs):

        train_sets = []
        test_sets = []     
               
        file_path = data_dir +'/'+data_filename
        scaled_inputs = np.asarray(scale_input_datapoint(model_inputs, data_dir))

        features, labels = get_scaled_data(file_path, data_dir)
        self.train_model(features, labels)
        scaled_pred = model_prediction(model_inputs)
        pred = unscale_data(scaled_pred.tolist(), data_dir)
        debug.info(1,"Unscaled Prediction = {}".format(pred))
        return pred

    def train_model(self, features, labels):
        """
        Supervised training of model.
        """
        
        self.model = LinearRegression()
        self.model.fit(features, labels)
        
    def model_prediction(self, features):    
        """
        Have the model perform a prediction and unscale the prediction
        as the model is trained with scaled values.
        """
        
        pred = self.model.predict(features)
        debug.info(1, "pred={}".format(pred))
        return pred
        