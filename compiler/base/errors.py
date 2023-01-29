# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#

class drc_error(Exception):
    """Exception raised for DRC errors.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    # def __init__(self, expression, message):
    #     self.expression = expression
    #     self.message = message
    def __init__(self, message):
        self.message = message
