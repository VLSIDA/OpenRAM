"""
This class should be called in the ptx function to draw addtional layer as some layer may not exist in the cmrf7sf technology
"""
import globals
import design
import tech



class ptx_port:
    def __init__(self,name):
	self.name=name
	self.width=0
	self.height=0



    def draw(self,instance_to_draw,offset,tx_type,height,width,tx=1):
	self.height=height
	self.width=width
	self.offset=offset
	if tx_type == "pmos":
		# draw BP layer
		if tx==1:
			instance_to_draw.add_rect(tech.layer["BP"],[offset[0]-tech.drc["BP_enclosure_active"],offset[1]-tech.drc["BP_enclosure_gate"]],width+2*tech.drc["BP_enclosure_active"],height+2*tech.drc["BP_enclosure_gate"])	
		else:
			instance_to_draw.add_rect(tech.layer["BP"],[offset[0]-tech.drc["BP_enclosure_active"],offset[1]-tech.drc["BP_enclosure_active"]],width+2*tech.drc["BP_enclosure_active"],height+2*tech.drc["BP_enclosure_active"])	


