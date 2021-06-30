# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

from .simulation import simulation
from globals import OPTS
import debug
import tech 

import math

class cacti(simulation):    
    """
    Delay model for the SRAM which which
    """
    
    def __init__(self, sram, spfile, corner):
        super().__init__(sram, spfile, corner)

        # self.targ_read_ports = []
        # self.targ_write_ports = []
        # self.period = 0
        # if self.write_size:
            # self.num_wmasks = int(math.ceil(self.word_size / self.write_size))
        # else:
            # self.num_wmasks = 0
        #self.set_load_slew(0, 0)
        self.set_corner(corner)
        self.create_signal_names()
        self.add_graph_exclusions()
    
    def get_lib_values(self, load_slews):
        """
        Return the analytical model results for the SRAM.
        """
        if OPTS.num_rw_ports > 1 or OPTS.num_w_ports > 0 and OPTS.num_r_ports > 0:
            debug.warning("In analytical mode, all ports have the timing of the first read port.")

        # Probe set to 0th bit, does not matter for analytical delay.
        self.set_probe('0' * self.addr_size, 0)
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
            path_delays = self.graph.get_timing(bl_path, self.corner, slew, load)

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
        
    def horowitz(inputramptime, # input rise time
                 tf,            # time constant of gate
                 vs1,           # threshold voltage
                 vs2,           # threshold voltage
                 rise):         # whether input rises or fall
{
        if inputramptime == 0 and vs1 == vs2:
            return tf * (-math.log(vs1) if vs1 < 1 else math.log(vs1))

        a = inputramptime / tf
        if rise == RISE:
            b = 0.5;
            td = tf * sqrt(math.log(vs1)*math.log(vs1) + 2*a*b*(1.0 - vs1)) + tf*(math.log(vs1) - math.log(vs2))

        else:
            b = 0.4;
            td = tf * sqrt(math.log(1.0 - vs1)*math.log(1.0 - vs1) + 2*a*b*(vs1)) + tf*(math.log(1.0 - vs1) - math.log(1.0 - vs2))

        return td
  
    def tr_R_on(width, nchannel, stack, _is_dram, _is_cell, _is_wl_tr, _is_sleep_tx):

        # FIXME: temp code until parameters have been determined
        if _is_dram and _is_cell:
            dt = tech.dram_acc   #DRAM cell access transistor
      
        elif _is_dram and _is_wl_tr:
            dt = tech.dram_wl    #DRAM wordline transistor
      
        elif not _is_dram and _is_cell:
            dt = tech.sram_cell  #SRAM cell access transistor
      
        elif _is_sleep_tx:
            dt = tech.sleep_tx  #Sleep transistor
      
        else:
            dt = tech.peri_global
      

        restrans = dt.R_nch_on if nchannel else dt.R_pch_on
        return stack * restrans / width

    def gate_C(width, wirelength, _is_dram, _is_cell, _is_wl_tr, _is_sleep_tx)

        if _is_dram and _is_cell:
            dt = tech.dram_acc   #DRAM cell access transistor
      
        elif _is_dram and _is_wl_tr:
            dt = tech.dram_wl    #DRAM wordline transistor
      
        elif not _is_dram and _is_cell:
            dt = tech.sram_cell  #SRAM cell access transistor
      
        elif _is_sleep_tx:
            dt = tech.sleep_tx   #Sleep transistor
      
        else:
            dt = tech.peri_global
      

        return (dt.C_g_ideal + dt.C_overlap + 3*dt.C_fringe)*width + dt.l_phy*Cpolywire
    
    def drain_C_(width,
                 nchannel,
                 stack,
                 next_arg_thresh_folding_width_or_height_cell,
                 fold_dimension,
                 _is_dram,
                 _is_cell,
                 _is_wl_tr,
                 _is_sleep_tx):

        if _is_dram and _is_cell:
            dt = tech.dram_acc   # DRAM cell access transistor
      
        elif _is_dram and _is_wl_tr:
            dt = &g_tp.dram_wl    # DRAM wordline transistor
      
        elif not _is_dram) and _is_cell:
            dt = tech.sram_cell  # SRAM cell access transistor
      
        elif _is_sleep_tx:
            dt = tech.sleep_tx  # Sleep transistor
      
        else
            dt = tech.peri_global
      

        c_junc_area = dt.C_junc;
        c_junc_sidewall = dt.C_junc_sidewall
        c_fringe = 2*dt.C_fringe
        c_overlap = 2*dt.C_overlap
        drain_C_metal_connecting_folded_tr = 0

        # determine the width of the transistor after folding (if it is getting folded)
        if next_arg_thresh_folding_width_or_height_cell == 0:
            # interpret fold_dimension as the the folding width threshold
            # i.e. the value of transistor width above which the transistor gets folded
            w_folded_tr = fold_dimension
      
        else:
            # interpret fold_dimension as the height of the cell that this transistor is part of.
            h_tr_region  = fold_dimension - 2 * tech.HPOWERRAIL
            # TODO : w_folded_tr must come from Component::compute_gate_area()
            ratio_p_to_n = 2.0 / (2.0 + 1.0)
            
            if nchannel:
                w_folded_tr = (1 - ratio_p_to_n) * (h_tr_region - tech.MIN_GAP_BET_P_AND_N_DIFFS)
            
            else:
                w_folded_tr = ratio_p_to_n * (h_tr_region - tech.MIN_GAP_BET_P_AND_N_DIFFS)
            
      
        num_folded_tr = int(ceil(width / w_folded_tr))

        if num_folded_tr < 2:
            w_folded_tr = width;
      

        total_drain_w = (tech.w_poly_contact + 2 * tech.spacing_poly_to_contact) +  # only for drain
                             (stack - 1) * tech.spacing_poly_to_poly
        drain_h_for_sidewall = w_folded_tr
        total_drain_height_for_cap_wrt_gate = w_folded_tr + 2 * w_folded_tr * (stack - 1)
        if num_folded_tr > 1:
            total_drain_w += (num_folded_tr - 2) * (tech.w_poly_contact + 2 * tech.spacing_poly_to_contact) +
                             (num_folded_tr - 1) * ((stack - 1) * tech.spacing_poly_to_poly)

            if num_folded_tr%2 == 0:
                drain_h_for_sidewall = 0
        
            total_drain_height_for_cap_wrt_gate *= num_folded_tr
            drain_C_metal_connecting_folded_tr   = tech.wire_local.C_per_um * total_drain_w
      

        drain_C_area     = c_junc_area * total_drain_w * w_folded_tr
        drain_C_sidewall = c_junc_sidewall * (drain_h_for_sidewall + 2 * total_drain_w)
        drain_C_wrt_gate = (c_fringe + c_overlap) * total_drain_height_for_cap_wrt_gate

        return drain_C_area + drain_C_sidewall + drain_C_wrt_gate + drain_C_metal_connecting_folded_tr
    


    