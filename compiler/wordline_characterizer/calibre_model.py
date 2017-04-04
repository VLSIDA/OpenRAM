#!/usr/bin/env python2.7
"""
Calibre the ana model
"""
from wl_utils import header, setup_output_path
from wl_delay import wl_delay
from wl_analytical_model import wl_analytical_model, wl_analytical_delay
import os, sys
import globals
OPTS = globals.OPTS
from decimal import Decimal

class calibre_model():
    def __init__(self, word_size, driver_size):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        self.word_size = word_size
        self.output_path = setup_output_path()
        self.driver_size = driver_size
        self.driver_mults = 1
    
    def calibre(self, wire_only = False):
        # calibre node, wire RC, 6t cell_rc
        # we use measured 0 , 0.25 word size adn 0.5 word_size as calibre point
        # need to space them out to keep it increase
        #node_ref = 112.2173 

        node_ref = self.set_up_node_ref(0,  cell_load=False)
        #node_c = 0.000712966918945
        node_c = self.calibre_node_capciatance(target_delay = node_ref)

        #print "node capacitance",node_c
        c_ref = self.set_up_node_ref(0.25 * self.word_size, wl_pos = 0.25 * self.word_size, cell_load=True)
        r_ref = self.set_up_node_ref(0.5 * self.word_size, wl_pos = 0.5 * self.word_size, cell_load=True)
        #c_ref = 145.0287 
        #r_ref = 177.2607
        #print "node_ref", node_ref, c_ref , r_ref



        c = self.set_C(target = c_ref, node_c=node_c)
        r = self.set_R(target = r_ref, node_c=node_c, c = c)

        r,c =self.tune_c(r_ref =  r_ref, c_ref = c_ref, node_c = node_c, r = r, c = c)
        #print "node_c",node_c,"r",r,"c",c

        predict = self.predict(node_c = node_c, r = r, c = c, word_size = self.word_size)


        driver_size = self.driver_size
        config = [int(self.word_size),driver_size,1]
        ref = wl_delay()
        measured = ref.single_test(config=config, cell_load=True, wl_pos = self.word_size)
        print "word size", self.word_size ,"error",abs(1-predict/max(measured))

    def tune_c(self, r_ref, c_ref, node_c, r, c):
        c = self.set_C(target = c_ref, node_c=node_c, r = r)
        predict_c_ref = self.predict(node_c = node_c, r = r, c = c, word_size = 0.25*self.word_size)
        predict_r_ref = self.predict(node_c = node_c, r = r, c = c, word_size = 0.5 *self.word_size)
        print "tune c: c_ref/predict_c_ref",abs(1-c_ref/predict_c_ref), "r_ref/predict_r_ref",abs(1-r_ref/predict_r_ref)
        if self.is_accurate(c_ref,  predict_c_ref) and self.is_accurate(r_ref,  predict_r_ref):
            return [r, c]
        else:
            return self.tune_r(r_ref =  r_ref, c_ref = c_ref, node_c = node_c, r = r, c = c)


    def tune_r(self, r_ref, c_ref, node_c, r, c):
        r = self.set_R(target = r_ref, node_c=node_c, c = c)
        predict_c_ref = self.predict(node_c = node_c, r = r, c = c, word_size = 0.25*self.word_size)
        predict_r_ref = self.predict(node_c = node_c, r = r, c = c, word_size = 0.5 *self.word_size)
        print "tune r: c_ref/predict_c_ref",abs(1-c_ref/predict_c_ref), "r_ref/predict_r_ref",abs(1-r_ref/predict_r_ref)
        if self.is_accurate(c_ref,  predict_c_ref) and self.is_accurate(r_ref,  predict_r_ref):
            return [r, c]
        else:
            return self.tune_c(r_ref =  r_ref, c_ref = c_ref, node_c = node_c, r = r, c = c)


    def predict(self, node_c, r, c, word_size):
        word_size = int(word_size)
        config = [word_size, self.driver_size,self.driver_mults]
        model = wl_analytical_model(word_size = word_size, 
                                    driver_strength= self.driver_size, 
                                    mults = 1)
        model.set_node(node_c)
        model.set_rc(r, c)

        test =  wl_analytical_delay()
        delay = test.test_model(model, cell_load = False)
        return delay

    def set_up_node_ref(self, word_size, cell_load = False, wl_pos=0):
        # should test without the wl load and mults should be 1 regardless
        driver_size = self.driver_size
        config = [int(word_size),driver_size,1]
        ref = wl_delay()
        ref = ref.single_test(config=config, cell_load=cell_load, wl_pos = wl_pos)
        # we should scan the whole line not single!
        return max(ref)

    def calibre_node_capciatance(self, target_delay, bound = [0, 0.1]):
        # should test without the wl load and mults should be 1 regardless
        word_size = 0
        node_c = sum(bound)*0.5
        model = wl_analytical_model(word_size = word_size, 
                                    driver_strength= self.driver_size, 
                                    mults = 1)
        model.set_node(node_c)

        test =  wl_analytical_delay()
        delay = test.test_model(model, cell_load = False)
        accurate  = self.is_accurate(target_delay, delay)
        if not accurate:    
            bound = self.binary_search(target_delay, delay, node_c ,bound)
            return self.calibre_node_capciatance(target_delay, bound)
        else:
            return node_c  

    def set_C(self, target, node_c, r = 0 , bound = [0,1], depth = 0):
        c = sum(bound)*0.5
        word_size = int(0.25 * self.word_size)
        config = [word_size, self.driver_size,self.driver_mults]
        # should test without the wl load, but now we bring in mults
        # need to test wire impact on drivers
        model = wl_analytical_model(word_size = word_size, 
                                    driver_strength= self.driver_size, 
                                    mults = self.driver_mults)
        model.set_node(node_c)
        model.set_rc(r, c)

        test =  wl_analytical_delay()
        delay = test.test_model(model, cell_load = False)
        accurate  = self.is_accurate(target, delay)
        #print "setting c", c, bound, target, delay
        if depth > 10:
            return c  
        if not accurate:
            bound = self.binary_search(target, delay, c, bound)#change C to match start point  
            return self.set_C(target=target, node_c = node_c, r = r,bound=bound, depth = depth+1)
        else:
            return c  

    def set_R(self, target, node_c, c, bound = [0,100], depth =0):
        r = sum(bound)*0.5
        word_size = int(0.5*self.word_size)
        config = [word_size, self.driver_size,self.driver_mults]
        model = wl_analytical_model(word_size = word_size, 
                                    driver_strength= self.driver_size, 
                                    mults = self.driver_mults)
        model.set_node(node_c)
        model.set_rc(r, c)

        test =  wl_analytical_delay()
        delay = test.test_model(model, cell_load = False)
        accurate  = self.is_accurate(target, delay)
        #print "setting r", r, bound, target, delay
        if depth > 10:
            return r  
        if not accurate:
            bound = self.binary_search(target, delay, r, bound)#change R to match end point  
            return self.set_R(target=target, node_c = node_c, c = c, bound=bound, depth = depth+1)
        else:
            return r  

    def is_accurate(self, target, value):
        precision = 0.03
        if abs(target - value) > target * precision:
            return False
        else:
            return True

    def init_bound(self, func, target):
        delay = self.func()

    def binary_search(self, target, value, parameter, parameter_max_min):
        if target >= value:# increas R/C to increase delay, update min
            parameter_max_min = [parameter, max(parameter_max_min)]    
        else:# decreas R/C to half of tested value to decrease delay, update max
            parameter_max_min = [min(parameter_max_min),parameter]    
        result_parameter = sum(parameter_max_min)*0.5  
        return parameter_max_min


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]


    for i in range (1,32):
        word_size = i * 32
        test = calibre_model(word_size, 32)
        #header(__file__, OPTS.tech_name,test.output_path)
        test.calibre()
    
    """
    test = calibre_model(1024, 2)
    header(__file__, OPTS.tech_name,test.output_path)
    test.calibre()

    test = calibre_model(1024, 4)
    header(__file__, OPTS.tech_name,test.output_path)
    test.calibre()

    test = calibre_model(1024, 8)
    header(__file__, OPTS.tech_name,test.output_path)
    test.calibre()

    test = calibre_model(1024, 16)
    header(__file__, OPTS.tech_name,test.output_path)
    test.calibre()

    test = calibre_model(1024, 32)
    header(__file__, OPTS.tech_name,test.output_path)
    test.calibre()
    """

