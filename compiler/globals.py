# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
This is called globals.py, but it actually parses all the arguments
and performs the global OpenRAM setup as well.
"""
import sys
import os
import re
import shutil
import optparse
import copy
import importlib
import getpass
import subprocess
from openram import debug
from openram import options


from openram import OPENRAM_HOME
VERSION = open(OPENRAM_HOME + "/../VERSION").read().rstrip()
NAME = "OpenRAM v{}".format(VERSION)
USAGE = "sram_compiler.py [options] <config file>\nUse -h for help.\n"

OPTS = options.options()


def parse_args():
    """ Parse the optional arguments for OpenRAM. """

    global OPTS

    option_list = {
        optparse.make_option("-b", "--backannotated",
                             action="store_true",
                             dest="use_pex",
                             help="Back annotate simulation"),
        optparse.make_option("-o", "--output",
                             dest="output_name",
                             help="Base output file name(s) prefix",
                             metavar="FILE"),
        optparse.make_option("-p", "--outpath",
                             dest="output_path",
                             help="Output file(s) location"),
        optparse.make_option("-i", "--inlinecheck",
                             action="store_true",
                             help="Enable inline LVS/DRC checks",
                             dest="inline_lvsdrc"),
        optparse.make_option("-n", "--nocheck",
                             action="store_false",
                             help="Disable all LVS/DRC checks",
                             dest="check_lvsdrc"),
        optparse.make_option("-j", "--threads",
                             action="store",
                             type="int",
                             help="Specify the number of threads (default: 1)",
                             dest="num_threads"),
        optparse.make_option("-m", "--sim_threads",
                             action="store",
                             type="int",
                             help="Specify the number of spice simulation threads (default: 3)",
                             dest="num_sim_threads"),
        optparse.make_option("-v", "--verbose",
                             action="count",
                             dest="verbose_level",
                             help="Increase the verbosity level"),
        optparse.make_option("-t", "--tech",
                             dest="tech_name",
                             help="Technology name"),
        optparse.make_option("-s", "--spice",
                             dest="spice_name",
                             help="Spice simulator executable name"),
        optparse.make_option("-r", "--remove_netlist_trimming",
                             action="store_false",
                             dest="trim_netlist",
                             help="Disable removal of noncritical memory cells during characterization"),
        optparse.make_option("-c", "--characterize",
                             action="store_false",
                             dest="analytical_delay",
                             help="Perform characterization to calculate delays (default is analytical models)"),
        optparse.make_option("-k", "--keeptemp",
                             action="store_true",
                             dest="keep_temp",
                             help="Keep the contents of the temp directory after a successful run"),
        optparse.make_option("-d", "--debug",
                             action="store_true",
                             dest="debug",
                             help="Run in debug mode to drop to pdb on failure")
        # -h --help is implicit.
    }

    parser = optparse.OptionParser(option_list=option_list,
                                   description=NAME,
                                   usage=USAGE,
                                   version=VERSION)

    (options, args) = parser.parse_args(values=OPTS)
    # If we don't specify a tech, assume scmos.
    # This may be overridden when we read a config file though...
    if OPTS.tech_name == "":
        OPTS.tech_name = "scmos"
    # Alias SCMOS to 180nm
    if OPTS.tech_name == "scmos":
        OPTS.tech_name = "scn4m_subm"
    # Alias s8 to sky130
    if OPTS.tech_name == "s8":
        OPTS.tech_name = "sky130"

    return (options, args)


def print_banner():
    """ Conditionally print the banner to stdout. """
    global OPTS
    if OPTS.is_unit_test:
        return

    debug.print_raw("|==============================================================================|")
    debug.print_raw("|=========" + NAME.center(60) + "=========|")
    debug.print_raw("|=========" + " ".center(60) + "=========|")
    debug.print_raw("|=========" + "VLSI Design and Automation Lab".center(60) + "=========|")
    debug.print_raw("|=========" + "Computer Science and Engineering Department".center(60) + "=========|")
    debug.print_raw("|=========" + "University of California Santa Cruz".center(60) + "=========|")
    debug.print_raw("|=========" + " ".center(60) + "=========|")
    user_info = "Usage help: openram-user-group@ucsc.edu"
    debug.print_raw("|=========" + user_info.center(60) + "=========|")
    dev_info = "Development help: openram-dev-group@ucsc.edu"
    debug.print_raw("|=========" + dev_info.center(60) + "=========|")
    debug.print_raw("|=========" + "See LICENSE for license info".center(60) + "=========|")
    debug.print_raw("|==============================================================================|")


def check_versions():
    """ Run some checks of required software versions. """

    # Now require python >=3.5
    major_python_version = sys.version_info.major
    minor_python_version = sys.version_info.minor
    major_required = 3
    minor_required = 5
    if not (major_python_version == major_required and minor_python_version >= minor_required):
        debug.error("Python {0}.{1} or greater is required.".format(major_required, minor_required), -1)

    # Verify any version of git is isntalled before proceeding
    try:
        subprocess.check_output(["git", "--version"])
    except:
        debug.error("Git is required. Please install git.", -1)

    # FIXME: Check versions of other tools here??
    # or, this could be done in each module (e.g. verify, characterizer, etc.)
    global OPTS

    def cmd_exists(cmd):
        return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

    if cmd_exists("coverage"):
        OPTS.coverage_exe = "coverage run -p "
    elif cmd_exists("python3-coverage"):
        OPTS.coverage_exe = "python3-coverage run -p "
    else:
        OPTS.coverage_exe = ""
        debug.warning("Failed to find coverage installation. This can be installed with pip3 install coverage")

    try:
        import coverage
        OPTS.coverage = 1
    except ModuleNotFoundError:
        OPTS.coverage = 0


def init_openram(config_file, is_unit_test=False):
    """ Initialize the technology, paths, simulators, etc. """

    check_versions()

    debug.info(1, "Initializing OpenRAM...")

    setup_paths()

    read_config(config_file, is_unit_test)

    install_conda()

    import_tech()

    set_default_corner()

    init_paths()

    from openram.sram_factory import factory
    factory.reset()

    global OPTS

    # Setup correct bitcell names
    setup_bitcell()

    # Import these to find the executables for checkpointing
    from openram import characterizer
    from openram import verify


def install_conda():
    """ Setup conda for default tools. """

    # Don't setup conda if not used
    if not OPTS.use_conda or OPTS.is_unit_test:
        return

    debug.info(1, "Creating conda setup...");

    from openram import CONDA_INSTALLER
    subprocess.call(CONDA_INSTALLER)


def setup_bitcell():
    """
    Determine the correct custom or parameterized bitcell for the design.
    """
    # If we have non-1rw ports,
    # and the user didn't over-ride the bitcell manually,
    # figure out the right bitcell to use
    if OPTS.bitcell == "pbitcell":
        OPTS.bitcell = "pbitcell"
        OPTS.dummy_bitcell = "dummy_pbitcell"
        OPTS.replica_bitcell = "replica_pbitcell"
    else:
        OPTS.num_ports = OPTS.num_rw_ports + OPTS.num_w_ports + OPTS.num_r_ports
        OPTS.bitcell = "bitcell_{}port".format(OPTS.num_ports)
        OPTS.dummy_bitcell = "dummy_" + OPTS.bitcell
        OPTS.replica_bitcell = "replica_" + OPTS.bitcell

    # See if bitcell exists
    try:
        c = importlib.import_module("openram.modules." + OPTS.bitcell)
        mod = getattr(c, OPTS.bitcell)
    except ImportError:
        # Use the pbitcell if we couldn't find a custom bitcell
        # or its custom replica  bitcell
        # Use the pbitcell (and give a warning if not in unit test mode)
        OPTS.bitcell = "pbitcell"
        OPTS.dummy_bitcell = "dummy_pbitcell"
        OPTS.replica_bitcell = "replica_pbitcell"
        if not OPTS.is_unit_test:
            msg = "Didn't find {0}rw {1}w {2}r port bitcell. ".format(OPTS.num_rw_ports, OPTS.num_w_ports, OPTS.num_r_ports)
            debug.warning("{} Using the parameterized bitcell which may have suboptimal density.".format(msg))
    debug.info(1, "Using bitcell: {}".format(OPTS.bitcell))


def get_tool(tool_type, preferences, default_name=None):
    """
    Find which tool we have from a list of preferences and return the
    one selected and its full path. If default is specified,
    find that one only and error otherwise.
    """
    debug.info(2, "Finding {} tool...".format(tool_type))

    if default_name:
        exe_name = find_exe(default_name)
        if exe_name == None:
            debug.error("{0} not found. Cannot find {1} tool.".format(default_name, tool_type)
                        + "Disable DRC/LVS with check_lvsdrc=False to ignore.",
                        2)
        else:
            debug.info(1, "Using {0}: {1}".format(tool_type, exe_name))
            return (default_name, exe_name)
    else:
        for name in preferences:
            exe_name = find_exe(name)
            if exe_name != None:
                debug.info(1, "Using {0}: {1}".format(tool_type, exe_name))
                return (name, exe_name)
            else:
                debug.info(1, "Could not find {0}, trying next {1} tool.".format(name, tool_type))
        else:
            return (None, "")


def read_config(config_file, is_unit_test=False):
    """
    Read the configuration file that defines a few parameters. The
    config file is just a Python file that defines some config
    options. This will only actually get read the first time. Subsequent
    reads will just restore the previous copy (ask mrg)
    """
    global OPTS

    # it is already not an abs path, make it one
    if not os.path.isabs(config_file):
        config_file = os.getcwd() + "/" +  config_file

    # Make it a python file if the base name was only given
    config_file = re.sub(r'\.py$', "", config_file)


    # Expand the user if it is used
    config_file = os.path.expanduser(config_file)

    OPTS.config_file = config_file + ".py"
    # Add the path to the system path
    # so we can import things in the other directory
    dir_name = os.path.dirname(config_file)
    module_name = os.path.basename(config_file)

    # Check that the module name adheres to Python's module naming conventions.
    # This will assist the user in interpreting subsequent errors in loading
    # the module. Valid Python module naming is described here:
    #   https://docs.python.org/3/reference/simple_stmts.html#the-import-statement
    if not module_name.isidentifier():
        debug.error("Configuration file name is not a valid Python module name: "
                    "{0}. It should be a valid identifier.".format(module_name))

    # Prepend the path to avoid if we are using the example config
    sys.path.insert(0, dir_name)
    # Import the configuration file of which modules to use
    debug.info(1, "Configuration file is " + config_file + ".py")
    try:
        config = importlib.import_module(module_name)
    except ImportError:
        debug.error("Unable to read configuration file: {0}".format(config_file), 2)

    OPTS.overridden = {}
    for k, v in config.__dict__.items():
        # The command line will over-ride the config file
        # except in the case of the tech name! This is because the tech name
        # is sometimes used to specify the config file itself (e.g. unit tests)
        # Note that if we re-read a config file, nothing will get read again!
        if k not in OPTS.__dict__ or k == "tech_name":
            OPTS.__dict__[k] = v
            OPTS.overridden[k] = True

    # Massage the output path to be an absolute one
    if not OPTS.output_path.endswith('/'):
        OPTS.output_path += "/"
    if not OPTS.output_path.startswith('/'):
        OPTS.output_path = os.getcwd() + "/" + OPTS.output_path
    debug.info(1, "Output saved in " + OPTS.output_path)

    # Remember if we are running unit tests to reduce output
    OPTS.is_unit_test = is_unit_test

    # If we are only generating a netlist, we can't do DRC/LVS
    if OPTS.netlist_only:
        OPTS.check_lvsdrc = False

    # If config didn't set output name, make a reasonable default.
    if (OPTS.output_name == ""):
        ports = ""
        if OPTS.num_rw_ports > 0:
            ports += "{}rw_".format(OPTS.num_rw_ports)
        if OPTS.num_w_ports > 0:
            ports += "{}w_".format(OPTS.num_w_ports)
        if OPTS.num_r_ports > 0:
            ports += "{}r_".format(OPTS.num_r_ports)
        OPTS.output_name = "sram_{0}b_{1}_{2}{3}".format(OPTS.word_size,
                                                         OPTS.num_words,
                                                         ports,
                                                         OPTS.tech_name)

    # If write size is not defined, set it equal to word size
    if OPTS.write_size is None:
        OPTS.write_size = OPTS.word_size


def end_openram():
    """ Clean up openram for a proper exit. """
    cleanup_paths()

    if OPTS.check_lvsdrc:
        from openram import verify
        verify.print_drc_stats()
        verify.print_lvs_stats()
        verify.print_pex_stats()


def purge_temp():
    """ Remove the temp directory. """
    debug.info(1, "Purging temp directory: {}".format(OPTS.openram_temp))
    #import inspect
    #s = inspect.stack()
    #print("Purge {0} in dir {1}".format(s[3].filename, OPTS.openram_temp))

    # This annoyingly means you have to re-cd into
    # the directory each debug iteration
    # shutil.rmtree(OPTS.openram_temp, ignore_errors=True)
    contents = [os.path.join(OPTS.openram_temp, i) for i in os.listdir(OPTS.openram_temp)]
    for i in contents:
        if os.path.isfile(i) or os.path.islink(i):
            os.remove(i)
        else:
            shutil.rmtree(i)


def cleanup_paths():
    """
    We should clean up the temp directory after execution.
    """
    global OPTS
    if OPTS.keep_temp:
        debug.info(0, "Preserving temp directory: {}".format(OPTS.openram_temp))
        return
    elif os.path.exists(OPTS.openram_temp):
        purge_temp()


def setup_paths():
    """ Set up the non-tech related paths. """
    debug.info(2, "Setting up paths...")

    global OPTS

    from openram import OPENRAM_HOME
    debug.info(1, "OpenRAM source code found in {}".format(OPENRAM_HOME))

    # Use a unique temp subdirectory if multithreaded
    if OPTS.num_threads > 1 or OPTS.openram_temp == "/tmp":
        # Make a unique subdir
        tempdir = "/openram_{0}_{1}_temp".format(getpass.getuser(),
                                                 os.getpid())
        # Only add the unique subdir one time
        if tempdir not in OPTS.openram_temp:
            OPTS.openram_temp += tempdir

    if not OPTS.openram_temp.endswith('/'):
        OPTS.openram_temp += "/"
    debug.info(1, "Temporary files saved in " + OPTS.openram_temp)


def is_exe(fpath):
    """ Return true if the given is an executable file that exists. """

    return os.path.exists(fpath) and os.access(fpath, os.X_OK)


def find_exe(check_exe):
    """
    Check if the binary exists in any path dir and return the full path.
    """

    # Search for conda setup if used
    if OPTS.use_conda:
        from openram import CONDA_HOME
        search_path = "{0}/bin{1}{2}".format(CONDA_HOME,
                                             os.pathsep,
                                             os.environ["PATH"])
    else:
        search_path = os.environ["PATH"]

    # Check if the preferred spice option exists in the path
    for path in search_path.split(os.pathsep):
        exe = os.path.join(path, check_exe)
        # if it is found, then break and use first version
        if is_exe(exe):
            return exe
    return None


def init_paths():
    """ Create the temp and output directory if it doesn't exist. """

    if os.path.exists(OPTS.openram_temp):
        purge_temp()
    else:
        # Make the directory if it doesn't exist
        try:
            debug.info(1, "Creating temp directory: {}".format(OPTS.openram_temp))
            os.makedirs(OPTS.openram_temp, 0o750)
        except OSError as e:
            if e.errno == 17: # errno.EEXIST
                os.chmod(OPTS.openram_temp, 0o750)
            else:
                debug.error("Unable to make temp directory: {}".format(OPTS.openram_temp), -1)
    #import inspect
    #s = inspect.stack()
    #from pprint import pprint
    #pprint(s)
    #print("Test {0} in dir {1}".format(s[2].filename, OPTS.openram_temp))


    # Don't delete the output dir, it may have other files!
    # make the directory if it doesn't exist
    try:
        os.makedirs(OPTS.output_path, 0o750)
    except OSError as e:
        if e.errno == 17: # errno.EEXIST
            os.chmod(OPTS.output_path, 0o750)
        else:
            debug.error("Unable to make output directory: {}".format(OPTS.output_path), -1)


