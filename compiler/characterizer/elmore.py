# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram import OPTS
from .simulation import simulation


class elmore(simulation):
    """
    Delay model for the SRAM which calculates Elmore delays along the SRAM critical path.
    """

    def __init__(self, sram, spfile, corner):
        super().__init__(sram, spfile, corner)

        # self.targ_read_ports = []
        # self.targ_write_ports = []
        # self.period = 0
        # if self.write_size != self.word_size:
            # self.num_wmasks = int(math.ceil(self.word_size / self.write_size))
        # else:
            # self.num_wmasks = 0
        #self.set_load_slew(0, 0)
        self.set_params()
        self.set_corner(corner)
        self.create_signal_names()
        self.add_graph_exclusions()

    def set_params(self):
        """Set parameters specific to the corner being simulated"""
        self.params = {}
        # Set the specific functions to use for timing defined in the SRAM module
        self.params["model_name"] = OPTS.model_name

    def get_lib_values(self, load_slews):
        """
        Return the analytical model results for the SRAM.
        """
        if OPTS.num_rw_ports > 1 or OPTS.num_w_ports > 0 and OPTS.num_r_ports > 0:
            debug.warning("In analytical mode, all ports have the timing of the first read port.")

        # Probe set to 0th bit, does not matter for analytical delay.
        self.set_probe('0' * self.bank_addr_size, 0)
        self.create_graph()
        self.set_internal_spice_names()
        self.create_measurement_names()

        port = self.read_ports[0]
        self.graph.get_all_paths('{}{}'.format("clk", port),
                                 '{}{}_{}'.format(self.dout_name, port, self.probe_data))

        # Select the path with the bitline (bl)
        bl_name, br_name = self.get_bl_name(self.graph.all_paths, port)
        bl_path = [path for path in self.graph.all_paths if bl_name in path][0]

        # Set delay/power for slews and loads
        port_data = self.get_empty_measure_data_dict()
        power = self.analytical_power(load_slews)
        debug.info(1, 'Slew, Load, Delay(ns), Slew(ns)')
        max_delay = 0.0
        for load,slew in load_slews:
            # Calculate delay based on slew and load
            path_delays = self.graph.get_timing(bl_path, self.corner, slew, load, self.params)

            total_delay = self.sum_delays(path_delays)
            max_delay = max(max_delay, total_delay.delay)
            debug.info(1,
                       '{}, {}, {}, {}'.format(slew,
                                               load,
                                               total_delay.delay / 1e3,
                                               total_delay.slew / 1e3))
            # Delay is only calculated on a single port and replicated for now.
            for port in self.all_ports:
                for mname in self.delay_meas_names + self.power_meas_names:
                    if "power" in mname:
                        port_data[port][mname].append(power.dynamic)
                    elif "delay" in mname and port in self.read_ports:
                        port_data[port][mname].append(total_delay.delay / 1e3)
                    elif "slew" in mname and port in self.read_ports:
                        port_data[port][mname].append(total_delay.slew / 1e3)

        # Margin for error in period. Calculated by averaging required margin for a small and large
        # memory. FIXME: margin is quite large, should be looked into.
        period_margin = 1.85
        sram_data = {"min_period": (max_delay / 1e3) * 2 * period_margin,
                     "leakage_power": power.leakage}

        debug.info(2, "SRAM Data:\n{}".format(sram_data))
        debug.info(2, "Port Data:\n{}".format(port_data))

        return (sram_data, port_data)

    def analytical_power(self, load_slews):
        """Get the dynamic and leakage power from the SRAM"""

        # slews unused, only last load is used
        load = load_slews[-1][0]
        power = self.sram.analytical_power(self.corner, load)
        # convert from nW to mW
        power.dynamic /= 1e6
        power.leakage /= 1e6
        debug.info(1, "Dynamic Power: {0} mW".format(power.dynamic))
        debug.info(1, "Leakage Power: {0} mW".format(power.leakage))
        return power
