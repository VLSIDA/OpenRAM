# Porting to a New Technology

If you want to support a new technology, you will need to create:
+ a setup script for each technology you want to use
+ a technology directory for each technology with the base cells

We provide two technology examples for [SCMOS] and [FreePDK45]. Each
specific technology (e.g., [FreePDK45]) should be a subdirectory
(e.g., `$OPENRAM_TECH/freepdk45`) and include certain folders and files:
* `gds_lib` folder with all the `.gds` (premade) library cells:
  * `dff.gds`
  * `sense_amp.gds`
  * `write_driver.gds`
  * `cell_1rw.gds`
  * `replica\_cell\_1rw.gds`
  * `dummy\_cell\_1rw.gds`
* `sp_lib` folder with all the `.sp` (premade) library netlists for the above cells.
* `layers.map`
* A valid tech Python module (tech directory with `__init__.py` and `tech.py`) with:
  * References in tech.py to spice models
  * DRC/LVS rules needed for dynamic cells and routing
  * Layer information
  * Spice and supply information
  * etc.



[FreePDK45]: https://www.eda.ncsu.edu/wiki/FreePDK45:Contents
[SCMOS]:     https://www.mosis.com/files/scmos/scmos.pdf
