from flask_table import *
from operating_conditions import *
from characterization_corners import *
from deliverables import *
from timing_and_current_data import *
from in_out import *
from hierarchy_design import total_drc_errors
from hierarchy_design import total_lvs_errors
import os
from globals import OPTS

class datasheet():
    """
    Defines the layout,but not the data,  of the html datasheet
    """
    def __init__(self,identifier):
        self.io = []
        self.corners = []
        self.timing = []
        self.operating = []
        self.dlv = []
        self.name = identifier
        self.html = ""
        

    def generate_html(self):
        """
        Generates html tables using flask-table
        """
        with open(os.path.abspath(os.environ.get("OPENRAM_HOME")) + '/datasheet/assets/datasheet.css', 'r') as datasheet_css:
            #css styling is kept in a seperate file
            self.html += datasheet_css.read()

        if OPTS.check_lvsdrc:
            
            DRC = str(total_drc_errors) + ' errors'
            LVS = str(total_lvs_errors) + ' errors'
            PEX = 'n/a'
        else:
            DRC = 'skipped'
            LVS = 'skipped'
            PEX = 'skipped'
       

        self.html +='<p style=font-size: 20px;font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;>'+ self.name + '.html' + '</p>'
        self.html +='<p style=font-size: 20px;font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;>'+ 'DRC: ' + str(DRC) + '</p>'
        self.html +='<p style=font-size: 20px;font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;>'+ 'LVS: ' + str(LVS) + '</p>'

        self.html +='<p style=font-size: 20px;font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;>Ports and Configuration (DEBUG)</p>'
        self.html += in_out(self.io,table_id='data').__html__().replace('&lt;','<').replace('&#34;','"').replace('&gt;',">")

        self.html +='<p style=font-size: 20px;font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;>Operating Conditions</p>'
        self.html += operating_conditions(self.operating,table_id='data').__html__()

        self.html += '<p style=font-size: 20px;font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;>Timing and Current Data</p>'
        self.html += timing_and_current_data(self.timing,table_id='data').__html__()

        self.html += '<p style=font-size: 20px;font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;>Characterization Corners</p>'
        self.html += characterization_corners(self.corners,table_id='data').__html__()

        self.html +='<p style=font-size: 20px;font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;>Deliverables</p>'
        self.html += deliverables(self.dlv,table_id='data').__html__().replace('&lt;','<').replace('&#34;','"').replace('&gt;',">")

        self.html +='<p style=font-size: 20px;font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;>*Feature only supported with characterizer</p>'
        
        self.html +='<img src=' + os.path.abspath(os.environ.get("OPENRAM_HOME")) + '/datasheet/assets/vlsi_logo.png alt="VLSIDA" />' 
