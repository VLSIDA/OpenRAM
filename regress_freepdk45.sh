#!/bin/bash
# This is a bash utility script to set the paths to the current
# directory of OpenRAM. It must be sourced in the local directory
# like this:
# source setpaths.sh

export OPENRAM_HOME="`pwd`/compiler"
export OPENRAM_TECH="`pwd`/technology"
python3 $OPENRAM_HOME/tests/regress.py -t freepdk45
