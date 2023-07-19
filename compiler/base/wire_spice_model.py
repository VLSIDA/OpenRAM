# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

class wire_spice_model():
    """
    This is the spice class to represent a wire
    """
    def __init__(self, lump_num, wire_length, wire_width):
        self.lump_num = lump_num # the number of segment the wire delay has
        self.wire_c = self.cal_wire_c(wire_length, wire_width) # c in each segment
        self.wire_r = self.cal_wire_r(wire_length, wire_width) # r in each segment

    def cal_wire_c(self, wire_length, wire_width):
        from openram.tech import spice
        # Convert the F/um^2 to fF/um^2 then multiple by width and length
        # FIXME: shouldn't it be 1e15?
        total_c = (spice["wire_unit_c"]*1e12) * wire_length * wire_width
        wire_c = total_c / self.lump_num
        return wire_c

    def cal_wire_r(self, wire_length, wire_width):
        from openram.tech import spice
        total_r = spice["wire_unit_r"] * wire_length / wire_width
        wire_r = total_r / self.lump_num
        return wire_r

    def return_input_cap(self):
        return 0.5 * self.wire_c * self.lump_num

    def return_delay_over_wire(self, slew, swing = 0.5):
        # delay will be sum of arithmetic sequence start from
        # rc to self.lump_num*rc with step of rc

        swing_factor = abs(math.log(1-swing)) # time constant based on swing
        sum_factor = (1+self.lump_num) * self.lump_num * 0.5 # sum of the arithmetic sequence
        delay = sum_factor * swing_factor * self.wire_r * self.wire_c
        slew = delay * 2 + slew
        result= delay_data(delay, slew)
        return result
