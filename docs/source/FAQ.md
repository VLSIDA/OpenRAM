### [Go Back](./index.md#table-of-contents)

# Frequently Asked Questions

## What units are `word_size` and `write_size` in?

Both are in **bits**, not bytes.

`word_size` is the width of a data word in bits. It is the number of bitcell
columns per word: `sram_config` computes `num_cols = words_per_row * word_size`,
so a 9-bit word is `word_size = 9` and needs no rounding up to a byte multiple.

`write_size` is the write-mask granularity, also in bits. It defaults to
`word_size` (one mask bit, i.e. no write mask) and otherwise gives
`ceil(word_size / write_size)` mask bits. Setting `write_size = 8` is what
produces byte write masks, and this is probably where the "bytes" idea comes
from — the byte is the mask granularity, not the unit of `word_size`.

For a worked example, `macros/sram_configs/sky130_sram_2kbyte_1rw1r_32x512_8.py`
is:

```python
word_size = 32   # Bits
num_words = 512
write_size = 8   # Bits
```

which is 32 bits x 512 words = 16384 bits = 2 kbyte, matching the macro name,
with byte write masks. The trailing `8` in these macro names is `write_size`.

Capacity in bytes is therefore `word_size * num_words / 8`.

## What to do if OpenRAM encounters an error?

When OpenRAM runs, it puts files in a temporary directory that is
shown in the banner at the top. Like:
```
  /tmp/openram_mrg_18128_temp/
```
This is where simulations and DRC/LVS get run so there is no network
traffic. The directory name is unique for each person and run of
OpenRAM to not clobber any files and allow simultaneous runs. If it
passes, the files are deleted. If it fails, you will see these files:
+ `temp.gds` is the layout (.mag files too if using SCMOS)
+ `temp.sp` is the netlist
+ `test1.drc.err` is the std err output of the DRC command
+ `test1.drc.out` is the standard output of the DRC command
+ `test1.drc.results` is the DRC results file
+ `test1.lvs.err` is the std err output of the LVS command
+ `test1.lvs.out` is the standard output of the LVS command
+ `test1.lvs.results` is the DRC results file

Depending on your DRC/LVS tools, there will also be:
+ `run\_drc.sh` is a script to run DRC
+ `run\_ext.sh` is a script to run extraction
+ `run\_lvs.sh` is a script to run LVS

If DRC/LVS fails, the first thing is to check if it ran in the `.out` and
`.err` file. This shows the standard output and error output from
running DRC/LVS. If there is a setup problem it will be shown here.

If DRC/LVS runs, but doesn't pass, you then should look at the `.results`
file. If the DRC fails, it will typically show you the command that was used
to run Calibre or Magic+Netgen. 


