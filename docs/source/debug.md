### [Go Back](./index.md#table-of-contents)

# Debugging and Unit Testing
This page of the documentation explains the debugging and unit testing of OpenRAM.



## Table of Contents
1. [Unit Tests](#unit-tests)
2. [Unit Test Organization](#unit-test-organization)
3. [Running Unit Tests](#running-unit-tests)
4. [Successful Unit Tests](#successful-unit-tests)
5. [Debugging Unsuccessful Unit Tests](#debugging-unsuccessful-unit-tests-or-openrampy)
6. [Temporary Output Files](#temporary-output-files)



## Unit Tests
OpenRAM has the set of thorough regression tests implemented with the Python unit test framework:
* Unit tests allow users to add features without worrying about breaking functionality. 
* Unit tests guide users when porting to new technologies. 
* Every sub-module has its own regression test. 
* There are regression tests for memory functionality, library cell verification, timing verification, and technology verification.



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



## Running Unit Tests

Regression testing  performs a number of tests for all modules in OpenRAM.
From the unit test directory ($OPENRAM\_HOME/tests),
use the following command to run all regression tests:

```
cd OpenRAM/compiler/tests
make -j 3
```
The -j can run with 3 threads. By default, this will run in all technologies.

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

To increase the verbosity of the test, add one (or more) -v options and
pass it as an argument to OpenRAM:
```
ARGS="-v" make 05_bitcell_array_test
```

Unit test results are put in a directory:
```
OpenRAM/compiler/tests/results/<technology>/<test>
```
If the test fails, there will be a tmp directory with intermediate results.
If the test passes, this directory will be deleted to save space.
You can view the .out file to see what the output of a test is in either case.
* Tests can be run in the `$OPENRAM_HOME/tests` directory
* Command line arguments 
    * `-v` for verbose
    * `-t` freepdk45 for tech
    * `-d` to preserve /tmp results (done automatically if test fails)
* Individual tests
    * `01_library_drc_test.py`
* All tests
    * `regress.py`


## Successful Unit Tests
```console
user@host:/openram/compiler/tests$ ./regress.py
 ______________________________________________________________________________ 
|==============================================================================|
|=========                     Running Test for:                      =========|
|=========                         scn4m_subm                         =========|
|=========                        ./regress.py                        =========|
|=========                /tmp/openram_mrg_13245_temp/                =========|
|==============================================================================|
runTest (00_code_format_check_test.code_format_test) ... ok
runTest (01_library_drc_test.library_drc_test) ... ok
runTest (02_library_lvs_test.library_lvs_test) ... ok
runTest (03_contact_test.contact_test) ... ok
runTest (03_path_test.path_test) ... ok
.
.
.
```
```console
user@host:/openram/compiler/tests$ ./03_ptx_1finger_nmos_test.py
 ______________________________________________________________________________ 
|==============================================================================|
|=========                     Running Test for:                      =========|
|=========                         scn4m_subm                         =========|
|=========               ./03_ptx_1finger_nmos_test.py                =========|
|=========                /tmp/openram_mrg_13750_temp/                =========|
|==============================================================================|
.
----------------------------------------------------------------------
Ran 1 test in 0.596s

OK
```



## Debugging Unsuccessful Unit Tests (or openram.py)
* You will get an ERROR during unit test and see a stack trace 
* Examine the temporary output files in the temp directory (/tmp/mydir)
```console
 _____________________________________________________________________________ 
|==============================================================================|
|=========                     Running Test for:                      =========|
|=========                         scn4m_subm                         =========|
|=========                   ./04_pinv_10x_test.py                    =========|
|=========                         /tmp/mydir                         =========|
|==============================================================================|
ERROR: file magic.py: line 174: DRC Errors pinv_0	2
F
======================================================================
FAIL: runTest (__main__.pinv_test)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "./04_pinv_10x_test.py", line 22, in runTest
    self.local_check(tx)
  File "/Users/mrg/openram/compiler/tests/testutils.py", line 45, in local_check
    self.fail("DRC failed: {}".format(a.name))
AssertionError: DRC failed: pinv_0

----------------------------------------------------------------------
Ran 1 test in 0.609s

FAILED (failures=1)
```

### It didn't finish... where are my files?
* OpenRAM puts all temporary files in a temporary directory named:
    * `/tmp/openram_<user>_<pid>_temp`
    * This allows multiple processes/users to simultaneously run
    * This allows /tmp to be mapped to a RAM disk for faster performance
    * After a successful run, the directory and contents are deleted
    * To preserve the contents, you can run with the `-d` option for debugging
* `OPENRAM_TMP` will override the temporary directory location for debug
    * `export OPENRAM_TMP="/home/myname/debugdir"`



## Temporary Output Files
* DRC standard output (`*.drc.out`), errors (`*.drc.err`), and results (`*.drc.results`)
* LVS standard output (`*.lvs.out`), errors (`*.lvs.out`), and results (`*.lvs.results`)
* GDS (and Magic) files for intermediate modules (`temp.gds`, `temp.mag`)
* SPICE netlist for intermediate module results (`temp.sp`)
* Extracted layout netlist for intermediate module results (`extracted.sp`)
* Magic only: Run scripts for DRC (`run_drc.sh`) and LVS (`run_lvs.sh`)
* Calibre only: Runset file for DRC (`drc_runset`) and LVS (`lvs_runset`)




