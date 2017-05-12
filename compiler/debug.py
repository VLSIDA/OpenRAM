import os
import inspect
import globals
import sys

# the debug levels:
# 0 = minimum output (default)
# 1 = major stages
# 2 = verbose
# n = custom setting

def check(check,str):
    (frame, filename, line_number, function_name, lines,
     index) = inspect.getouterframes(inspect.currentframe())[1]
    if not check:
        print "ERROR: file ", os.path.basename(filename), ": line ", line_number, ": ", str
        sys.exit(-1)

def error(str,return_value=None):
    (frame, filename, line_number, function_name, lines,
     index) = inspect.getouterframes(inspect.currentframe())[1]
    print "ERROR: file ", os.path.basename(filename), ": line ", line_number, ": ", str
    if return_value:
        sys.exit(return_value)

def warning(str):
    (frame, filename, line_number, function_name, lines,
     index) = inspect.getouterframes(inspect.currentframe())[1]
    print "WARNING: file ", os.path.basename(filename), ": line ", line_number, ": ", str


def info(lev, str):
    OPTS = globals.get_opts()
    if (OPTS.debug_level >= lev):
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        print "\n[", frm[0].f_code.co_name, "]: ", str
        # This sometimes gets a NoneType mod...
        # print "[" , mod.__name__ , "]: ", str
