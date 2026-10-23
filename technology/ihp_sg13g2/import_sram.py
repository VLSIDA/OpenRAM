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


def import_peripheral(layout, tech, cdl, name, gds_name, cdl_name,
                      ports, label_purpose, transistor_count):
    """Import an unchanged peripheral and its recursively flattened circuit."""
    original = layout.cell(gds_name)
    dest = kdb.Layout()
    dest.dbu = layout.dbu
    cell = dest.create_cell(name)
    box = original.bbox()
    shift = kdb.Trans(-box.left, -box.bottom)
    found = set()
    for index in layout.layer_indexes():
        info = layout.get_info(index)
        cell.shapes(dest.layer(info)).insert(
            kdb.Region(original.begin_shapes_rec(index)).merged().transformed(shift))
        if info.datatype != label_purpose:
            continue
        it = original.begin_shapes_rec(index)
        while not it.at_end():
            shape = it.shape()
            if shape.is_text():
                pin = ports[shape.text.string.rstrip("!")]
                point = shift * (it.trans() * kdb.Point(shape.text.trans.disp))
                metal = kdb.Region(original.begin_shapes_rec(layout.layer(info.layer, 0)))
                if not any(p.inside(shift.inverted() * point) for p in metal.each()):
                    raise ValueError(f"{name}: {pin} is not on source metal")
                cell.shapes(dest.layer(info.layer, 25)).insert(kdb.Text(pin, kdb.Trans(point)))
                found.add(pin)
            it.next()
    if found != set(ports.values()):
        raise ValueError(f"Missing {name} pins: {set(ports.values()) - found}")
    # An envelope, not an independently tileable pitch. Parent placement
    # must preserve the source's sharing and overlap conventions.
    cell.shapes(dest.layer(189, 4)).insert(kdb.Box(0, 0, box.width(), box.height()))
    dest.write(str(tech / "gds_lib" / (name + ".gds")))

    statements = re.sub(r"\n\+\s*", " ", cdl)
    circuits = {}
    for match in re.finditer(r"^\.SUBCKT\s+(\S+)([^\n]*)\n(.*?)^\.ENDS[^\n]*",
                             statements, re.MULTILINE | re.DOTALL):
        circuits[match[1]] = (match[2].split(), match[3].splitlines())
    netlist = [cdl[:cdl.index(".SUBCKT")].rstrip(),
               f"* Flattened from {cdl_name}; unchanged W/L/m.",
               ".subckt " + name + " " + " ".join(ports.values())]

    def flatten(name, nodes, prefix=""):
        formal, body = circuits[name]
        if len(formal) != len(nodes):
            raise ValueError(f"CDL pin count mismatch in {name}")
        mapping = dict(zip(formal, nodes))
        for line in body:
            tokens = line.split()
            if not tokens or tokens[0].startswith("*"):
                continue
            instance = prefix + tokens[0]
            if tokens[0].startswith("M"):
                params = dict(token.split("=", 1) for token in tokens[6:])
                netlist.append("X" + instance + " " +
                               " ".join(mapping.get(n, prefix + n) for n in tokens[1:5]) +
                               " " + tokens[5] + " " +
                               " ".join(key + "=" + params[key] for key in ("w", "l", "m")))
            elif tokens[0].startswith("X"):
                connections = [mapping.get(n, prefix + n) for n in tokens[1:-1] if n != "/"]
                flatten(tokens[-1], connections, instance + "_")
            else:
                raise ValueError(f"Unsupported peripheral CDL statement: {line}")

    flatten(cdl_name, list(ports.values()))
    if sum(line.startswith("X") for line in netlist) != transistor_count:
        raise ValueError(f"Expected {transistor_count} transistors in {name}")
    netlist.append(".ends " + name + "\n")
    (tech / "sp_lib" / (name + ".sp")).write_text("\n".join(netlist))


