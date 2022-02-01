
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

export SWROOT=/software

# Klayout
export PATH=$PATH:/usr/local/klayout

# Xyce
export XYCE_HOME=$SWROOT/Xyce/Parallel
export XYCE_PATH=$XYCE_HOME/bin
export PATH=$PATH:$XYCE_PATH
export XYCE_LIB=$XYCE_HOME/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$XYCE_LIB
export XYCE_NO_TRACKING="anything at all"

# PDKs
export FREEPDK45=/home/PDKs/FreePDK45
# Set to the PDK you want to use
export PDK_DIR=$FREEPDK45
