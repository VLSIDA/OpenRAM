"""
Generate word line analytical spice code

"""
from wl_utils import header, setup_output_path
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
OPTS = globals.OPTS



class wl_analytical_model():
    def __init__(self, target_path, setup):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        import tech
        if target_path==None:
            self.output_path = self.check_output_path()
        self.net_list = []
        self.net_list.append("*wl analytical model\n")
        for model in tech.spice["fet_models"]:
            self.net_list.append(".include "+str(model)+"\n")
        self.net_list.append("vvdd vdd 0 dc 1v \n")
        self.net_list.append("VWEb_trans sel 0 PWL (0 0v 0.9ns 0v 1ns 1v)\n")
        self.net_list.append("Vclk clk 0 PWL (0 1v 0.9ns 1v 1ns 0v)\n")
        wl, strength, mults  = setup
        self.driver_strength = strength
        self.driver_mults = mults
        self.wl_range = wl
        self.target_log =  self.output_path +"model_log"
        # set rc default value
        self.resistance = 1
        self.capacitance = 0.02


    def check_output_path(self):
        home_path = setup_output_path()
        output_path = home_path +"/Model_output/"
        # make the directory if it doesn't exist
        try:
            os.makedirs(output_path, 0750)
        except OSError as e:
            if e.errno == 17:  # errno.EEXIST
                os.chmod(output_path, 0750)
        return output_path

    def genrate_file(self):
        self.spice_file_name = self.output_path+"wl_analytical_model.sp"
        spice_file = open(self.spice_file_name, "w")
        for code in self.net_list:
            spice_file.write(code)
        spice_file.close()

    def driver_circuits(self):
        self.net_list.append("\n")
        #self.net_list.append("xdriver_pre sel wl_inv clk vdd gnd Wordline_driver\n")

        self.net_list.append("Xinv_clk0 clk clk_bar vdd gnd pinverter\n")
        self.net_list.append("Xclk clk gnd min_gate \n")
        self.net_list.append("Xclk_bar clk_bar gnd min_gate\n")
        self.net_list.append("Xnand sel clk_bar wl_inv vdd gnd pnand2\n")
        self.net_list.append("Xsel sel gnd min_gate\n")
        for i in range(self.driver_strength):
            self.net_list.append("Xwl0_ini"+str(i)+" wl0 gnd min_gate\n")

        self.net_list.append("Xwl_inv wl_inv gnd min_gate\n")

    def calibre_gate(self):
        # make sure we dont add wire
        self.wl_range=0

        self.driver_circuits()
        self.add_driver(self.net_list)

        self.define_wire(self.net_list)
        self.define_driver(self.net_list, self.driver_strength)
        self.define_pand(self.net_list, 2)
        self.define_measurement(self.net_list)

    def calibre_wire(self):
        self.driver_circuits()

        self.add_driver(self.net_list)
        self.add_wl_RC(self.net_list)

        self.define_wire(self.net_list)
        self.define_driver(self.net_list, self.driver_strength)
        self.define_pand(self.net_list)
        self.define_measurement(self.net_list)

    def main_setup(self):
        self.driver_circuits()

        self.add_driver(self.net_list)
        self.add_wl_RC(self.net_list)
        self.add_wl_6t(self.net_list)

        self.define_wire(self.net_list)
        self.define_driver(self.net_list, self.driver_strength)
        self.define_pand(self.net_list, 2)
        self.define_measurement(self.net_list)

    def add_driver(self,source_file):
        # driver/drivers
        source_file.append("\n*driver/drivers\n")
        source_file.append("xdriver0 wl_inv wl0 vdd gnd udrive\n")
        if self.driver_mults>1:
            step = self.wl_range/(self.driver_mults-1)
            for i in range(1,self.driver_mults):
                index = step + i*step
                source_file.append("xdriver"+str(i)+" wl_inv"+str(index)+" wl"+str(index)+" vdd gnd udrive\n")  
        else:
            index = 0

        #index is where input wire ends
        # driver input wire
        source_file.append("\n*driver input wire\n")
        for j in range(index):
            start = "wl_inv"+str(j)
            end = "wl_inv"+str(j+1)
            if j == 0:
                start = "wl_inv"
            source_file.append("xwire_wl_inv"+str(j)+" "+start+" "+end+" 0 wire_rc\n")

    def add_wl_RC(self,source_file):
        # rc load
        source_file.append("\n*wire rc load\n")
        for i in range(self.wl_range):
            start = "wl"+str(i)
            end = "wl"+str(i+1)
            source_file.append("xwl"+str(i)+" "+start+" "+end+" 0 wire_rc\n")
        
    def add_wl_6t(self,source_file):
        # rc load
        source_file.append("\n*wire rc load\n")
        for i in range(self.wl_range):
            start = "wl"+str(i)
            end = "wl"+str(i+1)
            source_file.append("xwl_gate"+str(i)+" "+end+" 0 cell_gate\n")

    def set_rc(self, r, c):
        self.resistance =  "{:f}".format(r)
        self.capacitance = "{:f}".format(c)
    
    def define_wire(self, source_file):
        # rc increase, rc ratio decrease
        #Max diff in delay0.4391
        #Avg delay152.018672727.
        #self.resistance = 1.698
        #self.capacitance = "0.000046"
        #source_file.append("\n.subckt wl_rc in out rcgnd\n")
        #source_file.append("rwl in out "+str(self.resistance)+"\n")
        #source_file.append("cwl out rcgnd "+str(self.capacitance)+"p\n")
        #source_file.append(".ends\n\n")

        #self.resistance = 2
        #self.capacitance = "0.0255"
        # 148.5985 - 117.4447 diff 31.4239


        source_file.append("\n.subckt wire_rc in out rcgnd\n")
        source_file.append("rwls in mid "+str(self.resistance)+"\n")
        source_file.append("cwls mid rcgnd "+str(self.capacitance)+"f\n")
        source_file.append("rwle mid out "+str(self.resistance)+"\n")
        source_file.append("cwle out rcgnd "+str(self.capacitance)+"f\n")
        source_file.append(".ends\n\n")

        gate_r = 1
        gate_c = 0.000889
        source_file.append("\n.subckt min_gate out rcgnd\n")
        source_file.append("rwl out net0 "+str(gate_r)+"\n")
        source_file.append("cwl net0 rcgnd "+str(gate_c)+"p\n")
        source_file.append(".ends\n\n")

        gate_r = 1
        gate_c = 0.002
        source_file.append("\n.subckt cell_gate out rcgnd\n")
        source_file.append("rwl out net0 "+str(gate_r)+"\n")
        source_file.append("cwl net0 rcgnd "+str(gate_c)+"p\n")
        source_file.append(".ends\n\n")


    def define_pand(self, source_file, nand_size):
        size = str(0.09*nand_size)
        source_file.append("\n")
        source_file.append(".SUBCKT pnand2 A B Z vdd gnd\n")
        source_file.append("MM1 Z A net1 gnd NMOS_VTG  W=0.18u L=0.05u\n")
        source_file.append("MM2 net1 B gnd gnd NMOS_VTG W=0.18u L=0.05u\n")
        source_file.append("MM3 vdd A Z vdd PMOS_VTG W=0.18u L=0.05u\n")
        source_file.append("MM4 Z B vdd vdd PMOS_VTG W=0.18u L=0.05u\n")
        source_file.append(".ENDS pnand2\n")

        source_file.append("\n")
        source_file.append(".SUBCKT pinverter A Z vdd gnd\n")
        source_file.append("MM1 Z A gnd gnd NMOS_VTG W=0.09u L=0.05u\n")
        source_file.append("MM2 Z A vdd vdd PMOS_VTG W=0.27u L=0.05u\n")
        source_file.append(".ENDS pinverter\n")

        source_file.append("\n")
        source_file.append(".SUBCKT Wordline_driver decode_out[0] net0 clk vdd gnd\n")
        source_file.append("XWordline_driver_inv_clk0 clk clk_bar[0] vdd gnd pinverter\n")
        source_file.append("XWordline_driver_nand0 decode_out[0] clk_bar[0] net0 vdd gnd pnand2\n")
        #source_file.append("XWordline_driver_inv0 net0 wl[0] vdd gnd udrive\n")
        source_file.append(".ENDS Wordline_driver\n")

    def define_driver(self, source_file, driver_strength):
        val = driver_strength
        basic = 90
        np_ratio =3
        nw = val * basic
        pw = nw * np_ratio
        # driver strength
        source_file.append("\n.subckt udrive in out vdd gnd\n")
        source_file.append("MM1 out in vdd vdd PMOS_VTG W="+str(pw)+"n L=50n\n")
        source_file.append("MM2 out in gnd gnd   NMOS_VTG W="+str(nw)+"n L=50n\n")
        source_file.append(".ends\n")

        source_file.append("\n.subckt udrivef in out vdd gnd\n")
        source_file.append("MM1 out in vdd vdd PMOS_VTG W=5400.00n L=50n\n")
        source_file.append("MM2 out in gnd gnd   NMOS_VTG W=1800.00n L=50n\n") 
        source_file.append(".ends\n")
    
    def define_measurement(self, source_file):
        source_file.append(".measure TRAN tdlay_clk_bar TRIG V(sel) VAL = 0.1 TD = 0.1n RISE = 1 TARG v(clk_bar) VAL = 0.9 RISE = 1\n")
        source_file.append(".measure TRAN tdlay_wl_inv TRIG V(sel) VAL = 0.1 TD = 0.1n RISE = 1 TARG v(wl_inv) VAL = 0.1 FALL = 1\n")
        source_file.append(".measure TRAN tdlay_wl0 TRIG V(sel) VAL = 0.1 TD = 0.1n RISE = 1 TARG v(wl0) VAL = 0.9 RISE = 1\n")
        wl_range=self.wl_range
        source_file.append("\n")
        for i in range(wl_range):
            port = "V(wl"+str(i+1)+")"
            source_file.append(".measure TRAN tdlay"+str(i)+" TRIG V(sel) VAL = 0.1 TD = 0.1n RISE = 1 TARG "+port+" VAL = 0.9 RISE = 1\n")

        source_file.append("\n.tran 0.001n 10n\n")
        source_file.append(".option POST=1 PROBE\n")
        source_file.append(".probe V(*)\n")
        source_file.append(".end\n")

    def run_sim(self):
        import os
        os.system("hspice "+self.spice_file_name+" > "+self.target_log)

    def grep_key(self,key):
        wl_range=self.wl_range
        log_file = open(self.target_log, "r")
        contents = log_file.read() 
        import re
        print "set up: [word line size]", self.wl_range,"[unit r]",self.resistance,"[unit c]",self.capacitance
        print "[driver_strength]",self.driver_strength,"x",self.driver_mults

        val = re.search("{0}(\s*)=(\s*)(\d*(.).*)(\s*)(targ)".format(key), contents)
        val = val.group(3)
        val = val.replace(" ", "")
        unit = val[len(val)-1]
        value = float(val[:-1])
        #print value, unit
        if unit == "p":
            unit_val = 1
        if unit == "n":
            unit_val = 1000
        results= value*unit_val

        return results

    def grep_result(self):
        wl_range=self.wl_range
        log_file = open(self.target_log, "r")
        contents = log_file.read() 
        import re
        #print "set up: [word line size]", self.wl_range,"[unit r]",self.resistance,"[unit c]",self.capacitance
        #print "[driver_strength]",self.driver_strength,"x",self.driver_mults
        results = []
        for i in range(wl_range):
            key = "tdlay"+str(i)
            val = re.search("{0}(\s*)=(\s*)(\d*(.).*)(\s*)(targ)".format(key), contents)
            val = val.group(3)
            val = val.replace(" ", "")
            unit = val[len(val)-1]
            value = float(val[:-1])
            #print value, unit
            if unit == "p":
                unit_val = 1
            if unit == "n":
                unit_val = 1000
            results.append(value*unit_val)
        if len(results)!= 0:
            #print "worst", max(results)
            #print "avg",sum(results)/len(results)
            r_avg = sum(results)/len(results)/430
            #print "diff", max(results)- min(results) 
            r_diff = (max(results)- min(results))/241
        #print "rc ratio", r_avg/r_diff
        return results

if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    setup_lst =[[128, 8 ,1], [64, 8 ,1], [1, 8 ,1]]
    for setup in setup_lst:
        model = wl_analytical_model(None, setup)
        model.main_setup()
        model.genrate_file()
        model.run_sim()
        model.grep_result()
