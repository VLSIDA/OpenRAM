import design
import debug
from tech import drc
from vector import vector
from precharge import precharge


class precharge_array(design.design):
    """
    Dynamically generated precharge array of all bitlines.  Cols is number
    of bit line columns, height is the height of the bit-cell array.
    """

    def __init__(self, name, columns, ptx_width, beta=2):
        design.design.__init__(self, name)
        debug.info(1, "Creating {0}".format(name))

        self.columns = columns
        self.ptx_width = ptx_width
        self.beta = beta

        self.add_pins()
        self.create_layout()
        self.DRC_LVS()

    def add_pins(self):
        """Adds pins for spice file"""
        for i in range(self.columns):
            self.add_pin("bl[{0}]".format(i))
            self.add_pin("br[{0}]".format(i))
        self.add_pin("clk")
        self.add_pin("vdd")

    def create_layout(self):
        self.create_pc_cell()
        self.setup_layout_constants()
        self.add_pc()
        self.add_rails()
        self.offset_all_coordinates()

    def setup_layout_constants(self):
        self.vdd_positions = []
        self.BL_positions = []
        self.BR_positions = []

        self.width = self.columns * self.pc_cell.width
        self.height = self.pc_cell.height

    def add_rails(self):
        self.add_vdd_rail()
        self.add_pclk_rail()

    def add_vdd_rail(self):
        offset = self.pc_cell.vdd_position
        self.add_layout_pin(text="vdd",
                            layer="metal1",
                            offset=offset,
                            width=self.width,
                            height=drc["minwidth_metal1"])
        self.vdd_positions.append(offset)

    def add_pclk_rail(self):
        self.pclk_position = self.pc_cell.pclk_position
        self.add_layout_pin(text="clk",
                            layer="metal1",
                            offset=self.pclk_position,
                            width=self.width,
                            height=drc["minwidth_metal1"])

    def create_pc_cell(self):
        """Initializes a single precharge cell"""
        self.pc_cell = precharge(name="precharge_cell",
                                 ptx_width=self.ptx_width,
                                 beta=self.beta)
        self.add_mod(self.pc_cell)

    def add_pc(self):
        """Creates a precharge array by horizontally tiling the precharge cell"""
        self.pc_cell_positions = []
        for i in range(self.columns):
            name = "pre_column_{0}".format(i)
            offset = vector(self.pc_cell.width * i, 0)
            self.pc_cell_positions.append(offset)
            self.add_inst(name=name,
                          mod=self.pc_cell,
                          offset=offset)
            self.add_label(text="bl[{0}]".format(i),
                           layer="metal2",
                           offset=offset+ self.pc_cell.BL_position.scale(1,0))
            self.add_label(text="br[{0}]".format(i),
                           layer="metal2",
                           offset=offset+ self.pc_cell.BR_position.scale(1,0))
            self.connect_inst(["bl[{0}]".format(i), "br[{0}]".format(i),
                               "clk", "vdd"])

            self.BL_positions.append(offset + self.pc_cell.BL_position.scale(1,0))
            self.BR_positions.append(offset + self.pc_cell.BR_position.scale(1,0))
