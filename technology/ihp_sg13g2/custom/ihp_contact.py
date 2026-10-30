# See LICENSE for licensing information.
"""SG13G2 contacts use implicit N+ diffusion, not the nSD exclusion layer."""

from openram.base.contact import contact


class ihp_contact(contact):
    def create_implant_well_enclosures(self):
        super().create_implant_well_enclosures()
        if self.implant_type == "n":
            from openram.tech import layer
            self.objs = [obj for obj in self.objs if obj.lpp != layer["nimplant"]]
