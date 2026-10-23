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
  `RSC_IHPSG13_DFPQD_MSAFFX2N` hierarchy; strict LVS now confirms that it
  matches this CDL despite the extra `N` in the layout name.

These are embedded macro building blocks, not standalone, characterized
OpenRAM-compatible library views. Reusing them needs logical adapters,
pin/placement definitions, enable/precharge sequencing, output-polarity
checks, DRC/LVS, and characterization. BLDRV and the sense/latch are now
available as explicit hard cells below, but neither peripheral is enabled
in the generic SRAM assembly. An IHP column-data hard cell now combines
them with connected source-parent routing and without duplicating BLDRV's
precharge/mux circuitry. The memory slice below joins these blocks to the
framed array; bank decoding/control integration remains outstanding.

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
- Regression tests cover BLDRV loading/pins, source XOR,
  LVS, and 21 DC operating cases: precharge selected/deselected, write both
  values, read selected/deselected with asymmetric levels, and a deselected
  write. Cases run at TT/1.20 V, SS/1.08 V, FF/1.32 V, all at 27 °C.

Run the existing `tests/test_bitcell.py -v` command above to repeat these
API/geometry, LVS, and electrical checks. DRC uses the same installed
`run_drc.py --path=... --run_dir=... --no_density` command as the frame.
Saved bring-up views and logs are in the sibling layout repo's locally
ignored `.amp/in/artifacts/bldrv/` directory. These are static hard-cell
checks, not timing, parasitic, noise-margin, mismatch, or full-memory tests.

## Sense/latch hard-cell bring-up

```python
sense = factory.create(module_type="ihp_sense_amp")
# Native interface: cp dn dp qn qp vdd gnd.
```

The shared peripheral importer preserves the source
`RSC_IHPSG13_DFPQD_MSAFFX2N` geometry, including both half-cell instances,
and imports all 19 FETs from `RSC_IHPSG13_DFPQD_MSAFFX2` CDL. Translation is
(0.510, 0.300) µm; the 9.69 × 9.00 µm boundary is the geometry envelope,
not a compiler column pitch. CP is on M2; DN, DP, QN, QP and supplies are
on M1. One VDD and two GND pin shapes are exposed.

Observed transient contract:

- CP high starts regenerative evaluation. With DP above DN, QP becomes
  high and QN low; opposite differential gives opposite outputs.
- CP low precharges the internal sensing nodes but **retains the output**.
  Once resolved, the output also survives input reversal while CP remains
  high. A low/high clock cycle permits a new decision.
- No power-up output value is guaranteed before a valid evaluation. Do
  not use CP low as an output-reset signal or treat this as a combinational
  sense amplifier.
- The shipped parent connects BLT_SEL to DP and BLC_SEL to DN. It obtains
  true read data by inverting QN externally; the standalone QP has the
  corresponding true polarity but its loading/drive is not characterized.

Both original and imported isolated layouts pass installed main/maximal
DRC with density disabled and no added markers/waivers. Polygon XOR is zero
apart from canonical label/boundary metadata. Strict-port LVS matches all
19 FETs with `--disable_tap_extraction`, **no implicit-net joins**, no
ignored ports, and no black boxes. This establishes the GDS/CDL mapping.

The regression suite also runs three transient sequences at TT/1.20 V,
SS/1.08 V, and FF/1.32 V, at 27 °C with 5 fF on each output. Inputs are at
VDD and 0.95 × VDD (54–66 mV differential). Each sequence checks both
decision polarities, input reversal during CP high, retention during CP
low, and a subsequent opposite decision. This is a functional smoke test,
not minimum input offset, metastability, mismatch, noise-margin, or timing
characterization. These checks run alongside both peripheral LVS checks
and the previous bitcell/frame and BLDRV electrical checks.

Bring-up GDS/SPICE, reference DRC, LVS, and the nominal waveform probe are
in the sibling repo's locally ignored `.amp/in/artifacts/sense-amp/`.
The column assembly below preserves the foundry placement and physically
joins BLDRV's supplies. The slice below validates the array connections;
extracted parasitics and bank integration remain outstanding.

## Four-column physical assembly

`factory.create(module_type="ihp_column_data")` loads four unchanged
BLDRVs sharing one sense/latch, following the `COLCTRL2` connectivity and
physical placement. Both layout and netlist-only modes are supported.
This remains an explicit IHP module, not a generic `port_data` override.
Its 12.24 × 32.865 µm boundary (402.27 µm²) is a geometry envelope, **not
a repeat pitch or a complete memory area**.

Ports, in order, are `bl_0 br_0 ... bl_3 br_3`, `sel_0 ... sel_3`,
`pre_n wr_one wr_zero sae qp qn vdd gnd`. The one-hot `sel` inputs select
both read and write columns. `qp` is the true read result and `qn` its
complement; neither includes a characterized output buffer. The caller
must generate the write-data encoding, one-hot decode, and control timing.
No separate precharge, column mux, or write-driver array is instantiated.
The foundry parent's data/mask registers, BIST logic, clock buffers, and
output inverter are not part of this prototype.

