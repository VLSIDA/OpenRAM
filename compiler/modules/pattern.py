from openram import debug
from openram.base.geometry import instance,geometry
from typing import List
from typing import Optional
from openram.base import design
from openram.globals import OPTS
class pattern():
    """
    This class is used to desribe the internals of a bitcell array. It describes 
    instance modules, rotation, and ordering

    """
    block = List[List[instance]]
    def __init__(self,
                 parent_design: design,
                 name:str,
                 core_block:block,
                 num_core_x:int,
                 num_core_y:int,
                 cores_per_x_block: int = 1,
                 cores_per_y_block: int = 1,
                 x_block: Optional[block] = None, 
                 y_block: Optional[block] = None, 
                 xy_block: Optional[block] = None,
                 initial_x_block:bool = False,
                 initial_y_block:bool = False,
                 final_x_block:bool = False,
                 final_y_block:bool = False
                 ): 
        """
        a "block" is a 2d list of instances
        core_block defines the main block that is tiled
        num_core defines the number of times the core block is to be tiled 
        (i.e. bitcells in dimension / bitcells in core_block)
        x_block defines a block that is inserted to the right of the core_block
        y_block defines a block that is inserted below the core block
        xy_block defines a block that is a inserted where the x_block and y_block intercept
        the initial and final booleans determine whether the pattern begins and/or ends with x/y blocks
        """
        self.parent_design = parent_design
        self.name = name
        self.core_block = core_block
        self.num_core_x = num_core_x
        self.num_core_y = num_core_y
        self.cores_per_x_block = cores_per_x_block
        self.cores_per_y_block = cores_per_y_block
        self.x_block = x_block
        self.y_block = y_block
        self.xy_block = xy_block
        self.initial_x_block = initial_x_block
        self.initial_y_block = initial_y_block
        self.final_x_block = final_x_block
        self.final_y_block = final_y_block
        if not OPTS.netlist_only:
            self.verify_interblock_dimensions() 
  
    def compute_and_verify_intrablock_dimensions(self, block: block) -> List[int]:
        for row in block:
            row_height = row[0].height
            for inst in row:
                debug.check(row_height == inst.height, "intrablock instances within the same row are different heights")
        
        for y in range(len(block[0])):
            debug.check(all([row[y].width for row in block]), "intrablock instances within the same column are different widths")
                
        block_width = sum([instance.width for instance in block[0]])
        block_height = sum([row[0].height for row in block]) 

        return [block_width, block_height]
        
    def verify_interblock_dimensions(self) -> None:
        """
        Ensure the individual blocks are valid and interblock dimensions are valid
        """
        debug.check(len(self.core_block) >= 1, "invalid core_block dimension: core_block rows must be >=1")
        debug.check(len(self.core_block[0]) >= 1, "invalid core_block dimension: core_block cols must be >=1")
        if self.x_block and self.y_block:
            debug.check(self.xy_block is not None, "must have xy_block if both x_block and y_block are provided")


        (self.core_block_width, self.core_block_height) = self.compute_and_verify_intrablock_dimensions(self.core_block)
        if self.x_block:
            (self.x_block_width, self.x_block_height) = self.compute_and_verify_intrablock_dimensions(self.x_block)
        if self.y_block:
            (self.y_block_width, self.y_block_height) = self.compute_and_verify_intrablock_dimensions(self.y_block)
        if self.xy_block:
            (self.xy_block_width, self.xy_block_height) = self.compute_and_verify_intrablock_dimensions(self.xy_block)
        if(self.x_block): 
            debug.check(self.core_block_width * self.cores_per_x_block == self.x_block_width, "core_block does not align with x_block")
        if(self.y_block):
            debug.check(self.core_block_height * self.cores_per_y_block == self.y_block_height, "core_block does not aligns with y_block")
        if(self.xy_block):
            debug.check(self.xy_block_height == self.x_block_height, "xy_block does not align with x_block")
            debug.check(self.xy_block_width == self.y_block_width, "xy_block does not align with y_block")

    def connect_block(self, block: block, x: int, y: int) -> None:
        for dy in range(len(block)):
            for dx in range(len(block[0])):
                inst = block[dy][dx]
                self.parent_design.cell_inst[x + dx, y + dy] = self.parent_design.add_existing_inst(inst)
                self.parent_design.connect_inst(self.parent_design.get_bitcell_pins(x+dx, y+dy))

    def place_block(self, block: block, x: int, y: int, place_x: float, place_y: float) -> None:
        x_offset = 0
        y_offset = 0
        for dy in range(len(block)):
            for dx in range(len(block[0])):
                inst = self.parent_design.cell_inst[x + dx, y +dy]
                inst.place((place_x + x_offset, place_y + y_offset), inst.mirror, inst.rotate)
                x_offset += inst.width
            x_offset = 0
            y_offset += inst.height

    def connect_array(self) -> None:
        x = 0
        y = 0
        for i in range(self.num_core_y):
            for j in range (self.num_core_x):
                print("connecting {} {}".format(x,y))
                self.connect_block(self.core_block, x,y)
                x += len(self.core_block[0])
            x = 0
            y += len(self.core_block)
    
    def place_array(self) -> None:

        x = 0
        y = 0
        place_x = 0
        place_y = 0
        for i in range(self.num_core_y):
            x = 0
            place_x = 0
            for j in range (self.num_core_x):
                print("placing {} {}".format(x,y))
                self.place_block(self.core_block, x, y, place_x, place_y)
                place_x += self.core_block_width
                x += len(self.core_block[0])
            y += len(self.core_block)
            place_y += self.core_block_height
        self.parent_design.width = x
        self.parent_design.height = y
        
        


        

    def connect_pins(self, array: design) -> None:
        array.connect_isnt()

