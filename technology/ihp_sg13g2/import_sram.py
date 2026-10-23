#!/usr/bin/env python3
"""Import the unchanged foundry 6T geometry as OpenRAM's cell_1rw hard cell.

Run inside IIC-OSIC after `iic-pdk ihp-sg13g2`. Requires KLayout Python.
The five-port netlist joins the shipped through-pins and ties NW/PW to VDD/VSS;
the array still needs the foundry tap/end structures to realize those ties.
"""

import os
from pathlib import Path
import re

import klayout.db as kdb


def main():
    if os.environ.get("PDK") != "ihp-sg13g2":
        raise SystemExit("Select the PDK first: iic-pdk ihp-sg13g2")
    tech = Path(__file__).resolve().parent
    source = Path(os.environ["PDKPATH"]) / "libs.ref/sg13g2_sram"
    macro = "RM_IHPSG13_1P_64x16_c2"
    layout = kdb.Layout()
    layout.read(str(source / "gds" / (macro + ".gds")))
    original = layout.cell("RM_IHPSG13_1P_BITKIT_CELL")

    dest = kdb.Layout()
    dest.dbu = layout.dbu
    cell = dest.create_cell("cell_1rw")
    # The repeat box, not the overlapping geometry envelope, sets placement.
    shift = kdb.Trans(round(1.405 / dest.dbu), round(0.535 / dest.dbu))
    for index in layout.layer_indexes():
        info = layout.get_info(index)
        region = kdb.Region(original.begin_shapes_rec(index)).merged()
        cell.shapes(dest.layer(info)).insert(region.transformed(shift))
    cell.shapes(dest.layer(189, 4)).insert(kdb.DBox(0, 0, 2.81, 1.07).to_itype(dest.dbu))

    # Replace the source text with canonical OpenRAM labels on actual metal.
    # Ground has two must-connect rails; both must remain exposed.
    for name, layer, x, y in [
        ("bl", 10, -0.5, 0.535), ("br", 10, 0.5, 0.535),
        ("wl", 30, 0, 0), ("vdd", 10, 0, 0),
        ("gnd", 10, -0.995, 0), ("gnd", 10, 0.995, 0),
        ("NT", 8, -0.995, 0), ("NC", 8, 0.995, 0),
    ]:
        point = kdb.Point(round(x / dest.dbu), round(y / dest.dbu)) + shift.disp
        metal = kdb.Region(cell.shapes(dest.layer(layer, 0)))
        if not any(polygon.inside(point) for polygon in metal.each()):
            raise ValueError(f"{name} label is not on source metal")
        cell.shapes(dest.layer(layer, 25)).insert(kdb.Text(name, kdb.Trans(point.x, point.y)))

    # Preserve the CDL license/provenance; translate only this six-FET circuit.
    cdl_path = source / "cdl" / (macro + ".cdl")
    cdl = cdl_path.read_text()
    source_name = "RM_IHPSG13_64x16_c2_1P_BITKIT_CELL"
    statements = re.sub(r"\n\+\s*", " ", cdl)
    match = re.search(r"^\.SUBCKT " + source_name + r"\s.*?^\.ENDS[^\n]*",
                      statements, re.MULTILINE | re.DOTALL)
    nodes = {"BLT_BOT": "bl", "BLT_TOP": "bl", "BLC_BOT": "br", "BLC_TOP": "br",
             "LWL": "wl", "RWL": "wl", "NW": "vdd", "PW": "gnd",
             "VDD": "vdd", "VSS": "gnd"}
    netlist = [line.rstrip() for line in cdl[:cdl.index(".SUBCKT")].splitlines()]
    netlist += ["* Imported from " + cdl_path.name + ": " + source_name,
                "* NW/PW require array taps. lvsres through-pins are joined.",
                ".subckt cell_1rw bl br wl vdd gnd"]
    count = 0
    for line in match.group().splitlines():
        if not line.startswith("M"):
            continue
        tokens = line.split()
        parameters = dict(token.split("=", 1) for token in tokens[6:])
        # SG13 LV simulation models are subcircuits, not primitive MOS models.
        netlist.append("X" + tokens[0][1:] + " " +
                       " ".join(nodes.get(node, node) for node in tokens[1:5]) +
                       " " + tokens[5] + " " +
                       " ".join(key + "=" + parameters[key] for key in ("w", "l", "m")))
        count += 1
    if count != 6:
        raise ValueError(f"Expected six source transistors, found {count}")
    netlist.append(".ends cell_1rw\n")
    (tech / "gds_lib").mkdir(exist_ok=True)
    (tech / "sp_lib").mkdir(exist_ok=True)
    dest.write(str(tech / "gds_lib/cell_1rw.gds"))
    (tech / "sp_lib/cell_1rw.sp").write_text("\n".join(netlist))
    print("Imported cell_1rw: pitch 2.81 x 1.07 um; six unchanged foundry FETs")


if __name__ == "__main__":
    main()
