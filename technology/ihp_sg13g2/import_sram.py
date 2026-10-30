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
                      ports, label_purposes, transistor_count):
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
        region = kdb.Region(original.begin_shapes_rec(index)).merged().transformed(shift)
        # OpenRAM discovers pin access rectangles, not arbitrary polygons.
        # Rectilinear decomposition preserves metal exactly while exposing
        # pins on T-shaped routing (notably COLDEC2's select outputs).
        if info.datatype == 0 and info.layer in (8, 10, 30, 50, 67):
            region = region.decompose_trapezoids_to_region()
        cell.shapes(dest.layer(info)).insert(region)
        if info.datatype not in label_purposes:
            continue
        it = original.begin_shapes_rec(index)
        while not it.at_end():
            shape = it.shape()
            if shape.is_text():
                source_pin = shape.text.string.rstrip("!")
                if source_pin not in ports or (source_pin not in ("VDD", "VSS") and it.cell() != original):
                    it.next()
                    continue  # Internal child labels are not peripheral ports.
                pin = ports[source_pin]
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
    netlist = ["\n".join(line.rstrip() for line in cdl[:cdl.index(".SUBCKT")].splitlines()).rstrip(),
               f"* Flattened from {cdl_name}; unchanged W/L/m.",
               ".subckt " + name + " " + " ".join(ports.values())]
    through_pins = []

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
            elif tokens[0].startswith("R") and tokens[3] == "lvsres":
                # Foundry through-pin annotations, not physical resistors.
                through_pins.append([mapping.get(n, prefix + n) for n in tokens[1:3]])
            else:
                raise ValueError(f"Unsupported peripheral CDL statement: {line}")

    # Canonical public names can coincide with distinct source-local nets
    # (CTRL's CS_I -> cs versus its internal mux output cs, for example).
    # Namespace all private nodes, including those at the root circuit.
    flatten(cdl_name, list(ports.values()), prefix="internal_")
    aliases = {}

    def joined(node):
        while node in aliases:
            node = aliases[node]
        return node

    for left, right in through_pins:
        left, right = joined(left), joined(right)
        if left == right:
            continue
        if right in ports.values():
            left, right = right, left
        if right in ports.values():
            raise ValueError(f"{name}: through-pin joins distinct public ports")
        aliases[right] = left
    for index, line in enumerate(netlist):
        if line.startswith("X"):
            tokens = line.split()
            tokens[1:5] = [joined(n) for n in tokens[1:5]]
            netlist[index] = " ".join(tokens)
    if sum(line.startswith("X") for line in netlist) != transistor_count:
        raise ValueError(f"Expected {transistor_count} transistors in {name}")
    netlist.append(".ends " + name + "\n")
    (tech / "sp_lib" / (name + ".sp")).write_text("\n".join(netlist))


def connected_parent_regions(layout, parent, blocks, clip):
    """Keep selected devices and parent routing connected to their metal."""
    conductors = (8, 19, 10, 29, 30, 49, 50)
    regions, seeds = {}, {}
    vias = [i for i in parent.each_inst() if i.cell.name.startswith(("M2_", "M3_", "viagen"))]
    for index in layout.layer_indexes():
        info = layout.get_info(index)
        seed = kdb.Region()
        for child, trans in blocks:
            seed += kdb.Region(child.begin_shapes_rec(index)).transformed(trans)
        if not (seed - clip).is_empty():
            raise ValueError(f"Peripheral crop truncates a retained device on {info}")
        region = seed.dup()
        for inst in vias:
            for trans in inst.cell_inst.each_trans():
                region += kdb.Region(inst.cell.begin_shapes_rec(index)).transformed(trans)
        if info.datatype == 0 and info.layer in conductors:
            region += kdb.Region(parent.shapes(index))
        regions[info.layer, info.datatype] = (region & clip).merged()
        seeds[info.layer, info.datatype] = seed
    trace = kdb.LayoutToNetlist("routes", layout.dbu)
    wires = {layer: regions[layer, 0].dup() for layer in conductors}
    for layer, region in wires.items():
        trace.register(region, str(layer))
        trace.connect(region)
    for lower, via, upper in ((8, 19, 10), (10, 29, 30), (30, 49, 50)):
        trace.connect(wires[lower], wires[via])
        trace.connect(wires[via], wires[upper])
    trace.extract_netlist()
    kept = {layer: kdb.Region() for layer in conductors}
    for net in trace.netlist().top_circuit().each_net():
        parts = {layer: trace.shapes_of_net(net, region, True) for layer, region in wires.items()}
        if any(not (part & seeds[layer, 0]).is_empty() for layer, part in parts.items()):
            for layer, part in parts.items():
                kept[layer] += part
    for layer, region in kept.items():
        regions[layer, 0] = region
    return regions


