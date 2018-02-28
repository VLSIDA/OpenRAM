"""
This is called globals.py, but it actually parses all the arguments and performs
the global OpenRAM setup as well.
"""
import os
import debug
import shutil
import optparse
import options
import sys
import re
import importlib

USAGE = "Usage: openram.py [options] <config file>\nUse -h for help.\n"

# Anonymous object that will be the options
OPTS = options.options()

def parse_args():
    """ Parse the optional arguments for OpenRAM """

    global OPTS

    option_list = {
        optparse.make_option("-b", "--backannotated", action="store_true", dest="run_pex",
                             help="Back annotate simulation"),
        optparse.make_option("-o", "--output", dest="output_name",
                             help="Base output file name(s) prefix", metavar="FILE"),
        optparse.make_option("-p", "--outpath", dest="output_path",
                             help="Output file(s) location"),
        optparse.make_option("-n", "--nocheck", action="store_false",
                             help="Disable inline LVS/DRC checks", dest="check_lvsdrc"),
        optparse.make_option("-v", "--verbose", action="count", dest="debug_level",
                             help="Increase the verbosity level"),
        optparse.make_option("-t", "--tech", dest="tech_name",
                             help="Technology name"),
        optparse.make_option("-s", "--spice", dest="spice_name",
                             help="Spice simulator executable name"),
        optparse.make_option("-r", "--remove_netlist_trimming", action="store_false", dest="trim_netlist",
                             help="Disable removal of noncritical memory cells during characterization"),
        optparse.make_option("-c", "--characterize", action="store_false", dest="analytical_delay",
                             help="Perform characterization to calculate delays (default is analytical models)"),
        optparse.make_option("-d", "--dontpurge", action="store_false", dest="purge_temp",
                             help="Don't purge the contents of the temp directory after a successful run")
        # -h --help is implicit.
    }

    parser = optparse.OptionParser(option_list=option_list,
                                   description="Compile and/or characterize an SRAM.",
                                   usage=USAGE,
                                   version="OpenRAM")

    (options, args) = parser.parse_args(values=OPTS)
    # If we don't specify a tech, assume freepdk45.
    # This may be overridden when we read a config file though...
    if OPTS.tech_name == "":
        OPTS.tech_name = "freepdk45"
    # Alias SCMOS to AMI 0.5um
    if OPTS.tech_name == "scmos":
        OPTS.tech_name = "scn3me_subm"

    return (options, args)

def print_banner():
    """ Conditionally print the banner to stdout """
    global OPTS
    if OPTS.is_unit_test:
        return

    print("|==============================================================================|")
    name = "OpenRAM Compiler"
    print("|=========" + name.center(60) + "=========|")
    print("|=========" + " ".center(60) + "=========|")
    print("|=========" + "VLSI Design and Automation Lab".center(60) + "=========|")
    print("|=========" + "University of California Santa Cruz CE Department".center(60) + "=========|")
    print("|=========" + " ".center(60) + "=========|")
    print("|=========" + "VLSI Computer Architecture Research Group".center(60) + "=========|")
    print("|=========" + "Oklahoma State University ECE Department".center(60) + "=========|")
    print("|=========" + " ".center(60) + "=========|")
    user_info = "Usage help: openram-user-group@ucsc.edu"
    print("|=========" + user_info.center(60) + "=========|")
    dev_info = "Development help: openram-dev-group@ucsc.edu"
    print("|=========" + dev_info.center(60) + "=========|")
    temp_info = "Temp dir: {}".format(OPTS.openram_temp)
    print("|=========" + temp_info.center(60) + "=========|")
    print("|==============================================================================|")


def check_versions():
    """ Run some checks of required software versions. """

    # check that we are not using version 3 and at least 2.7
    major_python_version = sys.version_info.major
    minor_python_version = sys.version_info.minor
    if not (major_python_version == 2 and minor_python_version >= 7):
        debug.error("Python 2.7 is required.",-1)

    # FIXME: Check versions of other tools here??
    # or, this could be done in each module (e.g. verify, characterizer, etc.)

def init_openram(config_file, is_unit_test=True):
    """Initialize the technology, paths, simulators, etc."""
    check_versions()

    debug.info(1,"Initializing OpenRAM...")

    setup_paths()
    
    read_config(config_file, is_unit_test)

    import_tech()



