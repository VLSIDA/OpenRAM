# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from abc import ABC, abstractmethod
from openram import debug
from openram.tech import drc, parameter, spice
from .stimuli import *
from .charutils import *


class spice_measurement(ABC):
    """Base class for spice stimulus measurements."""
    def __init__(self, measure_name, measure_scale=None, has_port=True):
        # Names must be unique for correct spice simulation, but not enforced here.
        self.name = measure_name
        self.measure_scale = measure_scale
        self.has_port = has_port # Needed for error checking
        # Some meta values used externally. variables are added here for consistency accross the objects
        self.meta_str = None
        self.meta_add_delay = False

    @abstractmethod
    def measure_function(self):
        return None

    @abstractmethod
    def get_measure_values(self):
        return None

    def write_measure(self, stim_obj, input_tuple):
        measure_vals = self.get_measure_values(*input_tuple)
        self.measure_function(stim_obj, *measure_vals)

    def retrieve_measure(self, port=None):
        self.port_error_check(port)
        if port is not None:
            value = parse_spice_list("timing", "{0}{1}".format(self.name.lower(), port))
        else:
            value = parse_spice_list("timing", "{0}".format(self.name.lower()))
        if type(value)!=float or self.measure_scale is None:
            return value
        else:
            return value * self.measure_scale

    def port_error_check(self, port):
        if self.has_port and port is None:
            debug.error("Cannot retrieve measurement, port input was expected.", 1)
        elif not self.has_port and port is not None:
            debug.error("Unexpected port input received during measure retrieval.", 1)


class delay_measure(spice_measurement):
    """Generates a spice measurement for the delay of 50%-to-50% points of two signals."""

    def __init__(self,
                 measure_name,
                 trig_name,
                 targ_name,
                 trig_dir_str,
                 targ_dir_str,
                 trig_vdd=0.5,
                 targ_vdd=0.5,
                 measure_scale=None,
                 has_port=True):
        spice_measurement.__init__(self, measure_name, measure_scale, has_port)
        self.set_meas_constants(trig_name, targ_name, trig_dir_str, targ_dir_str, trig_vdd, targ_vdd)

    def measure_function(self, stim_obj, meas_name, trig_name, targ_name, trig_val, targ_val, trig_dir, targ_dir, trig_td, targ_td):
        """ Creates the .meas statement for the measurement of delay """
        measure_string=".meas tran {0} TRIG v({1}) VAL={2} {3}=1 TD={4}n TARG v({5}) VAL={6} {7}=1 TD={8}n\n\n"
        stim_obj.mf.write(measure_string.format(meas_name.lower(),
                                                 trig_name,
                                                 trig_val,
                                                 trig_dir,
                                                 trig_td,
                                                 targ_name,
                                                 targ_val,
                                                 targ_dir,
                                                 targ_td))

    def set_meas_constants(self, trig_name, targ_name, trig_dir_str, targ_dir_str, trig_vdd, targ_vdd):
        """Set the constants for this measurement: signal names, directions, and trigger scales"""
        self.trig_dir_str = trig_dir_str
        self.targ_dir_str = targ_dir_str
        self.trig_val_of_vdd = trig_vdd
        self.targ_val_of_vdd = targ_vdd
        self.trig_name_no_port = trig_name
        self.targ_name_no_port = targ_name

        # Time delays and ports are variant and needed as inputs when writing the measurement

    def get_measure_values(self, trig_td, targ_td, vdd_voltage, port=None):
        """Constructs inputs to stimulus measurement function. Variant values are inputs here."""
        self.port_error_check(port)
        trig_val = self.trig_val_of_vdd * vdd_voltage
        targ_val = self.targ_val_of_vdd * vdd_voltage

        if port is not None:
            # For dictionary indexing reasons, the name is formatted differently than the signals
            meas_name = "{}{}".format(self.name, port)
            trig_name = self.trig_name_no_port.format(port)
            targ_name = self.targ_name_no_port.format(port)
        else:
            meas_name = self.name
            trig_name = self.trig_name_no_port
            targ_name = self.targ_name_no_port
        return (meas_name, trig_name, targ_name, trig_val, targ_val, self.trig_dir_str, self.targ_dir_str, trig_td, targ_td)


class slew_measure(delay_measure):

    def __init__(self, measure_name, signal_name, slew_dir_str, measure_scale=None, has_port=True):
        spice_measurement.__init__(self, measure_name, measure_scale, has_port)
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
            debug.error("Unrecognised slew measurement direction={}".format(slew_dir_str), 1)
        self.trig_name_no_port = signal_name
        self.targ_name_no_port = signal_name

        # Time delays and ports are variant and needed as inputs when writing the measurement


