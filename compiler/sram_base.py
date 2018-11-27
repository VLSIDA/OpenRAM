import sys
import datetime
import getpass
import debug
from importlib import reload
from vector import vector
from globals import OPTS, print_time

from design import design
        
class sram_base(design):
    """
    Dynamically generated SRAM by connecting banks to control logic. The
    number of banks should be 1 , 2 or 4
    """
    def __init__(self, name, sram_config):
        design.__init__(self, name)
        
        self.sram_config = sram_config
        sram_config.set_local_config(self)

        self.bank_insts = []


    def add_pins(self):
        """ Add pins for entire SRAM. """
        for port in self.write_ports:
            for bit in range(self.word_size):
                self.add_pin("DIN{0}[{1}]".format(port,bit),"INPUT")
                
        for port in self.all_ports:
            for bit in range(self.addr_size):
                self.add_pin("ADDR{0}[{1}]".format(port,bit),"INPUT")

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
            self.add_pin("csb{}".format(port),"INPUT")
        for port in self.readwrite_ports:
            self.add_pin("web{}".format(port),"INPUT")
        for port in self.all_ports:
            self.add_pin("clk{}".format(port),"INPUT")

        for port in self.read_ports:
            for bit in range(self.word_size):
                self.add_pin("DOUT{0}[{1}]".format(port,bit),"OUTPUT")
        
        self.add_pin("vdd","POWER")
        self.add_pin("gnd","GROUND")


    def create_netlist(self):
        """ Netlist creation """

        # Must create the control logic before pins to get the pins
        self.add_modules()
        self.add_pins()
        
        # This is for the lib file if we don't create layout
        self.width=0
        self.height=0

        
    def create_layout(self):
        """ Layout creation """    
        self.place_instances()

        self.route_layout()

        self.add_lvs_correspondence_points()
        
        self.offset_all_coordinates()

        # Must be done after offsetting lower-left
        self.route_supplies()

        highest_coord = self.find_highest_coords()
        self.width = highest_coord[0]
        self.height = highest_coord[1]

        
        self.DRC_LVS(final_verification=True)

        
    def route_supplies(self):
        """ Route the supply grid and connect the pins to them. """

        for inst in self.insts:
            self.copy_power_pins(inst,"vdd")
            self.copy_power_pins(inst,"gnd")

        from supply_router import supply_router as router
        layer_stack =("metal3","via3","metal4")
        rtr=router(layer_stack, self)
        rtr.route()
        

        
        
    def compute_bus_sizes(self):
        """ Compute the independent bus widths shared between two and four bank SRAMs """
        
        # address size + control signals + one-hot bank select signals
        self.num_vertical_line = self.addr_size + self.control_size + log(self.num_banks,2) + 1
        # data bus size
        self.num_horizontal_line = self.word_size

        self.vertical_bus_width = self.m2_pitch*self.num_vertical_line
        # vertical bus height depends on 2 or 4 banks
        
        self.data_bus_height = self.m3_pitch*self.num_horizontal_line
        self.data_bus_width = 2*(self.bank.width + self.bank_to_bus_distance) + self.vertical_bus_width
        
        self.control_bus_height = self.m1_pitch*(self.control_size+2) 
        self.control_bus_width = self.bank.width + self.bank_to_bus_distance + self.vertical_bus_width
        
        self.supply_bus_height = self.m1_pitch*2 # 2 for vdd/gnd placed with control bus
        self.supply_bus_width = self.data_bus_width

        # Sanity check to ensure we can fit the control logic above a single bank (0.9 is a hack really)
        debug.check(self.bank.width + self.vertical_bus_width > 0.9*self.control_logic.width,
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
            pen = "p_en{}".format(port)
            if self.port_id[port] == "r":
                self.control_bus_names[port].extend([sen, pen])
            elif self.port_id[port] == "w":
                self.control_bus_names[port].extend([wen])
            else:
                self.control_bus_names[port].extend([sen, wen, pen])
            self.vert_control_bus_positions = self.create_vertical_bus(layer="metal2",
                                                                       pitch=self.m2_pitch,
                                                                       offset=self.vertical_bus_offset,
                                                                       names=self.control_bus_names[port],
                                                                       length=self.vertical_bus_height)

            self.addr_bus_names=["A{0}[{1}]".format(port,i) for i in range(self.addr_size)]
            self.vert_control_bus_positions.update(self.create_vertical_pin_bus(layer="metal2",
                                                                                pitch=self.m2_pitch,
                                                                                offset=self.addr_bus_offset,
                                                                                names=self.addr_bus_names,
                                                                                length=self.addr_bus_height))

            
            self.bank_sel_bus_names = ["bank_sel{0}_{1}".format(port,i) for i in range(self.num_banks)]
            self.vert_control_bus_positions.update(self.create_vertical_pin_bus(layer="metal2",
                                                                                pitch=self.m2_pitch,
                                                                                offset=self.bank_sel_bus_offset,
                                                                                names=self.bank_sel_bus_names,
                                                                                length=self.vertical_bus_height))
            

            # Horizontal data bus
            self.data_bus_names = ["DATA{0}[{1}]".format(port,i) for i in range(self.word_size)]
            self.data_bus_positions = self.create_horizontal_pin_bus(layer="metal3",
                                                                     pitch=self.m3_pitch,
                                                                     offset=self.data_bus_offset,
                                                                     names=self.data_bus_names,
                                                                     length=self.data_bus_width)

            # Horizontal control logic bus
            # vdd/gnd in bus go along whole SRAM
            # FIXME: Fatten these wires?
            self.horz_control_bus_positions = self.create_horizontal_bus(layer="metal1",
                                                                         pitch=self.m1_pitch,
                                                                         offset=self.supply_bus_offset,
                                                                         names=["vdd"],
                                                                         length=self.supply_bus_width)
            # The gnd rail must not be the entire width since we protrude the right-most vdd rail up for
            # the decoder in 4-bank SRAMs
            self.horz_control_bus_positions.update(self.create_horizontal_bus(layer="metal1",
                                                                              pitch=self.m1_pitch,
                                                                              offset=self.supply_bus_offset+vector(0,self.m1_pitch),
                                                                              names=["gnd"],
                                                                              length=self.supply_bus_width))
            self.horz_control_bus_positions.update(self.create_horizontal_bus(layer="metal1",
                                                                              pitch=self.m1_pitch,
                                                                              offset=self.control_bus_offset,
                                                                              names=self.control_bus_names[port],
                                                                              length=self.control_bus_width))
        

        
    def add_multi_bank_modules(self):
        """ Create the multibank address flops and bank decoder """
        from dff_buf_array import dff_buf_array
        self.msb_address = dff_buf_array(name="msb_address",
                                         rows=1,
                                         columns=self.num_banks/2)
        self.add_mod(self.msb_address)

        if self.num_banks>2:
            self.msb_decoder = self.bank.decoder.pre2_4
            self.add_mod(self.msb_decoder)

            
    def add_modules(self):
        """ Create all the modules that will be used """
        c = reload(__import__(OPTS.bitcell))
        self.mod_bitcell = getattr(c, OPTS.bitcell)
        self.bitcell = self.mod_bitcell()
        
        c = reload(__import__(OPTS.control_logic))
        self.mod_control_logic = getattr(c, OPTS.control_logic)
        
        # Create the control logic module for each port type
        if len(self.readwrite_ports)>0:
            self.control_logic_rw = self.mod_control_logic(num_rows=self.num_rows,
                                                           words_per_row=self.words_per_row,
                                                           port_type="rw")
            self.add_mod(self.control_logic_rw)
        if len(self.writeonly_ports)>0:
            self.control_logic_w = self.mod_control_logic(num_rows=self.num_rows,
                                                          words_per_row=self.words_per_row,
                                                          port_type="w")
            self.add_mod(self.control_logic_w)
        if len(self.readonly_ports)>0:
            self.control_logic_r = self.mod_control_logic(num_rows=self.num_rows,
                                                          words_per_row=self.words_per_row,
                                                          port_type="r")
            self.add_mod(self.control_logic_r)

        # Create the address and control flops (but not the clk)
        from dff_array import dff_array
        self.row_addr_dff = dff_array(name="row_addr_dff", rows=self.row_addr_size, columns=1)
        self.add_mod(self.row_addr_dff)

        if self.col_addr_size > 0:
            self.col_addr_dff = dff_array(name="col_addr_dff", rows=1, columns=self.col_addr_size)
            self.add_mod(self.col_addr_dff)
        else:
            self.col_addr_dff = None

        self.data_dff = dff_array(name="data_dff", rows=1, columns=self.word_size)
        self.add_mod(self.data_dff)
        
        # Create the bank module (up to four are instantiated)
        from bank import bank
        self.bank = bank(self.sram_config,
                         name="bank")
        self.add_mod(self.bank)

        # Create bank decoder
        if(self.num_banks > 1):
            self.add_multi_bank_modules()

        self.bank_count = 0

        self.supply_rail_width = self.bank.supply_rail_width
        self.supply_rail_pitch = self.bank.supply_rail_pitch


    def create_bank(self,bank_num):
        """ Create a bank  """      
        self.bank_insts.append(self.add_inst(name="bank{0}".format(bank_num),
                                             mod=self.bank))

        temp = []
        for port in self.read_ports:
            for bit in range(self.word_size):
                temp.append("DOUT{0}[{1}]".format(port,bit))
        for port in self.write_ports:
            for bit in range(self.word_size):
                temp.append("BANK_DIN{0}[{1}]".format(port,bit))
        for port in self.all_ports:
            for bit in range(self.bank_addr_size):
                temp.append("A{0}[{1}]".format(port,bit))
        if(self.num_banks > 1):
            for port in self.all_ports:
                temp.append("bank_sel{0}[{1}]".format(port,bank_num))
        for port in self.read_ports:
            temp.append("s_en{0}".format(port))
        for port in self.read_ports:
            temp.append("p_en{0}".format(port))
        for port in self.write_ports:
            temp.append("w_en{0}".format(port))
        for port in self.all_ports:
            temp.append("wl_en{0}".format(port))
        temp.extend(["vdd", "gnd"])
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
                inputs.append("ADDR{}[{}]".format(port,bit+self.col_addr_size))
                outputs.append("A{}[{}]".format(port,bit+self.col_addr_size))

            self.connect_inst(inputs + outputs + ["clk_buf{}".format(port), "vdd", "gnd"])
        
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
                inputs.append("ADDR{}[{}]".format(port,bit))
                outputs.append("A{}[{}]".format(port,bit))

            self.connect_inst(inputs + outputs + ["clk_buf{}".format(port), "vdd", "gnd"])
        
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
            for bit in range(self.word_size):
                inputs.append("DIN{}[{}]".format(port,bit))
                outputs.append("BANK_DIN{}[{}]".format(port,bit))

            self.connect_inst(inputs + outputs + ["clk_buf{}".format(port), "vdd", "gnd"])
        
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
            
            temp = ["csb{}".format(port)]
            if port in self.readwrite_ports:
                temp.append("web{}".format(port))
            temp.append("clk{}".format(port))
            if port in self.read_ports:
                temp.append("s_en{}".format(port))
            if port in self.write_ports:
                temp.append("w_en{}".format(port))
            if port in self.read_ports:
                temp.append("p_en{}".format(port))
            temp.extend(["wl_en{}".format(port), "clk_buf{}".format(port), "vdd", "gnd"])
            self.connect_inst(temp)
        
        return insts


    def connect_rail_from_left_m2m3(self, src_pin, dest_pin):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pos = src_pin.rc()
        out_pos = dest_pin.center()
        self.add_wire(("metal3","via2","metal2"),[in_pos, vector(out_pos.x,in_pos.y),out_pos])
        self.add_via_center(layers=("metal2","via2","metal3"),
                            offset=src_pin.rc(),
                            rotate=90)

                            
    def connect_rail_from_left_m2m1(self, src_pin, dest_pin):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pos = src_pin.rc()
        out_pos = vector(dest_pin.cx(), in_pos.y)
        self.add_wire(("metal2","via1","metal1"),[in_pos, out_pos, out_pos - vector(0,self.m2_pitch)])


    def sp_write(self, sp_name):
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
        sp.write("**************************************************\n")        
        # This causes unit test mismatch
        # sp.write("* Created: {0}\n".format(datetime.datetime.now()))
        # sp.write("* User: {0}\n".format(getpass.getuser()))
        # sp.write(".global {0} {1}\n".format(spice["vdd_name"], 
        #                                     spice["gnd_name"]))
        usedMODS = list()
        self.sp_write_file(sp, usedMODS)
        del usedMODS
        sp.close()

        
    def analytical_delay(self, vdd, slew,load):
        """ LH and HL are the same in analytical model. """
        return self.bank.analytical_delay(vdd,slew,load)

        
