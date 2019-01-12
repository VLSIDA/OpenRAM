#!/bin/bash
python3 -m cProfile -o profile.dat ./openram.py example_config_scn4m_subm.py -v
echo "Run view_profile.py to view results"