The loaded-path regression exercises the framed slice and row-addressed
assembly below, including all 64 foundry bitcells in 16 rows × four columns,
with ideal supplies, 50 fF lumped load per bitline and 5 fF per sense output.
These are explicit test loads, not extracted
wire capacitances. At each of TT/1.20 V, SS/1.08 V, and FF/1.32 V (27 °C),
40 operations cover writes of both polarities in every column at rows 0,
5, 10 and 15, reads in mixed column order, overwrites in both directions, and
retention of the sixteen programmed cells. Read outputs are checked both
during evaluation and after returning to precharge. No storage-node
initial conditions force the written values. The full suite has thirteen tests.

The conservative test sequence uses a 16 ns operation period: disable
precharge, select a column 1 ns later, drive write data at 2 ns for a
write, assert the wordline at 3 ns, and assert sense enable at 5 ns for a
read. The wordline falls at 8 ns, write/sense enable at 9 ns, column select
at 11 ns, and precharge resumes at 12 ns. Edges take 50 ps. This proves
functional sequencing only, not maximum frequency, offset, mismatch,
read-disturb margin, physical supply integrity, or post-layout operation.

Physical assembly retains the source's overlapping placement, rather than
tiling hard-cell envelopes. In original GDS coordinates (µm), BLDRV columns
0..3 are respectively R0 at (0, −16.8), mirrored about Y at (5.61, −16.8),
R0 at (5.61, −16.8), and mirrored about Y at (11.22, −16.8). The sense
cell is R180 at (9.69, −25.2). The combined geometry is translated by
(0.510, 33.900) µm. Parent metal/vias are cropped at the sense-cell bottom;
the importer rejects any crop that truncates a retained hard-cell shape.
A metal/via connectivity trace removes routing components that do not
touch the five retained hard cells. Connected control stubs remain; no new
manufacturing geometry is drawn. Parent wells, diffusion, poly, contacts,
and implants belonging to omitted circuitry are not imported. Only the
five hard cells supply device geometry. This avoids narrow parent well
slivers left over when their neighboring logic is removed.

Strict-port LVS matches all 107 FETs with `--disable_tap_extraction`, **no
implicit-net joins**, no ignored ports, and no black boxes. All exposed
supply rails are therefore joined in this assembly rather than assumed
joined as in standalone BLDRV verification. The geometry passes installed
main/maximal DRC with density disabled and no rule waivers. Regression
checks also require zero manufacturing XOR through OpenRAM GDS export,
unchanged device-layer geometry for the five hard cells, and no added
manufacturing polygons relative to the source parent.

The empty space left by omitted logic has not been vertically compacted:
preserving the source routing is the first verified implementation, not
an assertion of minimum possible area. The slice below joins this block
to the framed 16-row array. Extracted parasitics remain uncharacterized.

Simulation decks and logs are saved in the sibling layout repo's locally
ignored `.amp/in/artifacts/column-layout/` directory, along with DRC/LVS
results and a KLayout rendering. Repeat the regression
with the same `tests/test_bitcell.py -v` command used above.

## Framed memory slice (not a complete bank)

```python
memory = factory.create(module_type="ihp_memory_slice", cols=32)
# 16 physical rows × 32 physical columns; four columns per word bit.
# Equivalent storage organization: 64 words × 8 bits, but no address decoder.
```

Supported widths are 4..32 columns in groups of four, always 16 rows.
Each four-column group gets one `ihp_column_data`, with no duplicate
precharge/mux/write circuitry. The array's lower-left origin is
(0, 32.840) µm; column group `g` is at (1.260 + 11.240 × g, 0) µm.
These transforms follow the right-hand bank in the source macro and
include a 25 nm overlap at the bitline interface. Bitlines, GND, and the
four column-select buses join through source geometry, not new signal
routing. VDD needs a new M4 continuation per group: a 2.81 µm-wide strip
from y=26 to 33 µm, overlapping both existing supply stripes. Without
this connection, strict LVS reports separate array/column VDD nets.

Between adjacent column groups, four 20 nm × 300 nm active bridges restore
the parent-level tap-stripe completion shapes from `COLCTRL2`. They are
not new transistor geometry. Omitting them leaves 20 nm active gaps and
fails `Act.b`; retaining them clears the abutment findings without waivers.

Top-level ports are `wl_0 ... wl_15`, `sel_0 ... sel_3`, then, for each
group `g`, `pre_n_g sae_g wr_one_g wr_zero_g qp_g qn_g`, then `vdd gnd`.
Wordlines and selection must be one-hot when active. Selection is shared
across word bits by physical source buses. Precharge, sense enable, and
write controls are separate per word bit; a future bank adapter must
distribute controls, encode data/masks, and supply adequate buffering.
The slice is not a replacement for generic `bank` or `port_data` yet.

