# Analyze fragility results for BBD and PHN studies

# Load modules
import os
import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats.stats import moment
from statsmodels.stats import multitest
from support_funs import di_geo_bbd, di_region

# Set directories
dir_base = os.getcwd() 
dir_output = os.path.join(dir_base,'output')

# Pre-set columns
cn_FI = ['test','swap']
cn_idx = cn_FI + ['msr','tt']
cn_gg = ['tt','ID']
cn_val = ['FI','FQ']
cn_desc_lvl = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
cn_desc_lbl = ['n', 'mean', 'se', 'min', 'l25', 'median', 'l75', 'max']
cn_num = ['IF','h_index','citation','wcitation','plum1','plum2']
cn_fac = ['journal', 'geo', 'study_design', 'type_random', 'concealment',
          'blinding', 'power_just', 'outcome', 'statistician', 'funding']


# Helper functions to return data.frames for groupby commands
def rho2df(a, b):
  test = stats.spearmanr(a, b)
  res = pd.DataFrame({'stat':test[0], 'pval':test[1]},index=[0])
  return res

def kruskal2df(a, b):
  assert len(a) == len(b)
  ua = np.unique(a)
  b_lst = [b[np.where(a == aa)[0]] for aa in ua]
  test = stats.kruskal(*b_lst)
  res = pd.DataFrame({'stat':test[0], 'pval':test[1]},index=[0])
  return res

def moments_ttest(x,ddof=1):
  res = pd.DataFrame({'mu':x.mean(), 'se':x.std(ddof=ddof), 'n':len(x)},index=[0])
  return res

def moments_study(x):
  res = pd.DataFrame({'mean':x.mean(), 'median':x.median(), 'max':x.max()},index=[0])
  return res


"""
Function to calculate the t-statistic for any multiindex pandas data.frame
"""
def ttest_uneq(x):
  assert x.columns.get_level_values(0).isin(['mu','se','n']).all()
  idx = pd.IndexSlice
  mu_mat = x.loc[:,idx['mu']].values
  n_mat = x.loc[:,idx['n']].values
  se_mat = x.loc[:,idx['se']].values
  # Calculate t-stat
  dmu_vec = mu_mat[:,0] - mu_mat[:,1]
  var_vec = np.sum(se_mat**2 / n_mat,1)
  se_vec = np.sqrt(var_vec)
  df_vec = var_vec**2 / np.sum((se_mat**2 / n_mat)**2 / (n_mat-1),1)
  stat_vec = dmu_vec / se_vec
  pval = 2*np.minimum(stats.t(df=df_vec).cdf(stat_vec),1-stats.t(df=df_vec).cdf(stat_vec))
  res = pd.DataFrame({'stat':stat_vec, 'pval':pval, 'df':df_vec},index=x.index)
  return res


#########################################
# ----------- (1) LOAD DATA ----------- #

# (i) Load study sizes
tmp_FI = pd.read_csv(os.path.join(dir_output,'df_FI.csv'))
# (ii) Load FI results (results group by test and swap)
tmp_res = pd.read_csv(os.path.join(dir_output,'df_res.csv'))
# (iii) Load test information
df_inf = pd.read_csv(os.path.join(dir_output,'df_inf.csv'))
df = df_inf.merge(tmp_FI,on=['tt','ID']).merge(tmp_res,on=['tt','ID'])
del tmp_FI, tmp_res
# Calculate fragility quotient
df['FQ'] = df.FI / (df.num1 + df.num2)
# Put into values wide format
df_val = df.melt(cn_gg + cn_FI,cn_val,'msr')


#############################################
# ----------- (2) SUMMARY STATS ----------- #

# Remove negative (positive) FIs from bbd+phn (neg)
dat_sumstats = df_val.query('(value>0 & tt!="neg") | (value < 0 & tt=="neg")')
# Calculate summary statistics for all studies, tests, and swaps
dat_sumstats = dat_sumstats.groupby(cn_idx).value.describe()
dat_sumstats.rename(columns=dict(zip(cn_desc_lvl, cn_desc_lbl)), inplace=True)
dat_sumstats = dat_sumstats.assign(n=lambda x: x.n.astype(int)).reset_index()
dat_sumstats = dat_sumstats.sort_values(cn_idx).reset_index(None,drop=True)
dat_sumstats.to_csv(os.path.join(dir_output,'summary_stats.csv'),index=False)


###################################################
# ----------- (3) PLUM + STUDY-DESIGN ----------- #

print('---------- (3) PLUM + STUDY-DESIGN ----------')
# Different plum measures and study design
cn_plum = ['plum1','plum2','plum3']

