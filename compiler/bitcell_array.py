import debug
import design
from vector import vector
from globals import OPTS


class bitcell_array(design.design):
    """
    Creates a rows x cols array of memory cells. Assumes bit-lines
    and word line is connected by abutment.
    Connects the word lines and bit lines.
    """

    def __init__(self, name, cols, rows):
        design.design.__init__(self, name)
        debug.info(1, "Creating {0} {1} x {2}".format(self.name, rows, cols))


        self.column_size = cols
        self.row_size = rows

        c = reload(__import__(OPTS.config.bitcell))
        self.mod_bitcell = getattr(c, OPTS.config.bitcell)
        self.bitcell_chars = self.mod_bitcell.chars

        self.add_pins()
        self.create_layout()
        self.add_labels()
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
        self.create_cell()
        self.setup_layout_constants()
        self.add_cells()
        self.offset_all_coordinates()

    def setup_layout_constants(self):
        self.vdd_positions = []
        self.gnd_positions = []
        self.BL_positions = []
        self.BR_positions = []
        self.WL_positions = []
        self.height = self.row_size * self.cell.height
        self.width = self.column_size * self.cell.width

    def create_cell(self):
        self.cell = self.mod_bitcell()
        self.add_mod(self.cell)

    def add_cells(self):
        xoffset = 0.0
        for col in range(self.column_size):
            yoffset = 0.0
            for row in range(self.row_size):
                name = "bit_r{0}_c{1}".format(row, col)

                if row % 2:
                    tempy = yoffset + self.cell.height
                    dir_key = "MX"
                else:
                    tempy = yoffset
                    dir_key = "R0"

                if OPTS.trim_noncritical == True:
                    if row == self.row_size - 1:
                        self.add_inst(name=name,
                                      mod=self.cell,
                                      offset=[xoffset, tempy],
                                      mirror=dir_key)
                        self.connect_inst(["bl[{0}]".format(col),
                                           "br[{0}]".format(col),
                                           "wl[{0}]".format(row),
                                           "vdd",
                                           "gnd"])
                else:
                    self.add_inst(name=name,
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

    def add_labels(self):
        offset = vector(0.0, 0.0)
        for col in range(self.column_size):
            offset.y = 0.0
            self.add_label(text="bl[{0}]".format(col),
                           layer="metal2",
                           offset=offset + vector(self.bitcell_chars["BL"][0],0))
            self.add_label(text="br[{0}]".format(col),
                           layer="metal2",
                           offset=offset + vector(self.bitcell_chars["BR"][0],0))
            self.BL_positions.append(offset + vector(self.bitcell_chars["BL"][0],0))
            self.BR_positions.append(offset + vector(self.bitcell_chars["BR"][0],0))

            # gnd offset is 0 in our cell, but it be non-zero
            self.add_label(text="gnd", 
                           layer="metal2",
                           offset=offset + vector(self.bitcell_chars["gnd"][0],0))
            self.gnd_positions.append(offset + vector(self.bitcell_chars["gnd"][0],0))

            for row in range(self.row_size):
                # only add row labels on the left most column
                if col == 0:
                    # flipped row
                    if row % 2:
                        base_offset = offset + vector(0, self.cell.height)
                        vdd_offset = base_offset - vector(0,self.bitcell_chars["vdd"][1])
                        wl_offset =  base_offset - vector(0,self.bitcell_chars["WL"][1])
                    # unflipped row
                    else:
                        vdd_offset = offset + vector(0,self.bitcell_chars["vdd"][1])
                        wl_offset = offset + vector(0,self.bitcell_chars["WL"][1])
                    # add vdd label and offset
                    self.add_label(text="vdd",
                                   layer="metal1",
                                   offset=vdd_offset)
                    self.vdd_positions.append(vdd_offset)
                    # add gnd label and offset
                    self.add_label(text="wl[{0}]".format(row),
                                   layer="metal1",
                                   offset=wl_offset)
                    self.WL_positions.append(wl_offset)

                # increments to the next row height
                offset.y += self.cell.height
            # increments to the next column width
            offset.x += self.cell.width
