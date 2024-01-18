### [Go Back](./index.md#table-of-contents)

# Debugging and Unit Testing
This page of the documentation explains the debugging and unit testing of
OpenRAM.



## Table of Contents
1. [Unit Tests](#unit-tests)
1. [Unit Test Organization](#unit-test-organization)
1. [Running Unit Tests](#running-unit-tests)
1. [Successful Unit Tests](#successful-unit-tests)
1. [Debugging Unsuccessful Unit Tests](#debugging-unsuccessful-unit-tests-or-sram_compilerpy)
1. [Temporary Output Files](#temporary-output-files)



## Unit Tests
OpenRAM has the set of thorough regression tests implemented with the Python
unit test framework:
* Unit tests allow users to add features without worrying about breaking
  functionality.
* Unit tests guide users when porting to new technologies. 
* Every sub-module has its own regression test. 
* There are regression tests for memory functionality, library cell
  verification, timing verification, and technology verification.



## Unit Test Organization
* `00_code_format_test.py` does basic lint checking.
* `01_library_drc_test.py` checks DRC of all library cells for the technology.
* `02_library_lvs_test.py` checks LVS of all library cells for the technology.
* `03_*_test.py` checks DRC and LVS of wires and transistors classes.
* `04_*_test.py` checks DRC and LVS of parameterized cells.
* `05-19_*_test.py` checks DRC and LVS of module cells (moving upward in hierarchy with numbers)
* `20_*_test.py` check DRC and LVS of full SRAM layouts with various configurations.
* `21_*_test.py` checks timing of full SRAMs and compares (with tolerance) to precomputed result.
    > **Note**: These tests may fail using different simulators due to the tolerance level.
* `22_*_test.py` checks functional simulation of full SRAMs with various configurations.
* `23-25_*_test.py` checks lib, lef, and verilog outputs using diff.
* `30_openram_test.py` checks command-line interface and whether output files are created.

## Setup

Before running any unit tests, make sure to install OpenRAM.

> See [Python library](./python_library.md#go-back) for details.

If you have the library already installed and `OPENRAM_HOME` set, the library will use the installation on the `OPENRAM_HOME` path.

## Running Unit Tests
Regression testing performs a number of tests for all modules in OpenRAM. From
the unit test directory (`$OPENRAM_HOME/tests`), use the following command to run
all regression tests:

```
cd OpenRAM/compiler/tests
make -j 3
```

The `-j` can run with 3 threads. By default, this will run in all technologies.
> **Note**: If you have not run openram before running unit tests, the conda
> environment will not be installed. You can install it by running
> `OpenRAM/install_conda.sh` (see [Basic Setup](basic_setup.md#anaconda) for
> more details).

To run a specific test in all technologies:
```
cd OpenRAM/compiler/tests
make 05_bitcell_array_test
```
To run a specific technology:
```
cd OpenRAM/compiler/tests
TECHS=scn4m_subm make 05_bitcell_array_test
```

To increase the verbosity of the test, add one (or more) `-v` options and pass
it as an argument to OpenRAM:
```
ARGS="-v" make 05_bitcell_array_test
```

Unit test results are put in a directory:
```
OpenRAM/compiler/tests/results/<technology>/<test>
```
If the test fails, there will be a `tmp` directory with intermediate results. If
the test passes, this directory will be deleted to save space. You can view the
`.out` file to see what the output of a test is in either case.

To preserve results on successful tests (done automatically if test fails):
```
KEEP=1 make 05_bitcell_array_test
```


## Successful Unit Tests
```console
user@host:/openram/compiler/tests$ make
scn4m_subm/12_tri_gate_array_test ... PASS!
scn4m_subm/19_pmulti_bank_test ... PASS!
freepdk45/21_ngspice_delay_global_test ... PASS!
scn4m_subm/23_lib_sram_linear_regression_test ... PASS!
.
.
.
```
```console
user@host:/openram/compiler/tests$ make 01_library_test
scn4m_subm/01_library_test ... PASS!
freepdk45/01_library_test ... PASS!
```



## Debugging Unsuccessful Unit Tests (or sram\_compiler.py)
* You will get a FAIL during unit test
* You can see the output and stack trace in
  `$OPENRAM_HOME/tests/results/<tech>/<test>.out`
* Examine the temporary output files in the temp directory
  (`$OPENRAM_HOME/tests/results/<tech>/<test>/`)
```console
user@host:/openram/compiler/tests$ make 01_library_test
scn4m_subm/01_library_test ... FAIL!
```

### It didn't finish... where are my files?
* OpenRAM puts all temporary files in a temporary directory named:
    * `$OPENRAM_HOME/tests/results/<tech>/<test>/`
    * This allows multiple unit tests to simultaneously run
    * After a successful run, the directory and contents are deleted
    * To preserve the contents, you can run with the `KEEP` option for debugging



## Temporary Output Files
* DRC standard output (`*.drc.out`), errors (`*.drc.err`), and results (`*.drc.results`)
* LVS standard output (`*.lvs.out`), errors (`*.lvs.out`), and results (`*.lvs.results`)
* GDS (and Magic) files for intermediate modules (`temp.gds`, `temp.mag`)
* SPICE netlist for intermediate module results (`temp.sp`)
* Extracted layout netlist for intermediate module results (`extracted.sp`)
* Magic only: Run scripts for DRC (`run_drc.sh`) and LVS (`run_lvs.sh`)
* Calibre only: Runset file for DRC (`drc_runset`) and LVS (`lvs_runset`)



