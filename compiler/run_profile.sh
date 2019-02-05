#!/bin/bash
python3 -m cProfile -o profile.dat ./openram.py example_configs/medium_config_scn4m_subm.py -v | tee -i medium.log
echo "Run view_profile.py to view results"
