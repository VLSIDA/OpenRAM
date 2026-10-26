# IHP SG13G2 SRAM technology

This port assembles the IHP Open PDK's SRAM hard cells through the normal
OpenRAM compiler API. It supports **64 words × 1–8 data bits**, one RW port,
one bank, four-way column selection, full-word writes, and no spares.
Unsupported organizations fail explicitly. Other technologies retain the
generic SRAM implementation.

**This is a compiler-compatible bring-up port, not a tapeout-qualified SRAM.**
Public no-density DRC, representative strict LVS, functional simulation,
normal exports, and a scoped signal-RC timing experiment have passed.
Manufacturing signoff and production timing-library qualification remain open.

## Build and test

Use the IIC-OSIC container and select the IHP PDK before running commands:

```sh
iic-pdk ihp-sg13g2
R=/foss/designs/ihp-openram/OpenRAM
export OPENRAM_HOME="$R/compiler" OPENRAM_TECH="$R/technology"
python3 "$R/technology/ihp_sg13g2/import_sram.py"
python3 "$R/technology/ihp_sg13g2/tests/test_bitcell.py" -v
python3 "$R/sram_compiler.py" "$R/macros/sram_configs/ihp_sg13g2_sram_1rw_2x64.py"
python3 "$R/technology/ihp_sg13g2/tests/verify_array.py" --sram --cols 8 \
  --output /tmp/ihp-sram-64x2
```

The hard-cell regression suite contains **16 tests**, including geometry,
LVS, and transistor-level electrical checks. Layout import/routing requires
KLayout's Python API, NumPy, and Matplotlib. Electrical checks require ngspice
with the selected PDK's PSP OSDI models. These are available in the IIC-OSIC
environment used for validation. Keep `use_nix=False` with those installed tools.

The example configuration uses `analytical_delay=False`, `trim_netlist=False`,
`use_pex=False`, and `check_lvsdrc=False`. Analytical, trimming, and compiler PEX
modes are unsupported and fail explicitly. Physical verification is a separate,
explicit invocation of `tests/verify_array.py`, not a blanket verification pass.
KLayout verification uses the installed PDK runners and their complete rule-deck
dependencies; this port does not vendor `.lydrc`/`.lylvs` decks or stub macros.
Automatic verification through OpenRAM's generic `check_lvsdrc=True` path is not
integrated. Keep that option disabled and run the explicit checker above.

## Compiler and electrical contract

`tech_modules["sram_1bank"] = "ihp_sram"` selects the synchronous top.
`ihp_input_registers` captures data, all six address bits, CSB, and WEB on the
external rising edge. The foundry controller receives the inverted external
clock and launches access on the falling edge. The standard OpenRAM Verilog
model applies: `csb0=0` selects the memory, `web0=0` writes, and `web0=1` reads.
The low two address bits select a column; the upper four select a row.

The foundry BLDRV combines precharge, column selection, and write drive.
There is **no duplicate generic precharge/mux/write-driver path**. Real gates
encode captured data into mutually exclusive `wr_one` and `wr_zero` controls.
The controller retains the real delay mux with delay-select tied high; removing
that mux eliminates the operation pulse. Its inputs are active high, and ECLK
is idle high/active low. Independent rising-edge request capture is necessary;
clock inversion alone would move both source capture and access to falling edge.

At the internal memory interface:

- `pre_n=0` precharges both bitlines. Never overlap precharge with selected write.
- `sel_0..3` are active-high one-hot read/write column selects.
- `wr_one=1` writes true one; `wr_zero=1` writes zero. Never assert both.
- Sense CP/SAE high evaluates; low resets internal sensing nodes while retaining
  output. The controller's SAE is idle high and rises at the end of a read pulse.
- `qp` is true read data and `qn` its complement. Power-up output is unspecified.
- Row selection requires CS high and ECLK low. The source row decoder contains
  high-transparent address latches, not generic edge-triggered registers.

Characterization obtains real BL/BR/SAE hierarchy through
`get_characterization_probes`, and storage nodes through NT/NC probes.
Electrical read/write/storage checks remain enabled; rising and falling delays
are measured independently. The PDK's ngspice initialization is preserved for
OSDI model loading. The representative input capacitance is 3.6 fF, rounded up
from TT input-charge measurements of 2.69–3.56 fF, not a per-pin/PVT guarantee.

## Physical organization and verification

`import_sram.py` reads the installed PDK's
`libs.ref/sg13g2_sram/gds/RM_IHPSG13_1P_64x16_c2.gds` and matching CDL.
It preserves source transistor dimensions and manufacturing geometry, translates
origins, merges duplicate polygons, and adds canonical pin/boundary metadata.
Through-pin `lvsres` annotations are joined logically; real resistors are not
silently discarded. Private root nets are namespaced to avoid collisions with
canonical public pins.

The assembly hierarchy is:

- `ihp_bitcell_array`: 16 rows, 4–32 columns in groups of four, with source taps,
  ends/corners, row supply straps, and M4 feeds. Core pitch is 2.81 × 1.07 µm,
  with alternate-column/row reflection. The 16×32 framed array has zero
  manufacturing-layer polygon XOR against the shipped matrix.