def get_tool(tool_type, preferences):
    """
    Find which tool we have from a list of preferences and return the
    one selected and its full path.
    """
    debug.info(2,"Finding {} tool...".format(tool_type))

    for name in preferences:
        exe_name = find_exe(name)
        if exe_name != None:
            debug.info(1, "Using {0}: {1}".format(tool_type,exe_name))
            return(name,exe_name)
        else:
            debug.info(1, "Could not find {0}, trying next {1} tool.".format(name,tool_type))
    else:
        return(None,"")

    

def read_config(config_file, is_unit_test=True):
    """ 
    Read the configuration file that defines a few parameters. The
    config file is just a Python file that defines some config
    options. 
    """
    global OPTS
    
    # Create a full path relative to current dir unless it is already an abs path
    if not os.path.isabs(config_file):
        config_file = os.getcwd() + "/" +  config_file
    # Make it a python file if the base name was only given
    config_file = re.sub(r'\.py$', "", config_file)
    # Expand the user if it is used
    config_file = os.path.expanduser(config_file)
    # Add the path to the system path so we can import things in the other directory
    dir_name = os.path.dirname(config_file)
    file_name = os.path.basename(config_file)
    # Prepend the path to avoid if we are using the example config
    sys.path.insert(0,dir_name)
    # Import the configuration file of which modules to use
    debug.info(1, "Configuration file is " + config_file + ".py")
    try:
        config = importlib.import_module(file_name) 
    except:
        debug.error("Unable to read configuration file: {0}".format(config_file),2)

    for k,v in config.__dict__.items():
        # The command line will over-ride the config file
        # except in the case of the tech name! This is because the tech name
        # is sometimes used to specify the config file itself (e.g. unit tests)
        if not k in OPTS.__dict__ or k=="tech_name":
            OPTS.__dict__[k]=v
    
    if not OPTS.output_path.endswith('/'):
        OPTS.output_path += "/"
    if not OPTS.output_path.startswith('/'):
        OPTS.output_path = os.getcwd() + "/" + OPTS.output_path
    debug.info(1, "Output saved in " + OPTS.output_path)

    OPTS.is_unit_test=is_unit_test

    # If config didn't set output name, make a reasonable default.
    if (OPTS.output_name == ""):
        OPTS.output_name = "sram_{0}rw_{1}b_{2}w_{3}bank_{4}".format(OPTS.rw_ports,
                                                                     OPTS.word_size,
                                                                     OPTS.num_words,
                                                                     OPTS.num_banks,
                                                                     OPTS.tech_name)
        
    # Don't delete the output dir, it may have other files!
    # make the directory if it doesn't exist
    try:
        os.makedirs(OPTS.output_path, 0o750)
    except OSError as e:
        if e.errno == 17:  # errno.EEXIST
            os.chmod(OPTS.output_path, 0o750)
    except:
        debug.error("Unable to make output directory.",-1)
    
        
        
def end_openram():
    """ Clean up openram for a proper exit """
    cleanup_paths()
    

    
    
def cleanup_paths():
    """
    We should clean up the temp directory after execution.
    """
    if not OPTS.purge_temp:
        debug.info(0,"Preserving temp directory: {}".format(OPTS.openram_temp))
        return
    if os.path.exists(OPTS.openram_temp):
        shutil.rmtree(OPTS.openram_temp, ignore_errors=True)
            
def setup_paths():
    """ Set up the non-tech related paths. """
    debug.info(2,"Setting up paths...")

    global OPTS

    try:
        OPENRAM_HOME = os.path.abspath(os.environ.get("OPENRAM_HOME"))
    except:
        debug.error("$OPENRAM_HOME is not properly defined.",1)
    debug.check(os.path.isdir(OPENRAM_HOME),"$OPENRAM_HOME does not exist: {0}".format(OPENRAM_HOME))

    # Add all of the subdirs to the python path
    # These subdirs are modules and don't need to be added: characterizer, verify
    for subdir in ["gdsMill", "tests", "router", "modules", "base", "pgates"]:
        full_path = "{0}/{1}".format(OPENRAM_HOME,subdir)
        debug.check(os.path.isdir(full_path),
                    "$OPENRAM_HOME/{0} does not exist: {1}".format(subdir,full_path))
        sys.path.append("{0}".format(full_path)) 

    if not OPTS.openram_temp.endswith('/'):
        OPTS.openram_temp += "/"
    debug.info(1, "Temporary files saved in " + OPTS.openram_temp)

    cleanup_paths()

    # make the directory if it doesn't exist
    try:
        os.makedirs(OPTS.openram_temp, 0o750)
    except OSError as e:
        if e.errno == 17:  # errno.EEXIST
            os.chmod(OPTS.openram_temp, 0o750)


