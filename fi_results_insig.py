
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

# Keep only bbd and phn studies and remove any REPORTED significant results
df_defl = df[(df.tt.isin(['bbd','phn'])) & (df.pval_rep <= 0.05)].reset_index(drop=True)
print(df_defl.tt.value_counts())
df_defl['pval_diff'] = df.pval_FI - df.pval_rep
df_defl['pval_diff2'] = df.pval_chi - df.pval_rep
df_defl['pval_diff3'] = df.pval_chi2 - df.pval_rep
df_defl['insig'] = np.where(df_defl['FI']==0,'yes','no')

# Load in the spot checks
spotcheck = pd.read_excel(os.path.join(dir_base,'insig_study.xlsx')).rename(columns={'type':'spot'})
# Remove studies that are actually significant
spotcheck_agg = spotcheck.groupby(['tt','spot']).size().reset_index().rename(columns={0:'n'})
spotcheck_agg = spotcheck_agg[~(spotcheck_agg.spot.isin(['significant','ignore']))].reset_index()
# Remove
print(spotcheck_agg)
print(spotcheck_agg.groupby('spot').n.sum())
print(spotcheck_agg.groupby('tt').n.sum())



# qq = pd.read_excel(os.path.join(dir_base,'Hydro FQ project.xlsx'),
#         usecols=['Study ID','AUTHORS','TITLE']).rename(columns={'Study ID':'ID'})

###############################################################################
# ----------- (2) SPOT CHECK AND FIX INSIG RESULTS WHERE RELEVANT ----------- #

for ii, rr in qq[qq.ID.isin(df_defl[(df_defl.FI == 0) & (df_defl.tt == 'phn')].ID.to_list())].iterrows():
    print('-------------')
    print(rr['ID']); print(rr['AUTHORS']); print(rr['TITLE'])
    print('-------------')


for ii, rr in df_defl[df_defl.FI == 0].sort_values(['tt','ID']).reset_index(drop=True).iterrows():
    tt, ID = rr['tt'],rr['ID']
    print('\n')
    print('---- Type: %s, ID: %s ----' % (tt, ID) )
    print(rr[['num1','num2','num_out1','num_out2']])
    print('\n')

for i in range(1):
    # ---- Type: bbd, ID: 40 ----
    print(stats.fisher_exact([[19,23-19],[12,23-12]])) # 6-month
    print(stats.fisher_exact([[4,23-4],[13,23-13]])) # 6-month (abstract typo)
    print(stats.fisher_exact([[13,23-13],[6,23-6]])) # 12-month
    # ---- Type: bbd, ID: 674 ----
    print(stats.fisher_exact([[2,5],[6,1]]))
    print(stats.chi2_contingency([[2,5],[6,1]],correction=False))
    # ---- Type: bbd, ID: 6577 ----
    print(stats.fisher_exact([[9,8+2],[68,28+9]])[1]) # full vs partial+no
    print(stats.fisher_exact([[9,8],[68,28]])[1]) # full vs partial
    print(stats.chi2_contingency([[9,8,2],[68,28,9]])[1])
    # ---- Type: bbd, ID: 16898 ----
    print(stats.fisher_exact([[9,50-9],[3,50-3]])) # insig 3-months
    print(stats.chi2_contingency([[9,50-9],[3,50-3]],correction=False)) # insig 3-months
    print(stats.fisher_exact([[9,50-9],[1,50-1]])) # sig 6 months
    # ---- Type: bbd, ID: 21436 ----
    print(stats.fisher_exact([[4,13],[11,7]]))
    # ---- Type: bbd, ID: 26684 ----
    print(stats.fisher_exact([[17,44-17],[9,45-9]]))
    # ---- Type: bbd, ID: 30660 ----
    print(stats.fisher_exact([[16,26-16],[26,30 - 26]]))
    print(stats.chi2_contingency([[16,26-16],[26,30 - 26]],correction=False))
    # ---- Type: bbd, ID: 31326 ----
    print(stats.fisher_exact([[8,0],[9,15]]))
    print(stats.fisher_exact([[8,0],[0,3]]))
    # ---- Type: bbd, ID: 31327 ----
    print(stats.fisher_exact([[42,74],[58,26]]))
    print(stats.fisher_exact([[42,58],[74,26]]))
    # ---- Type: bbd, ID: 31616 ----
    print(stats.fisher_exact([[1,16-1],[3,18-3]]))
    print(stats.fisher_exact([[5,16-5],[8,18-8]]))
    # ---- Type: bbd, ID: 34111 ----
    print(stats.fisher_exact([[4, 36], [10, 28]]))
    # ---- Type: bbd, ID: 34240 ----
    print(stats.chi2_contingency([[15,143],[25,120]],False)[1])
    # ---- Type: bbd, ID: 34442 ----
    print(stats.chi2_contingency([[125, 292-125], [54, 158-54]], False)[1])
    # ---- Type: bbd, ID: 34688 ----
    print(stats.fisher_exact([[30, 36-30], [(26+21+20), 33*3-(26+21+20)]]))
    print(stats.fisher_exact([[30, 36 - 30], [20, 33 - 20 ]]))
    # ---- Type: bbd, ID: 34807 ----
    print(stats.chi2_contingency([[54, 70-54], [34, 55-34]],False)[1])
    # ---- Type: bbd, ID: 34906 ----
    print(stats.fisher_exact([[45, 54-45], [35, 60-35]]))
    # ---- Type: bbd, ID: 35024 ----
    # ---- Type: bbd, ID: 35747 ----
    print(stats.fisher_exact([[31, 57 - 31], [3, 26 - 3]]))
    # ---- Type: bbd, ID: 35856 ----
    print(stats.chi2_contingency([[5, 15-5], [4, 38-4]],False)[1])

