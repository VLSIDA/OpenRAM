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

# Current version of OpenRAM.
VERSION = "1.01"

USAGE = "Usage: openram.py [options] <config file>\nUse -h for help.\n"

# Anonymous object that will be the options
OPTS = options.options()

# check that we are not using version 3 and at least 2.7
major_python_version = sys.version_info.major
minor_python_version = sys.version_info.minor
if not (major_python_version == 2 and minor_python_version >= 7):
    debug.error("Python 2.7 is required.",-1)

def is_exe(fpath):
    return os.path.exists(fpath) and os.access(fpath, os.X_OK)

# parse the optional arguments
# this only does the optional arguments


def parse_args():
    """Parse the arguments and initialize openram"""

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
        optparse.make_option("-q", "--quiet", action="store_false", dest="print_banner",
                             help="Don\'t display banner"),
        optparse.make_option("-v", "--verbose", action="count", dest="debug_level",
                             help="Increase the verbosity level"),
        optparse.make_option("-t", "--tech", dest="tech_name",
                             help="Technology name"),
        optparse.make_option("-s", "--spiceversion", dest="spice_version",
                             help="Spice simulator name"),
        optparse.make_option("-r", "--remove_netlist_trimming", action="store_false", dest="trim_netlist",
                             help="Disable removal of noncritical memory cells during characterization"),
        optparse.make_option("-a", "--analytical", action="store_true", dest="analytical_delay",
                             help="Use analytical models to calculate delays (default)"),
        optparse.make_option("-c", "--characterize", action="store_false", dest="analytical_delay",
                             help="Perform characterization to calculate delays (default is analytical models)")
    }
# -h --help is implicit.

    parser = optparse.OptionParser(option_list=option_list,
                                   description="Compile and/or characterize an SRAM.",
                                   usage=USAGE,
                                   version="sramc v" + VERSION)

    (options, args) = parser.parse_args(values=OPTS)

    # If we don't specify a tech, assume freepdk45.
    # This may be overridden when we read a config file though...
    if OPTS.tech_name == "":
        OPTS.tech_name = "freepdk45"
    

    return (options, args)


def get_opts():
    return(OPTS)

def print_banner():
    """ Conditionally print the banner to stdout """
    global OPTS
    if not OPTS.print_banner:
        return

    print("|==============================================================================|")
    name = "OpenRAM Compiler v"+VERSION
    print("|=========" + name.center(60) + "=========|")
    print("|=========" + " ".center(60) + "=========|")
    print("|=========" + "VLSI Design and Automation Lab".center(60) + "=========|")
    print("|=========" + "University of California Santa Cruz CE Department".center(60) + "=========|")
    print("|=========" + " ".center(60) + "=========|")
    print("|=========" + "VLSI Computer Architecture Research Group".center(60) + "=========|")
    print("|=========" + "Oklahoma State University ECE Department".center(60) + "=========|")
    print("|=========" + " ".center(60) + "=========|")
    print("|=========" + OPTS.openram_temp.center(60) + "=========|")
    print("|==============================================================================|")


def init_openram(config_file):
    """Initialize the technology, paths, simulators, etc."""

    debug.info(1,"Initializing OpenRAM...")

    setup_paths()
    
    read_config(config_file)

    import_tech()

    set_spice()

    set_calibre()


def read_config(config_file):
    global OPTS
    
    OPTS.config_file = config_file
    OPTS.config_file = re.sub(r'\.py$', "", OPTS.config_file)

    # dynamically import the configuration file of which modules to use
    debug.info(1, "Configuration file is " + OPTS.config_file + ".py")
    try:
        OPTS.config = importlib.import_module(OPTS.config_file)
    except:
        debug.error("Unable to read configuration file: {0}".format(OPTS.config_file+".py. Did you specify the technology?"),2)

    # This path must be setup after the config file.
    try:
        # If path not set on command line, try config file.
        if OPTS.output_path=="":
            OPTS.output_path=OPTS.config.output_path
    except:
        # Default to current directory.
        OPTS.output_path="."
    if not OPTS.output_path.endswith('/'):
        OPTS.output_path += "/"
    debug.info(1, "Output saved in " + OPTS.output_path)

    # Don't delete the output dir, it may have other files!
    # make the directory if it doesn't exist
    try:
        os.makedirs(OPTS.output_path, 0o750)
    except OSError as e:
        if e.errno == 17:  # errno.EEXIST
            os.chmod(OPTS.output_path, 0o750)
    except:
        debug.error("Unable to make output directory.",-1)
    
        

