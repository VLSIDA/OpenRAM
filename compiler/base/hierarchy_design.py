import hierarchy_layout
import hierarchy_spice
import globals
import verify
import debug
import os
from globals import OPTS

total_drc_errors = 0 
total_lvs_errors = 0

class hierarchy_design(hierarchy_spice.spice, hierarchy_layout.layout):
    """
    Design Class for all modules to inherit the base features.
    Class consisting of a set of modules and instances of these modules
    """
    name_map = []

    def __init__(self, name):
        try:
            self.gds_file
        except AttributeError:
            self.gds_file = OPTS.openram_tech + "gds_lib/" + name + ".gds"
        try:
            self.sp_file
        except AttributeError:
            self.sp_file = OPTS.openram_tech + "sp_lib/" + name + ".sp"

        self.name = name
        hierarchy_layout.layout.__init__(self, name)
        hierarchy_spice.spice.__init__(self, name)
        
            
        # Check if the name already exists, if so, give an error
        # because each reference must be a unique name.
        # These modules ensure unique names or have no changes if they
        # aren't unique
        ok_list = ['ms_flop',
                   'dff',
                   'dff_buf',
                   'bitcell',
                   'contact',
                   'ptx',
                   'sram',
                   'hierarchical_predecode2x4',
                   'hierarchical_predecode3x8']
        if name not in hierarchy_design.name_map:
            hierarchy_design.name_map.append(name)
        else:
            for ok_names in ok_list:
                if ok_names in self.__class__.__name__:
                    break
            else:
                debug.error("Duplicate layout reference name {0} of class {1}. GDS2 requires names be unique.".format(name,self.__class__),-1)
        
        
    def get_layout_pins(self,inst):
        """ Return a map of pin locations of the instance offset """
        # find the instance
        for i in self.insts:
            if i.name == inst.name:
                break
        else:
            debug.error("Couldn't find instance {0}".format(inst_name),-1)
        inst_map = inst.mod.pin_map
        return inst_map
        

    def DRC_LVS(self, final_verification=False):
        """Checks both DRC and LVS for a module"""
        # Unit tests will check themselves.
        # Do not run if disabled in options.

        if (not OPTS.is_unit_test and OPTS.check_lvsdrc and (OPTS.inline_lvsdrc or final_verification)):

            global total_drc_errors
            global total_lvs_errors
            tempspice = OPTS.openram_temp + "/temp.sp"
            tempgds = OPTS.openram_temp + "/temp.gds"
            self.sp_write(tempspice)
            self.gds_write(tempgds)

            num_drc_errors = verify.run_drc(self.name, tempgds, final_verification) 
            num_lvs_errors = verify.run_lvs(self.name, tempgds, tempspice, final_verification) 
            debug.check(num_drc_errors == 0,"DRC failed for {0} with {1} error(s)".format(self.name,num_drc_errors))
            debug.check(num_lvs_errors == 0,"LVS failed for {0} with {1} errors(s)".format(self.name,num_lvs_errors))
            total_drc_errors += num_drc_errors
            total_lvs_errors += num_lvs_errors

            os.remove(tempspice)
            os.remove(tempgds)

    def DRC(self, final_verification=False):
        """Checks DRC for a module"""
        # Unit tests will check themselves.
        # Do not run if disabled in options.

        if (not OPTS.is_unit_test and OPTS.check_lvsdrc and (OPTS.inline_lvsdrc or final_verification)):
            global total_drc_errors
            tempgds = OPTS.openram_temp + "/temp.gds"
            self.gds_write(tempgds)
            num_errors = verify.run_drc(self.name, tempgds, final_verification)  
            total_drc_errors += num_errors
            debug.check(num_errors == 0,"DRC failed for {0} with {1} error(s)".format(self.name,num_error))

            os.remove(tempgds)

    def LVS(self, final_verification=False):
        """Checks LVS for a module"""
        # Unit tests will check themselves.
        # Do not run if disabled in options.

        if (not OPTS.is_unit_test and OPTS.check_lvsdrc and (OPTS.inline_lvsdrc or final_verification)):
            global total_lvs_errors
            tempspice = OPTS.openram_temp + "/temp.sp"
            tempgds = OPTS.openram_temp + "/temp.gds"
            self.sp_write(tempspice)
            self.gds_write(tempgds)
            num_errors = verify.run_lvs(self.name, tempgds, tempspice, final_verification)
            total_lvs_errors += num_errors
            debug.check(num_errors == 0,"LVS failed for {0} with {1} error(s)".format(self.name,num_errors))
            os.remove(tempspice)
            os.remove(tempgds)

    def __str__(self):
        """ override print function output """
        return "design: " + self.name

    def __repr__(self):
        """ override print function output """
        text="( design: " + self.name + " pins=" + str(self.pins) + " " + str(self.width) + "x" + str(self.height) + " )\n"
        for i in self.objs:
            text+=str(i)+",\n"
        for i in self.insts:
            text+=str(i)+",\n"
        return text
     
