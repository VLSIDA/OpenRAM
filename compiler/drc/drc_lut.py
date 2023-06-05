# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug


class drc_lut():
    """
    Implement a lookup table of rules.
    Each element is a tuple with the last value being the rule.
    It searches through backwards until all of the key values are
    met and returns the rule value.
    For exampe, the key values can be width and length,
    and it would return the rule for a wire of at least a given width and length.
    A dimension can be ignored by passing inf.
    """
    def __init__(self, table):
        self.table = table

    def __call__(self, *key):
        """
        Lookup a given tuple in the table.
        """
        if len(key)==0:
            first_key = list(sorted(self.table.keys()))[0]
            return self.table[first_key]

        for table_key in sorted(self.table.keys(), reverse=True):
            if self.match(key, table_key):
                return self.table[table_key]

    def match(self, key1, key2):
        """
        Determine if key1>=key2 for all tuple pairs.
        (i.e. return false if key1<key2 for any pair.)
        """
        # If any one pair is less than, return False
        debug.check(len(key1) == len(key2), "Comparing invalid key lengths.")
        for k1, k2 in zip(key1, key2):
            if k1 < k2:
                return False
        return True