class power_measure(spice_measurement):
    """Generates a spice measurement for the average power between two time points."""

    def __init__(self, measure_name, power_type="", measure_scale=None, has_port=True):
        spice_measurement.__init__(self, measure_name, measure_scale, has_port)
        self.set_meas_constants(power_type)

    def measure_function(self, stim_obj, meas_name, t_initial, t_final):
        """ Creates the .meas statement for the measurement of avg power """
        # power mea cmd is different in different spice:
        if OPTS.spice_name == "hspice":
            power_exp = "power"
        else:
            # FIXME: Obtain proper vdd and gnd name
            power_exp = "par('(-1*v(" + "vdd" + ")*I(v" + "vdd" + "))')"
        stim_obj.mf.write(".meas tran {0} avg {1} from={2}n to={3}n\n\n".format(meas_name.lower(),
                                                                                 power_exp,
                                                                                 t_initial,
                                                                                 t_final))

    def set_meas_constants(self, power_type):
        """Sets values useful for power simulations. This value is only meta related to the lib file (rise/fall)"""
        # Not needed for power simulation
        self.power_type = power_type # Expected to be  "RISE"/"FALL"

    def get_measure_values(self, t_initial, t_final, port=None):
        """Constructs inputs to stimulus measurement function. Variant values are inputs here."""
        self.port_error_check(port)
        if port is not None:
            meas_name = "{}{}".format(self.name, port)
        else:
            meas_name = self.name
        return (meas_name, t_initial, t_final)


class voltage_when_measure(spice_measurement):
    """Generates a spice measurement to measure the voltage of a signal based on the voltage of another."""

    def __init__(self, measure_name, trig_name, targ_name, trig_dir_str, trig_vdd, measure_scale=None, has_port=True):
        spice_measurement.__init__(self, measure_name, measure_scale, has_port)
        self.set_meas_constants(trig_name, targ_name, trig_dir_str, trig_vdd)

    def measure_function(self, stim_obj, meas_name, trig_name, targ_name, trig_val, trig_dir, trig_td):
        """ Creates the .meas statement for the measurement of delay """
        measure_string=".meas tran {0} FIND v({1}) WHEN v({2})={3}v {4}=1 TD={5}n \n\n"
        stim_obj.mf.write(measure_string.format(meas_name.lower(),
                                                targ_name,
                                                trig_name,
                                                trig_val,
                                                trig_dir,
                                                trig_td))

    def set_meas_constants(self, trig_name, targ_name, trig_dir_str, trig_vdd):
        """Sets values useful for power simulations. This value is only meta related to the lib file (rise/fall)"""
        self.trig_dir_str = trig_dir_str
        self.trig_val_of_vdd = trig_vdd
        self.trig_name_no_port = trig_name
        self.targ_name_no_port = targ_name

    def get_measure_values(self, trig_td, vdd_voltage, port=None):
        """Constructs inputs to stimulus measurement function. Variant values are inputs here."""
        self.port_error_check(port)
        if port is not None:
            # For dictionary indexing reasons, the name is formatted differently than the signals
            meas_name = "{}{}".format(self.name, port)
            trig_name = self.trig_name_no_port.format(port)
            targ_name = self.targ_name_no_port.format(port)
        else:
            meas_name = self.name
            trig_name = self.trig_name_no_port
            targ_name = self.targ_name_no_port
        trig_voltage = self.trig_val_of_vdd * vdd_voltage
        return (meas_name, trig_name, targ_name, trig_voltage, self.trig_dir_str, trig_td)


class voltage_at_measure(spice_measurement):
    """Generates a spice measurement to measure the voltage at a specific time.
       The time is considered variant with different periods."""

    def __init__(self, measure_name, targ_name, measure_scale=None, has_port=True):
        spice_measurement.__init__(self, measure_name, measure_scale, has_port)
        self.set_meas_constants(targ_name)

    def measure_function(self, stim_obj, meas_name, targ_name, time_at):
        """ Creates the .meas statement for voltage at time"""
        measure_string=".meas tran {0} FIND v({1}) AT={2}n \n\n"
        stim_obj.mf.write(measure_string.format(meas_name.lower(),
                                                targ_name,
                                                time_at))

    def set_meas_constants(self, targ_name):
        """Sets values useful for power simulations. This value is only meta related to the lib file (rise/fall)"""
        self.targ_name_no_port = targ_name

    def get_measure_values(self, time_at, port=None):
        """Constructs inputs to stimulus measurement function. Variant values are inputs here."""
        self.port_error_check(port)
        if port is not None:
            # For dictionary indexing reasons, the name is formatted differently than the signals
            meas_name = "{}{}".format(self.name, port)
            targ_name = self.targ_name_no_port.format(port)
        else:
            meas_name = self.name
            targ_name = self.targ_name_no_port
        return (meas_name, targ_name, time_at)
