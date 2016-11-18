"""
This file generates the test structure and stimulus for an sram
simulation.  There are various functions that can be be used to
generate stimulus for other simulations as well.
"""

import globals
import tech
import debug
import subprocess
import os
import sys

OPTS = globals.get_opts()

vdd = tech.spice["supply_voltage"]
gnd = tech.spice["gnd_voltage"]
vdd_name = tech.spice["vdd_name"]
gnd_name = tech.spice["gnd_name"]
pmos_name = tech.spice["pmos_name"]
nmos_name = tech.spice["nmos_name"]
tx_width = tech.spice["minwidth_tx"]
tx_length = tech.spice["channel"]

def inst_sram(stim_file, abits, dbits, sram_name):
    """function to instatiate the sram subckt"""
    stim_file.write("Xsram ")
    for i in range(dbits):
        stim_file.write("DATA[{0}] ".format(i))
    for i in range(abits):
        stim_file.write("A[{0}]_buf ".format(i))
    for i in tech.spice["control_signals"]:
        stim_file.write("{0}_buf ".format(i))
    stim_file.write("{0}_buf_buf ".format(tech.spice["clk"]))
    stim_file.write("{0} {1} ".format(vdd_name, gnd_name))
    stim_file.write("{0}\n".format(sram_name))


def inst_model(stim_file, pins, model_name):
    """function to instantiate a model"""
    stim_file.write("X{0} ".format(model_name))
    for pin in pins:
        stim_file.write("{0} ".format(pin))
    stim_file.write("{0}\n".format(model_name))


def create_inverter(stim_file, size=1, beta=2.5):
    """Generates inverter for the top level signals (only for sim purposes)"""
    stim_file.write(".SUBCKT test_inv in out {0} {1}\n".format(vdd_name, gnd_name))
    stim_file.write("mpinv out in {0} {0} {1} w={2}u l={3}u\n".format(vdd_name,
                                                                      pmos_name,
                                                                      beta * size * tx_width,
                                                                      tx_length))
    stim_file.write("mninv out in {0} {0} {1} w={2}u l={3}u\n".format(gnd_name,
                                                                      nmos_name,
                                                                      size * tx_width,
                                                                      tx_length))
    stim_file.write(".ENDS test_inv\n")


def create_buffer(stim_file, buffer_name, size=[1,3], beta=2.5):
    """Generates buffer for top level signals (only for sim
    purposes). Size is pair for PMOS, NMOS width multiple. It includes
    a beta of 3."""

    stim_file.write(".SUBCKT test_{2} in out {0} {1}\n".format(vdd_name, 
                                                                   gnd_name,
                                                                   buffer_name))
    stim_file.write("mpinv1 out_inv in {0} {0} {1} w={2}u l={3}u\n".format(vdd_name,
                                                                           pmos_name,
                                                                           beta * size[0] * tx_width,
                                                                           tx_length))
    stim_file.write("mninv1 out_inv in {0} {0} {1} w={2}u l={3}u\n".format(gnd_name,
                                                                           nmos_name,
                                                                           size[0] * tx_width,
                                                                           tx_length))
    stim_file.write("mpinv2 out out_inv {0} {0} {1} w={2}u l={3}u\n".format(vdd_name,
                                                                                pmos_name,
                                                                                beta * size[1] * tx_width,
                                                                                tx_length))
    stim_file.write("mninv2 out out_inv {0} {0} {1} w={2}u l={3}u\n".format(gnd_name,
                                                                                nmos_name,
                                                                                size[1] * tx_width,
                                                                                tx_length))
    stim_file.write(".ENDS test_{0}\n".format(buffer_name))


def add_buffer(stim_file, buffer_name, signal_list):
    """Adds buffers to each top level signal that is in signal_list (only for sim purposes)"""
    for signal in signal_list:
        stim_file.write("X{0}_buffer {0} {0}_buf {1} {2} test_{3}\n".format(signal,
                                                                            "test"+vdd_name,
                                                                            "test"+gnd_name,
                                                                            buffer_name))


