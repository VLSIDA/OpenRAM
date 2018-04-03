import itertools
import geometry
import gdsMill
import debug
from tech import drc, GDS
from tech import layer as techlayer
import os
from vector import vector
from pin_layout import pin_layout
import lef

class layout(lef.lef):
    """
    Class consisting of a set of objs and instances for a module
    This provides a set of useful generic types for hierarchy
    management. If a module is a custom designed cell, it will read from
    the GDS and spice files and perform LVS/DRC. If it is dynamically
    generated, it should implement a constructor to create the
    layout/netlist and perform LVS/DRC.
    """

    def __init__(self, name):
        lef.lef.__init__(self, ["metal1", "metal2", "metal3"])
        self.name = name
        self.width = None
        self.height = None
        self.insts = []      # Holds module/cell layout instances
        self.objs = []       # Holds all other objects (labels, geometries, etc)
        self.pin_map = {}    # Holds name->pin_layout map for all pins
        self.visited = False # Flag for traversing the hierarchy 
        self.is_library_cell = False # Flag for library cells 
        self.gds_read()

    ############################################################
    # GDS layout
    ############################################################
    def offset_all_coordinates(self):
        """ This function is called after everything is placed to
        shift the origin in the lowest left corner """
        offset = self.find_lowest_coords()
        self.translate_all(offset)

    def get_gate_offset(self, x_offset, height, inv_num):
        """Gets the base offset and y orientation of stacked rows of gates
        assuming a minwidth metal1 vdd/gnd rail. Input is which gate
        in the stack from 0..n
        """

        if (inv_num % 2 == 0):
            base_offset=vector(x_offset, inv_num * height)
            y_dir = 1
        else:
            # we lose a rail after every 2 gates            
            base_offset=vector(x_offset, (inv_num+1) * height - (inv_num%2)*drc["minwidth_metal1"])
            y_dir = -1
            
        return (base_offset,y_dir)


    def find_lowest_coords(self):
        """Finds the lowest set of 2d cartesian coordinates within
        this layout"""

        if len(self.objs)>0:
            lowestx1 = min(obj.lx() for obj in self.objs if obj.name!="label")
            lowesty1 = min(obj.by() for obj in self.objs if obj.name!="label")
        else:
            lowestx1=lowesty1=None
        if len(self.insts)>0:
            lowestx2 = min(inst.lx() for inst in self.insts)
            lowesty2 = min(inst.by() for inst in self.insts)
        else:
            lowestx2=lowesty2=None
        if lowestx1==None:
            return vector(lowestx2,lowesty2)
        elif lowestx2==None:
            return vector(lowestx1,lowesty1)            
        else:
            return vector(min(lowestx1, lowestx2), min(lowesty1, lowesty2))

    def find_highest_coords(self):
        """Finds the highest set of 2d cartesian coordinates within
        this layout"""

        if len(self.objs)>0:
            highestx1 = max(obj.rx() for obj in self.objs if obj.name!="label")
            highesty1 = max(obj.uy() for obj in self.objs if obj.name!="label")
        else:
            highestx1=highesty1=None        
        if len(self.insts)>0:            
            highestx2 = max(inst.rx() for inst in self.insts)
            highesty2 = max(inst.uy() for inst in self.insts)
        else:
            highestx2=highesty2=None
        if highestx1==None:
            return vector(highestx2,highesty2)
        elif highestx2==None:
            return vector(highestx1,highesty1)            
        else:
            return vector(max(highestx1, highestx2), max(highesty1, highesty2))


    def translate_all(self, offset):
        """
        Translates all objects, instances, and pins by the given (x,y) offset
        """
        for obj in self.objs:
            obj.offset = vector(obj.offset - offset)
        for inst in self.insts:
            inst.offset = vector(inst.offset - offset)
            # The instances have a precomputed boundary that we need to update.
            if inst.__class__.__name__ == "instance":
                inst.compute_boundary(offset.scale(-1,-1))
        for pin_name in self.pin_map.keys():
            # All the pins are absolute coordinates that need to be updated.
            pin_list = self.pin_map[pin_name]
            for pin in pin_list:
                pin.rect = [pin.ll() - offset, pin.ur() - offset]
            

    def add_inst(self, name, mod, offset=[0,0], mirror="R0",rotate=0):
        """Adds an instance of a mod to this module"""
        self.insts.append(geometry.instance(name, mod, offset, mirror, rotate))
        debug.info(3, "adding instance {}".format(self.insts[-1]))
        debug.info(4, "instance list: " + ",".join(x.name for x in self.insts))
        return self.insts[-1]

    def get_inst(self, name):
        """Retrieve an instance by name"""
        for inst in self.insts:
            if inst.name == name:
                return inst
        return None
    
    def add_rect(self, layer, offset, width=0, height=0):
        """Adds a rectangle on a given layer,offset with width and height"""
        if width==0:
            width=drc["minwidth_{}".format(layer)]
        if height==0:
            height=drc["minwidth_{}".format(layer)]
        # negative layers indicate "unused" layers in a given technology
        layer_num = techlayer[layer]
        if layer_num >= 0:
            self.objs.append(geometry.rectangle(layer_num, offset, width, height))
            return self.objs[-1]
        return None

    def add_rect_center(self, layer, offset, width=0, height=0):
        """Adds a rectangle on a given layer at the center point with width and height"""
        if width==0:
            width=drc["minwidth_{}".format(layer)]
        if height==0:
            height=drc["minwidth_{}".format(layer)]
        # negative layers indicate "unused" layers in a given technology
        layer_num = techlayer[layer]
        corrected_offset = offset - vector(0.5*width,0.5*height)
        if layer_num >= 0:
            self.objs.append(geometry.rectangle(layer_num, corrected_offset, width, height))
            return self.objs[-1]
        return None


    def add_segment_center(self, layer, start, end):
        """ Add a min-width rectanglular segment using center line on the start to end point """
        minwidth_layer = drc["minwidth_{}".format(layer)]        
        if start.x!=end.x and start.y!=end.y:
            debug.error("Nonrectilinear center rect!",-1)
        elif start.x!=end.x:
            offset = vector(0,0.5*minwidth_layer)
            return self.add_rect(layer,start-offset,end.x-start.x,minwidth_layer)
        else:
            offset = vector(0.5*minwidth_layer,0)
            return self.add_rect(layer,start-offset,minwidth_layer,end.y-start.y)


    
    def get_pin(self, text):
        """ Return the pin or list of pins """
        try:
            if len(self.pin_map[text])>1:
                debug.warning("Should use a pin iterator since more than one pin {}".format(text))
            # If we have one pin, return it and not the list.
            # Otherwise, should use get_pins()
            return self.pin_map[text][0]
        except Exception as e:
            #print e
            self.gds_write("missing_pin.gds")
            debug.error("No pin found with name {0} on {1}. Saved as missing_pin.gds.".format(text,self.name),-1)
            
            

    def get_pins(self, text):
        """ Return a pin list (instead of a single pin) """
        return self.pin_map[text]
    
    def copy_layout_pin(self, instance, pin_name, new_name=""):
        """ 
        Create a copied version of the layout pin at the current level.
        You can optionally rename the pin to a new name. 
        """
        pins=instance.get_pins(pin_name)
        for pin in pins:
            if new_name=="":
                new_name = pin.name
            self.add_layout_pin(new_name, pin.layer, pin.ll(), pin.width(), pin.height())

    def add_layout_pin_center_segment(self, text, layer, start, end):
        """ Creates a path like pin with center-line convention """

        debug.check(start.x==end.x or start.y==end.y,"Cannot have a non-manhatten layout pin.")
        
        minwidth_layer = drc["minwidth_{}".format(layer)]
        
        # one of these will be zero
        width = max(start.x,end.x) - min(start.x,end.x)
        height = max(start.y,end.y) - min(start.y,end.y)
        ll_offset = vector(min(start.x,end.x),min(start.y,end.y))

        # Shift it down 1/2 a width in the 0 dimension
        if height==0:
            ll_offset -= vector(0,0.5*minwidth_layer)
        if width==0:
            ll_offset -= vector(0.5*minwidth_layer,0)
        # This makes sure it is long enough, but also it is not 0 width!
        height = max(minwidth_layer,height)
        width = max(minwidth_layer,width)
        
        
        return self.add_layout_pin(text, layer, ll_offset, width, height)

    def add_layout_pin_center_rect(self, text, layer, offset, width=None, height=None):
        """ Creates a path like pin with center-line convention """
        if width==None:
            width=drc["minwidth_{0}".format(layer)]
        if height==None:
            height=drc["minwidth_{0}".format(layer)]

        ll_offset = offset - vector(0.5*width,0.5*height)

        return self.add_layout_pin(text, layer, ll_offset, width, height)

    
    def remove_layout_pin(self, text):
        """Delete a labeled pin (or all pins of the same name)"""
        self.pin_map[text]=[]
        
    def add_layout_pin(self, text, layer, offset, width=None, height=None):
        """Create a labeled pin """
        if width==None:
            width=drc["minwidth_{0}".format(layer)]
        if height==None:
            height=drc["minwidth_{0}".format(layer)]
        
        new_pin = pin_layout(text, [offset,offset+vector(width,height)], layer)

        try:
            # Check if there's a duplicate!
            # and if so, silently ignore it.
            # Rounding errors may result in some duplicates.
            pin_list = self.pin_map[text]
            for pin in pin_list:
                if pin == new_pin:
                    return pin
            self.pin_map[text].append(new_pin)
        except KeyError:
            self.pin_map[text] = [new_pin]

        return new_pin

    def add_label_pin(self, text, layer, offset, width=None, height=None):
        """Create a labeled pin WITHOUT the pin data structure. This is not an
        actual pin but a named net so that we can add a correspondence point
        in LVS.
        """
        if width==None:
            width=drc["minwidth_{0}".format(layer)]
        if height==None:
            height=drc["minwidth_{0}".format(layer)]
        self.add_rect(layer=layer,
                      offset=offset,
                      width=width,
                      height=height)
        self.add_label(text=text,
                       layer=layer,
                       offset=offset)
            

    def add_label(self, text, layer, offset=[0,0],zoom=-1):
        """Adds a text label on the given layer,offset, and zoom level"""
        # negative layers indicate "unused" layers in a given technology
        debug.info(5,"add label " + str(text) + " " + layer + " " + str(offset))
        layer_num = techlayer[layer]
        if layer_num >= 0:
            self.objs.append(geometry.label(text, layer_num, offset, zoom))
            return self.objs[-1]
        return None


    def add_path(self, layer, coordinates, width=None):
        """Connects a routing path on given layer,coordinates,width."""
        debug.info(4,"add path " + str(layer) + " " + str(coordinates))
        import path
        # NOTE: (UNTESTED) add_path(...) is currently not used
        # negative layers indicate "unused" layers in a given technology
        #layer_num = techlayer[layer]
        #if layer_num >= 0:
        #    self.objs.append(geometry.path(layer_num, coordinates, width))

        path.path(obj=self,
                  layer=layer, 
                  position_list=coordinates, 
                  width=width)

    def add_route(self, design, layers, coordinates):
        """Connects a routing path on given layer,coordinates,width. The
        layers are the (horizontal, via, vertical). add_wire assumes
        preferred direction routing whereas this includes layers in
        the coordinates.
        """
        import route
        debug.info(4,"add route " + str(layers) + " " + str(coordinates))
        # add an instance of our path that breaks down into rectangles and contacts
        route.route(obj=self,
                    layer_stack=layers, 
                    path=coordinates)

    
    def add_wire(self, layers, coordinates):
        """Connects a routing path on given layer,coordinates,width.
        The layers are the (horizontal, via, vertical). """
        import wire
        # add an instance of our path that breaks down into rectangles and contacts
        wire.wire(obj=self,
                  layer_stack=layers, 
                  position_list=coordinates)

    def add_contact(self, layers, offset, size=[1,1], mirror="R0", rotate=0, implant_type=None, well_type=None):
        """ This is just an alias for a via."""
        return self.add_via(layers=layers,
                            offset=offset,
                            size=size,
                            mirror=mirror,
                            rotate=rotate,
                            implant_type=implant_type,
                            well_type=well_type)

    def add_contact_center(self, layers, offset, size=[1,1], mirror="R0", rotate=0, implant_type=None, well_type=None):
        """ This is just an alias for a via."""
        return self.add_via_center(layers=layers,
                                   offset=offset,
                                   size=size,
                                   mirror=mirror,
                                   rotate=rotate,
                                   implant_type=implant_type,
                                   well_type=well_type)      
    
    def add_via(self, layers, offset, size=[1,1], mirror="R0", rotate=0, implant_type=None, well_type=None):
        """ Add a three layer via structure. """
        import contact
        via = contact.contact(layer_stack=layers,
                              dimensions=size,
                              implant_type=implant_type,
                              well_type=well_type)
        self.add_mod(via)
        inst=self.add_inst(name=via.name, 
                           mod=via, 
                           offset=offset,
                           mirror=mirror,
                           rotate=rotate)
        # We don't model the logical connectivity of wires/paths
        self.connect_inst([])
        return inst

    def add_via_center(self, layers, offset, size=[1,1], mirror="R0", rotate=0, implant_type=None, well_type=None):
        """ Add a three layer via structure by the center coordinate accounting for mirroring and rotation. """
        import contact
        via = contact.contact(layer_stack=layers,
                              dimensions=size,
                              implant_type=implant_type,
                              well_type=well_type)

        debug.check(mirror=="R0","Use rotate to rotate vias instead of mirror.")
        
        height = via.height
        width = via.width

        if rotate==0:
            corrected_offset = offset + vector(-0.5*width,-0.5*height)
        elif rotate==90:
            corrected_offset = offset + vector(0.5*height,-0.5*width)
        elif rotate==180:
            corrected_offset = offset + vector(-0.5*width,0.5*height)
        elif rotate==270:
            corrected_offset = offset + vector(-0.5*height,0.5*width)
        else:
            debug.error("Invalid rotation argument.",-1)
            

        self.add_mod(via)
        inst=self.add_inst(name=via.name, 
                           mod=via, 
                           offset=corrected_offset,
                           mirror=mirror,
                           rotate=rotate)
        # We don't model the logical connectivity of wires/paths
        self.connect_inst([])
        return inst
    
    def add_ptx(self, offset, mirror="R0", rotate=0, width=1, mults=1, tx_type="nmos"):
        """Adds a ptx module to the design."""
        import ptx
        mos = ptx.ptx(width=width,
                      mults=mults,
                      tx_type=tx_type)
        self.add_mod(mos)
        inst=self.add_inst(name=mos.name, 
                           mod=mos, 
                           offset=offset,
                           mirror=mirror,
                           rotate=rotate)
        return inst



    def gds_read(self):
        """Reads a GDSII file in the library and checks if it exists
           Otherwise, start a new layout for dynamic generation."""
        # open the gds file if it exists or else create a blank layout
        if os.path.isfile(self.gds_file):
            debug.info(3, "opening %s" % self.gds_file)
            self.is_library_cell=True
            self.gds = gdsMill.VlsiLayout(units=GDS["unit"])
            reader = gdsMill.Gds2reader(self.gds)
            reader.loadFromFile(self.gds_file)
        else:
            debug.info(4, "creating structure %s" % self.name)
            self.gds = gdsMill.VlsiLayout(name=self.name, units=GDS["unit"])

    def print_gds(self, gds_file=None):
        """Print the gds file (not the vlsi class) to the terminal """
        if gds_file == None:
            gds_file = self.gds_file
        debug.info(4, "Printing %s" % gds_file)
        arrayCellLayout = gdsMill.VlsiLayout(units=GDS["unit"])
        reader = gdsMill.Gds2reader(arrayCellLayout, debugToTerminal=1)
        reader.loadFromFile(gds_file)

    def clear_visited(self):
        """ Recursively clear the visited flag """
        if not self.visited:
            for i in self.insts:
                i.mod.clear_visited()
        self.visited = False

    def gds_write_file(self, newLayout):
        """Recursive GDS write function"""
        # Visited means that we already prepared self.gds for this subtree
        if self.visited:
            return
        for i in self.insts:
            i.gds_write_file(newLayout)
        for i in self.objs:
            i.gds_write_file(newLayout)
        for pin_name in self.pin_map.keys():
            for pin in self.pin_map[pin_name]:
                pin.gds_write_file(newLayout)
        self.visited = True

    def gds_write(self, gds_name):
        """Write the entire gds of the object to the file."""
        debug.info(3, "Writing to {0}".format(gds_name))

        writer = gdsMill.Gds2writer(self.gds)
        # MRG: 3/2/18 We don't want to clear the visited flag since
        # this would result in duplicates of all instances being placed in self.gds
        # which may have been previously processed!
        #self.clear_visited()
        # recursively create all the remaining objects
        self.gds_write_file(self.gds)
        # populates the xyTree data structure for gds
        # self.gds.prepareForWrite()
        writer.writeToFile(gds_name)

    def get_boundary(self):
        """ Return the lower-left and upper-right coordinates of boundary """
        # This assumes nothing spans outside of the width and height!
        return [vector(0,0), vector(self.width, self.height)]
        #return [self.find_lowest_coords(), self.find_highest_coords()]

    def get_blockages(self, layer, top_level=False):
        """ 
        Write all of the obstacles in the current (and children) modules to the lef file 
        Do not write the pins since they aren't obstructions.
        """
        if type(layer)==str:
            layer_num = techlayer[layer]
        else:
            layer_num = layer
            
        blockages = []
        for i in self.objs:
            blockages += i.get_blockages(layer_num)
        for i in self.insts:
            blockages += i.get_blockages(layer_num)
        # Must add pin blockages to non-top cells
        if not top_level:
            blockages += self.get_pin_blockages(layer_num)
        return blockages

    def get_pin_blockages(self, layer_num):
        """ Return the pin shapes as blockages for non-top-level blocks. """
        # FIXME: We don't have a body contact in ptx, so just ignore it for now
        import copy
        pin_names = copy.deepcopy(self.pins)
        if self.name.startswith("pmos") or self.name.startswith("nmos"):
            pin_names.remove("B")
            
        blockages = []
        for pin_name in pin_names:
            pin_list = self.get_pins(pin_name)
            for pin in pin_list:
                if pin.layer_num==layer_num:
                    blockages += [pin.rect]

        return blockages

    def add_enclosure(self, insts, layer="nwell"):
        """ Add a layer that surrounds the given instances. Useful
        for creating wells, for example. Doesn't check for minimum widths or
        spacings."""

        xmin=insts[0].lx()
        ymin=insts[0].by()
        xmax=insts[0].rx()
        ymax=insts[0].uy()
        for inst in insts:
            xmin = min(xmin, inst.lx())
            ymin = min(ymin, inst.by())
            xmax = max(xmax, inst.rx())
            ymax = max(ymax, inst.uy())

        self.add_rect(layer=layer,
                      offset=vector(xmin,ymin),
                      width=xmax-xmin,
                      height=ymax-ymin)

    def pdf_write(self, pdf_name):
        # NOTE: Currently does not work (Needs further research)
        #self.pdf_name = self.name + ".pdf"
        debug.info(0, "Writing to %s" % pdf_name)
        pdf = gdsMill.pdfLayout(self.gds)

        return
        pdf.layerColors[self.gds.layerNumbersInUse[0]] = "#219E1C"
        pdf.layerColors[self.gds.layerNumbersInUse[1]] = "#271C9E"
        pdf.layerColors[self.gds.layerNumbersInUse[2]] = "#CC54C8"
        pdf.layerColors[self.gds.layerNumbersInUse[3]] = "#E9C514"
        pdf.layerColors[self.gds.layerNumbersInUse[4]] = "#856F00"
        pdf.layerColors[self.gds.layerNumbersInUse[5]] = "#BD1444"
        pdf.layerColors[self.gds.layerNumbersInUse[6]] = "#FD1444"
        pdf.layerColors[self.gds.layerNumbersInUse[7]] = "#FD1414"

        pdf.setScale(500)
        pdf.drawLayout()
        pdf.writeToFile(pdf_name)

    def print_attr(self):
        """Prints a list of attributes for the current layout object"""
        debug.info(0, 
                   "|==============================================================================|")
        debug.info(0, 
                   "|=========      LIST OF OBJECTS (Rects) FOR: " + self.name)
        debug.info(0, 
                   "|==============================================================================|")
        for obj in self.objs:
            debug.info(0, "layer={0} : offset={1} : size={2}".format(obj.layerNumber,
                                                                     obj.offset,
                                                                     obj.size))

        debug.info(0, 
                   "|==============================================================================|")
        debug.info(0, 
                   "|=========      LIST OF INSTANCES FOR: " + self.name)
        debug.info(0, 
                   "|==============================================================================|")
        for inst in self.insts:
            debug.info(0, "name={0} : mod={1} : offset={2}".format(inst.name,
                                                                   inst.mod.name,
                                                                   inst.offset))

