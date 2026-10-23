"""Export a framed array or memory slice and run installed SG13G2 checks.

Run after import_sram.py, inside IIC-OSIC with iic-pdk ihp-sg13g2.
The original compiler GDS/SPICE are kept alongside normalized LVS views.
"""

import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import klayout.db as kdb

ROOT = Path(__file__).resolve().parents[3]
os.environ["OPENRAM_HOME"] = str(ROOT / "compiler")
os.environ["OPENRAM_TECH"] = str(ROOT / "technology")
sys.path.insert(0, str(ROOT))
from common import make_openram_package
make_openram_package()
import openram
from openram import OPTS
from openram.sram_factory import factory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cols", type=int, choices=range(4, 33, 4), default=32)
    parser.add_argument("--slice", action="store_true", help="Verify array plus column-data assembly")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if os.environ.get("PDK") != "ihp-sg13g2":
        parser.error("Select iic-pdk ihp-sg13g2 first")
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ihp-frame-") as temp:
        OPTS.tech_name = "ihp_sg13g2"
        OPTS.openram_temp = temp + "/tmp/"
        OPTS.output_path = temp + "/output/"
        openram.init_openram(str(ROOT / "compiler/tests/configs/config.py"), is_unit_test=True)
        OPTS.check_lvsdrc = False  # Explicit installed-PDK runs below.
        array = (factory.create(module_type="ihp_memory_slice", cols=args.cols) if args.slice else
                 factory.create(module_type="ihp_bitcell_array", rows=16, cols=args.cols))
        array.gds_write(str(out / "array.gds"))
        array.sp_write(str(out / "array.sp"))
        openram.end_openram()

    # The simulation models are X subcircuits; the LVS reader expects M FETs.
    spice = (out / "array.sp").read_text().splitlines()
    (out / "array.cdl").write_text("\n".join(
        "M" + line[1:] if line.startswith("X") and " sg13_lv_" in line else line
        for line in spice) + "\n")

    layout = kdb.Layout()
    layout.read(str(out / "array.gds"))
    top = layout.top_cell()
    for cell in layout.each_cell():
        # Internal library labels (including storage-net probes) must not be
        # promoted to macro ports by flat LVS. Keep the actual top-level pins.
        if cell != top:
            for index in layout.layer_indexes():
                for shape in list(cell.shapes(index).each()):
                    if shape.is_text():
                        shape.delete()
        # The source uses lvsres to split through-pins. Our five-port circuit
        # joins those pins; remove ONLY their nonmanufacturing recognition
        # markers, not metal, contacts, SRAM markers, or real resistors.
        for metal in (10, 30):
            cell.shapes(layout.layer(metal, 29)).clear()
    layout.write(str(out / "array_lvs.gds"))

    pdk = Path(os.environ["PDKPATH"]) / "libs.tech/klayout/tech"
    for kind, flags, success in [
        ("drc", ["--path=" + str(out / "array.gds"), "--no_density"],
         "KLayout DRC Check Passed"),
        ("lvs", ["--layout=" + str(out / "array_lvs.gds"),
                 "--netlist=" + str(out / "array.cdl"), "--disable_tap_extraction"],
         "Congratulations! Netlists match."),
    ]:
        command = [sys.executable, str(pdk / kind / ("run_" + kind + ".py")),
                   "--run_dir=" + str(out / kind)] + flags
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        (out / (kind + ".log")).write_text(result.stdout)
        # These PDK runners can exit zero even when the comparison fails.
        if result.returncode or success not in result.stdout:
            raise SystemExit(f"{kind.upper()} failed: see {out / (kind + '.log')}")
        print(f"{kind.upper()} passed: {out / (kind + '.log')}")


if __name__ == "__main__":
    main()
