"""
Generate stimuls file
"""
import tech

class write_stim():
    def __init__(self, test_model, target_file):
        self.net_list = []
        self.net_list.append("*RC delay\n")
        for model in tech.spice["fet_models"]:
            self.net_list.append(".include "+str(model)+"\n")
        self.net_list.append(".include "+str(test_model)+"\n\n")

        self.net_list.append("vvdd vdd 0 dc 1v \n")
        self.net_list.append("vsel sel 0 PWL (0 0v 2n 0v 2.1n 1V)\n")
        self.net_list.append("vclk clk 0 PWL (0 1v 2n 1v 2.1n 0V))\n\n")

        self.net_list.append("xtestmod sel clk wl vdd 0 test_mod\n")
        self.net_list.append(".NODESET V(wl)=0\n\n")

        self.net_list.append(".tran 0.01n 100n UIC \n")
        self.net_list.append(".option POST=1 PROBE\n")
        self.net_list.append(".probe V(*)\n\n")

        self.net_list.append(".measure TRAN tdlay TRIG V(sel) VAL = 0.1 TD = 1n RISE = 1 TARG V(wl) VAL = 0.9 RISE = 1\n")
        self.net_list.append(".end\n\n")
        self.genrate_file(target_file)


    def genrate_file(self, target_file):
        self.file = open(target_file, "w")
        for code in self.net_list:
            self.file.write(code)
        self.file.close()
