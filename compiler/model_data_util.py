# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California, Santa Cruz
# All rights reserved.
#
import os
import csv
import re
import sys
import csv
import importlib

# Use the HTML file to extra the data. Easier to do than LIB
data_file_ext = ".html"
extended_name = "_extended" # Name addon of extended config file
DEFAULT_LAS = 0

def gen_regex_float_group(num, separator):
    if num <= 0:
        return ''
    float_regex = '([-+]?[0-9]*\.?[0-9]*)'
    full_regex = float_regex
    for i in range(num-1):
        full_regex+=separator+float_regex
    return full_regex

def import_module(mod_name, mod_path):
    spec = importlib.util.spec_from_file_location(mod_name, mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def get_config_mods(openram_dir):
    # Get dataset name used by all the files e.g. sram_1b_16
    files_names = [name for name in os.listdir(openram_dir) if os.path.isfile(openram_dir+'/'+name)]
    log = [name for name in files_names if '.log' in name][0]
    dataset_name = log[:-4]
    sys.path.append(openram_dir)
    print("Extracting dataset:{}".format(dataset_name))

    # Check that the config files exist (including special extended config)
    dir_path = openram_dir+"/"
    #sys.path.append(dir_path)
    #imp_mod = None
    imp_mod_extended = None
    # if not os.path.exists(openram_dir+'/'+dataset_name+".py"):
        # print("Python module for {} not found.".format(dataset_name))
        # imp_mod = None
    # else:
        # imp_mod = import_module(dataset_name, openram_dir+"/"+dataset_name+".py")

    if not os.path.exists(openram_dir+'/'+dataset_name+extended_name+".py"):
        print("Extended Python module for {} not found.".format(dataset_name))
        imp_mod_extended = None
    else:
        imp_mod_extended = import_module(dataset_name+extended_name, openram_dir+"/"+dataset_name+extended_name+".py")

    datasheet_fname = openram_dir+"/"+dataset_name+data_file_ext

    return dataset_name, imp_mod_extended, datasheet_fname

def get_corners(datafile_contents, dataset_name, tech):
    """Search through given datasheet to find all corners available"""

    corner_regex = r"{}.*{},([-+]?[0-9]*\.?[0-9]*),([-+]?[0-9]*\.?[0-9]*),([tsfTSF][tsfTSF]),".format(dataset_name, tech)
    corners = re.findall(corner_regex,datafile_contents)
    return corners # List of corner tuples in order (T, V, P)

feature_names = ['num_words',
                 'word_size',
                 'words_per_row',
                 'local_array_size',
                 'area',
                 'process',
                 'voltage',
                 'temperature',
                 'slew',
                 'load']
output_names =  ['rise_delay',
                 'fall_delay',
                 'rise_slew',
                 'fall_slew',
                 'write1_power',
                 'write0_power',
                 'read1_power',
                 'read0_power',
                 'leakage_power']

multivalue_names = ['cell_rise_0',
                    'cell_fall_0',
                    'rise_transition_0',
                    'fall_transition_0']
singlevalue_names = ['write_rise_power_0',
                    'write_fall_power_0',
                    'read_rise_power_0',
                    'read_fall_power_0']

def write_to_csv(dataset_name, csv_file, datasheet_fname, imp_mod, mode):


    writer = csv.writer(csv_file,lineterminator='\n')
    # If the file was opened to write and not append then we write the header
    if mode == 'w':
        writer.writerow(feature_names+output_names)

    try:
        load_slews = imp_mod.use_specified_load_slew
    except:
        load_slews = None

    if load_slews != None:
        num_items = len(load_slews)
        num_loads_or_slews = len(load_slews)
    else:
        # These are the defaults for openram
        num_items = 9
        num_loads_or_slews = 3

    try:
        f = open(datasheet_fname, "r")
    except IOError:
        print("Unable to open spice output file: {0}".format(datasheet_fname))
        return None
    print("Opened file",datasheet_fname)
    contents = f.read()
    f.close()

    available_corners = get_corners(contents, dataset_name, imp_mod.tech_name)

    # Loop through corners, adding data for each corner
    for (temp, voltage, process) in available_corners:

        # Create a regex to search the datasheet for specified outputs
        voltage_str = "".join(['\\'+i if i=='.' else i for i in str(voltage)])
        area_regex = r"Area \(&microm<sup>2<\/sup>\)<\/td><td>(\d+)"

        leakage_regex = r"leakage<\/td><td>([-+]?[0-9]*\.?[0-9]*)"
        slew_regex = r"rise transition<\/td><td>([-+]?[0-9]*\.?[0-9]*)"

        if load_slews == None:
            float_regex = gen_regex_float_group(num_loads_or_slews, ', ')
            inp_slews_regex = r"{},{}.*{},{},{},.*slews,\[{}".format(
                dataset_name,
                imp_mod.num_words,
                str(temp),
                voltage_str,
                process,
                float_regex)

            loads_regex = r"{},{}.*{},{},{},.*loads,\[{}".format(
                dataset_name,
                imp_mod.num_words,
                str(temp),
                voltage_str,
                process,
                float_regex)

        float_regex = gen_regex_float_group(num_items, ', ')
        multivalue_regexs = []
        for value_identifier in multivalue_names:
            regex_str = r"{},{}.*{},{},{},.*{},\[{}".format(
                dataset_name,
                imp_mod.num_words,
                str(temp),
                voltage_str,
                process,
                value_identifier,
                float_regex)
            multivalue_regexs.append(regex_str)

        singlevalue_regexs = []
        for value_identifier in singlevalue_names:
            regex_str = r"{},{}.*{},{},{},.*{},([-+]?[0-9]*\.?[0-9]*)".format(
                dataset_name,
                imp_mod.num_words,
                str(temp),
                voltage_str,
                process,
                value_identifier,
                float_regex)
            singlevalue_regexs.append(regex_str)

        area_vals = re.search(area_regex,contents)
        leakage_vals = re.search(leakage_regex,contents)
        if load_slews == None:
            inp_slew_vals = re.search(inp_slews_regex,contents)
            load_vals = re.search(loads_regex,contents)

        datasheet_multivalues = [re.search(r,contents) for r in multivalue_regexs]
        datasheet_singlevalues = [re.search(r,contents) for r in singlevalue_regexs]
        for dval in datasheet_multivalues+datasheet_singlevalues:
            if dval == None:
                print("Error occurred while searching through datasheet: {}".format(datasheet_fname))
                print("datasheet_multivalues",datasheet_multivalues)
                print("datasheet_singlevalues",datasheet_singlevalues)
                print("multivalue_regexs",multivalue_regexs[0])
                sys.exit()
                return None

        try:
            las = imp_mod.local_array_size
        except:
            las = DEFAULT_LAS

        # All the extracted values are delays but val[2] is the max delay
        feature_vals = [imp_mod.num_words,
                        imp_mod.word_size,
                        imp_mod.words_per_row,
                        las,
                        area_vals[1],
                        process,
                        voltage,
                        temp]

        if load_slews == None:
            c = 1
            for i in range(num_loads_or_slews):
                for j in range(num_loads_or_slews):
                    multi_values = [val[i+j+c] for val in datasheet_multivalues]
                    single_values = [val[1] for val in datasheet_singlevalues]
                    writer.writerow(feature_vals+[inp_slew_vals[i+1], load_vals[j+1]]+multi_values+single_values+[leakage_vals[1]])
                c+=2
        else:
            # if num loads and num slews are not equal then this might break because of how OpenRAM formats
            # the outputs
            c = 1
            for load,slew in load_slews:
                multi_values = [val[c] for val in datasheet_multivalues]
                single_values = [val[1] for val in datasheet_singlevalues]
                writer.writerow(feature_vals+[slew, load]+multi_values+single_values+[leakage_vals[1]])
                c+=1


def extract_data(openram_dir, out_dir, is_first):
    """Given an OpenRAM output dir, searches through datasheet files and ouputs
       a CSV files with data used in model."""

    # Get dataset name used by all the files e.g. sram_1b_16
    dataset_name, inp_mod, datasheet_fname = get_config_mods(openram_dir)
    if inp_mod == None:
        print("Config file(s) for this run not found. Skipping...")
        return

    if is_first:
        mode = 'w'
    else:
        mode = 'a+'
    with open("{}/sim_data.csv".format(out_dir), mode, newline='\n') as data_file:
        write_to_csv(dataset_name, data_file, datasheet_fname, inp_mod, mode)

    return out_dir

def gen_model_csv(openram_dir_path, out_dir):
    if not os.path.isdir(input_dir_path):
        print("Path does not exist: {}".format(input_dir_path))
        return

    if not os.path.isdir(out_path):
        print("Path does not exist: {}".format(out_path))
        return

    is_first = True
    oram_dirs = [openram_dir_path+'/'+name for name in os.listdir(openram_dir_path) if os.path.isdir(openram_dir_path+'/'+name)]
    for dir in oram_dirs:
        extract_data(dir, out_dir, is_first)
        is_first = False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python model_data_util.py path_to_openram_dirs out_dir_path")
    else:
        input_dir_path = sys.argv[1]
        out_path = sys.argv[2]
        gen_model_csv(input_dir_path, out_path)
