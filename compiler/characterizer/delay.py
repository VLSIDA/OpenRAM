# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import math
import shutil
from openram import debug
from openram import tech
from openram import OPTS
from .stimuli import *
from .trim_spice import *
from .charutils import *
from .simulation import simulation
from .measurements import *
from os import path
import re


class delay(simulation):
    """
    Functions to measure the delay and power of an SRAM at a given address and
    data bit.

    In general, this will perform the following actions:
    1) Trim the netlist to remove unnecessary logic.
    2) Find a feasible clock period using max load/slew on the trimmed netlist.
    3) Characterize all loads/slews and consider fail when delay is greater than 5% of feasible delay using trimmed netlist.
    4) Measure the leakage during the last cycle of the trimmed netlist when there is no operation.
    5) Measure the leakage of the whole netlist (untrimmed) in each corner.
    6) Subtract the trimmed leakage and add the untrimmed leakage to the power.

    Netlist trimming can be removed by setting OPTS.trim_netlist to
    False, but this is VERY slow.

    """

    def __init__(self, sram, spfile, corner, output_path=None):
        super().__init__(sram, spfile, corner)

        self.targ_read_ports = []
        self.targ_write_ports = []
        self.period = 0
        if self.write_size != self.word_size:
            self.num_wmasks = int(math.ceil(self.word_size / self.write_size))
        else:
            self.num_wmasks = 0

        if output_path is None:
            self.output_path = OPTS.openram_temp
        else:
            self.output_path = output_path

        self.set_load_slew(0, 0)
        self.set_corner(corner)
        self.create_signal_names()
        self.add_graph_exclusions()
        self.meas_id = 0

    def create_measurement_objects(self):
        """ Create the measurements used for read and write ports """

        self.read_meas_lists = self.create_read_port_measurement_objects()
        self.write_meas_lists = self.create_write_port_measurement_objects()
        self.check_meas_names(self.read_meas_lists + self.write_meas_lists)

    def check_meas_names(self, measures_lists):
        """
        Given measurements (in 2d list), checks that their names are unique.
        Spice sim will fail otherwise.
        """
        name_set = set()
        for meas_list in measures_lists:
            for meas in meas_list:
                name = meas.name.lower()
                debug.check(name not in name_set, ("SPICE measurements must have unique names. "
                                                   "Duplicate name={0}").format(name))
                name_set.add(name)

    def create_read_port_measurement_objects(self):
        """Create the measurements used for read ports: delays, slews, powers"""

        self.read_lib_meas = []
        self.clk_frmt = "clk{0}" # Unformatted clock name
        targ_name = "{0}{{}}_{1}".format(self.dout_name, self.probe_data) # Empty values are the port and probe data bit
        self.delay_meas = []
        self.delay_meas.append(delay_measure("delay_lh", self.clk_frmt, targ_name, "FALL", "RISE", measure_scale=1e9))
        self.delay_meas[-1].meta_str = sram_op.READ_ONE # Used to index time delay values when measurements written to spice file.
        self.delay_meas[-1].meta_add_delay = False
        self.delay_meas.append(delay_measure("delay_hl", self.clk_frmt, targ_name, "FALL", "FALL", measure_scale=1e9))
        self.delay_meas[-1].meta_str = sram_op.READ_ZERO
        self.delay_meas[-1].meta_add_delay = False
        self.read_lib_meas+=self.delay_meas

        self.slew_meas = []
        self.slew_meas.append(slew_measure("slew_lh", targ_name, "RISE", measure_scale=1e9))
        self.slew_meas[-1].meta_str = sram_op.READ_ONE
        self.slew_meas.append(slew_measure("slew_hl", targ_name, "FALL", measure_scale=1e9))
        self.slew_meas[-1].meta_str = sram_op.READ_ZERO
        self.read_lib_meas+=self.slew_meas

        self.read_lib_meas.append(power_measure("read1_power", "RISE", measure_scale=1e3))
        self.read_lib_meas[-1].meta_str = sram_op.READ_ONE
        self.read_lib_meas.append(power_measure("read0_power", "FALL", measure_scale=1e3))
        self.read_lib_meas[-1].meta_str = sram_op.READ_ZERO

        self.read_lib_meas.append(power_measure("disabled_read1_power", "RISE", measure_scale=1e3))
        self.read_lib_meas[-1].meta_str = "disabled_read1"
        self.read_lib_meas.append(power_measure("disabled_read0_power", "FALL", measure_scale=1e3))
        self.read_lib_meas[-1].meta_str = "disabled_read0"

        # This will later add a half-period to the spice time delay. Only for reading 0.
        # FIXME: Removed this to check, see if it affects anything
        #for obj in self.read_lib_meas:
        #    if obj.meta_str is sram_op.READ_ZERO:
        #        obj.meta_add_delay = True

        read_measures = []
        read_measures.append(self.read_lib_meas)
        # Other measurements associated with the read port not included in the liberty file
        read_measures.append(self.create_bitline_measurement_objects())
        read_measures.append(self.create_debug_measurement_objects())
        read_measures.append(self.create_read_bit_measures())
        # TODO: Maybe don't do this here (?)
        if OPTS.top_process != "memchar":
            read_measures.append(self.create_sen_and_bitline_path_measures())

        return read_measures

    def create_bitline_measurement_objects(self):
        """
        Create the measurements used for bitline delay values. Due to
        unique error checking, these are separated from other measurements.
        These measurements are only associated with read values.
        """

        self.bitline_volt_meas = []
        self.bitline_volt_meas.append(voltage_at_measure("v_bl_READ_ZERO",
                                                         self.bl_name))
        self.bitline_volt_meas[-1].meta_str = sram_op.READ_ZERO
        self.bitline_volt_meas.append(voltage_at_measure("v_br_READ_ZERO",
                                                         self.br_name))
        self.bitline_volt_meas[-1].meta_str = sram_op.READ_ZERO

        self.bitline_volt_meas.append(voltage_at_measure("v_bl_READ_ONE",
                                                         self.bl_name))
        self.bitline_volt_meas[-1].meta_str = sram_op.READ_ONE
        self.bitline_volt_meas.append(voltage_at_measure("v_br_READ_ONE",
                                                         self.br_name))
        self.bitline_volt_meas[-1].meta_str = sram_op.READ_ONE
        return self.bitline_volt_meas

    def create_write_port_measurement_objects(self):
        """Create the measurements used for read ports: delays, slews, powers"""

        self.write_lib_meas = []

        self.write_lib_meas.append(power_measure("write1_power", "RISE", measure_scale=1e3))
        self.write_lib_meas[-1].meta_str = sram_op.WRITE_ONE
        self.write_lib_meas.append(power_measure("write0_power", "FALL", measure_scale=1e3))
        self.write_lib_meas[-1].meta_str = sram_op.WRITE_ZERO

        self.write_lib_meas.append(power_measure("disabled_write1_power", "RISE", measure_scale=1e3))
        self.write_lib_meas[-1].meta_str = "disabled_write1"
        self.write_lib_meas.append(power_measure("disabled_write0_power", "FALL", measure_scale=1e3))
        self.write_lib_meas[-1].meta_str = "disabled_write0"

        write_measures = []
        write_measures.append(self.write_lib_meas)
        write_measures.append(self.create_write_bit_measures())

        return write_measures

    def create_debug_measurement_objects(self):
        """Create debug measurement to help identify failures."""

        self.dout_volt_meas = []
        for meas in self.delay_meas:
            # Output voltage measures
            self.dout_volt_meas.append(voltage_at_measure("v_{0}".format(meas.name),
                                                           meas.targ_name_no_port))
            self.dout_volt_meas[-1].meta_str = meas.meta_str

            if OPTS.use_pex and OPTS.pex_exe[0] != 'calibre':
                self.sen_meas = delay_measure("delay_sen", self.clk_frmt, self.sen_name, "FALL", "RISE", measure_scale=1e9)
            else:
                self.sen_meas = delay_measure("delay_sen", self.clk_frmt, self.sen_name + "{}", "FALL", "RISE", measure_scale=1e9)

        self.sen_meas.meta_str = sram_op.READ_ZERO
        self.sen_meas.meta_add_delay = True

        return self.dout_volt_meas + [self.sen_meas]

    def create_read_bit_measures(self):
        """ Adds bit measurements for read0 and read1 cycles """

        self.read_bit_meas = {bit_polarity.NONINVERTING: [], bit_polarity.INVERTING: []}
        meas_cycles = (sram_op.READ_ZERO, sram_op.READ_ONE)
        for cycle in meas_cycles:
            meas_tag = "a{0}_b{1}_{2}".format(self.probe_address, self.probe_data, cycle.name)
            single_bit_meas = self.get_bit_measures(meas_tag, self.probe_address, self.probe_data)
            for polarity, meas in single_bit_meas.items():
                meas.meta_str = cycle
                self.read_bit_meas[polarity].append(meas)
        # Dictionary values are lists, reduce to a single list of measurements
        return [meas for meas_list in self.read_bit_meas.values() for meas in meas_list]

    def create_write_bit_measures(self):
        """ Adds bit measurements for write0 and write1 cycles """

        self.write_bit_meas = {bit_polarity.NONINVERTING: [], bit_polarity.INVERTING: []}
        meas_cycles = (sram_op.WRITE_ZERO, sram_op.WRITE_ONE)
        for cycle in meas_cycles:
            meas_tag = "a{0}_b{1}_{2}".format(self.probe_address, self.probe_data, cycle.name)
            single_bit_meas = self.get_bit_measures(meas_tag, self.probe_address, self.probe_data)
            for polarity, meas in single_bit_meas.items():
                meas.meta_str = cycle
                self.write_bit_meas[polarity].append(meas)
        # Dictionary values are lists, reduce to a single list of measurements
        return [meas for meas_list in self.write_bit_meas.values() for meas in meas_list]

    def get_bit_measures(self, meas_tag, probe_address, probe_data):
        """
        Creates measurements for the q/qbar of input bit position.
        meas_tag is a unique identifier for the measurement.
        """

        bit_col = self.get_data_bit_column_number(probe_address, probe_data)
        bit_row = self.get_address_row_number(probe_address)
        if OPTS.top_process == "memchar":
            cell_name = self.cell_name.format(bit_row, bit_col)
            storage_names = ("Q", "Q_bar")
        else:
            (cell_name, cell_inst) = self.sram.get_cell_name(self.sram.name, bit_row, bit_col)
            storage_names = cell_inst.mod.get_storage_net_names()
        debug.check(len(storage_names) == 2, ("Only inverting/non-inverting storage nodes"
                                              "supported for characterization. Storage nets={0}").format(storage_names))
        if OPTS.use_pex and OPTS.pex_exe[0] != "calibre":
            bank_num = self.sram.get_bank_num(self.sram.name, bit_row, bit_col)
            q_name = "bitcell_Q_b{0}_r{1}_c{2}".format(bank_num, bit_row, bit_col)
            qbar_name = "bitcell_Q_bar_b{0}_r{1}_c{2}".format(bank_num, bit_row, bit_col)
        else:
            q_name = cell_name + OPTS.hier_seperator + str(storage_names[0])
            qbar_name = cell_name + OPTS.hier_seperator + str(storage_names[1])

        # Bit measures, measurements times to be defined later. The measurement names must be unique
        # but they is enforced externally. {} added to names to differentiate between ports allow the
        # measurements are independent of the ports
        q_meas = voltage_at_measure("v_q_{0}".format(meas_tag), q_name)
        qbar_meas = voltage_at_measure("v_qbar_{0}".format(meas_tag), qbar_name)

        return {bit_polarity.NONINVERTING: q_meas, bit_polarity.INVERTING: qbar_meas}

    def create_sen_and_bitline_path_measures(self):
        """Create measurements for the s_en and bitline paths for individual delays per stage."""

