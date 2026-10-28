# See LICENSE for licensing information.
"""Generic contacted FET geometry with SG13G2's implicit N+ diffusion."""

from openram.modules.ptx import ptx


class ihp_ptx(ptx):
    def create_netlist(self):
        super().create_netlist()
        # IHP subcircuit W/L use SI units, unlike SKY130's scaled models.
        self.spice_device = self.lvs_device

    def add_active(self):
        super().add_active()
        if self.tx_type == "nmos":
            # N+ is implicit outside pSD. Drawing nSD over a gate excludes
            # the MOS from the installed deck's device recognition.
            self.objs.remove(self.implant)
