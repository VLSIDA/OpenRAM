"""
Generate word line analytical spice code

"""
from wl_utils import header, setup_output_path
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
OPTS = globals.OPTS



class wl_analytical_delay():
    def __init__(self, target_path=None):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        if target_path==None:
            self.output_path = self.check_output_path()
        self.target_log =  self.output_path +"model_log"

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

    def test_model(self, model, cell_load = True):
        model.generate_netlist(cell_load)
        self.spice_file_name = self.output_path+"wl_analytical_model.sp"
        model.genrate_file(self.spice_file_name)
        self.run_sim()

        results = []
        for i in range(max(model.word_size,1)): # wl0 always exist
            key = "tdlay_wl"+str(i)
            value, unit = self.read_spice_log(self.target_log, key)
            unit_val = self.convert_delay_unit(unit)
            results.append(value*unit_val)
        return max(results)

    def run_sim(self):
        import os
        os.system("hspice "+self.spice_file_name+" > "+self.target_log)

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


    def convert_delay_unit(self, unit):
        # convert time to ps
        convert_table={"p":1, "n":1000}
        unit_val = convert_table[unit]
        return unit_val

class wl_analytical_model():
    def __init__(self, word_size, driver_strength, mults):  
        self.word_size = word_size
        self.driver_strength = driver_strength
        self.driver_mults = mults
        self.nand_size = 2
        # set rc default value
        self.node_c = 0.02
        self.resistance = 2
        self.capacitance = 0.0225
        self.net_list =[]

    def set_node(self, node_c):
        self.node_c = node_c

    def set_rc(self, r, c):
        self.resistance = r
        self.capacitance = c

    def generate_netlist(self, cell_load = True):
        self.net_list = []
        self.add_lib()
        self.driver_circuits()

        self.add_wl_inv_RC(self.net_list)
        self.add_driver(self.net_list)
        self.add_wl_RC(self.net_list)
        if cell_load == True:
            self.add_cell_rc(self.net_list)

        self.define_node(self.net_list)
        self.define_wire(self.net_list)
        self.define_driver(self.net_list, self.driver_strength)
        self.define_pand(self.net_list, 2)
        self.define_measurement(self.net_list)

    def add_lib(self):
        self.net_list.append("*wl analytical model\n")
        import tech
        for model in tech.spice["fet_models"]:
            self.net_list.append(".include "+str(model)+"\n")
        self.net_list.append("vvdd vdd 0 dc 1v \n")
        self.net_list.append("VWEb_trans sel 0 PWL (0 0v 0.9ns 0v 1ns 1v)\n")
        self.net_list.append("Vclk clk 0 PWL (0 1v 0.9ns 1v 1ns 0v)\n")

    def driver_circuits(self):
        # clk inv
        self.net_list.append("\n")
        self.net_list.append("Xinv_clk0 clk clk_bar vdd gnd pinverter\n")
        self.net_list.append("Xclk clk gnd min_gate \n")
        self.net_list.append("Xclk_bar clk_bar gnd min_gate\n")

        # nand
        self.net_list.append("\n")
        self.net_list.append("Xnand sel clk_bar wl_inv vdd gnd pnand2\n")
        self.net_list.append("Xwl_inv wl_inv gnd min_gate\n")
        for i in range(self.nand_size):
            self.net_list.append("Xsel"+str(i)+" sel gnd min_gate\n")

    def add_driver(self,source_file):
        # driver/drivers
        source_file.append("\n*driver/drivers\n")
        source_file.append("xdriver0 wl_inv wl0 vdd gnd udrive\n")
        if self.driver_mults>1:
            step = self.word_size/(self.driver_mults-1)
            print "step", step
            for i in range(1,self.driver_mults):
                index =  i*step
                source_file.append("xdriver"+str(i)+" wl_inv"+str(index)+" wl"+str(index)+" vdd gnd udrive\n")  
                for j in range(self.driver_strength):
                    self.net_list.append("xdriver_input"+str(i)+"_"+str(j)+" wl_inv"+str(i)+" gnd min_gate\n")


    def add_wl_inv_RC(self,source_file):
        # rc load
        source_file.append("\n*drivers input wire rc \n")
        if self.driver_mults >1:
            for i in range(self.word_size):
                start = "wl_inv"+str(i)
                end = "wl_inv"+str(i+1)
                source_file.append("xwl_inv"+str(i)+" "+start+" "+end+" 0 wire_rc\n")


    def add_wl_RC(self,source_file):
        # rc load
        source_file.append("\n*word line wire rc\n")
        for i in range(self.word_size):
            start = "wl"+str(i)
            end = "wl"+str(i+1)
            source_file.append("xwl"+str(i)+" "+start+" "+end+" 0 wl_wire_rc\n")

    def add_cell_rc(self,source_file):
        # rc load
        source_file.append("\n**word line cell load\n")
        for i in range(self.word_size):
            start = "wl"+str(i)
            end = "wl"+str(i+1)
            source_file.append("xwl_gate"+str(i)+" "+end+" 0 cell_gate\n")

    def define_node(self, source_file):
        source_file.append("\n.subckt min_gate out rcgnd\n")
        source_file.append("cwl out rcgnd "+str(self.node_c)+"p\n")
        source_file.append(".ends\n\n")

    def define_wire(self, source_file):
        r=1
        c=0.0001
        source_file.append("\n.subckt wire_rc in out rcgnd\n")
        source_file.append("rwls in mid "+str(r)+"\n")
        source_file.append("cwls mid rcgnd "+str(c)+"f\n")
        source_file.append("rwle mid out "+str(r)+"\n")
        source_file.append("cwle out rcgnd "+str(c)+"f\n")
        source_file.append(".ends\n\n")


        source_file.append("\n.subckt wl_wire_rc in out rcgnd\n")
        source_file.append("rwls in mid "+str(self.resistance)+"\n")
        source_file.append("cwls mid rcgnd "+str(self.capacitance)+"f\n")
        source_file.append("rwle mid out "+str(self.resistance)+"\n")
        source_file.append("cwle out rcgnd "+str(self.capacitance)+"f\n")
        source_file.append(".ends\n\n")

        self.gate_r = 1
        self.gate_c = 0.002
        source_file.append("\n.subckt cell_gate out rcgnd\n")
        source_file.append("rwl out net0 "+str(self.gate_r)+"\n")
        source_file.append("cwl net0 rcgnd "+str(self.gate_c)+"p\n")
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

        source_file.append("\n")
        for i in range(1, self.word_size):
            port = "V(wl"+str(i+1)+")"
            source_file.append(".measure TRAN tdlay_wl"+str(i)+" TRIG V(sel) VAL = 0.1 TD = 0.1n RISE = 1 TARG "+port+" VAL = 0.9 RISE = 1\n")

        source_file.append("\n.tran 0.001n 100n\n")
        source_file.append(".option POST=1 PROBE\n")
        source_file.append(".probe V(*)\n")
        source_file.append(".end\n")

    def genrate_file(self, target_file):
        spice_file = open(target_file, "w")
        for code in self.net_list:
            spice_file.write(code)
        spice_file.close()

if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]

    word_size = 32
    driver_strength= 8
    node_c = 0.001
    r = 150
    c = 0.2
    #r/c smaller, diff bigger
    #rc bigger, bigger
    # 312.4375 529.9795
    model = wl_analytical_model(word_size = word_size, 
                                driver_strength= driver_strength, 
                                mults =1)
    model.set_node(node_c)
    model.set_rc(r, c)
    test =  wl_analytical_delay()
    delay = test.test_model(model, cell_load = False)
    print "delay",r, c,delay


    model = wl_analytical_model(word_size = 2*word_size, 
                                driver_strength= driver_strength, 
                                mults = 1)
    model.set_node(node_c)
    model.set_rc(r, c)
    test =  wl_analytical_delay()
    delay = test.test_model(model, cell_load = False)
    print "delay",r,c,delay

