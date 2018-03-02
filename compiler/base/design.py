import hierarchy_layout
import hierarchy_spice
import globals
import verify
import debug
import os
from globals import OPTS


class design(hierarchy_spice.spice, hierarchy_layout.layout):
    """
    Design Class for all modules to inherit the base features.
    Class consisting of a set of modules and instances of these modules
    """
    name_map = []
    

    def __init__(self, name):
        self.gds_file = OPTS.openram_tech + "gds_lib/" + name + ".gds"
        self.sp_file = OPTS.openram_tech + "sp_lib/" + name + ".sp"

        self.name = name
        hierarchy_layout.layout.__init__(self, name)
        hierarchy_spice.spice.__init__(self, name)

        self.setup_drc_constants()
        
        # Check if the name already exists, if so, give an error
        # because each reference must be a unique name.
        # These modules ensure unique names or have no changes if they
        # aren't unique
        ok_list = ['ms_flop.ms_flop',
                   'bitcell.bitcell',
                   'contact.contact',
                   'ptx.ptx',
                   'sram.sram',
                   'hierarchical_predecode2x4.hierarchical_predecode2x4',
                   'hierarchical_predecode3x8.hierarchical_predecode3x8']
        if name not in design.name_map:
            design.name_map.append(name)
        elif str(self.__class__) in ok_list:
            pass
        else:
            debug.error("Duplicate layout reference name {0} of class {1}. GDS2 requires names be unique.".format(name,self.__class__),-1)
        
    def setup_drc_constants(self):
        """ These are some DRC constants used in many places in the compiler."""
        from tech import drc
        self.well_width = drc["minwidth_well"]
        self.poly_width = drc["minwidth_poly"]
        self.poly_space = drc["poly_to_poly"]        
        self.m1_width = drc["minwidth_metal1"]
        self.m1_space = drc["metal1_to_metal1"]        
        self.m2_width = drc["minwidth_metal2"]
        self.m2_space = drc["metal2_to_metal2"]        
        self.m3_width = drc["minwidth_metal3"]
        self.m3_space = drc["metal3_to_metal3"]
        self.active_width = drc["minwidth_active"]
        self.contact_width = drc["minwidth_contact"]
        
        self.poly_to_active = drc["poly_to_active"]
        self.poly_extend_active = drc["poly_extend_active"]
        self.contact_to_gate = drc["contact_to_gate"]
        self.well_enclose_active = drc["well_enclosure_active"]
        self.implant_enclose_active = drc["implant_enclosure_active"]
        self.implant_space = drc["implant_to_implant"]   
        
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
        if OPTS.check_lvsdrc:
            tempspice = OPTS.openram_temp + "/temp.sp"
            tempgds = OPTS.openram_temp + "/temp.gds"
            self.sp_write(tempspice)
            self.gds_write(tempgds)
            debug.check(verify.run_drc(self.name, tempgds) == 0,"DRC failed for {0}".format(self.name))
            debug.check(verify.run_lvs(self.name, tempgds, tempspice, final_verification) == 0,"LVS failed for {0}".format(self.name))
            os.remove(tempspice)
            os.remove(tempgds)

    def DRC(self):
        """Checks DRC for a module"""
        if OPTS.check_lvsdrc:
            tempgds = OPTS.openram_temp + "/temp.gds"
            self.gds_write(tempgds)
            debug.check(verify.run_drc(self.name, tempgds) == 0,"DRC failed for {0}".format(self.name))
            os.remove(tempgds)

    def LVS(self, final_verification=False):
        """Checks LVS for a module"""
        if OPTS.check_lvsdrc:
            tempspice = OPTS.openram_temp + "/temp.sp"
            tempgds = OPTS.openram_temp + "/temp.gds"
            self.sp_write(tempspice)
            self.gds_write(tempgds)
            debug.check(verify.run_lvs(self.name, tempgds, tempspice, final_verification) == 0,"LVS failed for {0}".format(self.name))
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
     
    def analytical_power(self, proc, vdd, temp, load):
        """ Get total power of a module  """
        total_module_power = self.return_power()
        for inst in self.insts:
            total_module_power += inst.mod.analytical_power(proc, vdd, temp, load)
        return total_module_power
