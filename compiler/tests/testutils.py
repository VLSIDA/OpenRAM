# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import unittest
import sys, os, glob
import pdb
import traceback
import time
from openram import debug
from openram import OPTS


class openram_test(unittest.TestCase):
    """ Base unit test that we have some shared classes in. """

    def setUp(self):
        self.start_time = time.time()

    def tearDown(self):
        duration = time.time() - self.start_time
        print('%s: %.3fs' % (self.id(), duration))

    def fail(self, msg):
        import inspect
        s = inspect.stack()
        base_filename = os.path.splitext(os.path.basename(s[2].filename))[0]

        try:
            OPENRAM_HOME = os.path.abspath(os.environ.get("OPENRAM_HOME"))
        except:
            debug.error("$OPENRAM_HOME is not properly defined.", 1)

        # import shutil
        # zip_file = "{0}/../{1}_{2}".format(OPENRAM_HOME, base_filename, os.getpid())
        # debug.info(0, "Archiving failed temp files {0} to {1}".format(OPTS.openram_temp, zip_file))
        # shutil.make_archive(zip_file, 'zip', OPTS.openram_temp)

        super().fail(msg)

    def local_drc_check(self, w):

        self.reset()

        tempgds = "{}.gds".format(w.name)
        w.gds_write("{0}{1}".format(OPTS.openram_temp, tempgds))
        from openram import verify

        result=verify.run_drc(w.name, tempgds, None)
        if result != 0:
            self.fail("DRC failed: {}".format(w.name))
        elif not OPTS.keep_temp:
            self.cleanup()

    def local_check(self, a, final_verification=False):

        self.reset()

        tempspice = "{}.sp".format(a.name)
        tempgds = "{}.gds".format(a.name)

        a.sp_write("{0}{1}".format(OPTS.openram_temp, tempspice), lvs=True)
        # cannot write gds in netlist_only mode
        if not OPTS.netlist_only:
            a.gds_write("{0}{1}".format(OPTS.openram_temp, tempgds))

            from openram import verify
            # Run both DRC and LVS even if DRC might fail
            # Magic can still extract despite DRC failing, so it might be ok in some techs
            # if we ignore things like minimum metal area of pins
            drc_result=verify.run_drc(a.name, tempgds, tempspice, extract=True, final_verification=final_verification)

            # We can still run LVS even if DRC fails in Magic OR Calibre
            lvs_result=verify.run_lvs(a.name, tempgds, tempspice, final_verification=final_verification)

            # Only allow DRC to fail and LVS to pass if we are using magic
            if lvs_result == 0 and drc_result != 0:
                # import shutil
                # zip_file = "/tmp/{0}_{1}".format(a.name, os.getpid())
                # debug.info(0, "Archiving failed files to {}.zip".format(zip_file))
                # shutil.make_archive(zip_file, 'zip', OPTS.openram_temp)
                self.fail("DRC failed but LVS passed: {}".format(a.name))
            elif drc_result != 0:
                # import shutil
                # zip_file = "/tmp/{0}_{1}".format(a.name, os.getpid())
                # debug.info(0,"Archiving failed files to {}.zip".format(zip_file))
                # shutil.make_archive(zip_file, 'zip', OPTS.openram_temp)
                self.fail("DRC failed: {}".format(a.name))

            if lvs_result != 0:
                # import shutil
                # zip_file = "/tmp/{0}_{1}".format(a.name, os.getpid())
                # debug.info(0,"Archiving failed files to {}.zip".format(zip_file))
                # shutil.make_archive(zip_file, 'zip', OPTS.openram_temp)
                self.fail("LVS mismatch: {}".format(a.name))

            if lvs_result == 0 and drc_result == 0 and not OPTS.keep_temp:
                self.cleanup()
        # For debug...
        # import pdb; pdb.set_trace()

    def run_pex(self, a, output=None):
        tempspice = "{}.sp".format(a.name)
        tempgds = "{}.gds".format(a.name)

        a.gds_write("{0}{1}".format(OPTS.openram_temp, tempgds))

        from openram import verify
        result=verify.run_pex(a.name, tempgds, tempspice, final_verification=False)
        if result != 0:
            self.fail("PEX ERROR: {}".format(a.name))
        return output

    def find_feasible_test_period(self, delay_obj, sram, load, slew):
        """Creates a delay simulation to determine a feasible period for the functional tests to run.
           Only determines the feasible period for a single port and assumes that for all ports for performance.
        """
        debug.info(1, "Finding feasible period for current test.")
        delay_obj.set_load_slew(load, slew)
        test_port = delay_obj.read_ports[0] # Only test one port, assumes other ports have similar period.
        delay_obj.analysis_init(probe_address="1" * sram.addr_size, probe_data=sram.word_size - 1)
        delay_obj.find_feasible_period_one_port(test_port)
        return delay_obj.period

    def cleanup(self):
        """ Reset the duplicate checker and cleanup files. """

        files = glob.glob(OPTS.openram_temp + '*')
        for f in files:
            # Only remove the files
            if os.path.isfile(f):
                os.remove(f)

    def reset(self):
        """
        Reset everything after each test.
        """
        # Reset the static duplicate name checker for unit tests.
        from openram.base import hierarchy_design
        hierarchy_design.name_map=[]

    def check_golden_data(self, data, golden_data, error_tolerance=1e-2):
        """
        This function goes through two dictionaries, key by key and compares
        each item. It uses relative comparisons for the items and returns false
        if there is a mismatch.
        """

        # Check each result
        data_matches = True
        for k in data.keys():
            if type(data[k])==list:
                for i in range(len(data[k])):
                    if not self.isclose(k, data[k][i], golden_data[k][i], error_tolerance):
                        data_matches = False
            else:
                if not self.isclose(k, data[k], golden_data[k], error_tolerance):
                    data_matches = False
        if not data_matches:
            import pprint
            data_string=pprint.pformat(data)
            debug.error("Results exceeded {:.1f}% tolerance compared to golden results:\n".format(error_tolerance * 100) + data_string)
        return data_matches

    def isclose(self, key, value, actual_value, error_tolerance=1e-2):
        """ This is used to compare relative values. """
        from openram import debug
        relative_diff = self.relative_diff(value, actual_value)
        check = relative_diff <= error_tolerance
        if check:
            debug.info(2, "CLOSE\t{0: <10}\t{1:.3f}\t{2:.3f}\tdiff={3:.1f}%".format(key, value, actual_value, relative_diff * 100))
            return True
        else:
            debug.error("NOT CLOSE\t{0: <10}\t{1:.3f}\t{2:.3f}\tdiff={3:.1f}%".format(key, value, actual_value, relative_diff * 100))
            return False

    def relative_diff(self, value1, value2):
        """ Compute the relative difference of two values and normalize to the largest.
        If largest value is 0, just return the difference."""

        # Edge case to avoid divide by zero
        if value1==0 and value2==0:
            return 0.0

        # Don't need relative, exact compare
        if value1==value2:
            return 0.0

        # Get normalization value
        norm_value = abs(max(value1, value2))

        return abs(value1 - value2) / norm_value

    def relative_compare(self, value, actual_value, error_tolerance):
        """ This is used to compare relative values. """
        if (value==actual_value): # if we don't need a relative comparison!
            return True
        return (abs(value - actual_value) / max(value, actual_value) <= error_tolerance)

    def isapproxdiff(self, filename1, filename2, error_tolerance=0.001):
        """Compare two files.

        Arguments:

        filename1 -- First file name

        filename2 -- Second file name

        Return value:

        True if the files are the same, False otherwise.

        """
        import re
        from openram import debug

        numeric_const_pattern = r"""
        [-+]? # optional sign
        (?:
        (?: \d* \. \d+ ) # .1 .12 .123 etc 9.1 etc 98.1 etc
        |
        (?: \d+ \.? ) # 1. 12. 123. etc 1 12 123 etc
        )
        # followed by optional exponent part if desired
        (?: [Ee] [+-]? \d+ ) ?
        """
        rx = re.compile(numeric_const_pattern, re.VERBOSE)
        fp1 = open(filename1, 'rb')
        fp2 = open(filename2, 'rb')
        mismatches=0
        line_num=0
        while True:
            line_num+=1
            line1 = fp1.readline().decode('utf-8')
            line2 = fp2.readline().decode('utf-8')
            # print("line1:", line1)
            # print("line2:", line2)

            # 1. Find all of the floats using a regex
            line1_floats=rx.findall(line1)
            line2_floats=rx.findall(line2)
            debug.info(3, "line1_floats: " + str(line1_floats))
            debug.info(3, "line2_floats: " + str(line2_floats))

            # 2. Remove the floats from the string
            for f in line1_floats:
                line1=line1.replace(f, "", 1)
            for f in line2_floats:
                line2=line2.replace(f, "", 1)
            # print("line1:", line1)
            # print("line2:", line2)

            # 3. Convert to floats rather than strings
            line1_floats = [float(x) for x in line1_floats]
            line2_floats = [float(x) for x in line1_floats]

            # 4. Check if remaining string matches
            if line1 != line2:
                # Uncomment if you want to see all the individual chars of the two lines
                # print(str([i for i in line1]))
                # print(str([i for i in line2]))
                if mismatches==0:
                    debug.error("Mismatching files:\nfile1={0}\nfile2={1}".format(filename1, filename2))
                mismatches += 1
                debug.error("MISMATCH Line ({0}):\n{1}\n!=\n{2}".format(line_num, line1.rstrip('\n'), line2.rstrip('\n')))

            # 5. Now compare that the floats match
            elif len(line1_floats)!=len(line2_floats):
                if mismatches==0:
                    debug.error("Mismatching files:\nfile1={0}\nfile2={1}".format(filename1, filename2))
                mismatches += 1
                debug.error("MISMATCH Line ({0}) Length {1} != {2}".format(line_num, len(line1_floats), len(line2_floats)))
            else:
                for (float1, float2) in zip(line1_floats, line2_floats):
                    relative_diff = self.relative_diff(float1, float2)
                    check = relative_diff <= error_tolerance
                    if not check:
                        if mismatches==0:
                            debug.error("Mismatching files:\nfile1={0}\nfile2={1}".format(filename1, filename2))
                        mismatches += 1
                        debug.error("MISMATCH Line ({0}) Float {1} != {2} diff: {3:.1f}%".format(line_num, float1, float2, relative_diff * 100))

            # Only show the first 10 mismatch lines
            if not line1 and not line2 or mismatches>10:
                fp1.close()
                fp2.close()
                return mismatches==0

        # Never reached
        return False

    def isdiff(self, filename1, filename2):
        """ This is used to compare two files and display the diff if they are different.. """
        from openram import debug
        import filecmp
        import difflib
        check = filecmp.cmp(filename1, filename2)
        if not check:
            debug.error("MISMATCH file1={0} file2={1}".format(filename1, filename2))
            f1 = open(filename1, mode="r", encoding='utf-8')
            s1 = f1.readlines()
            f1.close()
            f2 = open(filename2, mode="r", encoding='utf-8')
            s2 = f2.readlines()
            f2.close()
            mismatches=0
            for line in list(difflib.unified_diff(s1, s2)):
                mismatches += 1
                if mismatches==0:
                    print("DIFF LINES:")

                if mismatches<11:
                    print(line.rstrip('\n'))
                else:
                    return False
            return False
        else:
            debug.info(2, "MATCH {0} {1}".format(filename1, filename2))
        return True

    def dbg():
        import pdb; pdb.set_trace()


