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

    def get_prediction(self):

        train_sets = []
        test_sets = []     
               
        file_path = data_dir +'/'+data_filename
        num_points_train = 5

        non_ip_samples, unused_samples = sample_from_file(num_points_train, file_path, data_dir)
        nip_features_subset, nip_labels_subset = non_ip_samples[:, :-1], non_ip_samples[:,-1:]
        nip_test_feature_subset, nip_test_labels_subset = unused_samples[:, :-1], unused_samples[:,-1:]

        train_sets = [(nip_features_subset, nip_labels_subset)]
        test_sets = [(nip_test_feature_subset, nip_test_labels_subset)]

        runs_per_model = 1

        for train_tuple, test_tuple in zip(train_sets, test_sets):
            train_x, train_y = train_tuple
            test_x, test_y = test_tuple

            errors = {}
            min_train_set = None
            for _ in range(runs_per_model):
                new_error = self.run_model(train_x, train_y, test_x, test_y, data_dir)
                debug.info(1, "Model Error: {}".format(new_error))

    def run_model(x,y,test_x,test_y, reference_dir):
        model = LinearRegression()
        model.fit(x, y)

        pred = model.predict(test_x)

        #print(pred)
        unscaled_labels = unscale_data(test_y.tolist(), reference_dir)
        unscaled_preds = unscale_data(pred.tolist(), reference_dir)
        unscaled_labels, unscaled_preds = (list(t) for t in zip(*sorted(zip(unscaled_labels, unscaled_preds))))
        avg_error = abs_error(unscaled_labels, unscaled_preds)
        max_error = max_error(unscaled_labels, unscaled_preds)
        min_error = min_error(unscaled_labels, unscaled_preds)

        errors = {"avg_error": avg_error, "max_error":max_error, "min_error":min_error}    
        return errors