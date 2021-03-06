"""
SCRIPT TO CALCULATE EMPIRICAL RESULTS FOR FRAGILITY INDEX
"""

import os
import pandas as pd
import numpy as np
import scipy.stats as stats
from statsmodels.stats import multitest
import funs_fi as fi

dir_base = os.getcwd()
dir_output = os.path.join(dir_base,'output')

################################################
# ----------- (1) LOAD IN THE DATA ----------- #

tmp_FI = pd.read_csv(os.path.join('processed','df_FI.csv'))
tmp_inf = pd.read_csv(os.path.join('processed','df_inf.csv'))
tmp_res = pd.read_csv(os.path.join('processed','df_res.csv'))
df = tmp_inf.merge(tmp_FI,on=['tt','ID']).merge(tmp_res,on=['tt','ID'])
del tmp_FI, tmp_inf, tmp_res

# Calculate fragility quotient
df['FQ'] = df.FI / (df.num1 + df.num2)
df['FQ2'] = df.FI2 / (df.num1 + df.num2)



########################################################
# ----------- (2) PRINT SUMMARY STATISTICS ----------- #

dat_sumstats = df[['tt','ID','FI','FQ']].melt(['tt','ID']).groupby(['tt','variable']).value
# Mean, median, IQR, SE
dat_sumstats = dat_sumstats.apply(lambda x: pd.Series({'mean':x.mean(),'median':x.median(),
                  'se':x.std(),'l25':x.quantile(0.25),'l75':x.quantile(0.75),
                  'min':x.min(),'max':x.max()})).reset_index()
dat_sumstats = dat_sumstats.sort_values(['tt','variable']).pivot_table('value',['tt','variable'],'level_2').reset_index()
cn_ord = ['tt','variable','mean','se','median','l25','l75','min','max']
dat_sumstats = dat_sumstats[cn_ord]
dat_sumstats.columns.name = ''
# (1) Moments of the data
print('---------- (1) MOMENTS OF THE FI/FQ ----------')
print(np.round(dat_sumstats,2))
if not os.path.exists(dir_output):
  print('making output folder');os.mkdir(dir_output)
dat_sumstats.to_csv(os.path.join(dir_output,'summary_stats.csv'),index=False)

# (2) Summary statistics for PLUM
print('---------- (2) PLUM COMPARISONS ----------')
np.round(df[['tt','plum1','plum2','plum3']].groupby('tt').agg(['mean','std']).reset_index(),0)
dat_study_design = df[['tt','study_design']].groupby(['tt']).apply(lambda x: x['study_design'].value_counts(normalize=True)).reset_index()
dat_study_design.columns.name = ''
print(np.round(dat_study_design,2))

# (3) Plum-X captures for RCTs vs non-RCTs
plum2_rct = df[(df.tt == 'bbd') & (df.study_design=='RCT')].plum2
plum2_nrct = b=df[(df.tt == 'bbd') & ~(df.study_design=='RCT')].plum2
pval_plumx_rct = stats.ttest_ind(a=plum2_rct,b=plum2_nrct,equal_var=True).pvalue
print('Two-sided p-value: %0.1f%%\nRCT: mean (%0.0f), sd (%0.0f)\nnRCT: mean(%0.0f), sd(%0.0f)' %
      (pval_plumx_rct*100,plum2_rct.mean(),plum2_rct.std(),plum2_nrct.mean(),plum2_nrct.std()))

# (4) Alternative FI
df_fi = df[df.tt.isin(['bbd','phn'])].reset_index(drop=True)
df_fi['FI_max'] = df_fi[['FI','FI2']].max(axis=1)
df_fi['FQ_max'] = df_fi.FI_max / (df_fi.num1 + df_fi.num2)
df_fi.insert(0,'mm','all')
df_fi2 = df_fi[df_fi.FI > 0].drop(columns='mm').reset_index(drop=True)
df_fi2.insert(0,'mm','FI>0')
df_fi_long = pd.concat([df_fi, df_fi2]).reset_index(drop=True).melt(
    id_vars=['mm','tt','study_design'],value_vars=['FI','FQ','FI_max','FQ_max'])
