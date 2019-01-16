from table_gen import *
import os
import base64
from globals import OPTS


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

        with open(OPTS.openram_temp + "/datasheet.info") as info:
            self.html += '<!--'
            for row in info:
                self.html += row
#            for item in self.description:
#                self.html += item + ','
            self.html += 'EOL'
            self.html += '-->'

        vlsi_logo = 0
        with open(os.path.abspath(os.environ.get("OPENRAM_HOME")) + '/datasheet/assets/vlsi_logo.png', "rb") as image_file:
            vlsi_logo = base64.b64encode(image_file.read())

        openram_logo = 0
        with open(os.path.abspath(os.environ.get("OPENRAM_HOME")) + '/datasheet/assets/openram_logo_placeholder.png', "rb") as image_file:
            openram_logo = base64.b64encode(image_file.read())

        self.html += '<a href="https://vlsida.soe.ucsc.edu/"><img src="data:image/png;base64,{0}" alt="VLSIDA"></a>'.format(str(vlsi_logo)[
                                                                                                                            2:-1])

        self.html += '<p style="font-size: 18px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">' + \
            self.name + '.html' + '</p>'
        self.html += '<p style="font-size: 18px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">Compiled at: ' + self.time + '</p>'
        self.html += '<p style="font-size: 18px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">' + \
            'DRC errors: ' + str(self.DRC) + '</p>'
        self.html += '<p style="font-size: 18px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">' + \
            'LVS errors: ' + str(self.LVS) + '</p>'
        self.html += '<p style="font-size: 18px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">' + \
            'Git commit id: ' + str(self.git_id) + '</p>'

        self.html += '<p style="font-size: 26px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">Ports and Configuration</p>'
#        self.html += in_out(self.io,table_id='data').__html__().replace('&lt;','<').replace('&#34;','"').replace('&gt;',">")
        self.html += self.io_table.to_html()

        self.html += '<p style="font-size: 26px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">Operating Conditions</p>'
#        self.html += operating_conditions(self.operating,table_id='data').__html__()
        self.html += self.operating_table.to_html()

        self.html += '<p style="font-size: 26px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">Timing and Current Data</p>'
#        self.html += timing_and_current_data(self.timing,table_id='data').__html__()
        self.html += self.timing_table.to_html()

        self.html += '<p style="font-size: 26px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">Characterization Corners</p>'
#        self.html += characterization_corners(self.corners,table_id='data').__html__()
        self.html += self.corners_table.to_html()

        self.html += '<p style="font-size: 26px;font-family: Trebuchet MS, Arial, Helvetica, sans-serif;">Deliverables</p>'
#        self.html += deliverables(self.dlv,table_id='data').__html__().replace('&lt;','<').replace('&#34;','"').replace('&gt;',">")
        self.html += self.dlv_table.to_html()
