#!/bin/csh
# This is a csh utility script to set the paths to the current
# directory of OpenRAM. It must be sourced in the local directory
# like this:
# source setpaths.csh

setenv OPENRAM_HOME "`pwd`/compiler"
setenv OPENRAM_TECH "`pwd`/technology"
