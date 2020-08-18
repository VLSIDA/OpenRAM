# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import design
from globals import OPTS
from sram_factory import factory
import debug


class global_bitcell_array(design.design):
    """
    Creates a global bitcell array.
    Rows is an integer number for all local arrays.
    Cols is a list of the array widths.
    add_left_rbl and add_right_
    """
    def __init__(self, rows, cols, ports, name=""):
        # The total of all columns will be the number of columns
        super().__init__(name=name)
        self.cols = cols
        self.rows = rows
        self.all_ports = ports

        debug.check(len(ports)<=2, "Only support dual port or less in global bitcell array.")
        self.rbl = [1, 1 if len(self.all_ports)>1 else 0]
        self.left_rbl = self.rbl[0]
        self.right_rbl = self.rbl[1]
        

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()
        
    def create_netlist(self):
        """ Create and connect the netlist """
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):

        self.place()

        self.add_layout_pins()

        self.add_boundary()
        
        self.DRC_LVS()

    def add_modules(self):
        """ Add the modules used in this design """
        self.local_mods = []

        for i, cols in enumerate(self.cols):
            # Always add the left RBLs to the first subarray and the right RBLs to the last subarray
            if i == 0:
                la = factory.create(module_type="local_bitcell_array", rows=self.rows, cols=cols, rbl=self.rbl, add_rbl=[self.left_rbl, 0])
            elif i == len(self.cols) - 1:
                la = factory.create(module_type="local_bitcell_array", rows=self.rows, cols=cols, rbl=self.rbl, add_rbl=[0, self.right_rbl])
            else:
                la = factory.create(module_type="local_bitcell_array", rows=self.rows, cols=cols, rbl=self.rbl, add_rbl=[0, 0])
                
            self.add_mod(la)
            self.local_mods.append(la)

        import pdb; pdb.set_trace()
        
    def add_pins(self):

        self.add_bitline_pins()
        self.add_wordline_pins()

        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_bitline_pins(self):
        
        # Regular bitline names for all ports
        self.bitline_names = []
        
        for port in range(self.left_rbl):
            left_names=["rbl_{0}_{1}".format(self.cell.get_bl_name(x), port) for x in range(len(self.all_ports))]
            right_names=["rbl_{0}_{1}".format(self.cell.get_br_name(x), port) for x in range(len(self.all_ports))]
            # Interleave the left and right lists
            bitline_names = [x for t in zip(left_names, right_names) for x in t]
            self.bitline_names.extend(bitline_names)
            
        # Regular array bitline names
        for col in range(sum(self.cols)):
            left_names=["bl_{0}_{1}".format(self.cell.get_bl_name(x), port) for x in range(len(self.all_ports))]
            right_names=["bl_{0}_{1}".format(self.cell.get_br_name(x), port) for x in range(len(self.all_ports))]


        # Array of all port bitline names
        for port in range(self.add_left_rbl + self.add_right_rbl):
            left_names=["rbl_{0}_{1}".format(self.cell.get_bl_name(x), port) for x in range(len(self.all_ports))]
            right_names=["rbl_{0}_{1}".format(self.cell.get_br_name(x), port) for x in range(len(self.all_ports))]
            # Keep track of the left pins that are the RBL
            self.replica_bl_names[port]=left_names[self.all_ports[port]]
            # Interleave the left and right lists
            bitline_names = [x for t in zip(left_names, right_names) for x in t]
            self.replica_bitline_names[port] = bitline_names

        # Dummy bitlines are not connected to anything
        self.bitline_names.extend(self.bitcell_array_bitline_names)

        for port in self.all_ports:
            self.add_pin_list(self.replica_bitline_names[port], "INOUT")
        self.add_pin_list(self.bitline_names, "INOUT")
            
    def add_wordline_pins(self):
        
        # All wordline names for all ports
        self.wordline_names = []
        # Wordline names for each port
        self.wordline_names_by_port = [[] for x in self.all_ports]
        # Replica wordlines by port
        self.replica_wordline_names = [[] for x in self.all_ports]

        # Regular array wordline names
        self.bitcell_array_wordline_names = self.bitcell_array.get_all_wordline_names()
        
        # Create the full WL names include dummy, replica, and regular bit cells
        self.wordline_names = []
        
        # Left port WLs 
        for port in range(self.left_rbl):
            # Make names for all RBLs
            wl_names=["rbl_{0}_{1}".format(x, port) for x in self.cell.get_all_wl_names()]
            # Keep track of the pin that is the RBL
            self.replica_wordline_names[port] = wl_names
            self.wordline_names.extend(wl_names)
            
        # Regular WLs
        self.wordline_names.extend(self.bitcell_array_wordline_names)
        
        # Right port WLs
        for port in range(self.left_rbl, self.left_rbl + self.right_rbl):
            # Make names for all RBLs
            wl_names=["rbl_{0}_{1}".format(x, port) for x in self.cell.get_all_wl_names()]
            # Keep track of the pin that is the RBL
            self.replica_wordline_names[port] = wl_names
            self.wordline_names.extend(wl_names)
            
        self.dummy_wordline_names["top"] = ["{0}_top".format(x) for x in dummy_cell_wl_names]
        self.wordline_names.extend(self.dummy_wordline_names["top"])

        # Array of all port wl names
        for port in range(self.left_rbl + self.right_rbl):
            wl_names = ["rbl_{0}_{1}".format(x, port) for x in self.cell.get_all_wl_names()]
            self.replica_wordline_names[port] = wl_names

        self.add_pin_list(self.wordline_names, "INPUT")

        
    def create_instances(self):
        """ Create the module instances used in this design """
        self.local_inst = []
        for i, mod in self.local_mods:
            name = "la_{0}".format(i)
            self.local_inst.append(self.add_inst(name=name,
                                                 mod=mod))
            self.connect_inst(self.get_bitcell_pins(row, col))
        
    def place(self):
        offset = vector(0, 0)
        for inst in self.local_inst:
            inst.place(offset)
            offset = inst.rx() + 3 * self.m3_pitch
            
