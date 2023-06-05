# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

class table_gen:
    """small library of functions to generate the html tables"""

    def __init__(self, name):
        self.name = name
        self.rows = []
        self.table_id = 'data'

    def add_row(self, row):
        """add a row to table_gen object"""
        self.rows.append(row)

    def gen_table_head(self):
        """generate html table header"""
        html = ''

        html += '<thead>'
        html += '<tr>'
        for col in self.rows[0]:
            html += '<th>' + str(col) + '</th>'
        html += '</tr>'
        html += '</thead>'
        return html

    def gen_table_body(self,comments):
        """generate html body (used after gen_table_head)"""
        html = ''

        html += '<tbody>'
        html += '<tr>'
        for row in self.rows[1:]:

            if row[0] not in comments:
                html += '<tr>'
                for col in row:
                    html += '<td>' + str(col) + '</td>'
                html += '</tr>'

            else:
                html += '<!--'+row[0]+'<tr>'
                for col in row:
                    html += '<td>' + str(col) + '</td>'
                html += '</tr>'+row[0]+'-->'

        html += '</tr>'
        html += '</tbody>'
        return html
    def sort(self):
        self.rows[1:] = sorted(self.rows[1:], key=lambda x : x[0])

    def to_html(self,comments):
        """writes table_gen object to inline html"""
        html = ''
        html += '<table id= \"'+self.table_id+'\">'
        html += self.gen_table_head()
        html += self.gen_table_body(comments)
        html += '</table>\n'

        return html
