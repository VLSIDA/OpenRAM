"""
This type of setup script should be placed in the setup_scripts directory in
the trunk
"""

import os

TECHNOLOGY = "ihp_sg13g2"

os.environ["MGC_TMPDIR"] = "/tmp"

###########################
# OpenRAM Paths

if "PDK_ROOT" in os.environ:
    open_pdks = os.path.join(os.environ["PDK_ROOT"], "ihp-sg13g2", "libs.tech")
else:
    raise SystemError("Unable to find the IHP SG13G2 PDK. Set PDK_ROOT.")

# The ngspice models work with Xyce too now
spice_model_dir = os.path.join(open_pdks, "ngspice", "models")
ihp_lib_ngspice = os.path.join(open_pdks, "ngspice", ".spiceinit")
if not os.path.exists(ihp_lib_ngspice):
    raise SystemError("Did not find {} under {}".format(ihp_lib_ngspice, open_pdks))
os.environ["SPICE_MODEL_DIR"] = spice_model_dir

open_pdks = os.path.abspath(open_pdks)
ihp_magicrc = os.path.join(open_pdks, 'magic', "ihp-sg13g2.magicrc")
if not os.path.exists(ihp_magicrc):
    raise SystemError("Did not find {} under {}".format(ihp_magicrc, open_pdks))
os.environ["OPENRAM_MAGICRC"] = ihp_magicrc
ihp_netgenrc = os.path.join(open_pdks, 'netgen', "ihp-sg13g2_setup.tcl")
if not os.path.exists(ihp_netgenrc):
    raise SystemError("Did not find {} under {}".format(ihp_netgenrc, open_pdks))
os.environ["OPENRAM_NETGENRC"] = ihp_netgenrc

try:
    DRCLVS_HOME = os.path.abspath(os.environ.get("DRCLVS_HOME"))
except:
    DRCLVS_HOME= "not-found"
os.environ["DRCLVS_HOME"] = DRCLVS_HOME
