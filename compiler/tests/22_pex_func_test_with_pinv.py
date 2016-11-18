#!/usr/bin/env python2.7
"""
Run a regression test on an extracted SRAM to ensure functionality.
"""

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.get_opts()


@unittest.skip("SKIPPING 22_sram_func_test")
class sram_func_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))

        self.func_test(bank_num=1)
        self.func_test(bank_num=2)
        self.func_test(bank_num=4)

        globals.end_openram()
        
    def func_test(self, bank_num):

        import sram
        import tech

        debug.info(1, "Testing timing for sample 1bit, 16words SRAM with 1 bank")
        OPTS.check_lvsdrc = False
        OPTS.use_pex = True
        s = sram.sram(word_size=OPTS.config.word_size,
                      num_words=OPTS.config.num_words,
                      num_banks=OPTS.config.num_banks,
                      name="test_sram1")
        OPTS.check_lvsdrc = True
        OPTS.use_pex = False

        tempspice = OPTS.openram_temp + "temp.sp"
        tempgds = OPTS.openram_temp + "temp.gds"

        s.sp_write(tempspice)
        s.gds_write(tempgds)

        self.assertFalse(calibre.run_drc(s.name, tempgds))
        self.assertFalse(calibre.run_lvs(s.name, tempgds, tempspice))
        self.assertFalse(calibre.run_pex(s.name, tempgds,
                                         tempspice, output=OPTS.openram_temp + "temp_pex.sp"))

        import sp_file
        stimulus_file = OPTS.openram_temp + "stimulus.sp"
        a_stimulus = sp_file.sp_file(stimulus_file)
        self.write_stimulus(a_stimulus)

        simulator_file = OPTS.openram_temp + "simulator.sp"
        a_simulator = sp_file.sp_file(simulator_file)
        self.write_simulator(a_simulator)

        result_file = OPTS.openram_temp + "result"

        import os

        if OPTS.spice_version == "hspice":
            cmd = "hspice -mt 36 -i {0} > {1} ".format(
                simulator_file, result_file)
        else:
            cmd = "ngspice -b  -i {0} > {1}  ".format(
                simulator_file, result_file)
        os.system(cmd)

        import re
        sp_result = open(result_file, "r")
        contents = sp_result.read()
        key = "vr1"
        val = re.search(
            r"{0}(\s*)=(\s*)(\d*(.).*)(\s*)(from)".format(key), contents)
        val = val.group(3)
        value1 = float(self.convert_voltage_unit(val))

        key = "vr2"
        val = re.search(
            r"{0}(\s*)=(\s*)(\d*(.).*)(\s*)(from)".format(key), contents)
        val = val.group(3)
        value2 = float(self.convert_voltage_unit(val))

        self.assertTrue(round(value1) > 0.5 * tech.spice["supply_voltage"])
        self.assertTrue(round(value2) < 0.5 * tech.spice["supply_voltage"])

        OPTS.check_lvsdrc = True

    def convert_voltage_unit(self, string):
        newstring = ""
        for letter in string:
            if letter == "m":
                letter = "10e-3"
            elif letter == "u":
                letter = "10e-6"
            else:
                letter = letter
            newstring = str(newstring) + str(letter)
        return newstring

    def convert_time_unit(self, string):
        newstring = ""
        for letter in string:
            if letter == "f":
                letter = "10e-15"
            elif letter == "p":
                letter = "10e-12"
            elif letter == "n":
                letter = "10e-9"
            elif letter == "u":
                letter = "10e-6"
            elif letter == "m":
                letter = "10e-3"
            else:
                letter = letter
            newstring = str(newstring) + str(letter)
        return newstring

    def write_simulator(self, sim_file):
        sim_file.write("\n")
        import tech
        time_step = tech.spice["clock_period"]
        for model in tech.spice["fet_models"]:
            sim_file.write(".inc " + str(model) + "\n")
        sim_file.write(".inc stimulus.sp\n")
        sim_file.write(".inc temp_pex.sp\n")
        sim_file.write(".options post runlvl=6\n")
        sim_file.write("\n")

        sim_file.write(
            "Xsource DATA[0] ADDR[0] ADDR[1] ADDR[2] ADDR[3] CSb WEb WEb_inv OEb clk vdd vss source\n")
        sim_file.write(
            "Xsram DATA[0] ADDR[0] ADDR[1] ADDR[2] ADDR[3] CSb WEb OEb clk vdd vss test_sram1\n")
        sim_file.write("\n")

        sim_file.write(".MEASURE TRAN vr1 AVG V(DATA[0]) FROM ={0}ns TO ={1}ns\n".format(
            4.5 * tech.spice["clock_period"], 5 * tech.spice["clock_period"]))
        sim_file.write(".MEASURE TRAN vr2 AVG V(DATA[0]) FROM ={0}ns TO ={1}ns\n".format(
            9.5 * tech.spice["clock_period"], 10 * tech.spice["clock_period"]))
        sim_file.write("\n")

        if OPTS.spice_version == "hspice":
            sim_file.write(".probe v(x*.*)\n")
            sim_file.write(".tran 0.1ns {0}ns\n".format(
                10 * tech.spice["clock_period"]))
            sim_file.write(".end\n")
        else:
            sim_file.write(
                ".meas tran DELAY1.0 TRIG v(clk) VAL=0.5 RISE=6 TARG v(DATA[0]) VAL=0.5 TD=0.5n RISE=1\n")
            sim_file.write(".tran 0.1ns {0}ns\n".format(
                10 * tech.spice["clock_period"]))
            sim_file.write(".control\n")
            sim_file.write("run\n")
            #sim_file.write("plot CSb WEb OEb \n")
            #sim_file.write("plot clk DATA0 \n")
            sim_file.write("quit\n")
            sim_file.write(".endc\n")
            sim_file.write(".end\n")
        sim_file.file.close()

    def write_stimulus(self, sti_file):
        import tech
        import sp_file
        sti_file.write(
            ".subckt source DATA[0] ADDR[0] ADDR[1] ADDR[2] ADDR[3] CSb WEb WEb_inv OEb clk vdd vss\n")

        time_step = tech.spice["clock_period"]

        clk = sp_file.PWL(name="clk", port=["clk", "0"])
        for i in range(0, 11):
            clk.write_pulse(i * time_step, time_step, "UP")
        clk.write_to_sp(sti_file)

        WEB_inv = sp_file.PWL(name="WEb_inv", port=["WEb_inv", "0"])
        WEB = sp_file.PWL(name="WEB", port=["WEb", "0"])
        OEb = sp_file.PWL(name="OEb", port=["OEb", "0"])
        CSb = sp_file.PWL(name="CSb", port=["CSb", "0"])

        # write
        CSb.write_pulse(0.75 * time_step, time_step, "DN")
        WEB.write_pulse(0.75 * time_step, time_step, "DN")
        WEB_inv.write_pulse(0.75 * time_step, time_step, "UP")
        CSb.write_pulse(1.75 * time_step, time_step, "DN")
        WEB.write_pulse(1.75 * time_step, time_step, "DN")
        WEB_inv.write_pulse(1.75 * time_step, time_step, "UP")

        # read
        OEb.write_pulse(3.75 * time_step, time_step, "DN")
        CSb.write_pulse(3.75 * time_step, time_step, "DN")

        # write
        CSb.write_pulse(5.75 * time_step, time_step, "DN")
        WEB.write_pulse(5.75 * time_step, time_step, "DN")
        WEB_inv.write_pulse(5.75 * time_step, time_step, "UP")
        CSb.write_pulse(6.75 * time_step, time_step, "DN")
        WEB.write_pulse(6.75 * time_step, time_step, "DN")
        WEB_inv.write_pulse(6.75 * time_step, time_step, "UP")

        # read
        OEb.write_pulse(8.75 * time_step, time_step, "DN")
        CSb.write_pulse(8.75 * time_step, time_step, "DN")

        CSb.write_to_sp(sti_file)
        WEB.write_to_sp(sti_file)
        WEB_inv.write_to_sp(sti_file)
        OEb.write_to_sp(sti_file)

        sti_file.write("VA[0] A[0] 0 PWL(0n {0} {1}n {0} {2}n 0 {3}n 0 {4}n {0})\n".format(tech.spice["supply_voltage"], 8.875 * tech.spice[
                       "clock_period"], 13.875 * tech.spice["clock_period"], 14.5 * tech.spice["clock_period"], 14.501 * tech.spice["clock_period"]))
        sti_file.write("VA[1] A[1] 0 PWL(0n {0} {1}n {0} {2}n 0 {3}n 0 {4}n {0})\n".format(tech.spice["supply_voltage"], 8.875 * tech.spice[
                       "clock_period"], 13.875 * tech.spice["clock_period"], 14.5 * tech.spice["clock_period"], 14.501 * tech.spice["clock_period"]))
        sti_file.write("VA[2] A[2] 0 PWL(0n {0} {1}n {0} {2}n 0 {3}n 0 {4}n {0})\n".format(tech.spice["supply_voltage"], 8.875 * tech.spice[
                       "clock_period"], 13.875 * tech.spice["clock_period"], 14.5 * tech.spice["clock_period"], 14.501 * tech.spice["clock_period"]))
        sti_file.write("VA[3] A[3] 0 PWL(0n {0} {1}n {0} {2}n 0 {3}n 0 {4}n {0})\n".format(tech.spice["supply_voltage"], 8.875 * tech.spice[
                       "clock_period"], 13.875 * tech.spice["clock_period"], 14.5 * tech.spice["clock_period"], 14.501 * tech.spice["clock_period"]))

        sti_file.write(
            "xA[0]_buff A[0] ADDR[0]_inv ADDR[0] vdd vss test_buf\n")
        sti_file.write(
            "xA[1]_buff A[1] ADDR[1]_inv ADDR[1] vdd vss test_buf\n")
        sti_file.write(
            "xA[2]_buff A[2] ADDR[2]_inv ADDR[2] vdd vss test_buf\n")
        sti_file.write(
            "xA[3]_buff A[3] ADDR[3]_inv ADDR[3] vdd vss test_buf\n")

        VD_0 = sp_file.PWL(name="VD[0]", port=["D[0]", "0"])
        VD_0.write_pulse(0, 5 * time_step, "S1")
        VD_0.write_pulse(5 * time_step, 5 * time_step, "S0")
        VD_0.write_to_sp(sti_file)

        sti_file.write(
            "xD[0]_buff D[0] DATA[0]_inv DATA[0]s vdd vss test_buf\n")
        sti_file.write(
            "xD[0]_gate DATA[0]s WEb WEb_inv DATA[0] vdd vss tran_gate\n")
        sti_file.write("mp[0]_gate_vdd vdd write_v DATA[0] vdd " + str(tech.spice["pmos"]) +
                       " w=" + str(2 * tech.parameter["min_tx_size"]) + "u" +
                       " l=" + str(tech.drc["minlength_channel"]) + "u" +
                       "\n")
        sti_file.write("mn[0]_gate_vss vss write_g DATA[0] vss " + str(tech.spice["nmos"]) +
                       " w=" + str(tech.parameter["min_tx_size"]) + "u" +
                       " l=" + str(tech.drc["minlength_channel"]) + "u" +
                       "\n")

        Vwrite_v = sp_file.PWL(name="write_v", port=["write_vs", "0"])
        Vwrite_v.write_pulse(0, 0.5 * time_step, "S1")
        Vwrite_v.write_pulse(7.5 * time_step, time_step, "DN")
        Vwrite_v.write_to_sp(sti_file)
        sti_file.write(
            "xwrite_v write_vs  write_v_inv  write_v vdd vss test_buf\n")

        Vwrite_g = sp_file.PWL(name="write_g", port=["write_gs", "0"])
        Vwrite_g.write_pulse(0, 0.5 * time_step, "S0")
        Vwrite_g.write_pulse(3 * time_step, time_step, "UP")
        Vwrite_g.write_to_sp(sti_file)
        sti_file.write(
            "xwrite_g write_gs write_g_inv write_g vdd vss test_buf\n")

        sti_file.write("Vdd vdd 0 DC " +
                       str(tech.spice["supply_voltage"]) + "\n")
        sti_file.write("Vvss vss 0 DC 0\n")
        sti_file.write(".ENDS source\n")
        sti_file.write("\n")

        sti_file.write(".SUBCKT tran_gate in gate gate_inv out vdd vss\n")
        sti_file.write("mp0 in gate out vdd " + str(tech.spice["pmos"]) +
                       " w=" + str(2 * tech.parameter["min_tx_size"]) + "u" +
                       " l=" + str(tech.drc["minlength_channel"]) + "u" +
                       "\n")
        sti_file.write("mn0 in gate_inv out vss " + str(tech.spice["nmos"]) +
                       " w=" + str(tech.parameter["min_tx_size"]) + "u" +
                       " l=" + str(tech.drc["minlength_channel"]) + "u" +
                       "\n")
        sti_file.write(".ENDS tran_gate\n")
        sti_file.write("\n")

        sti_file.write(".SUBCKT test_buf in out_inv out_buf vdd vss\n")
        sti_file.write("mpinv1 out_inv in vdd vdd " + str(tech.spice["pmos"]) +
                       " w=" + str(2 * tech.parameter["min_tx_size"]) + "u" +
                       " l=" + str(tech.drc["minlength_channel"]) + "u" +
                       "\n")
        sti_file.write("mninv1 out_inv in vss vss " + str(tech.spice["nmos"]) +
                       " w=" + str(tech.parameter["min_tx_size"]) + "u" +
                       " l=" + str(tech.drc["minlength_channel"]) + "u" +
                       "\n")
        sti_file.write("mpinv2 out_buf out_inv vdd vdd " + str(tech.spice["pmos"]) +
                       " w=" + str(2 * tech.parameter["min_tx_size"]) + "u" +
                       " l=" + str(tech.drc["minlength_channel"]) + "u" +
                       "\n")
        sti_file.write("mninv2 out_buf out_inv vss vss " + str(tech.spice["nmos"]) +
                       " w=" + str(tech.parameter["min_tx_size"]) + "u" +
                       " l=" + str(tech.drc["minlength_channel"]) + "u" +
                       "\n")
        sti_file.write(".ENDS test_buf\n")
        sti_file.write("\n")

        sti_file.file.close()


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
