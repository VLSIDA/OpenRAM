# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
#!/usr/bin/env python3
"""
This is a script to load data from the characterization and layout processes into
a web friendly html datasheet.
"""
# TODO:
# Diagram generation
# Improve css


import os
import math
import csv
from openram import OPTS
from .datasheet import datasheet
from .table_gen import table_gen

# def process_name(corner):
# """
# Expands the names of the characterization corner types into something human friendly
# """
# if corner == "TS":
# return "Typical - Slow"
# if corner == "TT":
# return "Typical - Typical"
# if corner == "TF":
# return "Typical - Fast"
#
# if corner == "SS":
# return "Slow - Slow"
# if corner == "ST":
# return "Slow - Typical"
# if corner == "SF":
# return "Slow - Fast"
#
# if corner == "FS":
# return "Fast - Slow"
# if corner == "FT":
# return "Fast - Typical"
# if corner == "FF":
# return "Fast - Fast"
#
# else:
# return "custom"
#


def parse_characterizer_csv(f, pages):
    """
    Parses output data of the Liberty file generator in order to construct the timing and
    current table
    """
    with open(f) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:

            found = 0
            col = 0

            # defines layout of csv file
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

            ORIGIN_ID = row[col]
            col += 1

            DATETIME = row[col]
            col += 1

            ANALYTICAL_MODEL = row[col]
            col += 1

            DRC = row[col]
            col += 1

            LVS = row[col]
            col += 1

            AREA = row[col]
            col += 1

            for sheet in pages:

                if sheet.name == NAME:

                    found = 1
                    # if the .lib information is for an existing datasheet compare timing data

                    for item in sheet.operating_table.rows:
                        # check if the new corner data is worse than the previous worse corner data

                        if item[0] == 'Operating Temperature':
                            if float(TEMP) > float(item[3]):
                                item[2] = item[3]
                                item[3] = TEMP
                            if float(TEMP) < float(item[1]):
                                item[2] = item[1]
                                item[1] = TEMP

                        if item[0] == 'Power supply (VDD) range':
                            if float(VOLT) > float(item[3]):
                                item[2] = item[3]
                                item[3] = VOLT
                            if float(VOLT) < float(item[1]):
                                item[2] = item[1]
                                item[1] = VOLT

                        if item[0] == 'Operating Frequncy (F)':
                            try:
                                if float(math.floor(1000/float(MIN_PERIOD)) < float(item[3])):
                                    item[3] = str(math.floor(
                                        1000/float(MIN_PERIOD)))
                            except Exception:
                                pass
                    # check current .lib file produces the slowest timing results
                    while(True):
                        col_start = col
                        if(row[col].startswith('din')):
                            start = col
                            for item in sheet.timing_table.rows:
                                if item[0].startswith(row[col]):

                                    if item[0].endswith('setup rising'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                                    if item[0].endswith('setup falling'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                                    if item[0].endswith('hold rising'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                                    if item[0].endswith('hold falling'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                            col += 1

                        elif(row[col].startswith('dout')):
                            start = col
                            for item in sheet.timing_table.rows:
                                if item[0].startswith(row[col]):

                                    if item[0].endswith('cell rise'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                                    if item[0].endswith('cell fall'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                                    if item[0].endswith('rise transition'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                                    if item[0].endswith('fall transition'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                            col += 1

                        elif(row[col].startswith('csb')):
                            start = col
                            for item in sheet.timing_table.rows:
                                if item[0].startswith(row[col]):

                                    if item[0].endswith('setup rising'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                                    if item[0].endswith('setup falling'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                                    if item[0].endswith('hold rising'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                                    if item[0].endswith('hold falling'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                            col += 1

                        elif(row[col].startswith('web')):
                            start = col
                            for item in sheet.timing_table.rows:
                                if item[0].startswith(row[col]):

                                    if item[0].endswith('setup rising'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                                    if item[0].endswith('setup falling'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                                    if item[0].endswith('hold rising'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                                    if item[0].endswith('hold falling'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                            col += 1

                        elif(row[col].startswith('addr')):
                            start = col
                            for item in sheet.timing_table.rows:
                                if item[0].startswith(row[col]):

                                    if item[0].endswith('setup rising'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                                    if item[0].endswith('setup falling'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                                    if item[0].endswith('hold rising'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                                    if item[0].endswith('hold falling'):
                                        if float(row[col+1]) < float(item[1]):
                                            item[1] = row[col+1]
                                        if float(row[col+2]) > float(item[2]):
                                            item[2] = row[col+2]

                                    col += 2

                            col += 1

                        else:
                            for element in row[col_start: col - 1]:
                                sheet.description.append(str(element))
                            break

                    #check if new power is worse the previous
                    while(True):
                        col_start = col
                        if row[col] == 'power':
                            for item in sheet.power_table.rows:
                                if item[0].startswith(row[col+1]):
                                    if item[2].startswith('{0} Rising'.format(row[col+2])):
                                        if float(item[2]) < float(row[col+3]):
                                            item[2] = row[col+3]
                                    if item[2].startswith('{0} Falling'.format(row[col+2])):
                                        if float(item[2]) < float(row[col+3]):
                                            item[2] = row[col+3]
                            col += 4
                        else:
                            break
                    # check if new leakge is worse the previous
                    while(True):
                        col_start = col
                        if row[col] == 'leak':
                            for item in sheet.power_table.rows:
                                if item[0].startswith(row[col+1]):
                                    if float(item[2]) < float(row[col+2]):
                                            item[2] = row[col+2]
                            col += 3

                        else:
                            break
                    # add new corner information
                    new_sheet.corners_table.add_row(
                        [PROC, VOLT, TEMP, LIB_NAME.replace(OUT_DIR, '').replace(NAME, '')])
                    new_sheet.dlv_table.add_row(
                        ['.lib', 'Synthesis models', '<a href="file://{0}">{1}</a>'.format(LIB_NAME, LIB_NAME.replace(OUT_DIR, ''))])
                    new_sheet.dlv_table.add_row(
                        ['.db', 'Compiled .lib', '<a href="{1}">{1}</a>'.format(LIB_NAME[:-3] + 'db', LIB_NAME.replace(OUT_DIR, '')[:-3] + 'db')])


            if found == 0:

                # if this is the first corner for this sram, run first time configuration and set up tables
                new_sheet = datasheet(NAME)
                pages.append(new_sheet)

                new_sheet.git_id = ORIGIN_ID
                new_sheet.time = DATETIME
                new_sheet.DRC = DRC
                new_sheet.LVS = LVS
                new_sheet.ANALYTICAL_MODEL = ANALYTICAL_MODEL
                new_sheet.description = [NAME, NUM_WORDS, NUM_BANKS, NUM_RW_PORTS, NUM_W_PORTS,
                                         NUM_R_PORTS, TECH_NAME, MIN_PERIOD, WORD_SIZE, ORIGIN_ID, DATETIME]

                new_sheet.corners_table = table_gen("corners")
                new_sheet.corners_table.add_row(
                    ['Transistor Type', 'Power Supply', 'Temperature', 'Corner Name'])
                new_sheet.corners_table.add_row(
                    [PROC, VOLT, TEMP, LIB_NAME.replace(OUT_DIR, '').replace(NAME, '')])
                new_sheet.operating_table = table_gen(
                    "operating_table")
                new_sheet.operating_table.add_row(
                    ['Parameter', 'Min', 'Typ', 'Max', 'Units'])
                new_sheet.operating_table.add_row(
                    ['Power supply (VDD) range', VOLT, VOLT, VOLT, 'Volts'])
                new_sheet.operating_table.add_row(
                    ['Operating Temperature', TEMP, TEMP, TEMP, 'Celsius'])

                try:
                    new_sheet.operating_table.add_row(['Operating Frequency (F)', '', '', str(
                        math.floor(1000/float(MIN_PERIOD))), 'MHz'])
                except Exception:
                    # failed to provide non-zero MIN_PERIOD
                    new_sheet.operating_table.add_row(
                        ['Operating Frequency (F)', '', '', "not available in netlist only", 'MHz'])
                new_sheet.power_table = table_gen("power")
                new_sheet.power_table.add_row(
                    ['Pins', 'Mode', 'Power', 'Units'])
                new_sheet.timing_table = table_gen("timing")
                new_sheet.timing_table.add_row(
                    ['Parameter', 'Min', 'Max', 'Units'])
                # parse initial timing information
                while(True):
                    col_start = col
                    if(row[col].startswith('din')):
                        start = col

                        new_sheet.timing_table.add_row(
                            ['{0} setup rising'.format(row[start]), row[col+1], row[col+2], 'ns'])
                        col += 2

                        new_sheet.timing_table.add_row(
                            ['{0} setup falling'.format(row[start]), row[col+1], row[col+2], 'ns'])

                        col += 2

                        new_sheet.timing_table.add_row(
                            ['{0} hold rising'.format(row[start]), row[col+1], row[col+2], 'ns'])

                        col += 2

                        new_sheet.timing_table.add_row(
                            ['{0} hold falling'.format(row[start]), row[col+1], row[col+2], 'ns'])

                        col += 2

                        col += 1

                    elif(row[col].startswith('dout')):
                        start = col

                        new_sheet.timing_table.add_row(
                            ['{0} cell rise'.format(row[start]), row[col+1], row[col+2], 'ns'])
                        col += 2

                        new_sheet.timing_table.add_row(
                            ['{0} cell fall'.format(row[start]), row[col+1], row[col+2], 'ns'])

                        col += 2

                        new_sheet.timing_table.add_row(
                            ['{0} rise transition'.format(row[start]), row[col+1], row[col+2], 'ns'])

                        col += 2

                        new_sheet.timing_table.add_row(
                            ['{0} fall transition'.format(row[start]), row[col+1], row[col+2], 'ns'])

                        col += 2

                        col += 1

                    elif(row[col].startswith('csb')):
                        start = col

                        new_sheet.timing_table.add_row(
                            ['{0} setup rising'.format(row[start]), row[col+1], row[col+2], 'ns'])
                        col += 2

                        new_sheet.timing_table.add_row(
                            ['{0} setup falling'.format(row[start]), row[col+1], row[col+2], 'ns'])

                        col += 2

                        new_sheet.timing_table.add_row(
                            ['{0} hold rising'.format(row[start]), row[col+1], row[col+2], 'ns'])

                        col += 2

                        new_sheet.timing_table.add_row(
                            ['{0} hold falling'.format(row[start]), row[col+1], row[col+2], 'ns'])

                        col += 2

                        col += 1

                    elif(row[col].startswith('web')):
                        start = col

                        new_sheet.timing_table.add_row(
                            ['{0} setup rising'.format(row[start]), row[col+1], row[col+2], 'ns'])
                        col += 2

                        new_sheet.timing_table.add_row(
                            ['{0} setup falling'.format(row[start]), row[col+1], row[col+2], 'ns'])

                        col += 2

                        new_sheet.timing_table.add_row(
                            ['{0} hold rising'.format(row[start]), row[col+1], row[col+2], 'ns'])

                        col += 2

                        new_sheet.timing_table.add_row(
                            ['{0} hold falling'.format(row[start]), row[col+1], row[col+2], 'ns'])

                        col += 2

                        col += 1

                    elif(row[col].startswith('addr')):
                        start = col

                        new_sheet.timing_table.add_row(
                            ['{0} setup rising'.format(row[start]), row[col+1], row[col+2], 'ns'])
                        col += 2

                        new_sheet.timing_table.add_row(
                            ['{0} setup falling'.format(row[start]), row[col+1], row[col+2], 'ns'])

                        col += 2

                        new_sheet.timing_table.add_row(
                            ['{0} hold rising'.format(row[start]), row[col+1], row[col+2], 'ns'])

                        col += 2

                        new_sheet.timing_table.add_row(
                            ['{0} hold falling'.format(row[start]), row[col+1], row[col+2], 'ns'])

                        col += 2

                        col += 1

                    else:
                        for element in row[col_start:col-1]:
                            sheet.description.append(str(element))
                        break
                # parse initial power and leakage information
                while(True):
                    start = col
                    if(row[col].startswith('power')):
                        new_sheet.power_table.add_row([row[col+1],
                                                       '{0} Rising'.format(
                                                           row[col+2]),
                                                       row[col+3][0:6],
                                                       'mW']
                                                      )
                        new_sheet.power_table.add_row([row[col+1],
                                                       '{0} Falling'.format(
                                                           row[col+2]),
                                                       row[col+3][0:6],
                                                       'mW']
                                                      )

                        col += 4

                    elif(row[col].startswith('leak')):
                        new_sheet.power_table.add_row(
                            [row[col+1], 'leakage', row[col+2], 'mW'])
                        col += 3

                    else:
                        break

                new_sheet.dlv_table = table_gen("dlv")
                new_sheet.dlv_table.add_row(['Type', 'Description', 'Link'])

                new_sheet.io_table = table_gen("io")
                new_sheet.io_table.add_row(['Type', 'Value'])

                if not OPTS.netlist_only:
                    # physical layout files should not be generated in netlist only mode
                    new_sheet.dlv_table.add_row(
                        ['.gds', 'GDSII layout views', '<a href="{0}.{1}">{0}.{1}</a>'.format(OPTS.output_name, 'gds')])
                    new_sheet.dlv_table.add_row(
                        ['.lef', 'LEF files', '<a href="{0}.{1}">{0}.{1}</a>'.format(OPTS.output_name, 'lef')])

                new_sheet.dlv_table.add_row(
                    ['.log', 'OpenRAM compile log', '<a href="{0}.{1}">{0}.{1}</a>'.format(OPTS.output_name, 'log')])
                new_sheet.dlv_table.add_row(
                    ['.v', 'Verilog simulation models', '<a href="{0}.{1}">{0}.{1}</a>'.format(OPTS.output_name, 'v')])
                new_sheet.dlv_table.add_row(
                    ['.html', 'This datasheet', '<a href="{0}.{1}">{0}.{1}</a>'.format(OPTS.output_name, 'html')])
                new_sheet.dlv_table.add_row(
                    ['.lib', 'Synthesis models', '<a href="{1}">{1}</a>'.format(LIB_NAME, LIB_NAME.replace(OUT_DIR, ''))])
                new_sheet.dlv_table.add_row(
                    ['.db', 'Compiled .lib', '<a href="{1}">{1}</a>'.format(LIB_NAME[:-3] + 'db', LIB_NAME.replace(OUT_DIR, '')[:-3] + 'db')])
                new_sheet.dlv_table.add_row(
                    ['.py', 'OpenRAM configuration file', '<a href="{0}.{1}">{0}.{1}</a>'.format(OPTS.output_name, 'py')])
                new_sheet.dlv_table.add_row(
                    ['.sp', 'SPICE netlists', '<a href="{0}.{1}">{0}.{1}</a>'.format(OPTS.output_name, 'sp')])

                new_sheet.io_table.add_row(['WORD_SIZE', WORD_SIZE])
                new_sheet.io_table.add_row(['NUM_WORDS', NUM_WORDS])
                new_sheet.io_table.add_row(['NUM_BANKS', NUM_BANKS])
                new_sheet.io_table.add_row(['NUM_RW_PORTS', NUM_RW_PORTS])
                new_sheet.io_table.add_row(['NUM_R_PORTS', NUM_R_PORTS])
                new_sheet.io_table.add_row(['NUM_W_PORTS', NUM_W_PORTS])
                new_sheet.io_table.add_row(
                    ['Area (&microm<sup>2</sup>)', str(round(float(AREA)))])


class datasheet_gen():
    def datasheet_write(name):
        """writes the datasheet to a file"""
        if OPTS.output_datasheet_info:
            datasheet_path = OPTS.output_path
        else:
            datasheet_path = OPTS.openram_temp

        if not (os.path.isdir(datasheet_path)):
            os.mkdir(datasheet_path)

        datasheets = []
        parse_characterizer_csv(datasheet_path + "/datasheet.info", datasheets)

        for sheets in datasheets:
            with open(name, 'w+') as f:
                sheets.generate_html()
                f.write(sheets.html)
