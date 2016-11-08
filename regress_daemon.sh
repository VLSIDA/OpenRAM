#Check out a copy of the repository:
#cd ~
#git clone gitosis@mada0.cse.ucsc.edu:openram.git unit_test
#crontab -l views the crontab
#crontab -e edits the crontab
#Add a command like this to the crontab to call the regression script 
# m h dom mon dow user    command
#0 0,12 * * * /mada/users/wubin6666/unit_test/trunk/regress_daemon.sh
!/bin/bash
source /mada/software/setup.sh
export OPENRAM_HOME="/soe/mrg/unit_test/trunk/compiler"
export OPENRAM_TECH="/soe/mrg/unit_test/trunk/technology"
python ${HOME}/unit_test/trunk/regress_daemon.py -t freepdk45
python ${HOME}/unit_test/trunk/regress_daemon.py -t scn3me_subm
