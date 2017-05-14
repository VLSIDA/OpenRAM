import debug
import re
import os


class spice:
    """
    This provides a set of useful generic types for hierarchy
    management. If a module is a custom designed cell, it will read from
    the GDS and spice files and perform LVS/DRC. If it is dynamically
    generated, it should implement a constructor to create the
    layout/netlist and perform LVS/DRC.
    Class consisting of a set of modules and instances of these modules
    """

    def __init__(self, name):
        self.name = name

        self.mods = []  # Holds subckts/mods for this module
        self.pins = []  # Holds the pins for this module

        # for each instance, this is the set of nets/nodes that map to the pins for this instance
        # THIS MUST MATCH THE ORDER OF THE PINS (restriction imposed by the
        # Spice format)
        self.conns = []

        self.sp_read()

############################################################
# Spice circuit
############################################################

    def add_pin(self, name):
        """Adds a pin to the pins list"""
        self.pins.append(name)

    def add_pin_list(self, pin_list):
        """Adds a pin_list to the pins list"""
        self.pins = self.pins + pin_list

    def add_mod(self, mod):
        """Adds a subckt/submodule to the subckt hierarchy"""
        self.mods.append(mod)

    def connect_inst(self, args, check=True):
        """Connects the pins of the last instance added
        It is preferred to use the other function with the check to find if
        there is a problem. The check otion can be set to false
        where we dynamically generate groups of connections after a
        group of modules are generated."""

        if (check and (len(self.insts[-1].mod.pins) != len(args))):
            debug.error("Number of net connections ({0}) does not match last instance ({1})".format(len(self.insts[-1].mod.pins),
                                                                                                    len(args)), 1)
        self.conns.append(args)

        if check and (len(self.insts)!=len(self.conns)):
            debug.error("{0} : Not all instance pins ({1}) are connected ({2}).".format(self.name,
                                                                                        len(self.insts),
                                                                                        len(self.conns)))
            debug.error("Instances: \n"+str(self.insts))
            debug.error("-----")
            debug.error("Connections: \n"+str(self.conns),1)



    def sp_read(self):
        """Reads the sp file (and parse the pins) from the library 
           Otherwise, initialize it to null for dynamic generation"""
        if os.path.isfile(self.sp_file):
            debug.info(3, "opening {0}".format(self.sp_file))
            f = open(self.sp_file)
            self.spice = f.readlines()
            for i in range(len(self.spice)):
                self.spice[i] = self.spice[i].rstrip(" \n")

            # find first subckt line in the file
            subckt = re.compile("^.subckt", re.IGNORECASE)
            subckt_line = filter(subckt.search, self.spice)[0]
            # parses line into ports and remove subckt
            self.pins = subckt_line.split(" ")[2:]
        else:
            self.spice = []

    def contains(self, mod, modlist):
        for x in modlist:
            if x.name == mod.name:
                return True
        return False

    def sp_write_file(self, sp, usedMODS):
        """ Recursive spice subcircuit write;
            Writes the spice subcircuit from the library or the dynamically generated one"""
        if not self.spice:
            # recursively write the modules
            for i in self.mods:
                if self.contains(i, usedMODS):
                    continue
                usedMODS.append(i)
                i.sp_write_file(sp, usedMODS)

            if len(self.insts) == 0:
                return
            if self.pins == []:
                return
            # write out the first spice line (the subcircuit)
            sp.write("\n.SUBCKT {0} {1}\n".format(self.name,
                                                  " ".join(self.pins)))

            # every instance must have a set of connections, even if it is empty.
            if  len(self.insts)!=len(self.conns):
                debug.error("{0} : Not all instance pins ({1}) are connected ({2}).".format(self.name,
                                                                                            len(self.insts),
                                                                                            len(self.conns)))
                debug.error("Instances: \n"+str(self.insts))
                debug.error("-----")
                debug.error("Connections: \n"+str(self.conns),1)



            for i in range(len(self.insts)):
                # we don't need to output connections of empty instances.
                # these are wires and paths
                if self.conns[i] == []:
                    continue
                sp.write("X{0} {1} {2}\n".format(self.insts[i].name,
                                                 " ".join(self.conns[i]),
                                                 self.insts[i].mod.name))

            sp.write(".ENDS {0}\n".format(self.name))

        else:
            # write the subcircuit itself
            # Including the file path makes the unit test fail for other users.
            #if os.path.isfile(self.sp_file):
            #    sp.write("\n* {0}\n".format(self.sp_file))
            sp.write("\n".join(self.spice))
            sp.write("\n")

    def sp_write(self, spname):
        """Writes the spice to files"""
        debug.info(3, "Writing to {0}".format(spname))
        spfile = open(spname, 'w')
        spfile.write("*FIRST LINE IS A COMMENT\n")
        usedMODS = list()
        self.sp_write_file(spfile, usedMODS)
        del usedMODS
        spfile.close()

    def delay(self, slope, load=0.0):
        """Inform users undefined delay module while building new modules"""
        #debug.warning("Design Class {0} delay function needs to be defined"
        #              .format(self.__class__.__name__))
        #debug.warning("Class {0} name {1}"
        #              .format(self.__class__.__name__, 
        #                      self.name))         
        # return 0 to keep code running while building
        return {"delay":0.0, "slope":0.0}

    def cal_delay_over_path(self, path, slope):
        result = []
        for i in range(len(path)-1):
            start = path[i]
            end = path[i+1]
            delay = self.cal_delay_between_port(start, end, slope)
            if isinstance(delay["delay"],float):
                result.append(delay)
                slope = delay["slope"]
            else:
                delay_used = {"delay":delay["delay"][0], 
                              "slope":delay["slope"][0]}
                result.append(delay_used)
                slope = delay        
        return result

    def merge_delay_list(self, result):
        sum_delay = {"delay":0, "slope":0}
        for item in result:
            if not isinstance(item["delay"], dict):
                sum_delay["delay"]= sum_delay["delay"] + item["delay"]
                sum_delay["slope"]= item["slope"]  
            else:
                sum_delay["delay"]= sum_delay["delay"][0] + item["delay"] 
                sum_delay["slope"]= item["slope"][0]
        return sum_delay
            

    def cal_delay_between_port(self, start, end, slope):
        mod = self.find_sub_cir(start, end)
        stage_load = self.find_load(start, end)
        if not isinstance(slope, dict):
            mod_delay = mod.delay(slope=slope, load=stage_load)    
        else:
            mod_delay = mod.delay(wire_delay=slope, load=stage_load)    
        return mod_delay

    def find_sub_cir(self, start, end):
        """Find sub cir in inst list by matching ports"""
        result = None
        for inst in self.insts:
            index = self.insts.index(inst)
            if start in self.conns[index] and end in self.conns[index]:
                result = inst.mod
        if result == None:
            debug.error("Could not find matching circuit in {0} \
                         with target ports {1} and {2}"
                        .format(self.name, start, end))
        else:     
            return result

    def find_load_cir(self, start, end):
        """Find load cir in inst list by only matching end"""
        result = []
        for inst in self.insts:
            index = self.insts.index(inst)
            if start not in self.conns[index] and\
               end in self.conns[index]:
                result.append(inst.mod)
        return result

    def find_load(self, start, end):
        """Calculate sum of load cir """
        cir_lst = self.find_load_cir(start, end)
        if len (cir_lst)==1:
            return cir_lst[0].input_load()
        else: # merge load has not consider rc net work yet
            result = 0
            for cir in cir_lst:
                try:
                    load = cir.input_load()
                    result = result + load
                except:
                    load = None
                    debug.warning("cir input load skipped {0}".format(cir))
            return result

    def sum_delay(self, start, end):
        if isinstance(start["delay"],list): # start delay is list
            start_delay =  start["delay"][-1]
        else:
            start_delay = start["delay"]

        if not isinstance(end["delay"],list): # end delay not list
            result = {"delay": start_delay + end["delay"],
                      "slope": end["slope"]}
        else:
            for index in range(len(end["delay"])):
                end["delay"][index]=end["delay"][index]+ start_delay 
            result = end
        return result

    def view_mod(self):
        for inst in self.insts:
            if "via" not in inst.mod.name and \
                "wire" not in inst.mod.name and\
                "path" not in inst.mod.name:
                debug.info(3, " {0} inst {1}".format(self.name, inst))

    def gernerate_wire(self, lump_num, wire_length, wire_width):
        wire_r, wire_c = self.cal_wire_rc(wire_length, wire_width)
        result = {}
        result["lump_num"] = lump_num
        result["wire_r"] = wire_r 
        result["wire_c"] = wire_c               
        return result

    def cal_wire_rc(self, wire_length, wire_width):
        wire_uint_c = 0.64 # this should be a tech parameter eventually
        wire_uint_r = 0.075  # this should be a tech parameter eventually
        wire_r = wire_uint_r * wire_length/wire_width
        wire_c = wire_uint_r * (wire_length*wire_width)
        return wire_r, wire_c

    def cal_delay_with_rc(self, r, c ,slope):
        delay = 0.7*r*c#this value is in fs
        delay = delay*0.001#make the unit to ps
        #slope = 3 + 0.01* slope + delay*0.8*2# this is just a quick fit
        slope = delay*0.6*2 + 0.005* slope # the constant before slope should be explained as r change
        return {"delay":delay, "slope":slope}

    def wire_delay(self, slope, driver, wire):
        r , c = driver
        delay_to_out_node = 0.7*r*(c+wire["lump_num"]*0.5*wire["wire_c"])
        delay_to_out_node = delay_to_out_node*0.001#make the unit to ps
        slope_at_out_node = delay_to_out_node*0.6*2 + 0.005* slope # the constant before slope should be explained as r change
        result = self.propagate_delay_over_wire(slope=slope_at_out_node, 
                                 driver_r=r,
                                 wire=wire)
        init = {"delay":delay_to_out_node, "slope":0}
        result = self.sum_delay(init,result)
        return result

    def propagate_delay_over_wire(self, slope, driver_r, wire):
        r = driver_r
        delay_lst = []
        slope_lst = []
        for i in range(wire["lump_num"]):
            faction = (i+1.0)/wire["lump_num"]
            delay = (r + faction * wire["wire_r"])*wire["wire_c"]/wire["lump_num"]
            local_slope = delay*2 + slope

            delay_lst.append(delay)
            slope_lst.append(local_slope)
        result={"delay":delay_lst, "slope":slope_lst}
        return result
