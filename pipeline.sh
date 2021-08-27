#!/bin/bash

# PIPELINE TO RECREATE RESULTS FOR FI STUDIES #

echo "---- Running set_env.sh -----"
source set_env.sh

echo "---- Running 1_dataprep.py -----"
python -u 1_dataprep.py
# output: df_FI.csv, df_inf.csv

echo "---- Running 2_fragility.py ----"
python -u 2_fragility.py
# output: df_res.csv


echo "~~~ End of pipeline.sh ~~~"
return


# --- (3) Calculate summary statistics and figures --- #
echo "Running (3A)"
python fi_results_FIFQ.py
echo "Running (3B)"
python fi_results_insig.py
echo "Running (3C)"
python fi_results_neg.py


# https://drive.google.com/drive/folders/17jD5NU-6anD4nNI1TfFB9hFMH7vOU8Dd
# https://docs.google.com/document/d/1TP2Eruu5KSoniDDVqqH-0SG3scITsxaFhkLs5vdLB6Q/edit
# https://docs.google.com/document/d/1Y1K8awCn0_vdjw1ebn3qscwAEtosdjp2TdQfFHd036s/edit
# https://docs.google.com/document/d/1kH7Idwh_FFysSERnLhRqXbhTR3GhW_XcG_LrvpgKM2U/edit

