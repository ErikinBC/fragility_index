#!/bin/bash

# PIPELINE TO RECREATE RESULTS FOR FI STUDIES #

# Note swap={i} is for patient shift amongst group {i} (traditional FI is swap=1)

echo "---- Running set_env.sh -----"
source set_env.sh

echo "---- Running 1_dataprep.py -----"
python -u 1_dataprep.py
# output: df_FI.csv, df_inf.csv

echo "---- Running 2_fragility.py ----"
python -u 2_fragility.py
# output: df_res.csv

echo "---- Running 3_results_FIFQ.py ----"
python -u 3_results_FIFQ.py
# output: 
#           summary_stats.csv (moments of the FI/FQ by test and swap approach)
#           pval_plum_ttest.csv (t-test between RCT vs Other study_design by log(plum) metric appraoch (1/2/3))
#           dat_study.csv (mean/median/max of different FI/FQ by test and swap by study design)
#           dat_pvals.csv (, note FDR correction applied to groupby (test/swap))

echo "---- Running 4_results_insig.py ----"
python 4_results_insig.py
# output:   insig_spot.xlsx
#           df_acc.csv
# Note: the reason column is updated manually by checking paper results

echo "~~~ End of pipeline.sh ~~~"

# https://drive.google.com/drive/folders/17jD5NU-6anD4nNI1TfFB9hFMH7vOU8Dd
# https://docs.google.com/document/d/1TP2Eruu5KSoniDDVqqH-0SG3scITsxaFhkLs5vdLB6Q/edit
# https://docs.google.com/document/d/1Y1K8awCn0_vdjw1ebn3qscwAEtosdjp2TdQfFHd036s/edit
# https://docs.google.com/document/d/1kH7Idwh_FFysSERnLhRqXbhTR3GhW_XcG_LrvpgKM2U/edit

