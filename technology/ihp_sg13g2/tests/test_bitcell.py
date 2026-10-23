"""Foundry SRAM hard-cell contracts, not complete-macro qualification.

Run inside IIC-OSIC after selecting SG13G2 and running import_sram.py.
"""

import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
os.environ["OPENRAM_HOME"] = str(ROOT / "compiler")
os.environ["OPENRAM_TECH"] = str(ROOT / "technology")
sys.path.insert(0, str(ROOT))
from common import make_openram_package
make_openram_package()
import openram
from openram import OPTS
from openram.sram_factory import factory


class FoundryBitcellTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="ihp-bitcell-")
        OPTS.tech_name = "ihp_sg13g2"
        OPTS.openram_temp = cls.temp.name + "/tmp/"
        OPTS.output_path = cls.temp.name + "/output/"
        openram.init_openram(str(ROOT / "compiler/tests/configs/config.py"), is_unit_test=True)
        # These tests exercise API/placement. Core-only arrays lack body taps;
        # their DRC results must not be confused with a complete SRAM array.
        OPTS.check_lvsdrc = False

    @classmethod
    def tearDownClass(cls):
        openram.end_openram()
        cls.temp.cleanup()

    def test_hard_cell(self):
        cell = factory.create(module_type="bitcell_1port")
        self.assertEqual(cell.cell_name, "cell_1rw")
        self.assertAlmostEqual(cell.width, 2.81)
        self.assertAlmostEqual(cell.height, 1.07)
        self.assertEqual(list(cell.pins), ["bl", "br", "wl", "vdd", "gnd"])
        self.assertEqual(cell.get_storage_net_names(), ["NT", "NC"])
        for name in ("bl", "br", "vdd", "gnd"):
            self.assertTrue(cell.get_pins(name))
            self.assertTrue(all(pin.layer == "m2" for pin in cell.get_pins(name)))
        self.assertEqual(cell.get_pin("wl").layer, "m3")
        self.assertEqual(len(cell.get_pins("gnd")), 2)

    def test_peripheral_hard_cells(self):
        import klayout.db as kdb
        source = kdb.Layout()
        source.read(str(Path(os.environ["PDKPATH"]) / "libs.ref/sg13g2_sram/gds/RM_IHPSG13_1P_64x16_c2.gds"))
        for name, original_name, width, height, shift, ports, vdd_pins in [
            ("ihp_bldrv", "RM_IHPSG13_1P_BLDRV", 4.08, 17.625, (510, 4725),
             ["br", "br_sel", "bl", "bl_sel", "pre_n", "sel_p", "wr_one", "wr_zero", "vdd", "gnd"], 2),
            ("ihp_sense_amp", "RSC_IHPSG13_DFPQD_MSAFFX2N", 9.69, 9.0, (510, 300),
             ["cp", "dn", "dp", "qn", "qp", "vdd", "gnd"], 1),
        ]:
            with self.subTest(cell=name):
                cell = factory.create(module_type=name)
                self.assertEqual(list(cell.pins), ports)
                self.assertAlmostEqual(cell.width, width)
                self.assertAlmostEqual(cell.height, height)
                for pin in cell.pins:
                    self.assertTrue(cell.get_pins(pin), pin)
                self.assertEqual(len(cell.get_pins("vdd")), vdd_pins)
                self.assertEqual(len(cell.get_pins("gnd")), 2)
                if name == "ihp_bldrv":
                    self.assertEqual(cell.get_pin("bl").layer, "m2")
                    self.assertEqual(cell.get_pin("bl_sel").layer, "m3")
                    self.assertAlmostEqual(cell.get_pin("bl").cx(), 1.15)
                else:
                    self.assertEqual(cell.get_pin("cp").layer, "m2")
                    self.assertEqual(cell.get_pin("dp").layer, "m1")
                    self.assertAlmostEqual(cell.get_pin("dp").cx(), 3.51)
                original = source.cell(original_name)
                path = Path(self.temp.name) / (name + ".gds")
                cell.gds_write(str(path))
                actual = kdb.Layout()
                actual.read(str(path))
                for index in source.layer_indexes():
                    info = source.get_info(index)
                    if info.datatype == 25 or (info.layer, info.datatype) == (189, 4):
                        continue
                    expected = kdb.Region(original.begin_shapes_rec(index)).transformed(kdb.Trans(*shift))
                    result = kdb.Region(actual.top_cell().begin_shapes_rec(actual.layer(info)))
                    with self.subTest(layer=str(info)):
                        self.assertEqual((expected ^ result).area(), 0)

    def test_peripheral_lvs(self):
        path = Path(self.temp.name)
        runner = Path(os.environ["PDKPATH"]) / "libs.tech/klayout/tech/lvs/run_lvs.py"
        for name in ("ihp_bldrv", "ihp_sense_amp", "ihp_column_data"):
            with self.subTest(cell=name):
                dut = factory.create(module_type=name)
                dut.gds_write(str(path / (name + ".gds")))
                dut.sp_write(str(path / (name + ".sp")))
                lines = (path / (name + ".sp")).read_text().splitlines()
                (path / (name + ".cdl")).write_text("\n".join(
                    "M" + line[1:] if line.startswith("X") and " sg13_lv_" in line else line
                    for line in lines) + "\n")
                command = [sys.executable, str(runner),
                           "--layout=" + str(path / (name + ".gds")),
                           "--netlist=" + str(path / (name + ".cdl")),
                           "--run_dir=" + str(path / (name + "-lvs")), "--disable_tap_extraction"]
                # BLDRV's separate rails are must-connect at parent level.
                # The sense amp and routed column match without implicit joins.
                if name == "ihp_bldrv":
                    command.append("--implicit_nets=vdd,gnd")
                run = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                self.assertIn("Congratulations! Netlists match.", run.stdout, run.stdout + run.stderr)

    def test_bldrv_controls(self):
        # Asymmetric read levels distinguish polarity swaps; deselected writes
        # must leave the externally biased bitlines untouched. Weak selected-
        # line pulldowns make off vs on observable rather than floating.
        cases = [
            ("precharge_offselect", 0, 0, 0, 0, None, (1, 1, 0, 0)),
            ("precharge_selected", 0, 1, 0, 0, None, (1, 1, 1, 1)),
            ("write_one", 1, 1, 1, 0, None, (1, 0, 1, 0)),
            ("write_zero", 1, 1, 0, 1, None, (0, 1, 0, 1)),
            ("read_selected", 1, 1, 0, 0, (.9, .7), (.9, .7, .9, .7)),
            ("read_deselected", 1, 0, 0, 0, (.9, .7), (.9, .7, 0, 0)),
            ("write_deselected", 1, 0, 1, 0, (.3, .8), (.3, .8, 0, 0)),
        ]
        dut = factory.create(module_type="ihp_bldrv")
        path = Path(self.temp.name)
        dut.sp_write(str(path / "bldrv.sp"))
        models = Path(os.environ["PDKPATH"]) / "libs.tech/ngspice/models/cornerMOSlv.lib"
        for corner, supply in (("tt", 1.2), ("ss", 1.08), ("ff", 1.32)):
            for name, pre, select, one, zero, bias, expected in cases:
                with self.subTest(corner=corner, supply=supply, case=name):
                    lines = ["* BLDRV public-pin control contract",
                             f".lib {models} mos_{corner}", f".include {path / 'bldrv.sp'}",
                             ".temp 27",
                             f"VDD vdd 0 {supply}", f"Vpre pre 0 {pre * supply}",
                             f"Vsel sel 0 {select * supply}", f"Vone one 0 {one * supply}",
                             f"Vzero zero 0 {zero * supply}",
                             "Xdut br br_sel bl bl_sel pre sel one zero vdd 0 ihp_bldrv",
                             "Rbl bl 0 1g", "Rbr br 0 1g",
                             "Routs bl_sel 0 1meg", "Routr br_sel 0 1meg"]
                    if bias:
                        lines += [f"Vbl bias_bl 0 {bias[0] * supply}",
                                  f"Vbr bias_br 0 {bias[1] * supply}",
                                  "Rbiasbl bias_bl bl 1k", "Rbiasbr bias_br br 1k"]
                    lines += [".control", "op", "print v(bl) v(br) v(bl_sel) v(br_sel)",
                              "quit", ".endc", ".end"]
                    (path / "controls.sp").write_text("\n".join(lines) + "\n")
                    run = subprocess.run(["ngspice", "-b", str(path / "controls.sp")],
                                         capture_output=True, text=True)
                    self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                    values = dict(re.findall(r"^v\(([^)]+)\)\s*=\s*(\S+)", run.stdout, re.MULTILINE))
                    for pin, target in zip(("bl", "br", "bl_sel", "br_sel"), expected):
                        self.assertIn(pin, values, run.stdout + run.stderr)
                        self.assertAlmostEqual(float(values[pin]), target * supply,
                                               delta=.04 * supply, msg=pin)

    def test_sense_amp_evaluate_and_hold(self):
        dut = factory.create(module_type="ihp_sense_amp")
        path = Path(self.temp.name)
        dut.sp_write(str(path / "sense.sp"))
        models = Path(os.environ["PDKPATH"]) / "libs.tech/ngspice/models/cornerMOSlv.lib"
        samples = [("first", 2.8, 1), ("hold_high", 3.8, 1), ("hold_low", 7.5, 1),
                   ("second", 8.8, 0), ("hold_high2", 9.8, 0),
                   ("hold_low2", 13.5, 0), ("third", 14.8, 1)]
        for corner, supply in (("tt", 1.2), ("ss", 1.08), ("ff", 1.32)):
            with self.subTest(corner=corner, supply=supply):
                low = .95 * supply  # Nonzero input common mode, 5% VDD differential.
                lines = ["* Clocked differential evaluate, opposite decision, and retention",
                         f".lib {models} mos_{corner}", f".include {path / 'sense.sp'}",
                         ".temp 27", f"Vdd vdd 0 {supply}",
                         f"Vcp cp 0 PULSE(0 {supply} 2n 50p 50p 2n 6n)",
                         f"Vdp dp 0 PWL(0 {supply} 3n {supply} 3.05n {low} 9n {low} 9.05n {supply} 18n {supply})",
                         f"Vdn dn 0 PWL(0 {low} 3n {low} 3.05n {supply} 9n {supply} 9.05n {low} 18n {low})",
                         "Xdut cp dn dp qn qp vdd 0 ihp_sense_amp",
                         "Cqp qp 0 5f", "Cqn qn 0 5f", ".control", "tran 10p 18n"]
                for tag, time, _ in samples:
                    for pin in ("qp", "qn"):
                        lines.append(f"meas tran {pin}_{tag} find v({pin}) at={time}n")
                lines += ["quit", ".endc", ".end"]
                (path / "sense_controls.sp").write_text("\n".join(lines) + "\n")
                run = subprocess.run(["ngspice", "-b", str(path / "sense_controls.sp")],
                                     capture_output=True, text=True)
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                values = dict(re.findall(r"^(\w+)\s*=\s*([-\d.eE+]+)", run.stdout, re.MULTILINE))
                for tag, _, bit in samples:
                    for pin, expected in (("qp", bit), ("qn", 1 - bit)):
                        key = pin + "_" + tag
                        self.assertIn(key, values, run.stdout + run.stderr)
                        self.assertAlmostEqual(float(values[key]), expected * supply,
                                               delta=.05 * supply, msg=key)

    def test_memory_slice_write_read(self):
        # Opposite values in neighboring columns and the two extreme rows
        # distinguish column swaps, polarity errors, and half-select writes.
        path = Path(self.temp.name)
        models = Path(os.environ["PDKPATH"]) / "libs.tech/ngspice/models/cornerMOSlv.lib"
        pattern = {(0, 0): 1, (0, 1): 0, (0, 2): 0, (0, 3): 1,
                   (15, 0): 0, (15, 1): 1, (15, 2): 1, (15, 3): 0}
        operations = [("write", r, c, b) for (r, c), b in pattern.items()]
        operations += [("read", r, c, pattern[r, c])
                       for r, c in [(15, 2), (0, 3), (15, 0), (0, 1),
                                    (0, 0), (15, 3), (0, 2), (15, 1)]]
        operations += [("write", 0, 1, 1), ("read", 0, 1, 1),
                       ("read", 15, 1, 1), ("read", 0, 2, 0),
                       ("write", 0, 0, 0), ("read", 0, 0, 0),
                       ("read", 0, 3, 1), ("read", 15, 0, 0)]
        for cols, corner, supply in ((4, "tt", 1.2), (4, "ss", 1.08),
                                     (4, "ff", 1.32), (8, "tt", 1.2)):
            with self.subTest(cols=cols, corner=corner):
                dut = factory.create(module_type="ihp_memory_slice", cols=cols)
                dut.sp_write(str(path / f"slice_{cols}.sp"))
                groups = cols // 4
                signals = {p: [(0, 0)] for p in ["pre_n", "wr_one", "wr_zero", "sae"] +
                           [f"sel_{c}" for c in range(4)] + [f"wl_{r}" for r in range(16)]}
                measurements = []
                for index, (op, row, col, bit) in enumerate(operations):
                    start = 5 + 16 * index
                    pulses = [("pre_n", 0, 12), (f"sel_{col}", 1, 11),
                              (f"wl_{row}", 3, 8)]
                    if op == "write":
                        pulses.append(("wr_one" if bit else "wr_zero", 2, 9))
                    else:
                        pulses.append(("sae", 5, 9))
                        for tag, delay in (("read", 7), ("hold", 13)):
                            for group in range(groups):
                                value = bit ^ group
                                measurements += [(f"qp_{group}_{index}_{tag}", f"qp_{group}", start + delay, value),
                                                 (f"qn_{group}_{index}_{tag}", f"qn_{group}", start + delay, 1 - value)]
                    for pin, begin, end in pulses:
                        signals[pin] += [(start + begin, 0), (start + begin + .05, supply),
                                         (start + end, supply), (start + end + .05, 0)]
                    if op == "write":
                        for group in range(groups):
                            physical_col = 4 * group + col
                            measurements += [(f"written_{group}_{index}",
                                              f"xmemory.xarray.xbit_r{row}_c{physical_col}.nt",
                                              start + 13, bit ^ group)]
                end_time = 16 * len(operations) + 5
                final_pattern = dict(pattern)
                final_pattern[0, 1] = 1
                final_pattern[0, 0] = 0
                for (row, col), bit in final_pattern.items():
                    for group in range(groups):
                        physical_col = 4 * group + col
                        measurements += [(f"retained_{group}_{row}_{col}",
                                          f"xmemory.xarray.xbit_r{row}_c{physical_col}.nt",
                                          end_time - 1, bit ^ group)]
                lines = ["* Framed memory slice; lumped loads, no PEX",
                         f".lib {models} mos_{corner}", f".include {path / ('slice_' + str(cols) + '.sp')}",
                         ".temp 27", f"Vdd vdd 0 {supply}"]
                for pin, points in signals.items():
                    wave = " ".join(f"{time}n {voltage}" for time, voltage in points)
                    lines.append(f"V{pin} {pin} 0 PWL({wave})")
                connections = [f"wl_{row}" for row in range(16)]
                connections += [f"sel_{col}" for col in range(4)]
                for group in range(groups):
                    # The second group writes complementary data to a
                    # separate word bit, exposing cross-group shorts/swaps.
                    connections += ["pre_n", "sae"]
                    connections += (["wr_one", "wr_zero"] if group == 0 else ["wr_zero", "wr_one"])
                    connections += [f"qp_{group}", f"qn_{group}"]
                    lines += [f"Cqp_{group} qp_{group} 0 5f", f"Cqn_{group} qn_{group} 0 5f"]
                lines.append("Xmemory " + " ".join(connections + ["vdd", "0", dut.name]))
                for col in range(cols):
                    for pin in ("bl", "br"):
                        lines.append(f"C{pin}_{col} xmemory.{pin}_0_{col} 0 50f")
                lines += [".control", f"tran 20p {end_time}n"]
                for tag, node, time, _ in measurements:
                    lines.append(f"meas tran {tag} find v({node}) at={time}n")
                lines += ["quit", ".endc", ".end"]
                deck = path / f"slice_{cols}_{corner}.sp"
                deck.write_text("\n".join(lines) + "\n")
                run = subprocess.run(["ngspice", "-b", str(deck)], capture_output=True, text=True)
                (path / f"slice_{cols}_{corner}.log").write_text(run.stdout + run.stderr)
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                values = dict(re.findall(r"^(\w+)\s*=\s*([-\d.eE+]+)", run.stdout, re.MULTILINE))
                for tag, _, _, bit in measurements:
                    self.assertIn(tag, values, run.stdout + run.stderr)
                    self.assertAlmostEqual(float(values[tag]), bit * supply,
                                           delta=.1 * supply, msg=f"{cols}, {corner}: {tag}")

    def test_memory_slice_physical(self):
        # Eight columns exercise the array interface and an inter-group
        # shared-tap boundary. Missing VDD bridges fail LVS; missing tap
        # completion shapes fail DRC. No implicit supply joins are allowed.
        command = [sys.executable, str(Path(__file__).with_name("verify_array.py")),
                   "--slice", "--cols=8", "--output=" + str(Path(self.temp.name) / "slice-physical")]
        run = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertIn("DRC passed", run.stdout)
        self.assertIn("LVS passed", run.stdout)

    def test_column_data_layout(self):
        import klayout.db as kdb
        dut = factory.create(module_type="ihp_column_data")
        self.assertAlmostEqual(dut.width, 12.24)
        self.assertAlmostEqual(dut.height, 32.865)
        self.assertEqual(list(dut.pins),
                         ["bl_0", "br_0", "bl_1", "br_1", "bl_2", "br_2", "bl_3", "br_3",
                          "sel_0", "sel_1", "sel_2", "sel_3", "pre_n", "wr_one", "wr_zero",
                          "sae", "qp", "qn", "vdd", "gnd"])
        for pin in dut.pins:
            self.assertTrue(dut.get_pins(pin), pin)
        path = Path(self.temp.name) / "column-layout.gds"
        dut.gds_write(str(path))
        actual = kdb.Layout()
        actual.read(str(path))
        source = kdb.Layout()
        source.read(str(Path(os.environ["PDKPATH"]) / "libs.ref/sg13g2_sram/gds/RM_IHPSG13_1P_64x16_c2.gds"))
        parent = source.cell("RM_IHPSG13_1P_COLCTRL2")
        imported = kdb.Layout()
        imported.read(str(Path(OPTS.openram_tech) / "gds_lib/ihp_column_data.gds"))
        shift = kdb.Trans(510, 33900)
        for index in source.layer_indexes():
            info = source.get_info(index)
            if info.datatype != 0:
                continue
            with self.subTest(layer=str(info)):
                result = kdb.Region(actual.top_cell().begin_shapes_rec(actual.layer(info)))
                library = kdb.Region(imported.top_cell().begin_shapes_rec(imported.layer(info)))
                self.assertTrue((result ^ library).is_empty(), "GDS export changed geometry")
                reference = kdb.Region(parent.begin_shapes_rec(index)).transformed(shift)
                self.assertTrue((result - reference).is_empty(), "Added non-foundry geometry")
                if info.layer not in (8, 19, 10, 29, 30, 49, 50):
                    devices = kdb.Region()
                    for inst in parent.each_inst():
                        if inst.cell.name in ("RM_IHPSG13_1P_BLDRV", "RSC_IHPSG13_DFPQD_MSAFFX2N"):
                            for trans in inst.cell_inst.each_trans():
                                devices += kdb.Region(inst.cell.begin_shapes_rec(index)).transformed(trans)
                    self.assertTrue((result ^ devices.transformed(shift)).is_empty(),
                                    "Retained devices changed or unrelated devices remain")

    def test_asymmetric_arrays(self):
        for rows, cols in [(2, 3), (4, 3)]:
            with self.subTest(rows=rows, cols=cols):
                array = factory.create(module_type="bitcell_array", rows=rows, cols=cols)
                self.assertAlmostEqual(array.width, cols * 2.81)
                self.assertAlmostEqual(array.height, rows * 1.07)
                for col in range(cols):
                    x = col * 2.81 + (0.905 if col % 2 == 0 else 1.905)
                    self.assertAlmostEqual(array.get_pin(f"bl_0_{col}").cx(), x)
                for row in range(rows):
                    self.assertAlmostEqual(array.get_pin(f"wl_0_{row}").cy(), row * 1.07 + 0.535)

    def test_foundry_geometry_is_unchanged(self):
        import klayout.db as kdb
        source = kdb.Layout()
        source.read(str(Path(os.environ["PDKPATH"]) / "libs.ref/sg13g2_sram/gds/RM_IHPSG13_1P_64x16_c2.gds"))
        original = source.cell("RM_IHPSG13_1P_BITKIT_CELL")
        imported = kdb.Layout()
        imported.read(str(ROOT / "technology/ihp_sg13g2/gds_lib/cell_1rw.gds"))
        self.assertEqual(source.dbu, imported.dbu)
        shift = kdb.Trans(round(1.405 / source.dbu), round(0.535 / source.dbu))
        for index in source.layer_indexes():
            info = source.get_info(index)
            # Canonical text and the repeat-pitch boundary are intentional
            # metadata changes; manufacturing polygons must match exactly.
            if info.datatype == 25 or (info.layer, info.datatype) == (189, 4):
                continue
            expected = kdb.Region(original.begin_shapes_rec(index)).transformed(shift)
            actual = kdb.Region(imported.top_cell().begin_shapes_rec(imported.layer(info)))
            with self.subTest(layer=str(info)):
                self.assertTrue((expected ^ actual).is_empty())

    def test_framed_array_matches_shipped_matrix(self):
        import klayout.db as kdb
        source = kdb.Layout()
        source.read(str(Path(os.environ["PDKPATH"]) / "libs.ref/sg13g2_sram/gds/RM_IHPSG13_1P_64x16_c2.gds"))
        reference = source.cell("RM_IHPSG13_1P_MATRIX_16x32")
        array = factory.create(module_type="ihp_bitcell_array", rows=16, cols=32)
        self.assertAlmostEqual(array.width, 93.14)
        self.assertAlmostEqual(array.height, 18.92)
        path = Path(self.temp.name) / "framed.gds"
        array.gds_write(str(path))
        actual = kdb.Layout()
        actual.read(str(path))
        # Compare the complete assembled layout, including compiler pin metal,
        # directly against the shipped matrix, not against importer outputs.
        for index in source.layer_indexes():
            info = source.get_info(index)
            if info.datatype != 0:
                continue
            expected = kdb.Region(reference.begin_shapes_rec(index)).transformed(kdb.Trans(1610, 1435))
            result = kdb.Region(actual.top_cell().begin_shapes_rec(actual.layer(info)))
            with self.subTest(layer=str(info)):
                self.assertEqual((expected ^ result).area(), 0)
        for cols in (4, 12):
            smaller = factory.create(module_type="ihp_bitcell_array", rows=16, cols=cols)
            self.assertAlmostEqual(smaller.width, cols * 2.81 + 3.22)
            self.assertEqual(len(smaller.get_bitline_names()), cols * 2)
            self.assertEqual(len(smaller.get_wordline_names()), 16)
            self.assertAlmostEqual(smaller.get_pin("wl_0_15").cy(), 17.485)
            self.assertTrue(smaller.get_pins("vdd"))
            self.assertTrue(smaller.get_pins("gnd"))
        for rows, cols in ((32, 4), (16, 2), (16, 6), (16, 36)):
            with self.subTest(rows=rows, cols=cols), self.assertRaises(ValueError):
                factory.create(module_type="ihp_bitcell_array", rows=rows, cols=cols)


if __name__ == "__main__":
    unittest.main()