def is_exe(fpath):
    """ Return true if the given is an executable file that exists. """
    return os.path.exists(fpath) and os.access(fpath, os.X_OK)

def find_exe(check_exe):
    """ Check if the binary exists in any path dir and return the full path. """
    # Check if the preferred spice option exists in the path
    for path in os.environ["PATH"].split(os.pathsep):
        exe = os.path.join(path, check_exe)
        # if it is found, then break and use first version
        if is_exe(exe):
            return exe
    return None
        
# imports correct technology directories for testing
def import_tech():
    global OPTS

    debug.info(2,"Importing technology: " + OPTS.tech_name)

    # Set the tech to the config file we read in instead of the command line value.
    OPTS.tech_name = OPTS.tech_name
        
    # environment variable should point to the technology dir
    try:
        OPENRAM_TECH = os.path.abspath(os.environ.get("OPENRAM_TECH"))
    except:
        debug.error("$OPENRAM_TECH is not properly defined.",1)
    debug.check(os.path.isdir(OPENRAM_TECH),"$OPENRAM_TECH does not exist: {0}".format(OPENRAM_TECH))
    
    OPTS.openram_tech = OPENRAM_TECH + "/" + OPTS.tech_name
    if not OPTS.openram_tech.endswith('/'):
        OPTS.openram_tech += "/"
    debug.info(1, "Technology path is " + OPTS.openram_tech)

    try:
        filename = "setup_openram_{0}".format(OPTS.tech_name)
        # we assume that the setup scripts (and tech dirs) are located at the
        # same level as the compielr itself, probably not a good idea though.
        path = "{0}/setup_scripts".format(os.environ.get("OPENRAM_TECH"))
        debug.check(os.path.isdir(path),"OPENRAM_TECH does not exist: {0}".format(path))    
        sys.path.append(os.path.abspath(path))
        __import__(filename)
    except ImportError:
        debug.error("Nonexistent technology_setup_file: {0}.py".format(filename))
        sys.exit(1)

    import tech
    # Set some default options now based on the technology...
    if (OPTS.process_corners == ""):
        OPTS.process_corners = tech.spice["fet_models"].keys()
    if (OPTS.supply_voltages == ""):
        OPTS.supply_voltages = tech.spice["supply_voltages"]
    if (OPTS.temperatures == ""):
        OPTS.temperatures = tech.spice["temperatures"]


def print_time(name, now_time, last_time=None):
    """ Print a statement about the time delta. """
    if last_time:
        time = round((now_time-last_time).total_seconds(),1)
    else:
        time = now_time
    print("** {0}: {1} seconds".format(name,time))


def report_status():
    """ Check for valid arguments and report the info about the SRAM being generated """
    # Check if all arguments are integers for bits, size, banks
    if type(OPTS.word_size)!=int:
        debug.error("{0} is not an integer in config file.".format(OPTS.word_size))
    if type(OPTS.num_words)!=int:
        debug.error("{0} is not an integer in config file.".format(OPTS.sram_size))
    if type(OPTS.num_banks)!=int:
        debug.error("{0} is not an integer in config file.".format(OPTS.num_banks))

    if not OPTS.tech_name:
        debug.error("Tech name must be specified in config file.")

    print("Technology: {0}".format(OPTS.tech_name))
    print("Word size: {0}\nWords: {1}\nBanks: {2}".format(OPTS.word_size,
                                                          OPTS.num_words,
                                                          OPTS.num_banks))
    if not OPTS.check_lvsdrc:
        print("DRC/LVS/PEX checking is disabled.")
    