def add_inverter(stim_file, signal_list):
    """Adds inv for each signal that needs its inverted version (only for sim purposes)"""
    for signal in signal_list:
        stim_file.write("X{0}_inv {0} {0}_inv {1} {2} test_inv\n".format(signal,
                                                                         "test"+vdd_name,
                                                                         "test"+gnd_name))


def add_accesstx(stim_file, dbits):
    """Adds transmission gate for inputs to data-bus (only for sim purposes)"""
    stim_file.write("* Tx Pin-list: Drain Gate Source Body\n")
    for i in range(dbits):
        pmos_access_string="mp{0} DATA[{0}] WEb_trans_buf D[{0}]_buf {1} {2} w={3}u l={4}u\n"
        stim_file.write(pmos_access_string.format(i,
                                                  "test"+vdd_name,
                                                  pmos_name,
                                                  2 * tx_width,
                                                  tx_length))
        nmos_access_string="mn{0} DATA[{0}] WEb_trans_inv D[{0}]_buf {1} {2} w={3}u l={4}u\n"
        stim_file.write(nmos_access_string.format(i,
                                                  "test"+gnd_name,
                                                  nmos_name,
                                                  2 * tx_width,
                                                  tx_length))

def gen_pulse(stim_file, sig_name, v1=gnd, v2=vdd, offset=0, period=1, t_rise=0, t_fall=0):
    """Generates a periodic signal with 50% duty cycle and slew rates. Period is measured
    from 50% to 50%."""
    pulse_string="V{0} {0} 0 PULSE ({1} {2} {3}n {4}n {5}n {6}n {7}n)\n"
    stim_file.write(pulse_string.format(sig_name, 
                                        v1,
                                        v2,
                                        offset,
                                        t_rise,
                                        t_fall, 
                                        0.5*period-0.5*t_rise-0.5*t_fall,
                                        period))



def gen_clk_pwl(stim_file, cycle_times, t_fall, t_rise):
    """Generates a clk signal using pwl. The cycle times are the times of the
    clock rising edge. It is assumed to start at time 0 with clock 0. Duty
    cycle is assumed to be 50%. Rise/fall times are 0-100%."""
    stim_file.write("V{0} {0} 0 PWL (0n 0v ".format(tech.spice["clk"]))
    for i in range(len(cycle_times)-1):
        period = cycle_times[i+1] - cycle_times[i]
        t_current = cycle_times[i] - 0.5*t_rise # 50% point is at cycle time
        t_current2 = t_current + t_rise
        # rising edge
        stim_file.write("{0}n {1}v {2}n {3}v ".format(t_current, gnd, t_current2, vdd))
        t_current = t_current + 0.5*period - 0.5*t_fall # 50% point is at cycle time
        t_current2 = t_current + t_fall
        # falling edge
        stim_file.write("{0}n {1}v {2}n {3}v ".format(t_current, vdd, t_current2, gnd))
    # end time doesn't need a rising edge
    stim_file.write("{0}n {1}v)\n".format(cycle_times[-1], gnd))


def gen_data_pwl(stim_file, key_times, sig_name, data_value, feasible_period, target_period, t_rise, t_fall):
    """Generates the PWL data inputs for a simulation timing test."""
    data_value_invert = gnd if data_value == vdd else vdd

    t_current = 0.0
    stim_file.write("V{0} {0} 0 PWL ({1}n {2}v ".format(sig_name, t_current, data_value_invert))
    t_current = key_times[2] - 0.25 * target_period
    t_current += (0.5 * target_period)  # uses falling edge for ZBT mode
    slew_time = t_rise if data_value_invert == gnd else t_fall
    t_current2 = t_current + slew_time
    stim_file.write("{0}n {1}v {2}n {3}v ".format(t_current, data_value_invert, t_current2, data_value))
    t_current = key_times[2] + 0.25 * target_period
    t_current += (0.5 * target_period)  # uses falling edge for ZBT mode
    slew_time = t_rise if data_value == gnd else t_fall
    t_current2 = t_current + slew_time
    stim_file.write("{0}n {1}v {2}n {3}v ".format(t_current, data_value, t_current2, data_value_invert))
    t_current = key_times[5] + 0.25 * feasible_period
    stim_file.write("{0}n {1}v)\n".format(t_current, data_value_invert))


