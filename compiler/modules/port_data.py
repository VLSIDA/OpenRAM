# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
import math
from collections import namedtuple
from openram import debug
from openram.base import design
from openram.base import vector
from openram.sram_factory import factory
from openram.tech import drc
from openram.tech import cell_properties
from openram.tech import layer_properties as layer_props
from openram import OPTS


class port_data(design):
    """
    Create the data port (column mux, sense amps, write driver, etc.) for the given port number.
    When RBLs present: port 0 always has the RBL on the left while port 1 is on the right.
    """

    def __init__(self, sram_config, port, has_rbl, num_spare_cols=None, bit_offsets=None, name="",):

        sram_config.set_local_config(self)
        self.port = port
        self.has_rbl = has_rbl
        if self.write_size != self.word_size:
            self.num_wmasks = int(math.ceil(self.word_size / self.write_size))
        else:
            self.num_wmasks = 0

        if num_spare_cols is not None:
                self.num_spare_cols = num_spare_cols + self.num_spare_cols
        if self.num_spare_cols is None:
            self.num_spare_cols = 0
        if not bit_offsets:
            bitcell = factory.create(module_type=OPTS.bitcell)
            if(cell_properties.use_strap == True and OPTS.num_ports == 1):
                strap = factory.create(module_type=cell_properties.strap_module, version=cell_properties.strap_version)
                precharge_width = bitcell.width + strap.width
            else:
                precharge_width = bitcell.width
            self.bit_offsets = []
            for i in range(self.num_cols + self.num_spare_cols):
                self.bit_offsets.append(i * precharge_width)
        else:
            self.bit_offsets = bit_offsets
        if name == "":
            name = "port_data_{0}".format(self.port)
        super().__init__(name)
        debug.info(2,
                   "create data port of size {0} with {1} words per row".format(self.word_size,
                                                                                   self.words_per_row))

        self.create_netlist()
        if not OPTS.netlist_only:
            debug.check(len(self.all_ports)<=2,
                        "Bank layout cannot handle more than two ports.")
            self.create_layout()
            self.add_boundary()

    def get_bl_names(self):
        # bl lines are connect from the precharger
        return self.precharge.get_bl_names()

    def get_br_names(self):
        # br lines are connect from the precharger
        return self.precharge.get_br_names()

    def get_bl_name(self, port=0):
        return "bl_{}".format(port)

    def get_br_name(self, port=0):
        return "br_{}".format(port)

    def create_netlist(self):
        self.precompute_constants()
        self.add_pins()
        self.add_modules()
        self.create_instances()

    def create_instances(self):
        if self.precharge_array:
            self.create_precharge_array()
        else:
            self.precharge_array_inst = None

        if self.sense_amp_array:
            self.create_sense_amp_array()
        else:
            self.sense_amp_array_inst = None

        if self.write_driver_array:
            self.create_write_driver_array()
            if self.write_size != self.word_size:
                self.create_write_mask_and_array()
            else:
                self.write_mask_and_array_inst = None
        else:
            self.write_driver_array_inst = None
            self.write_mask_and_array_inst = None

        if self.column_mux_array:
            self.create_column_mux_array()
        else:
            self.column_mux_array_inst = None

    def create_layout(self):
        self.compute_instance_offsets()
        self.place_instances()
        self.route_layout()
        self.DRC_LVS()

    def add_pins(self):
        """ Adding pins for port data module"""

        if self.has_rbl:
            self.add_pin("rbl_bl", "INOUT")
            self.add_pin("rbl_br", "INOUT")
        for bit in range(self.num_cols):
            self.add_pin("bl_{0}".format(bit), "INOUT")
            self.add_pin("br_{0}".format(bit), "INOUT")
        for bit in range(self.num_spare_cols):
            self.add_pin("sparebl_{0}".format(bit), "INOUT")
            self.add_pin("sparebr_{0}".format(bit), "INOUT")
        if self.port in self.read_ports:
            for bit in range(self.word_size + self.num_spare_cols):
                self.add_pin("dout_{}".format(bit), "OUTPUT")
        if self.port in self.write_ports:
            for bit in range(self.word_size + self.num_spare_cols):
                self.add_pin("din_{}".format(bit), "INPUT")
        # Will be empty if no col addr lines
        sel_names = ["sel_{}".format(x) for x in range(self.num_col_addr_lines)]
        for pin_name in sel_names:
            self.add_pin(pin_name, "INPUT")
        if self.port in self.read_ports:
            self.add_pin("s_en", "INPUT")
        self.add_pin("p_en_bar", "INPUT")
        if self.port in self.write_ports:
            self.add_pin("w_en", "INPUT")
            for bit in range(self.num_wmasks):
                self.add_pin("bank_wmask_{}".format(bit), "INPUT")
            for bit in range(self.num_spare_cols):
                self.add_pin("bank_spare_wen{}".format(bit), "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def route_layout(self):
        """ Create routing among the modules """
        self.route_data_lines()
        self.route_layout_pins()
        self.route_supplies()

    def route_layout_pins(self):
        """ Add the pins """
        self.route_bitline_pins()
        self.route_control_pins()

    def route_data_lines(self):
        """ Route the bitlines depending on the port type rw, w, or r. """

        if self.port in self.readwrite_ports:
            # (write_mask_and ->) write_driver -> sense_amp -> (column_mux ->) precharge -> bitcell_array
            self.route_write_mask_and_array_in(self.port)
            self.route_write_mask_and_array_to_write_driver(self.port)
            self.route_write_driver_in(self.port)
            self.route_sense_amp_out(self.port)
            self.route_write_driver_to_sense_amp(self.port)
            self.route_sense_amp_to_column_mux_or_precharge_array(self.port)
            self.route_column_mux_to_precharge_array(self.port)
        elif self.port in self.read_ports:
            # sense_amp -> (column_mux) -> precharge -> bitcell_array
            self.route_sense_amp_out(self.port)
            self.route_sense_amp_to_column_mux_or_precharge_array(self.port)
            self.route_column_mux_to_precharge_array(self.port)
        else:
            # (write_mask_and ->) write_driver -> (column_mux ->) precharge -> bitcell_array
            self.route_write_mask_and_array_in(self.port)
            self.route_write_mask_and_array_to_write_driver(self.port)
            self.route_write_driver_in(self.port)
            self.route_write_driver_to_column_mux_or_precharge_array(self.port)
            self.route_column_mux_to_precharge_array(self.port)

    def route_supplies(self):
        """ Propagate all vdd/gnd pins up to this level for all modules """

        for inst in self.insts:
            self.copy_power_pins(inst, "vdd")
            self.copy_power_pins(inst, "gnd")

    def add_modules(self):

        # Extra column +1 is for RBL
        # Precharge will be shifted left if needed
        # Column offset is set to port so extra column can be on left or right
        # and mirroring happens correctly

        # Used for names/dimensions only
        cell = factory.create(module_type=OPTS.bitcell)
        if(cell_properties.use_strap == True and OPTS.num_ports == 1):
            strap = factory.create(module_type=cell_properties.strap_module, version=cell_properties.strap_version)
            precharge_width = cell.width + strap.width
        else:
            precharge_width = cell.width
        if self.has_rbl:
            if self.port == 0:
                # Append an offset on the left
                precharge_bit_offsets = [self.bit_offsets[0] - precharge_width] + self.bit_offsets
            else:
                # Append an offset on the right
                precharge_bit_offsets = self.bit_offsets + [self.bit_offsets[-1] + precharge_width]
        else:
            precharge_bit_offsets = self.bit_offsets

        # has_rbl is a boolean treated as 1 if true 0 if false typical python
        self.precharge_array = factory.create(module_type="precharge_array",
                                              columns=self.num_cols + self.num_spare_cols + self.has_rbl,
                                              offsets=precharge_bit_offsets,
                                              bitcell_bl=self.bl_names[self.port],
                                              bitcell_br=self.br_names[self.port],
                                              column_offset=self.port - 1)

        if self.port in self.read_ports:
            # RBLs don't get a sense amp
            self.sense_amp_array = factory.create(module_type="sense_amp_array",
                                                  word_size=self.word_size,
                                                  offsets=self.bit_offsets,
                                                  words_per_row=self.words_per_row,
                                                  num_spare_cols=self.num_spare_cols)
        else:
            self.sense_amp_array = None

        if self.col_addr_size > 0:
            # RBLs dont get a col mux
            self.column_mux_array = factory.create(module_type="column_mux_array",
                                                   columns=self.num_cols,
                                                   word_size=self.word_size,
                                                   offsets=self.bit_offsets,
                                                   bitcell_bl=self.bl_names[self.port],
                                                   bitcell_br=self.br_names[self.port])
        else:
            self.column_mux_array = None

        if self.port in self.write_ports:
            # RBLs dont get a write driver
            self.write_driver_array = factory.create(module_type="write_driver_array",
                                                     columns=self.num_cols,
                                                     word_size=self.word_size,
                                                     offsets=self.bit_offsets,
                                                     write_size=self.write_size,
                                                     num_spare_cols=self.num_spare_cols)
            if self.write_size != self.word_size:
                # RBLs don't get a write mask
                self.write_mask_and_array = factory.create(module_type="write_mask_and_array",
                                                           columns=self.num_cols,
                                                           offsets=self.bit_offsets,
                                                           word_size=self.word_size,
                                                           write_size=self.write_size)
            else:
                self.write_mask_and_array = None

        else:
            self.write_driver_array = None
            self.write_mask_and_array = None

    def precompute_constants(self):
        """  Get some preliminary data ready """

        # The central bus is the column address (one hot) and row address (binary)
        if self.col_addr_size>0:
            self.num_col_addr_lines = 2**self.col_addr_size
        else:
            self.num_col_addr_lines = 0

        # A space for wells or jogging m2 between modules
        self.m2_gap = max(2 * drc("pwell_to_nwell") + drc("nwell_enclose_active"),
                          3 * self.m2_pitch)


        # create arrays of bitline and bitline_bar names for read,
        # write, or all ports
        self.bitcell = factory.create(module_type=OPTS.bitcell)
        self.bl_names = self.bitcell.get_all_bl_names()
        self.br_names = self.bitcell.get_all_br_names()
        self.wl_names = self.bitcell.get_all_wl_names()
        # used for bl/br names
        self.precharge = factory.create(module_type=OPTS.precharge,
                                        bitcell_bl=self.bl_names[0],
                                        bitcell_br=self.br_names[0])

    def create_precharge_array(self):
        """ Creating Precharge """
        if not self.precharge_array:
            self.precharge_array_inst = None
            return

        self.precharge_array_inst = self.add_inst(name="precharge_array{}".format(self.port),
                                                  mod=self.precharge_array)
        temp = []
        # Use left BLs for RBL
        if self.port==0 and self.has_rbl:
            temp.append("rbl_bl")
            temp.append("rbl_br")
        for bit in range(self.num_cols):
            temp.append("bl_{0}".format(bit))
            temp.append("br_{0}".format(bit))

        for bit in range(self.num_spare_cols):
            temp.append("sparebl_{0}".format(bit))
            temp.append("sparebr_{0}".format(bit))

        # Use right BLs for RBL
        if self.port==1 and self.has_rbl:
            temp.append("rbl_bl")
            temp.append("rbl_br")
        temp.extend(["p_en_bar", "vdd"])
        self.connect_inst(temp)

    def place_precharge_array(self, offset):
        """ Placing Precharge """

        self.precharge_array_inst.place(offset=offset, mirror="MX")

    def create_column_mux_array(self):
        """ Creating Column Mux when words_per_row > 1 . """

        self.column_mux_array_inst = self.add_inst(name="column_mux_array{}".format(self.port),
                                                   mod=self.column_mux_array)

        temp = []
        for col in range(self.num_cols):
            temp.append("bl_{0}".format(col))
            temp.append("br_{0}".format(col))
        for word in range(self.words_per_row):
            temp.append("sel_{}".format(word))
        for bit in range(self.word_size):
            temp.append("bl_out_{0}".format(bit))
            temp.append("br_out_{0}".format(bit))

        temp.append("gnd")
        self.connect_inst(temp)

    def place_column_mux_array(self, offset):
        """ Placing Column Mux when words_per_row > 1 . """
        if self.col_addr_size == 0:
            return

        self.column_mux_array_inst.place(offset=offset, mirror="MX")

    def create_sense_amp_array(self):
        """ Creating Sense amp  """
        self.sense_amp_array_inst = self.add_inst(name="sense_amp_array{}".format(self.port),
                                                  mod=self.sense_amp_array)

        temp = []
        for bit in range(self.word_size):
            temp.append("dout_{}".format(bit))
            if self.words_per_row == 1:
                temp.append("bl_{0}".format(bit))
                temp.append("br_{0}".format(bit))
            else:
                temp.append("bl_out_{0}".format(bit))
                temp.append("br_out_{0}".format(bit))

        for bit in range(self.num_spare_cols):
            temp.append("dout_{}".format(self.word_size + bit))
            temp.append("sparebl_{0}".format(bit))
            temp.append("sparebr_{0}".format(bit))

        temp.append("s_en")
        temp.extend(["vdd", "gnd"])
        self.connect_inst(temp)

    def place_sense_amp_array(self, offset):
        """ Placing Sense amp  """
        self.sense_amp_array_inst.place(offset=offset, mirror="MX")

    def create_write_driver_array(self):
        """ Creating Write Driver  """
        self.write_driver_array_inst = self.add_inst(name="write_driver_array{}".format(self.port),
                                                     mod=self.write_driver_array)
        temp = []
        for bit in range(self.word_size + self.num_spare_cols):
            temp.append("din_{}".format(bit))

        for bit in range(self.word_size):
            if (self.words_per_row == 1):
                temp.append("bl_{0}".format(bit))
                temp.append("br_{0}".format(bit))
            else:
                temp.append("bl_out_{0}".format(bit))
                temp.append("br_out_{0}".format(bit))

        for bit in range(self.num_spare_cols):
            temp.append("sparebl_{0}".format(bit))
            temp.append("sparebr_{0}".format(bit))

        if self.write_size != self.word_size:
            for i in range(self.num_wmasks):
                temp.append("wdriver_sel_{}".format(i))
            for i in range(self.num_spare_cols):
                temp.append("bank_spare_wen{}".format(i))

        elif self.num_spare_cols and self.write_size == self.word_size:
            temp.append("w_en")
            for i in range(self.num_spare_cols):
                temp.append("bank_spare_wen{}".format(i))
        else:
            temp.append("w_en")
        temp.extend(["vdd", "gnd"])

        self.connect_inst(temp)

    def place_write_driver_array(self, offset):
        """ Placing Write Driver  """
        self.write_driver_array_inst.place(offset=offset, mirror="MX")

    def create_write_mask_and_array(self):
        """ Creating Write Mask AND Array  """
        self.write_mask_and_array_inst = self.add_inst(name="write_mask_and_array{}".format(self.port),
                                                       mod=self.write_mask_and_array)

        temp = []
        for bit in range(self.num_wmasks):
            temp.append("bank_wmask_{}".format(bit))
        temp.extend(["w_en"])
        for bit in range(self.num_wmasks):
            temp.append("wdriver_sel_{}".format(bit))
        temp.extend(["vdd", "gnd"])
        self.connect_inst(temp)

    def place_write_mask_and_array(self, offset):
        """ Placing Write Mask AND array  """
        self.write_mask_and_array_inst.place(offset=offset, mirror="MX")

    def compute_instance_offsets(self):
        """
        Compute the empty instance offsets for port0 and port1 (if needed)
        """

        vertical_port_order = []
        vertical_port_order.append(self.precharge_array_inst)
        vertical_port_order.append(self.column_mux_array_inst)
        vertical_port_order.append(self.sense_amp_array_inst)
        vertical_port_order.append(self.write_driver_array_inst)
        vertical_port_order.append(self.write_mask_and_array_inst)

        vertical_port_offsets = 5 * [None]
        self.width = 0
        self.height = 0
        for i, p in enumerate(vertical_port_order):
            if p == None:
                continue
            self.height += (p.height + self.m2_gap)
            self.width = max(self.width, p.width)
            vertical_port_offsets[i] = vector(0, self.height)

        # Reversed order
        self.write_mask_and_offset = vertical_port_offsets[4]
        self.write_driver_offset = vertical_port_offsets[3]
        self.sense_amp_offset = vertical_port_offsets[2]
        self.column_mux_offset = vertical_port_offsets[1]
        self.precharge_offset = vertical_port_offsets[0]

    def place_instances(self):
        """ Place the instances. """

        # These are fixed in the order: write mask ANDs, write driver, sense amp, column mux, precharge,
        # even if the item is not used in a given port (it will be None then)
        if self.write_mask_and_offset:
            self.place_write_mask_and_array(self.write_mask_and_offset)
        if self.write_driver_offset:
            self.place_write_driver_array(self.write_driver_offset)
        if self.sense_amp_offset:
            self.place_sense_amp_array(self.sense_amp_offset)
        if self.precharge_offset:
            self.place_precharge_array(self.precharge_offset)
        if self.column_mux_offset:
            self.place_column_mux_array(self.column_mux_offset)

    def route_sense_amp_out(self, port):
        """ Add pins for the sense amp output """
        for bit in range(self.word_size + self.num_spare_cols):
            data_pin = self.sense_amp_array_inst.get_pin("data_{}".format(bit))
            self.add_layout_pin_rect_center(text="dout_{0}".format(bit),
                                            layer=data_pin.layer,
                                            offset=data_pin.center(),
                                            height=data_pin.height(),
                                            width=data_pin.width())

    def route_write_driver_in(self, port):
        """ Connecting write driver   """

        for row in range(self.word_size + self.num_spare_cols):
            data_name = "data_{}".format(row)
            din_name = "din_{}".format(row)
            self.copy_layout_pin(self.write_driver_array_inst, data_name, din_name)

    def route_write_mask_and_array_in(self, port):
        """ Add pins for the write mask and array input """

        for bit in range(self.num_wmasks):
            wmask_in_name = "wmask_in_{}".format(bit)
            bank_wmask_name = "bank_wmask_{}".format(bit)
            self.copy_layout_pin(self.write_mask_and_array_inst, wmask_in_name, bank_wmask_name)

    def route_write_mask_and_array_to_write_driver(self, port):
        """
        Routing of wdriver_sel_{} between write mask AND array and
        write driver array. Adds layout pin for write
        mask AND array output and via for write driver enable
        """

        wmask_inst = self.write_mask_and_array_inst
        wdriver_inst = self.write_driver_array_inst

        for bit in range(self.num_wmasks):
            wmask_out_pin = wmask_inst.get_pin("wmask_out_{0}".format(bit))
            wdriver_en_pin = wdriver_inst.get_pin("en_{0}".format(bit))

            wmask_pos = wmask_out_pin.center()
            wdriver_pos = wdriver_en_pin.rc() - vector(self.m2_pitch, 0)
            mid_pos = vector(wdriver_pos.x, wmask_pos.y)

            # Add driver on mask output
            self.add_via_stack_center(from_layer=wmask_out_pin.layer,
                                      to_layer="m1",
                                      offset=wmask_pos)
            # Add via for the write driver array's enable input
            self.add_via_stack_center(from_layer=wdriver_en_pin.layer,
                                      to_layer="m2",
                                      offset=wdriver_pos)

            # Route between write mask AND array and write driver array
            self.add_wire(self.m1_stack, [wmask_pos, mid_pos, wdriver_pos])

    def route_column_mux_to_precharge_array(self, port):
        """ Routing of BL and BR between col mux and precharge array """

        # Only do this if we have a column mux!
        if self.col_addr_size==0:
            return

        start_bit = 1 if self.port == 0 and self.has_rbl else 0

        self.connect_bitlines(inst1=self.column_mux_array_inst,
                              inst2=self.precharge_array_inst,
                              num_bits=self.num_cols,
                              inst2_start_bit=start_bit)

    def route_sense_amp_to_column_mux_or_precharge_array(self, port):
        """ Routing of BL and BR between sense_amp and column mux or precharge array """
        inst2 = self.sense_amp_array_inst

        if self.col_addr_size>0:
            # Sense amp is connected to the col mux
            inst1 = self.column_mux_array_inst
            inst1_bls_templ = "{inst}_out_{bit}"
            start_bit = 0
        else:
            # Sense amp is directly connected to the precharge array
            inst1 = self.precharge_array_inst
            inst1_bls_templ="{inst}_{bit}"

            if self.port==0 and self.has_rbl:
                start_bit=1
            else:
                start_bit=0

        # spare cols connected to precharge array since they are read independently
        if self.num_spare_cols and self.col_addr_size>0:
            if self.port==0:
                off = 1
            else:
                off = 0
            if OPTS.num_ports > 1:
                self.channel_route_bitlines(inst1=self.column_mux_array_inst,
                                            inst1_bls_template="{inst}_out_{bit}",
                                            inst2=inst2,
                                            num_bits=self.word_size,
                                            inst1_start_bit=start_bit)

                self.channel_route_bitlines(inst1=self.precharge_array_inst,
                                            inst1_bls_template="{inst}_{bit}",
                                            inst2=inst2,
                                            num_bits=self.num_spare_cols,
                                            inst1_start_bit=self.num_cols + off,
                                            inst2_start_bit=self.word_size)
            else:
                self.connect_bitlines(inst1=self.column_mux_array_inst,
                                            inst1_bls_template="{inst}_out_{bit}",
                                            inst2=inst2,
                                            num_bits=self.word_size,
                                            inst1_start_bit=start_bit)

                self.connect_bitlines(inst1=self.precharge_array_inst,
                                            inst1_bls_template="{inst}_{bit}",
                                            inst2=inst2,
                                            num_bits=self.num_spare_cols,
                                            inst1_start_bit=self.num_cols + off,
                                            inst2_start_bit=self.word_size)

        elif layer_props.port_data.channel_route_bitlines:
            self.channel_route_bitlines(inst1=inst1,
                                        inst1_bls_template=inst1_bls_templ,
                                        inst2=inst2,
                                        num_bits=self.word_size + self.num_spare_cols,
                                        inst1_start_bit=start_bit)
        # This could be a channel route, but in some techs the bitlines
        # are too close together.
        else:
            self.connect_bitlines(inst1=inst1,
                                  inst1_bls_template=inst1_bls_templ,
                                  inst2=inst2,
                                  num_bits=self.word_size + self.num_spare_cols,
                                  inst1_start_bit=start_bit)

    def route_write_driver_to_column_mux_or_precharge_array(self, port):
        """ Routing of BL and BR between sense_amp and column mux or precharge array """
        inst2 = self.write_driver_array_inst

        if self.col_addr_size>0:
            # Write driver is connected to the col mux
            inst1 = self.column_mux_array_inst
            inst1_bls_templ = "{inst}_out_{bit}"
            start_bit = 0
        else:
            # Sense amp is directly connected to the precharge array
            inst1 = self.precharge_array_inst
            inst1_bls_templ="{inst}_{bit}"
            if self.port==0:
                start_bit=1
            else:
                start_bit=0

        if self.port==0:
            off = 1
        else:
            off = 0

        # Channel route spare columns' bitlines
        if self.num_spare_cols and self.col_addr_size>0:
            if self.port==0:
                off = 1
            else:
                off = 0

            self.channel_route_bitlines(inst1=self.column_mux_array_inst,
                                        inst1_bls_template="{inst}_out_{bit}",
                                        inst2=inst2,
                                        num_bits=self.word_size,
                                        inst1_start_bit=start_bit)

            self.channel_route_bitlines(inst1=self.precharge_array_inst,
                                        inst1_bls_template="{inst}_{bit}",
                                        inst2=inst2,
                                        num_bits=self.num_spare_cols,
                                        inst1_start_bit=self.num_cols + off,
                                        inst2_start_bit=self.word_size)

        # This could be a channel route, but in some techs the bitlines
        # are too close together.
        elif layer_props.port_data.channel_route_bitlines:
            self.channel_route_bitlines(inst1=inst1, inst2=inst2,
                                        num_bits=self.word_size + self.num_spare_cols,
                                        inst1_bls_template=inst1_bls_templ,
                                        inst1_start_bit=start_bit)
        else:
            self.connect_bitlines(inst1=inst1, inst2=inst2,
                                  num_bits=self.word_size,
                                  inst1_bls_template=inst1_bls_templ,
                                  inst1_start_bit=start_bit)

    def route_write_driver_to_sense_amp(self, port):
        """ Routing of BL and BR between write driver and sense amp """

        inst1 = self.write_driver_array_inst
        inst2 = self.sense_amp_array_inst

        # This could be a channel route, but in some techs the bitlines
        # are too close together.
        self.connect_bitlines(inst1=inst1,
                              inst2=inst2,
                              num_bits=self.word_size + self.num_spare_cols)

    def route_bitline_pins(self):
        """ Add the bitline pins for the given port """

        # Connect one bitline to the RBL and offset the indices for the other BLs
        if self.port==0 and self.has_rbl:
            self.copy_layout_pin(self.precharge_array_inst, "bl_0", "rbl_bl")
            self.copy_layout_pin(self.precharge_array_inst, "br_0", "rbl_br")
            bit_offset=1
        elif self.port==1 and self.has_rbl:
            self.copy_layout_pin(self.precharge_array_inst, "bl_{}".format(self.num_cols + self.num_spare_cols), "rbl_bl")
            self.copy_layout_pin(self.precharge_array_inst, "br_{}".format(self.num_cols + self.num_spare_cols), "rbl_br")
            bit_offset=0
        else:
            bit_offset=0

        for bit in range(self.num_cols):
            if self.precharge_array_inst:
                self.copy_layout_pin(self.precharge_array_inst,
                                     "bl_{}".format(bit + bit_offset),
                                     "bl_{}".format(bit))
                self.copy_layout_pin(self.precharge_array_inst,
                                     "br_{}".format(bit + bit_offset),
                                     "br_{}".format(bit))
            else:
                debug.error("Didn't find precharge array.")

        # Copy bitlines of spare columns
        for bit in range(self.num_spare_cols):
            if self.precharge_array_inst:
                self.copy_layout_pin(self.precharge_array_inst,
                                     "bl_{}".format(self.num_cols + bit + bit_offset),
                                     "sparebl_{}".format(bit))
                self.copy_layout_pin(self.precharge_array_inst,
                                     "br_{}".format(self.num_cols + bit + bit_offset),
                                     "sparebr_{}".format(bit))
            else:
                debug.error("Didn't find precharge array.")


    def route_control_pins(self):
        """ Add the control pins: s_en, p_en_bar, w_en """
        if self.precharge_array_inst:
            self.copy_layout_pin(self.precharge_array_inst, "en_bar", "p_en_bar")
        if self.column_mux_array_inst:
            sel_names = ["sel_{}".format(x) for x in range(self.num_col_addr_lines)]
            for pin_name in sel_names:
                self.copy_layout_pin(self.column_mux_array_inst, pin_name)
        if self.sense_amp_array_inst:
           self.copy_layout_pin(self.sense_amp_array_inst, "en", "s_en")
        if self.write_driver_array_inst:
            if self.write_mask_and_array_inst:
                for bit in range(self.num_wmasks):
                    # Add write driver's en_{} pins
                    self.copy_layout_pin(self.write_driver_array_inst, "en_{}".format(bit), "wdriver_sel_{}".format(bit))
                for bit in range(self.num_spare_cols):
                    # Add spare columns' en_{} pins
                    self.copy_layout_pin(self.write_driver_array_inst, "en_{}".format(bit + self.num_wmasks), "bank_spare_wen{}".format(bit))
            elif self.num_spare_cols and not self.write_mask_and_array_inst:
                self.copy_layout_pin(self.write_driver_array_inst, "en_0", "w_en")
                for bit in range(self.num_spare_cols):
                    self.copy_layout_pin(self.write_driver_array_inst, "en_{}".format(bit + 1), "bank_spare_wen{}".format(bit))
            else:
                self.copy_layout_pin(self.write_driver_array_inst, "en", "w_en")
        if self.write_mask_and_array_inst:
            self.copy_layout_pin(self.write_mask_and_array_inst, "en", "w_en")

    def _group_bitline_instances(self, inst1, inst2, num_bits,
                                 inst1_bls_template,
                                 inst1_start_bit,
                                 inst2_bls_template,
                                 inst2_start_bit):
        """
        Groups all the parameters into a named tuple and seperates them into
        top and bottom instances.
        """
        inst_group = namedtuple('InstanceGroup', ('inst', 'bls_template',
                                                  'bl_name', 'br_name', 'start_bit'))

        inst1_group = inst_group(inst1, inst1_bls_template,
                                 inst1.mod.get_bl_name(),
                                 inst1.mod.get_br_name(),
                                 inst1_start_bit)
        inst2_group = inst_group(inst2, inst2_bls_template,
                                 inst2.mod.get_bl_name(),
                                 inst2.mod.get_br_name(),
                                 inst2_start_bit)
        # determine top and bottom automatically.
        # since they don't overlap, we can just check the bottom y coordinate.
        if inst1.by() < inst2.by():
            bot_inst_group = inst1_group
            top_inst_group = inst2_group
        else:
            bot_inst_group = inst2_group
            top_inst_group = inst1_group

        return (bot_inst_group, top_inst_group)

    def _get_bitline_pins(self, inst_group, bit):
        """
        Extracts bl/br pins from an InstanceGroup based on the bit modifier.
        """
        full_bl_name = inst_group.bls_template.format(
            **{'inst': inst_group.bl_name,
               'bit': inst_group.start_bit + bit}
        )
        full_br_name = inst_group.bls_template.format(
            **{'inst': inst_group.br_name,
               'bit': inst_group.start_bit + bit}
        )
        return (inst_group.inst.get_pin(full_bl_name),
                inst_group.inst.get_pin(full_br_name))

    def channel_route_bitlines(self, inst1, inst2, num_bits,
                               inst1_bls_template="{inst}_{bit}",
                               inst1_start_bit=0,
                               inst2_bls_template="{inst}_{bit}",
                               inst2_start_bit=0):
        """
        Route the bl and br of two modules using the channel router.
        """

        bot_inst_group, top_inst_group = self._group_bitline_instances(inst1, inst2, num_bits,
                                                                       inst1_bls_template, inst1_start_bit,
                                                                       inst2_bls_template, inst2_start_bit)

        # Channel route each mux separately since we don't minimize the number
        # of tracks in teh channel router yet. If we did, we could route all the bits at once!
        offset = bot_inst_group.inst.ul() + vector(0, self.m1_nonpref_pitch)
        for bit in range(num_bits):
            bottom_names = self._get_bitline_pins(bot_inst_group, bit)
            top_names = self._get_bitline_pins(top_inst_group, bit)

            route_map = list(zip(bottom_names, top_names))
            self.create_horizontal_channel_route(route_map, offset, self.m1_stack)

    def connect_bitlines(self, inst1, inst2, num_bits,
                         inst1_bls_template="{inst}_{bit}",
                         inst1_start_bit=0,
                         inst2_bls_template="{inst}_{bit}",
                         inst2_start_bit=0):
        """
        Connect the bl and br of two modules.
        This assumes that they have sufficient space to create a jog
        in the middle between the two modules (if needed).
        """

        bot_inst_group, top_inst_group = self._group_bitline_instances(inst1, inst2, num_bits,
                                                                       inst1_bls_template, inst1_start_bit,
                                                                       inst2_bls_template, inst2_start_bit)

        for col in range(num_bits):
            bot_bl_pin, bot_br_pin = self._get_bitline_pins(bot_inst_group, col)
            top_bl_pin, top_br_pin = self._get_bitline_pins(top_inst_group, col)
            bot_bl, bot_br = bot_bl_pin.uc(), bot_br_pin.uc()
            top_bl, top_br = top_bl_pin.bc(), top_br_pin.bc()

            layer_pitch = getattr(self, "{}_pitch".format(top_bl_pin.layer))
            self.add_zjog(bot_bl_pin.layer, bot_bl, top_bl, "V", fixed_offset=top_bl_pin.by() - layer_pitch)
            self.add_zjog(bot_br_pin.layer, bot_br, top_br, "V", fixed_offset=top_bl_pin.by() - 2 * layer_pitch)

    def graph_exclude_precharge(self):
        """Precharge adds a loop between bitlines, can be excluded to reduce complexity"""
        if self.precharge_array_inst:
            self.graph_inst_exclude.add(self.precharge_array_inst)

    def graph_exclude_column_mux(self, column_include_num):
        """
        Excludes all columns muxes unrelated to the target bit being simulated.
        """
        if self.column_mux_array:
            self.column_mux_array.graph_exclude_columns(column_include_num)

    def graph_clear_column_mux(self):
        """
        Clear mux exclusions to allow different bit tests.
        """
        if self.column_mux_array:
            self.column_mux_array.init_graph_params()
