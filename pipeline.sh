#!/bin/bash

#######################################################
# --- PIPELINE TO RECREATE RESULTS FOR FI STUDIES --- #

# Clear out any old files
echo "Removing processed and output files"
rm output/*
rm processed/*

# --- (1) process excel files --- #
echo "Running (1)"
python fi_dataprep.py
# output: df_FI.csv, df_inf.csv

# --- (2) calculate FI or rev FI --- #
echo "Running (2)"
python fi_calc.py
# output: df_res.csv

# --- (3) Calculate summary statistics and figures --- #
echo "Running (3A)"
python fi_results_FIFQ.py
echo "Running (3B)"
python fi_results_insig.py
echo "Running (3C)"
python fi_results_neg.py


