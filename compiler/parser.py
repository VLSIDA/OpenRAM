#!/usr/bin/env python3
"""
Datasheet Generator

TODO:
locate all port elements in .lib
Locate all timing elements in .lib
Diagram generation
Improve css
"""

import os, math
import optparse
from flask_table import *
import csv
import contextlib
from globals import OPTS

class deliverables(Table):
	typ = Col('Type')
	description = Col('Description')
	link = Col('Link')
	


class deliverables_item(object):
	def __init__(self, typ, description,link):
		self.typ = typ
		self.description = description
		self.link = link

class operating_conditions(Table):
	parameter = Col('Parameter')
	min = Col('Min')
	typ = Col('Typ')
	max = Col('Max')
	units = Col('Units')

class operating_conditions_item(object):
	def __init__(self, parameter, min, typ, max, units):
		self.parameter = parameter
		self.min = min
		self.typ = typ
		self.max = max
		self.units = units

class timing_and_current_data(Table):
	parameter = Col('Parameter')
	min = Col('Min')
	max = Col('Max')
	units = Col('Units')

class timing_and_current_data_item(object):
	def __init__(self, parameter, min, max, units):
		self.parameter = parameter
		self.min = min
		self.max = max
		self.units = units

class characterization_corners(Table):
	corner_name = Col('Corner Name')
	process = Col('Process')
	power_supply = Col('Power Supply')
	temperature = Col('Temperature')
	library_name_suffix = Col('Library Name Suffix')

class characterization_corners_item(object):
	def __init__(self, corner_name, process, power_supply, temperature, library_name_suffix):
		self.corner_name = corner_name
		self.process = process
		self.power_supply = power_supply
		self.temperature = temperature
		self.library_name_suffix = library_name_suffix
		
def process_name(corner):
    if corner == "TT":
        return "Typical - Typical"
    if corner == "SS":
        return "Slow - Slow"
    if corner == "FF":
        return "Fast - Fast"
    else:
        return "custom"
           
def parse_file(f,pages):
    with open(f) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:                                            
            found = 0
            NAME = row[0]
            NUM_WORDS = row[1]
            NUM_BANKS = row[2]
            NUM_RW_PORTS = row[3]
            NUM_W_PORTS = row[4]
            NUM_R_PORTS = row[5]
            TECH_NAME = row[6]
            TEMP = row[7]
            VOLT = row[8]
            PROC = row[9]
            MIN_PERIOD = row[10]
            OUT_DIR = row[11]
            LIB_NAME = row[12]
            for sheet in pages:
                
                
                if sheet.name == row[0]:
                    found = 1
                    #if the .lib information is for an existing datasheet compare timing data
                    
                    for item in sheet.operating:
                    
                        if item.parameter == 'Operating Temperature':
                            if float(TEMP) > float(item.max):
                                item.typ = item.max
                                item.max = TEMP
                            if float(TEMP) < float(item.min):
                                item.typ = item.min
                                item.min = TEMP
                                
                        if item.parameter == 'Power supply (VDD) range':
                            if float(VOLT) > float(item.max):
                                item.typ = item.max
                                item.max = VOLT
                            if float(VOLT) < float(item.min):
                                item.typ = item.min
                                item.min = VOLT
                                
                        if item.parameter == 'Operating Frequncy (F)':
                            if float(math.floor(1000/float(MIN_PERIOD)) < float(item.max)):
                                item.max = str(math.floor(1000/float(MIN_PERIOD)))
                        
                        
                        
                    new_sheet.corners.append(characterization_corners_item(PROC,process_name(PROC),VOLT,TEMP,LIB_NAME.replace(OUT_DIR,'').replace(NAME,'')))
                    new_sheet.dlv.append(deliverables_item('.lib','Synthesis models','<a href="file://{0}">{1}</a>'.format(LIB_NAME,LIB_NAME.replace(OUT_DIR,''))))
                    
            if found == 0: 
                new_sheet = datasheet(NAME)
                pages.append(new_sheet)
                
                new_sheet.corners.append(characterization_corners_item(PROC,process_name(PROC),VOLT,TEMP,LIB_NAME.replace(OUT_DIR,'').replace(NAME,'')))
                
                new_sheet.operating.append(operating_conditions_item('Power supply (VDD) range',VOLT,VOLT,VOLT,'Volts'))
                new_sheet.operating.append(operating_conditions_item('Operating Temperature',TEMP,TEMP,TEMP,'Celsius'))
                new_sheet.operating.append(operating_conditions_item('Operating Frequency (F)','','',str(math.floor(1000/float(MIN_PERIOD))),'MHz'))
                
                new_sheet.timing.append(timing_and_current_data_item('1','2','3','4'))
                
                new_sheet.dlv.append(deliverables_item('.sp','SPICE netlists','<a href="file://{0}{1}.{2}">{1}.{2}</a>'.format(OUT_DIR,NAME,'sp')))
                new_sheet.dlv.append(deliverables_item('.v','Verilog simulation models','<a href="file://{0}{1}.{2}">{1}.{2}</a>'.format(OUT_DIR,NAME,'v')))
                new_sheet.dlv.append(deliverables_item('.gds','GDSII layout views','<a href="file://{0}{1}.{2}">{1}.{2}</a>'.format(OUT_DIR,NAME,'gds')))
                new_sheet.dlv.append(deliverables_item('.lef','LEF files','<a href="file://{0}{1}.{2}">{1}.{2}</a>'.format(OUT_DIR,NAME,'lef')))
                new_sheet.dlv.append(deliverables_item('.lib','Synthesis models','<a href="file://{0}">{1}</a>'.format(LIB_NAME,LIB_NAME.replace(OUT_DIR,''))))
                
                
           
