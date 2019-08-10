# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California 
# All rights reserved.
#

import debug
import design
from tech import drc, spice
from vector import vector
from globals import OPTS
from sram_factory import factory
import logical_effort
import bitcell_array
import replica_column
import dummy_array

class replica_bitcell_array(design.design):
    """
    Creates a bitcell arrow of cols x rows and then adds the replica
    and dummy columns and rows.  Replica columns are on the left and
    right, respectively and connected to the given bitcell ports.
    Dummy are the outside columns/rows with WL and BL tied to gnd.
    Requires a regular bitcell array, replica bitcell, and dummy
    bitcell (Bl/BR disconnected).
    """
    def __init__(self, cols, rows, left_rbl, right_rbl, bitcell_ports, name):
        design.design.__init__(self, name)
        debug.info(1, "Creating {0} {1} x {2}".format(self.name, rows, cols))
        self.add_comment("rows: {0} cols: {1}".format(rows, cols))

        self.column_size = cols
        self.row_size = rows
        self.left_rbl = left_rbl
        self.right_rbl = right_rbl
        self.bitcell_ports = bitcell_ports

        debug.check(left_rbl+right_rbl==len(self.all_ports),"Invalid number of RBLs for port configuration.")
        debug.check(left_rbl+right_rbl==len(self.bitcell_ports),"Bitcell ports must match total RBLs.")
        
        # Two dummy rows/cols plus replica for each port
        self.extra_rows = 2 + left_rbl + right_rbl
        self.extra_cols = 2 + left_rbl + right_rbl
        
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

        # We don't offset this because we need to align
        # the replica bitcell in the control logic
        #self.offset_all_coordinates()
        
        
    def create_netlist(self):
        """ Create and connect the netlist """
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def add_modules(self):
        """  Array and dummy/replica columns 

        d or D = dummy cell (caps to distinguish grouping)
        r or R = replica cell (caps to distinguish grouping)
        b or B = bitcell 
         replica columns 1 
         v              v
        bdDDDDDDDDDDDDDDdb <- Dummy row 
        bdDDDDDDDDDDDDDDrb <- Dummy row 
        br--------------rb
        br|   Array    |rb
        br| row x col  |rb
        br--------------rb
        brDDDDDDDDDDDDDDdb <- Dummy row
        bdDDDDDDDDDDDDDDdb <- Dummy row

          ^^^^^^^^^^^^^^^
          dummy rows cols x 1

        ^ dummy columns  ^
          1 x (rows + 4)
        """

        # Bitcell for port names only
        self.cell = factory.create(module_type="bitcell")

        # Bitcell array
        self.bitcell_array = factory.create(module_type="bitcell_array",
                                            cols=self.column_size,
                                            rows=self.row_size)
        self.add_mod(self.bitcell_array)

        # Replica bitlines
        self.replica_columns = {}
        for bit in range(self.left_rbl+self.right_rbl):
            if bit<self.left_rbl:
                replica_bit = bit+1
            else:
                replica_bit = bit+self.row_size+1
            self.replica_columns[bit] = factory.create(module_type="replica_column",
                                                       rows=self.row_size,
                                                       left_rbl=self.left_rbl,
                                                       right_rbl=self.right_rbl,
                                                       replica_bit=replica_bit)
            self.add_mod(self.replica_columns[bit])
        
        # Dummy row
        self.dummy_row = factory.create(module_type="dummy_array",
                                        cols=self.column_size,
                                        rows=1,
                                        mirror=0)
        self.add_mod(self.dummy_row)

        # Dummy col (mirror starting at first if odd replica+dummy rows)
        self.dummy_col = factory.create(module_type="dummy_array",
                                        cols=1,
                                        rows=self.row_size + self.extra_rows,
                                        mirror=(self.left_rbl+1)%2)
        self.add_mod(self.dummy_col)
        
        

    def add_pins(self):

        self.bitcell_array_wl_names = [x for x in self.bitcell_array.pins if x.startswith("w")]
        self.bitcell_array_bl_names = [x for x in self.bitcell_array.pins if x.startswith("b")]
        
        # These are the non-indexed names 
        self.dummy_cell_wl_names = ["dummy_"+x for x in self.cell.get_all_wl_names()]
        self.dummy_cell_bl_names = ["dummy_"+x for x in self.cell.get_all_bitline_names()]
        self.dummy_row_bl_names = self.bitcell_array_bl_names

        # A dictionary because some ports may have nothing
        self.rbl_bl_names = {}
        self.rbl_br_names = {}
        self.rbl_wl_names = {}
        
        # Create the full WL names include dummy, replica, and regular bit cells
        self.replica_col_wl_names = []
        self.replica_col_wl_names.extend(["{0}_bot".format(x) for x in self.dummy_cell_wl_names])
        # Left port WLs (one dummy for each port when we allow >1 port)
        for port in range(self.left_rbl):
            # Make names for all RBLs
            wl_names=["rbl_{0}_{1}".format(self.cell.get_wl_name(x),port) for x in range(len(self.all_ports))]
            # Keep track of the pin that is the RBL
            self.rbl_wl_names[port]=wl_names[self.bitcell_ports[port]]
            self.replica_col_wl_names.extend(wl_names)
        # Regular WLs
        self.replica_col_wl_names.extend(self.bitcell_array_wl_names)
        # Right port WLs (one dummy for each port when we allow >1 port)
        for port in range(self.left_rbl,self.left_rbl+self.right_rbl):
            # Make names for all RBLs
            wl_names=["rbl_{0}_{1}".format(self.cell.get_wl_name(x),port) for x in range(len(self.all_ports))]
            # Keep track of the pin that is the RBL
            self.rbl_wl_names[port]=wl_names[self.bitcell_ports[port]]
            self.replica_col_wl_names.extend(wl_names)
        self.replica_col_wl_names.extend(["{0}_top".format(x) for x in self.dummy_cell_wl_names])

        # Left/right dummy columns are connected identically to the replica column
        self.dummy_col_wl_names = self.replica_col_wl_names


        # Per port bitline names
        self.replica_bl_names = {}
        self.replica_wl_names = {}
        # Array of all port bitline names
        for port in range(self.left_rbl+self.right_rbl):
            left_names=["rbl_{0}_{1}".format(self.cell.get_bl_name(x),port) for x in range(len(self.all_ports))]
            right_names=["rbl_{0}_{1}".format(self.cell.get_br_name(x),port) for x in range(len(self.all_ports))]
            # Keep track of the left pins that are the RBL
            self.rbl_bl_names[port]=left_names[self.bitcell_ports[port]]
            self.rbl_br_names[port]=right_names[self.bitcell_ports[port]]
            # Interleave the left and right lists
            bl_names = [x for t in zip(left_names, right_names) for x in t]
            self.replica_bl_names[port] = bl_names

            wl_names = ["rbl_{0}_{1}".format(x,port) for x in self.cell.get_all_wl_names()]
            #wl_names[port] = "rbl_wl{}".format(port)
            self.replica_wl_names[port] = wl_names
            

        # External pins
        self.add_pin_list(self.bitcell_array_bl_names, "INOUT")
        # Need to sort by port order since dictionary values may not be in order
        bl_names = [self.rbl_bl_names[x] for x in sorted(self.rbl_bl_names.keys())]
        br_names = [self.rbl_br_names[x] for x in sorted(self.rbl_br_names.keys())]
        for (bl_name,br_name) in zip(bl_names,br_names):
            self.add_pin(bl_name,"OUTPUT")
            self.add_pin(br_name,"OUTPUT")
        self.add_pin_list(self.bitcell_array_wl_names, "INPUT")
        # Need to sort by port order since dictionary values may not be in order        
        wl_names = [self.rbl_wl_names[x] for x in sorted(self.rbl_wl_names.keys())]
        for pin_name in wl_names:
            self.add_pin(pin_name,"INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

        
    def create_instances(self):
        """ Create the module instances used in this design """

        supplies = ["vdd", "gnd"]
        
        # Used for names/dimensions only
        self.cell = factory.create(module_type="bitcell")
        
        # Main array
        self.bitcell_array_inst=self.add_inst(name="bitcell_array",
                                              mod=self.bitcell_array)
        self.connect_inst(self.bitcell_array_bl_names + self.bitcell_array_wl_names + supplies)

        # Replica columns
        self.replica_col_inst = {}
        for port in range(self.left_rbl+self.right_rbl):
            self.replica_col_inst[port]=self.add_inst(name="replica_col_{}".format(port),
                                                     mod=self.replica_columns[port])
            self.connect_inst(self.replica_bl_names[port] + self.replica_col_wl_names + supplies)
            
            
        # Dummy rows under the bitcell array (connected with with the replica cell wl)
        self.dummy_row_replica_inst = {}
        for port in range(self.left_rbl+self.right_rbl):
            self.dummy_row_replica_inst[port]=self.add_inst(name="dummy_row_{}".format(port),
                                                            mod=self.dummy_row)
            self.connect_inst(self.dummy_row_bl_names + self.replica_wl_names[port] + supplies)
        
        
        # Top/bottom dummy rows
        self.dummy_row_bot_inst=self.add_inst(name="dummy_row_bot",
                                                 mod=self.dummy_row)
        self.connect_inst(self.dummy_row_bl_names + [x+"_bot" for x in self.dummy_cell_wl_names] + supplies)
        self.dummy_row_top_inst=self.add_inst(name="dummy_row_top",
                                                 mod=self.dummy_row)
        self.connect_inst(self.dummy_row_bl_names + [x+"_top" for x in self.dummy_cell_wl_names] + supplies)


        # Left/right Dummy columns
        self.dummy_col_left_inst=self.add_inst(name="dummy_col_left",
                                               mod=self.dummy_col)
        self.connect_inst([x+"_left" for x in self.dummy_cell_bl_names] + self.dummy_col_wl_names + supplies)
        self.dummy_col_right_inst=self.add_inst(name="dummy_col_right",
                                               mod=self.dummy_col)
        self.connect_inst([x+"_right" for x in self.dummy_cell_bl_names] + self.dummy_col_wl_names + supplies)
        

                
    def create_layout(self):

        self.height = (self.row_size+self.extra_rows)*self.dummy_row.height
        self.width = (self.column_size+self.extra_cols)*self.cell.width

        # This is a bitcell x bitcell offset to scale
        offset = vector(self.cell.width, self.cell.height)
        
        self.bitcell_array_inst.place(offset=[0,0])

        # To the left of the bitcell array
        for bit in range(self.left_rbl):
            self.replica_col_inst[bit].place(offset=offset.scale(-bit-1,-self.left_rbl-1))
        # To the right of the bitcell array
        for bit in range(self.right_rbl):
            self.replica_col_inst[self.left_rbl+bit].place(offset=offset.scale(bit,-self.left_rbl-1)+self.bitcell_array_inst.lr())
                                         

        # Far top dummy row (first row above array is NOT flipped)
        flip_dummy = self.right_rbl%2
        self.dummy_row_top_inst.place(offset=offset.scale(0,self.right_rbl+flip_dummy)+self.bitcell_array_inst.ul(),
                                         mirror="MX" if flip_dummy else "R0")
        # Far bottom dummy row (first row below array IS flipped)
        flip_dummy = (self.left_rbl+1)%2
        self.dummy_row_bot_inst.place(offset=offset.scale(0,-self.left_rbl-1+flip_dummy),
                                      mirror="MX" if flip_dummy else "R0")
        # Far left dummy col
        self.dummy_col_left_inst.place(offset=offset.scale(-self.left_rbl-1,-self.left_rbl-1))
        # Far right dummy col
        self.dummy_col_right_inst.place(offset=offset.scale(self.right_rbl,-self.left_rbl-1)+self.bitcell_array_inst.lr())

        # Replica dummy rows
        for bit in range(self.left_rbl):
            self.dummy_row_replica_inst[bit].place(offset=offset.scale(0,-bit-bit%2),
                                                   mirror="R0" if bit%2 else "MX")
        for bit in range(self.right_rbl):
            self.dummy_row_replica_inst[self.left_rbl+bit].place(offset=offset.scale(0,bit+bit%2)+self.bitcell_array_inst.ul(),
                                                                 mirror="MX" if bit%2 else "R0")
            

        self.translate_all(offset.scale(-1-self.left_rbl,-1-self.left_rbl))
        
        self.add_layout_pins()
        
        self.add_boundary()
        
        self.DRC_LVS()

                
    def add_layout_pins(self):
        """ Add the layout pins """

        # Main array wl and bl/br
        pin_names = self.bitcell_array.get_pin_names()
        for pin_name in pin_names:
            if pin_name.startswith("wl"):
                pin_list = self.bitcell_array_inst.get_pins(pin_name)
                for pin in pin_list:
                    self.add_layout_pin(text=pin_name,
                                        layer=pin.layer,
                                        offset=pin.ll().scale(0,1),
                                        width=self.width,
                                        height=pin.height())
            elif pin_name.startswith("bl") or pin_name.startswith("br"):
                pin_list = self.bitcell_array_inst.get_pins(pin_name)
                for pin in pin_list:
                    self.add_layout_pin(text=pin_name,
                                        layer=pin.layer,
                                        offset=pin.ll().scale(1,0),
                                        width=pin.width(),
                                        height=self.height)


        # Replica wordlines
        for port in range(self.left_rbl+self.right_rbl):
            inst = self.replica_col_inst[port]
            for (pin_name,wl_name) in zip(self.cell.get_all_wl_names(),self.replica_wl_names[port]):
                # +1 for dummy row
                pin_bit = port+1
                # +row_size if above the array 
                if port>=self.left_rbl:
                    pin_bit += self.row_size
                    
                pin_name += "_{}".format(pin_bit)
                pin = inst.get_pin(pin_name)
                if wl_name in self.rbl_wl_names.values():
                    self.add_layout_pin(text=wl_name,
                                        layer=pin.layer,
                                        offset=pin.ll().scale(0,1),
                                        width=self.width,
                                        height=pin.height())


        # Replica bitlines
        for port in range(self.left_rbl+self.right_rbl):
            inst = self.replica_col_inst[port]
            for (pin_name, bl_name) in zip(self.cell.get_all_bitline_names(),self.replica_bl_names[port]):
                pin = inst.get_pin(pin_name)
                if bl_name in self.rbl_bl_names or bl_name in self.rbl_br_names:
                    name = bl_name
                else:
                    name = "rbl_{0}_{1}".format(pin_name,port)
                self.add_layout_pin(text=name,
                                    layer=pin.layer,
                                    offset=pin.ll().scale(1,0),
                                    width=pin.width(),
                                    height=self.height)

                    
        for pin_name in ["vdd","gnd"]:
            for inst in self.insts:
                pin_list = inst.get_pins(pin_name)
                for pin in pin_list:
                    self.add_power_pin(name=pin_name, loc=pin.center(), vertical=True, start_layer=pin.layer)



                        
    def get_rbl_wl_name(self, port):
        """ Return the WL for the given RBL port """
        return self.rbl_wl_names[port]
    
    def get_rbl_bl_name(self, port):
        """ Return the BL for the given RBL port """
        return self.rbl_bl_names[port]

    def get_rbl_br_name(self, port):
        """ Return the BR for the given RBL port """
        return self.rbl_br_names[port]

    def analytical_power(self, corner, load):
        """Power of Bitcell array and bitline in nW."""
        from tech import drc, parameter
        
        # Dynamic Power from Bitline
        bl_wire = self.gen_bl_wire()
        cell_load = 2 * bl_wire.return_input_cap() 
        bl_swing = OPTS.rbl_delay_percentage
        freq = spice["default_event_rate"]
        bitline_dynamic = self.calc_dynamic_power(corner, cell_load, freq, swing=bl_swing)
        
        #Calculate the bitcell power which currently only includes leakage 
        cell_power = self.cell.analytical_power(corner, load)
        
        #Leakage power grows with entire array and bitlines.
        total_power = self.return_power(cell_power.dynamic + bitline_dynamic * self.column_size,
                                        cell_power.leakage * self.column_size * self.row_size)
        return total_power

    def gen_bl_wire(self):
        if OPTS.netlist_only:
            height = 0
        else:
            height = self.height
        bl_pos = 0
        bl_wire = self.generate_rc_net(int(self.row_size-bl_pos), height, drc("minwidth_metal1"))
        bl_wire.wire_c =spice["min_tx_drain_c"] + bl_wire.wire_c # 1 access tx d/s per cell
        return bl_wire

    def get_wordline_cin(self):
        """Get the relative input capacitance from the wordline connections in all the bitcell"""
        #A single wordline is connected to all the bitcells in a single row meaning the capacitance depends on the # of columns
        bitcell_wl_cin = self.cell.get_wl_cin()
        total_cin = bitcell_wl_cin * self.column_size
        return total_cin

    def graph_exclude_bits(self, targ_row, targ_col):
        """Excludes bits in column from being added to graph except target"""
        self.bitcell_array.graph_exclude_bits(targ_row, targ_col)
    
    def graph_exclude_replica_col_bits(self):
        """Exclude all replica/dummy cells in the replica columns except the replica bit."""
           
        for port in range(self.left_rbl+self.right_rbl):
            self.replica_columns[port].exclude_all_but_replica()

    def get_cell_name(self, inst_name, row, col):
        """Gets the spice name of the target bitcell."""
        return self.bitcell_array.get_cell_name(inst_name+'.x'+self.bitcell_array_inst.name, row, col)        
