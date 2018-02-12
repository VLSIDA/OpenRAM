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

    def __init__(self, columns, size=1):
        design.design.__init__(self, "precharge_array")
        debug.info(1, "Creating {0}".format(self.name))

        self.columns = columns

        self.pc_cell = precharge(name="precharge", size=size)
        self.add_mod(self.pc_cell)

        self.width = self.columns * self.pc_cell.width
        self.height = self.pc_cell.height

        self.add_pins()
        self.create_layout()
        self.DRC_LVS()

    def add_pins(self):
        """Adds pins for spice file"""
        for i in range(self.columns):
            self.add_pin("bl[{0}]".format(i))
            self.add_pin("br[{0}]".format(i))
        self.add_pin("en")
        self.add_pin("vdd")

    def create_layout(self):
        self.add_insts()

        self.add_layout_pin(text="vdd",
                            layer="metal1",
                            offset=self.pc_cell.get_pin("vdd").ll(),
                            width=self.width,
                            height=drc["minwidth_metal1"])
        
        self.add_layout_pin(text="en",
                            layer="metal1",
                            offset=self.pc_cell.get_pin("en").ll(),
                            width=self.width,
                            height=drc["minwidth_metal1"])
        

    def add_insts(self):
        """Creates a precharge array by horizontally tiling the precharge cell"""
        for i in range(self.columns):
            name = "pre_column_{0}".format(i)
            offset = vector(self.pc_cell.width * i, 0)
            inst=self.add_inst(name=name,
                          mod=self.pc_cell,
                          offset=offset)
            bl_pin = inst.get_pin("bl")
            self.add_layout_pin(text="bl[{0}]".format(i),
                                layer="metal2",
                                offset=bl_pin.ll(),
                                width=drc["minwidth_metal2"],
                                height=bl_pin.height())
            br_pin = inst.get_pin("br") 
            self.add_layout_pin(text="br[{0}]".format(i),
                                layer="metal2",
                                offset=br_pin.ll(),
                                width=drc["minwidth_metal2"],
                                height=bl_pin.height())
            self.connect_inst(["bl[{0}]".format(i), "br[{0}]".format(i),
                               "en", "vdd"])

