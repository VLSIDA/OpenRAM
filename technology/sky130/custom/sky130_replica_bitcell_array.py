#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from math import sqrt
from openram import debug
from openram.base import vector
from openram.base import round_to_grid
from openram.tech import drc
from openram.tech import array_row_multiple
from openram.tech import array_col_multiple
from openram import OPTS
from .replica_bitcell_array import replica_bitcell_array
from .sky130_bitcell_base_array import sky130_bitcell_base_array


class sky130_replica_bitcell_array(replica_bitcell_array, sky130_bitcell_base_array):
    """
    Creates a bitcell arrow of cols x rows and then adds the replica
    and dummy columns and rows.  Replica columns are on the left and
    right, respectively and connected to the given bitcell ports.
    Dummy are the outside columns/rows with WL and BL tied to gnd.
    Requires a regular bitcell array, replica bitcell, and dummy
    bitcell (Bl/BR disconnected).
    """
    def __init__(self, rows, cols, rbl=None, left_rbl=None, right_rbl=None, name=""):
        total_ports = OPTS.num_rw_ports + OPTS.num_w_ports + OPTS.num_r_ports
        self.all_ports = list(range(total_ports))

        self.column_size = cols
        self.row_size = rows

        # This is how many RBLs are in all the arrays
        if rbl:
            self.rbl = rbl
        else:
            self.rbl=[1, 1 if len(self.all_ports)>1 else 0]
        # This specifies which RBL to put on the left or right
        # by port number
        # This could be an empty list
        if left_rbl != None:
            self.left_rbl = left_rbl
        else:
            self.left_rbl = [0]
        # This could be an empty list
        if right_rbl != None:
            self.right_rbl = right_rbl
        else:
            self.right_rbl=[1] if len(self.all_ports) > 1 else []
        self.rbls = self.left_rbl + self.right_rbl

        if ((self.column_size + self.rbl[0] + self.rbl[1]) % array_col_multiple != 0):
            debug.error("Invalid number of cols including rbl(s): {}. Total cols must be divisible by {}".format(self.column_size + self.rbl[0] + self.rbl[1], array_col_multiple), -1)

        if ((self.row_size + self.rbl[0] + self.rbl[1]) % array_row_multiple != 0):
            debug.error("invalid number of rows including dummy row(s): {}. Total cols must be divisible by {}".format(self.row_size + self.rbl[0] + self.rbl[1], array_row_multiple), -15)

        super().__init__(self.row_size, self.column_size, rbl, left_rbl, right_rbl, name)

    def create_layout(self):
        # We will need unused wordlines grounded, so we need to know their layer
        # and create a space on the left and right for the vias to connect to ground
        pin = self.cell.get_pin(self.cell.get_all_wl_names()[0])
        pin_layer = pin.layer
        self.unused_pitch = 1.5 * getattr(self, "{}_pitch".format(pin_layer))
        self.unused_offset = vector(self.unused_pitch, 0)

        # This is a bitcell x bitcell offset to scale
        self.bitcell_offset = vector(self.cell.width, self.cell.height)
        self.strap_offset = vector(self.replica_col_insts[0].mod.strap1.width, self.replica_col_insts[0].mod.strap1.height)
        self.col_end_offset = vector(self.dummy_row_insts[0].mod.colend1.width, self.dummy_row_insts[0].mod.colend1.height)
        self.row_end_offset = vector(self.dummy_col_insts[0].mod.rowend1.width, self.dummy_col_insts[0].mod.rowend1.height)

        # Everything is computed with the main array at (self.unused_pitch, 0) to start
        self.bitcell_array_inst.place(offset=self.unused_offset)

        self.add_replica_columns()

        self.add_end_caps()

        # Array was at (0, 0) but move everything so it is at the lower left
        self.offset_all_coordinates()

        # Add extra width on the left and right for the unused WLs
        #self.width = self.dummy_col_insts[0].rx() + self.unused_offset[0]
        self.width = self.dummy_col_insts[1].rx()
        self.height = self.dummy_col_insts[0].uy()

        self.add_layout_pins()

        self.route_unused_wordlines()

        self.add_boundary()

        self.DRC_LVS()

    def add_pins(self):
        super().add_pins()

    def add_replica_columns(self):
        """ Add replica columns on left and right of array """

        # Grow from left to right, toward the array
        for bit, port in enumerate(self.left_rbl):
            offset = self.bitcell_array_inst.ll() \
                     - vector(0, self.col_cap_bottom.height) \
                     - vector(0, self.dummy_row.height) \
                     - vector(self.replica_columns[0].width, 0)
            self.replica_col_insts[bit].place(offset + vector(0, self.replica_col_insts[bit].height), mirror="MX")

        # Grow to the right of the bitcell array, array outward
        for bit, port in enumerate(self.right_rbl):
            offset = self.bitcell_array_inst.lr() \
                     + self.bitcell_offset.scale(bit, -self.rbl[0] - (self.col_end_offset.y / self.cell.height)) \
                     + self.strap_offset.scale(bit, -self.rbl[0] - 1)
            self.replica_col_insts[self.rbl[0] + bit].place(offset)

        # Replica dummy rows
        # Add the dummy rows even if we aren't adding the replica column to this bitcell array
        # These grow up, toward the array
        for bit in range(self.rbl[0]):
            dummy_offset = self.bitcell_offset.scale(0, -self.rbl[0] + bit + (-self.rbl[0] + bit) % 2) + self.unused_offset
            self.dummy_row_replica_insts[bit].place(offset=dummy_offset,
                                                    mirror="MX" if (-self.rbl[0] + bit) % 2 else "R0")
        # These grow up, away from the array
        for bit in range(self.rbl[1]):
            dummy_offset = self.bitcell_offset.scale(0, bit + bit % 2) + self.bitcell_array_inst.ul()
            self.dummy_row_replica_insts[self.rbl[0] + bit].place(offset=dummy_offset,
                                                                  mirror="MX" if bit % 2 else "R0")

    def add_end_caps(self):
        """ Add dummy cells or end caps around the array """

        dummy_row_offset = self.bitcell_offset.scale(0, self.rbl[1]) + self.bitcell_array_inst.ul()
        self.dummy_row_insts[1].place(offset=dummy_row_offset)

        dummy_row_offset = self.bitcell_offset.scale(0, -self.rbl[0] - (self.col_end_offset.y / self.cell.height)) + self.unused_offset
        self.dummy_row_insts[0].place(offset=dummy_row_offset + vector(0, self.dummy_row_insts[0].height), mirror="MX")

        # Far left dummy col
        # Shifted down by the number of left RBLs even if we aren't adding replica column to this bitcell array
        dummy_col_offset = self.bitcell_offset.scale(len(self.right_rbl) * (1 + self.strap_offset.x / self.cell.width), -self.rbl[0] - (self.col_end_offset.y / self.cell.height)) - vector(self.replica_col_insts[0].width, 0) + self.unused_offset
        self.dummy_col_insts[0].place(offset=dummy_col_offset, mirror="MY")

        # Far right dummy col
        # Shifted down by the number of left RBLs even if we aren't adding replica column to this bitcell array
        dummy_col_offset = self.bitcell_offset.scale(len(self.right_rbl) * (1 + self.strap_offset.x / self.cell.width), -self.rbl[0] - (self.col_end_offset.y / self.cell.height)) + self.bitcell_array_inst.lr()
        self.dummy_col_insts[1].place(offset=dummy_col_offset)

    def route_unused_wordlines(self):
        """ Connect the unused RBL and dummy wordlines to gnd """
        return
        # This grounds all the dummy row word lines
        for inst in self.dummy_row_insts:
            for wl_name in self.col_cap.get_wordline_names():
                self.ground_pin(inst, wl_name)

        # Ground the unused replica wordlines
        for (names, inst) in zip(self.rbl_wordline_names, self.dummy_row_replica_insts):
            for (wl_name, pin_name) in zip(names, self.dummy_row.get_wordline_names()):
                if wl_name in self.gnd_wordline_names:
                    self.ground_pin(inst, pin_name)

    def add_layout_pins(self):
        """ Add the layout pins """

        for row_end in self.dummy_col_insts:
            row_end = row_end.mod
            for (rba_wl_name, wl_name) in zip(self.get_all_wordline_names(), row_end.get_wordline_names()):
                pin = row_end.get_pin(wl_name)
                self.add_layout_pin(text=rba_wl_name,
                    layer=pin.layer,
                    offset=vector(0,pin.ll().scale(0, 1)[1]),
                    #width=self.width,
                    width=pin.width(),
                    height=pin.height())

        pin_height = (round_to_grid(drc["minarea_m3"] / round_to_grid(sqrt(drc["minarea_m3"]))) + drc["{0}_to_{0}".format('m3')])
        drc_width = drc["{0}_to_{0}".format('m3')]

        # vdd/gnd are only connected in the perimeter cells
        # replica column should only have a vdd/gnd in the dummy cell on top/bottom
        supply_insts = self.dummy_row_insts + self.replica_col_insts

        for pin_name in self.supplies:
            for supply_inst in supply_insts:
                vdd_alternate = 0
                gnd_alternate = 0
                for cell_inst in supply_inst.mod.insts:
                    inst = cell_inst.mod
                    for pin in inst.get_pins(pin_name):
                        if pin.name == 'vdd':
                            if vdd_alternate:
                                connection_offset = 0.035
                                vdd_alternate = 0
                            else:
                                connection_offset = -0.035
                                vdd_alternate = 1
                            connection_width = drc["minwidth_{}".format('m1')]
                            track_offset = 1
                        elif pin.name == 'gnd':
                            if gnd_alternate:
                                connection_offset = 0.035
                                gnd_alternate = 0
                            else:
                                connection_offset = -0.035
                                gnd_alternate = 1
                            connection_width = drc["minwidth_{}".format('m1')]
                            track_offset = 4
                        pin_width = round_to_grid(sqrt(drc["minarea_m3"]))
                        pin_height = round_to_grid(drc["minarea_m3"] / pin_width)
                        if inst.cell_name == 'sky130_fd_bd_sram__sram_sp_colend_p_cent' or inst.cell_name == 'sky130_fd_bd_sram__sram_sp_colenda_p_cent' or inst.cell_name == 'sky130_fd_bd_sram__sram_sp_colend_cent' or inst.cell_name == 'sky130_fd_bd_sram__sram_sp_colenda_cent' or 'corner' in inst.cell_name:
                            if 'dummy_row' in supply_inst.name and supply_inst.mirror == 'MX':
                                pin_center = vector(pin.center()[0], -1 * track_offset * (pin_height + drc_width*2))
                                self.add_segment_center(pin.layer, pin_center+supply_inst.ll()+cell_inst.ll()+vector(connection_offset,0), vector((pin_center+supply_inst.ll()+cell_inst.ll())[0] + connection_offset, 0), connection_width)
                            elif 'dummy_row' in supply_inst.name:
                                pin_center = vector(pin.center()[0],inst.height + 1 * track_offset* (pin_height + drc_width*2))
                                self.add_segment_center(pin.layer, pin_center+supply_inst.ll()+cell_inst.ll()+vector(connection_offset,0), vector((pin_center+supply_inst.ll()+cell_inst.ll())[0] + connection_offset, self.height), connection_width)
                            elif 'replica_col' in supply_inst.name and cell_inst.mirror == 'MX':
                                pin_center = vector(pin.center()[0], -1 * track_offset* (pin_height + drc_width*2))
                                self.add_segment_center(pin.layer, pin_center+supply_inst.ll()+cell_inst.ll()+vector(connection_offset,0), vector((pin_center+supply_inst.ll()+cell_inst.ll())[0] + connection_offset, 0), connection_width)
                            elif 'replica_col' in supply_inst.name:
                                pin_center = vector(pin.center()[0],inst.height + 1 * track_offset * (pin_height + drc_width*2))
                                self.add_segment_center(pin.layer, pin_center+supply_inst.ll()+cell_inst.ll()+vector(connection_offset,0), vector((pin_center+supply_inst.ll()+cell_inst.ll())[0] + connection_offset,self.height), connection_width)
                            self.add_via_stack_center(from_layer=pin.layer,
                                            to_layer='m2',
                                            offset=pin_center+supply_inst.ll()+cell_inst.ll() + vector(connection_offset,0))


        # add well contacts to perimeter cells
        for pin_name in ['vpb', 'vnb']:
            for supply_inst in supply_insts:
                vnb_alternate = 0
                vpb_alternate = 0
                for cell_inst in supply_inst.mod.insts:

                    inst = cell_inst.mod
                    for pin in inst.get_pins(pin_name):
                        if pin.name == 'vpb':
                            if vpb_alternate:
                                connection_offset = 0.01
                                vpb_alternate = 0
                            else:
                                connection_offset = 0.02
                                vpb_alternate = 1
                            connection_width = drc["minwidth_{}".format('m1')]
                            track_offset = 2
                        elif pin.name == 'vnb':
                            if vnb_alternate:
                                connection_offset = -0.01
                                vnb_alternate = 0
                            else:
                                connection_offset = -0.02
                                vnb_alternate = 1
                            connection_width = drc["minwidth_{}".format('m1')]
                            track_offset = 3
                        if inst.cell_name == 'sky130_fd_bd_sram__sram_sp_colend_p_cent' or inst.cell_name == 'sky130_fd_bd_sram__sram_sp_colenda_p_cent' or inst.cell_name == 'sky130_fd_bd_sram__sram_sp_colend_cent' or inst.cell_name == 'sky130_fd_bd_sram__sram_sp_colenda_cent':
                            if 'dummy_row' in supply_inst.name and supply_inst.mirror == 'MX':
                                pin_center = vector(pin.center()[0], -1 * track_offset * (pin_height + drc_width*2))
                                self.add_segment_center(pin.layer, pin_center+supply_inst.ll()+cell_inst.ll()+vector(connection_offset,0), vector((pin_center+supply_inst.ll()+cell_inst.ll())[0] + connection_offset, 0), connection_width)
                            elif 'dummy_row' in supply_inst.name:
                                pin_center = vector(pin.center()[0],inst.height + 1 * track_offset* (pin_height + drc_width*2))
                                self.add_segment_center(pin.layer, pin_center+supply_inst.ll()+cell_inst.ll()+vector(connection_offset,0), vector((pin_center+supply_inst.ll()+cell_inst.ll())[0] + connection_offset, self.height), connection_width)
                            elif 'replica_col' in supply_inst.name and cell_inst.mirror == 'MX':
                                pin_center = vector(pin.center()[0], -1 * track_offset* (pin_height + drc_width*2))
                                self.add_segment_center(pin.layer, pin_center+supply_inst.ll()+cell_inst.ll()+vector(connection_offset,0), vector((pin_center+supply_inst.ll()+cell_inst.ll())[0] + connection_offset, 0), connection_width)
                            elif 'replica_col' in supply_inst.name:
                                pin_center = vector(pin.center()[0],inst.height + 1 * track_offset * (pin_height + drc_width*2))
                                self.add_segment_center(pin.layer, pin_center+supply_inst.ll()+cell_inst.ll()+vector(connection_offset,0), vector((pin_center+supply_inst.ll()+cell_inst.ll())[0] + connection_offset,self.height), connection_width)
                            self.add_via_stack_center(from_layer=pin.layer,
                                            to_layer='m2',
                                            offset=pin_center+supply_inst.ll()+cell_inst.ll() + vector(connection_offset,0))

        min_area = drc["minarea_{}".format('m3')]
        for track,supply, offset in zip(range(1,5),['vdd','vdd','gnd','gnd'],[min_area * 6,min_area * 6, 0, 0]):
            y_offset = track * (pin_height + drc_width*2)
            self.add_segment_center('m2', vector(0,-y_offset), vector(self.width, -y_offset), drc["minwidth_{}".format('m2')])
            self.add_segment_center('m2', vector(0,self.height + y_offset), vector(self.width, self.height + y_offset), drc["minwidth_{}".format('m2')])
            self.add_power_pin(name=supply,
                               loc=vector(round_to_grid(sqrt(min_area))/2 + offset, -y_offset),
                               start_layer='m2')
            self.add_power_pin(name=supply,
                               loc=vector(round_to_grid(sqrt(min_area))/2 + offset, self.height + y_offset),
                               start_layer='m2')
            self.add_power_pin(name=supply,
                               loc=vector(self.width - round_to_grid(sqrt(min_area))/2 - offset, -y_offset),
                               start_layer='m2')
            self.add_power_pin(name=supply,
                               loc=vector(self.width - round_to_grid(sqrt(min_area))/2 - offset, self.height + y_offset),
                               start_layer='m2')

        self.offset_all_coordinates()
        self.height = self.height + self.dummy_col_insts[0].lr().y * 2

        for pin_name in self.all_bitline_names:
            pin_list = self.bitcell_array_inst.get_pins(pin_name)
            for pin in pin_list:
                if 'bl' in pin.name:
                    self.add_layout_pin(text=pin_name,
                                        layer=pin.layer,
                                        offset=pin.ll().scale(1, 0),
                                        width=pin.width(),
                                        height=self.height)
                elif 'br' in pin_name:
                    self.add_layout_pin(text=pin_name,
                                        layer=pin.layer,
                                        offset=pin.ll().scale(1, 0) + vector(0,pin_height + drc_width*2),
                                        width=pin.width(),
                                        height=self.height - 2 *(pin_height + drc_width*2))
        # Replica bitlines
        if len(self.rbls) > 0:
            for (names, inst) in zip(self.rbl_bitline_names, self.replica_col_insts):
                pin_names = self.replica_columns[self.rbls[0]].all_bitline_names
                mirror = self.replica_col_insts[0].mirror
                for (bl_name, pin_name) in zip(names, pin_names):
                    pin = inst.get_pin(pin_name)
                    if 'rbl_bl' in bl_name:
                    #    if mirror != "MY":
                    #        bl_name = bl_name.replace("rbl_bl","rbl_br")
                        self.add_layout_pin(text=bl_name,
                                            layer=pin.layer,
                                            offset=pin.ll().scale(1, 0),
                                            width=pin.width(),
                                            height=self.height)
                    elif 'rbl_br' in bl_name:
                    #    if mirror != "MY":
                    #        bl_name = bl_name.replace("rbl_br","rbl_bl")
                        self.add_layout_pin(text=bl_name,
                                            layer=pin.layer,
                                            offset=pin.ll().scale(1, 0) + vector(0,(pin_height + drc_width*2)),
                                            width=pin.width(),
                                            height=self.height - 2 *(pin_height + drc_width*2))
        return

    def add_wordline_pins(self):

        # Wordlines to ground
        self.gnd_wordline_names = []

        for port in self.all_ports:
            for bit in self.all_ports:
                self.rbl_wordline_names[port].append("rbl_wl_{0}_{1}".format(port, bit))
                if bit != port:
                    self.gnd_wordline_names.append("rbl_wl_{0}_{1}".format(port, bit))

        self.all_rbl_wordline_names = [x for sl in self.rbl_wordline_names for x in sl]

        self.wordline_names = self.bitcell_array.wordline_names
        self.all_wordline_names = self.bitcell_array.all_wordline_names

        # All wordlines including dummy and RBL
        self.replica_array_wordline_names = []
        #self.replica_array_wordline_names.extend(["gnd"] * len(self.col_cap_top.get_wordline_names()))
        for bit in range(self.rbl[0]):
            self.replica_array_wordline_names.extend([x if x not in self.gnd_wordline_names else "gnd" for x in self.rbl_wordline_names[bit]])
        self.replica_array_wordline_names.extend(self.all_wordline_names)
        for bit in range(self.rbl[1]):
            self.replica_array_wordline_names.extend([x if x not in self.gnd_wordline_names else "gnd" for x in self.rbl_wordline_names[self.rbl[0] + bit]])
        #self.replica_array_wordline_names.extend(["gnd"] * len(self.col_cap_top.get_wordline_names()))

        for port in range(self.rbl[0]):
            self.add_pin(self.rbl_wordline_names[port][port], "INPUT")
        self.add_pin_list(self.all_wordline_names, "INPUT")
        for port in range(self.rbl[0], self.rbl[0] + self.rbl[1]):
            self.add_pin(self.rbl_wordline_names[port][port], "INPUT")

    def create_instances(self):
        """ Create the module instances used in this design """
        self.supplies = ["vdd", "gnd"]

        # Used for names/dimensions only
        # self.cell = factory.create(module_type=OPTS.bitcell)
        
        # Main array
        self.bitcell_array_inst=self.add_inst(name="bitcell_array",
                                                mod=self.bitcell_array)
        self.connect_inst(self.all_bitline_names + self.all_wordline_names + self.supplies)
        # Replica columns
        self.replica_col_insts = []
        for port in self.all_ports:
            if port in self.rbls:
                self.replica_col_insts.append(self.add_inst(name="replica_col_{}".format(port),
                                                            mod=self.replica_columns[port]))
                self.connect_inst(self.rbl_bitline_names[port] + self.replica_array_wordline_names + self.supplies + ["gnd"] + ["gnd"])
            else:
                self.replica_col_insts.append(None)
        
        # Dummy rows under the bitcell array (connected with with the replica cell wl)
        self.dummy_row_replica_insts = []
        # Note, this is the number of left and right even if we aren't adding the columns to this bitcell array!
        for port in self.all_ports:
            self.dummy_row_replica_insts.append(self.add_inst(name="dummy_row_{}".format(port),
                                                                mod=self.dummy_row))
            self.connect_inst(self.all_bitline_names + [x if x not in self.gnd_wordline_names else "gnd" for x in self.rbl_wordline_names[port]] + self.supplies)

        # Top/bottom dummy rows or col caps
        self.dummy_row_insts = []
        self.dummy_row_insts.append(self.add_inst(name="dummy_row_bot",
                                                  mod=self.col_cap_bottom))
        self.connect_inst(self.all_bitline_names + self.supplies + ["gnd"])
        self.dummy_row_insts.append(self.add_inst(name="dummy_row_top",
                                                  mod=self.col_cap_top))
        self.connect_inst(self.all_bitline_names + self.supplies + ["gnd"])

        # Left/right Dummy columns
        self.dummy_col_insts = []
        self.dummy_col_insts.append(self.add_inst(name="dummy_col_left",
                                                    mod=self.row_cap_left))
        self.connect_inst(["dummy_left_" + bl for bl in self.row_cap_left.all_bitline_names] + ["gnd"] + self.replica_array_wordline_names + ["gnd"] + self.supplies)
        self.dummy_col_insts.append(self.add_inst(name="dummy_col_right",
                                                    mod=self.row_cap_right))
        self.connect_inst(["dummy_right_" + bl for bl in self.row_cap_right.all_bitline_names] + ["gnd"] + self.replica_array_wordline_names + ["gnd"] + self.supplies)