def set_default_corner():
    """ Set the default corner. """

    from openram import tech
    # Set some default options now based on the technology...
    if (OPTS.process_corners == ""):
        if OPTS.nominal_corner_only:
            OPTS.process_corners = ["TT"]
        else:
            OPTS.process_corners = list(tech.spice["fet_models"].keys())

    if (OPTS.supply_voltages == ""):
        if OPTS.nominal_corner_only:
            OPTS.supply_voltages = [tech.spice["supply_voltages"][1]]
        else:
            OPTS.supply_voltages = tech.spice["supply_voltages"]

    if (OPTS.temperatures == ""):
        if OPTS.nominal_corner_only:
            OPTS.temperatures = [tech.spice["temperatures"][1]]
        else:
            OPTS.temperatures = tech.spice["temperatures"]

    # Load scales are fanout multiples of the DFF input cap
    if (OPTS.load_scales == ""):
        OPTS.load_scales = [0.25, 1, 4]

    # Load scales are fanout multiples of the default spice input slew
    if (OPTS.slew_scales == ""):
        OPTS.slew_scales = [0.25, 1, 8]


def import_tech():
    """ Dynamically adds the tech directory to the path and imports it. """
    global OPTS

    debug.info(2, "Importing technology: " + OPTS.tech_name)

    OPENRAM_TECH = ""

    # Check if $OPENRAM_TECH is defined
    try:
        OPENRAM_TECH = os.path.abspath(os.environ.get("OPENRAM_TECH"))
    except:
        debug.info(2,
                   "$OPENRAM_TECH environment variable is not defined. "
                   "Only the default technology modules will be considered if installed.")
    # Point to the default technology modules that are part of the openram package
    try:
        import openram
        if OPENRAM_TECH != "":
            OPENRAM_TECH += ":"
        OPENRAM_TECH += os.path.dirname(openram.__file__) + "/technology"
    except:
        if OPENRAM_TECH == "":
            debug.warning("Couldn't find a tech directory. "
                          "Install openram library or set $OPENRAM_TECH.")

    debug.info(1, "Tech directory found in {}".format(OPENRAM_TECH))

    # Add this environment variable to os.environ and openram namespace
    os.environ["OPENRAM_TECH"] = OPENRAM_TECH
    openram.OPENRAM_TECH = OPENRAM_TECH

    # Add all of the paths
    for tech_path in OPENRAM_TECH.split(":"):
        debug.check(os.path.isdir(tech_path),
                    "$OPENRAM_TECH does not exist: {}".format(tech_path))
        sys.path.append(tech_path)
        debug.info(1, "Adding technology path: {}".format(tech_path))

    # Import the tech
    try:
        tech_mod = __import__(OPTS.tech_name)
    except ImportError:
        debug.error("Nonexistent technology module: {}".format(OPTS.tech_name), -1)

    OPTS.openram_tech = os.path.dirname(tech_mod.__file__) + "/"

    # Append tech_path to openram.__path__ to import it from openram
    tech_path = OPTS.openram_tech
    openram.__path__.append(tech_path)
    try:
        from openram import tech
    except ImportError:
        debug.error("Could not load tech module.", -1)

    # Remove OPENRAM_TECH from sys.path because we should be done with those
    for tech_path in OPENRAM_TECH.split(":"):
        sys.path.remove(tech_path)

    # Add the custom modules to "tech"
    custom_mod_path = os.path.join(tech_path, "custom/")
    if os.path.exists(custom_mod_path):
        from openram import tech
        tech.__path__.append(custom_mod_path)


