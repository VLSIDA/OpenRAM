#!/usr/bin/env python2.7
"Run a regresion test on a basic parameterized transistors"

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.OPTS

#@unittest.skip("SKIPPING 03_ptx_test")


class ptx_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False

        import ptx
        import tech

        debug.info(2, "Checking min size NMOS with 1 finger")
        fet = ptx.ptx(name="nmos_1_finger",
                      width=tech.drc["minwidth_tx"],
                      mults=1,
                      tx_type="nmos")
        # return it back to it's normal state
        OPTS.check_lvsdrc = True

        self.local_check(fet)
        globals.end_openram()


    def add_mods(self, fet):
        self.create_contacts()
        self.add_well_extension(fet)
        self.add_wire_extension(fet)
        self.add_well_tiedown(fet)
        self.add_poly_tiedown(fet)

    def create_contacts(self):
        layer_stack = ("active", "contact", "metal1")
        self.well_contact = contact.contact(layer_stack)

        layer_stack = ("poly", "contact", "metal1")
        self.poly_contact = contact.contact(layer_stack)

    def add_well_tiedown(self, fet):
        offset = [fet.active_contact_positions[0][0],
                  fet.active_contact_positions[0][1] + fet.well_height]
        fet.add_inst(name="well_tap",
                     mod=self.well_contact,
                     offset=offset,
                     mirror="R0",
                     rotate=0)
        fet.well_contact = self.well_contact
        fet.well_tiedown_location = offset

    def add_well_extension(self, fet):
        well_define = {"pmos": "nwell",
                       "nmos": "pwell"}
        well_type = well_define[fet.tx_type]
        offset = getattr(fet,"{}_position".format(well_type))
        if tech.info["has_{0}".format(well_type)]:
            fet.add_rect(layerNumber=tech.layer[well_type],
                         offset=offset,
                         width=fet.well_width,
                         height=2 * fet.well_height)
        fet.add_rect(layerNumber=tech.layer["{0}implant".format(fet.tx_type[0])],
                     offset=offset,
                     width=fet.well_width,
                     height=2 * fet.well_height)
        fet.add_rect(layerNumber=tech.layer["vtg"],
                     offset=offset,
                     width=fet.well_width,
                     height=2 * fet.well_height)

        well_type = "{0}well".format(fet.tx_type[0])
        offset[1] = offset[1] - 3 * fet.well_height
        if tech.info["has_{0}".format(well_type)]:
            fet.add_rect(layerNumber=tech.layer[well_type],
                         offset=offset, 
                         width=fet.well_width,
                         height=3 * fet.well_height)
        fet.add_rect(layerNumber=tech.layer["{0}implant".format(well_define[fet.tx_type][
                     0])],
                     offset=offset,
                     width=fet.well_width,
                     height=3 * fet.well_height)
        fet.add_rect(layerNumber=tech.layer["vtg"],
                     offset=offset,
                     width=fet.well_width,
                     height=3 * fet.well_height)

    def add_wire_extension(self, fet):
        xcorrect = (fet.active_contact.width / 2) - (tech.drc["minwidth_metal1"] / 2)
        offset = [fet.active_contact_positions[0][0] + xcorrect,
                  fet.active_contact_positions[0][1]]
        fet.add_rect(layerNumber=tech.layer["metal1"],
                     offset=offset,
                     width=tech.drc["minwidth_metal1"],
                     height=fet.well_height)

        offset = [fet.active_contact_positions[-1][0] + xcorrect,
                  fet.active_contact_positions[-1][1] - 2 * fet.well_height]
        fet.add_rect(layerNumber=tech.layer["metal1"],
                     offset=offset,
                     width=tech.drc["minwidth_metal1"],
                     height=2 * fet.well_height)

        offset = [fet.poly_positions[-1][0],
                  fet.poly_positions[-1][1] - (fet.well_height)]
        fet.add_rect(layerNumber=tech.layer["poly"],
                     offset=offset,
                     width=tech.drc["minwidth_poly"],
                     height=fet.well_height)

    def add_poly_tiedown(self, fet):
        xcorrect = abs(self.poly_contact.upper_layer_vertical_enclosure -
                       self.poly_contact.lower_layer_vertical_enclosure)
        offset = [fet.poly_positions[-1][0] - xcorrect,
                  fet.poly_positions[-1][1] - (fet.well_height)]
        fet.add_inst(name="poly_contact",
                     mod=self.poly_contact,
                     offset=offset,
                     mirror="R270")


        offset = [fet.active_contact_positions[-1][0], fet.active_contact_positions
                  [-1][1] - 2 * fet.well_height - self.well_contact.height]
        fet.poly_tiedown_location = offset
        fet.add_inst(name="n_tiedown",
                     mod=self.well_contact,
                     offset=offset)
        tech.ptx_port.add_custom_layer(fet)

    def local_check(self, fet):
        tempspice = OPTS.openram_temp + "temp.sp"
        tempgds = OPTS.openram_temp + "temp.gds"

        fet.sp_write(tempspice)
        fet.gds_write(tempgds)

        self.assertFalse(calibre.run_drc(fet.name, tempgds))

        os.remove(tempspice)
        os.remove(tempgds)

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