for ii in range(1):
    # ---- Type: phn, ID: 34 ----
    # ---- Type: phn, ID: 268 ----
    # ---- Type: phn, ID: 410 ----
    print(stats.chi2_contingency([[83, 83-0], [83,83-4]], False)[1])
    # ---- Type: phn, ID: 424 - ---
    print(stats.fisher_exact([[20, 20-4], [20,20-1]]))
    # ---- Type: phn, ID: 432 ----
    print(stats.chi2_contingency([[32,131,45,78], [273 - 32, 1260 - 131, 274 - 45, 1377 - 78]])[1])
    print(stats.chi2_contingency([[32, 131], [273 - 32, 1260 - 131]])[1])
    # ---- Type: phn, ID: 456 ----
    print(stats.chi2_contingency([[21,33-21], [30,35-30]],False))
    # ---- Type: phn, ID: 469 ----
    print(stats.chi2_contingency([[12,18-12], [37,49-37]], False))
    # ---- Type: phn, ID: 496 - ---
    print(stats.chi2_contingency([[10, 47-10], [3,46-3]], False))
    # ---- Type: phn, ID: 613 ----
    print(stats.chi2_contingency([[24,6,41], [53-24,20-6,62-41]]))
    print(stats.chi2_contingency([[20, 8, 10], [53 - 20, 20 - 8, 62 - 10]]))
    # ---- Type: phn, ID: 726 - ---
    print(stats.chi2_contingency([[25, 31], [34-25,34-31]], False))
    print(stats.chi2_contingency([[25, 31], [34 - 25, 34 - 31]], True))
    # ---- Type: phn, ID: 776 ----
    print(stats.chi2_contingency([[22, 25], [26-22, 25-25]], False))
    # ---- Type: phn, ID: 904 ----
    print(stats.chi2_contingency([[16, 25], [44 - 16, 42 - 25]], False))
    # ---- Type: phn, ID: 941 ----
    print(stats.chi2_contingency([[109, 17], [112-109, 19 - 17]], False))
    # ---- Type: phn, ID: 1037 ----
    print(stats.chi2_contingency([[5, 7], [7 -5, 9 - 7]], False))
    # ---- Type: phn, ID: 1047 ----
    # ---- Type: phn, ID: 1049 - ---
    # ---- Type: phn, ID: 1133 ----
    print(stats.chi2_contingency([[3, 6], [45-3, 45-6]], False))
    # ---- Type: phn, ID: 1201 ----
    print(stats.fisher_exact([[17, 35], [43-17, 56-35]]))
    print(stats.fisher_exact([[17, 33], [43 - 17, 56 - 33]]))
    # ---- Type: phn, ID: 1273 ----
    print(stats.chi2_contingency([[21, 21], [30 - 21, 23 - 21]],False))
    # ---- Type: phn, ID: 1286 ----
    print(stats.fisher_exact([[9, 29], [88 - 9, 117 - 29]]))
    # ---- Type: phn, ID: 1473 - ---
    print(stats.chi2_contingency([[20, 12], [28 - 20, 28 - 12]],False))
    # ---- Type: phn, ID: 1572 - ---
    print(stats.chi2_contingency([[12, 1], [18 - 12, 5 - 1]], False))
    # ---- Type: phn, ID: 1702 ----
    print(stats.chi2_contingency([[17, 3], [56-17, 29-3]], False))
    # ---- Type: phn, ID: 1950 ----
    print(stats.chi2_contingency([[12, 8], [25 - 12, 38 - 8]], True))
    # ---- Type: phn, ID: 1973 ----
    print(stats.chi2_contingency([[3, 10], [26 - 3, 26 - 10]], False))
    # ---- Type: phn, ID: 2293 ----
    print(stats.fisher_exact([[15, 22], [8, 1]]))
    # ---- Type: phn, ID: 2405 ----
    # ---- Type: phn, ID: 2437 ----
    # ---- Type: phn, ID: 2745 - ---
    print(stats.chi2_contingency([[45, 40], [5, 1]], False))

#####################################################
# ----------- (3) INSIGNIFICANT RESULTS ----------- #

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

