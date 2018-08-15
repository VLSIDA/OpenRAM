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

    unique_id = 1
    
    def __init__(self, columns, size=1, BL="bl", BR="br"):
        name = "precharge_array_{}".format(precharge_array.unique_id)
        precharge_array.unique_id += 1
        design.design.__init__(self, name)
        debug.info(1, "Creating {0}".format(self.name))

        self.columns = columns
        self.BL = BL
        self.BR = BR

        self.pc_cell = precharge(name="precharge", size=size, BL=self.BL, BR=self.BR)
        self.add_mod(self.pc_cell)

        self.width = self.columns * self.pc_cell.width
        self.height = self.pc_cell.height

        self.add_pins()
        self.create_layout()
        self.DRC_LVS()

    def add_pins(self):
        """Adds pins for spice file"""
        for i in range(self.columns):
            self.add_pin(self.BL+"[{0}]".format(i))
            self.add_pin(self.BR+"[{0}]".format(i))
        self.add_pin("en")
        self.add_pin("vdd")

    def create_layout(self):
        self.add_insts()
        self.add_layout_pins()
        

    def add_layout_pins(self):

        self.add_layout_pin(text="en",
                            layer="metal1",
                            offset=self.pc_cell.get_pin("en").ll(),
                            width=self.width,
                            height=drc["minwidth_metal1"])

        for inst in self.local_insts:
            self.copy_layout_pin(inst, "vdd")
            
        

    def add_insts(self):
        """Creates a precharge array by horizontally tiling the precharge cell"""
        self.local_insts = []
        for i in range(self.columns):
            name = "pre_column_{0}".format(i)
            offset = vector(self.pc_cell.width * i, 0)
            inst = self.add_inst(name=name,
                                 mod=self.pc_cell,
                                 offset=offset)
            self.local_insts.append(inst)
            
            self.connect_inst([self.BL+"[{0}]".format(i), self.BR+"[{0}]".format(i), "en", "vdd"])
            bl_pin = inst.get_pin(self.BL)
            self.add_layout_pin(text=self.BL+"[{0}]".format(i),
                                layer="metal2",
                                offset=bl_pin.ll(),
                                width=drc["minwidth_metal2"],
                                height=bl_pin.height())
            br_pin = inst.get_pin(self.BR) 
            self.add_layout_pin(text=self.BR+"[{0}]".format(i),
                                layer="metal2",
                                offset=br_pin.ll(),
                                width=drc["minwidth_metal2"],
                                height=bl_pin.height())

