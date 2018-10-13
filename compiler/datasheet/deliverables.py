from flask_table import *

class deliverables(Table):
    typ = Col('Type')
    description = Col('Description')
    link = Col('Link')


class deliverables_item(object):
    def __init__(self, typ, description,link):
        self.typ = typ
        self.description = description
        self.link = link