def gen_addr_pwl(stim_file, key_times, addr, feasible_period, target_period, t_rise, t_fall):
    """Generates the PWL for address inputs for a simulation timing test"""
    # reverse string
    reversed_addr = addr[::-1]  
    # inverts all bits in address using intermediate value of 2
    invert_addr = reversed_addr.replace('1', '2').replace('0', '1').replace('2', '0')  

    for i in range(len(reversed_addr)):
        v_val = gnd if reversed_addr[i] == '0' else vdd
        v_val_invert = gnd if invert_addr[i] == '0' else vdd
        t_current = 0.0
        stim_file.write("V{0} {0} 0 PWL ({1}n {2}v ".format("A[{0}]".format(i), t_current, v_val))
        t_current = key_times[3] - 0.25 * target_period
        slew_time = t_rise if v_val == gnd else t_fall
        t_current2 = t_current + slew_time
        stim_file.write("{0}n {1}v {2}n {3}v ".format(t_current, v_val, t_current2, v_val_invert))
        t_current = key_times[4] - 0.25 * target_period
        slew_time = t_rise if v_val_invert == gnd else t_fall
        t_current2 = t_current + slew_time
        stim_file.write("{0}n {1}v {2}n {3}v ".format(t_current, v_val_invert, t_current2, v_val))
        t_current = key_times[5] + 0.25 * feasible_period
        stim_file.write("{0}n {1}v)\n".format(t_current, v_val))


def gen_constant(stim_file, sig_name, v_ref, v_val):
    """Generates a constant signal with reference voltage and the voltage value"""
    stim_file.write("V{0} {0} {1} DC {2}\n".format(sig_name, v_ref, v_val))

def gen_csb_pwl(key_times, feasible_period, target_period, t_rise, t_fall):
    """Returns two lists for x,y coordinates for the generation of CSb pwl"""
    t_current = 0.0
    x_list = [t_current]
    y_list = [vdd]

    for key_time in key_times[:2]:
        t_current = key_time - 0.25 * feasible_period
        x_list.append(t_current)
        y_list.append(vdd)
        x_list.append(t_current + t_fall)
        y_list.append(gnd)

        t_current = key_time + 0.25 * feasible_period
        x_list.append(t_current)
        y_list.append(gnd)
        x_list.append(t_current + t_rise)
        y_list.append(vdd)

    for key_time in key_times[2:-1]:
        t_current = key_time - 0.25 * target_period
        x_list.append(t_current)
        y_list.append(vdd)
        x_list.append(t_current + t_fall)
        y_list.append(gnd)

        t_current = key_time + 0.25 * target_period
        x_list.append(t_current)
        y_list.append(gnd)
        x_list.append(t_current + t_rise)
        y_list.append(vdd)

    return (x_list, y_list)


def gen_web_pwl(key_times, feasible_period, target_period, t_rise, t_fall):
    """Returns two lists for x,y coordinates for the generation of WEb pwl"""

    t_current = 0.0
    x_list = [t_current]
    y_list = [vdd]

    t_current = key_times[0] - 0.25 * feasible_period
    x_list.append(t_current)
    y_list.append(vdd)
    x_list.append(t_current + t_fall)
    y_list.append(gnd)

    t_current = key_times[0] + 0.25 * feasible_period
    x_list.append(t_current)
    y_list.append(gnd)
    x_list.append(t_current + t_rise)
    y_list.append(vdd)

    t_current = key_times[2] - 0.25 * target_period
    x_list.append(t_current)
    y_list.append(vdd)
    x_list.append(t_current + t_fall)
    y_list.append(gnd)

    t_current = key_times[2] + 0.25 * target_period
    x_list.append(t_current)
    y_list.append(gnd)
    x_list.append(t_current + t_rise)
    y_list.append(vdd)

    t_current = key_times[3] - 0.25 * target_period
    x_list.append(t_current)
    y_list.append(vdd)
    x_list.append(t_current + t_fall)
    y_list.append(gnd)

    t_current = key_times[3] + 0.25 * target_period
    x_list.append(t_current)
    y_list.append(gnd)
    x_list.append(t_current + t_rise)
    y_list.append(vdd)

    return (x_list, y_list)