df_mandy = df_fi_long.groupby(['mm','tt','study_design','variable']).describe().reset_index()
df_mandy.columns = pd.Series([x[0]+'_'+x[1] for x in df_mandy.columns]).str.replace('_$|value_','')
df_mandy = df_mandy.drop(columns=['std','25%','75%','count','min']).rename(columns={'50%':'median'})
df_mandy = df_mandy.sort_values(['study_design','mm','tt','variable'],ascending=False).reset_index(drop=True)
df_mandy.to_csv(os.path.join(dir_output,'df_mandy.csv'),index=False)
print(np.round(df_mandy,1))


###############################################################################
# ----------- (3) STATISTICAL TESTING FOR NUMERIC AND CATEGORICAL ----------- #

# ---- (3.A) Spearman correlation for numeric factors
cn_num = ['IF','h_index','citation','wcitation','plum1','plum2']
df_num = df[['tt','FI','FQ'] + cn_num].melt(['tt','FI','FQ'],
          var_name='metric').melt(['tt','metric','value'],value_name='FI')
df_num = df_num[df_num.value.notnull()].reset_index(drop=True)
dat_pval_num = df_num.groupby(['tt','metric','variable']).apply(lambda x:
    pd.Series({'pval':stats.spearmanr(a=x['value'],b=x['FI'])})).reset_index()
dat_pval_num = pd.concat([dat_pval_num.drop(columns='pval'),
    pd.DataFrame([[x.correlation, x.pvalue] for x in dat_pval_num.pval],
                        columns=['stat','pval'])],axis=1)
dat_pval_num.insert(0, 'feature', 'num')

# ---- (3.B) Kruskal-Wallis test for categorical features ---- #
cn_fac = ['journal', 'geo', 'study_design', 'type_random', 'concealment',
          'blinding', 'power_just', 'outcome', 'statistician', 'funding']

df_cat = df[['tt','FI','FQ'] + cn_fac].melt(['tt','FI','FQ'],
          var_name='metric').melt(['tt','metric','value'],value_name='FI')
df_cat['value'] = df_cat.value.fillna('missing')
# Drop features with > 50% missingness
#dat_cn_drop = df_cat.groupby(['tt','metric']).value.apply(lambda x: np.mean(x.isnull())).reset_index()
# dat_cn_drop = dat_cn_drop[dat_cn_drop.value > 0.5].reset_index(drop=True).drop(columns='value')
# dat_cn_drop.insert(0,'drop',True)
# df_cat = df_cat.merge(dat_cn_drop,on=['tt','metric'],how='left')
# df_cat = df_cat[df_cat['drop'].isnull()].drop(columns='drop').reset_index(drop=True)

dat_pval_cat = df_cat.groupby(['tt','metric','variable']).apply(lambda x:
  pd.Series({'pval': stats.kruskal(*[x['FI'][x['value']==gg] for gg in x['value'].unique()])}) ).reset_index()
dat_pval_cat = pd.concat([dat_pval_cat.drop(columns='pval'),
    pd.DataFrame([[x.statistic, x.pvalue] for x in dat_pval_cat.pval],
                        columns=['stat','pval'])],axis=1)
dat_pval_cat.insert(0, 'feature', 'cat')

# Merge and adjust
dat_pval = pd.concat([dat_pval_num,dat_pval_cat]).reset_index(drop=True)
dat_pval['fdr'] = dat_pval.groupby('tt').pval.transform(lambda x:
            multitest.fdrcorrection(pvals=x,alpha=0.1)[1])
dat_pval.to_csv(os.path.join(dir_output,'dat_pvals.csv'),index=False)
# Print the significant results
for tt in ['bbd','phn','neg']:
  print('Study type: %s' % (tt))
  tmp = dat_pval[(dat_pval.tt == tt) & (dat_pval.fdr < 0.1)]
  if tmp.shape[0] > 0:
    print(tmp)
  else:
    print('No statistically significant associations')

