# See LICENSE for licensing information.
"""Simulator-free regressions for optional hard-macro characterization."""
import builtins
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import openram
from openram import OPTS
from testutils import header, openram_test


class characterization_contracts_test(openram_test):

    def runTest(self):
        config = Path(__file__).resolve().parent / "configs" / "config"
        openram.init_openram(str(config), is_unit_test=True)
        try:
            OPTS.netlist_only = True
            OPTS.trim_netlist = False
            OPTS.use_pex = False
            self.check_startup_file()
            self.check_explicit_probes()
        finally:
            openram.end_openram()

    def check_startup_file(self):
        """An absent optional PDK init is harmless; an unreadable one is not."""
        from openram.characterizer import stimuli
        stim = stimuli(io.StringIO(), io.StringIO(), ("TT", 1.0, 25))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pdk = root / "pdk"
            pdk.mkdir()
            with patch.object(OPTS, "openram_temp", str(root) + "/"), \
                    patch.object(OPTS, "spice_name", "ngspice"), \
                    patch.object(OPTS, "spice_exe", "/bin/true"), \
                    patch("subprocess.run", return_value=SimpleNamespace(returncode=0)), \
                    patch.dict(os.environ):
                os.environ.pop("SPICE_USERINIT_DIR", None)
                stim.run_sim("stim.sp")
                default = (root / ".spiceinit").read_text()
                self.assertIn("set num_threads=", default)

                os.environ["SPICE_USERINIT_DIR"] = str(pdk)
                stim.run_sim("stim.sp")
                self.assertEqual((root / ".spiceinit").read_text(), default)

                (pdk / ".spiceinit").write_text("* PDK startup\npre_osdi /models/psp.osdi\n")
                stim.run_sim("stim.sp")
                self.assertEqual((root / ".spiceinit").read_text(),
                                 "* PDK startup\npre_osdi /models/psp.osdi\n\n" + default)

                real_open = builtins.open

                def unreadable(file, *args, **kwargs):
                    if str(file) == str(pdk / ".spiceinit"):
                        raise PermissionError("unreadable PDK startup")
                    return real_open(file, *args, **kwargs)

                with patch("builtins.open", side_effect=unreadable):
                    with self.assertRaises(PermissionError):
                        stim.run_sim("stim.sp")

    def check_explicit_probes(self):
        """A bankless two-port macro supplies complete, independently indexed nodes."""
        from openram.characterizer import delay, stimuli
        from openram.characterizer.delay import bit_polarity, sram_op
        ports = [0, 1]
        macro = SimpleNamespace(
            name="hard_macro", word_size=2, write_size=2, num_spare_cols=0,
            num_spare_rows=0, num_words=64, num_banks=1, words_per_row=4,
            num_rows=16, num_cols=8, addr_size=6, col_addr_size=2,
            bank_addr_size=6, readwrite_ports=ports, read_ports=ports,
            write_ports=ports, all_ports=ports, pins=list(range(28)),
            get_characterization_probes=lambda row, col, port: {
                "bl": "xhard_macro.array.r{}_c{}.bl{}".format(row, col, port),
                "br": "xhard_macro.array.r{}_c{}.br{}".format(row, col, port),
                "sen": "xhard_macro.control{}.sense".format(port)},
            get_cell_name=lambda name, row, col: (
                "x{}.array.cell_{}_{}".format(name, row, col),
                SimpleNamespace(mod=SimpleNamespace(
                    get_storage_net_names=lambda: ["NT", "NC"]))))
        with tempfile.TemporaryDirectory() as directory:
            netlist = Path(directory) / "macro.sp"
            netlist.write_text("* bankless macro test fixture\n")
            char = delay(macro, str(netlist), ("TT", 1.0, 25),
                         output_path=directory + "/")
            char.period = 10.0
            for address, bit, row, col in [("010011", 1, 4, 7), ("100101", 0, 9, 1)]:
                char.analysis_init(address, bit)
                char.stim = stimuli(io.StringIO(), io.StringIO(), char.corner)
                for port in ports:
                    char.sen_meas.write_measure(char.stim, (0.0, 0.0, 1.0, port))
                    for measure in char.bitline_volt_meas:
                        measure.write_measure(char.stim, (0.5, port))
                text = char.stim.mf.getvalue()
                for port in ports:
                    self.assertIn("delay_sen{}".format(port), text)
                    self.assertIn("xhard_macro.control{}.sense)".format(port), text)
                    self.assertIn("xhard_macro.array.r{}_c{}.bl{})".format(row, col, port), text)
                    self.assertIn("xhard_macro.array.r{}_c{}.br{})".format(row, col, port), text)
                bit_measures = char.get_bit_measures("storage", address, bit)
                self.assertEqual({measure.targ_name_no_port for measure in bit_measures.values()},
                                 {"xhard_macro.array.cell_{}_{}.{}".format(row, col, node)
                                  for node in ["NT", "NC"]})

            values = {"delay_lh": 1.1, "delay_hl": 2.3,
                      "slew_lh": 0.4, "slew_hl": 0.6}
            result = dict(values)
            self.assertTrue(char.check_valid_delays(result))
            self.assertEqual(result, values)
            for edge in ("delay_lh", "delay_hl", "slew_lh", "slew_hl"):
                for invalid in (-0.1, float("nan"), float("inf")):
                    with self.subTest(edge=edge, invalid=invalid):
                        self.assertFalse(char.check_valid_delays(dict(values, **{edge: invalid})))

            class StorageMeasurement:
                name = "storage"
                meta_str = sram_op.READ_ZERO

                def __init__(self, value):
                    self.value = value

                def retrieve_measure(self, port):
                    return self.value

            for bad in (1.0, "Failed"):
                measures = {bit_polarity.NONINVERTING:
                            [StorageMeasurement(bad), StorageMeasurement(0.0)]}
                self.assertFalse(char.check_bit_measures(measures, 0))
            self.assertTrue(char.check_bit_measures(
                {bit_polarity.NONINVERTING: [StorageMeasurement(0.0)]}, 0))


if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    header(__file__, OPTS.tech_name)
    del sys.argv[1:]
    unittest.main()