def gen_oeb_pwl(key_times, feasible_period, target_period, t_rise, t_fall):
    """Returns two lists for x,y coordinates for the generation of OEb pwl"""

    t_current = 0.0
    x_list = [t_current]
    y_list = [vdd]

    t_current = key_times[1] - 0.25 * feasible_period
    x_list.append(t_current)
    y_list.append(vdd)
    x_list.append(t_current + t_fall)
    y_list.append(gnd)

    t_current = key_times[1] + 0.25 * feasible_period
    x_list.append(t_current)
    y_list.append(gnd)
    x_list.append(t_current + t_rise)
    y_list.append(vdd)

    t_current = key_times[4] - 0.25 * target_period
    x_list.append(t_current)
    y_list.append(vdd)
    x_list.append(t_current + t_fall)
    y_list.append(gnd)

    t_current = key_times[4] + 0.25 * target_period
    x_list.append(t_current)
    y_list.append(gnd)
    x_list.append(t_current + t_rise)
    y_list.append(vdd)

    return (x_list, y_list)


def gen_web_trans_pwl(key_times, feasible_period, target_period, t_rise, t_fall):
    """Returns two lists for x,y coordinates for the generation of WEb_transmission_gate pwl"""

    t_current = 0.0
    x_list = [t_current]
    y_list = [vdd]

    t_current = key_times[0] + 0.5 * feasible_period
    t_current -= 0.25 * feasible_period
    x_list.append(t_current)
    y_list.append(vdd)
    x_list.append(t_current + t_fall)
    y_list.append(gnd)

    t_current += 0.5 * feasible_period
    x_list.append(t_current)
    y_list.append(gnd)
    x_list.append(t_current + t_rise)
    y_list.append(vdd)

    t_current = key_times[2] + 0.5 * target_period
    t_current -= 0.25 * target_period
    x_list.append(t_current)
    y_list.append(vdd)
    x_list.append(t_current + t_fall)
    y_list.append(gnd)

    t_current += 0.5 * target_period
    x_list.append(t_current)
    y_list.append(gnd)
    x_list.append(t_current + t_rise)
    y_list.append(vdd)

    t_current = key_times[3] + 0.5 * target_period
    t_current -= 0.25 * target_period
    x_list.append(t_current)
    y_list.append(vdd)
    x_list.append(t_current + t_fall)
    y_list.append(gnd)

    t_current += 0.5 * target_period
    x_list.append(t_current)
    y_list.append(gnd)
    x_list.append(t_current + t_rise)
    y_list.append(vdd)

    return (x_list, y_list)


def get_inverse_value(value):
    if value > 0.5*vdd:
        return gnd
    elif value <= 0.5*vdd:
        return vdd
    else:
        debug.error("Invalid value to get an inverse of: {0}".format(value))


def gen_pwl(stim_file, sig_name, x_list, y_list):
    """Generates an arbitrary pwl for a signal where xlist is times in
    ns and ylist is voltage. """

    t_current = 0.0
    stim_file.write("V{0} {0} 0 PWL (".format(sig_name))
    for p in zip(x_list,y_list):
        stim_file.write("{0}n {1}v ".format(p[0],p[1]))
    stim_file.write(")\n")

