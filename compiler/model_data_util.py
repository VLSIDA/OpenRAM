import os
import csv
import re
import sys
import csv

# Use the HTML file to extra the data. Easier to do than LIB
data_file_ext = ".html"
extended_name = "_extended" # Name addon of extended config file

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
    print("Extracting dataset:{}".format(dataset_name))
     
    # Check that the config files exist (including special extended config) 
    dir_path = openram_dir+"/"
    #sys.path.append(dir_path)
    imp_mod = None
    imp_mod_extended = None
    if not os.path.exists(openram_dir+'/'+dataset_name+".py"):
        print("Python module for {} not found. Returning...".format(dataset_name))
    else:
        imp_mod = import_module(dataset_name, openram_dir+"/"dataset_name+".py")
        
    if not os.path.exists(openram_dir+'/'+dataset_name+extended_name+".py"):
        print("Python module for {} not found. Returning...".format(dataset_name))
    else:
        imp_mod_extended = import_module(dataset_name+extended_name, openram_dir+"/"dataset_name+extended_name+".py")
        
    return imp_mod, imp_mod_extended  
    
def write_to_csv(csv_file, config_mod, config_mod_ext):    

    
    writer = csv.writer(csv_file)

    
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

   
                     
    writer.writerow(feature_names+output_names)

           
    available_corners = imp_mod_extended.use_specified_corners
    
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
      
    multivalue_names = ['cell_rise_0', 
                        'cell_fall_0',
                        'rise_transition_0',
                        'fall_transition_0']
    singlevalue_names = ['write_rise_power_0',
                        'write_fall_power_0',
                        'read_rise_power_0',
                        'read_fall_power_0'] 
    file_name = openram_dir+"/"+dataset_name+data_file_ext
    try:
        f = open(file_name, "r")
    except IOError:
        print("Unable to open spice output file: {0}".format(file_name))
        return None
    print("Opened file",file_name)
    contents = f.read()
    f.close()                    
                        
    # Loop through corners, adding data for each corner    
    for (process, voltage, temp) in available_corners:    
        
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
                print("Error occurred while searching through datasheet: {}".format(file_name))
                return None

        # All the extracted values are delays but val[2] is the max delay
        feature_vals = [imp_mod.num_words, 
                        imp_mod.word_size,
                        imp_mod_extended.words_per_row,
                        imp_mod.local_array_size,
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

    
def get_comparison_data(openram_dir, out_dir):
    """Given an OpenRAM output dir, searches through datasheet files and ouputs
       a CSV files with data used in model."""

    # Get dataset name used by all the files e.g. sram_1b_16
    inp_mod, imp_mod_extended = get_config_mods(openram_dir)

    data_file = open("{}/sim_data.csv".format(out_dir), 'w', newline='')
    write_to_csv(data_file, inp_mod, imp_mod_extended)

    return out_dir
    

if __name__ == "__main__":
    tech = "scn4m_subm"
    dir = '/soe/hznichol/git_repos/PrivateRAM/compiler/path_test'
    dir = get_comparison_data(tech, dir)  
    print(dir)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
