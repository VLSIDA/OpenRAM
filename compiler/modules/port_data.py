# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California 
# All rights reserved.
#
import sys
from tech import drc, parameter
import debug
import design
from sram_factory import factory
from vector import vector

from globals import OPTS

class port_data(design.design):
    """
    Create the data port (column mux, sense amps, write driver, etc.) for the given port number.
    """

    def __init__(self, sram_config, port, name=""):
        
        sram_config.set_local_config(self)
        self.port = port
        
        if name == "":
            name = "port_data_{0}".format(self.port)
        design.design.__init__(self, name)
        debug.info(2, "create data port of size {0} with {1} words per row".format(self.word_size,self.words_per_row))

        self.create_netlist()
        if not OPTS.netlist_only:
            debug.check(len(self.all_ports)<=2,"Bank layout cannot handle more than two ports.")
            self.create_layout()
            self.add_boundary()


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
        else:
            self.write_driver_array_inst = None
            
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
        """ Adding pins for port address module"""
        for bit in range(self.num_cols):
            self.add_pin(self.bl_names[self.port]+"_{0}".format(bit),"INOUT")
            self.add_pin(self.br_names[self.port]+"_{0}".format(bit),"INOUT")
        if self.port in self.read_ports:
            for bit in range(self.word_size):
                self.add_pin("dout_{}".format(bit),"OUTPUT")
        if self.port in self.write_ports:
            for bit in range(self.word_size):
                self.add_pin("din_{}".format(bit),"INPUT")
        # Will be empty if no col addr lines
        sel_names = ["sel_{}".format(x) for x in range(self.num_col_addr_lines)]
        for pin_name in sel_names:
            self.add_pin(pin_name,"INPUT")
        if self.port in self.read_ports:
            self.add_pin("s_en", "INPUT")
        if self.port in self.read_ports:
            self.add_pin("p_en_bar", "INPUT")
        if self.port in self.write_ports:
            self.add_pin("w_en", "INPUT")
        self.add_pin("vdd","POWER")
        self.add_pin("gnd","GROUND")

        
    def route_layout(self):
        """ Create routing amoung the modules """
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
            # write_driver -> sense_amp -> (column_mux) -> precharge -> bitcell_array
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
            # write_driver -> (column_mux) -> bitcell_array
            self.route_write_driver_in(self.port)    
            self.route_write_driver_to_column_mux_or_bitcell_array(self.port)            
        
    def route_supplies(self):
        """ Propagate all vdd/gnd pins up to this level for all modules """
        for inst in self.insts:
            self.copy_power_pins(inst,"vdd")
            self.copy_power_pins(inst,"gnd")
        
    def add_modules(self):

        if self.port in self.read_ports:
            self.precharge_array = factory.create(module_type="precharge_array",
                                                  columns=self.num_cols,
                                                  bitcell_bl=self.bl_names[self.port],
                                                  bitcell_br=self.br_names[self.port])
            self.add_mod(self.precharge_array)

            self.sense_amp_array = factory.create(module_type="sense_amp_array",
                                                  word_size=self.word_size, 
                                                  words_per_row=self.words_per_row)
            self.add_mod(self.sense_amp_array)
        else:
            self.precharge_array = None
            self.sense_amp_array = None

        if self.col_addr_size > 0:
            self.column_mux_array = factory.create(module_type="column_mux_array",
                                                   columns=self.num_cols, 
                                                   word_size=self.word_size,
                                                   bitcell_bl=self.bl_names[self.port],
                                                   bitcell_br=self.br_names[self.port])
            self.add_mod(self.column_mux_array)
        else:
            self.column_mux_array = None
                

        if self.port in self.write_ports:
            self.write_driver_array = factory.create(module_type="write_driver_array",
                                                     columns=self.num_cols,
                                                     word_size=self.word_size)
            self.add_mod(self.write_driver_array)
        else:
            self.write_driver_array = None


    def precompute_constants(self):
        """  Get some preliminary data ready """

        # The central bus is the column address (one hot) and row address (binary)
        if self.col_addr_size>0:
            self.num_col_addr_lines = 2**self.col_addr_size
        else:
            self.num_col_addr_lines = 0            
        

        # A space for wells or jogging m2 between modules
        self.m2_gap = max(2*drc("pwell_to_nwell") + drc("well_enclosure_active"),
                          3*self.m2_pitch)


        # create arrays of bitline and bitline_bar names for read, write, or all ports
        self.bitcell = factory.create(module_type="bitcell") 
        self.bl_names = self.bitcell.list_all_bl_names()
        self.br_names = self.bitcell.list_all_br_names()
        self.wl_names = self.bitcell.list_all_wl_names()

    def create_precharge_array(self):
        """ Creating Precharge """
        if not self.precharge_array:
            self.precharge_array_inst = None
            return
        
        self.precharge_array_inst = self.add_inst(name="precharge_array{}".format(self.port),
                                                  mod=self.precharge_array)
        temp = []
        for bit in range(self.num_cols):
            temp.append(self.bl_names[self.port]+"_{0}".format(bit))
            temp.append(self.br_names[self.port]+"_{0}".format(bit))
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
            temp.append(self.bl_names[self.port]+"_{0}".format(col))
            temp.append(self.br_names[self.port]+"_{0}".format(col))
        for word in range(self.words_per_row):
            temp.append("sel_{}".format(word))
        for bit in range(self.word_size):
            temp.append(self.bl_names[self.port]+"_out_{0}".format(bit))
            temp.append(self.br_names[self.port]+"_out_{0}".format(bit))
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
                temp.append(self.bl_names[self.port]+"_{0}".format(bit))
                temp.append(self.br_names[self.port]+"_{0}".format(bit))
            else:
                temp.append(self.bl_names[self.port]+"_out_{0}".format(bit))
                temp.append(self.br_names[self.port]+"_out_{0}".format(bit))
                    
        temp.extend(["s_en", "vdd", "gnd"])
        self.connect_inst(temp)

            
    def place_sense_amp_array(self, offset):
        """ Placing Sense amp  """
        self.sense_amp_array_inst.place(offset=offset, mirror="MX")

            
    def create_write_driver_array(self):
        """ Creating Write Driver  """
        self.write_driver_array_inst = self.add_inst(name="write_driver_array{}".format(self.port), 
                                                     mod=self.write_driver_array)

        temp = []
        for bit in range(self.word_size):
            temp.append("din_{}".format(bit))
        for bit in range(self.word_size):            
            if (self.words_per_row == 1):            
                temp.append(self.bl_names[self.port]+"_{0}".format(bit))
                temp.append(self.br_names[self.port]+"_{0}".format(bit))
            else:
                temp.append(self.bl_names[self.port]+"_out_{0}".format(bit))
                temp.append(self.br_names[self.port]+"_out_{0}".format(bit))
        temp.extend(["w_en", "vdd", "gnd"])
        self.connect_inst(temp)

            
    def place_write_driver_array(self, offset):
        """ Placing Write Driver  """
        self.write_driver_array_inst.place(offset=offset, mirror="MX")
            

    def compute_instance_offsets(self):
        """
        Compute the empty instance offsets for port0 and port1 (if needed)
        """

        vertical_port_order = []
        vertical_port_order.append(self.precharge_array_inst)
        vertical_port_order.append(self.column_mux_array_inst)
        vertical_port_order.append(self.sense_amp_array_inst)
        vertical_port_order.append(self.write_driver_array_inst)

        vertical_port_offsets = 4*[None]
        self.width = 0
        self.height = 0
        for i,p in enumerate(vertical_port_order):
            if p==None:
                continue
            self.height += (p.height + self.m2_gap)
            self.width = max(self.width, p.width)
            vertical_port_offsets[i]=vector(0,self.height)

        # Reversed order
        self.write_driver_offset = vertical_port_offsets[3]
        self.sense_amp_offset = vertical_port_offsets[2]
        self.column_mux_offset = vertical_port_offsets[1]
        self.precharge_offset = vertical_port_offsets[0]


            
    def place_instances(self):
        """ Place the instances. """

        # These are fixed in the order: write driver, sense amp, clumn mux, precharge,
        # even if the item is not used in a given port (it will be None then)
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
        
        for bit in range(self.word_size):
            data_pin = self.sense_amp_array_inst.get_pin("data_{}".format(bit))
            self.add_layout_pin_rect_center(text="dout_{0}".format(bit),
                                            layer=data_pin.layer, 
                                            offset=data_pin.center(),
                                            height=data_pin.height(),
                                            width=data_pin.width())
            
    def route_write_driver_in(self, port):
        """ Connecting write driver   """

        for row in range(self.word_size):
            data_name = "data_{}".format(row)
            din_name = "din_{}".format(row)
            self.copy_layout_pin(self.write_driver_array_inst, data_name, din_name)
            
    def route_column_mux_to_precharge_array(self, port):
        """ Routing of BL and BR between col mux and precharge array """

        # Only do this if we have a column mux!
        if self.col_addr_size==0:
            return
        
        inst1 = self.column_mux_array_inst
        inst2 = self.precharge_array_inst
        self.connect_bitlines(inst1, inst2, self.num_cols)


                                        
    def route_sense_amp_to_column_mux_or_precharge_array(self, port):
        """ Routing of BL and BR between sense_amp and column mux or precharge array """
        inst2 = self.sense_amp_array_inst
        
        if self.col_addr_size>0:
            # Sense amp is connected to the col mux
            inst1 = self.column_mux_array_inst
            inst1_bl_name = "bl_out_{}"
            inst1_br_name = "br_out_{}"
        else:
            # Sense amp is directly connected to the precharge array
            inst1 = self.precharge_array_inst
            inst1_bl_name = "bl_{}"
            inst1_br_name = "br_{}"
            
        self.channel_route_bitlines(inst1=inst1, inst2=inst2, num_bits=self.word_size,
                                    inst1_bl_name=inst1_bl_name, inst1_br_name=inst1_br_name)

    def route_write_driver_to_column_mux_or_bitcell_array(self, port):
        """ Routing of BL and BR between sense_amp and column mux or bitcell array """
        inst2 = self.write_driver_array_inst
        
        if self.col_addr_size>0:
            # Write driver is connected to the col mux
            inst1 = self.column_mux_array_inst
            inst1_bl_name = "bl_out_{}"
            inst1_br_name = "br_out_{}"
        else:
            # Write driver is directly connected to the bitcell array
            return
            
        self.channel_route_bitlines(inst1=inst1, inst2=inst2, num_bits=self.word_size,
                                    inst1_bl_name=inst1_bl_name, inst1_br_name=inst1_br_name)
        
    def route_write_driver_to_sense_amp(self, port):
        """ Routing of BL and BR between write driver and sense amp """
        
        inst1 = self.write_driver_array_inst
        inst2 = self.sense_amp_array_inst

        # These should be pitch matched in the cell library,
        # but just in case, do a channel route.
        self.channel_route_bitlines(inst1=inst1, inst2=inst2, num_bits=self.word_size)


    def route_bitline_pins(self):
        """ Add the bitline pins for the given port """

        for bit in range(self.num_cols):
            if self.port in self.read_ports:
                self.copy_layout_pin(self.precharge_array_inst, "bl_{}".format(bit))
                self.copy_layout_pin(self.precharge_array_inst, "br_{}".format(bit))
            elif self.column_mux_array_inst:
                self.copy_layout_pin(self.column_mux_array_inst, "bl_{}".format(bit))
                self.copy_layout_pin(self.column_mux_array_inst, "br_{}".format(bit))
            else:
                self.copy_layout_pin(self.write_driver_array_inst, "bl_{}".format(bit))  
                self.copy_layout_pin(self.write_driver_array_inst, "br_{}".format(bit))  

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
            self.copy_layout_pin(self.write_driver_array_inst, "en", "w_en")
            
        
    def channel_route_bitlines(self, inst1, inst2, num_bits,
                               inst1_bl_name="bl_{}", inst1_br_name="br_{}",
                               inst2_bl_name="bl_{}", inst2_br_name="br_{}"):
        """
        Route the bl and br of two modules using the channel router.
        """
        
        # determine top and bottom automatically.
        # since they don't overlap, we can just check the bottom y coordinate.
        if inst1.by() < inst2.by():
            (bottom_inst, bottom_bl_name, bottom_br_name) = (inst1, inst1_bl_name, inst1_br_name)
            (top_inst, top_bl_name, top_br_name) = (inst2, inst2_bl_name, inst2_br_name)
        else:
            (bottom_inst, bottom_bl_name, bottom_br_name) = (inst2, inst2_bl_name, inst2_br_name)
            (top_inst, top_bl_name, top_br_name) = (inst1, inst1_bl_name, inst1_br_name)


        # Channel route each mux separately since we don't minimize the number
        # of tracks in teh channel router yet. If we did, we could route all the bits at once!
        offset = bottom_inst.ul() + vector(0,self.m1_pitch)
        for bit in range(num_bits):
            bottom_names = [bottom_inst.get_pin(bottom_bl_name.format(bit)), bottom_inst.get_pin(bottom_br_name.format(bit))]
            top_names = [top_inst.get_pin(top_bl_name.format(bit)), top_inst.get_pin(top_br_name.format(bit))]            
            route_map = list(zip(bottom_names, top_names))
            self.create_horizontal_channel_route(route_map, offset)
            

    def connect_bitlines(self, inst1, inst2, num_bits,
                         inst1_bl_name="bl_{}", inst1_br_name="br_{}",
                         inst2_bl_name="bl_{}", inst2_br_name="br_{}"):
        """
        Connect the bl and br of two modules.
        This assumes that they have sufficient space to create a jog
        in the middle between the two modules (if needed).
        """
        
        # determine top and bottom automatically.
        # since they don't overlap, we can just check the bottom y coordinate.
        if inst1.by() < inst2.by():
            (bottom_inst, bottom_bl_name, bottom_br_name) = (inst1, inst1_bl_name, inst1_br_name)
            (top_inst, top_bl_name, top_br_name) = (inst2, inst2_bl_name, inst2_br_name)
        else:
            (bottom_inst, bottom_bl_name, bottom_br_name) = (inst2, inst2_bl_name, inst2_br_name)
            (top_inst, top_bl_name, top_br_name) = (inst1, inst1_bl_name, inst1_br_name)

        for col in range(num_bits):
            bottom_bl = bottom_inst.get_pin(bottom_bl_name.format(col)).uc()
            bottom_br = bottom_inst.get_pin(bottom_br_name.format(col)).uc()
            top_bl = top_inst.get_pin(top_bl_name.format(col)).bc()
            top_br = top_inst.get_pin(top_br_name.format(col)).bc()

            yoffset = 0.5*(top_bl.y+bottom_bl.y)
            self.add_path("metal2",[bottom_bl, vector(bottom_bl.x,yoffset),
                                    vector(top_bl.x,yoffset), top_bl])
            self.add_path("metal2",[bottom_br, vector(bottom_br.x,yoffset),
                                    vector(top_br.x,yoffset), top_br])
        
    def graph_exclude_precharge(self):
        """Precharge adds a loop between bitlines, can be excluded to reduce complexity"""
        if self.precharge_array_inst:
            self.graph_inst_exclude.add(self.precharge_array_inst)