The height is 51.76 µm; width is the array width (2.81 × cols + 3.22) µm.
Examples: 14.46 × 51.76 µm for 64 × 1 storage and 93.14 × 51.76 µm
for 64 × 8 storage. These envelopes include frame and column circuitry,
but exclude address decoding, wordline drivers, clock/control generation,
output buffers, and final bank power routing.

Verification uses main/maximal DRC with density disabled and strict-port
LVS, no implicit-net joins or black boxes, with tap-device extraction
disabled. All eight supported widths (4, 8, …, 32 columns) pass both
checks. As for the standalone array, the LVS-only GDS removes internal
child labels and datatype-29 Metal2/3 through-pin recognition markers;
raw manufacturing geometry is kept unchanged. Both raw and normalized
views are retained. The physical regression exercises eight columns,
including an inter-group boundary. The original electrical bring-up exercised
four columns at TT/1.20 V, SS/1.08 V, and FF/1.32 V, plus eight columns
at TT/1.20 V with complementary data in the two word bits. These are
functional lumped-load simulations, not PEX, timing, or mismatch signoff.
The expanded current electrical regression includes the row-addressed
assembly described below, retaining a direct-slice TT control case.

Run inside IIC-OSIC after selecting SG13G2:

```sh
python3 technology/ihp_sg13g2/tests/verify_array.py --slice --cols 32 \
  --output ../openram-ihp-port/.amp/in/artifacts/memory-slice/32
```

The verifier retains the existing `array.gds`, `array.sp`, `array.cdl`, and
`array_lvs.gds` filenames for either mode. Artifacts for the width sweep,
transients, and KLayout preview are under `.amp/in/artifacts/memory-slice/`
in the sibling layout repository. Next: row/column decoding and buffered
control/write-data adaptation, then complete-bank routing and PEX-based
timing/characterization. The current physical slice is not a characterized
or fabrication-qualified compiled SRAM.

## Foundry row decoder and wordline drivers

Two additional explicit factory modules reuse the source row path without
changing the generic compiler:

```python
decoder = factory.create(module_type="ihp_row_decoder")
drivers = factory.create(module_type="ihp_wordline_driver")
```

The decoder imports GDS `RM_IHPSG13_1P_ROWDEC4` and CDL
`RM_IHPSG13_64x16_c2_1P_ROWDEC4`, including its address latches and fill
capacitors: 222 unchanged FETs, with a 29.58 × 18.16 µm geometry envelope.
Its ordered ports are `addr_3 ... addr_0 cs eclk decode_15 ... decode_0
vdd gnd`. Source `ADDR_N_I<i>` maps directly to `addr_i`; the importer
does not invert it. At these terminals, the observed decode is ordinary
binary: `addr=5` selects `decode_5`, not `decode_10`.

Selection is active with **CS high and ECLK low**. Either CS low or ECLK
high makes all decode outputs low after settling. CS also clocks the
source's high-transparent address latches; this is not a generic
combinational decoder or an edge-triggered address register. Address
setup/hold and hazard-free control sequencing still need bank-level
verification. Do not connect the generic OpenRAM gated wordline-driver
interface to these terminals without adapting the control protocol.

The drivers import `RM_IHPSG13_1P_WLDRV16X4` and its matching CDL: sixteen
noninverting two-stage buffers, 64 unchanged FETs, with a 12.355 × 18.16 µm
geometry envelope. Ordered ports are `decode_15 ... decode_0 wl_15 ...
wl_0 vdd gnd`. Their supply labels come from datatype-2 child terminals;
the source's bank-level signal labels use datatype 25. These envelopes
are not abutment pitches. The standalone wrappers do not connect the
modules to one another; the row-addressed assembly below now
connects them to each other and the memory slice.

Both factory-exported cells have zero manufacturing-layer polygon XOR
against their respective source cells translated by (0.510, 0.300) µm.
Both pass installed main/maximal DRC with density disabled and strict-port
LVS with tap-device extraction disabled, **no implicit-net joins**, and no
black boxes. The decoder's two `lvsres` clock through-pin annotations are
joined in SPICE; only their Metal2 datatype-29 recognition polygons are
removed from the separate LVS view. Manufacturing geometry is unchanged.
Real resistors remain unsupported by this peripheral importer rather
than silently discarded.

The electrical regression connects the decoder to all sixteen wordline
buffers, each with a 100 fF lumped output load. At TT/1.20 V, SS/1.08 V,
and FF/1.32 V (27 °C), it exercises every binary address in alternating
low/high order and checks all sixteen wordlines in four states: clock
disabled before selection, selected, clock disabled afterward, and CS
disabled with an otherwise active clock. This is 1024 checked voltages
per corner. It establishes settled polarity, address order, and gating,
not maximum frequency, transition hazards, PEX timing, or array-loaded
read/write operation through this row path.

