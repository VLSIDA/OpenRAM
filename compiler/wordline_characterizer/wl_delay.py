#!/usr/bin/env python2.7
"""
Run a regresion test on a wordline_driver array
"""
from wl_utils import header, setup_output_path
import unittest
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre
import sys
OPTS = globals.OPTS

class wl_delay():
    def __init__(self):
        self.output_path, self.log_file = self.setup_output_path()

    def setup_output_path(self):
        # find the home path of test code 
        home_path = setup_output_path()
        output_path = home_path +"/OpenRAM_output/"
        log_file = home_path+"/exp_log"
        # make the directory if it doesn't exist
        try:
            os.makedirs(output_path, 0750)
        except OSError as e:
            if e.errno == 17:  # errno.EEXIST
                os.chmod(output_path, 0750)
        return output_path, log_file
    

    def single_test(self, config, wl_pos, cell_load=True):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False
        debug.info(2, "Checking driver")

        name="test_mod"
        import test_module
        word_size, strength, extra = config
        #print "strength",strength,"x",extra,". Word size ", word_size
        exp_log =  open(self.log_file, "a")
        exp_log.write("Word size "+str(word_size)+". Strength "+str(strength)+"x"+str(extra)+"\n")
        exp_log.close()
        set_result = []
        for i in range(10,11):
            WL_pos = 0.1*i
            #tm = test_module.test_module(name, word_size,  WL_pos, extra, strength)
            tm = test_module.test_module(name = name, word_size = word_size, driver_size = strength, mults = extra)
            tm.set_wl_label(wl_pos)
            tm.create_layout(cell_load = cell_load)
            #tm = test_module.test_module(name, word_size,  WL_pos, extra) #do not specify to auto size

            strength =  tm.inv_size
            nand_size = tm.nand_size        
            OPTS.check_lvsdrc = True
            pex_lib = self.generate_pex(tm, self.output_path)
            #value, unit  = self.setup_hspice(self.output_path, pex_lib)
            #pex_file = self.local_check(tm,strength, extra, word_size, WL_pos, nand_size)
            value, unit = self.setup_hspice(self.output_path, pex_lib)
            #print strength," ", extra," ", word_size," ", nand_size," ",value, unit
            exp_log =  open(self.log_file, "a")
            exp_log.write("WL "+ str(WL_pos)+". delay "+str(value)+str(unit)+"\n")
            exp_log.close()
            unit_val = self.convert_delay_unit(unit)
            set_result.append(value*unit_val)

        avg = sum(set_result)/len(set_result)
        diff = max(set_result)-min(set_result)
        wrst = max(set_result)

        exp_log =  open(self.log_file, "a")
        exp_log.write("Worst Delay"+str(wrst)+"\n")
        exp_log.write("Max diff in delay"+str(diff)+"\n")
        exp_log.write("Avg delay"+str(avg)+".\n\n")
        exp_log.close()
        return set_result        

    def convert_delay_unit(self, unit):
        # convert time to ps
        convert_table={"p":1, "n":1000}
        unit_val = convert_table[unit]
        return unit_val

    def generate_pex(self, test_module, path):
        tempspice = path + test_module.name+".sp"
        tempgds = path + test_module.name+".gds"

        test_module.sp_write(tempspice)
        test_module.gds_write(tempgds)
        
        assert(calibre.run_drc(test_module.name, 
                                         tempgds)==0)
        assert(calibre.run_lvs(test_module.name, 
                                         tempgds, 
                                         tempspice)==0)
        pex_file = test_module.name+"_pex.sp"
        #pex_file = "temp_pex.sp"
        assert(calibre.run_pex(test_module.name, 
                                         tempgds,
                                         tempspice, 
                                         output=path + pex_file)==0)
        return path + pex_file 
        
    def setup_hspice(self, path, test_model):
        stim_file = path+"stim_hspice.sp"
        from write_stim import write_stim
        write_stim(test_model, stim_file)

        cmd = ("hspice  "+stim_file+" >  "+str(self.output_path)+"spice_log")
        os.system(cmd)
        value,unit =self.read_spice_log(str(self.output_path)+"spice_log","tdlay")
        return [value,unit]

    def read_spice_log(self,log_file, key):
        log_file =  open(log_file, "r")
        contents = log_file.read() 
        import re
        val = re.search("{0}(\s*)=(\s*)(\d*(.).*)(\s*)(targ)".format(key), contents)
        val = val.group(3)
        val = val.replace(" ", "")
        unit = val[len(val)-1]
        value = float(val[:-1])
        return [value,unit]


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    test = wl_delay()
    header(__file__, OPTS.tech_name,test.output_path)
    config = [16,8,4]
    test.single_test(config, wire_only = True)
