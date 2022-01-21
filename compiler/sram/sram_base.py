# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import datetime
import debug
from math import log, ceil
from importlib import reload
from vector import vector
from globals import OPTS, print_time
from design import design
from verilog import verilog
from lef import lef
from sram_factory import factory
from tech import spice


class sram_base(design, verilog, lef):
    """
    Dynamically generated SRAM by connecting banks to control logic. The
    number of banks should be 1 , 2 or 4
    """
    def __init__(self, name, sram_config):
        design.__init__(self, name)
        lef.__init__(self, ["m1", "m2", "m3", "m4"])
        verilog.__init__(self)

        self.sram_config = sram_config
        sram_config.set_local_config(self)

        self.bank_insts = []

        if self.write_size:
            self.num_wmasks = int(ceil(self.word_size / self.write_size))
        else:
            self.num_wmasks = 0

        if not self.num_spare_cols:
            self.num_spare_cols = 0

        # For assigning only once the bbox
        self.bbox = None
        try:
            from tech import power_grid
            self.supply_stack = power_grid
        except ImportError:
            # if no power_grid is specified by tech we use sensible defaults
            # Route a M3/M4 grid
            self.supply_stack = self.m3_stack

    def add_pins(self):
        """ Add pins for entire SRAM. """

        for port in self.write_ports:
            for bit in range(self.word_size + self.num_spare_cols):
                self.add_pin("din{0}[{1}]".format(port, bit), "INPUT")

        for port in self.all_ports:
            for bit in range(self.addr_size):
                self.add_pin("addr{0}[{1}]".format(port, bit), "INPUT")

        # These are used to create the physical pins
        self.control_logic_inputs = []
        self.control_logic_outputs = []
        for port in self.all_ports:
            if port in self.readwrite_ports:
                self.control_logic_inputs.append(self.control_logic_rw.get_inputs())
                self.control_logic_outputs.append(self.control_logic_rw.get_outputs())
            elif port in self.write_ports:
                self.control_logic_inputs.append(self.control_logic_w.get_inputs())
                self.control_logic_outputs.append(self.control_logic_w.get_outputs())
            else:
                self.control_logic_inputs.append(self.control_logic_r.get_inputs())
                self.control_logic_outputs.append(self.control_logic_r.get_outputs())

        for port in self.all_ports:
            self.add_pin("csb{}".format(port), "INPUT")
        for port in self.readwrite_ports:
            self.add_pin("web{}".format(port), "INPUT")
        for port in self.all_ports:
            self.add_pin("clk{}".format(port), "INPUT")
        # add the optional write mask pins
        for port in self.write_ports:
            for bit in range(self.num_wmasks):
                self.add_pin("wmask{0}[{1}]".format(port, bit), "INPUT")
            if self.num_spare_cols == 1:
                self.add_pin("spare_wen{0}".format(port), "INPUT")
            else:
                for bit in range(self.num_spare_cols):
                    self.add_pin("spare_wen{0}[{1}]".format(port, bit), "INPUT")
        for port in self.read_ports:
            for bit in range(self.word_size + self.num_spare_cols):
                self.add_pin("dout{0}[{1}]".format(port, bit), "OUTPUT")

        # Standard supply and ground names
        try:
            self.vdd_name = spice["power"]
        except KeyError:
            self.vdd_name = "vdd"
        try:
            self.gnd_name = spice["ground"]
        except KeyError:
            self.gnd_name = "gnd"

        self.add_pin(self.vdd_name, "POWER")
        self.add_pin(self.gnd_name, "GROUND")
        self.ext_supplies = [self.vdd_name, self.gnd_name]
        self.ext_supply = {"vdd" : self.vdd_name, "gnd" : self.gnd_name}

    def add_global_pex_labels(self):
        """
        Add pex labels at the sram level for spice analysis
        """



        # add pex labels for bitcells
        for bank_num in range(len(self.bank_insts)):
            bank = self.bank_insts[bank_num]
            pex_data = bank.reverse_transformation_bitcell(self.bitcell.name)

            bank_offset = pex_data[0] # offset bank relative to sram
            Q_offset = pex_data[1] # offset of storage relative to bank
            Q_bar_offset = pex_data[2] # offset of storage relative to bank
            bl_offsets = pex_data[3]
            br_offsets = pex_data[4]
            bl_meta = pex_data[5]
            br_meta = pex_data[6]

            bl = []
            br = []

            storage_layer_name = "m1"
            bitline_layer_name = self.bitcell.get_pin("bl").layer

            for cell in range(len(bank_offset)):
                Q = [bank_offset[cell][0] + Q_offset[cell][0],
                     bank_offset[cell][1] + Q_offset[cell][1]]
                Q_bar = [bank_offset[cell][0] + Q_bar_offset[cell][0],
                         bank_offset[cell][1] + Q_bar_offset[cell][1]]
                OPTS.words_per_row = self.words_per_row
                row = int(cell % (OPTS.num_words / self.words_per_row))
                col = int(cell / (OPTS.num_words))
                self.add_layout_pin_rect_center("bitcell_Q_b{}_r{}_c{}".format(bank_num,
                                                                               row,
                                                                               col),
                                                                               storage_layer_name,
                                                                               Q)
                self.add_layout_pin_rect_center("bitcell_Q_bar_b{}_r{}_c{}".format(bank_num,
                                                                                   row,
                                                                                   col),
                                                                                   storage_layer_name,
                                                                                   Q_bar)

            for cell in range(len(bl_offsets)):
                col = bl_meta[cell][0][2]
                for bitline in range(len(bl_offsets[cell])):
                    bitline_location = [float(bank_offset[cell][0]) + bl_offsets[cell][bitline][0],
                                        float(bank_offset[cell][1]) + bl_offsets[cell][bitline][1]]
                    bl.append([bitline_location, bl_meta[cell][bitline][3], col])

            for cell in range(len(br_offsets)):
                col = br_meta[cell][0][2]
                for bitline in range(len(br_offsets[cell])):
                    bitline_location = [float(bank_offset[cell][0]) + br_offsets[cell][bitline][0],
                                        float(bank_offset[cell][1]) + br_offsets[cell][bitline][1]]
                    br.append([bitline_location, br_meta[cell][bitline][3], col])

            for i in range(len(bl)):
                self.add_layout_pin_rect_center("bl{0}_{1}".format(bl[i][1], bl[i][2]),
                                                bitline_layer_name, bl[i][0])

            for i in range(len(br)):
                self.add_layout_pin_rect_center("br{0}_{1}".format(br[i][1], br[i][2]),
                                                bitline_layer_name, br[i][0])

        # add pex labels for control logic
        for i in range(len(self.control_logic_insts)):
            instance = self.control_logic_insts[i]
            control_logic_offset = instance.offset
            for output in instance.mod.output_list:
                pin = instance.mod.get_pin(output)
                pin.transform([0, 0], instance.mirror, instance.rotate)
                offset = [control_logic_offset[0] + pin.center()[0],
                          control_logic_offset[1] + pin.center()[1]]
                self.add_layout_pin_rect_center("{0}{1}".format(pin.name, i),
                                                storage_layer_name,
                                                offset)

    def create_netlist(self):
        """ Netlist creation """

        start_time = datetime.datetime.now()

        # Must create the control logic before pins to get the pins
        self.add_modules()
        self.add_pins()
        self.create_modules()

        # This is for the lib file if we don't create layout
        self.width=0
        self.height=0

        if not OPTS.is_unit_test:
            print_time("Submodules", datetime.datetime.now(), start_time)

    def create_layout(self):
        """ Layout creation """
        start_time = datetime.datetime.now()
        self.place_instances()
        if not OPTS.is_unit_test:
            print_time("Placement", datetime.datetime.now(), start_time)

        start_time = datetime.datetime.now()
        self.route_layout()

        if not OPTS.is_unit_test:
            print_time("Routing", datetime.datetime.now(), start_time)

        self.add_lvs_correspondence_points()

        self.offset_all_coordinates()

        highest_coord = self.find_highest_coords()
        self.width = highest_coord[0]
        self.height = highest_coord[1]
        if OPTS.use_pex and OPTS.pex_exe[0] != "calibre":
            debug.info(2, "adding global pex labels")
            self.add_global_pex_labels()
        self.add_boundary(ll=vector(0, 0),
                          ur=vector(self.width, self.height))

        start_time = datetime.datetime.now()
        if not OPTS.is_unit_test:
            # We only enable final verification if we have routed the design
            # Only run this if not a unit test, because unit test will also verify it.
            self.DRC_LVS(final_verification=OPTS.route_supplies, force_check=OPTS.check_lvsdrc)
            print_time("Verification", datetime.datetime.now(), start_time)

    def create_modules(self):
        debug.error("Must override pure virtual function.", -1)

    def route_supplies(self, bbox=None):
        """ Route the supply grid and connect the pins to them. """

        # Copy the pins to the top level
        # This will either be used to route or left unconnected.
        for pin_name in ["vdd", "gnd"]:
            for inst in self.insts:
                self.copy_power_pins(inst, pin_name, self.ext_supply[pin_name])

        if not OPTS.route_supplies:
            # Do not route the power supply (leave as must-connect pins)
            return
        elif OPTS.route_supplies == "grid":
            from supply_grid_router import supply_grid_router as router
        else:
            from supply_tree_router import supply_tree_router as router
        rtr=router(layers=self.supply_stack,
                   design=self,
                   bbox=bbox,
                   pin_type=OPTS.supply_pin_type)

        rtr.route()

        if OPTS.supply_pin_type in ["left", "right", "top", "bottom", "ring"]:
            # Find the lowest leftest pin for vdd and gnd
            for pin_name in ["vdd", "gnd"]:
                # Copy the pin shape(s) to rectangles
                for pin in self.get_pins(pin_name):
                    self.add_rect(pin.layer,
                                  pin.ll(),
                                  pin.width(),
                                  pin.height())

                # Remove the pin shape(s)
                self.remove_layout_pin(pin_name)

                # Get new pins
                pins = rtr.get_new_pins(pin_name)
                for pin in pins:
                    self.add_layout_pin(self.ext_supply[pin_name],
                                        pin.layer,
                                        pin.ll(),
                                        pin.width(),
                                        pin.height())

        elif OPTS.route_supplies and OPTS.supply_pin_type == "single":
            # Update these as we may have routed outside the region (perimeter pins)
            lowest_coord = self.find_lowest_coords()

            # Find the lowest leftest pin for vdd and gnd
            for pin_name in ["vdd", "gnd"]:
                # Copy the pin shape(s) to rectangles
                for pin in self.get_pins(pin_name):
                    self.add_rect(pin.layer,
                                  pin.ll(),
                                  pin.width(),
                                  pin.height())

                # Remove the pin shape(s)
                self.remove_layout_pin(pin_name)

                # Get the lowest, leftest pin
                pin = rtr.get_ll_pin(pin_name)

                pin_width = 2 * getattr(self, "{}_width".format(pin.layer))

                # Add it as an IO pin to the perimeter
                route_width = pin.rx() - lowest_coord.x
                pin_offset = vector(lowest_coord.x, pin.by())
                self.add_rect(pin.layer,
                              pin_offset,
                              route_width,
                              pin.height())

                self.add_layout_pin(self.ext_supply[pin_name],
                                    pin.layer,
                                    pin_offset,
                                    pin_width,
                                    pin.height())
        else:
            # Grid is left with many top level pins
            pass

    def route_escape_pins(self, bbox):
        """
        Add the top-level pins for a single bank SRAM with control.
        """

        # List of pin to new pin name
        pins_to_route = []
        for port in self.all_ports:
            # Connect the control pins as inputs
            for signal in self.control_logic_inputs[port]:
                if signal.startswith("rbl"):
                    continue
                if signal=="clk":
                    pins_to_route.append("{0}{1}".format(signal, port))
                else:
                    pins_to_route.append("{0}{1}".format(signal, port))

            if port in self.write_ports:
                for bit in range(self.word_size + self.num_spare_cols):
                    pins_to_route.append("din{0}[{1}]".format(port, bit))

            if port in self.readwrite_ports or port in self.read_ports:
                for bit in range(self.word_size + self.num_spare_cols):
                    pins_to_route.append("dout{0}[{1}]".format(port, bit))

            for bit in range(self.col_addr_size):
                pins_to_route.append("addr{0}[{1}]".format(port, bit))

            for bit in range(self.row_addr_size):
                pins_to_route.append("addr{0}[{1}]".format(port, bit + self.col_addr_size))

            if port in self.write_ports:
                if self.write_size:
                    for bit in range(self.num_wmasks):
                        pins_to_route.append("wmask{0}[{1}]".format(port, bit))

            if port in self.write_ports:
                if self.num_spare_cols == 1:
                    pins_to_route.append("spare_wen{0}".format(port))
                else:
                    for bit in range(self.num_spare_cols):
                        pins_to_route.append("spare_wen{0}[{1}]".format(port, bit))

        from signal_escape_router import signal_escape_router as router
        rtr=router(layers=self.m3_stack,
                   design=self,
                   bbox=bbox)
        rtr.escape_route(pins_to_route)
        self.bbox = (rtr.ll, rtr.ur) # Capture the bbox after done with the escape routes, as can increase

    def compute_bus_sizes(self):
        """ Compute the independent bus widths shared between two and four bank SRAMs """

        # address size + control signals + one-hot bank select signals
        self.num_vertical_line = self.addr_size + self.control_size + log(self.num_banks, 2) + 1
        # data bus size
        self.num_horizontal_line = self.word_size

        self.vertical_bus_width = self.m2_pitch * self.num_vertical_line
        # vertical bus height depends on 2 or 4 banks

        self.data_bus_height = self.m3_pitch * self.num_horizontal_line
        self.data_bus_width = 2 * (self.bank.width + self.bank_to_bus_distance) + self.vertical_bus_width

        self.control_bus_height = self.m1_pitch * (self.control_size + 2)
        self.control_bus_width = self.bank.width + self.bank_to_bus_distance + self.vertical_bus_width

        self.supply_bus_height = self.m1_pitch * 2 # 2 for vdd/gnd placed with control bus
        self.supply_bus_width = self.data_bus_width

        # Sanity check to ensure we can fit the control logic above a single bank (0.9 is a hack really)
        debug.check(self.bank.width + self.vertical_bus_width > 0.9 * self.control_logic.width,
                    "Bank is too small compared to control logic.")

    def add_busses(self):
        """ Add the horizontal and vertical busses """
        # Vertical bus
        # The order of the control signals on the control bus:
        self.control_bus_names = []
        for port in self.all_ports:
            self.control_bus_names[port] = ["clk_buf{}".format(port)]
            wen = "w_en{}".format(port)
            sen = "s_en{}".format(port)
            pen = "p_en_bar{}".format(port)
            if self.port_id[port] == "r":
                self.control_bus_names[port].extend([sen, pen])
            elif self.port_id[port] == "w":
                self.control_bus_names[port].extend([wen, pen])
            else:
                self.control_bus_names[port].extend([sen, wen, pen])
            self.vert_control_bus_positions = self.create_vertical_bus(layer="m2",
                                                                       pitch=self.m2_pitch,
                                                                       offset=self.vertical_bus_offset,
                                                                       names=self.control_bus_names[port],
                                                                       length=self.vertical_bus_height)

            self.addr_bus_names=["A{0}[{1}]".format(port, i) for i in range(self.addr_size)]
            self.vert_control_bus_positions.update(self.create_vertical_pin_bus(layer="m2",
                                                                                pitch=self.m2_pitch,
                                                                                offset=self.addr_bus_offset,
                                                                                names=self.addr_bus_names,
                                                                                length=self.addr_bus_height))

            self.bank_sel_bus_names = ["bank_sel{0}_{1}".format(port, i) for i in range(self.num_banks)]
            self.vert_control_bus_positions.update(self.create_vertical_pin_bus(layer="m2",
                                                                                pitch=self.m2_pitch,
                                                                                offset=self.bank_sel_bus_offset,
                                                                                names=self.bank_sel_bus_names,
                                                                                length=self.vertical_bus_height))

            # Horizontal data bus
            self.data_bus_names = ["DATA{0}[{1}]".format(port, i) for i in range(self.word_size)]
            self.data_bus_positions = self.create_horizontal_pin_bus(layer="m3",
                                                                     pitch=self.m3_pitch,
                                                                     offset=self.data_bus_offset,
                                                                     names=self.data_bus_names,
                                                                     length=self.data_bus_width)

            # Horizontal control logic bus
            # vdd/gnd in bus go along whole SRAM
            # FIXME: Fatten these wires?
            self.horz_control_bus_positions = self.create_horizontal_bus(layer="m1",
                                                                         pitch=self.m1_pitch,
                                                                         offset=self.supply_bus_offset,
                                                                         names=["vdd"],
                                                                         length=self.supply_bus_width)
            # The gnd rail must not be the entire width since we protrude the right-most vdd rail up for
            # the decoder in 4-bank SRAMs
            self.horz_control_bus_positions.update(self.create_horizontal_bus(layer="m1",
                                                                              pitch=self.m1_pitch,
                                                                              offset=self.supply_bus_offset + vector(0, self.m1_pitch),
                                                                              names=["gnd"],
                                                                              length=self.supply_bus_width))
            self.horz_control_bus_positions.update(self.create_horizontal_bus(layer="m1",
                                                                              pitch=self.m1_pitch,
                                                                              offset=self.control_bus_offset,
                                                                              names=self.control_bus_names[port],
                                                                              length=self.control_bus_width))

    def add_multi_bank_modules(self):
        """ Create the multibank address flops and bank decoder """
        from dff_buf_array import dff_buf_array
        self.msb_address = dff_buf_array(name="msb_address",
                                         rows=1,
                                         columns=self.num_banks / 2)

        if self.num_banks>2:
            self.msb_decoder = self.bank.decoder.pre2_4

    def add_modules(self):
        self.bitcell = factory.create(module_type=OPTS.bitcell)
        self.dff = factory.create(module_type="dff")

        # Create the bank module (up to four are instantiated)
        self.bank = factory.create("bank", sram_config=self.sram_config, module_name="bank")

        self.num_spare_cols = self.bank.num_spare_cols

        # Create the address and control flops (but not the clk)
        self.row_addr_dff = factory.create("dff_array", module_name="row_addr_dff", rows=self.row_addr_size, columns=1)

        if self.col_addr_size > 0:
            self.col_addr_dff = factory.create("dff_array", module_name="col_addr_dff", rows=1, columns=self.col_addr_size)
        else:
            self.col_addr_dff = None

        self.data_dff = factory.create("dff_array", module_name="data_dff", rows=1, columns=self.word_size + self.num_spare_cols)

        if self.write_size:
            self.wmask_dff = factory.create("dff_array", module_name="wmask_dff", rows=1, columns=self.num_wmasks)

        if self.num_spare_cols:
            self.spare_wen_dff = factory.create("dff_array", module_name="spare_wen_dff", rows=1, columns=self.num_spare_cols)

        # Create bank decoder
        if(self.num_banks > 1):
            self.add_multi_bank_modules()

        self.bank_count = 0

        c = reload(__import__(OPTS.control_logic))
        self.mod_control_logic = getattr(c, OPTS.control_logic)

        # Create the control logic module for each port type
        if len(self.readwrite_ports) > 0:
            self.control_logic_rw = self.mod_control_logic(num_rows=self.num_rows,
                                                           words_per_row=self.words_per_row,
                                                           word_size=self.word_size,
                                                           spare_columns=self.num_spare_cols,
                                                           sram=self,
                                                           port_type="rw")
        if len(self.writeonly_ports) > 0:
            self.control_logic_w = self.mod_control_logic(num_rows=self.num_rows,
                                                          words_per_row=self.words_per_row,
                                                          word_size=self.word_size,
                                                          spare_columns=self.num_spare_cols,
                                                          sram=self,
                                                          port_type="w")
        if len(self.readonly_ports) > 0:
            self.control_logic_r = self.mod_control_logic(num_rows=self.num_rows,
                                                          words_per_row=self.words_per_row,
                                                          word_size=self.word_size,
                                                          spare_columns=self.num_spare_cols,
                                                          sram=self,
                                                          port_type="r")

    def create_bank(self, bank_num):
        """ Create a bank  """
        self.bank_insts.append(self.add_inst(name="bank{0}".format(bank_num),
                                             mod=self.bank))

        temp = []
        for port in self.read_ports:
            for bit in range(self.word_size + self.num_spare_cols):
                temp.append("dout{0}[{1}]".format(port, bit))
        for port in self.all_ports:
            temp.append("rbl_bl{0}".format(port))
        for port in self.write_ports:
            for bit in range(self.word_size + self.num_spare_cols):
                temp.append("bank_din{0}_{1}".format(port, bit))
        for port in self.all_ports:
            for bit in range(self.bank_addr_size):
                temp.append("a{0}_{1}".format(port, bit))
        if(self.num_banks > 1):
            for port in self.all_ports:
                temp.append("bank_sel{0}_{1}".format(port, bank_num))
        for port in self.read_ports:
            temp.append("s_en{0}".format(port))
        for port in self.all_ports:
            temp.append("p_en_bar{0}".format(port))
        for port in self.write_ports:
            temp.append("w_en{0}".format(port))
            for bit in range(self.num_wmasks):
                temp.append("bank_wmask{0}_{1}".format(port, bit))
            for bit in range(self.num_spare_cols):
                temp.append("bank_spare_wen{0}_{1}".format(port, bit))
        for port in self.all_ports:
            temp.append("wl_en{0}".format(port))
        temp.extend(self.ext_supplies)
        self.connect_inst(temp)

        return self.bank_insts[-1]

    def place_bank(self, bank_inst, position, x_flip, y_flip):
        """ Place a bank at the given position with orientations """

        # x_flip ==  1 --> no flip in x_axis
        # x_flip == -1 --> flip in x_axis
        # y_flip ==  1 --> no flip in y_axis
        # y_flip == -1 --> flip in y_axis

        # x_flip and y_flip are used for position translation

        if x_flip == -1 and y_flip == -1:
            bank_rotation = 180
        else:
            bank_rotation = 0

        if x_flip == y_flip:
            bank_mirror = "R0"
        elif x_flip == -1:
            bank_mirror = "MX"
        elif y_flip == -1:
            bank_mirror = "MY"
        else:
            bank_mirror = "R0"

        bank_inst.place(offset=position,
                        mirror=bank_mirror,
                        rotate=bank_rotation)

        return bank_inst

    def create_row_addr_dff(self):
        """ Add all address flops for the main decoder """
        insts = []
        for port in self.all_ports:
            insts.append(self.add_inst(name="row_address{}".format(port),
                                       mod=self.row_addr_dff))

            # inputs, outputs/output/bar
            inputs = []
            outputs = []
            for bit in range(self.row_addr_size):
                inputs.append("addr{}[{}]".format(port, bit + self.col_addr_size))
                outputs.append("a{}_{}".format(port, bit + self.col_addr_size))

            self.connect_inst(inputs + outputs + ["clk_buf{}".format(port)] + self.ext_supplies)

        return insts

    def create_col_addr_dff(self):
        """ Add and place all address flops for the column decoder """
        insts = []
        for port in self.all_ports:
            insts.append(self.add_inst(name="col_address{}".format(port),
                                       mod=self.col_addr_dff))

            # inputs, outputs/output/bar
            inputs = []
            outputs = []
            for bit in range(self.col_addr_size):
                inputs.append("addr{}[{}]".format(port, bit))
                outputs.append("a{}_{}".format(port, bit))

            self.connect_inst(inputs + outputs + ["clk_buf{}".format(port)] + self.ext_supplies)

        return insts

    def create_data_dff(self):
        """ Add and place all data flops """
        insts = []
        for port in self.all_ports:
            if port in self.write_ports:
                insts.append(self.add_inst(name="data_dff{}".format(port),
                                           mod=self.data_dff))
            else:
                insts.append(None)
                continue

            # inputs, outputs/output/bar
            inputs = []
            outputs = []
            for bit in range(self.word_size + self.num_spare_cols):
                inputs.append("din{}[{}]".format(port, bit))
                outputs.append("bank_din{}_{}".format(port, bit))

            self.connect_inst(inputs + outputs + ["clk_buf{}".format(port)] + self.ext_supplies)

        return insts

    def create_wmask_dff(self):
        """ Add and place all wmask flops """
        insts = []
        for port in self.all_ports:
            if port in self.write_ports:
                insts.append(self.add_inst(name="wmask_dff{}".format(port),
                                           mod=self.wmask_dff))
            else:
                insts.append(None)
                continue

            # inputs, outputs/output/bar
            inputs = []
            outputs = []
            for bit in range(self.num_wmasks):
                inputs.append("wmask{}[{}]".format(port, bit))
                outputs.append("bank_wmask{}_{}".format(port, bit))

            self.connect_inst(inputs + outputs + ["clk_buf{}".format(port)] + self.ext_supplies)

        return insts

    def create_spare_wen_dff(self):
        """ Add all spare write enable flops """
        insts = []
        for port in self.all_ports:
            if port in self.write_ports:
                insts.append(self.add_inst(name="spare_wen_dff{}".format(port),
                                           mod=self.spare_wen_dff))
            else:
                insts.append(None)
                continue

            # inputs, outputs/output/bar
            inputs = []
            outputs = []
            for bit in range(self.num_spare_cols):
                inputs.append("spare_wen{}[{}]".format(port, bit))
                outputs.append("bank_spare_wen{}_{}".format(port, bit))

            self.connect_inst(inputs + outputs + ["clk_buf{}".format(port)] + self.ext_supplies)

        return insts

    def create_control_logic(self):
        """ Add control logic instances """

        insts = []
        for port in self.all_ports:
            if port in self.readwrite_ports:
                mod = self.control_logic_rw
            elif port in self.write_ports:
                mod = self.control_logic_w
            else:
                mod = self.control_logic_r

            insts.append(self.add_inst(name="control{}".format(port), mod=mod))

            # Inputs
            temp = ["csb{}".format(port)]
            if port in self.readwrite_ports:
                temp.append("web{}".format(port))
            temp.append("clk{}".format(port))
            temp.append("rbl_bl{}".format(port))

            # Outputs
            if port in self.read_ports:
                temp.append("s_en{}".format(port))
            if port in self.write_ports:
                temp.append("w_en{}".format(port))
            temp.append("p_en_bar{}".format(port))
            temp.extend(["wl_en{}".format(port), "clk_buf{}".format(port)] + self.ext_supplies)
            self.connect_inst(temp)

        return insts

    def sp_write(self, sp_name, lvs=False, trim=False):
        # Write the entire spice of the object to the file
        ############################################################
        # Spice circuit
        ############################################################
        sp = open(sp_name, 'w')

        sp.write("**************************************************\n")
        sp.write("* OpenRAM generated memory.\n")
        sp.write("* Words: {}\n".format(self.num_words))
        sp.write("* Data bits: {}\n".format(self.word_size))
        sp.write("* Banks: {}\n".format(self.num_banks))
        sp.write("* Column mux: {}:1\n".format(self.words_per_row))
        sp.write("* Trimmed: {}\n".format(trim))
        sp.write("* LVS: {}\n".format(lvs))
        sp.write("**************************************************\n")
        # This causes unit test mismatch

        # sp.write("* Created: {0}\n".format(datetime.datetime.now()))
        # sp.write("* User: {0}\n".format(getpass.getuser()))
        # sp.write(".global {0} {1}\n".format(spice["vdd_name"],
        #                                     spice["gnd_name"]))
        usedMODS = list()
        self.sp_write_file(sp, usedMODS, lvs=lvs, trim=trim)
        del usedMODS
        sp.close()

    def graph_exclude_bits(self, targ_row, targ_col):
        """
        Excludes bits in column from being added to graph except target
        """
        self.bank.graph_exclude_bits(targ_row, targ_col)

    def clear_exclude_bits(self):
        """
        Clears the bit exclusions
        """
        self.bank.clear_exclude_bits()

    def graph_exclude_column_mux(self, column_include_num, port):
        """
        Excludes all columns muxes unrelated to the target bit being simulated.
        """
        self.bank.graph_exclude_column_mux(column_include_num, port)

    def graph_clear_column_mux(self, port):
        """
        Clear mux exclusions to allow different bit tests.
        """
        self.bank.graph_clear_column_mux(port)
