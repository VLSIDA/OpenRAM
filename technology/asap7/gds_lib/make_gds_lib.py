#!/usr/bin/env python3
"""
Build the ASAP7 gds_lib used by OpenRAM in netlist-only mode (needs gdstk).

usage: make_gds_lib.py <asap7sc7p5t_28_R GDS> <output dir>

dff.gds is DFFHQx4_ASAP7_75t_R from the asap7sc7p5t library (BSD-3-Clause),
renamed to "dff" with pins CLK->clk, VDD->vdd, VSS->gnd; the well/substrate
pin labels are dropped because OpenRAM only takes metal pins.

The other cells are abstracts: a boundary (100,0) and M1/M2 pin shapes with
labels on purpose 251. They give OpenRAM sizes and pin locations only and are
not DRC/LVS-clean layouts. The bitcell abstract has the boundary of
sram_cell_6t_122 from asap7_sram_0p0 (0.108 x 0.270 um, BSD-3-Clause), turned
so that bitlines run vertically as OpenRAM expects: 0.270 wide, 0.108 tall.
"""
import sys
import gdstk

UNIT, PREC = 1e-6, 2.5e-10
BND, M1, M2, PIN = 100, 19, 20, 251
W = 0.270            # bitcell width (sram_cell_6t_122 height); peripheral cells match it
H_BC = 0.108         # bitcell height (sram_cell_6t_122 width, two gate pitches)
T = 0.018            # M1/M2 minimum width


def abstract(name, h, vpins, hpins):
    """vpins: {name: x} vertical M1 strips; hpins: {name: y} horizontal M2 strips."""
    c = gdstk.Cell(name)
    c.add(gdstk.rectangle((0, 0), (W, h), layer=BND, datatype=0))
    for pin, x in vpins.items():
        for dt in (0, PIN):
            c.add(gdstk.rectangle((x - T/2, 0), (x + T/2, h), layer=M1, datatype=dt))
        c.add(gdstk.Label(pin, (x, h/2), layer=M1, texttype=PIN))
    for pin, y in hpins.items():
        for dt in (0, PIN):
            c.add(gdstk.rectangle((0, y - T/2), (W, y + T/2), layer=M2, datatype=dt))
        c.add(gdstk.Label(pin, (W/2, y), layer=M2, texttype=PIN))
    return c


def write(cell, out):
    lib = gdstk.Library(unit=UNIT, precision=PREC)
    lib.add(cell)
    lib.write_gds("{}/{}.gds".format(out, cell.name))


def main(stdlib, out):
    bl, br = 0.036, W - 0.036
    for name in ("cell_1rw", "replica_cell_1rw", "dummy_cell_1rw"):
        write(abstract(name, H_BC, {"bl": bl, "br": br},
                       {"gnd": T/2, "wl": H_BC/2, "vdd": H_BC - T/2}), out)
    for name, h, v, hp in (
            ("sense_amp", 1.08, {"bl": bl, "br": br, "dout": W/2},
             {"gnd": T/2, "en": 0.54, "vdd": 1.08 - T/2}),
            ("write_driver", 1.08, {"bl": bl, "br": br, "din": W/2},
             {"gnd": T/2, "en": 0.54, "vdd": 1.08 - T/2}),
            ("tri_gate", 0.54, {"in": bl, "out": br},
             {"gnd": T/2, "en": 0.18, "en_bar": 0.36, "vdd": 0.54 - T/2})):
        write(abstract(name, h, v, hp), out)

    src = gdstk.read_gds(stdlib)
    ff = [c for c in src.cells if c.name == "DFFHQx4_ASAP7_75t_R"][0].copy("dff")
    ff.flatten()
    ren = {"CLK": "clk", "VDD": "vdd", "VSS": "gnd", "D": "D", "Q": "Q"}
    keep = []
    for lb in ff.labels:
        if lb.layer == M1 and lb.text in ren:
            keep.append(gdstk.Label(ren[lb.text], lb.origin, layer=M1, texttype=PIN))
    ff.remove(*ff.labels)
    ff.add(*keep)
    write(ff, out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
