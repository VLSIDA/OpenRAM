from flask_table import *

class in_out(Table):
    typ = Col('Type')
    description = Col('Description')


class in_out_item(object):
    def __init__(self, typ, description):
        self.typ = typ
        self.description = description
