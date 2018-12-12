import sys,re,shutil
import debug
import tech
import math
from .stimuli import *
from .trim_spice import *
from .charutils import *
import utils
from globals import OPTS
from .delay import delay

class bitline_delay(delay):
    """Functions to test for the worst case delay in a target SRAM

    The current worst case determines a feasible period for the SRAM then tests
    several bits and record the delay and differences between the bits.

    """

    def __init__(self, sram, spfile, corner):
        delay.__init__(self,sram,spfile,corner)
        self.period = tech.spice["feasible_period"]
        self.is_bitline_measure = True
    
    def create_measurement_names(self):
        """Create measurement names. The names themselves currently define the type of measurement"""
        #Altering the names will crash the characterizer. TODO: object orientated approach to the measurements.
        self.bitline_meas_names = ["bl_volt", "br_volt"]
    
    def write_delay_measures(self):
        """
        Write the measure statements to quantify the bitline voltage at sense amp enable 50%.
        """
        self.sf.write("\n* Measure statements for delay and power\n")

        # Output some comments to aid where cycles start and
        for comment in self.cycle_comments:
            self.sf.write("* {}\n".format(comment))
            
        for read_port in self.targ_read_ports:
           self.write_bitline_measures_read_port(read_port)       
           
    def write_bitline_measures_read_port(self, port):
        """
        Write the measure statements to quantify the delay and power results for a read port.
        """
        # add measure statements for delays/slews
        measure_bit = 0
        self.stim.gen_meas_find_voltage("bl_volt", "Xsram.s_en0", "Xsram.Xbank0.bl_{}".format(measure_bit), .5, "RISE", 3*self.period)
        self.stim.gen_meas_find_voltage("br_volt", "Xsram.s_en0", "Xsram.Xbank0.br_{}".format(measure_bit), .5, "RISE", 3*self.period)
    
    def gen_test_cycles_one_port(self, read_port, write_port):
        """Sets a list of key time-points [ns] of the waveform (each rising edge)
        of the cycles to do a timing evaluation of a single port """

        # Create the inverse address for a scratch address
        inverse_address = self.calculate_inverse_address()

        # For now, ignore data patterns and write ones or zeros
        data_ones = "1"*self.word_size
        data_zeros = "0"*self.word_size
        
        if self.t_current == 0:
            self.add_noop_all_ports("Idle cycle (no positive clock edge)",
                      inverse_address, data_zeros)
        
        self.add_write("W data 1 address {}".format(inverse_address),
                       inverse_address,data_ones,write_port) 

        self.add_write("W data 0 address {} to write value".format(self.probe_address),
                       self.probe_address,data_zeros,write_port)
        self.measure_cycles[write_port]["write0"] = len(self.cycle_times)-1
        
        # This also ensures we will have a H->L transition on the next read
        self.add_read("R data 1 address {} to set DOUT caps".format(inverse_address),
                      inverse_address,data_zeros,read_port) 

        self.add_read("R data 0 address {} to check W0 worked".format(self.probe_address),
                      self.probe_address,data_zeros,read_port)
    
    def run_delay_simulation(self):
        """
        This tries to simulate a period and checks if the result works. If
        so, it returns True and the delays, slews, and powers.  It
        works on the trimmed netlist by default, so powers do not
        include leakage of all cells.
        """
        #Sanity Check
        debug.check(self.period > 0, "Target simulation period non-positive") 
        
        result = [{} for i in self.all_ports]
        # Checking from not data_value to data_value
        self.write_delay_stimulus()

        self.stim.run_sim() #running sim prodoces spice output file.
          
        for port in self.targ_read_ports:  
            bitlines_meas_vals = {}
            for mname in self.bitline_meas_names:
                bitlines_meas_vals[mname] = parse_spice_list("timing", mname)
            #Check that power parsing worked.
            for name, val in bitlines_meas_vals.items():
                if type(val)!=float:
                    debug.error("Failed to Parse Bitline Values:\n\t\t{0}".format(bitlines_meas_vals),1) #Printing the entire dict looks bad.
            result[port].update(bitlines_meas_vals)
        
          
        # The delay is from the negative edge for our SRAM
        return (True,result)
    
    def analyze(self, probe_address, probe_data, slews, loads):
        """Measures the bitline swing of the differential bitlines (bl/br) at 50% s_en """
        self.set_probe(probe_address, probe_data)
        self.load=max(loads)
        self.slew=max(slews)
        
        port = 0
        bitline_swings = {}
        self.targ_read_ports = [self.read_ports[port]]
        self.targ_write_ports = [self.write_ports[port]]
        debug.info(1,"Bitline swing test: corner {}".format(self.corner))
        (success, results)=self.run_delay_simulation()
        debug.check(success, "Bitline Failed: period {}".format(self.period))
        for mname in self.bitline_meas_names:
            bitline_swings[mname] = results[port][mname]
        debug.info(1,"Bitline values (bl/br): {}".format(bitline_swings))
        return bitline_swings

        
    
