# Script to calculate RI for each study in sheet

# Load modules
import os
import numpy as np
import pandas as pd
import scipy.stats as stats
from funs_fragility import FI_func

dir_base = os.getcwd() 
dir_output = os.path.join(dir_base,'output')
# Load in existing processed data
df_FI = pd.read_csv(os.path.join(dir_output,'df_FI.csv'))
df_inf = pd.read_csv(os.path.join(dir_output,'df_inf.csv'))

##############################
# ----- (1) Sanity Check --- #

# Type-I error rate
alpha = 0.05

# Forward and backward shuold get the same result conditional on test/swap
n1A, n1, n2A, n2 = 160, 200, 50, 100
forward1 = FI_func(n1A, n1, n2A, n2, 'fisher', 1, mode='forward', alpha=alpha)
backward1 = FI_func(n1A, n1, n2A, n2, 'fisher', 1, mode='backward', alpha=alpha)
forward2 = FI_func(n1A, n1, n2A, n2, 'fisher', 2, mode='forward', alpha=alpha)
backward2 = FI_func(n1A, n1, n2A, n2, 'fisher', 2, mode='backward', alpha=alpha)

assert np.all(np.array(forward1['tbl_FI']) == np.array(backward1['tbl_FI']))
assert np.all(np.array(forward2['tbl_FI']) == np.array(backward2['tbl_FI']))



##############################
# ----- (2) Calculate FI --- #

vec_test = np.repeat(['fisher','chi2','chi2_cont'],2)
vec_swap = np.tile([1,2],3)

holder = []
for ii, rr in df_FI.iterrows():
    n1A, n1, n2A, n2 = rr['num_out1'], rr['num1'], rr['num_out2'], rr['num2']
    print('Study %i of %i (n=%i)' % (ii+1, df_FI.shape[0], n1+n2))
    # (i) Fisher
    fisher_1 = FI_func(n1A, n1, n2A, n2, 'fisher', 1, None, None, None, 0.05)
    fisher_2 = FI_func(n1A, n1, n2A, n2, 'fisher', 2, None, None, None, 0.05)
    # (ii) Chi2
    chi2_1_False = FI_func(n1A, n1, n2A, n2, 'chi2', 1, None, None, None, 0.05, False)
    chi2_2_False = FI_func(n1A, n1, n2A, n2, 'chi2', 2, None, None, None, 0.05, False)
    # (iii) Chi2 + Continuity
    chi2_1_True = FI_func(n1A, n1, n2A, n2, 'chi2', 1, None, None, None, 0.05, True)
    chi2_2_True = FI_func(n1A, n1, n2A, n2, 'chi2', 2, None, None, None, 0.05, True)
    # (iv) Combine and store
    lst_res = [fisher_1, fisher_2, chi2_1_False, chi2_2_False, chi2_1_True, chi2_2_True]
    vec_FI = [lst['FI'] for lst in lst_res]
    vec_pval = [lst['pv_bl'] for lst in lst_res]
    res = pd.DataFrame({'test':vec_test, 'swap':vec_swap,'FI':vec_FI,'pval':vec_pval})
    res.insert(0,'ID',rr['ID'])
    res.insert(0,'tt',rr['tt'])


    # # ---- Baseline significance ---- #
    # if (n1A==0) & (n2A==0):
    #     print('Zero events happened for either group')
    #     pval_FI, pval_chi, pval_chi2 = 1, 1, 1
    # else:
    #     pval_FI, pval_chi, pval_chi2 = stats.fisher_exact(tab)[1], \
    #                         stats.chi2_contingency(tab,correction=True)[1], \
    #                         stats.chi2_contingency(tab,correction=False)[1]
    # ---- Insignificant results ---- #
    if rr['tt'] == 'neg': # reverse fragility
        assert pval_FI > 0.05
        tmp_fi = fi.fi_func_neg(n1a, n1, n2a, n2)['FI']
        tmp_fi2 = tmp_fi.copy()
    else: # normal fragility
        if (n1+n2>2000): # run it backwards when its high
            tmp_fi = fi.fi_func_rev(n1a,n1,n2a,n2)['FI']
            tmp_fi2 = tmp_fi
        else:
            tmp_fi = fi.fi_func(n1a,n1,n2a,n2)['FI']
            tmp_fi2 = fi.fi_func2(n1a,n1,n2a,n2)['FI']
    # Save results    
    tmp = rr[0:2].append(pd.Series({'pval_FI': pval_FI, 'pval_chi':pval_chi,
                     'pval_chi2':pval_chi2,'FI':tmp_fi,'FI2':tmp_fi2}))
    holder.append(tmp)

# Combine
df_res = pd.concat(holder,axis=1).T
df_res.to_csv(os.path.join(dir_base,'processed','df_res.csv'),index=False)

if not df_res.shape[0] == df_FI.shape[0]:
    import sys; sys.exit('error! IDs do not line up!')
print('end of script!')


