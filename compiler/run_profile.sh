#!/bin/bash
python3 -m cProfile -o profile.dat ./openram.py example_configs/giant_config_scn4m_subm.py -v | tee -i big.log
echo "Run view_profile.py to view results"
