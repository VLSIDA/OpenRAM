#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

import unittest
from testutils import *
import sys,os,re
sys.path.append(os.getenv("OPENRAM_HOME"))
import globals
import debug

class code_format_test(openram_test):
    "Run a test to check for tabs instead of spaces in the all source files."

    def runTest(self):
        source_code_dir = os.environ["OPENRAM_HOME"]
        source_codes = setup_files(source_code_dir)
        errors = 0

        # Check for tabs or carriage returns
        for code in source_codes:
            if re.search("gdsMill", code):
                continue
            errors += check_file_format_tab(code)
            errors += check_file_format_carriage(code)            

        for code in source_codes:
            if re.search("gdsMill", code):
                continue
            if re.search("debug.py$", code):
                continue
            if re.search("openram.py$", code):
                continue
            if re.search("testutils.py$", code):
                continue
            if re.search("gen_stimulus.py$", code):
                continue
            errors += check_print_output(code)


        # fails if there are any tabs in any files
        self.assertEqual(errors, 0)


def setup_files(path):
    files = []
    for (dir, _, current_files) in os.walk(path):
        for f in current_files:
            files.append(os.getenv("OPENRAM_HOME"))
    nametest = re.compile("\.py$", re.IGNORECASE)
    select_files = list(filter(nametest.search, files))
    return select_files


def check_file_format_tab(file_name):
    """
    Check if any files contain tabs and return the number of tabs.
    """
    f = open(file_name, "r+b")
    key_positions = []
    for num, line in enumerate(f, 1):
        if b'\t' in line:
            key_positions.append(num)
    if len(key_positions) > 0:
        if len(key_positions)>10:
            line_numbers = key_positions[:10] + [" ..."]
        else:
            line_numbers = key_positions
        debug.info(0, '\nFound ' + str(len(key_positions)) + ' tabs in ' +
                   str(file_name) + ' (lines ' + ",".join(str(x) for x in line_numbers) + ')')
    f.close()
    return len(key_positions)


def check_file_format_carriage(file_name):
    """
    Check if file contains carriage returns at the end of lines 
    and return the number of carriage return lines.
    """

    f = open(file_name, 'r+b')
    key_positions = []
    for num, line in enumerate(f.readlines()):
        if b'\r\n' in line:
            key_positions.append(num)
    if len(key_positions) > 0:
        if len(key_positions)>10:
            line_numbers = key_positions[:10] + [" ..."]
        else:
            line_numbers = key_positoins
        debug.info(0, '\nFound ' + str(len(key_positions)) + ' carriage returns in ' +
                   str(file_name) + ' (lines ' + ",".join(str(x) for x in line_numbers) + ')')
    f.close()
    return len(key_positions)


def check_print_output(file_name):
    """Check if any files (except debug.py) call the _print_ function. We should
    use the debug output with verbosity instead!"""
    file = open(file_name, "r+b")
    line = file.read().decode('utf-8')
    # skip comments with a hash
    line = re.sub(r'#.*', '', line)
    # skip doc string comments
    line=re.sub(r'\"\"\"[^\"]*\"\"\"', '', line, flags=re.S|re.M)
    count = len(re.findall("[^p]+print\(", line))
    if count > 0:
        debug.info(0, "\nFound " + str(count) +
                   " _print_ calls " + str(file_name))

    file.close()
    return(count)


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
