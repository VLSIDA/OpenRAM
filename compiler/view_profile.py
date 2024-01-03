#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import pstats
p = pstats.Stats("profile.dat")
p.strip_dirs()
# p.sort_stats("cumulative")
p.sort_stats("tottime")
# p.print_stats(50)
p.print_stats()

