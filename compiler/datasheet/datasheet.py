# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os
import base64
from openram import OPTS
from .table_gen import *


class datasheet():
    """
    Defines the layout,but not the data,  of the html datasheet
    """

    def __init__(self, identifier):
        self.name = identifier
        self.html = ""

    def generate_html(self):
        """
        Generates html tables using flask-table
        """
        with open(os.path.abspath(os.environ.get("OPENRAM_HOME")) + '/datasheet/assets/datasheet.css', 'r') as datasheet_css:
            # css styling is kept in a seperate file
            self.html += datasheet_css.read()

        if OPTS.output_datasheet_info:
            datasheet_path = OPTS.output_path
        else:
            datasheet_path = OPTS.openram_temp
        with open(datasheet_path + "/datasheet.info") as info:
            self.html += '<!--'
            for row in info:
                self.html += row
#            for item in self.description:
#                self.html += item + ','
            self.html += '-->'
        # Add vlsida logo
        vlsi_logo = 0
        with open(os.path.abspath(os.environ.get("OPENRAM_HOME")) + '/datasheet/assets/vlsi_logo.png', "rb") as image_file:
            vlsi_logo = base64.b64encode(image_file.read())

        # Add openram logo
        openram_logo = 0
        with open(os.path.abspath(os.environ.get("OPENRAM_HOME")) + '/datasheet/assets/OpenRAM_logo.png', "rb") as image_file:
            openram_logo = base64.b64encode(image_file.read())

        #comment table rows which we may want to enable after compile time
        comments = ['.db']

        self.html += '<a href="https://vlsida.soe.ucsc.edu/"><img src="data:image/png;base64,{0}" alt="VLSIDA"></a><a href ="https://github.com/VLSIDA/OpenRAM"><img src ="data:image/png;base64,{1}" alt = "OpenRAM"></a>'.format(str(vlsi_logo)[2:-1], str(openram_logo)[2:-1])

        self.html += '<p style="font-size: 18px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">' + \
            self.name + '.html' + '</p>'
        self.html += '<p style="font-size: 18px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">Compiled at: ' + self.time + '</p>'
        self.html += '<p style="font-size: 18px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">' + \
            'DRC errors: ' + str(self.DRC) + '</p>'
        self.html += '<p style="font-size: 18px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">' + \
            'LVS errors: ' + str(self.LVS) + '</p>'
        self.html += '<p style="font-size: 18px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">' + \
            'Git commit id: ' + str(self.git_id) + '</p>'
        # print port table
        self.html += '<p style="font-size: 26px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">Ports and Configuration</p>'
        self.html += self.io_table.to_html(comments)

        # print operating condidition information
        self.html += '<p style="font-size: 26px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">Operating Conditions</p>'
        self.html += self.operating_table.to_html(comments)

        # check if analytical model is being used
        self.html += '<p style="font-size: 26px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">Timing Data</p>'
        model = ''
        if self.ANALYTICAL_MODEL == 'True':
            model = "analytical model: results may not be precise"
        else:
            model = "spice characterizer"
        # display timing data
        self.html += '<p style="font-size: 26px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">Using '+model+'</p>'
        self.html += self.timing_table.to_html(comments)
        # display power data
        self.html += '<p style="font-size: 26px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">Power Data</p>'
        self.html += self.power_table.to_html(comments)
        # display corner information
        self.html += '<p style="font-size: 26px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">Characterization Corners</p>'
        self.html += self.corners_table.to_html(comments)
        # display deliverables table
        self.html += '<p style="font-size: 26px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">Deliverables</p>'
        self.dlv_table.sort()
        self.html += self.dlv_table.to_html(comments)