def gen_trap_pwl(stim_file, sig_name, x_list, y_list, t_rise, t_fall):
    """Generates a trapezoidal pwl for a signal where xlist is times in ns and ylist is voltage. 
    Transitions are assumed to ignore slew and the slew rates are generated automatically
    using the provided 0-100% slew times and centering times at the 50% point.."""

    stim_file.write("V{0} {0} 0 PWL (".format(sig_name))
    for p in zip(x_list,y_list):
        slew = t_rise if p[1]>0.5*vdd else t_fall
        start = max(p[0]-0.5*slew,0)
        end = p[0]+0.5*slew
        stim_file.write("{0}n {1}v ".format(start, get_inverse_value(p[1])))
        stim_file.write("{0}n {1}v ".format(end, p[1]))
    stim_file.write(")\n")



def gen_meas_delay(stim_file, meas_name, trig_name, targ_name, trig_val, targ_val, trig_dir, targ_dir, td):
    """Creates the .meas statement for the measurement of delay"""
    measure_string=".meas tran {0} TRIG v({1}) VAL={2} RISE={3} TARG v({4}) VAL={5} TD={7}n {6}=1\n"
    stim_file.write(measure_string.format(meas_name,
                                          trig_name,
                                          trig_val,
                                          trig_dir,
                                          targ_name,
                                          targ_val,
                                          targ_dir,
                                          td))

def gen_meas_power(stim_file, meas_name, t_initial, t_final):
    """Creates the .meas statement for the measurement of avg power"""
    # power mea cmd is different in different spice:
    if OPTS.spice_version == "hspice":
        power_exp = "power"
    else:
        power_exp = "par('(-1*v(" + str(vdd_name) + ")*I(v" + str(vdd_name) + "))')"
    stim_file.write(".meas tran {0} avg {1} from={2}n to={3}n\n".format(meas_name,
                                                                        power_exp,
                                                                        t_initial,
                                                                        t_final))


def write_include(stim_file, models):
    """Writes include statements, inputs are lists of model files"""
    for item in list(models):
        stim_file.write(".include \"{0}\"\n".format(item))


def write_supply(stim_file, vdd_name, gnd_name, vdd_voltage, gnd_voltage):
    """Writes supply voltage statements"""
    stim_file.write("V{0} {0} 0.0 {1}\n".format(vdd_name, vdd_voltage))
    stim_file.write("V{0} {0} 0.0 {1}\n".format(gnd_name, gnd_voltage))
    # This is for the test power supply
    stim_file.write("V{0} {0} 0.0 {1}\n".format("test"+vdd_name, vdd_voltage))
    stim_file.write("V{0} {0} 0.0 {1}\n".format("test"+gnd_name, gnd_voltage))




def run_sim():
    """Run hspice in batch mode and output rawfile to parse."""
    temp_stim = "{0}stim.sp".format(OPTS.openram_temp)
    
    if OPTS.spice_version == "hspice":
        # TODO: Should make multithreading parameter a configuration option
        cmd = "{0} -mt 8 -i {1} -o {2}timing".format(OPTS.spice_exe,
                                                                     temp_stim,
                                                                     OPTS.openram_temp)
        valid_retcode=0
    else:
        cmd = "{0} -b -o {2}timing.lis {1}".format(OPTS.spice_exe,
                                                        temp_stim,
                                                        OPTS.openram_temp)
        # for some reason, ngspice-25 returns 1 when it only has acceptable warnings
        valid_retcode=1

        
    spice_stdout = open("{0}spice_stdout.log".format(OPTS.openram_temp), 'w')
    spice_stderr = open("{0}spice_stderr.log".format(OPTS.openram_temp), 'w')

    debug.info(3, cmd)
    retcode = subprocess.call(cmd, stdout=spice_stdout, stderr=spice_stderr, shell=True)

    spice_stdout.close()
    spice_stderr.close()
    
    if (retcode > valid_retcode):
        debug.error("Spice simulation error: " + cmd, -1)

    
