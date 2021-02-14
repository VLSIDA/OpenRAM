import os
import sys

util_dir = "gen_model_util"
cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, cur_dir+'/'+util_dir)

import mapping 
import linreg_scikit
#import keras_models

train_sets = []
test_sets = []     
     
filename = "delays.csv" 
reference_dir = "data"   
file_path = reference_dir +'/'+filename
num_points_train = 7
mp = mapping.mapping()

non_ip_samples, unused_samples = mp.sample_from_file(num_points_train, file_path, reference_dir)
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
        #new_error = lr_scikit.run_model(train_x, train_y, test_x, test_y)
        new_error = keras_models.run_model(train_x, train_y, test_x, test_y)
        print(new_error)