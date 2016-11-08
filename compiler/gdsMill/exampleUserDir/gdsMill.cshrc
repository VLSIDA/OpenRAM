#-----------------------------
#Need a path to a recent python distribution
#If a recent one is already installed locally, just comment this out
#setenv PATH /some/path/to/python/Python2.6.1/bin\:$PATH

#-----------------------------
#To do automatic stream IN/OUT, we need a path to PIPO (the cadence stream executable)
#PIPO is usually inside the dfII/bin directory of your cadence installation
#if not used, this can be commented out
#setenv PATH /some/path/to/cadence/ic-5.141_usr5/tools/dfII/bin\:/some/path/to/cadence/ic-5.141_usr5/tools/bin\:$PATH

#-----------------------------
#This is the search path where Python will find GDSMill
if ( ! ($?PYTHONPATH) ) then
    setenv PYTHONPATH /design/common/GDSMill
else
    setenv PYTHONPATH /design/common/GDSMill\:$PYTHONPATH
endif

#-----------------------------
#If you are going to use GDS Mill in conjunction with a particular Cadence work directory, it often makes sense to source the shell script
#required within that directory (for example, a shell script in my work directory sets up permissions to access the design kit files)
source ~/design/600nmAmi/600nmAmi.cshrc

