# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os
import inspect
import globals
import sys

# the debug levels:
# 0 = minimum output (default)
# 1 = major stages
# 2 = verbose
# n = custom setting


def check(check, str):
    if not check:
        (frame, filename, line_number, function_name, lines,
         index) = inspect.getouterframes(inspect.currentframe())[1]
        sys.stderr.write("ERROR: file {0}: line {1}: {2}\n".format(
            os.path.basename(filename), line_number, str))
        log("ERROR: file {0}: line {1}: {2}\n".format(
            os.path.basename(filename), line_number, str))

        assert 0


def error(str, return_value=0):
    (frame, filename, line_number, function_name, lines,
     index) = inspect.getouterframes(inspect.currentframe())[1]
    sys.stderr.write("ERROR: file {0}: line {1}: {2}\n".format(
        os.path.basename(filename), line_number, str))
    log("ERROR: file {0}: line {1}: {2}\n".format(
        os.path.basename(filename), line_number, str))

    assert return_value == 0


def warning(str):
    (frame, filename, line_number, function_name, lines,
     index) = inspect.getouterframes(inspect.currentframe())[1]
    sys.stderr.write("WARNING: file {0}: line {1}: {2}\n".format(
        os.path.basename(filename), line_number, str))
    log("WARNING: file {0}: line {1}: {2}\n".format(
        os.path.basename(filename), line_number, str))


def print_raw(str):
    print(str)
    log(str)


def log(str):
    if globals.OPTS.output_name != '':
        if log.create_file:
            # We may have not yet read the config, so we need to ensure
            # it ends with a /
            # This is also done in read_config if we change the path
            # FIXME: There's actually a bug here. The first few lines
            # could be in one log file and after read_config it could be
            # in another log file if the path or name changes.
            if not globals.OPTS.output_path.endswith('/'):
                globals.OPTS.output_path += "/"
            if not os.path.isdir(globals.OPTS.output_path):
                os.mkdir(globals.OPTS.output_path)
            compile_log = open(globals.OPTS.output_path +
                               globals.OPTS.output_name + '.log', "w+")
            log.create_file = 0
        else:
            compile_log = open(globals.OPTS.output_path +
                               globals.OPTS.output_name + '.log', "a")

        if len(log.setup_output) != 0:
            for line in log.setup_output:
                compile_log.write(line)
            log.setup_output = []
        compile_log.write(str + '\n')
    else:
        log.setup_output.append(str + "\n")


# use a static list of strings to store messages until the global paths are set up
log.setup_output = []
log.create_file = True


def info(lev, str):
    from globals import OPTS
    if (OPTS.debug_level >= lev):
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        # classname = frm.f_globals['__name__']
        if mod.__name__ == None:
            class_name = ""
        else:
            class_name = mod.__name__
        print_raw("[{0}/{1}]: {2}".format(class_name,
                                          frm[0].f_code.co_name, str))
