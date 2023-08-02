from openram import debug
from openram.base.geometry import instance,geometry
from typing import List
from typing import Optional
from openram.base import design
from openram.globals import OPTS
from math import ceil
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
                 num_rows:int,
                 num_cols:int,
                 num_cores_x: Optional[int] = 0,
                 num_cores_y: Optional[int] = 0,
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
        self.num_rows = num_rows 
        self.num_cols = num_cols
        self.num_cores_x = num_cores_x
        self.num_cores_y = num_cores_y
        if num_cores_x == 0:
            self.num_cores_x = ceil(num_cols/len(core_block[0]))
        if num_cores_y == 0:
            self.num_cores_y = ceil(num_rows/len(core_block))

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
        

    def connect_block(self, block: block, col: int, row: int):
        for dr in range(len(block)):
            for dc in range(len(block[0])):
                if(self.bit_rows.count(self.num_rows) != self.num_cols and self.bit_cols.count(self.bit_cols) != self.num_rows):
                    inst = block[dr][dc]
                    if(len(self.bit_rows) <= col + dc):
                        self.bit_rows.append(0)
                    if(len(self.bit_cols) <= row + dr):
                        self.bit_cols.append(0)
                    if(self.bit_rows[col+dc] < self.num_rows and self.bit_cols[row+dr] < self.num_cols):
                        if(inst.is_bitcell):
                            self.bit_rows[col+dc] += 1
                            self.bit_cols[row+dr] += 1
                            self.parent_design.cell_inst[row + dr, col + dc] = self.parent_design.add_existing_inst(inst,"bit_r{}_c{}".format(row +dr, col+dc))
                            self.parent_design.connect_inst(self.parent_design.get_bitcell_pins(row+dr, col+dc))

    def connect_array(self) -> None:
        self.bit_rows = []
        self.bit_cols = []
        row = 0
        col = 0
        for i in range(self.num_cores_y):
            for j in range (self.num_cores_x):
                self.connect_block(self.core_block, col, row)
                col += len(self.core_block[0])
            col = 0
            row += len(self.core_block)

    def place_inst(self, inst, offset) -> None:
        x = offset[0]
        y = offset[1]
        if "X" in inst.mirror:
            y += inst.height
        if "Y" in inst.mirror:
            x += inst.width
        inst.place((x, y), inst.mirror, inst.rotate)

                            

    def place_block(self, block: block, row: int, col: int, place_x: float, place_y: float, bx, by):
        x_offset = 0
        y_offset = 0
        bounding_x = bx
        bounding_y = by
        for dr in range(len(block)):
            for dc in range(len(block[0])):
                if(self.bit_rows.count(self.num_rows) != self.num_cols and self.bit_cols.count(self.bit_cols) != self.num_rows):
                    if(len(self.bit_rows) <= col + dc):
                        self.bit_rows.append(0)
                    if(len(self.bit_cols) <= row + dr):
                        self.bit_cols.append(0)
                    if(self.bit_rows[col+dc] < self.num_rows and self.bit_cols[row+dr] < self.num_cols):
                        inst = self.parent_design.cell_inst[row + dr, col +dc]
                        if(inst.is_bitcell):
                            self.bit_rows[col+dc] += 1
                            self.bit_cols[row+dr] += 1
                        self.place_inst(inst, (place_x + x_offset, place_y + y_offset))
                        if(place_x + x_offset + inst.width > bounding_x):
                            bounding_x = place_x + x_offset + inst.width
                        if(place_y + y_offset + inst.height > bounding_y):
                            bounding_y = place_y + y_offset + inst.height
                        x_offset += inst.width
            x_offset = 0
            y_offset += inst.height
        return bounding_x, bounding_y

    def place_array(self):
        self.bit_rows = []
        self.bit_cols = []

        row = 0
        col = 0
        place_x = 0
        place_y = 0
        bounding_x = 0
        bounding_y = 0
        for i in range(self.num_cores_y):
            col = 0
            place_x = 0
            for j in range(self.num_cores_x):
                self.parent_design.width, self.parent_design.height= self.place_block(self.core_block, row, col, place_x, place_y, bounding_x, bounding_y)
                if(self.bit_rows.count(self.num_rows) == self.num_cols and self.bit_cols.count(self.bit_cols) == self.num_rows):
                    return

                place_x += self.core_block_width
                col += len(self.core_block[0])
            row += len(self.core_block)
            place_y += self.core_block_height