#        # FIXME: There should be a default_read_port variable in this case, pathing is done with this
#        # but is never mentioned otherwise
        port = self.read_ports[0]
        sen_and_port = self.sen_name + str(port)
        bl_and_port = self.bl_name.format(port) # bl_name contains a '{}' for the port
        # Isolate the s_en and bitline paths
        debug.info(1, "self.bl_name = {0}".format(self.bl_name))
        debug.info(2, "self.graph.all_paths = {0}".format(self.graph.all_paths))
        sen_paths = [path for path in self.graph.all_paths if sen_and_port in path]
        bl_paths = [path for path in self.graph.all_paths if bl_and_port in path]
        debug.check(len(sen_paths)==1, 'Found {0} paths which contain the s_en net.'.format(len(sen_paths)))
        debug.check(len(bl_paths)==1, 'Found {0} paths which contain the bitline net.'.format(len(bl_paths)))
        sen_path = sen_paths[0]
        bitline_path = bl_paths[0]

        # Get the measures
        self.sen_path_meas = self.create_delay_path_measures(sen_path, "sen")
        self.bl_path_meas = self.create_delay_path_measures(bitline_path, "bl")
        all_meas = self.sen_path_meas + self.bl_path_meas

        # Paths could have duplicate measurements, remove them before they go to the stim file
        all_meas = self.remove_duplicate_meas_names(all_meas)
        # FIXME: duplicate measurements still exist in the member variables, since they have the same
        # name it will still work, but this could cause an issue in the future.

        return all_meas

    def remove_duplicate_meas_names(self, measures):
        """Returns new list of measurements without duplicate names"""

        name_set = set()
        unique_measures = []
        for meas in measures:
            if meas.name not in name_set:
                name_set.add(meas.name)
                unique_measures.append(meas)

        return unique_measures

    def create_delay_path_measures(self, path, process):
        """Creates measurements for each net along given path."""

        # Determine the directions (RISE/FALL) of signals
        path_dirs = self.get_meas_directions(path)

        # Create the measurements
        path_meas = []
        for i in range(len(path) - 1):
            cur_net, next_net = path[i], path[i + 1]
            cur_dir, next_dir = path_dirs[i], path_dirs[i + 1]
            meas_name = "delay_{0}_to_{1}".format(cur_net, next_net)
            meas_name += "_" + process + "_id" + str(self.meas_id)
            self.meas_id += 1
            if i + 1 != len(path) - 1:
                path_meas.append(delay_measure(meas_name, cur_net, next_net, cur_dir, next_dir, measure_scale=1e9, has_port=False))
            else: # Make the last measurement always measure on FALL because is a read 0
                path_meas.append(delay_measure(meas_name, cur_net, next_net, cur_dir, "FALL", measure_scale=1e9, has_port=False))
            # Some bitcell logic is hardcoded for only read zeroes, force that here as well.
            path_meas[-1].meta_str = sram_op.READ_ZERO
            path_meas[-1].meta_add_delay = True

        return path_meas

    def get_meas_directions(self, path):
        """Returns SPICE measurements directions based on path."""

        # Get the edges modules which define the path
        edge_mods = self.graph.get_edge_mods(path)

        # Convert to booleans based on function of modules (inverting/non-inverting)
        mod_type_bools = [mod.is_non_inverting() for mod in edge_mods]

        # FIXME: obtuse hack to differentiate s_en input from bitline in sense amps
        if self.sen_name in path:
            # Force the sense amp to be inverting for s_en->DOUT.
            # bitline->DOUT is non-inverting, but the module cannot differentiate inputs.
            s_en_index = path.index(self.sen_name)
            mod_type_bools[s_en_index] = False
            debug.info(2, 'Forcing sen->dout to be inverting.')

        # Use these to determine direction list assuming delay start on neg. edge of clock (FALL)
        # Also, use shorthand that 'FALL' == False, 'RISE' == True to simplify logic
        bool_dirs = [False]
        cur_dir = False # All Paths start on FALL edge of clock
        for mod_bool in mod_type_bools:
            cur_dir = (cur_dir == mod_bool)
            bool_dirs.append(cur_dir)

        # Convert from boolean to string
        return ['RISE' if dbool else 'FALL' for dbool in bool_dirs]

    def set_load_slew(self, load, slew):
        """ Set the load and slew """

        self.load = load
        self.slew = slew

    def check_arguments(self):
        """Checks if arguments given for write_stimulus() meets requirements"""

        try:
            int(self.probe_address, 2)
        except ValueError:
            debug.error("Probe Address is not of binary form: {0}".format(self.probe_address), 1)

        if len(self.probe_address) != self.bank_addr_size:
            debug.error("Probe Address's number of bits does not correspond to given SRAM", 1)

        if not isinstance(self.probe_data, int) or self.probe_data>self.word_size or self.probe_data<0:
            debug.error("Given probe_data is not an integer to specify a data bit", 1)

        # Adding port options here which the characterizer cannot handle. Some may be added later like ROM
        if len(self.read_ports) == 0:
            debug.error("Characterizer does not currently support SRAMs without read ports.", 1)
        if len(self.write_ports) == 0:
            debug.error("Characterizer does not currently support SRAMs without write ports.", 1)

    def write_generic_stimulus(self):
        """ Create the instance, supplies, loads, and access transistors. """

        # add vdd/gnd statements
        self.sf.write("\n* Global Power Supplies\n")
        self.stim.write_supply()

        # instantiate the sram
        self.sf.write("\n* Instantiation of the SRAM\n")
        self.stim.inst_model(pins=self.pins,
                             model_name=self.sram.name)

        self.sf.write("\n* SRAM output loads\n")
        for port in self.read_ports:
            for i in range(self.word_size + self.num_spare_cols):
                self.sf.write("CD{0}{1} {2}{0}_{1} 0 {3}f\n".format(port, i, self.dout_name, self.load))

    def write_delay_stimulus(self):
        """
        Creates a stimulus file for simulations to probe a bitcell at a given clock period.
        Address and bit were previously set with set_probe().
        Input slew (in ns) and output capacitive load (in fF) are required for charaterization.
        """

        self.check_arguments()

        # obtains list of time-points for each rising clk edge
        self.create_test_cycles()

        # creates and opens stimulus file for writing
        self.delay_stim_sp = "delay_stim.sp"
        temp_stim = path.join(self.output_path, self.delay_stim_sp)
        self.sf = open(temp_stim, "w")

        # creates and opens measure file for writing
        self.delay_meas_sp = "delay_meas.sp"
        temp_meas = path.join(self.output_path, self.delay_meas_sp)
        self.mf = open(temp_meas, "w")

        if OPTS.spice_name == "spectre":
            self.sf.write("simulator lang=spice\n")
        self.sf.write("* Delay stimulus for period of {0}n load={1}fF slew={2}ns\n\n".format(self.period,
                                                                                             self.load,
                                                                                             self.slew))
        self.stim = stimuli(self.sf, self.mf, self.corner)
        # include files in stimulus file
        self.stim.write_include(self.trim_sp_file)

        self.write_generic_stimulus()

        # generate data and addr signals
        self.sf.write("\n* Generation of data and address signals\n")
        self.gen_data()
        self.gen_addr()

        # generate control signals
        self.sf.write("\n* Generation of control signals\n")
        self.gen_control()

        self.sf.write("\n* Generation of Port clock signal\n")
        for port in self.all_ports:
            self.stim.gen_pulse(sig_name="CLK{0}".format(port),
                                v1=0,
                                v2=self.vdd_voltage,
                                offset=self.period,
                                period=self.period,
                                t_rise=self.slew,
                                t_fall=self.slew)

        self.sf.write(".include {0}".format(temp_meas))
        # self.load_all_measure_nets()
        self.write_delay_measures()
        # self.write_simulation_saves()

        # run until the end of the cycle time
        self.stim.write_control(self.cycle_times[-1] + self.period)

        self.sf.close()
        self.mf.close()

    def write_power_stimulus(self, trim):
        """ Creates a stimulus file to measure leakage power only.
        This works on the *untrimmed netlist*.
        """
        self.check_arguments()

        # creates and opens stimulus file for writing
        self.power_stim_sp = "power_stim.sp"
        temp_stim = path.join(self.output_path, self.power_stim_sp)
        self.sf = open(temp_stim, "w")
        self.sf.write("* Power stimulus for period of {0}n\n\n".format(self.period))

        # creates and opens measure file for writing
        self.power_meas_sp = "power_meas.sp"
        temp_meas = path.join(self.output_path, self.power_meas_sp)
        self.mf = open(temp_meas, "w")
        self.stim = stimuli(self.sf, self.mf, self.corner)

        # include UNTRIMMED files in stimulus file
        if trim:
            self.stim.write_include(self.trim_sp_file)
        else:
            self.stim.write_include(self.sim_sp_file)

        self.write_generic_stimulus()

        # generate data and addr signals
        self.sf.write("\n* Generation of data and address signals\n")
        for write_port in self.write_ports:
            for i in range(self.word_size + self.num_spare_cols):
                self.stim.gen_constant(sig_name="{0}{1}_{2} ".format(self.din_name, write_port, i),
                                       v_val=0)
        for port in self.all_ports:
            for i in range(self.bank_addr_size):
                self.stim.gen_constant(sig_name="{0}{1}_{2}".format(self.addr_name, port, i),
                                       v_val=0)

        # generate control signals
        self.sf.write("\n* Generation of control signals\n")
        for port in self.all_ports:
            self.stim.gen_constant(sig_name="CSB{0}".format(port), v_val=self.vdd_voltage)
            if port in self.readwrite_ports:
                self.stim.gen_constant(sig_name="WEB{0}".format(port), v_val=self.vdd_voltage)

        self.sf.write("\n* Generation of global clock signal\n")
        for port in self.all_ports:
            self.stim.gen_constant(sig_name="CLK{0}".format(port), v_val=0)

        self.sf.write(".include {}".format(temp_meas))
        self.write_power_measures()

        # run until the end of the cycle time
        self.stim.write_control(2 * self.period)

        self.sf.close()
        self.mf.close()

    def get_measure_variants(self, port, measure_obj, measure_type=None):
        """
        Checks the measurement object and calls respective function for
        related measurement inputs.
        """

        meas_type = type(measure_obj)
        if meas_type is delay_measure or meas_type is slew_measure:
            variant_tuple = self.get_delay_measure_variants(port, measure_obj)
        elif meas_type is power_measure:
            variant_tuple = self.get_power_measure_variants(port, measure_obj, measure_type)
        elif meas_type is voltage_when_measure:
            variant_tuple = self.get_volt_when_measure_variants(port, measure_obj)
        elif meas_type is voltage_at_measure:
            variant_tuple = self.get_volt_at_measure_variants(port, measure_obj)
        else:
            debug.error("Input function not defined for measurement type={0}".format(meas_type))
        # Removes port input from any object which does not use it. This shorthand only works if
        # the measurement has port as the last input. Could be implemented by measurement type or
        # remove entirely from measurement classes.
        if not measure_obj.has_port:
            variant_tuple = variant_tuple[:-1]
        return variant_tuple

    def get_delay_measure_variants(self, port, delay_obj):
        """
        Get the measurement values that can either vary from simulation to
        simulation (vdd, address) or port to port (time delays)
        """

        # Return value is intended to match the delay measure format:  trig_td, targ_td, vdd, port
        # vdd is arguably constant as that is true for a single lib file.
        if delay_obj.meta_str == sram_op.READ_ZERO:
            # Falling delay are measured starting from neg. clk edge. Delay adjusted to that.
            meas_cycle_delay = self.cycle_times[self.measure_cycles[port][delay_obj.meta_str]]
        elif delay_obj.meta_str == sram_op.READ_ONE:
            meas_cycle_delay = self.cycle_times[self.measure_cycles[port][delay_obj.meta_str]]
        else:
            debug.error("Unrecognized delay Index={0}".format(delay_obj.meta_str), 1)

        # These measurements have there time further delayed to the neg. edge of the clock.
        if delay_obj.meta_add_delay:
            meas_cycle_delay += self.period / 2

        return (meas_cycle_delay, meas_cycle_delay, self.vdd_voltage, port)

    def get_power_measure_variants(self, port, power_obj, operation):
        """Get the measurement values that can either vary port to port (time delays)"""

        # Return value is intended to match the power measure format:  t_initial, t_final, port
        t_initial = self.cycle_times[self.measure_cycles[port][power_obj.meta_str]]
        t_final = self.cycle_times[self.measure_cycles[port][power_obj.meta_str] + 1]

        return (t_initial, t_final, port)

    def get_volt_at_measure_variants(self, port, volt_meas):
        """
        Get the measurement values that can either vary port to port (time delays)
        """

        meas_cycle = self.cycle_times[self.measure_cycles[port][volt_meas.meta_str]]

        # Measurement occurs slightly into the next period so we know that the value
        # "stuck" after the end of the period -> current period start + 1.25*period
        at_time = meas_cycle + 1.25 * self.period

        return (at_time, port)

    def get_volt_when_measure_variants(self, port, volt_meas):
        """
        Get the measurement values that can either vary port to port (time delays)
        """

        # Only checking 0 value reads for now.
        t_trig = self.cycle_times[self.measure_cycles[port][sram_op.READ_ZERO]]

        return (t_trig, self.vdd_voltage, port)

    def write_delay_measures_read_port(self, port):
        """
        Write the measure statements to quantify the delay and power results for a read port.
        """

        # add measure statements for delays/slews
        for meas_list in self.read_meas_lists:
            for measure in meas_list:
                measure_variant_inp_tuple = self.get_measure_variants(port, measure, "read")
                measure.write_measure(self.stim, measure_variant_inp_tuple)

    def write_delay_measures_write_port(self, port):
        """
        Write the measure statements to quantify the power results for a write port.
        """

        # add measure statements for power
        for meas_list in self.write_meas_lists:
            for measure in meas_list:
                measure_variant_inp_tuple = self.get_measure_variants(port, measure, "write")
                measure.write_measure(self.stim, measure_variant_inp_tuple)

    def write_delay_measures(self):
        """
        Write the measure statements to quantify the delay and power results for all targeted ports.
        """

        self.sf.write("\n* Measure statements for delay and power\n")

        # Output some comments to aid where cycles start and
        # what is happening
        for comment in self.cycle_comments:
            self.mf.write("* {0}\n".format(comment))

        self.sf.write("\n")
        for read_port in self.targ_read_ports:
            self.mf.write("* Read ports {0}\n".format(read_port))
            self.write_delay_measures_read_port(read_port)

        for write_port in self.targ_write_ports:
            self.mf.write("* Write ports {0}\n".format(write_port))
            self.write_delay_measures_write_port(write_port)

    def load_pex_net(self, net: str):
        from subprocess import check_output, CalledProcessError
        prefix = (self.sram_instance_name + OPTS.hier_seperator).lower()
        if not net.lower().startswith(prefix) or not OPTS.use_pex or not OPTS.calibre_pex:
            return net
        original_net = net
        net = net[len(prefix):]
        net = net.replace(".", "_").replace("[", r"\[").replace("]", r"\]")
        for pattern in [r"\sN_{}_[MXmx]\S+_[gsd]".format(net), net]:
            try:
                match = check_output(["grep", "-m1", "-o", "-iE", pattern, self.sp_file])
                return prefix + match.decode().strip()
            except CalledProcessError:
                pass
        return original_net

    def load_all_measure_nets(self):
        measurement_nets = set()
        for port, meas in zip(self.targ_read_ports * len(self.read_meas_lists)
                              + self.targ_write_ports * len(self.write_meas_lists),
                              self.read_meas_lists + self.write_meas_lists):
            for measurement in meas:
                visited = getattr(measurement, 'pex_visited', False)
                for prop in ["trig_name_no_port", "targ_name_no_port"]:
                    if hasattr(measurement, prop):
                        net = getattr(measurement, prop).format(port)
                        if not visited:
                            net = self.load_pex_net(net)
                        setattr(measurement, prop, net)
                        measurement_nets.add(net)
                measurement.pex_visited = True
        self.measurement_nets = measurement_nets
        return measurement_nets

    def write_simulation_saves(self):
        for net in self.measurement_nets:
            self.sf.write(".plot V({0}) \n".format(net))
        probe_nets = set()
        sram_name = self.sram_instance_name
        col = self.bitline_column
        row = self.wordline_row
        for port in set(self.targ_read_ports + self.targ_write_ports):
            probe_nets.add("WEB{0}".format(port))
            probe_nets.add("{0}{2}w_en{1}".format(self.sram_instance_name, port, OPTS.hier_seperator))
            probe_nets.add("{0}{3}Xbank0{3}Xport_data{1}{3}Xwrite_driver_array{1}{3}Xwrite_driver{2}{3}en_bar".format(self.sram_instance_name,
                                                                                                                      port,
                                                                                                                      self.bitline_column,
                                                                                                                      OPTS.hier_seperator))
            probe_nets.add("{0}{3}Xbank0{3}br_{1}_{2}".format(self.sram_instance_name,
                                                              port,
                                                              self.bitline_column,
                                                              OPTS.hier_seperator))
            if not OPTS.use_pex:
                continue
            probe_nets.add(
                "{0}{3}vdd_Xbank0_Xbitcell_array_xbitcell_array_xbit_r{1}_c{2}".format(sram_name,
                                                                                       row,
                                                                                       col - 1,
                                                                                       OPTS.hier_seperator))
            probe_nets.add(
                "{0}{3}p_en_bar{1}_Xbank0_Xport_data{1}_Xprecharge_array{1}_Xpre_column_{2}".format(sram_name,
                                                                                                    port,
                                                                                                    col,
                                                                                                    OPTS.hier_seperator))
            probe_nets.add(
                "{0}{3}vdd_Xbank0_Xport_data{1}_Xprecharge_array{1}_xpre_column_{2}".format(sram_name,
                                                                                            port,
                                                                                            col,
                                                                                            OPTS.hier_seperator))
            probe_nets.add("{0}{3}vdd_Xbank0_Xport_data{1}_Xwrite_driver_array{1}_xwrite_driver{2}".format(sram_name,
                                                                                                           port,
                                                                                                           col,
                                                                                                           OPTS.hier_seperator))
        probe_nets.update(self.measurement_nets)
        for net in probe_nets:
            debug.info(2, "Probe: {0}".format(net))
            self.sf.write(".plot V({0}) \n".format(self.load_pex_net(net)))

    def write_power_measures(self):
        """
        Write the measure statements to quantify the leakage power only.
        """

        self.sf.write("\n* Measure statements for idle leakage power\n")

        # add measure statements for power
        # TODO: Convert to measure statement insted of using stimuli
        # measure = power_measure('leakage_power',
        t_initial = self.period
        t_final = 2 * self.period
        self.stim.gen_meas_power(meas_name="leakage_power",
                                 t_initial=t_initial,
                                 t_final=t_final)

    def find_feasible_period_one_port(self, port):
        """
        Uses an initial period and finds a feasible period before we
        run the binary search algorithm to find min period. We check if
        the given clock period is valid and if it's not, we continue to
        double the period until we find a valid period to use as a
        starting point.
        """
        debug.check(port in self.read_ports, "Characterizer requires a read port to determine a period.")

        feasible_period = float(tech.spice["feasible_period"])
        time_out = 9
        while True:
            time_out -= 1
            if (time_out <= 0):
                debug.error("Timed out, could not find a feasible period.", 2)

            # Write ports are assumed non-critical to timing, so the first available is used
            self.targ_write_ports = [self.write_ports[0]]
            # Set target read port for simulation
            self.targ_read_ports = [port]

            debug.info(1, "Trying feasible period: {0}ns on Port {1}".format(feasible_period, port))
            self.period = feasible_period
            (success, results)=self.run_delay_simulation()

            # Clear these target ports after simulation
            self.targ_write_ports = []
            self.targ_read_ports = []

            if not success:
                feasible_period = 2 * feasible_period
                continue

            # Positions of measurements currently hardcoded. First 2 are delays, next 2 are slews
            feasible_delays = [results[port][mname] for mname in self.delay_meas_names if "delay" in mname]
            feasible_slews = [results[port][mname] for mname in self.delay_meas_names if "slew" in mname]
            delay_str = "feasible_delay {0:.4f}ns/{1:.4f}ns".format(*feasible_delays)
            slew_str = "slew {0:.4f}ns/{1:.4f}ns".format(*feasible_slews)
            debug.info(2, "feasible_period passed for Port {3}: {0}ns {1} {2} ".format(feasible_period,
                                                                                       delay_str,
                                                                                       slew_str,
                                                                                       port))

            if success:
                debug.info(2, "Found feasible_period for port {0}: {1}ns".format(port, feasible_period))
                self.period = feasible_period
                # Only return results related to input port.
                return results[port]

    def find_feasible_period(self):
        """
        Loops through all read ports determining the feasible period and collecting
        delay information from each port.
        """
        feasible_delays = [{} for i in self.all_ports]

        # Get initial feasible delays from first port
        feasible_delays[self.read_ports[0]] = self.find_feasible_period_one_port(self.read_ports[0])
        previous_period = self.period

        # Loops through all the ports checks if the feasible period works. Everything restarts it if does not.
        # Write ports do not produce delays which is why they are not included here.
        i = 1
        while i < len(self.read_ports):
            port = self.read_ports[i]
            # Only extract port values from the specified port, not the entire results.
            feasible_delays[port].update(self.find_feasible_period_one_port(port))
            # Function sets the period. Restart the entire process if period changes to collect accurate delays
            if self.period > previous_period:
                i = 0
            else:
                i+=1
            previous_period = self.period
        debug.info(1, "Found feasible_period: {0}ns".format(self.period))
        return feasible_delays

    def run_delay_simulation(self):
        """
        This tries to simulate a period and checks if the result works. If
        so, it returns True and the delays, slews, and powers.  It
        works on the trimmed netlist by default, so powers do not
        include leakage of all cells.
        """

        debug.check(self.period > 0, "Target simulation period non-positive")

        self.write_delay_stimulus()

        self.stim.run_sim(self.delay_stim_sp)

        return self.check_measurements()

    def check_measurements(self):
        """ Check the write and read measurements """

        # Loop through all targeted ports and collect delays and powers.
        result = [{} for i in self.all_ports]

        for port in self.targ_write_ports:
            if not self.check_bit_measures(self.write_bit_meas, port):
                return (False, {})

            debug.info(2, "Checking write values for port {0}".format(port))
            write_port_dict = {}
            for measure in self.write_lib_meas:
                write_port_dict[measure.name] = measure.retrieve_measure(port=port)

            if not check_dict_values_is_float(write_port_dict):
                debug.error("Failed to Measure Write Port Values:\n\t\t{0}".format(write_port_dict), 1)
            result[port].update(write_port_dict)

        for port in self.targ_read_ports:
            # First, check that the memory has the right values at the right times
            if not self.check_bit_measures(self.read_bit_meas, port):
                return (False, {})

            debug.info(2, "Checking read delay values for port {0}".format(port))
            # Check sen timing, then bitlines, then general measurements.
            if not self.check_sen_measure(port):
                return (False, {})

            if not self.check_read_debug_measures(port):
                return (False, {})

            # Check timing for read ports. Power is only checked if it was read correctly
            read_port_dict = {}
            for measure in self.read_lib_meas:
                read_port_dict[measure.name] = measure.retrieve_measure(port=port)

            if not self.check_valid_delays(read_port_dict):
                return (False, {})

            if not check_dict_values_is_float(read_port_dict):
                debug.error("Failed to Measure Read Port Values:\n\t\t{0}".format(read_port_dict), 1)

            result[port].update(read_port_dict)

            if self.sen_path_meas and self.bl_path_meas:
                self.path_delays = self.check_path_measures()

        return (True, result)

    def check_sen_measure(self, port):
        """Checks that the sen occurred within a half-period"""

        sen_val = self.sen_meas.retrieve_measure(port=port)
        debug.info(2, "s_en delay={0}ns".format(sen_val))
        if self.sen_meas.meta_add_delay:
            max_delay = self.period / 2
        else:
            max_delay = self.period
        return not (type(sen_val) != float or sen_val > max_delay)

    def check_read_debug_measures(self, port):
        """Debug measures that indicate special conditions."""

        # Currently, only check if the opposite than intended value was read during
        # the read cycles i.e. neither of these measurements should pass.
        # FIXME: these checks need to be re-done to be more robust against possible errors
        bl_vals = {}
        br_vals = {}
        for meas in self.bitline_volt_meas:
            val = meas.retrieve_measure(port=port)
            if self.bl_name == meas.targ_name_no_port:
                bl_vals[meas.meta_str] = val
            elif self.br_name == meas.targ_name_no_port:
                br_vals[meas.meta_str] = val

            debug.info(2, "{0}={1}".format(meas.name, val))

        dout_success = True
        bl_success = False
        for meas in self.dout_volt_meas:
            val = meas.retrieve_measure(port=port)
            debug.info(2, "{0}={1}".format(meas.name, val))
            debug.check(type(val)==float, "Error retrieving numeric measurement: {0} {1}".format(meas.name, val))

            if meas.meta_str == sram_op.READ_ONE and val < self.vdd_voltage * 0.1:
                dout_success = False
                debug.info(1, "Debug measurement failed. Value {0}V was read on read 1 cycle.".format(val))
                bl_success = self.check_bitline_meas(bl_vals[sram_op.READ_ONE], br_vals[sram_op.READ_ONE])
            elif meas.meta_str == sram_op.READ_ZERO and val > self.vdd_voltage * 0.9:
                dout_success = False
                debug.info(1, "Debug measurement failed. Value {0}V was read on read 0 cycle.".format(val))
                bl_success = self.check_bitline_meas(br_vals[sram_op.READ_ONE], bl_vals[sram_op.READ_ONE])

            # If the bitlines have a correct value while the output does not then that is a
            # sen error. FIXME: there are other checks that can be done to solidfy this conclusion.
            if not dout_success and bl_success:
                debug.error("Sense amp enable timing error. Increase the delay chain through the configuration file.", 1)

        return dout_success

    def check_bit_measures(self, bit_measures, port):
        """
        Checks the measurements which represent the internal storage voltages
        at the end of the read cycle.
        """
        success = False
        for polarity, meas_list in bit_measures.items():
            for meas in meas_list:
                val = meas.retrieve_measure(port=port)
                debug.info(2, "{0}={1}".format(meas.name, val))
                if type(val) != float:
                    continue
                meas_cycle = meas.meta_str
                # Loose error conditions. Assume it's not metastable but account for noise during reads.
                if (meas_cycle == sram_op.READ_ZERO and polarity == bit_polarity.NONINVERTING) or\
                   (meas_cycle == sram_op.READ_ONE and polarity == bit_polarity.INVERTING):
                    success = val < self.vdd_voltage / 2
                elif (meas_cycle == sram_op.READ_ZERO and polarity == bit_polarity.INVERTING) or\
                     (meas_cycle == sram_op.READ_ONE and polarity == bit_polarity.NONINVERTING):
                    success = val > self.vdd_voltage / 2
                elif (meas_cycle == sram_op.WRITE_ZERO and polarity == bit_polarity.INVERTING) or\
                     (meas_cycle == sram_op.WRITE_ONE and polarity == bit_polarity.NONINVERTING):
                    success = val > self.vdd_voltage / 2
                elif (meas_cycle == sram_op.WRITE_ONE and polarity == bit_polarity.INVERTING) or\
                     (meas_cycle == sram_op.WRITE_ZERO and polarity == bit_polarity.NONINVERTING):
                    success = val < self.vdd_voltage / 2
                if not success:
                    debug.info(1, ("Wrong value detected on probe bit during read/write cycle. "
                                   "Check writes and control logic for bugs.\n measure={0}, op={1}, "
                                   "bit_storage={2}, V(bit)={3}").format(meas.name, meas_cycle.name, polarity.name, val))

        return success

    def check_bitline_meas(self, v_discharged_bl, v_charged_bl):
        """
        Checks the value of the discharging bitline. Confirms s_en timing errors.
        Returns true if the bitlines are at there their value.
        """
        # The inputs looks at discharge/charged bitline rather than left or right (bl/br)
        # Performs two checks, discharging bitline is at least 10% away from vdd and there is a
        # 10% vdd difference between the bitlines. Both need to fail to be considered a s_en error.
        min_dicharge = v_discharged_bl < self.vdd_voltage * 0.9
        min_diff = (v_charged_bl - v_discharged_bl) > self.vdd_voltage * 0.1

        debug.info(1, "min_dicharge={0}, min_diff={1}".format(min_dicharge, min_diff))
        return (min_dicharge and min_diff)

    def check_path_measures(self):
        """Get and check all the delays along the sen and bitline paths"""

        # Get and set measurement, no error checking done other than prints.
        debug.info(2, "Checking measures in Delay Path")
        value_dict = {}
        for meas in self.sen_path_meas + self.bl_path_meas:
            val = meas.retrieve_measure()
            debug.info(2, '{0}={1}'.format(meas.name, val))
            if type(val) != float or val > self.period / 2:
                debug.info(1, 'Failed measurement:{}={}'.format(meas.name, val))
            value_dict[meas.name] = val
        # debug.info(0, "value_dict={}".format(value_dict))
        return value_dict

    def run_power_simulation(self):
        """
        This simulates a disabled SRAM to get the leakage power when it is off.
        """

        debug.info(1, "Performing leakage power simulations.")
        self.write_power_stimulus(trim=False)
        self.stim.run_sim(self.power_stim_sp)
        leakage_power=parse_spice_list("timing", "leakage_power")
        debug.check(leakage_power!="Failed", "Could not measure leakage power.")
        debug.info(1, "Leakage power of full array is {0} mW".format(leakage_power * 1e3))
        # debug
        # sys.exit(1)

        self.write_power_stimulus(trim=True)
        self.stim.run_sim(self.power_stim_sp)
        trim_leakage_power=parse_spice_list("timing", "leakage_power")
        debug.check(trim_leakage_power!="Failed", "Could not measure leakage power.")
        debug.info(1, "Leakage power of trimmed array is {0} mW".format(trim_leakage_power * 1e3))

        # For debug, you sometimes want to inspect each simulation.
        # key=raw_input("press return to continue")
        return (leakage_power * 1e3, trim_leakage_power * 1e3)

    def check_valid_delays(self, result_dict):
        """ Check if the measurements are defined and if they are valid. """

        # Hard coded names currently
        delay_hl = result_dict["delay_hl"]
        delay_lh = result_dict["delay_lh"]
        slew_hl = result_dict["slew_hl"]
        slew_lh = result_dict["slew_lh"]
        period_load_slew_str = "period {0} load {1} slew {2}".format(self.period, self.load, self.slew)

        # if it failed or the read was longer than a period
        if type(delay_hl)!=float or type(delay_lh)!=float or type(slew_lh)!=float or type(slew_hl)!=float:
            delays_str = "delay_hl={0} delay_lh={1}".format(delay_hl, delay_lh)
            slews_str = "slew_hl={0} slew_lh={1}".format(slew_hl, slew_lh)
            debug.info(2, "Failed simulation (in sec):\n\t\t{0}\n\t\t{1}\n\t\t{2}".format(period_load_slew_str,
                                                                                          delays_str,
                                                                                          slews_str))
            return False

        delays_str = "delay_hl={0} delay_lh={1}".format(delay_hl, delay_lh)
        slews_str = "slew_hl={0} slew_lh={1}".format(slew_hl, slew_lh)
        # high-to-low delays start at neg. clk edge, so they need to be less than half_period
        half_period = self.period / 2
        if abs(delay_hl)>half_period or abs(delay_lh)>half_period or abs(slew_hl)>half_period or abs(slew_lh)>self.period \
           or (delay_hl<0 and delay_lh<0) or slew_hl<0 or slew_lh<0:
            debug.info(2, "UNsuccessful simulation (in ns):\n\t\t{0}\n\t\t{1}\n\t\t{2}".format(period_load_slew_str,
                                                                                               delays_str,
                                                                                               slews_str))
            return False
        else:
            debug.info(2, "Successful simulation (in ns):\n\t\t{0}\n\t\t{1}\n\t\t{2}".format(period_load_slew_str,
                                                                                             delays_str,
                                                                                             slews_str))

        if delay_lh < 0 and delay_hl > 0:
            result_dict["delay_lh"] = result_dict["delay_hl"]
            debug.info(2, "delay_lh captured precharge, using delay_hl instead")
        elif delay_hl < 0 and delay_lh > 0:
            result_dict["delay_hl"] = result_dict["delay_lh"]
            debug.info(2, "delay_hl captured precharge, using delay_lh instead")

        return True

    def find_min_period(self, feasible_delays):
        """
        Determine a single minimum period for all ports.
        """

        feasible_period = ub_period = self.period
        lb_period = 0.0
        target_period = 0.5 * (ub_period + lb_period)

        # Find the minimum period for all ports. Start at one port and perform binary search then use that delay as a starting position.
        # For testing purposes, only checks read ports.
        for port in self.read_ports:
            target_period = self.find_min_period_one_port(feasible_delays, port, lb_period, ub_period, target_period)
            # The min period of one port becomes the new lower bound. Reset the upper_bound.
            lb_period = target_period
            ub_period = feasible_period

        # Clear the target ports before leaving
        self.targ_read_ports = []
        self.targ_write_ports = []
        return target_period

    def find_min_period_one_port(self, feasible_delays, port, lb_period, ub_period, target_period):
        """
        Searches for the smallest period with output delays being within 5% of
        long period. For the current logic to characterize multiport, bounds are required as an input.
        """

        # previous_period = ub_period = self.period
        # ub_period = self.period
        # lb_period = 0.0
        # target_period = 0.5 * (ub_period + lb_period)

        # Binary search algorithm to find the min period (max frequency) of input port
        time_out = 25
        # Write ports are assumed non-critical to timing, so the first available is used
        self.targ_write_ports = [self.write_ports[0]]
        self.targ_read_ports = [port]
        while True:
            time_out -= 1
            if (time_out <= 0):
                debug.error("Timed out, could not converge on minimum period.", 2)

            self.period = target_period
            debug.info(1, "MinPeriod Search Port {3}: {0}ns (ub: {1} lb: {2})".format(target_period,
                                                                                      ub_period,
                                                                                      lb_period,
                                                                                      port))

            if self.try_period(feasible_delays):
                ub_period = target_period
            else:
                lb_period = target_period

            if relative_compare(ub_period, lb_period, error_tolerance=0.05):
                # ub_period is always feasible.
                return ub_period

            # Update target
            target_period = 0.5 * (ub_period + lb_period)
            # key=input("press return to continue")

    def try_period(self, feasible_delays):
        """
        This tries to simulate a period and checks if the result
        works. If it does and the delay is within 5% still, it returns True.
        """

        # Run Delay simulation but Power results not used.
        (success, results) = self.run_delay_simulation()
        if not success:
            return False

        # Check the values of target readwrite and read ports. Write ports do not produce delays in this current version
        for port in self.targ_read_ports:
            # check that the delays and slews do not degrade with tested period.
            for dname in self.delay_meas_names:

                # FIXME: This is a hack solution to fix the min period search. The slew will always be based on the period when there
                # is a column mux. Therefore, the checks are skipped for this condition. This is hard to solve without changing the netlist.
                # Delays/slews based on the period will cause the min_period search to come to the wrong period.
                if self.sram.col_addr_size>0 and "slew" in dname:
                    continue

                if not relative_compare(results[port][dname], feasible_delays[port][dname], error_tolerance=0.05):
                    debug.info(2, "Delay too big {0} vs {1}".format(results[port][dname], feasible_delays[port][dname]))
                    return False

            # key=raw_input("press return to continue")

            delay_str = ', '.join("{0}={1}ns".format(mname, results[port][mname]) for mname in self.delay_meas_names)
            debug.info(2, "Successful period {0}, Port {2}, {1}".format(self.period,
                                                                        delay_str,
                                                                        port))
        return True

    def set_probe(self, probe_address, probe_data):
        """
        Probe address and data can be set separately to utilize other
        functions in this characterizer besides analyze.
        Netlist reduced for simulation.
        """
        super().set_probe(probe_address, probe_data)

    def prepare_netlist(self):
        """ Prepare a trimmed netlist and regular netlist. """

        # Set up to trim the netlist here if that is enabled
        # TODO: Copy old netlist if memchar
        if OPTS.trim_netlist:
            #self.trim_sp_file = "{0}trimmed.sp".format(self.output_path)
            self.trim_sp_file = "{0}trimmed.sp".format(OPTS.openram_temp)
            # Only genrate spice when running openram process
            if OPTS.top_process != "memchar":
                self.sram.sp_write(self.trim_sp_file, lvs=False, trim=True)
        else:
            # The non-reduced netlist file when it is disabled
            self.trim_sp_file = "{0}sram.sp".format(self.output_path)

        # The non-reduced netlist file for power simulation
        self.sim_sp_file = "{0}sram.sp".format(self.output_path)
        # Make a copy in temp for debugging
        if self.sp_file != self.sim_sp_file:
            shutil.copy(self.sp_file, self.sim_sp_file)

    def recover_measurment_objects(self):
        mf_path = path.join(OPTS.output_path, "delay_meas.sp")
        self.sen_path_meas = None
        self.bl_path_meas = None
        if not path.exists(mf_path):
            debug.info(1, "Delay measure file not found. Skipping measure recovery")
            return
        mf = open(mf_path, "r")
        measure_text = mf.read()
        port_iter = re.finditer(r"\* (Read|Write) ports (\d*)", measure_text)
        port_measure_lines = []
        loc = 0
        port_name = ''
        for port in port_iter:
            port_measure_lines.append((port_name, measure_text[loc:port.end(0)]))
            loc = port.start(0)
            port_name = port.group(1) + port.group(2)

        mf.close()
        # Cycle comments, not sure if i need this
        # cycle_lines = port_measure_lines.pop(0)[1]
        # For now just recover the bit_measures and sen_and_bitline_path_measures
        self.read_meas_lists.append([])
        self.read_bit_meas = {bit_polarity.NONINVERTING: [], bit_polarity.INVERTING: []}
        self.write_bit_meas = {bit_polarity.NONINVERTING: [], bit_polarity.INVERTING: []}
