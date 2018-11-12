from design import design
class gds_cell(design):
    """
    A generic GDS design.
    """
    def __init__(self, name, gds_file):
        self.name = name
        self.gds_file = gds_file
        self.sp_file = None
        
        design.__init__(self, name)

        # The dimensions will not be defined, so do this...
        self.width=0
        self.height=0

