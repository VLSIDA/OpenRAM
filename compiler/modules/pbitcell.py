# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import logical_effort
from openram.base import vector
from openram.tech import drc, parameter, layer
from openram.tech import cell_properties as props
from openram import OPTS
from .ptx import ptx
from .bitcell_base import bitcell_base


class pbitcell(bitcell_base):
    """
    This module implements a parametrically sized multi-port bitcell,
    with a variable number of read/write, write, and read ports
    """

    def __init__(self, name, replica_bitcell=False, dummy_bitcell=False):
        self.num_rw_ports = OPTS.num_rw_ports
        self.num_w_ports = OPTS.num_w_ports
        self.num_r_ports = OPTS.num_r_ports
        self.total_ports = self.num_rw_ports + self.num_w_ports + self.num_r_ports

        self.replica_bitcell = replica_bitcell
        self.dummy_bitcell = dummy_bitcell
        self.mirror = props.bitcell_1port.mirror
        self.end_caps = props.bitcell_1port.end_caps

        self.wl_layer = "m1"
        self.wl_dir = "H"

        self.bl_layer = "m2"
        self.bl_dir = "V"

        self.vdd_layer = "m1"
        self.vdd_dir = "H"

        self.gnd_layer = "m1"
        self.gnd_dir = "H"

        bitcell_base.__init__(self, name)
        fmt_str = "{0} rw ports, {1} w ports and {2} r ports"
        info_string = fmt_str.format(self.num_rw_ports,
                                     self.num_w_ports,
                                     self.num_r_ports)
        debug.info(2,
                   "create a multi-port bitcell with {}".format(info_string))
        self.add_comment(info_string)

        if self.dummy_bitcell:
            self.add_comment("dummy bitcell")
        if self.replica_bitcell:
            self.add_comment("replica bitcell")

        self.create_netlist()
        # We must always create the bitcell layout
        # because some transistor sizes in the other netlists depend on it
        self.create_layout()
        self.add_boundary()

    def create_netlist(self):
        self.add_pins()
        self.add_modules()
        self.create_storage()

        if(self.num_rw_ports > 0):
            self.create_readwrite_ports()
        if(self.num_w_ports > 0):
            self.create_write_ports()
        if(self.num_r_ports > 0):
            self.create_read_ports()

    def create_layout(self):
        self.calculate_spacing()
        self.calculate_postions()

        self.place_storage()
        self.route_storage()

        self.route_rails()

        if(self.num_rw_ports > 0):
            self.place_readwrite_ports()
            self.route_readwrite_access()
        if(self.num_w_ports > 0):
            self.place_write_ports()
            self.route_write_access()
        if(self.num_r_ports > 0):
            self.place_read_ports()
            self.route_read_access()
        self.extend_well()

        self.route_wordlines()
        self.route_bitlines()
        self.route_supplies()

        if self.replica_bitcell:
            self.route_rbc_short()

        # in netlist_only mode, calling offset_all_coordinates or
        # translate_all will not be possible
        # this function is not needed to calculate the dimensions
        # of pbitcell in netlist_only mode though
        if not OPTS.netlist_only:
            self.translate_all(vector(self.leftmost_xpos, self.botmost_ypos))

    def add_pins(self):
        """ add pins and set names for bitlines and wordlines """
        self.rw_bl_names = []
        self.rw_br_names = []
        self.w_bl_names = []
        self.w_br_names = []
        self.r_bl_names = []
        self.r_br_names = []
        self.rw_wl_names = []
        self.w_wl_names = []
        self.r_wl_names = []
        port = 0

        for k in range(self.num_rw_ports):
            self.add_pin("bl{}".format(port), "OUTPUT")
            self.add_pin("br{}".format(port), "OUTPUT")
            self.rw_bl_names.append("bl{}".format(port))
            self.rw_br_names.append("br{}".format(port))
            port += 1
        for k in range(self.num_w_ports):
            self.add_pin("bl{}".format(port), "INPUT")
            self.add_pin("br{}".format(port), "INPUT")
            self.w_bl_names.append("bl{}".format(port))
            self.w_br_names.append("br{}".format(port))
            port += 1
        for k in range(self.num_r_ports):
            self.add_pin("bl{}".format(port), "OUTPUT")
            self.add_pin("br{}".format(port), "OUTPUT")
            self.r_bl_names.append("bl{}".format(port))
            self.r_br_names.append("br{}".format(port))
            port += 1

        port = 0
        for k in range(self.num_rw_ports):
            self.add_pin("wl{}".format(port), "INPUT")
            self.rw_wl_names.append("wl{}".format(port))
            port += 1
        for k in range(self.num_w_ports):
            self.add_pin("wl{}".format(port), "INPUT")
            self.w_wl_names.append("wl{}".format(port))
            port += 1
        for k in range(self.num_r_ports):
            self.add_pin("wl{}".format(port), "INPUT")
            self.r_wl_names.append("wl{}".format(port))
            port += 1

        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

        # if this is a replica bitcell, replace the instances of Q_bar with vdd
        if self.replica_bitcell:
            self.Q_bar = "vdd"
        else:
            self.Q_bar = "Q_bar"
        self.Q = "Q"
        self.storage_nets = [self.Q, self.Q_bar]

    def add_modules(self):
        """ Determine size of transistors and add ptx modules """
        # if there are any read/write ports,
        # then the inverter nmos is sized based the number of read/write ports
        if(self.num_rw_ports > 0):
            inverter_nmos_width = self.num_rw_ports * parameter["6T_inv_nmos_size"]
            inverter_pmos_width = parameter["6T_inv_pmos_size"]
            readwrite_nmos_width = parameter["6T_access_size"]
            write_nmos_width = parameter["6T_access_size"]
            read_nmos_width = 2 * parameter["6T_inv_pmos_size"]

        # if there are no read/write ports,
        # then the inverter nmos is statically sized for the dual port case
        else:
            inverter_nmos_width = 2 * parameter["6T_inv_pmos_size"]
            inverter_pmos_width = parameter["6T_inv_pmos_size"]
            readwrite_nmos_width = parameter["6T_access_size"]
            write_nmos_width = parameter["6T_access_size"]
            read_nmos_width = 2 * parameter["6T_inv_pmos_size"]

        # create ptx for inverter transistors
        self.inverter_nmos = ptx(width=inverter_nmos_width,
                                 tx_type="nmos")

        self.inverter_pmos = ptx(width=inverter_pmos_width,
                                 tx_type="pmos")

        # create ptx for readwrite transitors
        self.readwrite_nmos = ptx(width=readwrite_nmos_width,
                                  tx_type="nmos")

        # create ptx for write transitors
        self.write_nmos = ptx(width=write_nmos_width,
                              tx_type="nmos")

        # create ptx for read transistors
        self.read_nmos = ptx(width=read_nmos_width,
                             tx_type="nmos")

    def calculate_spacing(self):
        """ Calculate transistor spacings """
        # calculate metal contact extensions over transistor active
        readwrite_nmos_contact_extension = 0.5 * \
                                           (self.readwrite_nmos.active_contact.height - self.readwrite_nmos.active_height)
        write_nmos_contact_extension = 0.5 * \
                                       (self.write_nmos.active_contact.height - self.write_nmos.active_height)
        read_nmos_contact_extension = 0.5 * \
                                      (self.read_nmos.active_contact.height - self.read_nmos.active_height)
        max_contact_extension = max(readwrite_nmos_contact_extension,
                                    write_nmos_contact_extension,
                                    read_nmos_contact_extension)

        # y-offset for the access transistor's gate contact
        self.gate_contact_yoffset = max_contact_extension + self.m2_space \
                                    + 0.5 * max(self.poly_contact.height, self.m1_via.height)

        # y-position of access transistors
        self.port_ypos = self.m1_space + 0.5 * self.m1_via.height + self.gate_contact_yoffset

        # y-position of inverter nmos
        self.inverter_nmos_ypos = self.port_ypos

        # spacing between ports (same for read/write and write ports)
        self.bitline_offset = -0.5 * self.readwrite_nmos.active_width \
                              + 0.5 * self.m1_via.height \
                              + self.m2_space + self.m2_width
        m2_constraint = self.bitline_offset + self.m2_space \
                        + 0.5 * self.m1_via.height \
                        - 0.5 * self.readwrite_nmos.active_width
        self.write_port_spacing = max(self.active_space,
                                      self.m1_space,
                                      m2_constraint)
        self.read_port_spacing = self.bitline_offset + self.m2_space

        # spacing between cross coupled inverters
        self.inverter_to_inverter_spacing = self.poly_contact.width + self.m1_space

        # calculations related to inverter connections
        inverter_pmos_contact_extension = 0.5 * \
                                          (self.inverter_pmos.active_contact.height - self.inverter_pmos.active_height)
        inverter_nmos_contact_extension = 0.5 * \
                                          (self.inverter_nmos.active_contact.height - self.inverter_nmos.active_height)
        self.inverter_gap = max(self.poly_to_active,
                                self.m1_space + inverter_nmos_contact_extension) \
                                + self.poly_to_contact + 2 * self.poly_contact.width \
                                + self.m1_space + inverter_pmos_contact_extension
        self.cross_couple_lower_ypos = self.inverter_nmos_ypos \
                                       + self.inverter_nmos.active_height \
                                       + max(self.poly_to_active,
                                             self.m1_space + inverter_nmos_contact_extension) \
                                       + 0.5 * self.poly_contact.width
        self.cross_couple_upper_ypos = self.inverter_nmos_ypos \
                                       + self.inverter_nmos.active_height \
                                       + max(self.poly_to_active,
                                             self.m1_space + inverter_nmos_contact_extension) \
                                       + self.poly_to_contact \
                                       + 1.5 * self.poly_contact.width

        # spacing between wordlines (and gnd)
        self.m1_offset = -0.5 * self.m1_width

        # spacing for vdd
        implant_constraint = max(inverter_pmos_contact_extension, 0) \
                             + 2 * self.implant_enclose_active \
                             + 0.5*(self.inverter_pmos.active_contact.height - self.m1_width)
        metal1_constraint = max(inverter_pmos_contact_extension, 0) + self.m1_space
        self.vdd_offset = max(implant_constraint, metal1_constraint)  + self.m1_width

        # read port dimensions
        width_reduction = self.read_nmos.active_width - self.read_nmos.get_pin("D").cx()
        self.read_port_width = 2 * self.read_nmos.active_width - 2 * width_reduction

    def calculate_postions(self):
        """
        Calculate positions that describe the edges
        and dimensions of the cell
        """
        self.botmost_ypos = self.m1_offset - self.total_ports * self.m1_nonpref_pitch
        self.topmost_ypos = self.inverter_nmos_ypos \
                            + self.inverter_nmos.active_height \
                            + self.inverter_gap \
                            + self.inverter_pmos.active_height \
                            + self.vdd_offset

        self.leftmost_xpos = -0.5 * self.inverter_to_inverter_spacing \
                             - self.inverter_nmos.active_width \
                             - self.num_rw_ports * \
                             (self.readwrite_nmos.active_width + self.write_port_spacing) \
                             - self.num_w_ports * \
                             (self.write_nmos.active_width + self.write_port_spacing) \
                             - self.num_r_ports * \
                             (self.read_port_width + self.read_port_spacing) \
                             - self.bitline_offset - 0.5 * self.m1_via.width

        self.width = -2 * self.leftmost_xpos
        self.height = self.topmost_ypos - self.botmost_ypos
        self.center_ypos = 0.5 * (self.topmost_ypos + self.botmost_ypos)

    def create_storage(self):
        """
        Creates the crossed coupled inverters that act
        as storage for the bitcell.
        The stored value of the cell is denoted as "Q",
        and the inverted value as "Q_bar".
        """
        # create active for nmos
        self.inverter_nmos_left = self.add_inst(name="inverter_nmos_left",
                                                mod=self.inverter_nmos)
        self.connect_inst([self.Q, self.Q_bar, "gnd", "gnd"])

        self.inverter_nmos_right = self.add_inst(name="inverter_nmos_right",
                                                 mod=self.inverter_nmos)
        self.connect_inst(["gnd", self.Q, self.Q_bar, "gnd"])

        # create active for pmos
        self.inverter_pmos_left = self.add_inst(name="inverter_pmos_left",
                                                mod=self.inverter_pmos)
        self.connect_inst([self.Q, self.Q_bar, "vdd", "vdd"])

        self.inverter_pmos_right = self.add_inst(name="inverter_pmos_right",
                                                 mod=self.inverter_pmos)
        self.connect_inst(["vdd", self.Q, self.Q_bar, "vdd"])

    def place_storage(self):
        """
        Places the transistors for the crossed
        coupled inverters in the bitcell
        """
        # calculate transistor offsets
        left_inverter_xpos = -0.5 * self.inverter_to_inverter_spacing \
                             - self.inverter_nmos.active_width
        right_inverter_xpos = 0.5 * self.inverter_to_inverter_spacing
        inverter_pmos_ypos = self.inverter_nmos_ypos \
                             + self.inverter_nmos.active_height \
                             + self.inverter_gap

        # create active for nmos
        self.inverter_nmos_left.place([left_inverter_xpos,
                                       self.inverter_nmos_ypos])
        self.inverter_nmos_right.place([right_inverter_xpos,
                                        self.inverter_nmos_ypos])

        # create active for pmos
        self.inverter_pmos_left.place([left_inverter_xpos,
                                       inverter_pmos_ypos])
        self.inverter_pmos_right.place([right_inverter_xpos,
                                        inverter_pmos_ypos])

        # update furthest left and right transistor edges
        # (this will propagate to further transistor offset calculations)
        self.left_building_edge = left_inverter_xpos
        self.right_building_edge = right_inverter_xpos \
                                   + self.inverter_nmos.active_width

    def add_pex_labels(self, left_inverter_offset, right_inverter_offset):
        self.add_label("Q", "metal1", left_inverter_offset)
        self.add_label("Q_bar", "metal1", right_inverter_offset)
        self.storage_net_offsets = [left_inverter_offset, right_inverter_offset]

    def route_storage(self):
        """ Routes inputs and outputs of inverters to cross couple them """
        # connect input (gate) of inverters
        self.add_path("poly",
                      [self.inverter_nmos_left.get_pin("G").uc(),
                       self.inverter_pmos_left.get_pin("G").bc()])
        self.add_path("poly",
                      [self.inverter_nmos_right.get_pin("G").uc(),
                       self.inverter_pmos_right.get_pin("G").bc()])

        # connect output (drain/source) of inverters
        self.add_path("m1",
                      [self.inverter_nmos_left.get_pin("D").uc(),
                       self.inverter_pmos_left.get_pin("D").bc()],
                      width=self.inverter_nmos_left.get_pin("D").width())
        self.add_path("m1",
                      [self.inverter_nmos_right.get_pin("S").uc(),
                       self.inverter_pmos_right.get_pin("S").bc()],
                      width=self.inverter_nmos_right.get_pin("S").width())

        # add contacts to connect gate poly to drain/source
        # metal1 (to connect Q to Q_bar)
        contact_offset_left =  vector(self.inverter_nmos_left.get_pin("D").rc().x \
                                      + 0.5 * self.poly_contact.height,
                                      self.cross_couple_upper_ypos)
        self.add_via_center(layers=self.poly_stack,
                            offset=contact_offset_left,
                            directions=("H", "H"))

        contact_offset_right =  vector(self.inverter_nmos_right.get_pin("S").lc().x \
                                       - 0.5*self.poly_contact.height,
                                       self.cross_couple_lower_ypos)
        self.add_via_center(layers=self.poly_stack,
                            offset=contact_offset_right,
                            directions=("H", "H"))

        # connect contacts to gate poly (cross couple connections)
        gate_offset_right = vector(self.inverter_nmos_right.get_pin("G").lc().x,
                                   contact_offset_left.y)
        self.add_path("poly", [contact_offset_left, gate_offset_right])

        gate_offset_left = vector(self.inverter_nmos_left.get_pin("G").rc().x,
                                  contact_offset_right.y)
        self.add_path("poly", [contact_offset_right, gate_offset_left])
        if OPTS.use_pex:
        # add labels to cross couple inverter for extracted simulation
            contact_offset_left_output =  vector(self.inverter_nmos_left.get_pin("D").rc().x \
                                    + 0.5 * self.poly.height,
                                    self.cross_couple_upper_ypos)

            contact_offset_right_output =  vector(self.inverter_nmos_right.get_pin("S").lc().x \
                                    - 0.5*self.poly.height,
                                    self.cross_couple_lower_ypos)
            self.add_pex_labels(contact_offset_left_output, contact_offset_right_output)

    def route_rails(self):
        """ Adds gnd and vdd rails and connects them to the inverters """

        # Add rails for vdd and gnd
        gnd_ypos = self.m1_offset - self.total_ports * self.m1_nonpref_pitch
        self.gnd_position = vector(0, gnd_ypos)
        self.add_layout_pin_rect_center(text="gnd",
                                       layer="m1",
                                       offset=self.gnd_position,
                                       width=self.width)

        vdd_ypos = self.inverter_nmos_ypos \
                   + self.inverter_nmos.active_height \
                   + self.inverter_gap \
                   + self.inverter_pmos.active_height \
                   + self.vdd_offset
        self.vdd_position = vector(0, vdd_ypos)
        self.add_layout_pin_rect_center(text="vdd",
                                        layer="m1",
                                        offset=self.vdd_position,
                                        width=self.width)

    def create_readwrite_ports(self):
        """
        Creates read/write ports to the bit cell. A differential
        pair of transistor can both read and write, like in a 6T cell.
        A read or write is enabled by setting a Read-Write-Wordline (RWWL)
        high, subsequently turning on the transistor.
        The transistor is connected between a Read-Write-Bitline (RWBL)
        and the storage component of the cell (Q).
        In a write operation, driving RWBL high or low sets the value
        of the cell.
        In a read operation, RWBL is precharged, then is either remains
        high or is discharged depending on the value of the cell.
        This is a differential design, so each write port has a mirrored
        port that connects RWBR to Q_bar.
        """
        # define read/write transistor variables as empty arrays based
        # on the number of read/write ports
        self.readwrite_nmos_left = [None] * self.num_rw_ports
        self.readwrite_nmos_right = [None] * self.num_rw_ports

        # iterate over the number of read/write ports
        for k in range(0, self.num_rw_ports):
            bl_name = self.rw_bl_names[k]
            br_name = self.rw_br_names[k]
            if self.dummy_bitcell:
                bl_name += "_noconn"
                br_name += "_noconn"

            # add read/write transistors
            self.readwrite_nmos_left[k] = self.add_inst(name="readwrite_nmos_left{}".format(k),
                                                        mod=self.readwrite_nmos)
            self.connect_inst([bl_name, self.rw_wl_names[k], self.Q, "gnd"])

            self.readwrite_nmos_right[k] = self.add_inst(name="readwrite_nmos_right{}".format(k),
                                                         mod=self.readwrite_nmos)
            self.connect_inst([self.Q_bar,
                               self.rw_wl_names[k], br_name, "gnd"])


    def place_readwrite_ports(self):
        """ Places read/write ports in the bit cell """
        # define read/write transistor variables as empty arrays
        # based on the number of read/write ports
        self.rwwl_positions = [None] * self.num_rw_ports
        self.rwbl_positions = [None] * self.num_rw_ports
        self.rwbr_positions = [None] * self.num_rw_ports

        # iterate over the number of read/write ports
        for k in range(0, self.num_rw_ports):
            # calculate read/write transistor offsets
            left_readwrite_transistor_xpos = self.left_building_edge \
                                             - (k + 1) * self.write_port_spacing \
                                             - (k + 1) * self.readwrite_nmos.active_width

            right_readwrite_transistor_xpos = self.right_building_edge \
                                              + (k + 1) * self.write_port_spacing \
                                              + k * self.readwrite_nmos.active_width

            # place read/write transistors
            self.readwrite_nmos_left[k].place(offset=[left_readwrite_transistor_xpos,
                                                      self.port_ypos])

            self.readwrite_nmos_right[k].place(offset=[right_readwrite_transistor_xpos,
                                                       self.port_ypos])

            # add pin for RWWL
            rwwl_ypos = self.m1_offset - k * self.m1_nonpref_pitch
            self.rwwl_positions[k] = vector(0, rwwl_ypos)
            self.add_layout_pin_rect_center(text=self.rw_wl_names[k],
                                            layer="m1",
                                            offset=self.rwwl_positions[k],
                                            width=self.width)

            # add pins for RWBL and RWBR
            rwbl_xpos = left_readwrite_transistor_xpos \
                        - self.bitline_offset \
                        + 0.5 * self.m2_width
            self.rwbl_positions[k] = vector(rwbl_xpos, self.center_ypos)
            self.add_layout_pin_rect_center(text=self.rw_bl_names[k],
                                            layer="m2",
                                            offset=self.rwbl_positions[k],
                                            height=self.height)

            rwbr_xpos = right_readwrite_transistor_xpos \
                        + self.readwrite_nmos.active_width \
                        + self.bitline_offset \
                        - 0.5 * self.m2_width
            self.rwbr_positions[k] = vector(rwbr_xpos, self.center_ypos)
            self.add_layout_pin_rect_center(text=self.rw_br_names[k],
                                            layer="m2",
                                            offset=self.rwbr_positions[k],
                                            height=self.height)

            if self.dummy_bitcell:
                bl_name = self.rw_bl_names[k]
                br_name = self.rw_br_names[k]
                bl_name += "_noconn"
                br_name += "_noconn"

                # This helps with LVS matching in klayout
                drain_pin = self.readwrite_nmos_left[k].get_pin("S")
                self.add_label(bl_name, drain_pin.layer, drain_pin.center())

                # This helps with LVS matching in klayout
                source_pin = self.readwrite_nmos_right[k].get_pin("D")
                self.add_label(br_name, source_pin.layer, source_pin.center())


        # update furthest left and right transistor edges
        self.left_building_edge = left_readwrite_transistor_xpos
        self.right_building_edge = right_readwrite_transistor_xpos \
                                   + self.readwrite_nmos.active_width

    def create_write_ports(self):
        """
        Creates write ports in the bit cell. A differential pair of
        transistors can write only.
        A write is enabled by setting a Write-Rowline (WWL) high,
        subsequently turning on the transistor.
        The transistor is connected between a Write-Bitline (WBL)
        and the storage component of the cell (Q).
        In a write operation, driving WBL high or low sets the value
        of the cell.
        This is a differential design, so each write port has a
        mirrored port that connects WBR to Q_bar.
        """
        # define write transistor variables as empty arrays based
        # on the number of write ports
        self.write_nmos_left = [None] * self.num_w_ports
        self.write_nmos_right = [None] * self.num_w_ports

        # iterate over the number of write ports
        for k in range(0, self.num_w_ports):
            bl_name = self.w_bl_names[k]
            br_name = self.w_br_names[k]
            if self.dummy_bitcell:
                bl_name += "_noconn"
                br_name += "_noconn"

            # add write transistors
            self.write_nmos_left[k] = self.add_inst(name="write_nmos_left{}".format(k),
                                                    mod=self.write_nmos)
            self.connect_inst([bl_name, self.w_wl_names[k], self.Q, "gnd"])

            self.write_nmos_right[k] = self.add_inst(name="write_nmos_right{}".format(k),
                                                     mod=self.write_nmos)
            self.connect_inst([self.Q_bar, self.w_wl_names[k], br_name, "gnd"])

    def place_write_ports(self):
        """ Places write ports in the bit cell """
        # define write transistor variables as empty arrays based
        # on the number of write ports
        self.wwl_positions = [None] * self.num_w_ports
        self.wbl_positions = [None] * self.num_w_ports
        self.wbr_positions = [None] * self.num_w_ports

        # iterate over the number of write ports
        for k in range(0, self.num_w_ports):
            # Add transistors
            # calculate write transistor offsets
            left_write_transistor_xpos = self.left_building_edge \
                                         - (k + 1) * self.write_port_spacing \
                                         - (k + 1) * self.write_nmos.active_width

            right_write_transistor_xpos = self.right_building_edge \
                                          + (k + 1) * self.write_port_spacing \
                                          + k * self.write_nmos.active_width

            # add write transistors
            self.write_nmos_left[k].place(offset=[left_write_transistor_xpos,
                                                  self.port_ypos])

            self.write_nmos_right[k].place(offset=[right_write_transistor_xpos,
                                                   self.port_ypos])

            # add pin for WWL
            wwl_ypos = rwwl_ypos = self.m1_offset \
                                   - self.num_rw_ports * self.m1_nonpref_pitch \
                                   - k * self.m1_nonpref_pitch
            self.wwl_positions[k] = vector(0, wwl_ypos)
            self.add_layout_pin_rect_center(text=self.w_wl_names[k],
                                            layer="m1",
                                            offset=self.wwl_positions[k],
                                            width=self.width)

            # add pins for WBL and WBR
            wbl_xpos = left_write_transistor_xpos \
                       - self.bitline_offset \
                       + 0.5 * self.m2_width
            self.wbl_positions[k] = vector(wbl_xpos, self.center_ypos)
            self.add_layout_pin_rect_center(text=self.w_bl_names[k],
                                            layer="m2",
                                            offset=self.wbl_positions[k],
                                            height=self.height)

            wbr_xpos = right_write_transistor_xpos \
                       + self.write_nmos.active_width \
                       + self.bitline_offset \
                       - 0.5 * self.m2_width
            self.wbr_positions[k] = vector(wbr_xpos, self.center_ypos)
            self.add_layout_pin_rect_center(text=self.w_br_names[k],
                                            layer="m2",
                                            offset=self.wbr_positions[k],
                                            height=self.height)

            if self.dummy_bitcell:
                bl_name = self.w_bl_names[k]
                br_name = self.w_br_names[k]
                bl_name += "_noconn"
                br_name += "_noconn"

                # This helps with LVS matching in klayout
                drain_pin = self.write_nmos_left[k].get_pin("S")
                self.add_label(bl_name, drain_pin.layer, drain_pin.center())

                # This helps with LVS matching in klayout
                source_pin = self.write_nmos_right[k].get_pin("D")
                self.add_label(br_name, source_pin.layer, source_pin.center())

        # update furthest left and right transistor edges
        self.left_building_edge = left_write_transistor_xpos
        self.right_building_edge = right_write_transistor_xpos \
                                   + self.write_nmos.active_width

    def create_read_ports(self):
        """
        Creates read ports in the bit cell. A differential pair
        of ports can read only.
        Two transistors function as a read port, denoted as the
        "read transistor" and the "read-access transistor".
        The read transistor is connected to RWL (gate), RBL (drain),
        and the read-access transistor (source).
        The read-access transistor is connected to Q_bar (gate),
        gnd (source), and the read transistor (drain).
        A read is enabled by setting a Read-Rowline (RWL) high,
        subsequently turning on the read transistor.
        The Read-Bitline (RBL) is precharged to high, and when the
        value of Q_bar is high, the read-access transistor
        is turned on, creating a connection between RBL and gnd.
        RBL subsequently discharges allowing for a differential read
        using sense amps. This is a differential design, so each
        read port has a mirrored port that connects RBL_bar to Q.
        """

        # define read transistor variables as empty arrays based
        # on the number of read ports
        self.read_nmos_left = [None] * self.num_r_ports
        self.read_nmos_right = [None] * self.num_r_ports
        self.read_access_nmos_left = [None] * self.num_r_ports
        self.read_access_nmos_right = [None] * self.num_r_ports

        # iterate over the number of read ports
        for k in range(0, self.num_r_ports):
            bl_name = self.r_bl_names[k]
            br_name = self.r_br_names[k]
            if self.dummy_bitcell:
                bl_name += "_noconn"
                br_name += "_noconn"

            # add read-access transistors
            self.read_access_nmos_left[k] = self.add_inst(name="read_access_nmos_left{}".format(k),
                                                          mod=self.read_nmos)
            self.connect_inst(["RA_to_R_left{}".format(k), self.Q_bar, "gnd", "gnd"])

            self.read_access_nmos_right[k] = self.add_inst(name="read_access_nmos_right{}".format(k),
                                                           mod=self.read_nmos)
            self.connect_inst(["gnd", self.Q, "RA_to_R_right{}".format(k), "gnd"])

            # add read transistors
            self.read_nmos_left[k] = self.add_inst(name="read_nmos_left{}".format(k),
                                                   mod=self.read_nmos)
            self.connect_inst([bl_name, self.r_wl_names[k], "RA_to_R_left{}".format(k), "gnd"])

            self.read_nmos_right[k] = self.add_inst(name="read_nmos_right{}".format(k),
                                                    mod=self.read_nmos)
            self.connect_inst(["RA_to_R_right{}".format(k), self.r_wl_names[k], br_name, "gnd"])

    def place_read_ports(self):
        """ Places the read ports in the bit cell """
        # define read transistor variables as empty arrays based
        # on the number of read ports
        self.rwl_positions = [None] * self.num_r_ports
        self.rbl_positions = [None] * self.num_r_ports
        self.rbr_positions = [None] * self.num_r_ports

        # calculate offset to overlap the drain of the read-access transistor
        # with the source of the read transistor
        overlap_offset = self.read_nmos.get_pin("D").cx() \
                         - self.read_nmos.get_pin("S").cx()

        # iterate over the number of read ports
        for k in range(0, self.num_r_ports):
            # calculate transistor offsets
            left_read_transistor_xpos = self.left_building_edge \
                                        - (k + 1) * self.read_port_spacing \
                                        - (k + 1) * self.read_port_width

            right_read_transistor_xpos = self.right_building_edge \
                                         + (k + 1) * self.read_port_spacing \
                                         + k * self.read_port_width

            # add read-access transistors
            self.read_access_nmos_left[k].place(offset=[left_read_transistor_xpos+overlap_offset,
                                                        self.port_ypos])

            self.read_access_nmos_right[k].place(offset=[right_read_transistor_xpos,
                                                         self.port_ypos])

            # add read transistors
            self.read_nmos_left[k].place(offset=[left_read_transistor_xpos,
                                                 self.port_ypos])

            self.read_nmos_right[k].place(offset=[right_read_transistor_xpos+overlap_offset,
                                                  self.port_ypos])

            # add pin for RWL
            rwl_ypos = rwwl_ypos = self.m1_offset \
                                   - self.num_rw_ports * self.m1_nonpref_pitch \
                                   - self.num_w_ports * self.m1_nonpref_pitch \
                                   - k * self.m1_nonpref_pitch
            self.rwl_positions[k] = vector(0, rwl_ypos)
            self.add_layout_pin_rect_center(text=self.r_wl_names[k],
                                            layer="m1",
                                            offset=self.rwl_positions[k],
                                            width=self.width)

            # add pins for RBL and RBR
            rbl_xpos = left_read_transistor_xpos \
                       - self.bitline_offset \
                       + 0.5 * self.m2_width
            self.rbl_positions[k] = vector(rbl_xpos, self.center_ypos)
            self.add_layout_pin_rect_center(text=self.r_bl_names[k],
                                            layer="m2",
                                            offset=self.rbl_positions[k],
                                            height=self.height)

            rbr_xpos = right_read_transistor_xpos \
                       + self.read_port_width \
                       + self.bitline_offset \
                       - 0.5 * self.m2_width
            self.rbr_positions[k] = vector(rbr_xpos, self.center_ypos)
            self.add_layout_pin_rect_center(text=self.r_br_names[k],
                                            layer="m2",
                                            offset=self.rbr_positions[k],
                                            height=self.height)

            if self.dummy_bitcell:
                bl_name = self.r_bl_names[k]
                br_name = self.r_br_names[k]
                bl_name += "_noconn"
                br_name += "_noconn"

                # This helps with LVS matching in klayout
                drain_pin = self.read_access_nmos_left[k].get_pin("S")
                self.add_label(bl_name, drain_pin.layer, drain_pin.center())

                # This helps with LVS matching in klayout
                source_pin = self.read_access_nmos_right[k].get_pin("D")
                self.add_label(br_name, source_pin.layer, source_pin.center())

    def route_wordlines(self):
        """ Routes gate of transistors to their respective wordlines """
        port_transistors = []
        for k in range(self.num_rw_ports):
            port_transistors.append(self.readwrite_nmos_left[k])
            port_transistors.append(self.readwrite_nmos_right[k])
        for k in range(self.num_w_ports):
            port_transistors.append(self.write_nmos_left[k])
            port_transistors.append(self.write_nmos_right[k])
        for k in range(self.num_r_ports):
            port_transistors.append(self.read_nmos_left[k])
            port_transistors.append(self.read_nmos_right[k])

        wl_positions = []
        for k in range(self.num_rw_ports):
            wl_positions.append(self.rwwl_positions[k])
            wl_positions.append(self.rwwl_positions[k])
        for k in range(self.num_w_ports):
            wl_positions.append(self.wwl_positions[k])
            wl_positions.append(self.wwl_positions[k])
        for k in range(self.num_r_ports):
            wl_positions.append(self.rwl_positions[k])
            wl_positions.append(self.rwl_positions[k])

        for k in range(2 * self.total_ports):
            gate_offset = port_transistors[k].get_pin("G").bc()
            port_contact_offset = gate_offset \
                                  + vector(0,
                                           -self.gate_contact_yoffset + self.poly_extend_active)
            wl_contact_offset = vector(gate_offset.x, wl_positions[k].y)

            # first transistor on either side of the cross coupled inverters
            # does not need to route to wordline on metal2
            if (k == 0) or (k == 1):
                self.add_via_center(layers=self.poly_stack,
                                    offset=port_contact_offset)


                self.add_path("poly", [gate_offset, port_contact_offset])
                self.add_path("m1",
                              [port_contact_offset, wl_contact_offset])

            else:
                self.add_via_center(layers=self.poly_stack,
                                    offset=port_contact_offset)
                self.add_via_center(layers=self.m1_stack,
                                    offset=port_contact_offset)

                self.add_via_center(layers=self.m1_stack,
                                    offset=wl_contact_offset)

                self.add_path("poly", [gate_offset, port_contact_offset])
                self.add_path("m2",
                              [port_contact_offset, wl_contact_offset])

    def route_bitlines(self):
        """ Routes read/write transistors to their respective bitlines """
        left_port_transistors = []
        right_port_transistors = []
        for k in range(self.num_rw_ports):
            left_port_transistors.append(self.readwrite_nmos_left[k])
            right_port_transistors.append(self.readwrite_nmos_right[k])
        for k in range(self.num_w_ports):
            left_port_transistors.append(self.write_nmos_left[k])
            right_port_transistors.append(self.write_nmos_right[k])
        for k in range(self.num_r_ports):
            left_port_transistors.append(self.read_nmos_left[k])
            right_port_transistors.append(self.read_nmos_right[k])

        bl_positions = []
        br_positions = []
        for k in range(self.num_rw_ports):
            bl_positions.append(self.rwbl_positions[k])
            br_positions.append(self.rwbr_positions[k])
        for k in range(self.num_w_ports):
            bl_positions.append(self.wbl_positions[k])
            br_positions.append(self.wbr_positions[k])
        for k in range(self.num_r_ports):
            bl_positions.append(self.rbl_positions[k])
            br_positions.append(self.rbr_positions[k])

        for k in range(self.total_ports):
            port_contact_offest = left_port_transistors[k].get_pin("S").center()
            bl_offset = vector(bl_positions[k].x, port_contact_offest.y)

            # Leave bitline disconnected if a dummy cell
            if not self.dummy_bitcell:
                self.add_via_center(layers=self.m1_stack,
                                    offset=port_contact_offest,
                                    directions="nonpref")

            self.add_path("m2",
                          [port_contact_offest, bl_offset], width=self.m1_via.height)

        for k in range(self.total_ports):
            port_contact_offest = right_port_transistors[k].get_pin("D").center()
            br_offset = vector(br_positions[k].x, port_contact_offest.y)

            # Leave bitline disconnected if a dummy cell
            if not self.dummy_bitcell:
                self.add_via_center(layers=self.m1_stack,
                                    offset=port_contact_offest,
                                    directions="nonpref")

            self.add_path("m2",
                          [port_contact_offest, br_offset], width=self.m1_via.height)

    def route_supplies(self):
        """ Route inverter nmos and read-access nmos to gnd. Route inverter pmos to vdd. """
        # route inverter nmos and read-access nmos to gnd
        nmos_contact_positions = []
        nmos_contact_positions.append(self.inverter_nmos_left.get_pin("S").center())
        nmos_contact_positions.append(self.inverter_nmos_right.get_pin("D").center())
        for k in range(self.num_r_ports):
            nmos_contact_positions.append(self.read_access_nmos_left[k].get_pin("D").center())
            nmos_contact_positions.append(self.read_access_nmos_right[k].get_pin("S").center())

        for position in nmos_contact_positions:
            self.add_via_center(layers=self.m1_stack,
                                offset=position,
                                directions=("V", "V"))


            if position.x > 0:
                contact_correct = 0.5 * self.m1_via.height
            else:
                contact_correct = -0.5 * self.m1_via.height
            supply_offset = vector(position.x + contact_correct,
                                   self.gnd_position.y)
            self.add_via_center(layers=self.m1_stack,
                                offset=supply_offset,
                                directions=("H", "H"))

            self.add_path("m2", [position, supply_offset])

        # route inverter pmos to vdd
        vdd_pos_left = vector(self.inverter_nmos_left.get_pin("S").uc().x,
                              self.vdd_position.y)
        self.add_path("m1",
                      [self.inverter_pmos_left.get_pin("S").uc(), vdd_pos_left])

        vdd_pos_right = vector(self.inverter_nmos_right.get_pin("D").uc().x,
                               self.vdd_position.y)
        self.add_path("m1",
                      [self.inverter_pmos_right.get_pin("D").uc(), vdd_pos_right])

    def route_readwrite_access(self):
        """
        Routes read/write transistors to the storage
        component of the bitcell
        """
        for k in range(self.num_rw_ports):
            mid = vector(self.readwrite_nmos_left[k].get_pin("D").uc().x,
                         self.cross_couple_lower_ypos)
            Q_pos = vector(self.inverter_nmos_left.get_pin("D").lx(),
                           self.cross_couple_lower_ypos)
            self.add_path("m1",
                          [self.readwrite_nmos_left[k].get_pin("D").uc(), mid, Q_pos])

            mid = vector(self.readwrite_nmos_right[k].get_pin("S").uc().x,
                         self.cross_couple_lower_ypos)
            Q_bar_pos = vector(self.inverter_nmos_right.get_pin("S").rx(),
                               self.cross_couple_lower_ypos)
            self.add_path("m1",
                          [self.readwrite_nmos_right[k].get_pin("S").uc(), mid, Q_bar_pos])

    def route_write_access(self):
        """
        Routes read/write transistors to the storage
        component of the bitcell
        """
        for k in range(self.num_w_ports):
            mid = vector(self.write_nmos_left[k].get_pin("D").uc().x,
                         self.cross_couple_lower_ypos)
            Q_pos = vector(self.inverter_nmos_left.get_pin("D").lx(),
                           self.cross_couple_lower_ypos)
            self.add_path("m1",
                          [self.write_nmos_left[k].get_pin("D").uc(), mid, Q_pos])

            mid = vector(self.write_nmos_right[k].get_pin("S").uc().x,
                         self.cross_couple_lower_ypos)
            Q_bar_pos = vector(self.inverter_nmos_right.get_pin("S").rx(),
                               self.cross_couple_lower_ypos)
            self.add_path("m1",
                          [self.write_nmos_right[k].get_pin("S").uc(), mid, Q_bar_pos])

    def route_read_access(self):
        """
        Routes read access transistors to the storage
        component of the bitcell
        """
        # add poly to metal1 contacts for gates of the inverters
        left_storage_contact =  vector(self.inverter_nmos_left.get_pin("G").lc().x \
                                       - self.poly_to_contact - 0.5*self.poly_contact.width,
                                       self.cross_couple_upper_ypos)
        self.add_via_center(layers=self.poly_stack,
                            offset=left_storage_contact,
                            directions=("H", "H"))


        right_storage_contact =  vector(self.inverter_nmos_right.get_pin("G").rc().x \
                                        + self.poly_to_contact + 0.5*self.poly_contact.width,
                                        self.cross_couple_upper_ypos)
        self.add_via_center(layers=self.poly_stack,
                            offset=right_storage_contact,
                            directions=("H", "H"))

        inverter_gate_offset_left = vector(self.inverter_nmos_left.get_pin("G").lc().x, self.cross_couple_upper_ypos)
        self.add_path("poly", [left_storage_contact, inverter_gate_offset_left])

        inverter_gate_offset_right = vector(self.inverter_nmos_right.get_pin("G").rc().x, self.cross_couple_upper_ypos)
        self.add_path("poly", [right_storage_contact, inverter_gate_offset_right])

        # add poly to metal1 contacts for gates of read-access transistors
        # route from read-access contacts to inverter contacts on metal1
        for k in range(self.num_r_ports):
            port_contact_offset = self.read_access_nmos_left[k].get_pin("G").uc() \
                                  + vector(0,
                                           self.gate_contact_yoffset - self.poly_extend_active)

            self.add_via_center(layers=self.poly_stack,
                                offset=port_contact_offset)

            self.add_path("poly",
                          [self.read_access_nmos_left[k].get_pin("G").uc(), port_contact_offset])

            mid = vector(self.read_access_nmos_left[k].get_pin("G").uc().x,
                         self.cross_couple_upper_ypos)
            self.add_path("m1",
                          [port_contact_offset, mid, left_storage_contact])

            port_contact_offset = self.read_access_nmos_right[k].get_pin("G").uc() \
                                  + vector(0,
                                           self.gate_contact_yoffset - self.poly_extend_active)

            self.add_via_center(layers=self.poly_stack,
                                offset=port_contact_offset)

            self.add_path("poly",
                          [self.read_access_nmos_right[k].get_pin("G").uc(), port_contact_offset])

            mid = vector(self.read_access_nmos_right[k].get_pin("G").uc().x,
                         self.cross_couple_upper_ypos)
            self.add_path("m1",
                          [port_contact_offset, mid, right_storage_contact])

    def extend_well(self):
        """
        Connects wells between ptx modules and places well contacts
        """
        if "pwell" in layer:
            # extend pwell to encompass entire nmos region of the cell up to the
            # height of the tallest nmos transistor
            max_nmos_well_height = max(self.inverter_nmos.well_height,
                                       self.readwrite_nmos.well_height,
                                       self.write_nmos.well_height,
                                       self.read_nmos.well_height)
            well_height = max_nmos_well_height + self.port_ypos \
                          - self.nwell_enclose_active - self.gnd_position.y
            # FIXME fudge factor xpos
            well_width = self.width + 2 * self.nwell_enclose_active
            offset = vector(self.leftmost_xpos - self.nwell_enclose_active, self.botmost_ypos)
            self.add_rect(layer="pwell",
                          offset=offset,
                          width=well_width,
                          height=well_height)

        # extend nwell to encompass inverter_pmos
        # calculate offset of the left pmos well
        if "nwell" in layer:
            inverter_well_xpos = -(self.inverter_nmos.active_width + 0.5 * self.inverter_to_inverter_spacing) \
                                 - self.nwell_enclose_active
            inverter_well_ypos = self.inverter_nmos_ypos + self.inverter_nmos.active_height \
                                 + self.inverter_gap - self.nwell_enclose_active

            # calculate width of the two combined nwells
            # calculate height to encompass nimplant connected to vdd
            well_width = 2 * (self.inverter_nmos.active_width + 0.5 * self.inverter_to_inverter_spacing) \
                         + 2 * self.nwell_enclose_active
            well_height = self.vdd_position.y - inverter_well_ypos \
                          + self.nwell_enclose_active + drc["minwidth_tx"]

            offset = [inverter_well_xpos, inverter_well_ypos]
            self.add_rect(layer="nwell",
                          offset=offset,
                          width=well_width,
                          height=well_height)

        # add well contacts
        # connect pimplants to gnd
        offset = vector(0, self.gnd_position.y)
        self.add_via_center(layers=self.active_stack,
                            offset=offset,
                            directions=("H", "H"),
                            implant_type="p",
                            well_type="p")

        # connect nimplants to vdd
        offset = vector(0, self.vdd_position.y)
        self.add_via_center(layers=self.active_stack,
                            offset=offset,
                            directions=("H", "H"),
                            implant_type="n",
                            well_type="n")

    def get_bitcell_pins(self, col, row):
        """
        Creates a list of connections in the bitcell, indexed by column
        and row, for instance use in bitcell_array
        """
        bitcell_pins = []
        for port in range(self.total_ports):
            bitcell_pins.append("bl{0}_{1}".format(port, col))
            bitcell_pins.append("br{0}_{1}".format(port, col))
        for port in range(self.total_ports):
            bitcell_pins.append("wl{0}_{1}".format(port, row))
        bitcell_pins.append("vdd")
        bitcell_pins.append("gnd")
        return bitcell_pins

    def get_all_wl_names(self):
        """ Creates a list of all wordline pin names """
        wordline_names = self.rw_wl_names + self.w_wl_names + self.r_wl_names
        return wordline_names

    def get_all_bitline_names(self):
        """ Creates a list of all bitline pin names (both bl and br) """
        bitline_pins = []
        for port in range(self.total_ports):
            bitline_pins.append("bl{0}".format(port))
            bitline_pins.append("br{0}".format(port))
        return bitline_pins

    def get_all_bl_names(self):
        """ Creates a list of all bl pins names """
        return self.rw_bl_names + self.w_bl_names + self.r_bl_names

    def get_all_br_names(self):
        """ Creates a list of all br pins names """
        return self.rw_br_names + self.w_br_names + self.r_br_names

    def route_rbc_short(self):
        """
        Route the short from Q_bar to gnd necessary for
        the replica bitcell
        """
        Q_bar_pos = self.inverter_pmos_right.get_pin("S").center()
        vdd_pos = self.inverter_pmos_right.get_pin("D").center()
        self.add_path("m1", [Q_bar_pos, vdd_pos])

    def get_storage_net_names(self):
        """
        Returns names of storage nodes in bitcell in
        [non-inverting, inverting] format.
        """
        return self.storage_nets

    def get_bl_name(self, port=0):
        """Get bl name by port"""
        return "bl{}".format(port)

    def get_br_name(self, port=0):
        """Get bl name by port"""
        return "br{}".format(port)

    def get_wl_name(self, port=0):
        """Get wl name by port"""
        debug.check(port < 2, "Two ports for bitcell_2port only.")
        return "wl{}".format(port)

    def get_stage_effort(self, load):
        parasitic_delay = 1
        # This accounts for bitline being drained thought the access
        # TX and internal node
        size = 0.5
        # Assumes always a minimum sizes inverter. Could be
        # specified in the tech.py file.
        cin = 3

        # Internal loads due to port configs are halved.
        # This is to account for the size already being halved
        # for stacked TXs, but internal loads do not see this size
        # estimation.
        write_port_load = self.num_w_ports \
                          * logical_effort.convert_farad_to_relative_c(parameter['bitcell_drain_cap']) / 2
        # min size NMOS gate load
        read_port_load = self.num_r_ports / 2
        total_load = load + read_port_load + write_port_load
        return logical_effort('bitline',
                              size,
                              cin,
                              load + read_port_load,
                              parasitic_delay,
                              False)

    def input_load(self):
        """ Return the relative capacitance of the access transistor gates """

        # FIXME: This applies to bitline capacitances as well.
        # pbitcell uses the different sizing for the port access tx's. Not accounted for in this model.
        access_tx_cin = self.readwrite_nmos.get_cin()
        return 2 * access_tx_cin

    def build_graph(self, graph, inst_name, port_nets):
        """Adds edges to graph for pbitcell. Only readwrite and read ports."""

        if self.dummy_bitcell:
            return

        pin_dict = {pin: port for pin, port in zip(list(self.pins), port_nets)}

        # Edges added wl->bl, wl->br for every port except write ports
        rw_pin_names = zip(self.r_wl_names, self.r_bl_names, self.r_br_names)
        r_pin_names = zip(self.rw_wl_names, self.rw_bl_names, self.rw_br_names)

        for pin_zip in [rw_pin_names, r_pin_names]:
            for wl, bl, br in pin_zip:
                graph.add_edge(pin_dict[wl], pin_dict[bl], self)
                graph.add_edge(pin_dict[wl], pin_dict[br], self)
