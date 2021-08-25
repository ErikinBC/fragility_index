# Fragility index (FI) for bowel and bladder dysfunction (BBD) and hydronephrosis (PHN)

Output from results used for the following studies:

1. How popular is the bladder and bowel dysfunction literature: PlumX metrics contrasted with fragility indicators
2. “Close to being significant:” reverse fragility index as a novel metric for null-effect studies in the Pediatric Urology literature
3. A second-look at reported statistics: Challenges in replicating reported p-values in pediatric urology literature

This code will calculate the 1) p-value fragility (for significant studies), 2) reverse p-value fragility (for non-significant studies), and 3) errors in reported p-value calculations.

To replicate the results:

1. Install conda environment: `conda install --file fi_env.txt`
2. Run the python scripts in order: `source pipeline.sh`

The pipeline shell is as follows:

1. `1_dataprep.py`: This script loads in the hard-coded excel files that have the list of studies with the different group counts and study covariates (study year, impact factor, study design). It will output `~/output/{df_FI,df_inf}.csv`, the former having the group 1/2 counts, and the latter havng the study annotations.
2. 


