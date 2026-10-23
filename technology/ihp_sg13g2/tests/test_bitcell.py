"""Foundry hard-cell loading/placement contract, not array DRC qualification.

Run inside IIC-OSIC after selecting SG13G2 and running import_sram.py.
"""

import os
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