def header(filename, technology):
    # Skip the header for gitlab regression
    import getpass
    if getpass.getuser() == "gitlab-runner":
        return

    tst = "Running Test for:"
    print("\n")
    print(" ______________________________________________________________________________ ")
    print("|==============================================================================|")
    print("|=========" + tst.center(60) + "=========|")
    print("|=========" + technology.center(60) + "=========|")
    print("|=========" + filename.center(60) + "=========|")
    from openram import OPTS
    if OPTS.openram_temp:
        print("|=========" + OPTS.openram_temp.center(60) + "=========|")
    print("|==============================================================================|")


def debugTestRunner(post_mortem=None):
    """unittest runner doing post mortem debugging on failing tests"""
    if post_mortem is None and OPTS.debug:
        post_mortem = pdb.post_mortem

    class DebugTestResult(unittest.TextTestResult):
        def addError(self, test, err):
            # called before tearDown()
            traceback.print_exception(*err)
            if post_mortem:
                post_mortem(err[2])
            super(DebugTestResult, self).addError(test, err)

        def addFailure(self, test, err):
            traceback.print_exception(*err)
            if post_mortem:
                post_mortem(err[2])
            super(DebugTestResult, self).addFailure(test, err)
    return unittest.TextTestRunner(resultclass=DebugTestResult)
