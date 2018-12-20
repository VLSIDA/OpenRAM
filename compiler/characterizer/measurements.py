import debug
from tech import drc, parameter, spice
from abc import ABC, abstractmethod
from .stimuli import *

class spice_measurement(ABC):
    """Base class for spice stimulus measurements."""
    def __init__(self, measure_name):
        #Names must be unique for correct spice simulation, but not enforced here.
        self.name = measure_name

    @abstractmethod
    def get_measure_function(self):
        return None    
        
    @abstractmethod
    def get_measure_values(self):
        return None
        
    def write_measure(self, stim_obj, input_tuple):
        measure_func = self.get_measure_function()
        if measure_func == None:
            debug.error("Did not set measure function",1)
        measure_vals = self.get_measure_values(*input_tuple)
        measure_func(stim_obj, *measure_vals)
       
           
class delay_measure(spice_measurement):
    """Generates a spice measurement for the delay of 50%-to-50% points of two signals."""
    
    def __init__(self, measure_name, trig_name, targ_name, trig_dir_str, targ_dir_str):
        spice_measurement.__init__(self, measure_name)
        self.set_meas_constants(trig_name, targ_name, trig_dir_str, targ_dir_str)
    
    def get_measure_function(self):
        return stimuli.gen_meas_delay
    
    def set_meas_constants(self, trig_name, targ_name, trig_dir_str, targ_dir_str):
        """Set the values needed to generate a Spice measurement statement based on the name of the measurement."""
        self.trig_dir_str = trig_dir_str
        self.targ_dir_str = targ_dir_str
        
        self.trig_val_of_vdd = 0.5 
        self.targ_val_of_vdd = 0.5
        
        self.trig_name_no_port = trig_name
        self.targ_name_no_port = targ_name
        
        #Time delays and ports are variant and needed as inputs when writing the measurement
        
    def get_measure_values(self, trig_td, targ_td, vdd_voltage, port=None):    
        """Constructs inputs to stimulus measurement function. Variant values are inputs here."""
        trig_val = self.trig_val_of_vdd * vdd_voltage
        targ_val = self.targ_val_of_vdd * vdd_voltage
        
        if port != None:
            meas_name = self.name.format(port)
            trig_name = self.trig_name_no_port.format(port)
            targ_name = self.targ_name_no_port.format(port)
        else:
            meas_name = self.name
            trig_name = self.trig_name_no_port
            targ_name = self.targ_name_no_port

        return (meas_name,trig_name,targ_name,trig_val,targ_val,self.trig_dir_str,self.targ_dir_str,trig_td,targ_td)            
 
 
class slew_measure(delay_measure):        
    
    def __init__(self, measure_name, signal_name, slew_dir_str):
        spice_measurement.__init__(self, measure_name)
        self.set_meas_constants(signal_name, slew_dir_str)
    
    def set_meas_constants(self, signal_name, slew_dir_str):
        """Set the values needed to generate a Spice measurement statement based on the name of the measurement."""
        self.trig_dir_str = slew_dir_str
        self.targ_dir_str = slew_dir_str
        
        if slew_dir_str == "RISE":
            self.trig_val_of_vdd = 0.1 
            self.targ_val_of_vdd = 0.9
        elif slew_dir_str == "FALL":
            self.trig_val_of_vdd = 0.9 
            self.targ_val_of_vdd = 0.1
        else:
            debug.error("Unrecognised slew measurement direction={}".format(slew_dir_str),1)
        
        self.trig_name_no_port = signal_name
        self.targ_name_no_port = signal_name
        
        #Time delays and ports are variant and needed as inputs when writing the measurement 
 