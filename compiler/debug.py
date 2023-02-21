# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import sys
import os
import pdb
import inspect
from openram import globals

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

        if globals.OPTS.debug:
            pdb.set_trace()

        assert 0


def error(str, return_value=0):
    (frame, filename, line_number, function_name, lines,
     index) = inspect.getouterframes(inspect.currentframe())[1]
    sys.stderr.write("ERROR: file {0}: line {1}: {2}\n".format(
        os.path.basename(filename), line_number, str))
    log("ERROR: file {0}: line {1}: {2}\n".format(
        os.path.basename(filename), line_number, str))

    if globals.OPTS.debug:
        pdb.set_trace()

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
    from openram.globals import OPTS
    # 99 is a special never print level
    if lev == 99:
        return

    if (OPTS.verbose_level >= lev):
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        # classname = frm.f_globals['__name__']
        if mod.__name__ is None:
            class_name = ""
        else:
            class_name = mod.__name__
        print_raw("[{0}/{1}]: {2}".format(class_name,
                                          frm[0].f_code.co_name, str))


def archive():
    from openram.globals import OPTS
    try:
        OPENRAM_HOME = os.path.abspath(os.environ.get("OPENRAM_HOME"))
    except:
        error("$OPENRAM_HOME is not properly defined.", 1)

    import shutil
    zip_file = "{0}/{1}_{2}".format(OPENRAM_HOME, "fail_", os.getpid())
    info(0, "Archiving failed files to {}.zip".format(zip_file))
    shutil.make_archive(zip_file, 'zip', OPTS.openram_temp)


def bp():
    """
    An empty function so you can set soft breakpoints in pdb.
    Usage:
    1) Add a breakpoint anywhere in your code with "import debug; debug.bp()".
    2) Run "python3 -m pdb sram_compiler.py config.py" or "python3 -m pdb 05_bitcell_array.test" (for example)
    3) When pdb starts, run "break debug.bp" to set a SOFT breakpoint. (Or you can add this to your ~/.pdbrc)
    4) Then run "cont" to continue.
    5) You can now set additional breakpoints or display commands
    and whenever you encounter the debug.bp() they won't be "reset".
    """
    pass