- `ihp_column_data`: four BLDRVs and one sense/latch, retaining overlapping
  foundry placement and connected parent metal. Hard-cell envelopes are not
  legal repeat pitches. The column assembly physically joins split supply rails.
- `ihp_memory_slice`: framed array plus column groups. It preserves source
  bitline/select connections, adds VDD continuations, and restores parent tap
  completion bridges between groups without changing transistor geometry.
- `ihp_row_memory`: row decoder, sixteen wordline buffers, binary column decoder,
  and memory slice, with explicit signal and supply routing.
- `ihp_sram`: input registers, cycle controller, write encoding, and routed
  synchronous memory. Inputs/clock/supplies have bottom-perimeter M5 pins;
  outputs have top-perimeter M5 pins.

For subassembly checks, the verifier also accepts `--slice`, `--row-memory`,
`--cell`, `--control-cell`, `--control-logic`, and `--input-registers`.
Its output includes raw compiler GDS/SPICE, normalized LVS views, and runner logs.

DRC uses installed main/maximal decks with **density disabled**, retaining SRAM
markers and manufacturing polygons. Core-only arrays lack their required tap
context and are not expected to pass in isolation. LVS uses strict top-level
ports and no implicit-net joins for complete assemblies, with tap-device
extraction disabled because tap devices are absent from the schematic; physical
body connectivity is still compared. Only internal labels and datatype-29
metal through-pin recognition markers are removed in a separate LVS view.
Simulation X model calls become M devices for the LVS reader. No transistor
black boxes or signal-port waivers are used.

All eight complete-macro widths pass public no-density DRC. Widths 1, 2, and 8
pass the stock strict-port flat LVS runner; the final normal compiler 64×2
GDS/LVS-SPICE passes with zero warnings/errors. Intermediate widths additionally
pass an independent full extracted-transistor comparison using uniquely
topology-derived net hints; changed-width and wrong-gate negative controls fail.
That comparison is distinct from the stock runner, not a device waiver.

## Functional and timing evidence

- Loaded peripheral and row-memory regressions cover both data polarities,
  asymmetric row/column addresses, overwrites, retention, and output hold at
  TT/1.20 V, SS/1.08 V, and FF/1.32 V at 27 °C with stated lumped loads.
- The normal 64×2 functional simulator passes at a 16 ns period and 14.4 fF
  output load for TT/1.20 V/27 °C, SS/1.08 V/125 °C, and FF/1.32 V/−55 °C.
  A separate input-capture test changes requests between the two clock edges.
- Normal compilation exports SPICE, LVS-SPICE, GDS, LEF, Verilog, Liberty,
  configuration, and datasheet. The final Verilog parses with Icarus; LEF and
  Liberty load in OpenROAD with the installed technology LEF and all 15 public
  pins accessible. LEF database units are 1000.
- The final 64×2 schematic single-point Liberty at TT/1.20 V/27 °C, 14.4 fF
  load, and 50 ps slew reports 2.181 ns rising and 2.255 ns falling delay,
  with a searched minimum period of 4.531 ns and area of 9607.25 µm².
  These are unextracted nominal results, not a guaranteed frequency.

A separate **64×2 signal-RC timing experiment** used KPEX 0.6.8 2.5D extraction,
2132 physical FETs, 12080 retained resistors, and 105229 retained capacitors.
The full-RC netlist failed a VSS connectivity consistency check; it is not
reported as a full-RC pass. For the signal-only experiment, VDD/VSS were
idealized and signal-to-supply capacitance retained. Connectivity, device
dimensions, and retained resistor components were independently audited,
including wrong-gate/width negative controls. At TT/1.20 V/27 °C, 16 ns period,
14.4 fF load, and 50 ps slew:

| Netlist | Rising delay (ns) | Falling delay (ns) |
|---|---:|---:|
| Schematic control | 2.18864 | 2.26250 |
| Signal RC, ideal supplies | 3.14548 | 3.23445 |

The extracted evaluation passes OpenRAM's read/write/storage/SAE/output checks.
It is **not** compiler `use_pex=True` integration, extracted Liberty generation,
power-grid analysis, or full PVT/load/slew qualification. Density/fill, antenna,
private SRAM manufacturing rules, mismatch/yield, and production per-pin timing
remain outside these results. Manufacturing signoff is not required to establish
the scoped compiler compatibility, but is required before claiming tapeout readiness.

## License and provenance

The source GDS and CDL match IHP Open PDK commit
[`a49358cc`](https://github.com/IHP-GmbH/IHP-Open-PDK/commit/a49358cc0b20635fcb53c0940505e3563763fc7a)
byte-for-byte. SHA-256 hashes are respectively
`0cc794e39c7c6006a7df329c97f73cb38ae6c94feb8761e7756b378cda4302a7`
and `240ef98547a85fa24378a13d5dbd46099b0f23962e953903ad60a81d98b3702b`.
That revision declares Apache-2.0 licensing, with no separate SRAM exception
found. [LICENSE.IHP-PDK](LICENSE.IHP-PDK) retains the upstream license;
[NOTICE](NOTICE) records attribution, source paths, and importer modifications.
Generated SPICE preserves the source CDL notice. Preserve those notices when
redistributing the views. License provenance is not fabrication qualification.
