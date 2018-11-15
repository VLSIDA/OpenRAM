# OpenRAM
[![pipeline status](https://scone.soe.ucsc.edu:8888/mrg/PrivateRAM/badges/dev/pipeline.svg)](https://scone.soe.ucsc.edu:8888/mrg/PrivateRAM/commits/dev)
[![Download](images/download.svg)](https://github.com/VLSIDA/PrivateRAM/archive/dev.zip)
[![License: BSD 3-clause](./images/license_badge.svg)](./LICENSE)

An open-source static random access memory (SRAM) compiler.

# Why OpenRAM?


# Basic Setup

The OpenRAM compiler has very few dependencies:
+ [Ngspice] 26 (or later) or HSpice I-2013.12-1 (or later) or CustomSim 2017 (or later)
+ Python 3.5 and higher
+ Python numpy (pip3 install numpy to install)
+ flask_table (pip3 install flask to install)

If you want to perform DRC and LVS, you will need either:
+ Calibre (for [FreePDK45] or [SCMOS])
+ Magic + Netgen (for [SCMOS] only)

You must set two environment variables: OPENRAM\_HOME should point to
the compiler source directory. OPENERAM\_TECH should point to a root
technology directory that contains subdirs of all other technologies.
For example, in bash, add to your .bashrc:
```
  export OPENRAM_HOME="$HOME/openram/compiler"
  export OPENRAM_TECH="$HOME/openram/technology"
```
For example, in csh/tcsh, add to your .cshrc/.tcshrc:
```
  setenv OPENRAM_HOME "$HOME/openram/compiler"
  setenv OPENRAM_TECH "$HOME/openram/technology"
```

We include the tech files necessary for [FreePDK45] and [SCMOS]. The [SCMOS]
spice models, however, are generic and should be replaced with foundry 
models.
If you are using [FreePDK45], you should also have that set up and have the
environment variable point to the PDK. 
For example, in bash, add to your .bashrc:
```
  export FREEPDK45="/bsoe/software/design-kits/FreePDK45"
```
For example, in csh/tcsh, add to your .tcshrc:
```
  setenv FREEPDK45 "/bsoe/software/design-kits/FreePDK45"
```
We do not distribute the PDK, but you may download [FreePDK45]

If you are using [SCMOS], you should install [Magic] and [Netgen].
We have included the SCN4M design rules from [Qflow].

# Directory Structure

* compiler - openram compiler itself (pointed to by OPENRAM_HOME)
  * compiler/base - base data structure modules
  * compiler/pgates - parameterized cells (e.g. logic gates)
  * compiler/bitcells - various bitcell styles
  * compiler/modules - high-level modules (e.g. decoders, etc.)
  * compiler/verify - DRC and LVS verification wrappers
  * compiler/characterizer - timing characterization code
  * compiler/gdsMill - GDSII reader/writer
  * compiler/router - router for signals and power supplies
  * compiler/tests - unit tests
* technology - openram technology directory (pointed to by OPENRAM_TECH)
  * technology/freepdk45 - example configuration library for [FreePDK45 technology node
  * technology/scn4m_subm - example configuration library [SCMOS] technology node
  * technology/scn3me_subm - unsupported configuration (not enough metal layers)
  * technology/setup_scripts - setup scripts to customize your PDKs and OpenRAM technologies
* docs - LaTeX manual (outdated)
* lib - IP library of pregenerated memories


# Unit Tests

Regression testing  performs a number of tests for all modules in OpenRAM.

Use the command:
```
   python3 regress.py
```
To run a specific test:
```
   python3 {unit test}.py 
```
The unit tests take the same arguments as openram.py itself. 

To increase the verbosity of the test, add one (or more) -v options:
```
   python3 tests/00_code_format_check_test.py -v -t freepdk45
```
To specify a particular technology use "-t <techname>" such as
"-t freepdk45" or "-t scn4m\_subm". The default for a unit test is scn4m_subm. 
The default for openram.py is specified in the configuration file.


# Creating Custom Technologies

If you want to support a enw technology, you will need to create:
+ a setup script for each technology you want to use
+ a technology directory for each technology with the base cells 

All setup scripts should be in the setup\_scripts directory under the
$OPENRAM\_TECH directory.  We provide two technology examples for [SCMOS] and [FreePDK45]. 
Please look at the following file for an example of what is needed for OpenRAM:
```
  $OPENRAM_TECH/setup_scripts/setup_openram_freepdk45.py
```
Each setup script should be named as: setup\_openram\_{tech name}.py.

Each specific technology (e.g., [FreePDK45]) should be a subdirectory
(e.g., $OPENRAM_TECH/freepdk45) and include certain folders and files:
  1. gds_lib folder with all the .gds (premade) library cells. At a
     minimum this includes:
     * ms_flop.gds
     * sense_amp.gds
     * write_driver.gds
     * cell_6t.gds
     * replica_cell_6t.gds 
     * tri_gate.gds
  2. sp_lib folder with all the .sp (premade) library netlists for the above cells.
  3. layers.map 
  4. A valid tech Python module (tech directory with __init__.py and tech.py) with:
     * References in tech.py to spice models
     * DRC/LVS rules needed for dynamic cells and routing
     * Layer information
     * etc.

# License 

OpenRAM is licensed under the [BSD 3-clause License](./LICENSE).

# Contributors & Acknowledgment

- [Matthew Guthaus][Matthew Guthaus] created the OpenRAM project and is the lead architect.


* * *

[Matthew Guthaus]:       https://users.soe.ucsc.edu/~mrg
[Github releases]:       https://github.com/PrivateRAM/PrivateRAM/releases
[Github issues]:         https://github.com/PrivateRAM/PrivateRAM/issues
[Github pull requests]:  https://github.com/PrivateRAM/PrivateRAM/pulls
[Github projects]:       https://github.com/PrivateRAM/PrivateRAM/projects
[Github insights]:       https://github.com/PrivateRAM/PrivateRAM/pulse
[email me]:              mailto:mrg+openram@ucsc.edu
[VLSIDA]:                https://vlsida.soe.ucsc.edu
[OSUPDK]:                https://vlsiarch.ecen.okstate.edu/flow/
[Magic]:                 http://opencircuitdesign.com/magic/
[Netgen]:                http://opencircuitdesign.com/netgen/
[Qflow]:                 http://opencircuitdesign.com/qflow/history.html
[FreePDK45]:             https://www.eda.ncsu.edu/wiki/FreePDK45:Contents
[SCMOS]:                 https://www.mosis.com/files/scmos/scmos.pdf
[Ngspice]:               http://ngspice.sourceforge.net/