#        bit_measure_rule = re.compile(r"\.meas tran (v_q_a\d+_b\d+_(read|write)_(zero|one)\d+) FIND v\((.*)\) AT=(\d+(\.\d+)?)n")
#        for measures in port_measure_lines:
#            port_name = measures[0]
#            text = measures[1]
#            bit_measure_iter = bit_measure_rule.finditer(text)
#            for bit_measure in bit_measure_iter:
#                meas_name = bit_measure.group(1)
#                read = bit_measure.group(2) == "read"
#                cycle =  bit_measure.group(3)
#                probe = bit_measure.group(4)
#                polarity = bit_polarity.NONINVERTING
#                if "q_bar" in meas_name:
#                    polarity = bit_polarity.INVERTING
#                meas = voltage_at_measure(meas_name, probe)
#                if read:
#                    if cycle == "one":
#                        meas.meta_str = sram_op.READ_ONE
#                    else:
#                        meas.meta_str = sram_op.READ_ZERO
#                    self.read_bit_meas[polarity].append(meas)
#                    self.read_meas_lists[-1].append(meas)
#                else:
#                    if cycle == "one":
#                        meas.meta_str = sram_op.WRITE_ONE
#                    else:
#                        meas.meta_str = sram_op.WRITE_ZERO
#                    self.write_bit_meas[polarity].append(meas)
#                    self.write_meas_lists[-1].append(meas)

        delay_path_rule = re.compile(r"\.meas tran delay_(.*)_to_(.*)_(sen|bl)_(id\d*) TRIG v\((.*)\) VAL=(\d+(\.\d+)?) (RISE|FALL)=(\d+) TD=(\d+(\.\d+)?)n TARG v\((.*)\) VAL=(\d+(\.\d+)?) (RISE|FALL)=(\d+) TD=(\d+(\.\d+)?)n")
        port = self.read_ports[0]
        meas_buff = []
        self.sen_path_meas = []
        self.bl_path_meas = []
        for measures in port_measure_lines:
            text = measures[1]
            delay_path_iter = delay_path_rule.finditer(text)
            for delay_path_measure in delay_path_iter:
                from_ = delay_path_measure.group(1)
                to_ = delay_path_measure.group(2)
                path_ = delay_path_measure.group(3)
                id_ = delay_path_measure.group(4)
                trig_rise = delay_path_measure.group(8)
                targ_rise = delay_path_measure.group(15)
                meas_name = "delay_{0}_to_{1}_{2}_{3}".format(from_, to_, path_, id_)
                meas = delay_measure(meas_name, from_, to_, trig_rise, targ_rise, measure_scale=1e9, has_port=False)
                meas.meta_str = sram_op.READ_ZERO
                meas.meta_add_delay = True
                meas_buff.append(meas)
                if path_ == "sen":
                    self.sen_path_meas.extend(meas_buff.copy())
                    meas_buff.clear()
                elif path_ == "bl":
                    self.bl_path_meas.extend(meas_buff.copy())
                    meas_buff.clear()
        self.read_meas_lists.append(self.sen_path_meas + self.bl_path_meas)

    def set_spice_names(self):
        """This is run in place of set_internal_spice_names function from
        simulation.py when running stand-alone characterizer."""
        self.bl_name = OPTS.bl_format.format(name=self.sram.name,
                                             hier_sep=OPTS.hier_seperator,
                                             row="{}",
                                             col=self.bitline_column)
        self.br_name = OPTS.br_format.format(name=self.sram.name,
                                             hier_sep=OPTS.hier_seperator,
                                             row="{}",
                                             col=self.bitline_column)
        self.sen_name = OPTS.sen_format.format(name=self.sram.name,
                                               hier_sep=OPTS.hier_seperator)
        self.cell_name = OPTS.cell_format.format(name=self.sram.name,
                                                 hier_sep=OPTS.hier_seperator,
                                                 row="{}",
                                                 col="{}")

    def analysis_init(self, probe_address, probe_data):
        """Sets values which are dependent on the data address/bit being tested."""

        self.set_probe(probe_address, probe_data)
        self.prepare_netlist()
        if OPTS.top_process == "memchar":
            self.set_spice_names()
            self.create_measurement_names()
            self.create_measurement_objects()
            self.recover_measurment_objects()
        else:
            self.create_graph()
            self.set_internal_spice_names()
            self.create_measurement_names()
            self.create_measurement_objects()

    def analyze(self, probe_address, probe_data, load_slews):
        """
        Main function to characterize an SRAM for a table. Computes both delay and power characterization.
        """

        # Dict to hold all characterization values
        char_sram_data = {}
        self.analysis_init(probe_address, probe_data)
        loads = []
        slews = []
        for load, slew in load_slews:
            loads.append(load)
            slews.append(slew)
        self.load=max(loads)
        self.slew=max(slews)

        # 1) Find a feasible period and it's corresponding delays using the trimmed array.
        feasible_delays = self.find_feasible_period()

        # 2) Finds the minimum period without degrading the delays by X%
        self.set_load_slew(max(loads), max(slews))
        min_period = self.find_min_period(feasible_delays)
        debug.check(type(min_period)==float, "Couldn't find minimum period.")
        debug.info(1, "Min Period Found: {0}ns".format(min_period))
        char_sram_data["min_period"] = round_time(min_period)

        # 3) Find the leakage power of the trimmmed and  UNtrimmed arrays.
        (full_array_leakage, trim_array_leakage)=self.run_power_simulation()
        char_sram_data["leakage_power"]=full_array_leakage
        leakage_offset = full_array_leakage - trim_array_leakage
        # 4) At the minimum period, measure the delay, slew and power for all slew/load pairs.
        self.period = min_period
        char_port_data = self.simulate_loads_and_slews(load_slews, leakage_offset)
        if OPTS.use_specified_load_slew is not None and len(load_slews) > 1:
            debug.warning("Path delay lists not correctly generated for characterizations of more than 1 load,slew")
        # Get and save the path delays
        if self.sen_path_meas and self.bl_path_meas:
            bl_names, bl_delays, sen_names, sen_delays = self.get_delay_lists(self.path_delays)
        # Removed from characterization output temporarily
        # char_sram_data["bl_path_measures"] = bl_delays
        # char_sram_data["sen_path_measures"] = sen_delays
        # char_sram_data["bl_path_names"] = bl_names
        # char_sram_data["sen_path_names"] = sen_names
        # FIXME: low-to-high delays are altered to be independent of the period. This makes the lib results less accurate.
        self.alter_lh_char_data(char_port_data)

        return (char_sram_data, char_port_data)

    def alter_lh_char_data(self, char_port_data):
        """Copies high-to-low data to low-to-high data to make them consistent on the same clock edge."""

        # This is basically a hack solution which should be removed/fixed later.
        for port in self.all_ports:
            char_port_data[port]['delay_lh'] = char_port_data[port]['delay_hl']
            char_port_data[port]['slew_lh'] = char_port_data[port]['slew_hl']

    def simulate_loads_and_slews(self, load_slews, leakage_offset):
        """Simulate all specified output loads and input slews pairs of all ports"""

        measure_data = self.get_empty_measure_data_dict()
        # Set the target simulation ports to all available ports. This make sims slower but failed sims exit anyways.
        self.targ_read_ports = self.read_ports
        self.targ_write_ports = self.write_ports
        for load, slew in load_slews:
            self.set_load_slew(load, slew)
            # Find the delay, dynamic power, and leakage power of the trimmed array.
            (success, delay_results) = self.run_delay_simulation()
            debug.check(success, "Couldn't run a simulation. slew={0} load={1}\n".format(self.slew, self.load))
            debug.info(1, "Simulation Passed: Port {0} slew={1} load={2}".format("All", self.slew, self.load))
            # The results has a dict for every port but dicts can be empty (e.g. ports were not targeted).
            for port in self.all_ports:
                for mname, value in delay_results[port].items():
                    if "power" in mname:
                        # Subtract partial array leakage and add full array leakage for the power measures
                        debug.info(1, "Adding leakage offset to {0} {1} + {2} = {3}".format(mname, value, leakage_offset, value + leakage_offset))
                        measure_data[port][mname].append(value + leakage_offset)
                    else:
                        measure_data[port][mname].append(value)
        return measure_data

    def get_delay_lists(self, value_dict):
        """Returns dicts for path measures of bitline and sen paths"""
        sen_name_list = []
        sen_delay_list = []
        for meas in self.sen_path_meas:
            sen_name_list.append(meas.name)
            sen_delay_list.append(value_dict[meas.name])

        bl_name_list = []
        bl_delay_list = []
        for meas in self.bl_path_meas:
            bl_name_list.append(meas.name)
            bl_delay_list.append(value_dict[meas.name])

        return sen_name_list, sen_delay_list, bl_name_list, bl_delay_list

    def calculate_inverse_address(self):
        """Determine dummy test address based on probe address and column mux size."""

        # The inverse address needs to share the same bitlines as the probe address as the trimming will remove all other bitlines
        # This is only an issue when there is a column mux and the address maps to different bitlines.
        column_addr = self.get_column_addr() # do not invert this part
        inverse_address = ""
        for c in self.probe_address[self.sram.col_addr_size:]: # invert everything else
            if c=="0":
                inverse_address += "1"
            elif c=="1":
                inverse_address += "0"
            else:
                debug.error("Non-binary address string", 1)
        return inverse_address + column_addr

    def gen_test_cycles_one_port(self, read_port, write_port):
        """Sets a list of key time-points [ns] of the waveform (each rising edge)
        of the cycles to do a timing evaluation of a single port """

        # Create the inverse address for a scratch address
        inverse_address = self.calculate_inverse_address()

        # For now, ignore data patterns and write ones or zeros
        data_ones = "1" * (self.word_size + self.num_spare_cols)
        data_zeros = "0" * (self.word_size + self.num_spare_cols)
        wmask_ones = "1" * self.num_wmasks

        if self.t_current == 0:
            self.add_noop_all_ports("Idle cycle (no positive clock edge)")

        self.add_write("W data 1 address {0}".format(inverse_address),
                       inverse_address,
                       data_ones,
                       wmask_ones,
                       write_port)

        self.add_write("W data 0 address {0} to write value".format(self.probe_address),
                       self.probe_address,
                       data_zeros,
                       wmask_ones,
                       write_port)
        self.measure_cycles[write_port][sram_op.WRITE_ZERO] = len(self.cycle_times) - 1

        self.add_noop_clock_one_port(write_port)
        self.measure_cycles[write_port]["disabled_write0"] = len(self.cycle_times) - 1

        # This also ensures we will have a H->L transition on the next read
        self.add_read("R data 1 address {0} to set dout caps".format(inverse_address),
                      inverse_address,
                      read_port)

        self.add_read("R data 0 address {0} to check W0 worked".format(self.probe_address),
                      self.probe_address,
                      read_port)
        self.measure_cycles[read_port][sram_op.READ_ZERO] = len(self.cycle_times) - 1

        self.add_noop_clock_one_port(read_port)
        self.measure_cycles[read_port]["disabled_read0"] = len(self.cycle_times) - 1

        self.add_noop_all_ports("Idle cycle (if read takes >1 cycle)")

        self.add_write("W data 1 address {0} to write value".format(self.probe_address),
                       self.probe_address,
                       data_ones,
                       wmask_ones,
                       write_port)
        self.measure_cycles[write_port][sram_op.WRITE_ONE] = len(self.cycle_times) - 1

        self.add_noop_clock_one_port(write_port)
        self.measure_cycles[write_port]["disabled_write1"] = len(self.cycle_times) - 1

        self.add_write("W data 0 address {0} to clear din caps".format(inverse_address),
                       inverse_address,
                       data_zeros,
                       wmask_ones,
                       write_port)

        self.add_noop_clock_one_port(read_port)
        self.measure_cycles[read_port]["disabled_read1"] = len(self.cycle_times) - 1

        # This also ensures we will have a L->H transition on the next read
        self.add_read("R data 0 address {0} to clear dout caps".format(inverse_address),
                      inverse_address,
                      read_port)

        self.add_read("R data 1 address {0} to check W1 worked".format(self.probe_address),
                      self.probe_address,
                      read_port)
        self.measure_cycles[read_port][sram_op.READ_ONE] = len(self.cycle_times) - 1

        self.add_noop_all_ports("Idle cycle (if read takes >1 cycle))")

    def get_available_port(self, get_read_port):

        """Returns the first accessible read or write port. """
        if get_read_port and len(self.read_ports) > 0:
            return self.read_ports[0]
        elif not get_read_port and len(self.write_ports) > 0:
            return self.write_ports[0]
        return None

    def set_stimulus_variables(self):
        simulation.set_stimulus_variables(self)
        self.measure_cycles = [{} for port in self.all_ports]

    def create_test_cycles(self):
        """
        Returns a list of key time-points [ns] of the waveform (each rising edge)
        of the cycles to do a timing evaluation. The last time is the end of the simulation
        and does not need a rising edge.
        """

        # Using this requires setting at least one port to target for simulation.
        if len(self.targ_write_ports) == 0 or len(self.targ_read_ports) == 0:
            debug.error("Write and read port must be specified for characterization.", 1)
        self.set_stimulus_variables()

        # Get any available read/write port in case only a single write or read ports is being characterized.
        cur_read_port = self.get_available_port(get_read_port=True)
        cur_write_port = self.get_available_port(get_read_port=False)
        debug.check(cur_read_port is not None,
                    "Characterizer requires at least 1 read port")
        debug.check(cur_write_port is not None,
                    "Characterizer requires at least 1 write port")

        # Create test cycles for specified target ports.
        write_pos = 0
        read_pos = 0
        while True:
            # Exit when all ports have been characterized
            if write_pos >= len(self.targ_write_ports) and read_pos >= len(self.targ_read_ports):
                break

            # Select new write and/or read ports for the next cycle. Use previous port if none remaining.
            if write_pos < len(self.targ_write_ports):
                cur_write_port = self.targ_write_ports[write_pos]
                write_pos+=1
            if read_pos < len(self.targ_read_ports):
                cur_read_port = self.targ_read_ports[read_pos]
                read_pos+=1

            # Add test cycle of read/write port pair. One port could have been used already, but the other has not.
            self.gen_test_cycles_one_port(cur_read_port, cur_write_port)

    def gen_data(self):
        """ Generates the PWL data inputs for a simulation timing test. """

        for write_port in self.write_ports:
            for i in range(self.word_size + self.num_spare_cols):
                sig_name="{0}{1}_{2} ".format(self.din_name, write_port, i)
                self.stim.gen_pwl(sig_name, self.cycle_times, self.data_values[write_port][i], self.period, self.slew, 0.05)

    def gen_addr(self):
        """
        Generates the address inputs for a simulation timing test.
        This alternates between all 1's and all 0's for the address.
        """

        for port in self.all_ports:
            for i in range(self.bank_addr_size):
                sig_name = "{0}{1}_{2}".format(self.addr_name, port, i)
                self.stim.gen_pwl(sig_name, self.cycle_times, self.addr_values[port][i], self.period, self.slew, 0.05)

    def gen_control(self):
        """ Generates the control signals """

        for port in self.all_ports:
            self.stim.gen_pwl("CSB{0}".format(port), self.cycle_times, self.csb_values[port], self.period, self.slew, 0.05)
            if port in self.readwrite_ports:
                self.stim.gen_pwl("WEB{0}".format(port), self.cycle_times, self.web_values[port], self.period, self.slew, 0.05)
                if self.sram.num_wmasks:
                    for bit in range(self.sram.num_wmasks):
                        self.stim.gen_pwl("WMASK{0}_{1}".format(port, bit), self.cycle_times, self.wmask_values[port][bit], self.period, self.slew, 0.05)
