# SG13G2 foundry-bitcell bring-up

The IHP technology now supplies `gds_lib/cell_1rw.gds` and
`sp_lib/cell_1rw.sp` for OpenRAM's existing `bitcell_1port` hard-cell class.
No custom bitcell class or change to the generic compiler is needed.
**This is core-cell/placement integration, not a complete, tapeout-ready
OpenRAM SRAM port.** Tap/end cells, replica/dummy cells, peripherals, full
array DRC/LVS, and characterization remain to be integrated.

## Rebuild and test inside IIC-OSIC

Use the running IIC-OSIC container, not host EDA tools. Inside its shell:

```sh
iic-pdk ihp-sg13g2
R=/foss/designs/ihp-openram/OpenRAM
python3 "$R/technology/ihp_sg13g2/import_sram.py"
python3 "$R/technology/ihp_sg13g2/tests/test_bitcell.py" -v
```

The importer uses the installed PDK's
`libs.ref/sg13g2_sram/gds/RM_IHPSG13_1P_64x16_c2.gds` and matching CDL.
It extracts `RM_IHPSG13_1P_BITKIT_CELL`, merges duplicate polygons, translates
the origin, adds canonical labels, and adds a `prBoundary` repeat box.
It does **not** resize any manufacturing geometry or strip the SRAM marker.
The translated cell has a repeat box of (0, 0)–(2.81, 1.07) µm; its physical
geometry extends beyond that box for sharing with neighboring cells.
Alternate columns reflect x and alternate rows reflect y. The technology
properties enable both axes in OpenRAM's existing array placer.

After normal `openram.init_openram(...)`, the compiler API is unchanged:

```python
from openram.sram_factory import factory
cell = factory.create(module_type="bitcell_1port")
core = factory.create(module_type="bitcell_array", rows=4, cols=3)
# cell: 2.81 × 1.07 µm; core repeat area: 8.43 × 4.28 µm.
```

Creating a core does not insert foundry taps/end cells. The API regression
tests explicitly disable automatic DRC/LVS for these incomplete cores; that
is not a waiver for a finished array. Run physical verification separately.

## Electrical interface

The generated SPICE port order is `bl br wl vdd gnd`:

| OpenRAM | Foundry terminals joined in the circuit view | Layout layer |
|---|---|---|
| bl | BLT_BOT, BLT_TOP | M2 |
| br | BLC_BOT, BLC_TOP | M2 |
| wl | LWL, RWL | M3 |
| vdd | VDD, NW | M2 |
| gnd | VSS, PW | M2; two must-connect rails |

The shipped `lvsres` devices identify through-connections, not transistor
loads; the five-port view joins them directly. `NT` and `NC` remain the two
storage nodes. All four NMOS retain W/L = 0.30/0.13 µm; both PMOS retain
0.15/0.13 µm. CDL primitive-M instances become X instances because the SG13G2
LV simulation models are subcircuits. Body ties in this schematic require
the real array taps; they are not contacts magically added to the core GDS.

## Checks performed

- Factory loading finds all five ports, both ground rails, and storage nets.
- Asymmetric 3-column × 2-row and 3-column × 4-row arrays have correct repeat
  dimensions, bitline positions, and wordline positions.
- KLayout XOR confirms unchanged source polygons after translation.
- An independently tiled source array has zero physical-layer XOR difference
  from the actual factory-generated 3×4 GDS, including its pin routing.
- A nominal TT/1.2 V ngspice smoke test writes 1, holds 1, writes 0, holds 0.
  This is not read-margin, PVT, mismatch, timing, or yield characterization.
- Official KLayout DRC on the **core-only** array still reports `LU.a`,
  `LU.b`, and `NW.b1`, as does the equivalently isolated foundry core array.
  The shipped block with its original tap/end context passes; these missing
  structures are the next integration task, not errors to suppress.

Bring-up GDS, SPICE, simulation and DRC logs are in the sibling layout repo's
locally ignored `.amp/in/artifacts/openram-foundry/` directory. They are not
part of the technology library or evidence of complete SRAM signoff.

## Does the macro also contain sense amps and write drivers?

Yes, both GDS and CDL contain the relevant peripheral circuitry:

- **Write/bitline driver:** GDS `RM_IHPSG13_1P_BLDRV`; CDL
  `RM_IHPSG13_64x16_c2_1P_BLDRV`. It combines write pull-up/down, precharge,
  and read column-selection devices. Its interface includes `WR_ONE`,
  `WR_ZERO`, `PRE_N`, `SEL_P`, and selected bitlines, not OpenRAM's simple
  `din/bl/br/en` interface.
- **Sense/latch:** CDL `RSC_IHPSG13_DFPQD_MSAFFX2` has `CP DN DP QN QP VDD VSS`.
  The column-control CDL explicitly instantiates it as `XA_ISENSE`, driven
  by `A_SAE`, `A_BLC_SEL`, and `A_BLT_SEL`. GDS contains the associated
  `RSC_IHPSG13_DFPQD_MSAFFX2N` hierarchy; the layout/CDL name difference and
  correspondence still need LVS verification before importing it.

These are embedded macro building blocks, not standalone, characterized
OpenRAM-compatible library views. Reusing them needs logical adapters,
pin/placement definitions, enable/precharge sequencing, output-polarity
checks, DRC/LVS, and characterization. They are not enabled by this bitcell
import. First integrate the core's tap/end context; then adapt peripherals
one at a time instead of replacing them solely on matching cell names.

## Upstream availability history

These internal cells are not a recent addition. Git history and historical
GDS/CDL inspection in `IHP-GmbH/IHP-Open-PDK` establish:

- [2023-07-04, first SRAM GDS macros](https://github.com/IHP-GmbH/IHP-Open-PDK/commit/f6b6ac001c48f337a4c49f5b99b9240527818e18):
  the original 64×64, 256×64, and 1024×64 macros already contain real
  BITKIT_CELL, BLDRV, and MSAFFX2N hierarchical layout cells.
- [2023-11-17, additional EDA views](https://github.com/IHP-GmbH/IHP-Open-PDK/commit/6610df3d2454a243cb786bea9729eca53140e79a):
  transistor-level CDL definitions for those internal cells were added.
- [2026-08-11, minimal 64×16 macro](https://github.com/IHP-GmbH/IHP-Open-PDK/commit/9bda06925aeac5377bb932c448328dc97556f405):
  the specific macro used by this importer was added, with the same internal
  GDS cell names already present in 2023.

These are Git commit dates, not independent public-release or fabrication
dates. No separate standalone-cell library files were found in the inspected
upstream history. The older GDS/CDL name differences were already present in
2023; they do not indicate recently introduced cells or a recent rename.

The generated SPICE retains the source CDL's Apache-2.0 notice. Preserve
upstream notices/provenance when redistributing; separate confirmation of
the binary layout's license coverage and any fabrication qualifications
remains outside this bring-up.
