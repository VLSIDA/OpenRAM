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
            col = 0

            #defines layout of csv file
            NAME = row[col]
            col += 1

            NUM_WORDS = row[col]
            col += 1

            NUM_BANKS = row[col]
            col += 1

            NUM_RW_PORTS = row[col]
            col += 1

            NUM_W_PORTS = row[col]
            col += 1

            NUM_R_PORTS = row[col]
            col += 1

            TECH_NAME = row[col]
            col += 1

            TEMP = row[col]
            col += 1

            VOLT = row[col]
            col += 1

            PROC = row[col]
            col += 1

            MIN_PERIOD = row[col]
            col += 1

            OUT_DIR = row[col]
            col += 1

            LIB_NAME = row[col]
            col += 1

            WORD_SIZE = row[col]
            col += 1

            FF_SETUP_LH_MIN = "1"
            FF_SETUP_LH_MAX = "2"

            FF_SETUP_HL_MIN = "3"
            FF_SETUP_HL_MAX = "4"

            FF_HOLD_LH_MIN = "5"
            FF_HOLD_LH_MAX = "6"

            FF_HOLD_HL_MIN = "7"
            FF_HOLD_HL_MAX = "8"
           
    
            for sheet in pages:


                if sheet.name == NAME:

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



                    while(True):
                        if(row[col].startswith('DIN')):
                            start = col
                            for item in sheet.timing:
                                if item.parameter.startswith(row[col]):

                                    if item.parameter.endswith('setup rising'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                                    elif item.parameter.endswith('setup falling'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                                    elif item.parameter.endswith('hold rising'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                                    elif item.parameter.endswith('hold falling'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                            col += 1

                        elif(row[col].startswith('DOUT')):
                            start = col
                            for item in sheet.timing:
                                if item.parameter.startswith(row[col]):

                                    if item.parameter.endswith('cell rise'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                                    elif item.parameter.endswith('cell fall'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                                    elif item.parameter.endswith('rise transition'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                                    elif item.parameter.endswith('fall transition'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                            col += 1

                        elif(row[col].startswith('CSb')):
                            start = col
                            for item in sheet.timing:
                                if item.parameter.startswith(row[col]):

                                    if item.parameter.endswith('setup rising'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                                    elif item.parameter.endswith('setup falling'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                                    elif item.parameter.endswith('hold rising'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                                    elif item.parameter.endswith('hold falling'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                            col += 1


                        elif(row[col].startswith('WEb')):
                            start = col
                            for item in sheet.timing:
                                if item.parameter.startswith(row[col]):

                                    if item.parameter.endswith('setup rising'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                                    elif item.parameter.endswith('setup falling'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                                    elif item.parameter.endswith('hold rising'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                                    elif item.parameter.endswith('hold falling'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                            col += 1


                        elif(row[col].startswith('ADDR')):
                            start = col
                            for item in sheet.timing:
                                if item.parameter.startswith(row[col]):

                                    if item.parameter.endswith('setup rising'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                                    elif item.parameter.endswith('setup falling'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                                    elif item.parameter.endswith('hold rising'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                                    elif item.parameter.endswith('hold falling'):
                                        if float(row[col+1]) < float(item.min):
                                            item.min = row[col+1]
                                        if float(row[col+2]) > float(item.max):
                                            item.max = row[col+2]

                                        col += 2

                            col += 1
                        else:
                            break


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

                while(True):
                    if(row[col].startswith('DIN')):
                        start = col
                        new_sheet.timing.append(timing_and_current_data_item('{0} setup rising'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2

                        new_sheet.timing.append(timing_and_current_data_item('{0} setup falling'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2
                    
                        new_sheet.timing.append(timing_and_current_data_item('{0} hold rising'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2

                        new_sheet.timing.append(timing_and_current_data_item('{0} hold falling'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2

                        col +=1
                        
                    elif(row[col].startswith('DOUT')):
                        start = col
                        new_sheet.timing.append(timing_and_current_data_item('{0} cell rise'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2

                        new_sheet.timing.append(timing_and_current_data_item('{0} cell fall'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2
                    
                        new_sheet.timing.append(timing_and_current_data_item('{0} rise transition'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2

                        new_sheet.timing.append(timing_and_current_data_item('{0} fall transition'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2

                        col +=1

                    elif(row[col].startswith('CSb')):
                        start = col
                        new_sheet.timing.append(timing_and_current_data_item('{0} setup rising'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2

                        new_sheet.timing.append(timing_and_current_data_item('{0} setup falling'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2
                    
                        new_sheet.timing.append(timing_and_current_data_item('{0} hold rising'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2

                        new_sheet.timing.append(timing_and_current_data_item('{0} hold falling'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2

                        col +=1

                    elif(row[col].startswith('WEb')):
                        start = col
                        new_sheet.timing.append(timing_and_current_data_item('{0} setup rising'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2

                        new_sheet.timing.append(timing_and_current_data_item('{0} setup falling'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2
                    
                        new_sheet.timing.append(timing_and_current_data_item('{0} hold rising'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2

                        new_sheet.timing.append(timing_and_current_data_item('{0} hold falling'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2

                        col +=1

                    elif(row[col].startswith('ADDR')):
                        start = col
                        new_sheet.timing.append(timing_and_current_data_item('{0} setup rising'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2

                        new_sheet.timing.append(timing_and_current_data_item('{0} setup falling'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2
                    
                        new_sheet.timing.append(timing_and_current_data_item('{0} hold rising'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2

                        new_sheet.timing.append(timing_and_current_data_item('{0} hold falling'.format(row[start]),row[col+1],row[col+2],'ns'))
                        col += 2

                        col +=1
                    else:
                        break


                    
                new_sheet.timing.append(timing_and_current_data_item('AC current','2','3','4'))
                new_sheet.timing.append(timing_and_current_data_item('Standby current','2','3','4'))
                
                if not OPTS.netlist_only:
                    #physical layout files should not be generated in netlist only mode
                    new_sheet.dlv.append(deliverables_item('.gds','GDSII layout views','<a href="file://{0}{1}.{2}">{1}.{2}</a>'.format(OUT_DIR,OPTS.output_name,'gds')))
                    new_sheet.dlv.append(deliverables_item('.lef','LEF files','<a href="file://{0}{1}.{2}">{1}.{2}</a>'.format(OUT_DIR,OPTS.output_name,'lef')))
   

                new_sheet.dlv.append(deliverables_item('.sp','SPICE netlists','<a href="{0}.{1}">{0}.{1}</a>'.format(OPTS.output_name,'sp')))
                new_sheet.dlv.append(deliverables_item('.v','Verilog simulation models','<a href="{0}.{1}">{0}.{1}</a>'.format(OPTS.output_name,'v')))
                new_sheet.dlv.append(deliverables_item('.html','This datasheet','<a href="{0}.{1}">{0}.{1}</a>'.format(OPTS.output_name,'html')))
                new_sheet.dlv.append(deliverables_item('.lib','Synthesis models','<a href="{1}">{1}</a>'.format(LIB_NAME,LIB_NAME.replace(OUT_DIR,''))))
                new_sheet.dlv.append(deliverables_item('.py','OpenRAM configuration file','<a href="{0}.{1}">{0}.{1}</a>'.format(OPTS.output_name,'py')))



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
