import debug
import design
from tech import drc, spice
from vector import vector
from globals import OPTS



class bitcell_array(design.design):
    """
    Creates a rows x cols array of memory cells. Assumes bit-lines
    and word line is connected by abutment.
    Connects the word lines and bit lines.
    """

    def __init__(self, cols, rows, name="bitcell_array"):
        design.design.__init__(self, name)
        debug.info(1, "Creating {0} {1} x {2}".format(self.name, rows, cols))


        self.column_size = cols
        self.row_size = rows

        c = reload(__import__(OPTS.bitcell))
        self.mod_bitcell = getattr(c, OPTS.bitcell)
        self.cell = self.mod_bitcell()
        self.add_mod(self.cell)

        # We increase it by a well enclosure so the precharges don't overlap our wells
        self.height = self.row_size*self.cell.height + drc["well_enclosure_active"] + self.m1_width
        self.width = self.column_size*self.cell.width + self.m1_width
        
        self.add_pins()
        self.create_layout()
        self.add_layout_pins()

        # We don't offset this because we need to align
        # the replica bitcell in the control logic
        #self.offset_all_coordinates()
        
        self.DRC_LVS()

    def add_pins(self):
        for col in range(self.column_size):
            self.add_pin("bl[{0}]".format(col))
            self.add_pin("br[{0}]".format(col))
        for row in range(self.row_size):
            self.add_pin("wl[{0}]".format(row))
        self.add_pin("vdd")
        self.add_pin("gnd")

    def create_layout(self):
        xoffset = 0.0
        self.cell_inst = {}
        for col in range(self.column_size):
            yoffset = 0.0
            for row in range(self.row_size):
                name = "bit_r{0}_c{1}".format(row, col)

                if row % 2:
                    tempy = yoffset + self.cell.height
                    dir_key = "MX"
                else:
                    tempy = yoffset
                    dir_key = ""

                self.cell_inst[row,col]=self.add_inst(name=name,
                                                      mod=self.cell,
                                                      offset=[xoffset, tempy],
                                                      mirror=dir_key)
                self.connect_inst(["bl[{0}]".format(col),
                                   "br[{0}]".format(col),
                                   "wl[{0}]".format(row),
                                   "vdd",
                                   "gnd"])
                yoffset += self.cell.height
            xoffset += self.cell.width


    def add_layout_pins(self):
        """ Add the layout pins """
        
        offset = vector(0.0, 0.0)
        for col in range(self.column_size):
            # get the pin of the lower row cell and make it the full width
            bl_pin = self.cell_inst[0,col].get_pin("BL")
            br_pin = self.cell_inst[0,col].get_pin("BR")
            self.add_layout_pin(text="bl[{0}]".format(col),
                                layer="metal2",
                                offset=bl_pin.ll(),
                                width=bl_pin.width(),
                                height=self.height)
            self.add_layout_pin(text="br[{0}]".format(col),
                                layer="metal2",
                                offset=br_pin.ll(),
                                width=br_pin.width(),
                                height=self.height)
                    
            # increments to the next column width
            offset.x += self.cell.width

        offset.x = 0.0
        for row in range(self.row_size):
            wl_pin = self.cell_inst[row,0].get_pin("WL")
            self.add_layout_pin(text="wl[{0}]".format(row),
                                layer="metal1",
                                offset=wl_pin.ll(),
                                width=self.width,
                                height=wl_pin.height())

            # increments to the next row height
            offset.y += self.cell.height

        # For every second row and column, add a via for vdd
        for row in range(self.row_size):
            for col in range(self.column_size):
                inst = self.cell_inst[row,col]
                for vdd_pin in inst.get_pins("vdd"):
                    # Drop to M1 if needed
                    if vdd_pin.layer == "metal1":
                        self.add_via_center(layers=("metal1", "via1", "metal2"),
                                            offset=vdd_pin.center(),
                                            rotate=90)
                    # Always drop to M2
                    self.add_via_center(layers=("metal2", "via2", "metal3"),
                                        offset=vdd_pin.center())
                    self.add_layout_pin_rect_center(text="vdd",
                                                    layer="metal3",
                                                    offset=vdd_pin.center())
                                            
                
        # For every second row and column (+1), add a via for gnd
        for row in range(self.row_size):
            for col in range(self.column_size):
                inst = self.cell_inst[row,col]
                for gnd_pin in inst.get_pins("gnd"):
                    # Drop to M1 if needed
                    if gnd_pin.layer == "metal1":
                        self.add_via_center(layers=("metal1", "via1", "metal2"),
                                            offset=gnd_pin.center(),
                                            rotate=90)
                    # Always drop to M2
                    self.add_via_center(layers=("metal2", "via2", "metal3"),
                                        offset=gnd_pin.center())
                    self.add_layout_pin_rect_center(text="gnd",
                                                    layer="metal3",
                                                    offset=gnd_pin.center())

    def analytical_delay(self, slew, load=0):
        from tech import drc
        wl_wire = self.gen_wl_wire()
        wl_wire.return_delay_over_wire(slew)

        wl_to_cell_delay = wl_wire.return_delay_over_wire(slew)
        # hypothetical delay from cell to bl end without sense amp
        bl_wire = self.gen_bl_wire()
        cell_load = 2 * bl_wire.return_input_cap() # we ingore the wire r
                                                   # hence just use the whole c
        bl_swing = 0.1
        cell_delay = self.cell.analytical_delay(wl_to_cell_delay.slew, cell_load, swing = bl_swing)

        #we do not consider the delay over the wire for now
        return self.return_delay(cell_delay.delay+wl_to_cell_delay.delay,
                                 wl_to_cell_delay.slew)
                        
    def analytical_power(self, proc, vdd, temp, load):
        """Power of Bitcell array and bitline in nW."""
        from tech import drc
        
        # Dynamic Power from Bitline
        bl_wire = self.gen_bl_wire()
        cell_load = 2 * bl_wire.return_input_cap() 
        bl_swing = 0.1 #This should probably be defined in the tech file or input
        freq = spice["default_event_rate"]
        bitline_dynamic = bl_swing*cell_load*vdd*vdd*freq #not sure if calculation is correct
        
        #Calculate the bitcell power which currently only includes leakage 
        cell_power = self.cell.analytical_power(proc, vdd, temp, load)
        
        #Leakage power grows with entire array and bitlines.
        total_power = self.return_power(cell_power.dynamic + bitline_dynamic * self.column_size,
                                        cell_power.leakage * self.column_size * self.row_size)
        return total_power

    def gen_wl_wire(self):
        wl_wire = self.generate_rc_net(int(self.column_size), self.width, drc["minwidth_metal1"])
        wl_wire.wire_c = 2*spice["min_tx_gate_c"] + wl_wire.wire_c # 2 access tx gate per cell
        return wl_wire

    def gen_bl_wire(self):
        bl_pos = 0
        bl_wire = self.generate_rc_net(int(self.row_size-bl_pos), self.height, drc["minwidth_metal1"])
        bl_wire.wire_c =spice["min_tx_drain_c"] + bl_wire.wire_c # 1 access tx d/s per cell
        return bl_wire

    def output_load(self, bl_pos=0):
        bl_wire = self.gen_bl_wire()
        return bl_wire.wire_c # sense amp only need to charge small portion of the bl
                              # set as one segment for now

    def input_load(self):
        wl_wire = self.gen_wl_wire()
        return wl_wire.return_input_cap()