def import_column_data(layout, tech):
    """Keep four drivers, one sense/latch, and their connected parent metal.

    Discard the parent's other devices and their disconnected routing. Keep
    connected routing stubs, rather than inventing a new routing topology.
    The crop stops at the sense-cell bottom; it cuts no retained device.
    """
    parent = layout.cell("RM_IHPSG13_1P_COLCTRL2")
    driver_name = "RM_IHPSG13_1P_BLDRV"
    sense_name = "RSC_IHPSG13_DFPQD_MSAFFX2N"
    blocks = []
    for inst in parent.each_inst():
        if inst.cell.name not in (driver_name, sense_name):
            continue
        for trans in inst.cell_inst.each_trans():
            if inst.cell.name == driver_name:
                col = {(0, False): 0, (5610, True): 1,
                       (5610, False): 2, (11220, True): 3}[(trans.disp.x, trans.is_mirror())]
                names = {"BLC": f"br_{col}", "BLC_SEL": "br_sel", "BLT": f"bl_{col}",
                         "BLT_SEL": "bl_sel", "PRE_N": "pre_n", "SEL_P": f"sel_{col}",
                         "WR_ONE": "wr_one", "WR_ZERO": "wr_zero", "VDD": "vdd", "VSS": "gnd"}
                blocks.append((inst.cell, trans, f"driver_{col}", names, 2, "ihp_bldrv"))
            else:
                names = {"CP": "sae", "DN": "br_sel", "DP": "bl_sel", "QN": "qn",
                         "QP": "qp", "VDD": "vdd", "VSS": "gnd"}
                blocks.append((inst.cell, trans, "sense", names, 25, "ihp_sense_amp"))
    if len(blocks) != 5:
        raise ValueError("Expected four BLDRVs and one sense/latch")
    ports = [p for col in range(4) for p in (f"bl_{col}", f"br_{col}")]
    ports += [f"sel_{col}" for col in range(4)]
    ports += ["pre_n", "wr_one", "wr_zero", "sae", "qp", "qn", "vdd", "gnd"]
    clip = kdb.Region(kdb.Box(-800, -33900, 12245, -1035))
    shift = kdb.Trans(510, 33900)
    regions = connected_parent_regions(layout, parent, [(b[0], b[1]) for b in blocks], clip)
    dest = kdb.Layout()
    dest.dbu = layout.dbu
    cell = dest.create_cell("ihp_column_data")
    for (layer, purpose), region in regions.items():
        cell.shapes(dest.layer(layer, purpose)).insert(region.transformed(shift))
    found = set()
    for child, trans, _, names, purpose, _ in blocks:
        for index in layout.layer_indexes():
            info = layout.get_info(index)
            if info.datatype != purpose:
                continue
            it = child.begin_shapes_rec(index)
            while not it.at_end():
                shape = it.shape()
                if shape.is_text():
                    pin = names[shape.text.string.rstrip("!")]
                    if pin in ports:
                        point = shift * (trans * (it.trans() * kdb.Point(shape.text.trans.disp)))
                        cell.shapes(dest.layer(info.layer, 25)).insert(kdb.Text(pin, kdb.Trans(point)))
                        found.add(pin)
                it.next()
    if found != set(ports):
        raise ValueError(f"Missing column pins: {set(ports) - found}")
    cell.shapes(dest.layer(189, 4)).insert(cell.bbox())
    dest.write(str(tech / "gds_lib/ihp_column_data.gds"))

    # Flatten the already imported, verified peripheral circuits. Source
    # pin order agrees with names insertion order; dimensions are unchanged.
    header = (tech / "sp_lib/ihp_bldrv.sp").read_text().split(".subckt")[0]
    lines = [header.rstrip(), ".subckt ihp_column_data " + " ".join(ports)]
    for _, _, prefix, names, _, module in blocks:
        source = (tech / "sp_lib" / (module + ".sp")).read_text().splitlines()
        formal = next(line.split()[2:] for line in source if line.startswith(".subckt"))
        mapping = dict(zip(formal, names.values()))
        for line in source:
            if line.startswith("X"):
                tokens = line.split()
                nodes = [mapping.get(n, prefix + "_" + n) for n in tokens[1:5]]
                lines.append("X" + prefix + "_" + tokens[0][1:] + " " +
                             " ".join(nodes + tokens[5:]))
    if sum(line.startswith("X") for line in lines) != 107:
        raise ValueError("Expected 107 column-data FETs")
    lines.append(".ends ihp_column_data\n")
    (tech / "sp_lib/ihp_column_data.sp").write_text("\n".join(lines))


