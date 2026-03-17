# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#

from openram import debug
from openram.base import vector
from openram.base import contact
from openram import debug
from openram.base import round_to_grid
from openram.sram_factory import factory
from openram.tech import drc, spice
from openram.tech import cell_properties as props
from openram import OPTS
from openram.modules.capped_replica_bitcell_array import capped_replica_bitcell_array
from .sky130_bitcell_base_array import sky130_bitcell_base_array
from math import sqrt


class sky130_capped_replica_bitcell_array(capped_replica_bitcell_array, sky130_bitcell_base_array):
    """
    Creates a replica bitcell array then adds the row and column caps to all
    sides of a bitcell array.
    """
    def __init__(self, rows, cols, rbl=None, left_rbl=None, right_rbl=None, name=""):
        super().__init__(rows, cols, rbl, left_rbl, right_rbl, name)
    
    def route_power_ring(self, v_layer, h_layer):
        # ring is manually added and routed in add_layout_pins
        pass

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
        supply_insts = self.dummy_row_insts

        for pin_name in self.supplies:
            for supply_inst in supply_insts:
                vdd_alternate = 0
                gnd_alternate = 0
                for cell_inst in supply_inst.mod.insts:
                    inst = cell_inst.mod
                    for pin in inst.get_pins(pin_name):
                        if pin.name == 'vdd':
                            if vdd_alternate:
                                connection_offset = -0.02
                                vdd_alternate = 0
                            else:
                                connection_offset = 0.02
                                vdd_alternate = 1
                            connection_width = drc["minwidth_{}".format('m1')]
                            track_offset = 1
                        elif pin.name == 'gnd':
                            if gnd_alternate:
                                connection_offset = 0.00
                                gnd_alternate = 0
                            else:
                                connection_offset = 0.00
                                gnd_alternate = 1
                            connection_width = drc["minwidth_{}".format('m1')]
                            track_offset = 4
                        pin_width = round_to_grid(sqrt(drc["minarea_m3"]))
                        pin_height = round_to_grid(drc["minarea_m3"] / pin_width)
                        if inst.cell_name == 'sky130_fd_bd_sram__sram_sp_colend_p_cent' or inst.cell_name == 'sky130_fd_bd_sram__sram_sp_colenda_p_cent' or inst.cell_name == 'sky130_fd_bd_sram__sram_sp_colend_cent' or inst.cell_name == 'sky130_fd_bd_sram__sram_sp_colenda_cent' or 'corner' in inst.cell_name:
                            if 'dummy_row_bot' in supply_inst.name:
                                pin_center = vector(pin.center()[0], -1 * track_offset * (pin_height + drc_width*2))
                                self.add_segment_center(pin.layer, pin_center+supply_inst.ll()+cell_inst.ll()+vector(connection_offset,0), vector((pin_center+supply_inst.ll()+cell_inst.ll())[0] + connection_offset, 0), connection_width)
                            elif 'dummy_row_top' in supply_inst.name:
                                pin_center = vector(pin.center()[0],inst.height + 1 * track_offset* (pin_height + drc_width*2))
                                self.add_segment_center(pin.layer, pin_center+supply_inst.ll()+cell_inst.ll()+vector(connection_offset,0), vector((pin_center+supply_inst.ll()+cell_inst.ll())[0] + connection_offset, self.height), connection_width)
                            # elif 'replica_col' in supply_inst.name and cell_inst.mirror == 'MX':
                            #     pin_center = vector(pin.center()[0], -1 * track_offset* (pin_height + drc_width*2))
                            #     self.add_segment_center(pin.layer, pin_center+supply_inst.ll()+cell_inst.ll()+vector(connection_offset,0), vector((pin_center+supply_inst.ll()+cell_inst.ll())[0] + connection_offset, 0), connection_width)
                            # elif 'replica_col' in supply_inst.name:
                            #     pin_center = vector(pin.center()[0],inst.height + 1 * track_offset * (pin_height + drc_width*2))
                            #     self.add_segment_center(pin.layer, pin_center+supply_inst.ll()+cell_inst.ll()+vector(connection_offset,0), vector((pin_center+supply_inst.ll()+cell_inst.ll())[0] + connection_offset,self.height), connection_width)
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
                            if 'dummy_row_bot' in supply_inst.name:
                                pin_center = vector(pin.center()[0], -1 * track_offset * (pin_height + drc_width*2))
                                self.add_segment_center(pin.layer, pin_center+supply_inst.ll()+cell_inst.ll()+vector(connection_offset,0), vector((pin_center+supply_inst.ll()+cell_inst.ll())[0] + connection_offset, 0), connection_width)
                            elif 'dummy_row_top' in supply_inst.name:
                                pin_center = vector(pin.center()[0],inst.height + 1 * track_offset* (pin_height + drc_width*2))
                                self.add_segment_center(pin.layer, pin_center+supply_inst.ll()+cell_inst.ll()+vector(connection_offset,0), vector((pin_center+supply_inst.ll()+cell_inst.ll())[0] + connection_offset, self.height), connection_width)
                            # elif 'replica_col' in supply_inst.name:
                            #     pin_center = vector(pin.center()[0], -1 * track_offset* (pin_height + drc_width*2))
                            #     self.add_segment_center(pin.layer, pin_center+supply_inst.ll()+cell_inst.ll()+vector(connection_offset,0), vector((pin_center+supply_inst.ll()+cell_inst.ll())[0] + connection_offset, 0), connection_width)
                            # elif 'replica_col' in supply_inst.name:
                            #     pin_center = vector(pin.center()[0],inst.height + 1 * track_offset * (pin_height + drc_width*2))
                            #     self.add_segment_center(pin.layer, pin_center+supply_inst.ll()+cell_inst.ll()+vector(connection_offset,0), vector((pin_center+supply_inst.ll()+cell_inst.ll())[0] + connection_offset,self.height), connection_width)
                            self.add_via_stack_center(from_layer=pin.layer,
                                            to_layer='m2',
                                            offset=pin_center+supply_inst.ll()+cell_inst.ll() + vector(connection_offset,0))

        min_area = drc["minarea_{}".format('m3')]
        for track,supply, offset in zip(range(1,5),['vdd','vdd','gnd','gnd'],[min_area * 6,min_area * 6, 0, 0]):
            y_offset = track * (pin_height + drc_width*2)
            self.add_segment_center('m2', vector(-0.4,-y_offset), vector(self.width+0.4, -y_offset), drc["minwidth_{}".format('m2')])
            self.add_segment_center('m2', vector(-0.4,self.height + y_offset), vector(self.width+0.4, self.height + y_offset), drc["minwidth_{}".format('m2')])
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
        

        for pin_name in self.bitline_pin_list:
            pin_list = self.replica_bitcell_array_inst.get_pins(pin_name)
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
        
        # # Replica bitlines
        # if len(self.rbls) > 0:
        #     for (names, inst) in zip(self.rbl_bitline_names, self.replica_col_insts):
        #         pin_names = self.replica_bitcell_array_inst.mod.replica_columns[self.rbls[0]].all_bitline_names
        #         mirror = self.replica_col_insts[0].mirror
        #         for (bl_name, pin_name) in zip(names, pin_names):
        #             pin = inst.get_pin(pin_name)
        #             if 'rbl_bl' in bl_name:
        #             #    if mirror != "MY":
        #             #        bl_name = bl_name.replace("rbl_bl","rbl_br")
        #                 self.add_layout_pin(text=bl_name,
        #                                     layer=pin.layer,
        #                                     offset=pin.ll().scale(1, 0),
        #                                     width=pin.width(),
        #                                     height=self.height)
        #             elif 'rbl_br' in bl_name:
        #             #    if mirror != "MY":
        #             #        bl_name = bl_name.replace("rbl_br","rbl_bl")
        #                 self.add_layout_pin(text=bl_name,
        #                                     layer=pin.layer,
        #                                     offset=pin.ll().scale(1, 0) + vector(0,(pin_height + drc_width*2)),
        #                                     width=pin.width(),
        #                                     height=self.height - 2 *(pin_height + drc_width*2))
        return
