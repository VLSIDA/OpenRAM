#!/usr/bin/env python3
import pstats
p = pstats.Stats("profile.dat")
p.strip_dirs()
p.sort_stats("cumulative")
#p.print_stats(50)
p.print_stats()

