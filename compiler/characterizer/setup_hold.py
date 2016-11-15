import sys
import globals
import tech
import stimuli
import debug
import charutils as ch
import ms_flop

OPTS = globals.get_opts()

vdd = tech.spice["supply_voltage"]
gnd = tech.spice["gnd_voltage"]


class setup_hold():
    """
    Functions to calculate the setup and hold times of the SRAM
    (Bisection Methodology)
    """

    def __init__(self):
        # This must match the spice model order
        self.pins = ["data_buf", "dout", "dout_bar", "clk_buf", "vdd", "gnd"]
        self.output_name = "dout"
        self.model_name = "ms_flop"
        self.model_location = OPTS.openram_tech + "sp_lib/ms_flop.sp"


    def check_arguments(self, correct_value, period):
        """Checks if given arguments for write_stimulus() meets requirements"""
        if not isinstance(correct_value, float):
            if not isinstance(correct_value, int):
                debug.error("Given correct_value is not a valid number",1)
                
        if not isinstance(period, float):
            if not isinstance(period, int):
                debug.error("Given period is not a valid number",1)


    def write_stimulus(self, mode, target_time, correct_value, period, noise_margin):
        """Creates a stimulus file for SRAM setup/hold time calculation"""
        self.check_arguments(correct_value,period)

        # creates and opens the stimulus file for writing
        temp_stim = OPTS.openram_temp + "stim.sp"
        self.sf = open(temp_stim, "w")

        self.write_header(correct_value, period)

        # instantiate the master-slave d-flip-flop
        self.sf.write("* Instantiation of the Master-Slave D-flip-flop\n")
        stimuli.inst_model(stim_file=self.sf,
                           pins=self.pins,
                           model_name=self.model_name)
        self.sf.write("\n")

        # create a buffer for the inputs
        self.sf.write("* Buffer subckt\n")
        stimuli.create_buffer(stim_file=self.sf,
                              buffer_name="buffer",
                              size=[1, 1])
        self.sf.write("\n")

        self.write_data(mode=mode,
                        target_time=target_time,
                        period=period,
                        correct_value=correct_value)

        self.write_clock(period)

        self.write_measures(mode=mode, 
                            correct_value=correct_value,
                            noise_margin=noise_margin, 
                            period=period)

        self.write_control(period=period)

        self.sf.close()

    def write_header(self, correct_value, period):
        """ Write the header file with all the models and the power supplies. """
        self.sf.write("* Stimulus for setup/hold: data {0} period {1}n\n".format(correct_value, period))
        self.sf.write("\n")

        # include files in stimulus file
        self.model_list = tech.spice["fet_models"] + [self.model_location]
        stimuli.write_include(stim_file=self.sf,
                              models=self.model_list)
        self.sf.write("\n")

        # add vdd/gnd statements
        self.sf.write("* Global Power Supplies\n")
        stimuli.write_supply(stim_file=self.sf,
                             vdd_name=tech.spice["vdd_name"],
                             gnd_name=tech.spice["gnd_name"],
                             vdd_voltage=vdd,
                             gnd_voltage=gnd)
        self.sf.write("\n")


    def write_data(self, mode, period, target_time, correct_value):
        """ Create the buffered data signals for setup/hold analysis """
        self.sf.write("* Buffer for the DATA signal\n")
        stimuli.add_buffer(stim_file=self.sf,
                           buffer_name="buffer",
                           signal_list=["DATA"])
        self.sf.write("* Generation of the data and clk signals\n")
        incorrect_value = stimuli.get_inverse_value(correct_value)
        if mode=="HOLD":
            start_value = correct_value
            end_value = incorrect_value
        else:
            start_value = incorrect_value
            end_value = correct_value

        stimuli.gen_pulse(stim_file=self.sf,
                          sig_name="DATA",
                          v1=start_value,
                          v2=end_value,
                          offset=target_time,
                          period=2*period,
                          t_rise=tech.spice["rise_time"],
                          t_fall=tech.spice["fall_time"])
        self.sf.write("\n")

    def write_clock(self,period):
        """ Create the buffered clock signal for setup/hold analysis """
        self.sf.write("* Buffer for the clk signal\n")
        stimuli.add_buffer(stim_file=self.sf,
                           buffer_name="buffer",
                           signal_list=["clk"])
        self.sf.write("\n")
        stimuli.gen_pulse(stim_file=self.sf,
                          sig_name="clk",
                          offset=period,
                          period=period,
                          t_rise=tech.spice["rise_time"],
                          t_fall=tech.spice["fall_time"])
        self.sf.write("\n")


    def write_measures(self, mode, correct_value, noise_margin, period):
        """ Measure statements for setup/hold with right phases. """

        if correct_value == vdd:
            max_or_min = "MAX"
            rise_or_fall = "RISE"
        else:
            max_or_min = "MIN"
            rise_or_fall = "FALL"

        incorrect_value = stimuli.get_inverse_value(correct_value)

        self.sf.write("* Measure statements for pass/fail verification\n")
        self.sf.write(".IC v({0})={1}\n".format(self.output_name, incorrect_value))
        #self.sf.write(".MEASURE TRAN {0}VOUT {0} v({1}) GOAL={2}\n".format(max_or_min, output_name, noise_margin))
        # above is the old cmd for hspice, below is the one work for both
        self.sf.write(".MEASURE TRAN {0}VOUT {0} v({1}) from ={2}n to ={3}n\n".format(max_or_min,
                                                                                      self.output_name,
                                                                                      1.5*period,
                                                                                      2*period))
        self.sf.write("\n")


    def write_control(self, period):
        # transient window
        end_time = 2 * period
        self.sf.write(".TRAN 5p {0}n\n".format(end_time))
        self.sf.write(".OPTIONS POST=1 PROBE\n")
        # create plots for all signals
        self.sf.write(".probe V(*)\n")
        # end the stimulus file
        self.sf.write(".end\n")

    def bidir_search(self, correct_value, noise_margin, measure_name, mode):
        """ This will perform a bidirectional search for either setup or hold times.
        It starts with the feasible priod and looks a half period beyond or before it
        depending on whether we are doing setup or hold. 
        """
        period = tech.spice["feasible_period"]
        debug.info(2,"Feasible period from technology file: {0} ".format(period))
                   
        
        # The clock will start being offset by a period, so we want to look before and after
        # this time by half a period. 
        if mode == "HOLD":
            target_time = 1.5 * period
            lower_bound = 0.5*period
            upper_bound = 1.5 * period
        else:
            target_time = 0.5 * period
            lower_bound = 0.5 * period
            upper_bound = 1.5*period

        previous_time = target_time
        # Initial Check if reference setup time passes for correct_value 
        self.write_stimulus(mode=mode, 
                            target_time=target_time, 
                            correct_value=correct_value, 
                            period=period, 
                            noise_margin=noise_margin)
        stimuli.run_sim()
        output_value = ch.convert_to_float(ch.parse_output("timing", measure_name))
        debug.info(3,"Correct: {0} Output: {1} NM: {2}".format(correct_value,output_value,noise_margin))
        if mode == "HOLD":
            setuphold_time = target_time - period
        else:
            setuphold_time = period - target_time
        debug.info(2,"Checked initial {0} time {1}, data at {2}, clock at {3} ".format(mode,setuphold_time,
                                                                                       target_time,period))
        debug.info(3,"Target time: {0} Low: {1} Up: {2} Measured: {3}".format(target_time,
                                                                              lower_bound,
                                                                              upper_bound,
                                                                              setuphold_time))
        if not self.pass_fail_test(output_value, correct_value, noise_margin):
            debug.error("Initial period/target hold time fails for data value",2)

        # We already found it feasible, so advance one step first thing.
        debug.info(2,"Performing bidir search on {3} time: {2} LB: {0} UB: {1} ".format(lower_bound,
                                                                                        upper_bound,
                                                                                        setuphold_time,
                                                                                        mode))
        if mode == "HOLD":
            target_time -= 0.5 * (upper_bound - lower_bound)
        else:
            target_time += 0.5 * (upper_bound - lower_bound)
        while True:
            self.write_stimulus(mode=mode, 
                                target_time=target_time, 
                                correct_value=correct_value, 
                                period=period, 
                                noise_margin=noise_margin)
            if mode == "HOLD":
                setuphold_time = target_time - period
            else:
                setuphold_time = period - target_time
            debug.info(3,"Target time: {0} Low: {1} Up: {2} Measured: {3}".format(target_time,
                                                                                  lower_bound,
                                                                                  upper_bound,
                                                                                  setuphold_time))

            stimuli.run_sim()
            output_value = ch.convert_to_float(ch.parse_output("timing", measure_name))
            debug.info(3,"Correct: {0} Output: {1} NM: {2}".format(correct_value,output_value,noise_margin))
            if self.pass_fail_test(output_value,correct_value,noise_margin):
                debug.info(3,"PASS")
                if ch.relative_compare(target_time, previous_time):
                    debug.info(3,"CONVERGE " + str(target_time) + " " + str(previous_time))
                    break
                previous_time = target_time
                if mode == "HOLD":
                    upper_bound = target_time
                    target_time -= 0.5 * (upper_bound - lower_bound)
                else:
                    lower_bound = target_time
                    target_time += 0.5 * (upper_bound - lower_bound)
            else:
                debug.info(3,"FAIL")
                if mode == "HOLD":
                    lower_bound = target_time
                    target_time += 0.5 * (upper_bound - lower_bound)
                else:
                    upper_bound = target_time
                    target_time -= 0.5 * (upper_bound - lower_bound)
            #raw_input("Press Enter to continue...")
            # the clock starts offset by one clock period, 
            # so we always measure our setup or hold relative to this time
            if mode == "HOLD":
                setuphold_time = target_time - period
            else:
                setuphold_time = period - target_time

        debug.info(2,"Converged on {0} time {1}, data at {2}, clock at {3}.".format(mode,setuphold_time,target_time,period))
        return setuphold_time


    def setup_time(self):
        """Calculates the setup time for low-to-high and high-to-low
        transition for a D-flip-flop"""

        one_found = self.bidir_search(vdd, 0.9*vdd, "maxvout", "SETUP")

        zero_found = self.bidir_search(gnd, 0.1*vdd, "minvout", "SETUP")

        return [one_found, zero_found]

    def hold_time(self):
        """Calculates the hold time for low-to-high and high-to-low
        transition for a D-flip-flop"""

        one_found = self.bidir_search(vdd, 0.9*vdd, "maxvout", "HOLD")

        zero_found = self.bidir_search(gnd, 0.1*vdd, "minvout", "HOLD")

        return [one_found, zero_found]


    def pass_fail_test(self,value,correct_value,noise_margin):
        """Function to Test if the output value reached the
        noise_margin to determine if it passed or failed"""
        if correct_value == vdd:
            return True if value >= noise_margin else False
        else:
            return True if value <= noise_margin else False




    def analyze(self):
        """main function to calculate both setup and hold time for the
        d-flip-flop returns a dictionary that contains 4 times for both
        setup/hold times for high_to_low and low_to_high transition
        dictionary keys: setup_time_one (low_to_high), setup_time_zero
        (high_to_low), hold_time_one (low_to_high), hold_time_zero
        (high_to_low)
        """

        [one_setup_time, zero_setup_time] = self.setup_time()
        [one_hold_time, zero_hold_time] = self.hold_time()
        debug.info(1, "Setup Time for low_to_high transistion: {0}".format(one_setup_time))
        debug.info(1, "Setup Time for high_to_low transistion: {0}".format(zero_setup_time))
        debug.info(1, "Hold Time for low_to_high transistion: {0}".format(one_hold_time))
        debug.info(1, "Hold Time for high_to_low transistion: {0}".format(zero_hold_time))
        times = {"setup_time_one": one_setup_time,
                 "setup_time_zero": zero_setup_time,
                 "hold_time_one": one_hold_time,
                 "hold_time_zero": zero_hold_time
                 }
        return times

