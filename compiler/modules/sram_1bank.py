# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import datetime
from math import ceil
from importlib import import_module, reload
from openram import debug
from openram.base import vector
from openram.base import channel_route
from openram.base import design
from openram.base import verilog
from openram.base import lef
from openram.router import router_tech
from openram.sram_factory import factory
from openram.tech import spice
from openram import OPTS, print_time


class sram_1bank(design, verilog, lef):
    """
    Procedures specific to a one bank SRAM.
    """
    def __init__(self, name, sram_config):
        design.__init__(self, name)
        lef.__init__(self, ["m1", "m2", "m3", "m4"])
        verilog.__init__(self)
        self.sram_config = sram_config
        sram_config.set_local_config(self)

        self.bank_insts = []

        if self.write_size != self.word_size:
            self.num_wmasks = int(ceil(self.word_size / self.write_size))
        else:
            self.num_wmasks = 0

        if not self.num_spare_cols:
            self.num_spare_cols = 0

        try:
            from openram.tech import power_grid
            self.supply_stack = power_grid
        except ImportError:
            # if no power_grid is specified by tech we use sensible defaults
            # Route a M3/M4 grid
            self.supply_stack = self.m3_stack

        # delay control logic does not have RBLs
        self.has_rbl = OPTS.control_logic != "control_logic_delay"

    def add_pins(self):
        """ Add pins for entire SRAM. """

        for port in self.write_ports:
            for bit in range(self.word_size + self.num_spare_cols):
                self.add_pin("din{0}[{1}]".format(port, bit), "INPUT")
        for port in self.all_ports:
            for bit in range(self.bank_addr_size):
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
            from openram.router import supply_grid_router as router
        else:
            from openram.router import supply_tree_router as router
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
                if self.write_size != self.word_size:
                    for bit in range(self.num_wmasks):
                        pins_to_route.append("wmask{0}[{1}]".format(port, bit))

            if port in self.write_ports:
                if self.num_spare_cols == 1:
                    pins_to_route.append("spare_wen{0}".format(port))
                else:
                    for bit in range(self.num_spare_cols):
                        pins_to_route.append("spare_wen{0}[{1}]".format(port, bit))

        from openram.router import signal_escape_router as router
        rtr=router(layers=self.m3_stack,
                   design=self,
                   bbox=bbox)
        rtr.escape_route(pins_to_route)

    def compute_bus_sizes(self):
        """ Compute the independent bus widths shared between two and four bank SRAMs """

        # address size + control signals + one-hot bank select signals
        self.num_vertical_line = self.bank_addr_size + self.control_size + 1# + log(self.num_banks, 2) + 1
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

            self.addr_bus_names=["A{0}[{1}]".format(port, i) for i in range(self.bank_addr_size)]
            self.vert_control_bus_positions.update(self.create_vertical_pin_bus(layer="m2",
                                                                                pitch=self.m2_pitch,
                                                                                offset=self.addr_bus_offset,
                                                                                names=self.addr_bus_names,
                                                                                length=self.addr_bus_height))

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

        if self.write_size != self.word_size:
            self.wmask_dff = factory.create("dff_array", module_name="wmask_dff", rows=1, columns=self.num_wmasks)

        if self.num_spare_cols:
            self.spare_wen_dff = factory.create("dff_array", module_name="spare_wen_dff", rows=1, columns=self.num_spare_cols)

        self.bank_count = 0

        c = reload(import_module("." + OPTS.control_logic, "openram.modules"))
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
        if self.has_rbl:
            for port in self.all_ports:
                temp.append("rbl_bl{0}".format(port))
        for port in self.write_ports:
            for bit in range(self.word_size + self.num_spare_cols):
                temp.append("bank_din{0}_{1}".format(port, bit))
        for port in self.all_ports:
            for bit in range(self.bank_addr_size):
                temp.append("a{0}_{1}".format(port, bit))
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
            if self.has_rbl:
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

        if self.write_size != self.word_size:
            self.wmask_dff_insts = self.create_wmask_dff()
            self.data_dff_insts = self.create_data_dff()
        else:
            self.data_dff_insts = self.create_data_dff()

        if self.num_spare_cols:
            self.spare_wen_dff_insts = self.create_spare_wen_dff()
        else:
            self.num_spare_cols = 0

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
        self.control_pos = [None] * len(self.all_ports)
        self.row_addr_pos = [None] * len(self.all_ports)

        # DFFs are placd on their own
        self.col_addr_pos = [None] * len(self.all_ports)
        self.wmask_pos = [None] * len(self.all_ports)
        self.spare_wen_pos = [None] * len(self.all_ports)
        self.data_pos = [None] * len(self.all_ports)

        # These positions utilize the channel route sizes.
        # FIXME: Auto-compute these rather than manual computation.
        # If a horizontal channel, they rely on the vertical channel non-preferred (contacted) pitch.
        # If a vertical channel, they rely on the horizontal channel non-preferred (contacted) pitch.
        # So, m3 non-pref pitch means that this is routed on the m2 layer.
        self.data_bus_gap = self.m4_nonpref_pitch * 2

        # Spare wen are on a separate layer so not included
        # Start with 1 track minimum
        self.data_bus_size = [1] * len(self.all_ports)
        self.col_addr_bus_size = [1] * len(self.all_ports)
        for port in self.all_ports:
            # The column address wires are routed separately from the data bus and will always be smaller.
            # All ports need the col addr flops
            self.col_addr_bus_size[port] = self.col_addr_size * self.m4_nonpref_pitch
            # Write ports need the data input flops and write mask flops
            if port in self.write_ports:
                self.data_bus_size[port] += self.num_wmasks + self.word_size
            # This is for the din pins that get routed in the same channel
            # when we have dout and din together
            if port in self.readwrite_ports:
                self.data_bus_size[port] += self.word_size
            # Convert to length
            self.data_bus_size[port] *= self.m4_nonpref_pitch
            # Add the gap in unit length
            self.data_bus_size[port] += self.data_bus_gap

        # The control and row addr flops are independent of any bus widths.
        self.place_control()
        self.place_row_addr_dffs()

        # Place with an initial wide channel (from above)
        self.place_dffs()

        # Route the channel and set to the new data bus size
        # We need to temporarily add some pins for the x offsets
        # but we'll remove them so that they have the right y
        # offsets after the DFF placement.
        self.add_layout_pins(add_vias=False)
        self.route_dffs(add_routes=False)
        self.remove_layout_pins()

        # Re-place with the new channel size
        self.place_dffs()

    def place_row_addr_dffs(self):
        """
        Must be run after place control logic.
        """
        port = 0
        # The row address bits are placed above the control logic aligned on the right.
        x_offset = self.control_logic_insts[port].rx() - self.row_addr_dff_insts[port].width
        # It is above the control logic and the predecoder array
        y_offset = max(self.control_logic_insts[port].uy(), self.bank.predecoder_top)

        self.row_addr_pos[port] = vector(x_offset, y_offset)
        self.row_addr_dff_insts[port].place(self.row_addr_pos[port])

        if len(self.all_ports)>1:
            port = 1
            # The row address bits are placed above the control logic aligned on the left.
            x_offset = self.control_pos[port].x - self.control_logic_insts[port].width + self.row_addr_dff_insts[port].width
            # If it can be placed above the predecoder and below the control logic, do it
            y_offset = self.bank.predecoder_bottom
            self.row_addr_pos[port] = vector(x_offset, y_offset)
            self.row_addr_dff_insts[port].place(self.row_addr_pos[port], mirror="XY")

    def place_control(self):
        port = 0

        # This includes 2 M2 pitches for the row addr clock line.
        # The delay line is aligned with the bitcell array while the control logic is aligned with the port_data
        # using the control_logic_center value.
        self.control_pos[port] = vector(-self.control_logic_insts[port].width - 2 * self.m2_pitch,
                                        self.bank.bank_array_ll.y - self.control_logic_insts[port].mod.control_logic_center.y)
        self.control_logic_insts[port].place(self.control_pos[port])
        if len(self.all_ports) > 1:
            port = 1
            # This includes 2 M2 pitches for the row addr clock line
            # The delay line is aligned with the bitcell array while the control logic is aligned with the port_data
            # using the control_logic_center value.
            self.control_pos[port] = vector(self.bank_inst.rx() + self.control_logic_insts[port].width + 2 * self.m2_pitch,
                                            self.bank.bank_array_ur.y
                                            + self.control_logic_insts[port].height
                                            - self.control_logic_insts[port].height
                                            + self.control_logic_insts[port].mod.control_logic_center.y)
            self.control_logic_insts[port].place(self.control_pos[port], mirror="XY")

    def place_dffs(self):
        """
        Place the col addr, data, wmask, and spare data DFFs.
        This can be run more than once after we recompute the channel width.
        """

        port = 0
        # Add the col address flops below the bank to the right of the control logic
        x_offset = self.control_logic_insts[port].rx() + self.dff.width
        # Place it a data bus below the x-axis, but at least as low as the control logic to not block
        # the control logic signals
        y_offset = min(-self.data_bus_size[port] - self.dff.height,
                       self.control_logic_insts[port].by())
        if self.col_addr_dff:
            self.col_addr_pos[port] = vector(x_offset,
                                             y_offset)
            self.col_addr_dff_insts[port].place(self.col_addr_pos[port])
            x_offset = self.col_addr_dff_insts[port].rx()
        else:
            self.col_addr_pos[port] = vector(x_offset, 0)

        if port in self.write_ports:
            if self.write_size != self.word_size:
                # Add the write mask flops below the write mask AND array.
                self.wmask_pos[port] = vector(x_offset,
                                              y_offset)
                self.wmask_dff_insts[port].place(self.wmask_pos[port])
                x_offset = self.wmask_dff_insts[port].rx()

            # Add the data flops below the write mask flops.
            self.data_pos[port] = vector(x_offset,
                                         y_offset)
            self.data_dff_insts[port].place(self.data_pos[port])
            x_offset = self.data_dff_insts[port].rx()

            # Add spare write enable flops to the right of data flops since the spare columns
            # will be on the right
            if self.num_spare_cols:
                self.spare_wen_pos[port] = vector(x_offset,
                                                  y_offset)
                self.spare_wen_dff_insts[port].place(self.spare_wen_pos[port])
                x_offset = self.spare_wen_dff_insts[port].rx()

        else:
            self.wmask_pos[port] = vector(x_offset, y_offset)
            self.data_pos[port] = vector(x_offset, y_offset)
            self.spare_wen_pos[port] = vector(x_offset, y_offset)

        if len(self.all_ports) > 1:
            port = 1

            # Add the col address flops below the bank to the right of the control logic
            x_offset = self.control_logic_insts[port].lx() - 2 * self.dff.width
            # Place it a data bus below the x-axis, but at least as high as the control logic to not block
            # the control logic signals
            y_offset = max(self.bank.height + self.data_bus_size[port] + self.dff.height,
                           self.control_logic_insts[port].uy() - self.dff.height)
            if self.col_addr_dff:
                self.col_addr_pos[port] = vector(x_offset,
                                                 y_offset)
                self.col_addr_dff_insts[port].place(self.col_addr_pos[port], mirror="XY")
                x_offset = self.col_addr_dff_insts[port].lx()
            else:
                self.col_addr_pos[port] = vector(x_offset, y_offset)

            if port in self.write_ports:
                # Add spare write enable flops to the right of the data flops since the spare
                # columns will be on the left
                if self.num_spare_cols:
                    self.spare_wen_pos[port] = vector(x_offset - self.spare_wen_dff_insts[port].width,
                                                      y_offset)
                    self.spare_wen_dff_insts[port].place(self.spare_wen_pos[port], mirror="MX")
                    x_offset = self.spare_wen_dff_insts[port].lx()

                if self.write_size != self.word_size:
                    # Add the write mask flops below the write mask AND array.
                    self.wmask_pos[port] = vector(x_offset - self.wmask_dff_insts[port].width,
                                                  y_offset)
                    self.wmask_dff_insts[port].place(self.wmask_pos[port], mirror="MX")
                    x_offset = self.wmask_dff_insts[port].lx()

                # Add the data flops below the write mask flops.
                self.data_pos[port] = vector(x_offset - self.data_dff_insts[port].width,
                                             y_offset)
                self.data_dff_insts[port].place(self.data_pos[port], mirror="MX")
        else:
            self.wmask_pos[port] = vector(x_offset, y_offset)
            self.data_pos[port] = vector(x_offset, y_offset)
            self.spare_wen_pos[port] = vector(x_offset, y_offset)

    def add_layout_pins(self, add_vias=True):
        """
        Add the top-level pins for a single bank SRAM with control.
        """
        for port in self.all_ports:
            # Hack: If we are escape routing, set the pin layer to
            # None so that we will start from the pin layer
            # Otherwise, set it as the pin layer so that no vias are added.
            # Otherwise, when we remove pins to move the dff array dynamically,
            # we will leave some remaining vias when the pin locations change.
            if add_vias:
                pin_layer = None
            else:
                pin_layer = self.pwr_grid_layers[0]

            # Connect the control pins as inputs
            for signal in self.control_logic_inputs[port]:
                if signal.startswith("rbl"):
                    continue
                self.add_io_pin(self.control_logic_insts[port],
                                signal,
                                signal + "{}".format(port),
                                start_layer=pin_layer)

            if port in self.write_ports:
                for bit in range(self.word_size + self.num_spare_cols):
                    self.add_io_pin(self.data_dff_insts[port],
                                    "din_{}".format(bit),
                                    "din{0}[{1}]".format(port, bit),
                                    start_layer=pin_layer)

            if port in self.readwrite_ports or port in self.read_ports:
                for bit in range(self.word_size + self.num_spare_cols):
                    self.add_io_pin(self.bank_inst,
                                    "dout{0}_{1}".format(port, bit),
                                    "dout{0}[{1}]".format(port, bit),
                                    start_layer=pin_layer)

            for bit in range(self.col_addr_size):
                self.add_io_pin(self.col_addr_dff_insts[port],
                                "din_{}".format(bit),
                                "addr{0}[{1}]".format(port, bit),
                                start_layer=pin_layer)

            for bit in range(self.row_addr_size):
                self.add_io_pin(self.row_addr_dff_insts[port],
                                "din_{}".format(bit),
                                "addr{0}[{1}]".format(port, bit + self.col_addr_size),
                                start_layer=pin_layer)

            if port in self.write_ports:
                if self.write_size != self.word_size:
                    for bit in range(self.num_wmasks):
                        self.add_io_pin(self.wmask_dff_insts[port],
                                        "din_{}".format(bit),
                                        "wmask{0}[{1}]".format(port, bit),
                                        start_layer=pin_layer)

            if port in self.write_ports:
                if self.num_spare_cols == 1:
                    self.add_io_pin(self.spare_wen_dff_insts[port],
                                    "din_{}".format(0),
                                    "spare_wen{0}".format(port),
                                    start_layer=pin_layer)
                else:
                    for bit in range(self.num_spare_cols):
                        self.add_io_pin(self.spare_wen_dff_insts[port],
                                        "din_{}".format(bit),
                                        "spare_wen{0}[{1}]".format(port, bit),
                                        start_layer=pin_layer)

    def route_layout(self):
        """ Route a single bank SRAM """

        self.route_clk()

        self.route_control_logic()

        self.route_row_addr_dff()

        self.route_dffs()

        # We add the vias to M3 before routing supplies because
        # they might create some blockages
        self.add_layout_pins()

        # Some technologies have an isolation
        self.add_dnwell(inflate=2.5)

        # Route the supplies together and/or to the ring/stripes.
        # This is done with the original bbox since the escape routes need to
        # be outside of the ring for OpenLane
        rt = router_tech(self.supply_stack, 1)
        init_bbox = self.get_bbox(side="ring",
                                  margin=rt.track_width)

        # We need the initial bbox for the supply rings later
        # because the perimeter pins will change the bbox
        # Route the pins to the perimeter
        if OPTS.perimeter_pins:
            # We now route the escape routes far enough out so that they will
            # reach past the power ring or stripes on the sides
            bbox = self.get_bbox(side="ring",
                                 margin=11*rt.track_width)
            self.route_escape_pins(bbox)

        self.route_supplies(init_bbox)


    def route_dffs(self, add_routes=True):

        for port in self.all_ports:
            self.route_dff(port, add_routes)

    def route_dff(self, port, add_routes):

        # This is only done when we add_routes because the data channel will be larger
        # so that can be used for area estimation.
        if add_routes:
            self.route_col_addr_dffs(port)

        self.route_data_dffs(port, add_routes)

    def route_col_addr_dffs(self, port):

        route_map = []

        # column mux dff is routed on it's own since it is to the far end
        # decoder inputs are min pitch M2, so need to use lower layer stack
        if self.col_addr_size > 0:
            dff_names = ["dout_{}".format(x) for x in range(self.col_addr_size)]
            dff_pins = [self.col_addr_dff_insts[port].get_pin(x) for x in dff_names]
            bank_names = ["addr{0}_{1}".format(port, x) for x in range(self.col_addr_size)]
            bank_pins = [self.bank_inst.get_pin(x) for x in bank_names]
            route_map.extend(list(zip(bank_pins, dff_pins)))

        if len(route_map) > 0:

            # This layer stack must be different than the data dff layer stack
            layer_stack = self.m1_stack

            if port == 0:
                offset = vector(self.control_logic_insts[port].rx() + self.dff.width,
                                - self.data_bus_size[port] + 2 * self.m3_pitch)
                cr = channel_route(netlist=route_map,
                                   offset=offset,
                                   layer_stack=layer_stack,
                                   parent=self)
                # This causes problem in magic since it sometimes cannot extract connectivity of instances
                # with no active devices.
                self.add_inst(cr.name, cr)
                self.connect_inst([])
                # self.add_flat_inst(cr.name, cr)
            else:
                offset = vector(0,
                                self.bank.height + self.m3_pitch)
                cr = channel_route(netlist=route_map,
                                   offset=offset,
                                   layer_stack=layer_stack,
                                   parent=self)
                # This causes problem in magic since it sometimes cannot extract connectivity of instances
                # with no active devices.
                self.add_inst(cr.name, cr)
                self.connect_inst([])
                # self.add_flat_inst(cr.name, cr)

    def route_data_dffs(self, port, add_routes):
        route_map = []

        # wmask dff
        if self.num_wmasks > 0 and port in self.write_ports:
            dff_names = ["dout_{}".format(x) for x in range(self.num_wmasks)]
            dff_pins = [self.wmask_dff_insts[port].get_pin(x) for x in dff_names]
            bank_names = ["bank_wmask{0}_{1}".format(port, x) for x in range(self.num_wmasks)]
            bank_pins = [self.bank_inst.get_pin(x) for x in bank_names]
            route_map.extend(list(zip(bank_pins, dff_pins)))

        if port in self.write_ports:
            # synchronized inputs from data dff
            dff_names = ["dout_{}".format(x) for x in range(self.word_size + self.num_spare_cols)]
            dff_pins = [self.data_dff_insts[port].get_pin(x) for x in dff_names]
            bank_names = ["din{0}_{1}".format(port, x) for x in range(self.word_size + self.num_spare_cols)]
            bank_pins = [self.bank_inst.get_pin(x) for x in bank_names]
            route_map.extend(list(zip(bank_pins, dff_pins)))

        # spare wen dff
        if self.num_spare_cols > 0 and port in self.write_ports:
            dff_names = ["dout_{}".format(x) for x in range(self.num_spare_cols)]
            dff_pins = [self.spare_wen_dff_insts[port].get_pin(x) for x in dff_names]
            bank_names = ["bank_spare_wen{0}_{1}".format(port, x) for x in range(self.num_spare_cols)]
            bank_pins = [self.bank_inst.get_pin(x) for x in bank_names]
            route_map.extend(list(zip(bank_pins, dff_pins)))

        if len(route_map) > 0:

            # This layer stack must be different than the column addr dff layer stack
            layer_stack = self.m3_stack
            if port == 0:
                # This is relative to the bank at 0,0 or the s_en which is routed on M3 also
                if "s_en" in self.control_logic_insts[port].mod.pin_map:
                    y_bottom = min(0, self.control_logic_insts[port].get_pin("s_en").by())
                else:
                    y_bottom = 0

                y_offset = y_bottom - self.data_bus_size[port] + 2 * self.m3_pitch
                offset = vector(self.control_logic_insts[port].rx() + self.dff.width,
                                y_offset)
                cr = channel_route(netlist=route_map,
                                   offset=offset,
                                   layer_stack=layer_stack,
                                   parent=self)
                if add_routes:
                    # This causes problem in magic since it sometimes cannot extract connectivity of instances
                    # with no active devices.
                    self.add_inst(cr.name, cr)
                    self.connect_inst([])
                    # self.add_flat_inst(cr.name, cr)
                else:
                    self.data_bus_size[port] = max(cr.height, self.col_addr_bus_size[port]) + self.data_bus_gap
            else:
                if "s_en" in self.control_logic_insts[port].mod.pin_map:
                    y_top = max(self.bank.height, self.control_logic_insts[port].get_pin("s_en").uy())
                else:
                    y_top = self.bank.height
                y_offset = y_top + self.m3_pitch
                offset = vector(0,
                                y_offset)
                cr = channel_route(netlist=route_map,
                                   offset=offset,
                                   layer_stack=layer_stack,
                                   parent=self)
                if add_routes:
                    # This causes problem in magic since it sometimes cannot extract connectivity of instances
                    # with no active devices.
                    self.add_inst(cr.name, cr)
                    self.connect_inst([])
                    # self.add_flat_inst(cr.name, cr)
                else:
                    self.data_bus_size[port] = max(cr.height, self.col_addr_bus_size[port]) + self.data_bus_gap

    def route_clk(self):
        """ Route the clock network """

        # This is the actual input to the SRAM
        for port in self.all_ports:
            # Connect all of these clock pins to the clock in the central bus
            # This is something like a "spine" clock distribution. The two spines
            # are clk_buf and clk_buf_bar
            control_clk_buf_pin = self.control_logic_insts[port].get_pin("clk_buf")
            control_clk_buf_pos = control_clk_buf_pin.center()

            # This uses a metal2 track to the right (for port0) of the control/row addr DFF
            # to route vertically. For port1, it is to the left.
            row_addr_clk_pin = self.row_addr_dff_insts[port].get_pin("clk")
            if port % 2:
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
            self.add_path(control_clk_buf_pin.layer, [control_clk_buf_pos, clk_steiner_pos])
            self.add_via_stack_center(from_layer=control_clk_buf_pin.layer,
                                      to_layer="m2",
                                      offset=clk_steiner_pos)

            # Note, the via to the control logic is taken care of above
            self.add_wire(self.m2_stack[::-1],
                          [row_addr_clk_pos, mid1_pos, clk_steiner_pos])

            if self.col_addr_dff:
                dff_clk_pin = self.col_addr_dff_insts[port].get_pin("clk")
                dff_clk_pos = dff_clk_pin.center()
                mid_pos = vector(clk_steiner_pos.x, dff_clk_pos.y)
                self.add_wire(self.m2_stack[::-1],
                              [dff_clk_pos, mid_pos, clk_steiner_pos])
            elif port in self.write_ports:
                data_dff_clk_pin = self.data_dff_insts[port].get_pin("clk")
                data_dff_clk_pos = data_dff_clk_pin.center()
                mid_pos = vector(clk_steiner_pos.x, data_dff_clk_pos.y)
                # In some designs, the steiner via will be too close to the mid_pos via
                # so make the wire as wide as the contacts
                self.add_path("m2",
                              [mid_pos, clk_steiner_pos],
                              width=max(self.m2_via.width, self.m2_via.height))
                self.add_wire(self.m2_stack[::-1],
                              [data_dff_clk_pos, mid_pos, clk_steiner_pos])

    def route_control_logic(self):
        """
        Route the control logic pins that are not inputs
        """

        for port in self.all_ports:
            for signal in self.control_logic_outputs[port]:
                # The clock gets routed separately and is not a part of the bank
                if "clk" in signal:
                    continue
                src_pin = self.control_logic_insts[port].get_pin(signal)
                dest_pin = self.bank_inst.get_pin(signal + "{}".format(port))
                self.connect_vbus(src_pin, dest_pin)

        if self.has_rbl:
            for port in self.all_ports:
                # Only input (besides pins) is the replica bitline
                src_pin = self.control_logic_insts[port].get_pin("rbl_bl")
                dest_pin = self.bank_inst.get_pin("rbl_bl_{0}_{0}".format(port))
                self.add_wire(self.m3_stack,
                              [src_pin.center(), vector(src_pin.cx(), dest_pin.cy()), dest_pin.rc()])
                self.add_via_stack_center(from_layer=src_pin.layer,
                                          to_layer="m4",
                                          offset=src_pin.center())
                self.add_via_stack_center(from_layer=dest_pin.layer,
                                          to_layer="m3",
                                          offset=dest_pin.center())

    def route_row_addr_dff(self):
        """
        Connect the output of the row flops to the bank pins
        """
        for port in self.all_ports:
            for bit in range(self.row_addr_size):
                flop_name = "dout_{}".format(bit)
                bank_name = "addr{0}_{1}".format(port, bit + self.col_addr_size)
                flop_pin = self.row_addr_dff_insts[port].get_pin(flop_name)
                bank_pin = self.bank_inst.get_pin(bank_name)
                flop_pos = flop_pin.center()
                bank_pos = bank_pin.center()
                mid_pos = vector(bank_pos.x, flop_pos.y)
                self.add_via_stack_center(from_layer=flop_pin.layer,
                                          to_layer="m3",
                                          offset=flop_pos)
                self.add_path("m3", [flop_pos, mid_pos])
                self.add_via_stack_center(from_layer=bank_pin.layer,
                                          to_layer="m3",
                                          offset=mid_pos)
                self.add_path(bank_pin.layer, [mid_pos, bank_pos])

    def add_lvs_correspondence_points(self):
        """
        This adds some points for easier debugging if LVS goes wrong.
        These should probably be turned off by default though, since extraction
        will show these as ports in the extracted netlist.
        """
        return
        for n in self.control_logic_outputs[0]:
            pin = self.control_logic_insts[0].get_pin(n)
            self.add_label(text=n,
                           layer=pin.layer,
                           offset=pin.center())

    def graph_exclude_data_dff(self):
        """
        Removes data dff and wmask dff (if applicable) from search graph.
        """
        # Data dffs and wmask dffs are only for writing so are not useful for evaluating read delay.
        for inst in self.data_dff_insts:
            self.graph_inst_exclude.add(inst)
        if self.write_size != self.word_size:
            for inst in self.wmask_dff_insts:
                self.graph_inst_exclude.add(inst)
        if self.num_spare_cols:
            for inst in self.spare_wen_dff_insts:
                self.graph_inst_exclude.add(inst)

    def graph_exclude_addr_dff(self):
        """
        Removes data dff from search graph.
        """
        # Address is considered not part of the critical path, subjectively removed
        for inst in self.row_addr_dff_insts:
            self.graph_inst_exclude.add(inst)

        if self.col_addr_dff:
            for inst in self.col_addr_dff_insts:
                self.graph_inst_exclude.add(inst)

    def graph_exclude_ctrl_dffs(self):
        """
        Exclude dffs for CSB, WEB, etc from graph
        """
        # Insts located in control logic, exclusion function called here
        for inst in self.control_logic_insts:
            inst.mod.graph_exclude_dffs()

    def get_cell_name(self, inst_name, row, col):
        """
        Gets the spice name of the target bitcell.
        """
        # Sanity check in case it was forgotten
        if inst_name.find("x") != 0:
            inst_name = "x" + inst_name
        return self.bank_inst.mod.get_cell_name(inst_name + "{}x".format(OPTS.hier_seperator) + self.bank_inst.name, row, col)

    def get_bank_num(self, inst_name, row, col):
        return 0
