#-----------------------------
#To do automatic stream IN/OUT, we need a path to PIPO (the cadence stream executable)
#PIPO is usually inside the dfII/bin directory of your cadence installation
#if not used, this can be commented out
#setenv PATH /some/path/to/cadence/ic-5.141_usr5/tools/dfII/bin\:/some/path/to/cadence/ic-5.141_usr5/tools/bin\:$PATH

#-----------------------------
#This is the search path where Python will find GDSMill

export PYTHONPATH=`pwd`/:$PYTHONPATH
