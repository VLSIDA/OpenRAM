#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import sys, os, re
import unittest
from testutils import *

import openram
from openram import debug


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
            errors += check_file_format_whitespace(code)

        # Check for "print"
        for code in source_codes:
            if re.search("gdsMill", code):
                continue
            if re.search("debug.py$", code):
                continue
            if re.search("sram_compiler.py$", code):
                continue
            if re.search("testutils.py$", code):
                continue
            if re.search("gen_stimulus.py$", code):
                continue
            errors += check_print_output(code)

        # Check for copyright
        for code in source_codes:
            if re.search("gdsMill", code):
                continue
            errors += check_copyright(code)

        # fails if there are any tabs in any files
        self.assertEqual(errors, 0)


def setup_files(path):
    files = []
    for (dir, _, current_files) in os.walk(path):
        for f in current_files:
            files.append(os.path.join(dir, f))
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
            line_numbers = key_positions
        debug.info(0, '\nFound ' + str(len(key_positions)) + ' carriage returns in ' +
                   str(file_name) + ' (lines ' + ",".join(str(x) for x in line_numbers) + ')')
    f.close()
    return len(key_positions)


def check_file_format_whitespace(file_name):
    """
    Check if file contains a line with whitespace at the end
    and return the number of these lines.
    """

    f = open(file_name, "r")
    key_positions = []
    for num, line in enumerate(f.readlines()):
        if re.match(r".*[ \t]$", line):
            key_positions.append(num)
    if len(key_positions) > 0:
        if len(key_positions) > 10:
            line_numbers = key_positions[:10] + [" ..."]
        else:
            line_numbers = key_positions
        debug.info(0, "\nFound " + str(len(key_positions)) + " ending whitespace in " +
                   str(file_name) + " (lines " + ",".join(str(x) for x in line_numbers) + ")")
    f.close()
    return len(key_positions)


def check_print_output(file_name):
    """Check if any files (except debug.py) call the _print_ function. We should
    use the debug output with verbosity instead!"""

    skip_files = ["printGDS.py", "uniquifyGDS.py", "processGDS.py", "model_data_util.py"]
    base_file_name = os.path.basename(file_name)
    if base_file_name in skip_files:
        return(0)
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


def check_copyright(file_name):
    """ Check if any file doesn't contain the copyright at the top. """

    from datetime import date
    year = date.today().year
    old_copyright = ("# See LICENSE for licensing information.\n"
                     "#\n"
                     "# Copyright (c) 2016-{} Regents of the University of California and The Board\n"
                     "# of Regents for the Oklahoma Agricultural and Mechanical College\n"
                     "# (acting for and on behalf of Oklahoma State University)\n"
                     "# All rights reserved.\n"
                     "#\n").format(year)
    new_copyright = ("# See LICENSE for licensing information.\n"
                     "#\n"
                     "# Copyright (c) 2016-{} Regents of the University of California, Santa Cruz\n"
                     "# All rights reserved.\n"
                     "#\n").format(year)
    skip_files = []
    base_file_name = os.path.basename(file_name)
    if base_file_name in skip_files:
        return 0
    file = open(file_name, "r")
    line = file.read()
    file.close()
    # Skip possible shebang at the top
    line = re.sub(r'#!.*\n', '', line)
    # Check if copyright is missing
    if not line.startswith(old_copyright) and not line.startswith(new_copyright):
        debug.info(0, "\nFound missing/wrong copyright in " + file_name)
        return 1
    return 0


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