def import_column_decoder(layout, tech, cdl):
    """Retain COLDEC2's combinational gates, not its BIST registers/fill."""
    parent = layout.cell("RM_IHPSG13_1P_COLDEC2")
    blocks = [(i.cell, i.trans) for i in parent.each_inst()
              if i.cell.name in ("RSC_IHPSG13_INVX2", "RSC_IHPSG13_NAND2X2")]
    if len(blocks) != 12:
        raise ValueError("Expected eight inverters and four NAND2 column-decode gates")
    regions = connected_parent_regions(layout, parent, blocks,
                                       kdb.Region(kdb.Box(16320, -21525, 32640, -12075)))
    dest = kdb.Layout()
    dest.dbu = layout.dbu
    cell = dest.create_cell("ihp_column_decoder")
    for (layer, purpose), region in regions.items():
        cell.shapes(dest.layer(layer, purpose)).insert(region)
    # Removing fillers leaves separate VDD rails. Join them physically in
    # M1 and use the empty left margin for an M2 top-to-bottom strap.
    for y, right in ((-21000, 32130), (-12600, 18870)):
        cell.shapes(dest.layer(8, 0)).insert(kdb.Box(16320, y - 200, right, y + 200))
        cell.shapes(dest.layer(19, 0)).insert(kdb.Box(16425, y - 95, 16615, y + 95))
    cell.shapes(dest.layer(10, 0)).insert(kdb.Box(16320, -21200, 16720, -12400))
    # These are the two inverter-chain inputs, traced against the source
    # NAND/output connectivity. The shipped source labels only the register
    # inputs, which are deliberately not part of this combinational view.
    for pin, x, y in (("addr_1", 17240, -18580), ("addr_0", 17240, -15020)):
        cell.shapes(dest.layer(8, 25)).insert(kdb.Text(pin, kdb.Trans(x, y)))
    for child, trans in blocks:
        for shape in child.shapes(layout.layer(8, 2)).each():
            if shape.is_text() and shape.text.string in ("VDD!", "VSS!"):
                point = trans * kdb.Point(shape.text.trans.disp)
                pin = "vdd" if shape.text.string == "VDD!" else "gnd"
                cell.shapes(dest.layer(8, 25)).insert(kdb.Text(pin, kdb.Trans(point)))
    for index in layout.layer_indexes():
        info = layout.get_info(index)
        for shape in parent.shapes(index).each():
            if shape.is_text() and shape.text.string in [f"ADDR_DEC<{i}>" for i in range(4)]:
                pin = "sel_" + shape.text.string[-2]
                cell.shapes(dest.layer(info.layer, 25)).insert(kdb.Text(pin, shape.text.trans))

    statements = re.sub(r"\n\+\s*", " ", cdl)
    body = re.search(r"^\.SUBCKT RM_IHPSG13_64x16_c2_1P_COLDEC2[^\n]*\n(.*?)^\.ENDS",
                     statements, re.MULTILINE | re.DOTALL)[1]
    gates = [line for line in body.splitlines() if re.match(r"XI(?:1|2|3|13)<", line)]
    if len(gates) != 12:
        raise ValueError("Expected twelve combinational column-decode CDL instances")
    ports = {"padr_int<1>": "addr_1", "padr_int<0>": "addr_0",
             **{f"ADDR_DEC<{i}>": f"sel_{i}" for i in range(4)}, "VDD": "vdd", "VSS": "gnd"}
    subset = "\n.SUBCKT column_decode_subset " + " ".join(ports) + "\n"
    subset += "\n".join(gates) + "\n.ENDS\n"
    import_peripheral(dest, tech, cdl + subset, "ihp_column_decoder", cell.name,
                      "column_decode_subset", dict(zip(ports.values(), ports.values())), (25,), 32)


