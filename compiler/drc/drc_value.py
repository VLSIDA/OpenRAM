
class drc_value():
    """ 
    A single DRC value.
    """
    def __init__(self, value):
        self.value = value

    def __call__(self, *args):
        """
        Return the value.
        """
        return self.value
                
            
        