def import_frame(layout, tech, cdl):
    """Extract frame overlays, leaving the compiler's real bit instances intact.

    Coordinates follow the shipped 16-row matrix. Only the core geometry is
    removed from the overlay; CELL_2x1's additional supply straps stay intact.
    """
    layout.cell("RM_IHPSG13_1P_BITKIT_CELL").clear()
    header = cdl[:cdl.index(".SUBCKT")]
    for name, source, dx, width, labels, ports in [
        ("ihp_frame_tile", "16x2_SRAM", 0, 5.62,
         [("vdd", 30, 1.405, -.535), ("gnd", 30, 1.405, .535)],
         ["vdd", "gnd"]),
        ("ihp_frame_edge", "16x2_EDGE_LR", 1.61, 1.61,
         [(f"wl_{row}", 30, -.095, row * 1.07) for row in range(16)] +
         [("vdd", 30, -.095, -.535), ("gnd", 30, -.095, .535)],
         [f"wl_{row}" for row in range(16)] + ["vdd", "gnd"]),
        ("ihp_frame_power", "16x2_POWER_ramblk", 0, 11.24,
         [("gnd", 50, 1.565, .535), ("vdd", 50, 7.185, 1.605)],
         ["vdd", "gnd"]),
    ]:
        dest = kdb.Layout()
        dest.dbu = layout.dbu
        cell = dest.create_cell(name)
        original = layout.cell("RM_IHPSG13_1P_BITKIT_" + source)
        shift = kdb.Trans(round(dx / dest.dbu), round(1.435 / dest.dbu))
        for index in layout.layer_indexes():
            info = layout.get_info(index)
            cell.shapes(dest.layer(info)).insert(
                kdb.Region(original.begin_shapes_rec(index)).merged().transformed(shift))
        cell.shapes(dest.layer(189, 4)).insert(
            kdb.DBox(0, 0, width, 18.92).to_itype(dest.dbu))
        for pin, layer, x, y in labels:
            point = kdb.Point(round(x / dest.dbu), round(y / dest.dbu)) + shift.disp
            if not any(p.inside(point) for p in kdb.Region(cell.shapes(dest.layer(layer, 0))).each()):
                raise ValueError(f"{name}: {pin} is not on metal")
            cell.shapes(dest.layer(layer, 25)).insert(kdb.Text(pin, kdb.Trans(point)))
        dest.write(str(tech / "gds_lib" / (name + ".gds")))
        netlist = [header.rstrip(), "* Unchanged foundry frame geometry; bodies tied by taps.",
                   ".subckt " + name + " " + " ".join(ports)]
        if name == "ihp_frame_edge":
            # EDGE_LR CDL has two grounded diffusion devices per row. The
            # second gate is deliberately floating, as in the shipped CDL.
            for row in range(16):
                netlist += [f"Xwl_{row} gnd wl_{row} gnd gnd sg13_lv_nmos w=300n l=130n m=1",
                            f"Xdummy_{row} gnd floating_{row} gnd gnd sg13_lv_nmos w=300n l=130n m=1"]
        netlist.append(".ends " + name + "\n")
        (tech / "sp_lib" / (name + ".sp")).write_text("\n".join(netlist))


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
    import_peripheral(layout, tech, cdl, "ihp_bldrv", "RM_IHPSG13_1P_BLDRV",
                      "RM_IHPSG13_64x16_c2_1P_BLDRV",
                      {"BLC": "br", "BLC_SEL": "br_sel", "BLT": "bl", "BLT_SEL": "bl_sel",
                       "PRE_N": "pre_n", "SEL_P": "sel_p", "WR_ONE": "wr_one",
                       "WR_ZERO": "wr_zero", "VDD": "vdd", "VSS": "gnd"}, 2, 22)
    print("Imported ihp_bldrv: 22 FETs; precharge, column selection, and write drive")
    import_peripheral(layout, tech, cdl, "ihp_sense_amp", "RSC_IHPSG13_DFPQD_MSAFFX2N",
                      "RSC_IHPSG13_DFPQD_MSAFFX2",
                      {"CP": "cp", "DN": "dn", "DP": "dp", "QN": "qn", "QP": "qp",
                       "VDD": "vdd", "VSS": "gnd"}, 25, 19)
    print("Imported ihp_sense_amp: 19 FETs; clocked differential sense/latch")
    import_frame(layout, tech, cdl)
    print("Imported 16-row tap/strap, edge/corner, and 4-column M4 power overlays")


if __name__ == "__main__":
    main()
