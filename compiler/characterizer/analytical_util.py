# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os
import csv
import math
import numpy as np
from openram import debug


process_transform = {'SS':0.0, 'TT': 0.5, 'FF':1.0}

def get_data_names(file_name, exclude_area=True):
    """
    Returns just the data names in the first row of the CSV
    """

    with open(file_name, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        row_iter = 0
        # reader is iterable not a list, probably  a better way to do this
        for row in csv_reader:
            # Return names from first row
            names = row[0].split(',')
            break
    if exclude_area:
        try:
            area_ind = names.index('area')
        except ValueError:
            area_ind = -1

        if area_ind != -1:
            names = names[:area_ind] + names[area_ind+1:]
    return names

def get_data(file_name):
    """
    Returns data in CSV as lists of features
    """

    with open(file_name, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        row_iter = 0
        removed_items = 1
        for row in csv_reader:
            row_iter += 1
            if row_iter == 1:
                feature_names = row[0].split(',')
                input_list = [[] for _ in range(len(feature_names)-removed_items)]
                try:
                    # Save to remove area
                    area_ind = feature_names.index('area')
                except ValueError:
                    area_ind = -1

                try:
                    process_ind = feature_names.index('process')
                except:
                    debug.error('Process not included as a feature.')
                continue



            data = []
            split_str = row[0].split(',')
            for i in range(len(split_str)):
                if i == process_ind:
                    data.append(process_transform[split_str[i]])
                elif i == area_ind:
                    continue
                else:
                    data.append(float(split_str[i]))

            data[0] = math.log(data[0], 2)

            for i in range(len(data)):
                input_list[i].append(data[i])

    return input_list

def apply_samples_to_data(all_data, algo_samples):
    # Take samples from algorithm and match them to samples in data
    data_samples, unused_data = [], []
    sample_positions = set()
    for sample in algo_samples:
        sample_positions.add(find_sample_position_with_min_error(all_data, sample))

    for i in range(len(all_data)):
        if i in sample_positions:
            data_samples.append(all_data[i])
        else:
            unused_data.append(all_data[i])

    return data_samples, unused_data

def find_sample_position_with_min_error(data, sampled_vals):
    min_error = 0
    sample_pos = 0
    count = 0
    for data_slice in data:
        error = squared_error(data_slice, sampled_vals)
        if min_error == 0 or error < min_error:
            min_error = error
            sample_pos = count
        count += 1
    return sample_pos

def squared_error(list_a, list_b):
    error_sum = 0;
    for a,b in zip(list_a, list_b):
        error_sum+=(a-b)**2
    return error_sum


def get_max_min_from_datasets(dir):
    if not os.path.isdir(dir):
        debug.warning("Input Directory not found:{}".format(dir))
        return [], [], []

    # Assuming all files are CSV
    data_files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    maxs,mins,sums,total_count = [],[],[],0
    for file in data_files:
        data = get_data(os.path.join(dir, file))
        # Get max, min, sum, and count from every file
        data_max, data_min, data_sum, count = [],[],[], 0
        for feature_list in data:
            data_max.append(max(feature_list))
            data_min.append(min(feature_list))
            data_sum.append(sum(feature_list))
            count = len(feature_list)

        # Aggregate the data
        if not maxs or not mins or not sums:
             maxs,mins,sums,total_count = data_max,data_min,data_sum,count
        else:
            for i in range(len(maxs)):
                maxs[i] = max(data_max[i], maxs[i])
                mins[i] = min(data_min[i], mins[i])
                sums[i] = data_sum[i]+sums[i]
            total_count+=count

    avgs = [s/total_count for s in sums]
    return maxs,mins,avgs

def get_max_min_from_file(path):
    if not os.path.isfile(path):
        debug.warning("Input file not found: {}".format(path))
        return [], [], []


    data = get_data(path)
    # Get max, min, sum, and count from every file
    data_max, data_min, data_sum, count = [],[],[], 0
    for feature_list in data:
        data_max.append(max(feature_list))
        data_min.append(min(feature_list))
        data_sum.append(sum(feature_list))
        count = len(feature_list)

    avgs = [s/count for s in data_sum]
    return data_max, data_min, avgs

def get_data_and_scale(file_name, sample_dir):
    maxs,mins,avgs = get_max_min_from_datasets(sample_dir)

    # Get data
    all_data = get_data(file_name)

    # Scale data from file
    self_scaled_data = [[] for _ in range(len(all_data[0]))]
    self_maxs,self_mins = [],[]
    for feature_list, cur_max, cur_min in zip(all_data,maxs, mins):
        for i in range(len(feature_list)):
            self_scaled_data[i].append((feature_list[i]-cur_min)/(cur_max-cur_min))

    return np.asarray(self_scaled_data)

def rescale_data(data, old_maxs, old_mins, new_maxs, new_mins):
    # unscale from old values, rescale by new values
    data_new_scaling = []
    for data_row in data:
        scaled_row = []
        for val, old_max,old_min, cur_max, cur_min in zip(data_row, old_maxs,old_mins, new_maxs, new_mins):
            unscaled_data = val*(old_max-old_min) + old_min
            scaled_row.append((unscaled_data-cur_min)/(cur_max-cur_min))

        data_new_scaling.append(scaled_row)

    return data_new_scaling

def sample_from_file(num_samples, file_name, sample_dir=None):
    """
    Get a portion of the data from CSV file and scale it based on max/min of dataset.
    Duplicate samples are trimmed.
    """

    if sample_dir:
        maxs,mins,avgs = get_max_min_from_datasets(sample_dir)
    else:
        maxs,mins,avgs = [], [], []

    # Get data
    all_data = get_data(file_name)

    # Get algorithms sample points, assuming hypercube for now
    num_labels = 1
    inp_dims = len(all_data) - num_labels
    samples = np.random.rand(num_samples, inp_dims)


    # Scale data from file
    self_scaled_data = [[] for _ in range(len(all_data[0]))]
    self_maxs,self_mins = [],[]
    for feature_list in all_data:
        max_val = max(feature_list)
        self_maxs.append(max_val)
        min_val = min(feature_list)
        self_mins.append(min_val)
        for i in range(len(feature_list)):
            self_scaled_data[i].append((feature_list[i]-min_val)/(max_val-min_val))
    # Apply algorithm sampling points to available data
    sampled_data, unused_data = apply_samples_to_data(self_scaled_data,samples)

    #unscale values and rescale using all available data (both sampled and unused points rescaled)
    if len(maxs)!=0 and len(mins)!=0:
        sampled_data = rescale_data(sampled_data, self_maxs,self_mins, maxs, mins)
        unused_new_scaling = rescale_data(unused_data, self_maxs,self_mins, maxs, mins)

    return np.asarray(sampled_data), np.asarray(unused_new_scaling)

def get_scaled_data(file_name):
    """Get data from CSV file and scale it based on max/min of dataset"""

    if file_name:
        maxs,mins,avgs = get_max_min_from_file(file_name)
    else:
        maxs,mins,avgs = [], [], []

    # Get data
    all_data = get_data(file_name)

    # Data is scaled by max/min and data format is changed to points vs feature lists
    self_scaled_data = scale_data_and_transform(all_data)
    data_np = np.asarray(self_scaled_data)
    return data_np

def scale_data_and_transform(data):
    """
    Assume data is a list of features, change to a list of points and max/min scale
    """

    scaled_data = [[] for _ in range(len(data[0]))]
    for feature_list in data:
        max_val = max(feature_list)
        min_val = min(feature_list)

        for i in range(len(feature_list)):
            if max_val == min_val:
                scaled_data[i].append(0.0)
            else:
                scaled_data[i].append((feature_list[i]-min_val)/(max_val-min_val))
    return scaled_data

def scale_input_datapoint(point, file_path):
    """
    Input data has no output and needs to be scaled like the model inputs during
    training.
    """
    maxs, mins, avgs = get_max_min_from_file(file_path)
    debug.info(3, "maxs={}".format(maxs))
    debug.info(3, "mins={}".format(mins))
    debug.info(3, "point={}".format(point))

    scaled_point = []
    for feature, mx, mn in zip(point, maxs, mins):
        if mx == mn:
            scaled_point.append(0.0)
        else:
            scaled_point.append((feature-mn)/(mx-mn))
    return scaled_point

def unscale_data(data, file_path, pos=None):
    if file_path:
        maxs,mins,avgs = get_max_min_from_file(file_path)
    else:
        debug.error("Must provide reference data to unscale")
        return None

    # Hard coded to only convert the last max/min (i.e. the label of the data)
    if pos == None:
        maxs,mins,avgs = maxs[-1],mins[-1],avgs[-1]
    else:
        maxs,mins,avgs = maxs[pos],mins[pos],avgs[pos]
    unscaled_data = []
    for data_row in data:
        unscaled_val = data_row*(maxs-mins) + mins
        unscaled_data.append(unscaled_val)

    return unscaled_data

def abs_error(labels, preds):
    total_error = 0
    for label_i, pred_i in zip(labels, preds):
        cur_error = abs(label_i[0]-pred_i[0])/label_i[0]
        total_error += cur_error
    return total_error/len(labels)

def max_error(labels, preds):
    mx_error = 0
    for label_i, pred_i in zip(labels, preds):
        cur_error = abs(label_i[0]-pred_i[0])/label_i[0]
        mx_error = max(cur_error, mx_error)
    return mx_error

def min_error(labels, preds):
    mn_error = 1
    for label_i, pred_i in zip(labels, preds):
        cur_error = abs(label_i[0]-pred_i[0])/label_i[0]
        mn_error = min(cur_error, mn_error)
    return mn_error
