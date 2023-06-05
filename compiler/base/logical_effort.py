# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.tech import parameter


class logical_effort():
    """
    Class to support the values behind logical effort. Useful for storing the different components
    such as logical effort, electrical effort, and parasitic delay.
    """
    beta = parameter["beta"]
    min_inv_cin = 1+beta
    pinv=parameter["min_inv_para_delay"]
    tau = parameter['le_tau']

    def __init__(self, name, size, cin, cout, parasitic, out_is_rise=True):
        self.name = name
        self.cin = cin
        self.cout = cout
        self.logical_effort = (self.cin/size)/logical_effort.min_inv_cin
        self.electrical_effort = self.cout/self.cin
        self.parasitic_scale = parasitic
        self.is_rise = out_is_rise

    def __str__(self):
        return  "Name={}, g={}, h={}, p={}*pinv, rise_delay={}".format(self.name,
                                                                       self.logical_effort,
                                                                       self.electrical_effort,
                                                                       self.parasitic_scale,
                                                                       self.is_rise
                                                                       )

    def get_stage_effort(self):
        return  self.logical_effort*self.electrical_effort

    def get_parasitic_delay(self):
        return logical_effort.pinv*self.parasitic_scale

    def get_stage_delay(self):
        return self.get_stage_effort()+self.get_parasitic_delay()

    def get_absolute_delay(self):
        return logical_effort.tau*self.get_stage_delay()

def calculate_delays(stage_effort_list):
    """Convert stage effort objects to list of delay values"""
    return [stage.get_stage_delay() for stage in stage_effort_list]

def calculate_relative_delay(stage_effort_list):
    """Calculates the total delay of a given delay path made of a list of logical effort objects."""
    total_rise_delay, total_fall_delay = calculate_relative_rise_fall_delays(stage_effort_list)
    return total_rise_delay + total_fall_delay

def calculate_absolute_delay(stage_effort_list):
    """Calculates the total delay of a given delay path made of a list of logical effort objects."""
    total_delay = 0
    for stage in stage_effort_list:
        total_delay+=stage.get_absolute_delay()
    return total_delay

def calculate_relative_rise_fall_delays(stage_effort_list):
    """Calculates the rise/fall delays of a given delay path made of a list of logical effort objects."""
    debug.info(2, "Calculating rise/fall relative delays")
    total_rise_delay, total_fall_delay = 0,0
    for stage in stage_effort_list:
        debug.info(2, stage)
        if stage.is_rise:
            total_rise_delay += stage.get_stage_delay()
        else:
            total_fall_delay += stage.get_stage_delay()
    return total_rise_delay, total_fall_delay

def convert_farad_to_relative_c(c_farad):
    """Converts capacitance in Femto-Farads to relative capacitance."""
    return c_farad*parameter['cap_relative_per_ff']

def convert_relative_c_to_farad(c_relative):
    """Converts capacitance in logical effort relative units to Femto-Farads."""
    return c_relative/parameter['cap_relative_per_ff']
