class table_gen:
    def __init__(self, name):
        self.name = name
        self.rows = []
        self.table_id = 'data'

    def add_row(self, row):
        self.rows.append(row)

    def gen_table_head(self):
        html = ''

        html += '<thead>'
        html += '<tr>'
        for col in self.rows[0]:
            html += '<th>' + str(col) + '</th>'
        html += '</tr>'
        html += '</thead>'
        return html

    def gen_table_body(self):
        html = ''

        html += '<tbody>'
        html += '<tr>'
        for row in self.rows[1:]:
            html += '<tr>'
            for col in row:
                html += '<td>' + str(col) + '</td>'
            html += '</tr>'
        html += '</tr>'
        html += '</tbody>'
        return html

    def to_html(self):

        html = ''
        html += '<table id= \"'+self.table_id+'\">'
        html += self.gen_table_head()
        html += self.gen_table_body()
        html += '</table>'

        return html