def set_calibre():
    debug.info(2,"Finding calibre...")
    global OPTS

    # check if calibre is installed, if so, we should be running LVS/DRC on
    # everything.
    if not OPTS.check_lvsdrc:
        # over-ride the check LVS/DRC option
        debug.info(0,"Over-riding LVS/DRC. Not performing LVS/DRC.")
    else:
        # see if calibre is in the path (extend to other tools later)
        for path in os.environ["PATH"].split(os.pathsep):
            OPTS.calibre_exe = os.path.join(path, "calibre")
            # if it is found, do inline LVS/DRC
            if is_exe(OPTS.calibre_exe):
                OPTS.check_lvsdrc = True
                debug.info(1, "Using calibre: " + OPTS.calibre_exe)
                break
        else:
            # otherwise, give warning and procede
            debug.warning("Calibre not found. Not performing LVS/DRC.")
            OPTS.check_lvsdrc = False

def end_openram():
    """ Clean up openram for a proper exit """
    cleanup_paths()

    # Reset the static duplicate name checker for unit tests.
    # This is needed for running unit tests.
    import design
    design.design.name_map=[]
    
    
def cleanup_paths():
    # we should clean up this temp directory after execution...
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
    
    debug.check(os.path.isdir(OPENRAM_HOME+"/gdsMill"),
                "$OPENRAM_HOME/gdsMill does not exist: {0}".format(OPENRAM_HOME+"/gdsMill"))
    sys.path.append("{0}/gdsMill".format(OPENRAM_HOME)) 
    debug.check(os.path.isdir(OPENRAM_HOME+"/tests"),
                "$OPENRAM_HOME/tests does not exist: {0}".format(OPENRAM_HOME+"/tests"))
    sys.path.append("{0}/tests".format(OPENRAM_HOME))
    debug.check(os.path.isdir(OPENRAM_HOME+"/characterizer"),
                "$OPENRAM_HOME/characterizer does not exist: {0}".format(OPENRAM_HOME+"/characterizer"))
    sys.path.append("{0}/characterizer".format(OPENRAM_HOME))
    debug.check(os.path.isdir(OPENRAM_HOME+"/router"),
                "$OPENRAM_HOME/router does not exist: {0}".format(OPENRAM_HOME+"/router"))
    sys.path.append("{0}/router".format(OPENRAM_HOME))

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


    

def find_spice(check_exe):
    # Check if the preferred spice option exists in the path
    for path in os.environ["PATH"].split(os.pathsep):
        spice_exe = os.path.join(path, check_exe)
        # if it is found, then break and use first version
        if is_exe(spice_exe):
            OPTS.spice_exe = spice_exe
            return True
    return False

def set_spice():
    debug.info(2,"Finding spice...")
    global OPTS

    if OPTS.analytical_delay:
        debug.info(1,"Using analytical delay models (no characterization)")
        return
    else:
        spice_preferences = ["xa", "hspice", "ngspice", "ngspice.exe"]
        if OPTS.spice_version != "":
            if not find_spice(OPTS.spice_version):
                debug.error("{0} not found. Unable to perform characterization.".format(OPTS.spice_version),1)
        else:
            for spice_name in spice_preferences:
                if find_spice(spice_name):
                    OPTS.spice_version=spice_name
                    debug.info(1, "Using spice: " + OPTS.spice_exe)
                    break
                else:
                    debug.info(1, "Could not find {}, trying next spice simulator. ".format(spice_name))

    # set the input dir for spice files if using ngspice 
    if OPTS.spice_version == "ngspice":
        os.environ["NGSPICE_INPUT_DIR"] = "{0}".format(OPTS.openram_temp)

    if OPTS.spice_exe == "":
        debug.error("No recognizable spice version found. Unable to perform characterization.",1)


        
# imports correct technology directories for testing
def import_tech():
    global OPTS

    debug.info(2,"Importing technology: " + OPTS.tech_name)

    # Set the tech to the config file we read in instead of the command line value.
    OPTS.tech_name = OPTS.config.tech_name
    
    
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

