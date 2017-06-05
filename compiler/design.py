import hierarchy_layout
import hierarchy_spice
import globals
import calibre
import debug
import os

OPTS = globals.get_opts()


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
        
        # Check if the name already exists, if so, give an error
        # because each reference must be a unique name.
        ok_list = ['ms_flop.ms_flop', 'bitcell.bitcell', 'contact.contact',
                   'ptx.ptx', 'sram.sram',
                   'hierarchical_predecode2x4.hierarchical_predecode2x4',
                   'hierarchical_predecode3x8.hierarchical_predecode3x8']
        if name not in design.name_map:
            design.name_map.append(name)
        elif str(self.__class__) in ok_list:
            pass
        else:
            debug.error("Duplicate layout reference name {0} of class {1}. GDS2 requires names be unique.".format(name,self.__class__),-1)
        
        

    def DRC_LVS(self):
        """Checks both DRC and LVS for a module"""
        if OPTS.check_lvsdrc:
            tempspice = OPTS.openram_temp + "/temp.sp"
            tempgds = OPTS.openram_temp + "/temp.gds"
            self.sp_write(tempspice)
            self.gds_write(tempgds)
            debug.check(calibre.run_drc(self.name, tempgds) == 0,"DRC failed for {0}".format(self.name))
            debug.check(calibre.run_lvs(self.name, tempgds, tempspice) == 0,"LVS failed for {0}".format(self.name))
            os.remove(tempspice)
            os.remove(tempgds)

    def DRC(self):
        """Checks DRC for a module"""
        if OPTS.check_lvsdrc:
            tempgds = OPTS.openram_temp + "/temp.gds"
            self.gds_write(tempgds)
            debug.check(calibre.run_drc(self.name, tempgds) == 0,"DRC failed for {0}".format(self.name))
            os.remove(tempgds)

    def LVS(self):
        """Checks LVS for a module"""
        if OPTS.check_lvsdrc:
            tempspice = OPTS.openram_temp + "/temp.sp"
            tempgds = OPTS.openram_temp + "/temp.gds"
            self.sp_write(tempspice)
            self.gds_write(tempgds)
            debug.check(calibre.run_lvs(self.name, tempgds, tempspice) == 0,"LVS failed for {0}".format(self.name))
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
