# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import sys
import tech
from .stimuli import *
import debug
from .charutils import *
import dff
from globals import OPTS


class setup_hold():
    """
    Functions to calculate the setup and hold times of the SRAM
    (Bisection Methodology)
    """

    def __init__(self, corner):
        # This must match the spice model order
        self.pins = ["data", "dout", "clk", "vdd", "gnd"]
        self.model_name = "dff"
        self.model_location = OPTS.openram_tech + "sp_lib/dff.sp"
        self.period = tech.spice["feasible_period"]

        debug.info(2,"Feasible period from technology file: {0} ".format(self.period))

        self.set_corner(corner)

                
    def set_corner(self,corner):
        """ Set the corner values """
        self.corner = corner
        (self.process, self.vdd_voltage, self.temperature) = corner
        self.gnd_voltage = 0


    def write_stimulus(self, mode, target_time, correct_value):
        """Creates a stimulus file for SRAM setup/hold time calculation"""

        # creates and opens the stimulus file for writing
        temp_stim = OPTS.openram_temp + "stim.sp"
        self.sf = open(temp_stim, "w")
        self.stim = stimuli(self.sf, self.corner)

        self.write_header(correct_value)

        # instantiate the master-slave d-flip-flop
        self.sf.write("\n* Instantiation of the Master-Slave D-flip-flop\n")
        self.stim.inst_model(pins=self.pins,
                             model_name=self.model_name)

        self.write_data(mode=mode,
                        target_time=target_time,
                        correct_value=correct_value)

        self.write_clock()

        self.write_measures(mode=mode, 
                            correct_value=correct_value)
                         

        self.stim.write_control(4*self.period)

        self.sf.close()

    def write_header(self, correct_value):
        """ Write the header file with all the models and the power supplies. """
        self.sf.write("\n* Stimulus for setup/hold: data {0} period {1}n\n".format(correct_value, self.period))

        # include files in stimulus file
        self.stim.write_include(self.model_location)

        # add vdd/gnd statements
        self.sf.write("\n* Global Power Supplies\n")
        self.stim.write_supply()


    def write_data(self, mode, target_time, correct_value):
        """Create the data signals for setup/hold analysis. First period is to
        initialize it to the opposite polarity. Second period is used for
        characterization.

        """
        self.sf.write("\n* Generation of the data and clk signals\n")
        incorrect_value = self.stim.get_inverse_value(correct_value)
        if mode=="HOLD":
            init_value = incorrect_value
            start_value = correct_value
            end_value = incorrect_value
        else:
            init_value = incorrect_value
            start_value = incorrect_value
            end_value = correct_value

        self.stim.gen_pwl(sig_name="data",
                          clk_times=[0, self.period, target_time],
                          data_values=[init_value, start_value, end_value],
                          period=target_time,
                          slew=self.constrained_input_slew,
                          setup=0)        

    def write_clock(self):
        """ Create the clock signal for setup/hold analysis. First period initializes the FF
        while the second is used for characterization."""
        
        self.stim.gen_pwl(sig_name="clk",
                          # initial clk edge is right after the 0 time to initialize a flop 
                          # without using .IC on an internal node.
                          # Return input to value after one period.
                          # The second pulse is the characterization one at 2*period
                          clk_times=[0, 0.1*self.period,self.period,2*self.period],
                          data_values=[0, 1, 0, 1],
                          period=2*self.period,
                          slew=self.constrained_input_slew,
                          setup=0)        



    def write_measures(self, mode, correct_value):
        """ Measure statements for setup/hold with right phases. """

        if correct_value == 1:
            dout_rise_or_fall = "RISE"
        else:
            dout_rise_or_fall = "FALL"

        # in SETUP mode, the input mirrors what the output should be
        if mode == "SETUP":
            din_rise_or_fall = dout_rise_or_fall
        else:
            # in HOLD mode, however, the input should be opposite of the output
            if correct_value == 1:
                din_rise_or_fall = "FALL"
            else:
                din_rise_or_fall = "RISE"


        self.sf.write("\n* Measure statements for pass/fail verification\n")
        trig_name = "clk"
        targ_name = "dout"
        trig_val = targ_val = 0.5 * self.vdd_voltage
        # Start triggers right before the clock edge at 2*period
        self.stim.gen_meas_delay(meas_name="clk2q_delay",
                                 trig_name=trig_name,
                                 targ_name=targ_name,
                                 trig_val=trig_val,
                                 targ_val=targ_val,
                                 trig_dir="RISE",
                                 targ_dir=dout_rise_or_fall,
                                 trig_td=1.9*self.period,
                                 targ_td=1.9*self.period)
        
        targ_name = "data"
        # Start triggers right after initialize value is returned to normal
        # at one period
        self.stim.gen_meas_delay(meas_name="setup_hold_time",
                                 trig_name=trig_name,
                                 targ_name=targ_name,
                                 trig_val=trig_val,
                                 targ_val=targ_val,
                                 trig_dir="RISE",
                                 targ_dir=din_rise_or_fall,
                                 trig_td=1.2*self.period,
                                 targ_td=1.2*self.period)
        



    def bidir_search(self, correct_value, mode):
        """ This will perform a bidirectional search for either setup or hold times.
        It starts with the feasible priod and looks a half period beyond or before it
        depending on whether we are doing setup or hold. 
        """

        # NOTE: The feasible bound is always feasible. This is why they are different for setup and hold.
        # The clock will always be offset by 2*period from the start, so we want to look before and after
        # this time. They are also unbalanced so that the average won't be right on the clock edge in the
        # first iteration.
        if mode == "SETUP":
            feasible_bound = 1.25*self.period
            infeasible_bound = 2.5*self.period
        else:
            infeasible_bound = 1.5*self.period
            feasible_bound = 2.75*self.period

        # Initial check if reference feasible bound time passes for correct_value, if not, we can't start the search!
        self.write_stimulus(mode=mode, 
                            target_time=feasible_bound, 
                            correct_value=correct_value)
        self.stim.run_sim()
        ideal_clk_to_q = convert_to_float(parse_spice_list("timing", "clk2q_delay"))
        setuphold_time = convert_to_float(parse_spice_list("timing", "setup_hold_time"))
        debug.info(2,"*** {0} CHECK: {1} Ideal Clk-to-Q: {2} Setup/Hold: {3}".format(mode, correct_value,ideal_clk_to_q,setuphold_time))

        if type(ideal_clk_to_q)!=float or type(setuphold_time)!=float:
            debug.error("Initial hold time fails for data value feasible bound {0} Clk-to-Q {1} Setup/Hold {2}".format(feasible_bound,ideal_clk_to_q,setuphold_time),2)

        if mode == "SETUP": # SETUP is clk-din, not din-clk
            setuphold_time *= -1e9
        else:
            setuphold_time *= 1e9
            
        passing_setuphold_time = setuphold_time
        debug.info(2,"Checked initial {0} time {1}, data at {2}, clock at {3} ".format(mode,
                                                                                       setuphold_time,
                                                                                       feasible_bound,
                                                                                       2*self.period))
        #raw_input("Press Enter to continue...")
            
        while True:
            target_time = (feasible_bound + infeasible_bound)/2
            self.write_stimulus(mode=mode, 
                                target_time=target_time, 
                                correct_value=correct_value)

            debug.info(2,"{0} value: {1} Target time: {2} Infeasible: {3} Feasible: {4}".format(mode,
                                                                                                correct_value,
                                                                                                target_time,
                                                                                                infeasible_bound,
                                                                                                feasible_bound))


            self.stim.run_sim()
            clk_to_q = convert_to_float(parse_spice_list("timing", "clk2q_delay"))
            setuphold_time = convert_to_float(parse_spice_list("timing", "setup_hold_time"))
            if type(clk_to_q)==float and (clk_to_q<1.1*ideal_clk_to_q) and type(setuphold_time)==float:
                if mode == "SETUP": # SETUP is clk-din, not din-clk
                    setuphold_time *= -1e9
                else:
                    setuphold_time *= 1e9

                debug.info(2,"PASS Clk-to-Q: {0} Setup/Hold: {1}".format(clk_to_q,setuphold_time))
                passing_setuphold_time = setuphold_time
                feasible_bound = target_time
            else:
                debug.info(2,"FAIL Clk-to-Q: {0} Setup/Hold: {1}".format(clk_to_q,setuphold_time))
                infeasible_bound = target_time

            #raw_input("Press Enter to continue...")
            if relative_compare(feasible_bound, infeasible_bound, error_tolerance=0.001):
                debug.info(3,"CONVERGE {0} vs {1}".format(feasible_bound,infeasible_bound))
                break
            

        debug.info(2,"Converged on {0} time {1}.".format(mode,passing_setuphold_time))
        return passing_setuphold_time


    def setup_LH_time(self):
        """Calculates the setup time for low-to-high transition for a DFF
        """
        return self.bidir_search(1, "SETUP")


    def setup_HL_time(self):
        """Calculates the setup time for high-to-low transition for a DFF
        """
        return self.bidir_search(0, "SETUP")
    
    def hold_LH_time(self):
        """Calculates the hold time for low-to-high transition for a DFF
        """
        return self.bidir_search(1, "HOLD")

    def hold_HL_time(self):
        """Calculates the hold time for high-to-low transition for a DFF
        """
        return self.bidir_search(0, "HOLD")


    def analyze(self, related_slews, constrained_slews):
        """main function to calculate both setup and hold time for the
        DFF and returns a dictionary that contains 4 lists for both
        setup/hold times for high_to_low and low_to_high transitions
        for all the slew combinations of the data and clock.
        """
        LH_setup = []
        HL_setup = []
        LH_hold = []
        HL_hold = []
        
        #For debugging, skips characterization and returns dummy values.
        # i = 1.0
        # for self.related_input_slew in related_slews:
            # for self.constrained_input_slew in constrained_slews:
                # LH_setup.append(i)
                # HL_setup.append(i+1.0)
                # LH_hold.append(i+2.0)
                # HL_hold.append(i+3.0)
                # i+=4.0
                
        # times = {"setup_times_LH": LH_setup,
                 # "setup_times_HL": HL_setup,
                 # "hold_times_LH": LH_hold,
                 # "hold_times_HL": HL_hold
                 # }
        # return times
        
        
        for self.related_input_slew in related_slews:
            for self.constrained_input_slew in constrained_slews:
                debug.info(1, "Clock slew: {0} Data slew: {1}".format(self.related_input_slew,self.constrained_input_slew))
                LH_setup_time = self.setup_LH_time()
                debug.info(1, "  Setup Time for low_to_high transition: {0}".format(LH_setup_time))
                HL_setup_time = self.setup_HL_time()
                debug.info(1, "  Setup Time for high_to_low transition: {0}".format(HL_setup_time))
                LH_hold_time = self.hold_LH_time()
                debug.info(1, "  Hold Time for low_to_high transition: {0}".format(LH_hold_time))
                HL_hold_time = self.hold_HL_time()
                debug.info(1, "  Hold Time for high_to_low transition: {0}".format(HL_hold_time))
                LH_setup.append(LH_setup_time)
                HL_setup.append(HL_setup_time)
                LH_hold.append(LH_hold_time)
                HL_hold.append(HL_hold_time)
                
        times = {"setup_times_LH": LH_setup,
                 "setup_times_HL": HL_setup,
                 "hold_times_LH": LH_hold,
                 "hold_times_HL": HL_hold
                 }
        return times

    def analytical_setuphold(self,related_slews, constrained_slews):
        """ Just return the fixed setup/hold times from the technology.
        """
        LH_setup = []
        HL_setup = []
        LH_hold = []
        HL_hold = []
        
        for self.related_input_slew in related_slews:
            for self.constrained_input_slew in constrained_slews:
                # convert from ps to ns
                LH_setup.append(tech.spice["msflop_setup"]/1e3)
                HL_setup.append(tech.spice["msflop_setup"]/1e3)
                LH_hold.append(tech.spice["msflop_hold"]/1e3)
                HL_hold.append(tech.spice["msflop_hold"]/1e3)
                
        times = {"setup_times_LH": LH_setup,
                 "setup_times_HL": HL_setup,
                 "hold_times_LH": LH_hold,
                 "hold_times_HL": HL_hold
                 }
        return times
