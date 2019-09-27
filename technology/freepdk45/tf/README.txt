These technology files are from the FreePDK45nm design kit.

FreePDK 45nm verion 1.4 (2011-04-07)
(Subversion Repository revision 173)

Copyright 2007 - W. Rhett Davis, Paul Franzon, Michael Bucher, 
                 and Sunil Basavarajaiah, North Carolina State University
Copyright 2008 - W. Rhett Davis, Michael Bucher, and Sunil Basavarajaiah,
                 North Carolina State University (ncsu_basekit subtree)
                 James Stine, and Ivan Castellanos,
                 and Oklahoma State University (osu_soc subtree)
Copyright 2011 - W. Rhett Davis, and Harun Demircioglu,
                 North Carolina State University

SVRF Technology in this kit is licensed under the the agreement found
in the file SVRF_EULA_06Feb09.txt in this directory.  All other files
are licensed under the Apache License, Version 2.0 (the "License");
you may not use these files except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

***** Welcome to the FreePDK 45nm Free, Open-Source Process Design Kit *****

This initiative is brought to you by the Semiconductor Research
Corporation (SRC), the National Science Foundation (NSF), Silicon 
Integration Initiative (Si2), Mentor Graphics, and Synopsys.

This version of the kit was created by Rhett Davis, Paul Franzon,
Michael Bucher, Sunil Basavarajaiah, and Harun Demircioglu 
of North Carolina State University, and James Stine and Ivan Castellanos 
of Oklahoma State University.

Contributions and modifications to this kit are welcomed and encouraged.

***** Contents *****

ncsu_basekit/     Base kit for custom design
osu_soc/          Standard-cell kit for synthesis, place, & route

FreePDK45.lyp is converted automatically from the .tf using:
https://github.com/klayoutmatthias/tf_import
Command line:
klayout -z -rd tf_file=FreePDK45.tf -rd lyp_file=FreePDK45.lyp
You can then view layouts with:
klayout file.gds -l mosis.lyp

glade_freepdk45.py is a script for Glade:
https://peardrop.co.uk/
to load the .tf using:
glade -script ~/openram/technology/freepdk45/tf/glade_freepdk45.py -gds file.gds
