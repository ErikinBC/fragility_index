# Fragility index (FI) for bowel and bladder dysfunction (BBD) and hydronephrosis (PHN)

Output from results used for the following studies:

1. [Trends and relevance in the bladder and bowel dysfunction literature: PlumX metrics contrasted with fragility indicators](https://pubmed.ncbi.nlm.nih.gov/32684443)
2. [A second-look at reported statistics: Challenges in replicating reported p-values in pediatric urology literature](https://www.auajournals.org/doi/abs/10.1097/JU.0000000000002065.13)

This code will calculate the 1) p-value fragility (for significant studies), 2) reverse p-value fragility (for non-significant studies), and 3) errors in reported p-value calculations.

To replicate the results:

1. Install conda environment: `conda install --file conda.env`
2. Run the python scripts in order: `source pipeline.sh`

The pipeline shell is as follows:

1. `1_dataprep.py`: This script loads in the hard-coded excel files that have the list of studies with the different group counts and study covariates (study year, impact factor, study design). It will output `~/output/{df_FI,df_inf}.csv`, the former having the group 1/2 counts, and the latter havng the study annotations.
2. `2_fragility.py`: Calculates the different FI index measures for all studies and saves results in `df_res.csv`.
3. `3_results_FIFQ.py`: Calculates statistical associations on different journal factors and FI/FQ measures.
4. `4_results_insig.py`: Explores the papers that had baseline insignificant results and whether these could be accounted for.

