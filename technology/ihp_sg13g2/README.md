# SG13G2 foundry-bitcell bring-up

The IHP technology now supplies `gds_lib/cell_1rw.gds` and
`sp_lib/cell_1rw.sp` for OpenRAM's existing `bitcell_1port` hard-cell class.
No custom bitcell class or change to the generic compiler is needed.
The explicit `ihp_bitcell_array` module also assembles a foundry-framed
16-row array with the shipped taps, ends/corners, row supply straps, and M4
feeds. **This is not a complete, tapeout-ready OpenRAM SRAM port.** Replica
integration, peripherals, complete-macro verification, and characterization
remain. The generic compiler has not been switched to this array globally.

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

Creating a generic `bitcell_array` still does not insert foundry taps/end
cells. Use the technology-specific module below for a framed array. API
tests disable the incomplete generic verifier; physical verification uses
the installed PDK runners explicitly, not a blanket DRC waiver.

## Foundry array frame (step 1)

```python
array = factory.create(module_type="ihp_bitcell_array", rows=16, cols=32)
# 512 bits; full framed envelope 93.14 × 18.92 µm.
```

Supported dimensions are **16 rows, 4–32 columns in groups of four**.
Other heights, offset parity, and replica attachments are rejected rather
than extrapolating an unverified tap topology. The unchanged reference uses
top/bottom taps for this 16-row height. The core remains 2.81 × 1.07 µm per
bit; the frame does not enlarge the bitcell pitch.

The importer emits three overlays, deliberately excluding only the core
bitcell geometry so OpenRAM retains real individually connected bit instances:

- `ihp_frame_tile`: two columns of top/bottom taps and the extra Via2/M3
  supply straps from `BITKIT_CELL_2x1`.
- `ihp_frame_edge`: the complete 16-row side edge and its two physical
  corners, reflected for the right side. The source's two dummy NMOS per
  row are included in SPICE; one gate in each pair is intentionally floating.
- `ihp_frame_power`: the original alternating GND/VDD M4 feeds for four
  columns, including Via3 arrays.

The 16×32 output has **zero manufacturing-layer polygon XOR** against
`RM_IHPSG13_1P_MATRIX_16x32`, after translating the reference by
(1.61, 1.435) µm. This compares the actual factory-written GDS, including
its pin routing, to the original shipped matrix—not to another reconstruction.
The full envelope area is 1762.2088 µm², identical to that reference matrix;
it excludes the macro's decoder, column circuitry, and control logic.

To export and verify a supported width inside the container:

```sh
iic-pdk ihp-sg13g2
R=/foss/designs/ihp-openram/OpenRAM
python3 "$R/technology/ihp_sg13g2/tests/verify_array.py" --cols 32 \
  --output /tmp/ihp-frame-16x32
```

The checker keeps the original compiler GDS/SPICE, the LVS views, and logs.
DRC uses the installed main/maximal decks with the original SRAM marker
intact and `--no_density`; it does not disable SRAM-related rule categories.
The shipped matrix is the geometric authority for this reuse, not a claim
that the public general rules cover every private SRAM manufacturing rule.
Density/fill, antenna, integration context, and fabrication signoff remain
outside this standalone-array check.

LVS uses strict top-level ports and **no implicit-net joins**. Its separate
view removes child text labels (otherwise storage probes become macro
ports in flat extraction) and only Metal2/Metal3 datatype-29 `lvsres`
recognition markers. This implements the same through-pin joining as the
five-port netlist; no manufacturing polygons, contacts, or SRAM marker are
removed. The LVS CDL changes X model calls to M devices for the PDK reader.
`--disable_tap_extraction` omits tap *devices* absent from the schematic;
physical tap-to-body connectivity is still extracted and compared.
An unnormalized flat LVS run is not expected to match these joined-pin views.

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
- Four API/geometry regression tests pass, including the complete framed
  16×32 matrix comparison against the shipped GDS.
- All eight supported widths (4, 8, 12, 16, 20, 24, 28, 32 columns) pass
  installed-PDK main/maximal DRC with density disabled and the strict LVS
  comparison described above. The LVS views retain identical manufacturing
  geometry to their original compiler GDS.
- An independently tiled source array has zero physical-layer XOR difference
  from the actual factory-generated 3×4 GDS, including its pin routing.
- A nominal TT/1.2 V ngspice smoke test writes 1, holds 1, writes 0, holds 0.
  This is not read-margin, PVT, mismatch, timing, or yield characterization.
- Official KLayout DRC on the **core-only** array still reports `LU.a`,
  `LU.b`, and `NW.b1`, as does the equivalently isolated foundry core array.
  The shipped block with its original tap/end context passes. The framed
  array now supplies those structures rather than suppressing their errors.

