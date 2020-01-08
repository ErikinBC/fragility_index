#!/bin/bash

#######################################################
# --- PIPELINE TO RECREATE RESULTS FOR FI STUDIES --- #

# --- (1) process excel files --- #
echo "Running (1)"
python fi_dataprep.py
# output: df_FI.csv, df_inf.csv

# --- (2) calculate FI or rev FI --- #
echo "Running (2)"
python fi_calc.py
# output: df_res.csv

# --- (3) Calculate summary statistics and figures --- #
echo "Running (3)"
#python fi_results.py




