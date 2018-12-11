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
        self.period = 1
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
        for dname in self.delay_meas_names:
            meas_values = self.get_delay_meas_values(dname, port)
            self.stim.gen_meas_delay(*meas_values)
    
    
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

        
    
