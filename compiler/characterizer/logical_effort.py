import debug
from tech import drc, parameter, spice

class logical_effort():
    """
    Class to support the values behind logical effort. Useful for storing the different components
    such as logical effort, electrical effort, and parasitic delay.
    """
    beta = parameter["beta"]
    min_inv_cin = 1+beta
    pinv=parameter["min_inv_para_delay"]
    
    def __init__(self, size, cin, cout, parasitic, out_is_rise=True):
        self.cin = cin
        self.cout = cout
        self.logical_effort = (self.cin/size)/logical_effort.min_inv_cin
        self.eletrical_effort = self.cout/self.cin
        self.parasitic_scale = parasitic
        self.is_rise = out_is_rise
     
    def __str__(self):
        return "g=" + str(self.logical_effort) + ", h=" + str(self.eletrical_effort) + ", p=" + str(self.parasitic_scale)+"*pinv, rise_delay="+str(self.is_rise)
    
    def get_stage_effort(self):
        return  self.logical_effort*self.eletrical_effort
        
    def get_parasitic_delay(self, pinv):
        return pinv * self.parasitic_scale
    
    def get_stage_delay(self, pinv):
        return self.get_stage_effort()+self.get_parasitic_delay(pinv)
    
def calculate_relative_delay(stage_effort_list, pinv=parameter["min_inv_para_delay"]):
    """Calculates the total delay of a given delay path made of a list of logical effort objects."""
    total_rise_delay, total_fall_delay = calculate_relative_rise_fall_delays(stage_effort_list, pinv)
    return total_rise_delay + total_fall_delay
    
def calculate_relative_rise_fall_delays(stage_effort_list, pinv=parameter["min_inv_para_delay"]):
    """Calculates the rise/fall delays of a given delay path made of a list of logical effort objects."""
    debug.info(2, "Calculating rise/fall relative delays")
    total_rise_delay, total_fall_delay = 0,0
    for stage in stage_effort_list:
        debug.info(3, stage)
        if stage.is_rise:
            total_rise_delay += stage.get_stage_delay(pinv)
        else:
            total_fall_delay += stage.get_stage_delay(pinv)
    return total_rise_delay, total_fall_delay
   