def import_control_cells(layout, tech, cdl):
    """Keep the shipped controller, timing elements and interface gates."""
    controller_ports = "ACLK_N BIST_CK_I BIST_CS_I BIST_EN BIST_RE_I BIST_WE_I B_TIEL_O CK_I CS_I DCLK ECLK PULSE_H PULSE_L PULSE_O RCLK RE_I ROW_CS WCLK WE_I VDD VSS".split()
    canonical = "aclk_n bist_clk bist_cs bist_en bist_re bist_we tie_low clk cs dclk eclk pulse_h pulse_l pulse rclk re row_cs wclk we vdd gnd".split()
    import_peripheral(layout, tech, cdl, "ihp_controller", "RM_IHPSG13_1P_CTRL",
                      "RM_IHPSG13_64x16_c2_1P_CTRL", dict(zip(controller_ports, canonical)), (25,), 242)
    for name, source, circuit, count in (
        ("delay_high", "RM_IHPSG13_1P_DLY_1", "RM_IHPSG13_64x16_c2_1P_DLY_pcell_2", 22),
    ):
        import_peripheral(layout, tech, cdl, "ihp_" + name, source, circuit,
                          {"A": "a", "Z": "z", "VDD": "vdd", "VSS": "gnd"}, (25,), count)
    # DLY_MUX has no parent pin texts. Its CDL connects A/SEL to the
    # mux's A0/S and Z to the final inverter's Z. Label those exact child
    # terminals in parent coordinates, retaining all source parent routing.
    mux = layout.cell("RM_IHPSG13_1P_DLY_MUX")
    for inst in mux.each_inst():
        names = {"RSC_IHPSG13_MX2IX1": {"A0": "A", "S": "SEL"},
                 "RSC_IHPSG13_CINVX2": {"Z": "Z"}}.get(inst.cell.name, {})
        for index in layout.layer_indexes():
            for shape in inst.cell.shapes(index).each():
                if shape.is_text() and shape.text.string in names:
                    point = inst.trans * kdb.Point(shape.text.trans.disp)
                    mux.shapes(index).insert(kdb.Text(names[shape.text.string], kdb.Trans(point)))
    # Its two rows have separate VDD rails. Complete them physically in
    # the unused left margin instead of relying on implicit LVS joins.
    for y in (0, 8400):
        mux.shapes(layout.layer(8, 0)).insert(kdb.Box(-2000, y - 200, -900, y + 200))
        mux.shapes(layout.layer(19, 0)).insert(kdb.Box(-1895, y - 95, -1705, y + 95))
    mux.shapes(layout.layer(10, 0)).insert(kdb.Box(-2000, -200, -1600, 8600))
    import_peripheral(layout, tech, cdl, "ihp_delay_mux", mux.name,
                      "RM_IHPSG13_64x16_c2_1P_DLY_MUX",
                      {"A": "a", "SEL": "sel", "Z": "z", "VDD": "vdd", "VSS": "gnd"},
                      (2, 25), 36)
    for name, source, ports, count in (
        ("inv", "INVX2", {"A": "a", "Z": "z", "VDD": "vdd", "VSS": "gnd"}, 2),
        ("and2", "AND2X2", {"A": "a", "B": "b", "Z": "z", "VDD": "vdd", "VSS": "gnd"}, 6),
        ("nor2", "NOR2X2", {"A": "a", "B": "b", "Z": "z", "VDD": "vdd", "VSS": "gnd"}, 4),
        ("dff", "DFNQX2", {"CN": "clk_n", "D": "d", "Q": "q", "VDD": "vdd", "VSS": "gnd"}, 24),
    ):
        source = "RSC_IHPSG13_" + source
        import_peripheral(layout, tech, cdl, "ihp_" + name, source, source, ports, (2, 25), count)


