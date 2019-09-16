;; NCSU CDK v. 1.6.0.beta
;; Last Modified: 2007-07-12

The NCSU CDK is Copyright (C) NC State University, 1998, 1999, 2004, 
2006, 2007. Users are free to use or modify the NCSU CDK as appropriate as long 
as this notice appears in the modified package.   The NCSU CDK is
provided with NO WARRANTY. 

As of version 1.5.1, all documentation for the NCSU CDK is provided
by the NCSU EDA Wiki which can be found at:

                    http://www.eda.ncsu.edu/

This beta release of the kit is to be used in migrating to Cadence Virtuoso 6.1
for OpenAccess.  Details of the conversion of the CDK from the CDB version can
be found in the file cdb2oa/OA_Conversion.txt.

This kit is not yet fully supported.  Please post problems and solutions at
http://www.chiptalk.org -> Forums -> NCSU CDK -> NCSU CDK 1.6.0.beta for Virtuoso 6.1

Modified 2018 by MRG to contain SCN4ME Via3/Metal4 layers.

mosis.lyp is converted automatically from the .tf using:
https://github.com/klayoutmatthias/tf_import
Command line:
klayout -z -rd tf_file=FreePDK45.tf -rd lyp_file=FreePDK45.ly
You can then view layouts with:
klayout file.gds -l mosis.lyp

glade_scn4m_subm.py is a script for Glade:
https://peardrop.co.uk/
to load the .tf using:
glade -script ~/openram/technology/scn3me_subm/tf/glade_scn3me_subm.py -gds file.gds