def print_time(name, now_time, last_time=None, indentation=2):
    """ Print a statement about the time delta. """
    global OPTS

    # Don't print during testing
    if not OPTS.is_unit_test or OPTS.verbose_level > 0:
        if last_time:
            time = str(round((now_time - last_time).total_seconds(), 1)) + " seconds"
        else:
            time = now_time.strftime('%m/%d/%Y %H:%M:%S')
        debug.print_raw("{0} {1}: {2}".format("*" * indentation, name, time))


def report_status():
    """
    Check for valid arguments and report the
    info about the SRAM being generated
    """
    global OPTS

    # Check if all arguments are integers for bits, size, banks
    if type(OPTS.word_size) != int:
        debug.error("{0} is not an integer in config file.".format(OPTS.word_size))
    if type(OPTS.num_words) != int:
        debug.error("{0} is not an integer in config file.".format(OPTS.sram_size))
    if type(OPTS.write_size) is not int and OPTS.write_size is not None:
        debug.error("{0} is not an integer in config file.".format(OPTS.write_size))

    # If a write mask is specified by the user, the mask write size should be the same as
    # the word size so that an entire word is written at once.
    if OPTS.write_size is not None and OPTS.write_size != OPTS.word_size:
        if (OPTS.word_size % OPTS.write_size != 0):
            debug.error("Write size needs to be an integer multiple of word size.")
        # If write size is more than half of the word size,
        # then it doesn't need a write mask. It would be writing
        # the whole word.
        if (OPTS.write_size < 1 or OPTS.write_size > OPTS.word_size / 2):
            debug.error("Write size needs to be between 1 bit and {0} bits.".format(int(OPTS.word_size / 2)))

    if not OPTS.tech_name:
        debug.error("Tech name must be specified in config file.")

    debug.print_raw("Technology: {0}".format(OPTS.tech_name))
    total_size = OPTS.word_size*OPTS.num_words*OPTS.num_banks
    debug.print_raw("Total size: {} bits".format(total_size))
    if total_size >= 2**14 and not OPTS.analytical_delay:
        debug.warning("Characterizing large memories ({0}) will have a large run-time.".format(total_size))
    debug.print_raw("Word size: {0}\nWords: {1}\nBanks: {2}".format(OPTS.word_size,
                                                                    OPTS.num_words,
                                                                    OPTS.num_banks))
    if (OPTS.write_size != OPTS.word_size):
        debug.print_raw("Write size: {}".format(OPTS.write_size))
    debug.print_raw("RW ports: {0}\nR-only ports: {1}\nW-only ports: {2}".format(OPTS.num_rw_ports,
                                                                                 OPTS.num_r_ports,
                                                                                 OPTS.num_w_ports))

    if OPTS.netlist_only:
        debug.print_raw("Netlist only mode (no physical design is being done, netlist_only=False to disable).")

    if not OPTS.route_supplies:
        debug.print_raw("Design supply routing skipped. Supplies will have multiple must-connect pins. (route_supplies=True to enable supply routing).")

    if not OPTS.inline_lvsdrc:
        debug.print_raw("DRC/LVS/PEX is only run on the top-level design to save run-time (inline_lvsdrc=True to do inline checking).")

    if not OPTS.check_lvsdrc:
        debug.print_raw("DRC/LVS/PEX is disabled (check_lvsdrc=True to enable).")

    if OPTS.analytical_delay:
        debug.print_raw("Characterization is disabled (using analytical delay models) (analytical_delay=False to simulate).")
    else:
        if OPTS.spice_name != "":
            debug.print_raw("Performing simulation-based characterization with {}".format(OPTS.spice_name))
        if OPTS.trim_netlist:
            debug.print_raw("Trimming netlist to speed up characterization (trim_netlist=False to disable).")
    if OPTS.nominal_corner_only:
        debug.print_raw("Only generating nominal corner timing.")