Repeat physical checks inside the selected IIC-OSIC environment:

```sh
python3 technology/ihp_sg13g2/tests/verify_array.py --cell ihp_row_decoder \
  --output ../openram-ihp-port/.amp/in/artifacts/row-path/decoder
python3 technology/ihp_sg13g2/tests/verify_array.py --cell ihp_wordline_driver \
  --output ../openram-ihp-port/.amp/in/artifacts/row-path/driver
```

The existing `tests/test_bitcell.py -v` command includes source-geometry,
LVS, and decoder-to-driver electrical regressions. The assembly below
integrates the row path with the slice; column-address/control adaptation,
a complete bank interface and post-layout characterization remain.

## Row-addressed memory assembly

`factory.create(module_type="ihp_row_memory", cols=32)` physically connects
the foundry decoder and sixteen wordline buffers to `ihp_memory_slice`.
Supported physical widths remain 4..32 columns in groups of four, with
16 rows. This removes the external one-hot wordline interface; it does
not yet provide the complete synchronous compiler/bank interface.

Ordered ports are `addr_3 ... addr_0 cs eclk`, then `sel_0 ... sel_3`,
then each word-bit group's `pre_n_g sae_g wr_one_g wr_zero_g qp_g qn_g`,
then `vdd gnd`. Row addressing is binary and selection requires CS high
with ECLK low. Column selection, write-data encoding, masking, and
precharge/sense timing are still externally supplied. No duplicate
precharge, write-driver or mux blocks are added.

The decoder, wordline drivers, and slice are placed respectively at
(1.20, 33.60), (29.76, 33.60), and (41.25, 0) µm. Their relative positions
follow the source macro's right-hand bank. Short M3 paths connect matching
decoder outputs and driver inputs, and driver outputs to array wordlines.
Two M1 rail continuations join the split bottom supply rails. M5 supply
straps connect these rails to the corresponding existing M4 slice feeds;
new M1-to-M5 via stacks sit in a 1.20 µm left access channel, outside the
decoder's packed M2/M3 routing. Placing those stacks inside the original
decoder envelope produced M2/M3 spacing errors; the separate access
channel avoids those errors without waivers or resizing source devices.
An independent metal/via-only connectivity trace of the eight-column
assembly checks all 2220 recursive VDD/GND labels: one connected metal
component per supply, no missing probes, and no VDD-to-GND short. Thus
power continuity does not depend solely on substrate/well connectivity.

The height remains 51.76 µm. Width is 41.25 µm plus the slice width:
55.71 µm for four columns and 134.39 µm for 32 columns. These are
intermediate assembly envelopes, not final SRAM macro area figures;
clock/control, column decoding, data/mask registers and output buffering
are not included. Space below the decoder remains available for that
logic rather than representing a final compact floorplan.

The physical checker supports `--row-memory` and retains raw and normalized
views as for the existing slice. All eight supported widths (4, 8, …, 32
columns) pass strict-port flat LVS with no implicit-net joins or black
boxes and main/maximal DRC with density disabled. Flat comparison can
be slow for these repeated transistor networks. A hierarchical-mode trial
did not match; the reported passes and supported checker use flat mode.
The regression checks both the original slice and row-addressed assembly
at eight columns, including their inter-group
tap boundary. Run a particular width inside the selected container:

```sh
python3 technology/ihp_sg13g2/tests/verify_array.py --row-memory --cols 32 \
  --output ../openram-ihp-port/.amp/in/artifacts/row-memory/32
```

The memory electrical regression now exercises binary row addresses
through decoder and drivers at TT/1.20 V, SS/1.08 V, and FF/1.32 V for
four columns, and TT/1.20 V for eight columns with complementary word-bit
data. A direct-wordline four-column slice remains a TT control case.
Each case runs 40 operations across all four column choices and rows
0, 5, 10, and 15, covering both values, mixed-order reads, overwrites,
retention, and output hold. Intermediate asymmetric addresses distinguish
row-address bit swaps that testing only 0 and 15 would miss. Loads remain
50 fF per bitline and 5 fF per sense output, with ideal supplies and no PEX.
The 16 ns sequence asserts CS at 1 ns, lowers ECLK at 3 ns, raises it at
8 ns, and lowers CS at 9 ns relative to each operation's start. Other
column/write/precharge/sense timing follows the original slice sequence.

Next: column decoding, clock/control and data/mask adaptation, followed by
normal SRAM compiler entry-point integration and extracted characterization.
These are required for the intended complete technology port, rather than
optional work after upstreaming an isolated-cell prototype.

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