print('---------- (3) P-VALUE RESULTS FOR BBD STUDIES ------------')
print(np.round(dat_pval[dat_pval.tt == 'bbd'],3))

df_bbd = df[df.tt == 'bbd']
rho_FI_act = stats.spearmanr(df_bbd.FI, df_bbd.pval_FI)
rho_FQ_act = stats.spearmanr(df_bbd.FQ, df_bbd.pval_FI)
rho_FI_rep = stats.spearmanr(df_bbd.FI, df_bbd.pval_rep)
rho_FQ_rep = stats.spearmanr(df_bbd.FQ, df_bbd.pval_rep)

print('Actual: FI %0.3f (%0.3f), FQ %0.3f (%0.3f)\nReported: FI %0.3f (%0.3f), FQ %0.3f (%0.3f)' %
      (rho_FI_act.correlation, rho_FI_act.pvalue,rho_FQ_act.correlation, rho_FQ_act.pvalue,
       rho_FI_rep.correlation, rho_FI_rep.pvalue,rho_FQ_rep.correlation, rho_FQ_rep.pvalue))


print('---------- (4) CHECK TABLE 2 ------------')

from support_fi import di_geo_bbd

# Should Russia/Israel currently part of Asia
di_region = {'Turkey':'Asia','Iran':'Asia','USA':'NAmerica','Brazil':'SAmerica',
 'Chile':'SAmerica','China':'Asia','Netherlands':'Europe','Italy':'Europe',
 'Belgium':'Europe','India':'Asia','Egypt':'Africa','Denmark':'Europe',
 'Taiwan':'Asia','Greece':'Europe','Russia':'Asia','Hungary':'Europe',
 'France':'Europe','England':'Europe','Germany':'Europe','Sweden':'Europe',
 'Australia':'Austalia','Israel':'Asia','Iraq':'Asia','Finland':'Europe',
 'Portugal':'Europe','Korea':'Asia','Canada':'NAmerica','Japan':'Asia','Serbia':'Europe',
 'Poland':'Europe','Austria':'Europe','Saudi Arabia':'Asia','Slovenia':'Europe',
 'Kuwait':'Asia','Norway':'Europe','Romania':'Europe','Switzerland':'Europe'}
print(df_bbd.geo.map(di_geo_bbd).map(di_region).value_counts().reset_index())
df_bbd['region'] = df_bbd.geo.map(di_geo_bbd).map(di_region).to_list()

df_region = df_bbd.groupby('region').IF.apply(lambda x: pd.Series({'med':x.median(),
        'l25':x.quantile(0.25),'l75':x.quantile(0.75)})).reset_index().round(2)
df_region = df_region.pivot('region','level_1','IF').reset_index()
tmp = df_region.med.astype(str) + '  (' + df_region.l25.astype(str)+'-'+df_region.l75.astype(str) + ')'
print(pd.DataFrame({'region':df_region.region, 'val':tmp}))


uregion = df_bbd.region.unique()
# Kruskal wallis all way!
IF_region = [df_bbd.IF[df_bbd.region == rr].to_list() for rr in uregion]
print(stats.kruskal(*IF_region))

# Test the h_index
print(stats.kruskal(*[df_bbd.h_index[df_bbd.region == rr].to_list() for rr in uregion])[1] * 7)

pstore = []
for rr in uregion:
    pstore.append(stats.kruskal(df_bbd.IF[df_bbd.region == rr].to_list(),
                            df_bbd.IF[~(df_bbd.region == rr)].to_list())[1])
print(pd.DataFrame({'region':uregion,
              'sig':multitest.multipletests(pstore, alpha=0.05, method='bonferroni')[0]}))

# Run t-test to compare FI between regions
stats.ttest_ind(a=df_bbd.FI[df_bbd.region=='Europe'].to_list(),
                b=df_bbd.FI[df_bbd.region=='Africa'].to_list(),equal_var=False)