# BBD is only study of interest (PHN has no plum data)
df_plum = df_inf[cn_gg+cn_plum].query('tt == "bbd"')
df_plum[cn_plum] = df_plum[cn_plum].astype(int)
# Merge with study design
df_plum = df_inf[cn_gg+['study_design']].merge(df_plum,'inner')
# Set order for study so t-test will be RCT - Other
df_plum['study_design'] = pd.Categorical(df_plum.study_design,['RCT','Other'])
df_plum = df_plum.melt(['tt','ID','study_design'],None,'plum')
df_plum['plum'] = df_plum.plum.str.replace('plum','').astype(int)
# Applying log transformation so distribution is more normal
df_plum['lvalue'] = np.log(df_plum.value + 1)

cn_gg_plum = ['tt','plum','study_design']
df_plum_ttest = df_plum.groupby(cn_gg_plum)['lvalue'].apply(moments_ttest,ddof=1).reset_index()
df_plum_ttest.drop(columns='level_'+str(len(cn_gg_plum)), inplace=True)
df_plum_ttest = df_plum_ttest.pivot_table(['mu','se','n'],cn_gg_plum[:-1],'study_design')
pval_plum_ttest = ttest_uneq(df_plum_ttest).reset_index()
pval_plum_ttest.to_csv(os.path.join(dir_output,'pval_plum_ttest.csv'),index=False)

# Calculate mean/median/max by different FI approaches
dat_study = df_val.query('tt!="neg"')
tmp1 = dat_study.assign(mm='all')
tmp2 = dat_study.query('value>0').assign(mm='FI>0')
dat_study = pd.concat(objs=[tmp1, tmp2], axis=0).reset_index(None,drop=True)
dat_study = dat_study.merge(df_inf[cn_gg+['study_design']])
dat_study['study_design'] = pd.Categorical(dat_study.study_design,['RCT','Other'])
dat_study = dat_study.groupby(cn_idx+['mm','study_design'])['value'].apply(moments_study).reset_index()
dat_study.drop(columns='level_'+str(len(cn_idx)+2),inplace=True)
dat_study.to_csv(os.path.join(dir_output,'dat_study.csv'),index=False)


###################################################
# ----------- (4) STATISTICAL TESTING ----------- #
print('---------- (4) STATISTICAL TESTING ----------')

# (4.A) Spearman correlation for numeric factors
df_num = df.melt(['tt']+cn_FI+cn_val, cn_num, 'metric', 'num')
df_num = df_num.melt(cn_FI+['tt','metric','num'],None,'msr','fifq')
# Remove missing values
df_num = df_num.dropna().reset_index(None,drop=True)
# Calculate spearman's test statistic
dat_pval_num = df_num.groupby(cn_idx+['metric']).apply(lambda x: rho2df(x.num.values, x.fifq.values))
dat_pval_num = dat_pval_num.reset_index().drop(columns='level_'+str(len(cn_idx)+1))
dat_pval_num.insert(0, 'feature', 'num')

# (4.B) Kruskal-Wallis test for categorical features

df_fac = df.melt(['tt']+cn_FI+cn_val, cn_fac, 'metric', 'fac')
df_fac = df_fac.melt(cn_FI+['tt','metric','fac'],None,'msr','fifq')
df_fac['fac'] = df_fac['fac'].fillna('missing')
dat_pval_fac = df_fac.groupby(cn_idx+['metric']).apply(lambda x: kruskal2df(x.fac.values, x.fifq.values))
dat_pval_fac = dat_pval_fac.reset_index().drop(columns='level_'+str(len(cn_idx)+1))
dat_pval_fac.insert(0, 'feature', 'fac')


# (4.C) Merge and adjust for multiple tests
dat_pval = pd.concat(objs=[dat_pval_num,dat_pval_fac],axis=0).reset_index(drop=True)
dat_pval['fdr'] = dat_pval.groupby(cn_idx).pval.transform(lambda x:
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


#######################################################
# ----------- (5) P-VALUE/FI RELATIONSHIP ----------- #
print('---------- (5) P-VALUE/FI RELATIONSHIP ----------')

df_rho_pval = df.melt(cn_gg+['pval_FI','pval_rep'],cn_val,'msr','fifq').query('tt!="neg"')
df_rho_pval = df_rho_pval.melt(cn_gg+['msr','fifq'],None,'sig','pval')
df_rho_pval['sig'] = df_rho_pval['sig'].str.replace('pval_','')
df_rho_pval = df_rho_pval.groupby(['tt','msr','sig']).apply(lambda x: rho2df(a=x.fifq.values, b=x.pval.values))
df_rho_pval = df_rho_pval.reset_index().drop(columns='level_3')
print(np.round(df_rho_pval,5))


################################################
# ----------- (6) PRINT STATISTICS ----------- #

print('---------- MOMENTS OF THE FI/FQ ----------')
print(np.round(dat_sumstats,2))

print('---------- STUDY DESIGN FREQUENCY ----------')
dat_study_design = df_inf[['tt','study_design']].groupby(['tt']).apply(lambda x: x['study_design'].value_counts(normalize=True)).reset_index()
dat_study_design.columns.name = ''
print(np.round(dat_study_design,2))

print('~~~ End of 3a_results_FIFQ.py ~~~')