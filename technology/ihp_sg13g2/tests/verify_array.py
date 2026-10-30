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
if __name__ == "__main__":
    os.environ["OPENRAM_HOME"] = str(ROOT / "compiler")
    os.environ["OPENRAM_TECH"] = str(ROOT / "technology")
    sys.path.insert(0, str(ROOT))
    from common import make_openram_package
    make_openram_package()
import openram
from openram import OPTS
from openram.sram_factory import factory


def _input(path):
    path = Path(path)
    return path.resolve() if path.is_absolute() else (Path(OPTS.openram_temp) / path).resolve()


def _run(kind, cell_name, flags, output_path):
    out = Path(output_path or OPTS.openram_temp).resolve()
    out.mkdir(parents=True, exist_ok=True)
    pdk = Path(os.environ["PDK_ROOT"]) / "ihp-sg13g2/libs.tech/klayout/tech"
    command = [sys.executable, str(pdk / kind / ("run_" + kind + ".py")),
               "--topcell=" + cell_name, "--run_dir=" + str(out / (cell_name + "." + kind))] + flags
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    log = out / (cell_name + "." + kind + ".out")
    log.write_text(result.stdout)
    success = {"drc": "KLayout DRC Check Passed", "lvs": "Congratulations! Netlists match."}[kind]
    # These PDK runners can exit zero even when the comparison fails.
    failed = result.returncode != 0 or success not in result.stdout
    print(f"{kind.upper()} {'failed' if failed else 'passed'}: {log}")
    return int(failed)


def run_drc(cell_name, gds_name, sp_name=None, extract=True, final_verification=False,
            output_path=None):
    # Regression inputs are unfilled cells/macros, not manufacturing signoff.
    return _run("drc", cell_name, ["--path=" + str(_input(gds_name)),
                                  "--no_density", "--mp=1", "--density_thr=1"], output_path)


def run_lvs(cell_name, gds_name, sp_name, final_verification=False, output_path=None):
    out = Path(output_path or OPTS.openram_temp).resolve()
    out.mkdir(parents=True, exist_ok=True)
    # The simulation models are X subcircuits; the LVS reader expects M FETs.
    spice = _input(sp_name).read_text().splitlines()
    cdl = out / (cell_name + ".cdl")
    cdl.write_text("\n".join(
        "M" + line[1:] if line.startswith("X") and " sg13_lv_" in line else line
        for line in spice) + "\n")

    layout = kdb.Layout()
    layout.read(str(_input(gds_name)))
    top = layout.cell(cell_name)
    if top is None:
        raise ValueError("Missing LVS top cell: " + cell_name)
    for cell in layout.each_cell():
        # Flat LVS must not promote internal library/probe labels to ports.
        # Keep the actual top-level pins, including power and ground.
        if cell != top:
            for index in layout.layer_indexes():
                for shape in list(cell.shapes(index).each()):
                    if shape.is_text():
                        shape.delete()
        # The source uses lvsres to split through-pins joined in our netlist.
        # Remove ONLY nonmanufacturing recognition markers, not metal,
        # contacts, SRAM markers, or real resistors.
        for metal in (8, 10, 30, 50, 67):
            cell.shapes(layout.layer(metal, 29)).clear()
    gds = out / (cell_name + "_lvs.gds")
    layout.write(str(gds))
    # No implicit supply joins or missing-port exemptions, including cell tests.
    return _run("lvs", cell_name, ["--layout=" + str(gds), "--netlist=" + str(cdl),
                                  "--run_mode=flat", "--disable_tap_extraction"], out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cols", type=int, choices=range(4, 129, 4), default=32)
    parser.add_argument("--write-size", type=int, help="Bits per write mask, for --sram")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--slice", action="store_true", help="Verify array plus column-data assembly")
    mode.add_argument("--row-memory", action="store_true", help="Verify row-addressed memory assembly")
    mode.add_argument("--sram", action="store_true", help="Verify synchronous SRAM; word width is cols/4")
    mode.add_argument("--cell", choices=("ihp_row_decoder", "ihp_wordline_driver", "ihp_column_decoder"),
                      help="Verify an imported peripheral hard cell instead of an array")
    mode.add_argument("--control-cell", choices=("controller", "delay_high", "delay_mux", "inv", "and2", "nor2", "dff"),
                      help="Verify a foundry control/interface hard cell")
    mode.add_argument("--control-logic", action="store_true",
                      help="Verify the assembled raw cycle controller")
    mode.add_argument("--input-registers", type=int, choices=range(1, 73),
                      help="Verify a rising-edge input-register bank of this width")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if os.environ.get("PDK") != "ihp-sg13g2":
        parser.error("Select iic-pdk ihp-sg13g2 first")
    if args.write_size is not None and not args.sram:
        parser.error("--write-size requires --sram")
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ihp-frame-") as temp:
        OPTS.tech_name = "ihp_sg13g2"
        OPTS.openram_temp = temp + "/tmp/"
        OPTS.output_path = temp + "/output/"
        openram.init_openram(str(ROOT / "compiler/tests/configs/config.py"), is_unit_test=True)
        OPTS.check_lvsdrc = False  # Explicit installed-PDK runs below.
        if args.sram:
            OPTS.analytical_delay = False
            OPTS.trim_netlist = False
            OPTS.use_pex = False
            config = openram.sram_config(word_size=args.cols // 4, num_words=64,
                                        words_per_row=4, write_size=args.write_size)
            array = openram.sram(sram_config=config, name="ihp_sram_check").s
        elif args.cell:
            array = factory.create(module_type=args.cell)
        elif args.control_cell:
            array = factory.create(module_type="ihp_control_cell", kind=args.control_cell)
        elif args.control_logic:
            array = factory.create(module_type="ihp_control_logic")
        elif args.input_registers:
            array = factory.create(module_type="ihp_input_registers", bits=args.input_registers)
        elif args.row_memory:
            array = factory.create(module_type="ihp_row_memory", cols=args.cols)
        elif args.slice:
            array = factory.create(module_type="ihp_memory_slice", cols=args.cols)
        else:
            array = factory.create(module_type="ihp_bitcell_array", rows=16, cols=args.cols)
        array.gds_write(str(out / "array.gds"))
        array.sp_write(str(out / "array.sp"))
        if args.sram:
            array.lef_write(str(out / "array.lef"))
            array.verilog_write(str(out / "array.v"))
        openram.end_openram()

    drc_errors = run_drc(array.cell_name, out / "array.gds", output_path=out)
    lvs_errors = run_lvs(array.cell_name, out / "array.gds", out / "array.sp", output_path=out)
    if drc_errors or lvs_errors:
        raise SystemExit(f"DRC/LVS failed: see {out}")


if __name__ == "__main__":
    main()
