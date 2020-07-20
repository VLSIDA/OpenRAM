# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
from vector import vector
from sram_base import sram_base
from contact import m2_via
from globals import OPTS
import channel_route


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
        self.route_dffs(add_routes=False)
        # Re-place with the new channel size
        self.place_dffs()
        # Now route the channel
        self.route_dffs()

    def place_row_addr_dffs(self):
        """
        Must be run after place control logic.
        """
        port = 0
        # The row address bits are placed above the control logic aligned on the right.
        x_offset = self.control_logic_insts[port].rx() - self.row_addr_dff_insts[port].width
        # It is above the control logic but below the top of the bitcell array
        y_offset = max(self.control_logic_insts[port].uy(), self.bank_inst.uy() - self.row_addr_dff_insts[port].height)
        self.row_addr_pos[port] = vector(x_offset, y_offset)
        self.row_addr_dff_insts[port].place(self.row_addr_pos[port])

        if len(self.all_ports)>1:
            port = 1
            # The row address bits are placed above the control logic aligned on the left.
            x_offset = self.control_pos[port].x - self.control_logic_insts[port].width + self.row_addr_dff_insts[port].width
            # It is below the control logic but below the bottom of the bitcell array
            y_offset = min(self.control_logic_insts[port].by(), self.bank_inst.by() + self.row_addr_dff_insts[port].height)
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
        y_offset = - self.data_bus_size[port] - self.dff.height
        if self.col_addr_dff:
            self.col_addr_pos[port] = vector(x_offset,
                                             y_offset)
            self.col_addr_dff_insts[port].place(self.col_addr_pos[port])
            x_offset = self.col_addr_dff_insts[port].rx()
        else:
            self.col_addr_pos[port] = vector(x_offset, 0)
            
        if port in self.write_ports:
            if self.write_size:
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
            y_offset = self.bank.height + self.data_bus_size[port] + self.dff.height
            if self.col_addr_dff:
                self.col_addr_pos[port] = vector(x_offset,
                                                 y_offset)
                self.col_addr_dff_insts[port].place(self.col_addr_pos[port], mirror="XY")
                x_offset = self.col_addr_dff_insts[port].lx() - self.col_addr_dff_insts[port].width
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

                if self.write_size:
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

    def add_layout_pins(self):
        """
        Add the top-level pins for a single bank SRAM with control.
        """
        highest_coord = self.find_highest_coords()
        lowest_coord = self.find_lowest_coords()
        bbox = [lowest_coord, highest_coord]
        
        for port in self.all_ports:
            # Depending on the port, use the bottom/top or left/right sides
            # Port 0 is left/bottom
            # Port 1 is right/top
            bottom_or_top = "bottom" if port==0 else "top"
            left_or_right = "left" if port==0 else "right"

            # Connect the control pins as inputs
            for signal in self.control_logic_inputs[port]:
                if signal == "clk":
                    continue
                if OPTS.perimeter_pins:
                    self.add_perimeter_pin(name=signal + "{}".format(port),
                                           pin=self.control_logic_insts[port].get_pin(signal),
                                           side=left_or_right,
                                           bbox=bbox)
                else:
                    self.copy_layout_pin(self.control_logic_insts[port],
                                         signal,
                                         signal + "{}".format(port))

            if OPTS.perimeter_pins:
                self.add_perimeter_pin(name="clk{}".format(port),
                                       pin=self.control_logic_insts[port].get_pin("clk"),
                                       side=bottom_or_top,
                                       bbox=bbox)
            else:
                self.copy_layout_pin(self.control_logic_insts[port],
                                     "clk",
                                     "clk{}".format(port))

            # Data input pins go to BOTTOM/TOP
            din_ports = []
            if port in self.write_ports:
                for bit in range(self.word_size + self.num_spare_cols):
                    if OPTS.perimeter_pins:
                        p = self.add_perimeter_pin(name="din{0}[{1}]".format(port, bit),
                                                   pin=self.data_dff_insts[port].get_pin("din_{0}".format(bit)),
                                                   side=bottom_or_top,
                                                   bbox=bbox)
                        din_ports.append(p)
                    else:
                        self.copy_layout_pin(self.data_dff_insts[port],
                                             "din_{}".format(bit),
                                             "din{0}[{1}]".format(port, bit))
                        
            # Data output pins go to BOTTOM/TOP
            if port in self.readwrite_ports and OPTS.perimeter_pins:
                for bit in range(self.word_size + self.num_spare_cols):
                    # This should be routed next to the din pin
                    p = din_ports[bit]
                    self.add_layout_pin_rect_center(text="dout{0}[{1}]".format(port, bit),
                                                    layer=p.layer,
                                                    offset=p.center() + vector(self.m3_pitch, 0),
                                                    width=p.width(),
                                                    height=p.height())
            elif port in self.read_ports:
                for bit in range(self.word_size + self.num_spare_cols):
                    if OPTS.perimeter_pins:
                        # This should have a clear route to the perimeter if there are no din routes
                        self.add_perimeter_pin(name="dout{0}[{1}]".format(port, bit),
                                               pin=self.bank_inst.get_pin("dout{0}_{1}".format(port, bit)),
                                               side=bottom_or_top,
                                               bbox=bbox)
                    else:
                        self.copy_layout_pin(self.bank_inst,
                                             "dout{0}_{1}".format(port, bit),
                                             "dout{0}[{1}]".format(port, bit))
                    
                        

            # Lower address bits go to BOTTOM/TOP
            for bit in range(self.col_addr_size):
                if OPTS.perimeter_pins:
                    self.add_perimeter_pin(name="addr{0}[{1}]".format(port, bit),
                                           pin=self.col_addr_dff_insts[port].get_pin("din_{}".format(bit)),
                                           side=bottom_or_top,
                                           bbox=bbox)
                else:
                    self.copy_layout_pin(self.col_addr_dff_insts[port],
                                         "din_{}".format(bit),
                                         "addr{0}[{1}]".format(port, bit))
                
            # Upper address bits go to LEFT/RIGHT
            for bit in range(self.row_addr_size):
                if OPTS.perimeter_pins:
                    self.add_perimeter_pin(name="addr{0}[{1}]".format(port, bit + self.col_addr_size),
                                           pin=self.row_addr_dff_insts[port].get_pin("din_{}".format(bit)),
                                           side=left_or_right,
                                           bbox=bbox)
                else:
                    self.copy_layout_pin(self.row_addr_dff_insts[port],
                                         "din_{}".format(bit),
                                         "addr{0}[{1}]".format(port, bit + self.col_addr_size))
                    
            # Write mask pins go to BOTTOM/TOP
            if port in self.write_ports:
                if self.write_size:
                    for bit in range(self.num_wmasks):
                        if OPTS.perimeter_pins:
                            self.add_perimeter_pin(name="wmask{0}[{1}]".format(port, bit),
                                                   pin=self.wmask_dff_insts[port].get_pin("din_{}".format(bit)),
                                                   side=bottom_or_top,
                                                   bbox=bbox)
                        else:
                            self.copy_layout_pin(self.wmask_dff_insts[port],
                                                 "din_{}".format(bit),
                                                 "wmask{0}[{1}]".format(port, bit))

            # Spare wen pins go to BOTTOM/TOP
            if port in self.write_ports:
                for bit in range(self.num_spare_cols):
                    if OPTS.perimeter_pins:
                        self.add_perimeter_pin(name="spare_wen{0}[{1}]".format(port, bit),
                                               pin=self.spare_wen_dff_insts[port].get_pin("din_{}".format(bit)),
                                               side=left_or_right,
                                               bbox=bbox)
                    else:
                        self.copy_layout_pin(self.spare_wen_dff_insts[port],
                                             "din_{}".format(bit),
                                             "spare_wen{0}[{1}]".format(port, bit))

    def route_layout(self):
        """ Route a single bank SRAM """

        self.add_layout_pins()

        self.route_clk()
        
        self.route_control_logic()
        
        self.route_row_addr_dff()

    def route_dffs(self, add_routes=True):
        
        for port in self.all_ports:
            self.route_dff(port, add_routes)

    def route_dff(self, port, add_routes):

        route_map = []
        
        # column mux dff is routed on it's own since it is to the far end
        # decoder inputs are min pitch M2, so need to use lower layer stack
        if self.col_addr_size > 0:
            dff_names = ["dout_{}".format(x) for x in range(self.col_addr_size)]
            dff_pins = [self.col_addr_dff_insts[port].get_pin(x) for x in dff_names]
            bank_names = ["addr{0}_{1}".format(port, x) for x in range(self.col_addr_size)]
            bank_pins = [self.bank_inst.get_pin(x) for x in bank_names]
            route_map.extend(list(zip(bank_pins, dff_pins)))

            if port == 0:
                offset = vector(self.control_logic_insts[port].rx() + self.dff.width,
                                - self.data_bus_size[port] + 2 * self.m1_pitch)
            else:
                offset = vector(0,
                                self.bank.height + 2 * self.m1_space)
            
            cr = channel_route.channel_route(netlist=route_map,
                                             offset=offset,
                                             layer_stack=self.m1_stack,
                                             parent=self)
            if add_routes:
                self.add_inst("hc", cr)
                self.connect_inst([])
            else:
                self.col_addr_bus_size[port] = cr.height

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
            
        if port in self.readwrite_ports and OPTS.perimeter_pins:
            # outputs from sense amp
            # These are the output pins which had their pin placed on the perimeter, so route from the
            # sense amp which should not align with write driver input
            sram_names = ["dout{0}[{1}]".format(port, x) for x in range(self.word_size + self.num_spare_cols)]
            sram_pins = [self.get_pin(x) for x in sram_names]
            bank_names = ["dout{0}_{1}".format(port, x) for x in range(self.word_size + self.num_spare_cols)]
            bank_pins = [self.bank_inst.get_pin(x) for x in bank_names]
            route_map.extend(list(zip(bank_pins, sram_pins)))

        # spare wen dff
        if self.num_spare_cols > 0 and port in self.write_ports:
            dff_names = ["dout_{}".format(x) for x in range(self.num_spare_cols)]
            dff_pins = [self.spare_wen_dff_insts[port].get_pin(x) for x in dff_names]
            bank_names = ["bank_spare_wen{0}_{1}".format(port, x) for x in range(self.num_spare_cols)]
            bank_pins = [self.bank_inst.get_pin(x) for x in bank_names]
            route_map.extend(list(zip(bank_pins, dff_pins)))
                
        if len(route_map) > 0:
            
            if self.num_wmasks > 0 and port in self.write_ports:
                layer_stack = self.m3_stack
            else:
                layer_stack = self.m1_stack
                
            if port == 0:
                offset = vector(self.control_logic_insts[port].rx() + self.dff.width,
                                - self.data_bus_size[port] + 2 * self.m1_pitch)
                cr = channel_route.channel_route(netlist=route_map,
                                                 offset=offset,
                                                 layer_stack=layer_stack,
                                                 parent=self)
                if add_routes:
                    self.add_inst("hc", cr)
                    self.connect_inst([])
                else:
                    self.data_bus_size[port] = max(cr.height, self.col_addr_bus_size[port])
            else:
                offset = vector(0,
                                self.bank.height + 2 * self.m1_space)
                cr = channel_route.channel_route(netlist=route_map,
                                                 offset=offset,
                                                 layer_stack=layer_stack,
                                                 parent=self)
                if add_routes:
                    self.add_inst("hc", cr)
                    self.connect_inst([])
                else:
                    self.data_bus_size[port] = max(cr.height, self.col_addr_bus_size[port])
                    
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
                              width=max(m2_via.width, m2_via.height))
                self.add_wire(self.m2_stack[::-1],
                              [data_dff_clk_pos, mid_pos, clk_steiner_pos])

    def route_control_logic(self):
        """ Route the control logic pins that are not inputs """

        for port in self.all_ports:
            for signal in self.control_logic_outputs[port]:
                # The clock gets routed separately and is not a part of the bank
                if "clk" in signal:
                    continue
                src_pin = self.control_logic_insts[port].get_pin(signal)
                dest_pin = self.bank_inst.get_pin(signal + "{}".format(port))
                self.connect_vbus(src_pin, dest_pin)

        for port in self.all_ports:
            # Only input (besides pins) is the replica bitline
            src_pin = self.control_logic_insts[port].get_pin("rbl_bl")
            dest_pin = self.bank_inst.get_pin("rbl_bl{}".format(port))
            self.add_wire(self.m2_stack[::-1],
                          [src_pin.center(), vector(src_pin.cx(), dest_pin.cy()), dest_pin.rc()])
            self.add_via_stack_center(from_layer=src_pin.layer,
                                      to_layer="m2",
                                      offset=src_pin.center())
            self.add_via_stack_center(from_layer=dest_pin.layer,
                                      to_layer="m2",
                                      offset=dest_pin.center())
            
    def route_row_addr_dff(self):
        """ Connect the output of the row flops to the bank pins """
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
        
        for n in self.control_logic_outputs[0]:
            pin = self.control_logic_insts[0].get_pin(n)
            self.add_label(text=n,
                           layer=pin.layer,
                           offset=pin.center())
                           
    def graph_exclude_data_dff(self):
        """Removes data dff and wmask dff (if applicable) from search graph. """
        # Data dffs and wmask dffs are only for writing so are not useful for evaluating read delay.
        for inst in self.data_dff_insts:
            self.graph_inst_exclude.add(inst)
        if self.write_size:
            for inst in self.wmask_dff_insts:
                self.graph_inst_exclude.add(inst)
        if self.num_spare_cols:
            for inst in self.spare_wen_dff_insts:
                self.graph_inst_exclude.add(inst)
    
    def graph_exclude_addr_dff(self):
        """Removes data dff from search graph. """
        # Address is considered not part of the critical path, subjectively removed
        for inst in self.row_addr_dff_insts:
            self.graph_inst_exclude.add(inst)
            
        if self.col_addr_dff:
            for inst in self.col_addr_dff_insts:
                self.graph_inst_exclude.add(inst)

    def graph_exclude_ctrl_dffs(self):
        """Exclude dffs for CSB, WEB, etc from graph"""
        # Insts located in control logic, exclusion function called here
        for inst in self.control_logic_insts:
            inst.mod.graph_exclude_dffs()
            
    def get_sen_name(self, sram_name, port=0):
        """Returns the s_en spice name."""
        # Naming scheme is hardcoded using this function, should be built into the
        # graph in someway.
        sen_name = "s_en{}".format(port)
        control_conns = self.get_conns(self.control_logic_insts[port])
        # Sanity checks
        if sen_name not in control_conns:
            debug.error("Signal={} not contained in control logic connections={}".format(sen_name,
                                                                                         control_conns))
        if sen_name in self.pins:
            debug.error("Internal signal={} contained in port list. Name defined by the parent.".format(sen_name))
        return "X{}.{}".format(sram_name, sen_name)
        
    def get_cell_name(self, inst_name, row, col):
        """Gets the spice name of the target bitcell."""
        # Sanity check in case it was forgotten
        if inst_name.find('x') != 0:
            inst_name = 'x' + inst_name
        return self.bank_inst.mod.get_cell_name(inst_name + '.x' + self.bank_inst.name, row, col)
