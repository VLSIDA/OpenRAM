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
VERSION = "1.0"


USAGE = "usage: openram.py [options] <config file>\n"

# Anonymous object that will be the options
OPTS = options.options()

def is_exe(fpath):
    return os.path.exists(fpath) and os.access(fpath, os.X_OK)

# parse the optional arguments
# this only does the optional arguments


def parse_args():
    """Parse the arguments and initialize openram"""

    global OPTS

    option_list = {
        optparse.make_option("-b", "--backannotated", dest="run_pex",
                             help="back annotated simulation for characterizer"),
        optparse.make_option("-o", "--output", dest="out_name",
                             help="Base output file name.", metavar="FILE"),
        optparse.make_option("-p", "--outpath", dest="out_path",
                             help="output file location."),
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
        # TODO: Why is this -f?
        optparse.make_option("-f", "--trim_noncritical", dest="trim_noncritical",
                             help="Trim noncritical memory cells during simulation"),
        optparse.make_option("-a", "--analyticaldelay", dest="analytical_delay",
                             help="Use analytical model to calculate delay or not")
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

    print "|==============================================================================|"
    name = "OpenRAM Compiler v"+VERSION
    print "|=========" + name.center(60) + "=========|"
    print "|=========" + " ".center(60) + "=========|"
    print "|=========" + "VLSI Design and Automation Lab".center(60) + "=========|"
    print "|=========" + "University of California Santa Cruz CE Department".center(60) + "=========|"
    print "|=========" + " ".center(60) + "=========|"
    print "|=========" + "VLSI Computer Architecture Research Group".center(60) + "=========|"
    print "|=========" + "Oklahoma State University ECE Department".center(60) + "=========|"
    print "|=========" + " ".center(60) + "=========|"
    print "|=========" + OPTS.openram_temp.center(60) + "=========|"
    print "|==============================================================================|"


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


def set_calibre():
    debug.info(2,"Finding calibre...")
    global OPTS

    # check if calibre is installed, if so, we should be running LVS/DRC on
    # everything.
    if not OPTS.check_lvsdrc:
        # over-ride the check LVS/DRC option
        debug.info(0,"Over-riding LVS/DRC. Not performing inline LVS/DRC.")
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
            debug.warning("Calibre not found. Not performing inline LVS/DRC.")
            OPTS.check_lvsdrc = False

def end_openram():
    """ Clean up openram for a proper exit """
    cleanup_paths()
    
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
        os.makedirs(OPTS.openram_temp, 0750)
    except OSError as e:
        if e.errno == 17:  # errno.EEXIST
            os.chmod(OPTS.openram_temp, 0750)

    # Don't delete the output dir, it may have other files!
    # make the directory if it doesn't exist
    try:
        os.makedirs(OPTS.out_path, 0750)
    except OSError as e:
        if e.errno == 17:  # errno.EEXIST
            os.chmod(OPTS.out_path, 0750)
    
    if OPTS.out_path=="":
        OPTS.out_path="."
    if not OPTS.out_path.endswith('/'):
        OPTS.out_path += "/"
    debug.info(1, "Output saved in " + OPTS.out_path)


def set_spice():
    debug.info(2,"Finding spice...")
    global OPTS

    OPTS.spice_exe = ""
    
    # Check if the preferred spice option exists in the path
    for path in os.environ["PATH"].split(os.pathsep):
        spice_exe = os.path.join(path, OPTS.spice_version)
        # if it is found, then break and use first version
        if is_exe(spice_exe):
            debug.info(1, "Using spice: " + spice_exe)
            OPTS.spice_exe = spice_exe
            break
        
    if not OPTS.force_spice and OPTS.spice_exe == "":
        # if we didn't find the preferred version, try the other version and warn
        prev_version=OPTS.spice_version
        if OPTS.spice_version == "hspice":
            OPTS.spice_version = "ngspice"
        else:
            OPTS.spice_version = "hspice"
        debug.warning("Unable to find {0} so trying {1}".format(prev_version,OPTS.spice_version))

        for path in os.environ["PATH"].split(os.pathsep):
            spice_exe = os.path.join(path, OPTS.spice_version)
            # if it is found, then break and use first version
            if is_exe(spice_exe):
                found_spice = True
                debug.info(1, "Using spice: " + spice_exe)
                OPTS.spice_exe = spice_exe
                break

    # set the input dir for spice files if using ngspice 
    if OPTS.spice_version == "ngspice":
        os.environ["NGSPICE_INPUT_DIR"] = "{0}".format(OPTS.openram_temp)

    if OPTS.spice_exe == "":
        # otherwise, give warning and procede
        if OPTS.force_spice:
            debug.error("{0} not found. Unable to perform characterization.".format(OPTS.spice_version),1)
        else:
            debug.error("Neither hspice/ngspice not found. Unable to perform characterization.",1)
                        

        
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

