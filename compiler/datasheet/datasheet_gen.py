#!/usr/bin/env python3
"""
This is a script to load data from the characterization and layout processes into 
a web friendly html datasheet. This script requres the python-flask and flask-table
packages to be installed.
"""
#TODO:
#locate all port elements in .lib
#Locate all timing elements in .lib
#Diagram generation
#Improve css

import debug
from globals import OPTS

if OPTS.datasheet_gen:
    import flask_table
    import os, math
    import optparse
    import csv
    from deliverables import *
    from operating_conditions import *
    from timing_and_current_data import *
    from characterization_corners import *
    from datasheet import *
    from in_out import *
else:
    debug.warning("Python library flask_table not found. Skipping html datasheet generation. This can be installed with pip install flask-table.")
    #make sure appropriate python libraries are installed


def process_name(corner):
    """
    Expands the names of the characterization corner types into something human friendly
    """
    if corner == "TT":
        return "Typical - Typical"
    if corner == "SS":
        return "Slow - Slow"
    if corner == "FF":
        return "Fast - Fast"
    else:
        return "custom"

def parse_characterizer_csv(sram,f,pages):
    """
    Parses output data of the Liberty file generator in order to construct the timing and
    current table
    """
    with open(f) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            found = 0

            #defines layout of csv file
            NAME = row[0]
            NUM_WORDS = row[1]
            NUM_BANKS = row[2]
            NUM_RW_PORTS = row[3]
            NUM_W_PORTS = row[4]
            NUM_R_PORTS = row[5]
            TECH_NAME = row[6]
            TEMP = row[8]
            VOLT = row[7]
            PROC = row[9]
            MIN_PERIOD = row[10]
            OUT_DIR = row[11]
            LIB_NAME = row[12]
            WORD_SIZE = row[13]

            FF_SETUP_LH_MIN = row[14]
            FF_SETUP_LH_MAX = row[15]

            FF_SETUP_HL_MIN = row[16]
            FF_SETUP_HL_MAX = row[17]

            FF_HOLD_LH_MIN = row[18]
            FF_HOLD_LH_MAX = row[19]

            FF_HOLD_HL_MIN = row[20]
            FF_HOLD_HL_MAX = row[21]
            
    
            for sheet in pages:


                if sheet.name == row[0]:

                    found = 1
                    #if the .lib information is for an existing datasheet compare timing data

                    for item in sheet.operating:
                        #check if the new corner dataa is worse than the previous worse corner data

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
                            try:
                                if float(math.floor(1000/float(MIN_PERIOD)) < float(item.max)):
                                    item.max = str(math.floor(1000/float(MIN_PERIOD)))
                            except Exception:
                                #pass if MIN_PERIOD is zero (not supported by analyitcal model)
                                pass

                    for item in sheet.timing:
                        if item.parameter == "CSb setup rising":
                            if float(FF_SETUP_LH_MIN) < float(item.min):
                                item.min = FF_SETUP_LH_MIN
                            elif float(FF_SETUP_LH_MAX) > float(item.max):
                                item.max = FF_SETUP_LH_MAX

                        if item.parameter == "CSb setup falling":
                            if float(FF_SETUP_HL_MIN) < float(item.min):
                                item.min = FF_SETUP_HL_MIN
                            elif float(FF_SETUP_HL_MAX) > float(item.max):
                                item.max = FF_SETUP_HL_MAX

                        if item.parameter == "CSb hold rising":
                            if float(FF_HOLD_HL_MIN) < float(item.min):
                                item.min = FF_SETUP_HL_MIN
                            elif float(FF_HOLD_HL_MAX) > float(item.max):
                                item.max = FF_SETUP_HL_MAX

                        if item.parameter == "CSb hold falling":
                            if float(FF_HOLD_HL_MIN) < float(item.min):
                                item.min = FF_SETUP_HL_MIN
                            elif float(FF_HOLD_HL_MAX) > float(item.max):
                                item.max = FF_SETUP_HL_MAX
                            

                    #regardless of if there is already a corner for the current sram, append the new corner to the datasheet
                    new_sheet.corners.append(characterization_corners_item(PROC,process_name(PROC),VOLT,TEMP,LIB_NAME.replace(OUT_DIR,'').replace(NAME,'')))
                    new_sheet.dlv.append(deliverables_item('.lib','Synthesis models','<a href="file://{0}">{1}</a>'.format(LIB_NAME,LIB_NAME.replace(OUT_DIR,''))))

            if found == 0:
                
                #if this is the first corner for this sram, run first time configuration and set up tables
                new_sheet = datasheet(NAME)
                pages.append(new_sheet)

                new_sheet.corners.append(characterization_corners_item(PROC,process_name(PROC),VOLT,TEMP,LIB_NAME.replace(OUT_DIR,'').replace(NAME,'')))

                new_sheet.operating.append(operating_conditions_item('Power supply (VDD) range',VOLT,VOLT,VOLT,'Volts'))
                new_sheet.operating.append(operating_conditions_item('Operating Temperature',TEMP,TEMP,TEMP,'Celsius'))
                try:
                    new_sheet.operating.append(operating_conditions_item('Operating Frequency (F)*','','',str(math.floor(1000/float(MIN_PERIOD))),'MHz'))
                except Exception:
                    new_sheet.operating.append(operating_conditions_item('Operating Frequency (F)*','','',"unknown",'MHz')) #analytical model fails to provide MIN_PERIOD
                
                #place holder timing and current data
                new_sheet.timing.append(timing_and_current_data_item('Cycle time','2','3','4'))
                new_sheet.timing.append(timing_and_current_data_item('Access time','2','3','4'))
                new_sheet.timing.append(timing_and_current_data_item('Positive clk setup','2','3','4'))
                new_sheet.timing.append(timing_and_current_data_item('Positive clk hold','2','3','4'))
                new_sheet.timing.append(timing_and_current_data_item('CSb setup rising',FF_SETUP_LH_MIN,FF_SETUP_LH_MAX,'ns'))
                new_sheet.timing.append(timing_and_current_data_item('CSb setup falling',FF_SETUP_HL_MIN,FF_SETUP_HL_MAX,'ns'))
                new_sheet.timing.append(timing_and_current_data_item('CSb hold rising',FF_HOLD_LH_MIN,FF_HOLD_LH_MAX,'ns'))
                new_sheet.timing.append(timing_and_current_data_item('CSb hold falling',FF_HOLD_HL_MIN,FF_HOLD_HL_MAX,'ns'))
                new_sheet.timing.append(timing_and_current_data_item('AC current','2','3','4'))
                new_sheet.timing.append(timing_and_current_data_item('Standby current','2','3','4'))
                
                if not OPTS.netlist_only:
                    #physical layout files should not be generated in netlist only mode
                    new_sheet.dlv.append(deliverables_item('.gds','GDSII layout views','<a href="file://{0}{1}.{2}">{1}.{2}</a>'.format(OUT_DIR,OPTS.output_name,'gds')))
                    new_sheet.dlv.append(deliverables_item('.lef','LEF files','<a href="file://{0}{1}.{2}">{1}.{2}</a>'.format(OUT_DIR,OPTS.output_name,'lef')))
   

                new_sheet.dlv.append(deliverables_item('.sp','SPICE netlists','<a href="file://{0}{1}.{2}">{1}.{2}</a>'.format(OUT_DIR,OPTS.output_name,'sp')))
                new_sheet.dlv.append(deliverables_item('.v','Verilog simulation models','<a href="file://{0}{1}.{2}">{1}.{2}</a>'.format(OUT_DIR,OPTS.output_name,'v')))
                new_sheet.dlv.append(deliverables_item('.html','This datasheet','<a href="file://{0}{1}.{2}">{1}.{2}</a>'.format(OUT_DIR,OPTS.output_name,'html')))
                new_sheet.dlv.append(deliverables_item('.lib','Synthesis models','<a href="file://{0}">{1}</a>'.format(LIB_NAME,LIB_NAME.replace(OUT_DIR,'lib'))))
                new_sheet.dlv.append(deliverables_item('.py','OpenRAM configuration file','<a href="file://{0}{1}.{2}">{1}.{2}</a>'.format(OUT_DIR,OPTS.output_name,'py')))



                #debug table for multiport information
                new_sheet.io.append(in_out_item('WORD_SIZE',WORD_SIZE))
                new_sheet.io.append(in_out_item('NUM_WORDS',NUM_WORDS))
                new_sheet.io.append(in_out_item('NUM_BANKS',NUM_BANKS))
                new_sheet.io.append(in_out_item('NUM_RW_PORTS',NUM_RW_PORTS))
                new_sheet.io.append(in_out_item('NUM_R_PORTS',NUM_R_PORTS))
                new_sheet.io.append(in_out_item('NUM_W_PORTS',NUM_W_PORTS))
                new_sheet.io.append(in_out_item('Area',sram.width * sram.height))
                





class datasheet_gen():
     def datasheet_write(sram,name):
        
        if OPTS.datasheet_gen:
            in_dir = OPTS.openram_temp
        
            if not (os.path.isdir(in_dir)):
                os.mkdir(in_dir)


            datasheets = []
            parse_characterizer_csv(sram, in_dir + "/datasheet.info", datasheets)


            for sheets in datasheets:
                with open(name, 'w+') as f:
                    sheets.generate_html()
                    f.write(sheets.html)
