# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os
import re
from enum import Enum
from openram import debug
from openram import OPTS


def relative_compare(value1, value2, error_tolerance=0.001):
    """ This is used to compare relative values for convergence. """
    return (abs(value1 - value2) / abs(max(value1, value2)) <= error_tolerance)


def parse_spice_list(filename, key):
    """Parses a hspice output.lis file for a key value"""

    lower_key = key.lower()

    if OPTS.spice_name == "xa" :
        # customsim has a different output file name
        full_filename="{0}xa.meas".format(OPTS.openram_temp)
    elif OPTS.spice_name == "spectre":
        full_filename = os.path.join(OPTS.openram_temp, "delay_stim.measure")
    elif OPTS.spice_name in ["Xyce", "xyce"]:
        full_filename = os.path.join(OPTS.openram_temp, "spice_stdout.log")
    else:
        # ngspice/hspice using a .lis file
        full_filename = "{0}{1}.lis".format(OPTS.openram_temp, filename)

    try:
        f = open(full_filename, "r")
    except IOError:
        debug.error("Unable to open spice output file: {0}".format(full_filename),1)
        debug.archive()

    contents = f.read().lower()
    f.close()
    # val = re.search(r"{0}\s*=\s*(-?\d+.?\d*\S*)\s+.*".format(key), contents)
    val = re.search(r"{0}\s*=\s*(-?\d+.?\d*[e]?[-+]?[0-9]*\S*)\s+.*".format(lower_key), contents)
    if val != None:
        debug.info(4, "Key = " + lower_key + " Val = " + val.group(1))
        return convert_to_float(val.group(1))
    else:
        return "Failed"


def round_time(time, time_precision=3):
    # times are in ns, so this is how many digits of precision
    # 3 digits = 1ps
    # 4 digits = 0.1ps
    # etc.
    return round(time, time_precision)


def round_voltage(voltage, voltage_precision=5):
    # voltages are in volts
    # 3 digits = 1mv
    # 4 digits = 0.1mv
    # 5 digits = 0.01mv
    # 6 digits = 1uv
    # etc
    return round(voltage, voltage_precision)


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


def check_dict_values_is_float(dict):
    """Checks if all the values are floats. Useful for checking failed Spice measurements."""
    for key, value in dict.items():
        if type(value)!=float:
            return False
    return True


def bidir_search(func, upper, lower, time_out=9):
    """
    Performs bidirectional search over given function with given
    upper and lower bounds.
    """
    time_count = 0
    while time_count < time_out:
        val = (upper + lower) / 2
        if func(val):
            return (True, val)
        time_count += 1
    return (False, 0)


class bit_polarity(Enum):
    NONINVERTING = 0
    INVERTING = 1


class sram_op(Enum):
    READ_ZERO = 0
    READ_ONE = 1
    WRITE_ZERO = 2
    WRITE_ONE = 3
    DISABLED_READ_ZERO = 4
    DISABLED_READ_ONE = 5
    DISABLED_WRITE_ZERO = 6
    DISABLED_WRITE_ONE = 7
