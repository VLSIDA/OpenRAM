import globals
import re
import debug

OPTS = globals.get_opts()

# 0.1% is the relative tolerance for convergence
error_tolerance = 0.001 

# times are in ns, so this is how many digits of precision
# 3 digits = 1ps
# 4 digits = 0.1ps
# etc.
time_precision = 3
# voltages are in volts
# 3 digits = 1mv
# 4 digits = 0.1mv
# 5 digits = 0.01mv
# 6 digits = 1uv
# etc
voltage_precision = 5
        
def relative_compare(value1,value2):
    """ This is used to compare relative values for convergence. """
    return (abs(value1 - value2) / max(value1,value2) <= error_tolerance)


def parse_output(filename, key):
    """Parses a hspice output.lis file for a key value"""
    full_filename="{0}{1}.lis".format(OPTS.openram_temp, filename)
    try:
        f = open(full_filename, "r")
    except IOError:
        debug.error("Unable to open spice output file: {0}".format(full_filename),1)
    contents = f.read()
    val = re.search(r"{0}\s*=\s*(-?\d+.?\d*\S*)\s+.*".format(key), contents)
    if val != None:
        debug.info(3, "Key = " + key + " Val = " + val.group(1))
        return val.group(1)
    else:
        return "Failed"
    
def round_time(time):
    return round(time,time_precision)

def round_voltage(voltage):
    return round(voltage,voltage_precision)

def convert_to_float(number):
    """Converts a string into a (float) number; also converts units(m,u,n,p)"""
    if number == "Failed":
        return False
    
    # start out with a binary value
    float_value = False
    try:  
        # checks if string is a float without letter units
        float_value = float(number)
    except ValueError:
        # see if it is in scientific notation
        unit = re.search(r"(-?\d+\.?\d*)e(\-?\+?\d+)", number)
        if unit != None:
            float_value=float(unit.group(1)) * (10 ^ float(unit.group(2)))
            
        # see if it is in spice notation
        unit = re.search(r"(-?\d+\.?\d*)(m?u?n?p?f?)", number)
        if unit != None:
            float_value = {
                'm': lambda x: x * 0.001,  # milli
                'u': lambda x: x * 0.000001,  # micro
                'n': lambda x: x * 0.000000001,  # nano
                'p': lambda x: x * 0.000000000001,  # pico
                'f': lambda x: x * 0.000000000000001  # femto
                }[unit.group(2)](float(unit.group(1)))

    # if we weren't able to convert it to a float then error out
    if not type(float_value)==float:
        debug.error("Invalid number: {0}".format(number),1)

    return float_value
