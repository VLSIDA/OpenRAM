# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import sys
from tech import drc, spice
import debug
from math import log,sqrt,ceil
import datetime
import getpass
import numpy as np
from vector import vector
from globals import OPTS, print_time

from sram_base import sram_base
from bank import bank
from contact import m2m3
from dff_buf_array import dff_buf_array
from dff_array import dff_array


class sram_1bank(sram_base):
    """
    Procedures specific to a one bank SRAM.
    """
    def __init__(self, name, sram_config):
        sram_base.__init__(self, name, sram_config)
            
    def create_modules(self):
        """ 
        This adds the modules for a single bank SRAM with control
        logic. 
        """
        
        self.bank_inst=self.create_bank(0)

        self.control_logic_insts = self.create_control_logic()

        self.row_addr_dff_insts = self.create_row_addr_dff()

        if self.col_addr_dff:
            self.col_addr_dff_insts = self.create_col_addr_dff()

        if self.write_size:
            self.wmask_dff_insts = self.create_wmask_dff()
            self.data_dff_insts = self.create_data_dff()
        else:
            self.data_dff_insts = self.create_data_dff()

    def place_instances(self):
        """ 
        This places the instances for a single bank SRAM with control
        logic and up to 2 ports.
        """
        
        # No orientation or offset
        self.place_bank(self.bank_inst, [0, 0], 1, 1)

        # The control logic is placed such that the vertical center (between the delay/RBL and
        # the actual control logic is aligned with the vertical center of the bank (between
        # the sense amps/column mux and cell array)
        # The x-coordinate is placed to allow a single clock wire (plus an extra pitch)
        # up to the row address DFFs.
        control_pos = [None]*len(self.all_ports)
        row_addr_pos = [None]*len(self.all_ports)
        col_addr_pos = [None]*len(self.all_ports)
        wmask_pos = [None]*len(self.all_ports)
        data_pos = [None]*len(self.all_ports)

        # This is M2 pitch even though it is on M1 to help stem via spacings on the trunk
        # The M1 pitch is for supply rail spacings
        max_gap_size = self.m2_pitch*max(self.word_size+1,self.col_addr_size+1) + 2*self.m1_pitch
        
        # Port 0
        port = 0

        if self.write_size:
            if port in self.write_ports:
                # Add the write mask flops below the write mask AND array.
                wmask_pos[port] = vector(self.bank.bank_array_ll.x,
                                         -0.5*max_gap_size - self.dff.height)
                self.wmask_dff_insts[port].place(wmask_pos[port])

                # Add the data flops below the write mask flops.
                data_pos[port] = vector(self.bank.bank_array_ll.x,
                                        -1.5*max_gap_size - 2*self.dff.height)
                self.data_dff_insts[port].place(data_pos[port])
            else:
                wmask_pos[port] = vector(self.bank.bank_array_ll.x, 0)
                data_pos[port] = vector(self.bank.bank_array_ll.x,0)

        else:
            # Add the data flops below the bank to the right of the lower-left of bank array
            # This relies on the lower-left of the array of the bank
            # decoder in upper left, bank in upper right, sensing in lower right.
            # These flops go below the sensing and leave a gap to channel route to the
            # sense amps.
            if port in self.write_ports:
                data_pos[port] = vector(self.bank.bank_array_ll.x,
                                        -max_gap_size - self.dff.height)
                self.data_dff_insts[port].place(data_pos[port])

            else:
                data_pos[port] = vector(self.bank.bank_array_ll.x,0)

        # Add the col address flops below the bank to the left of the lower-left of bank array
        if self.col_addr_dff:
            col_addr_pos[port] = vector(self.bank.bank_array_ll.x - self.col_addr_dff_insts[port].width - self.bank.m2_gap,
                                        -max_gap_size - self.col_addr_dff_insts[port].height)
            self.col_addr_dff_insts[port].place(col_addr_pos[port])
        else:
            col_addr_pos[port] = vector(self.bank.bank_array_ll.x,0)
            
        # This includes 2 M2 pitches for the row addr clock line.
        control_pos[port] = vector(-self.control_logic_insts[port].width - 2*self.m2_pitch,
                                   self.bank.bank_array_ll.y - self.control_logic_insts[port].mod.control_logic_center.y - 2*self.bank.m2_gap )
        self.control_logic_insts[port].place(control_pos[port])
        
        # The row address bits are placed above the control logic aligned on the right.
        x_offset = self.control_logic_insts[port].rx() - self.row_addr_dff_insts[port].width
        # It is above the control logic but below the top of the bitcell array
        y_offset = max(self.control_logic_insts[port].uy(), self.bank_inst.uy() - self.row_addr_dff_insts[port].height)
        row_addr_pos[port] = vector(x_offset, y_offset)
        self.row_addr_dff_insts[port].place(row_addr_pos[port])
        
        # Add the col address flops below the bank to the left of the lower-left of bank array
        if self.col_addr_dff:
            col_addr_pos[port] = vector(self.bank.bank_array_ll.x - self.col_addr_dff_insts[port].width - self.bank.m2_gap,
                                        -max_gap_size - self.col_addr_dff_insts[port].height)
            self.col_addr_dff_insts[port].place(col_addr_pos[port])


        if len(self.all_ports)>1:
            # Port 1
            port = 1

            if port in self.write_ports:
                if self.write_size:
                    # Add the write mask flops below the write mask AND array.
                    wmask_pos[port] = vector(self.bank.bank_array_ur.x - self.data_dff_insts[port].width,
                                             self.bank.height + 0.5*max_gap_size + self.dff.height)
                    self.wmask_dff_insts[port].place(wmask_pos[port], mirror="MX")

                    # Add the data flops below the write mask flops
                    data_pos[port] = vector(self.bank.bank_array_ur.x - self.data_dff_insts[port].width,
                                            self.bank.height + 1.5*max_gap_size + 2*self.dff.height)
                    self.data_dff_insts[port].place(data_pos[port], mirror="MX")

                else:
                    # Add the data flops above the bank to the left of the upper-right of bank array
                    # This relies on the upper-right of the array of the bank
                    # decoder in upper left, bank in upper right, sensing in lower right.
                    # These flops go below the sensing and leave a gap to channel route to the
                    # sense amps.
                    data_pos[port] = vector(self.bank.bank_array_ur.x - self.data_dff_insts[port].width,
                                            self.bank.height + max_gap_size + self.dff.height)
                    self.data_dff_insts[port].place(data_pos[port], mirror="MX")

            # Add the col address flops above the bank to the right of the upper-right of bank array
            if self.col_addr_dff:
                col_addr_pos[port] = vector(self.bank.bank_array_ur.x + self.bank.m2_gap,
                                            self.bank.height + max_gap_size + self.dff.height)
                self.col_addr_dff_insts[port].place(col_addr_pos[port], mirror="MX")
            else:
                col_addr_pos[port] = self.bank_inst.ur()
        
            # This includes 2 M2 pitches for the row addr clock line
            control_pos[port] = vector(self.bank_inst.rx() + self.control_logic_insts[port].width + 2*self.m2_pitch,
                                       self.bank.bank_array_ur.y + self.control_logic_insts[port].height -
                                       (self.control_logic_insts[port].height - self.control_logic_insts[port].mod.control_logic_center.y)
                                       + 2*self.bank.m2_gap)
            #import pdb; pdb.set_trace()
            self.control_logic_insts[port].place(control_pos[port], mirror="XY")
        
            # The row address bits are placed above the control logic aligned on the left.
            x_offset = control_pos[port].x - self.control_logic_insts[port].width + self.row_addr_dff_insts[port].width
            # It is below the control logic but below the bottom of the bitcell array
            y_offset = min(self.control_logic_insts[port].by(), self.bank_inst.by() + self.row_addr_dff_insts[port].height)
            row_addr_pos[port] = vector(x_offset, y_offset)
            self.row_addr_dff_insts[port].place(row_addr_pos[port], mirror="XY")


    def add_layout_pins(self):
        """
        Add the top-level pins for a single bank SRAM with control.
        """
        for port in self.all_ports:
            # Connect the control pins as inputs
            for signal in self.control_logic_inputs[port] + ["clk"]:
                self.copy_layout_pin(self.control_logic_insts[port], signal, signal+"{}".format(port))

            if port in self.read_ports:
                for bit in range(self.word_size):
                    self.copy_layout_pin(self.bank_inst, "dout{0}_{1}".format(port,bit), "dout{0}[{1}]".format(port,bit))

            # Lower address bits
            for bit in range(self.col_addr_size):
                self.copy_layout_pin(self.col_addr_dff_insts[port], "din_{}".format(bit),"addr{0}[{1}]".format(port,bit))
            # Upper address bits
            for bit in range(self.row_addr_size):
                self.copy_layout_pin(self.row_addr_dff_insts[port], "din_{}".format(bit),"addr{0}[{1}]".format(port,bit+self.col_addr_size))

            if port in self.write_ports:
                for bit in range(self.word_size):
                    self.copy_layout_pin(self.data_dff_insts[port], "din_{}".format(bit), "din{0}[{1}]".format(port,bit))
                    
                if self.write_size:
                    for bit in range(self.num_wmasks):
                        self.copy_layout_pin(self.wmask_dff_insts[port], "din_{}".format(bit), "wmask{0}[{1}]".format(port,bit))

            
    def route_layout(self):
        """ Route a single bank SRAM """

        self.add_layout_pins()

        self.route_clk()
        
        self.route_control_logic()
        
        self.route_row_addr_dff()

        if self.col_addr_dff:
            self.route_col_addr_dff()
        
        self.route_data_dff()
        
        if self.write_size:
            self.route_wmask_dff()

    def route_clk(self):
        """ Route the clock network """

        # This is the actual input to the SRAM
        for port in self.all_ports:
            self.copy_layout_pin(self.control_logic_insts[port], "clk", "clk{}".format(port))

            # Connect all of these clock pins to the clock in the central bus
            # This is something like a "spine" clock distribution. The two spines
            # are clk_buf and clk_buf_bar
            control_clk_buf_pin = self.control_logic_insts[port].get_pin("clk_buf")
            control_clk_buf_pos = control_clk_buf_pin.center()
            
            # This uses a metal2 track to the right (for port0) of the control/row addr DFF
            # to route vertically. For port1, it is to the left.
            row_addr_clk_pin = self.row_addr_dff_insts[port].get_pin("clk")
            if port%2:
                control_clk_buf_pos = control_clk_buf_pin.lc()
                row_addr_clk_pos = row_addr_clk_pin.lc()
                mid1_pos = vector(self.row_addr_dff_insts[port].lx() - self.m2_pitch,
                                  row_addr_clk_pos.y)
            else:
                control_clk_buf_pos = control_clk_buf_pin.rc()
                row_addr_clk_pos = row_addr_clk_pin.rc()
                mid1_pos = vector(self.row_addr_dff_insts[port].rx() + self.m2_pitch,
                                  row_addr_clk_pos.y)

            # This is the steiner point where the net branches out
            clk_steiner_pos = vector(mid1_pos.x, control_clk_buf_pos.y)
            self.add_path("metal1", [control_clk_buf_pos, clk_steiner_pos])
            self.add_via_center(layers=("metal1","via1","metal2"),
                                offset=clk_steiner_pos)
            
            # Note, the via to the control logic is taken care of above
            self.add_wire(("metal3","via2","metal2"),[row_addr_clk_pos, mid1_pos, clk_steiner_pos])
        
            if self.col_addr_dff:
                dff_clk_pin = self.col_addr_dff_insts[port].get_pin("clk")
                dff_clk_pos = dff_clk_pin.center()
                mid_pos = vector(clk_steiner_pos.x, dff_clk_pos.y)
                self.add_wire(("metal3","via2","metal2"),[dff_clk_pos, mid_pos, clk_steiner_pos])

            if port in self.write_ports:
                data_dff_clk_pin = self.data_dff_insts[port].get_pin("clk")
                data_dff_clk_pos = data_dff_clk_pin.center()
                mid_pos = vector(clk_steiner_pos.x, data_dff_clk_pos.y)
                # In some designs, the steiner via will be too close to the mid_pos via
                # so make the wire as wide as the contacts
                self.add_path("metal2",[mid_pos, clk_steiner_pos], width=max(m2m3.width,m2m3.height))
                self.add_wire(("metal3","via2","metal2"),[data_dff_clk_pos, mid_pos, clk_steiner_pos])

                if self.write_size:
                    wmask_dff_clk_pin = self.wmask_dff_insts[port].get_pin("clk")
                    wmask_dff_clk_pos = wmask_dff_clk_pin.center()
                    mid_pos = vector(clk_steiner_pos.x, wmask_dff_clk_pos.y)
                    # In some designs, the steiner via will be too close to the mid_pos via
                    # so make the wire as wide as the contacts
                    self.add_path("metal2", [mid_pos, clk_steiner_pos], width=max(m2m3.width, m2m3.height))
                    self.add_wire(("metal3", "via2", "metal2"), [wmask_dff_clk_pos, mid_pos, clk_steiner_pos])

            
    def route_control_logic(self):
        """ Route the control logic pins that are not inputs """

        for port in self.all_ports:
            for signal in self.control_logic_outputs[port]:
                # The clock gets routed separately and is not a part of the bank
                if "clk" in signal:
                    continue
                src_pin = self.control_logic_insts[port].get_pin(signal)
                dest_pin = self.bank_inst.get_pin(signal+"{}".format(port))                
                self.connect_vbus_m2m3(src_pin, dest_pin)

        for port in self.all_ports:
            # Only input (besides pins) is the replica bitline
            src_pin = self.control_logic_insts[port].get_pin("rbl_bl")
            dest_pin = self.bank_inst.get_pin("rbl_bl{}".format(port))                
            self.connect_vbus_m2m3(src_pin, dest_pin)
        

    def route_row_addr_dff(self):
        """ Connect the output of the row flops to the bank pins """
        for port in self.all_ports:
            for bit in range(self.row_addr_size):
                flop_name = "dout_{}".format(bit)
                bank_name = "addr{0}_{1}".format(port,bit+self.col_addr_size)
                flop_pin = self.row_addr_dff_insts[port].get_pin(flop_name)
                bank_pin = self.bank_inst.get_pin(bank_name)
                flop_pos = flop_pin.center()
                bank_pos = bank_pin.center()
                mid_pos = vector(bank_pos.x,flop_pos.y)
                self.add_wire(("metal3","via2","metal2"),[flop_pos, mid_pos,bank_pos])
                self.add_via_center(layers=("metal2","via2","metal3"),
                                    offset=flop_pos)

    def route_col_addr_dff(self):
        """ Connect the output of the row flops to the bank pins """
        for port in self.all_ports:
            if port%2:
                offset = self.col_addr_dff_insts[port].ll() - vector(0, (self.word_size+2)*self.m1_pitch) 
            else:
                offset = self.col_addr_dff_insts[port].ul() + vector(0, 2*self.m1_pitch)

            bus_names = ["addr_{}".format(x) for x in range(self.col_addr_size)]        
            col_addr_bus_offsets = self.create_horizontal_bus(layer="metal1",
                                                              pitch=self.m1_pitch,
                                                              offset=offset,
                                                              names=bus_names,
                                                              length=self.col_addr_dff_insts[port].width)

            dff_names = ["dout_{}".format(x) for x in range(self.col_addr_size)]
            data_dff_map = zip(dff_names, bus_names)
            self.connect_horizontal_bus(data_dff_map, self.col_addr_dff_insts[port], col_addr_bus_offsets)
            
            bank_names = ["addr{0}_{1}".format(port,x) for x in range(self.col_addr_size)]
            data_bank_map = zip(bank_names, bus_names)
            self.connect_horizontal_bus(data_bank_map, self.bank_inst, col_addr_bus_offsets)
        

    def route_data_dff(self):
        """ Connect the output of the data flops to the write driver """
        # This is where the channel will start (y-dimension at least)
        for port in self.write_ports:
            if port%2:
                offset = self.data_dff_insts[port].ll() - vector(0, (self.word_size+2)*self.m1_pitch) 
            else:
                offset = self.data_dff_insts[port].ul() + vector(0, 2*self.m1_pitch)


            dff_names = ["dout_{}".format(x) for x in range(self.word_size)]
            dff_pins = [self.data_dff_insts[port].get_pin(x) for x in dff_names]
            if self.write_size:
                for x in dff_names:
                    pin_offset = self.data_dff_insts[port].get_pin(x).center()
                    self.add_via_center(layers=("metal1", "via1", "metal2"),
                                        offset=pin_offset,
                                        directions = ("V", "V"))
                    self.add_via_center(layers=("metal2", "via2", "metal3"),
                                        offset=pin_offset)
                    self.add_via_center(layers=("metal3", "via3", "metal4"),
                                        offset=pin_offset)
            
            bank_names = ["din{0}_{1}".format(port,x) for x in range(self.word_size)]
            bank_pins = [self.bank_inst.get_pin(x) for x in bank_names]
            if self.write_size:
                for x in bank_names:
                    pin_offset = self.bank_inst.get_pin(x).bc()
                    self.add_via_center(layers=("metal1", "via1", "metal2"),
                                        offset=pin_offset)
                    self.add_via_center(layers=("metal2", "via2", "metal3"),
                                        offset=pin_offset)
                    self.add_via_center(layers=("metal3", "via3", "metal4"),
                                        offset=pin_offset)

            route_map = list(zip(bank_pins, dff_pins))
            if self.write_size:
                self.create_horizontal_channel_route(netlist=route_map,
                                                     offset=offset,
                                                     layer_stack=("metal3", "via3", "metal4"))
            else:
                self.create_horizontal_channel_route(route_map, offset)

    def route_wmask_dff(self):
        """ Connect the output of the wmask flops to the write mask AND array """
        # This is where the channel will start (y-dimension at least)
        for port in self.write_ports:
            if port % 2:
                offset = self.wmask_dff_insts[port].ll() - vector(0, (self.word_size + 2) * self.m1_pitch)
            else:
                offset = self.wmask_dff_insts[port].ul() + vector(0, 2 * self.m1_pitch)

            dff_names = ["dout_{}".format(x) for x in range(self.num_wmasks)]
            dff_pins = [self.wmask_dff_insts[port].get_pin(x) for x in dff_names]
            for x in dff_names:
                offset_pin = self.wmask_dff_insts[port].get_pin(x).center()
                self.add_via_center(layers=("metal1", "via1", "metal2"),
                                    offset=offset_pin,
                                    directions=("V", "V"))

            bank_names = ["bank_wmask{0}_{1}".format(port, x) for x in range(self.num_wmasks)]
            bank_pins = [self.bank_inst.get_pin(x) for x in bank_names]
            for x in bank_names:
                offset_pin = self.bank_inst.get_pin(x).center()
                self.add_via_center(layers=("metal1", "via1", "metal2"),
                                    offset=offset_pin)


            route_map = list(zip(bank_pins, dff_pins))
            self.create_horizontal_channel_route(route_map,offset)


    def add_lvs_correspondence_points(self):
        """ 
        This adds some points for easier debugging if LVS goes wrong. 
        These should probably be turned off by default though, since extraction
        will show these as ports in the extracted netlist.
        """
        
        for n in self.control_logic_outputs[0]:
            pin = self.control_logic_insts[0].get_pin(n)
            self.add_label(text=n,
                           layer=pin.layer,
                           offset=pin.center())
                           
    def graph_exclude_data_dff(self):
        """Removes data dff and wmask dff (if applicable) from search graph. """
        #Data dffs and wmask dffs are only for writing so are not useful for evaluating read delay.
        for inst in self.data_dff_insts:
            self.graph_inst_exclude.add(inst)
        if self.write_size:
            for inst in self.wmask_dff_insts:
                self.graph_inst_exclude.add(inst)
    
    def graph_exclude_addr_dff(self):
        """Removes data dff from search graph. """
        #Address is considered not part of the critical path, subjectively removed
        for inst in self.row_addr_dff_insts:
            self.graph_inst_exclude.add(inst)
            
        if self.col_addr_dff:
            for inst in self.col_addr_dff_insts:
                self.graph_inst_exclude.add(inst)

    def graph_exclude_ctrl_dffs(self):
        """Exclude dffs for CSB, WEB, etc from graph"""
        #Insts located in control logic, exclusion function called here
        for inst in self.control_logic_insts:
            inst.mod.graph_exclude_dffs()
            
    def get_sen_name(self, sram_name, port=0):
        """Returns the s_en spice name."""
        #Naming scheme is hardcoded using this function, should be built into the 
        #graph in someway.
        sen_name = "s_en{}".format(port)
        control_conns = self.get_conns(self.control_logic_insts[port])
        #Sanity checks
        if sen_name not in control_conns:
            debug.error("Signal={} not contained in control logic connections={}"\
                                                 .format(sen_name, control_conns))
        if sen_name in self.pins:
            debug.error("Internal signal={} contained in port list. Name defined by the parent.")                
        return "X{}.{}".format(sram_name, sen_name)
        
    def get_cell_name(self, inst_name, row, col):
        """Gets the spice name of the target bitcell."""
        #Sanity check in case it was forgotten
        if inst_name.find('x') != 0:
            inst_name = 'x'+inst_name
        return self.bank_inst.mod.get_cell_name(inst_name+'.x'+self.bank_inst.name, row, col)