class datasheet():

    def __init__(self,identifier):
        self.corners = []
        self.timing = []
        self.operating = []
        self.dlv = []
        self.name = identifier
        
    def print(self):
        print("""<style>
#data {
    font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
    border-collapse: collapse;
    width: 100%;
    max-width: 800px
}

#data td, #data th {
    border: 1px solid #ddd;
    padding: 8px;
}

#data tr:nth-child(even){background-color: #f2f2f2;}

#data tr:hover {background-color: #ddd;}

#data th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #4CAF50;
    color: white;
}
</style>""")
        print('<p style=font-size: 20px;font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;>{0}</p>')
        print('<p style=font-size: 20px;font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;>{0}</p>')
        print('<p style=font-size: 20px;font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;>{0}</p>')
        print('<p style=font-size: 20px;font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;>Operating Conditions</p>')
        print(operating_conditions(self.operating,table_id='data').__html__())
        print('<p style=font-size: 20px;font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;>Timing and Current Data</p>')
        print(timing_and_current_data(self.timing,table_id='data').__html__())
        print('<p style=font-size: 20px;font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;>Characterization Corners</p>')  
        print(characterization_corners(self.corners,table_id='data').__html__())
        print('<p style=font-size: 20px;font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;>Deliverables</p>') 
        print(deliverables(self.dlv,table_id='data').__html__().replace('&lt;','<').replace('&#34;','"').replace('&gt;',">"))
        
        
class parse():
    def __init__(self,in_dir,out_dir):
    
        if not (os.path.isdir(in_dir)):
	        os.mkdir(in_dir)
	        
        if not (os.path.isdir(out_dir)):
            os.mkdir(out_dir)
	    
        datasheets = []
        parse_file(in_dir + "/datasheet.info", datasheets)
        
        
        for sheets in datasheets:
            print (out_dir + sheets.name + ".html")
            with open(out_dir + "/" + sheets.name + ".html", 'w+') as f:
                with contextlib.redirect_stdout(f):
                    sheets.print()
               
        
        
        
        
        
        
        
        
        
        
        
        