Bring-up GDS, SPICE, simulation and DRC logs are in the sibling layout repo's
locally ignored `.amp/in/artifacts/openram-foundry/` directory. They are not
part of the technology library or evidence of complete SRAM signoff.
Frame checks are in the sibling repo's `.amp/in/artifacts/array-frame/`.

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
checks, DRC/LVS, and characterization. BLDRV is now available as the explicit
hard cell below, but neither peripheral is enabled in the generic SRAM
assembly. The next integration step is the sense amplifier, followed by an
IHP column-data module that does not duplicate BLDRV's precharge/mux circuitry.

## BLDRV hard-cell bring-up

```python
driver = factory.create(module_type="ihp_bldrv")
# NOT module_type="write_driver": this cell also precharges and selects.
```

`import_sram.py` imports the unchanged `RM_IHPSG13_1P_BLDRV` polygons and
recursively flattens its matching CDL plus two NANDs and three inverters.
All 22 FETs retain their source W/L/m; X model calls are used for simulation.
The source pin texts are on datatype 2. Canonical datatype-25 labels are
added at those same physical terminals after translating by (0.510, 4.725) µm.

| Source terminal | OpenRAM terminal | Metal |
|---|---|---|
| BLT / BLC | bl / br | M2 |
| BLT_SEL / BLC_SEL | bl_sel / br_sel | M3 |
| PRE_N | pre_n | M1 |
| SEL_P | sel_p | M1 |
| WR_ONE / WR_ZERO | wr_one / wr_zero | M1 |
| VDD! / VSS! | vdd / gnd | M1, two must-connect rails each |

The control contract, confirmed by DC simulation, is:

- `pre_n=0` charges both bitlines, independent of selection. There is no
  separate bitline equalizer transistor in this block.
- `sel_p=1` connects the bitlines to the selected read lines through PMOS
  pass devices; this is intended for high-common-mode, small-swing reads,
  not guaranteed full-swing CMOS transmission.
- With `pre_n=1, sel_p=1`, `wr_one=1, wr_zero=0` drives bl high / br low;
  the opposite controls drive bl low / br high.
- For reading, both write controls are zero. Selection low isolates the
  selected read lines and disables write drive.
- Do not assert both write controls or overlap precharge with a selected
  write: these cause pull-up/pull-down contention. Sequencing is still the
  responsibility of the future column/control adapter.

The reported 4.08 × 17.625 µm boundary is a **geometry envelope, not an array
repeat pitch**. The shipped parent uses staggered/reflected overlapping
placements; do not tile drivers at `driver.width` or assume exact bitcell
pitch alignment. Parent routing must connect both VDD and both GND rails.

Verification inside IIC-OSIC with the selected IHP PDK:

- Zero polygon XOR versus the shipped BLDRV after translation, except
  intentional label/boundary metadata.
- Both the isolated original and imported cell pass installed main/maximal
  DRC with `--no_density`; no SRAM marker or rule waiver is added.
- Strict-port KLayout LVS passes with `--disable_tap_extraction` and
  `--implicit_nets=vdd,gnd`. **Those supply joins are a bottom-up assumption,
  not proof that parent power routing is complete.** No signal joins,
  ignored ports, or transistor black boxes are used. CDL changes X calls
  back to M devices for the LVS reader.
- Seven regression tests pass, including BLDRV loading/pins, source XOR,
  LVS, and 21 DC operating cases: precharge selected/deselected, write both
  values, read selected/deselected with asymmetric levels, and a deselected
  write. Cases run at TT/1.20 V, SS/1.08 V, FF/1.32 V, all at 27 °C.

Run the existing `tests/test_bitcell.py -v` command above to repeat these
API/geometry, LVS, and electrical checks. DRC uses the same installed
`run_drc.py --path=... --run_dir=... --no_density` command as the frame.
Saved bring-up views and logs are in the sibling layout repo's locally
ignored `.amp/in/artifacts/bldrv/` directory. These are static hard-cell
checks, not timing, parasitic, noise-margin, mismatch, or full-memory tests.

## c4m / PDKMaster comparison

The inspected local FlexMem builds its own procedural bitcells, with taps
embedded at cell boundaries and shared by abutment; it does not import IHP
BITKIT. The c4m IHP model declares an `SRAM` auxiliary layer, but explicitly
leaves `extra/relaxed rules inside SRAM layer` as TODO in
`c4m/pdk/ihpsg13g2/pdkmaster.py`. PDKMaster derives rules from its encoded
primitive model; satisfying that subset is not full foundry DRC signoff.
No SRAM DRC pass/fail reports were found in these checkouts. Their configured
IHP library signoff targets standard-cell/I/O libraries, not FlexMem SRAM.
This is useful generator architecture reference, not evidence to waive or
replace the shipped BITKIT frame. FlexMem also currently assumes one NMOS
implant, whereas the c4m IHP NMOS primitive declares none, so those checked-out
versions are not a demonstrated drop-in working IHP SRAM flow.

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
