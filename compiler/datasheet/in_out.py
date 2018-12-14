from flask_table import *

class in_out(Table):
    """
    Set up I/O table columns and title information for multiport debugging
    """
    typ = Col('Type')
    description = Col('Description')


class in_out_item(object):
    """
    Define table row element for I/O table
    """
    def __init__(self, typ, description):
        self.typ = typ
        self.description = description