def import_frame(layout, tech, cdl):
    """Extract frame overlays, leaving the compiler's real bit instances intact.

    Coordinates follow the shipped 16-row matrix. Only the core geometry is
    removed from the overlay; CELL_2x1's additional supply straps stay intact.
    """
    layout.cell("RM_IHPSG13_1P_BITKIT_CELL").clear()
    header = "\n".join(line.rstrip() for line in cdl[:cdl.index(".SUBCKT")].splitlines())
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
                       "WR_ZERO": "wr_zero", "VDD": "vdd", "VSS": "gnd"}, (2,), 22)
    print("Imported ihp_bldrv: 22 FETs; precharge, column selection, and write drive")
    import_peripheral(layout, tech, cdl, "ihp_sense_amp", "RSC_IHPSG13_DFPQD_MSAFFX2N",
                      "RSC_IHPSG13_DFPQD_MSAFFX2",
                      {"CP": "cp", "DN": "dn", "DP": "dp", "QN": "qn", "QP": "qp",
                       "VDD": "vdd", "VSS": "gnd"}, (25,), 19)
    print("Imported ihp_sense_amp: 19 FETs; clocked differential sense/latch")
    import_peripheral(layout, tech, cdl, "ihp_row_decoder", "RM_IHPSG13_1P_ROWDEC4",
                      "RM_IHPSG13_64x16_c2_1P_ROWDEC4",
                      {**{f"ADDR_N_I<{i}>": f"addr_{i}" for i in reversed(range(4))},
                       "CS_I": "cs", "ECLK_I": "eclk",
                       **{f"WL_O<{i}>": f"decode_{i}" for i in reversed(range(16))},
                       "VDD": "vdd", "VSS": "gnd"}, (25,), 222)
    print("Imported ihp_row_decoder: 222 FETs; latched 4-to-16 decode")
    import_peripheral(layout, tech, cdl, "ihp_wordline_driver", "RM_IHPSG13_1P_WLDRV16X4",
                      "RM_IHPSG13_64x16_c2_1P_WLDRV16X4",
                      {**{f"A<{i}>": f"decode_{i}" for i in reversed(range(16))},
                       **{f"Z<{i}>": f"wl_{i}" for i in reversed(range(16))},
                       "VDD": "vdd", "VSS": "gnd"}, (2, 25), 64)
    print("Imported ihp_wordline_driver: 64 FETs; sixteen noninverting buffers")
    import_column_data(layout, tech)
    print("Imported ihp_column_data: four BLDRVs, one sense/latch, and connected parent routing")
    import_column_decoder(layout, tech, cdl)
    print("Imported ihp_column_decoder: 32 FETs; combinational 2-to-4 decode without BIST registers")
    import_control_cells(layout, tech, cdl)
    print("Imported shipped controller, delay chains, and interface logic cells")
    import_frame(layout, tech, cdl)
    print("Imported 16-row tap/strap, edge/corner, and 4-column M4 power overlays")


if __name__ == "__main__":
    main()
