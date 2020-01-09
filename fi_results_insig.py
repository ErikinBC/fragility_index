
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

#####################################################
# ----------- (2) INSIGNIFICANT RESULTS ----------- #

# Keep only bbd and phn studies and remove any REPORTED significant results
df_defl = df[(df.tt.isin(['bbd','phn'])) & (df.pval_rep <= 0.05)].reset_index(drop=True)
print(df_defl.tt.value_counts())
df_defl['pval_diff'] = df.pval_FI - df.pval_rep
df_defl['pval_diff2'] = df.pval_chi - df.pval_rep
df_defl['pval_diff3'] = df.pval_chi2 - df.pval_rep
df_defl['insig'] = np.where(df_defl['FI']==0,'yes','no')

# --- INSIGNIFICANT ONLY --- #
cn_defl = ['tt','ID','pval_FI','pval_chi','pval_chi2','pval_rep']
df_defl_long = df_defl[cn_defl].melt(['tt','ID','pval_rep'],
                var_name='test',value_name='pval_act')
df_defl_long.test = df_defl_long.test.str.replace('pval_','')
dat_insig = df_defl_long.groupby(['tt','test']).pval_act.apply(lambda x: sum(x > 0.05)).reset_index()
dat_insig = dat_insig.rename(columns={'pval_act':'n'}).sort_values('test').reset_index(drop=True)
print(dat_insig)
print(np.round(dat_insig.groupby('test').n.apply(lambda x:
        pd.Series({'prop':sum(x)/df_defl.tt.shape[0],'n':sum(x)})).reset_index(),2))

# FI of all Yates-correction papers
df_yates = df_defl[(df_defl.pval_chi2 < 0.05) & (df_defl.pval_FI>0.05)][['tt','ID']].merge(
    df_defl[['tt','ID','pval_chi2','num1','num2','num_out1','num_out2']],
    on=['tt','ID'],how='left')

df_yates['FI'] = df_yates.apply(lambda x: fi.fi_func_yates(n1A=x['num_out1'],n1=x['num1'],
                                    n2A=x['num_out2'],n2=x['num2'])['FI'],axis=1)
print(df_yates)

cn_num = ['IF','h_index','citation','wcitation','plum1','plum2']
cn_fac = ['journal', 'geo', 'study_design', 'type_random', 'concealment',
          'blinding', 'power_just', 'outcome', 'statistician', 'funding']

df_num = df_defl[['tt','insig'] + cn_num].melt(['tt','insig'],var_name='metric')
df_num = df_num[df_num.value.notnull()].reset_index(drop=True)
dat_pval_num = df_num.groupby(['tt','metric']).apply(lambda x:
    pd.Series({'pval': stats.mannwhitneyu(*[x['value'][x['insig']==yy] for yy in x['insig'].unique()])})).reset_index()
dat_pval_num = pd.concat([dat_pval_num.drop(columns='pval'),
    pd.DataFrame([[x.statistic, x.pvalue] for x in dat_pval_num.pval],
                        columns=['stat','pval'])],axis=1)
dat_pval_num.insert(0, 'feature', 'num')

df_cat = df_defl[['tt','insig'] + cn_fac].melt(['tt','insig'],var_name='metric')
dat_pval_cat = df_cat.groupby(['tt','metric']).apply(lambda x:
        pd.Series({'pval':stats.chi2_contingency(pd.crosstab(x['insig'],x['value']))})).reset_index()
dat_pval_cat = pd.concat([dat_pval_cat.drop(columns='pval'),
    pd.DataFrame([[x[0], x[1]] for x in dat_pval_cat.pval],
                        columns=['stat','pval'])],axis=1)
dat_pval_cat.insert(0, 'feature', 'cat')

dat_pval = pd.concat([dat_pval_num,dat_pval_cat]).reset_index(drop=True)
dat_pval['fdr'] = dat_pval.groupby('tt').pval.transform(lambda x:
            multitest.fdrcorrection(pvals=x,alpha=0.1)[1])
print(dat_pval[dat_pval.fdr < 0.1])

#print(df_defl.groupby(['tt','insig']).IF.describe())
#df_defl[(df_defl.insig == 'yes') & (df_defl.tt == 'bbd')][['ID']].to_list()

print(df[df.ID == 35856].T)


##################################################
# ----------- (3) DEFLATED P-VALUES  ----------- #

# --- INFLATED OR INSIGNIFICANT --- #
df_infl = df_defl[df_defl.pval_diff > 0.01].reset_index(drop=True)

print(pd.cut(x=df_infl.pval_rep,
       bins=[0,0.001,0.01,0.05],labels=['<0.001','<0.01','<0.05']).value_counts())

