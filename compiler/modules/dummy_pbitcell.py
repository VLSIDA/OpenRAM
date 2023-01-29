# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import design
from openram.base import vector
from openram.sram_factory import factory
from openram import OPTS


class dummy_pbitcell(design):
    """
    Creates a replica bitcell using pbitcell
    """

    def __init__(self, name, cell_name=None):
        self.num_rw_ports = OPTS.num_rw_ports
        self.num_w_ports = OPTS.num_w_ports
        self.num_r_ports = OPTS.num_r_ports
        self.total_ports = self.num_rw_ports + self.num_w_ports + self.num_r_ports

        design.__init__(self, name)
        debug.info(1, "create a dummy bitcell using pbitcell with {0} rw ports, {1} w ports and {2} r ports".format(self.num_rw_ports,
                                                                                                                    self.num_w_ports,
                                                                                                                    self.num_r_ports))

        self.create_netlist()
        self.create_layout()
        self.add_boundary()

    def create_netlist(self):
        self.add_pins()
        self.add_modules()
        self.create_modules()

    def create_layout(self):
        self.place_pbitcell()
        self.route_rbc_connections()
        self.DRC_LVS()

    def add_pins(self):
        for port in range(self.total_ports):
            self.add_pin("bl{}".format(port))
            self.add_pin("br{}".format(port))

        for port in range(self.total_ports):
            self.add_pin("wl{}".format(port))

        self.add_pin("vdd")
        self.add_pin("gnd")

    def add_modules(self):
        self.prbc = factory.create(module_type="pbitcell",
                                   dummy_bitcell=True)

        self.height = self.prbc.height
        self.width = self.prbc.width

    def create_modules(self):
        self.prbc_inst = self.add_inst(name="pbitcell",
                                       mod=self.prbc)

        temp = []
        for port in range(self.total_ports):
            temp.append("bl{}".format(port))
            temp.append("br{}".format(port))
        for port in range(self.total_ports):
            temp.append("wl{}".format(port))
        temp.append("vdd")
        temp.append("gnd")
        self.connect_inst(temp)

    def place_pbitcell(self):
        self.prbc_inst.place(offset=vector(0, 0))

    def route_rbc_connections(self):
        for port in range(self.total_ports):
            self.copy_layout_pin(self.prbc_inst, "bl{}".format(port))
            self.copy_layout_pin(self.prbc_inst, "br{}".format(port))
        for port in range(self.total_ports):
            self.copy_layout_pin(self.prbc_inst, "wl{}".format(port))
        self.copy_layout_pin(self.prbc_inst, "vdd")
        self.copy_layout_pin(self.prbc_inst, "gnd")

    def get_wl_cin(self):
        """Return the relative capacitance of the access transistor gates"""
        #This module is made using a pbitcell. Get the cin from that module
        return self.prbc.get_wl_cin()
