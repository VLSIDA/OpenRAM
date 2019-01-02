from flask_table import *

class deliverables(Table):
    """
    Set up delivarables table columns and title information
    """
    typ = Col('Type')
    description = Col('Description')
    link = Col('Link')


class deliverables_item(object):
    """
    Define deliverables table row elemenent information
    """
    def __init__(self, typ, description,link):
        self.typ = typ
        self.description = description
        self.link = link
