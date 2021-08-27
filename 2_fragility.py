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
    print('Study %i of %i (ii=%i)' % (ii+1, df_FI.shape[0], n1+n2))
    
    # (i) Fisher
    print('fisher_1')
    fisher_1 = FI_func(n1A, n1, n2A, n2, 'fisher', 1, None, None, None, 0.05)
    print('fisher_2')
    if fisher_1['FI'] > 0:
        fisher_2 = FI_func(n1A, n1, n2A, n2, 'fisher', 2, None, None, None, 0.05)
    else:  # If baseline result is insig (i.e. pval>alpha), then swap=2 will have no effect
        fisher_2 = fisher_1.copy()
    
    # (ii) Chi2
    print('chi2_1_False')
    chi2_1_False = FI_func(n1A, n1, n2A, n2, 'chi2', 1, None, None, None, 0.05, False)
    print('chi2_2_False')
    if chi2_1_False['FI'] > 0:
        chi2_2_False = FI_func(n1A, n1, n2A, n2, 'chi2', 2, None, None, None, 0.05, False)
    else:
        chi2_2_False = chi2_1_False.copy()
    
    # (iii) Chi2 + Continuity
    print('chi2_1_True')
    chi2_1_True = FI_func(n1A, n1, n2A, n2, 'chi2', 1, None, None, None, 0.05, True)
    print('chi2_2_True')
    if chi2_1_True['FI'] > 0:
        chi2_2_True = FI_func(n1A, n1, n2A, n2, 'chi2', 2, None, None, None, 0.05, True)
    else:
        chi2_2_True = chi2_1_True.copy()    
    
    # (iv) Combine and store
    lst_res = [fisher_1, fisher_2, chi2_1_False, chi2_2_False, chi2_1_True, chi2_2_True]
    vec_FI = [lst['FI'] for lst in lst_res]
    vec_pvbl = [lst['pv_bl'] for lst in lst_res]
    vec_pvFI = [lst['pv_FI'] for lst in lst_res]
    res = pd.DataFrame({'test':vec_test, 'swap':vec_swap,'FI':vec_FI,'pval_bl':vec_pvbl,'pval_FI':vec_pvFI})
    res.insert(0,'ID',rr['ID'])
    res.insert(0,'tt',rr['tt'])
    
    # (v) Store and clean
    holder.append(res)
    del res, lst_res, vec_FI, vec_pvbl, vec_pvFI, fisher_1, fisher_2, chi2_1_False, chi2_2_False, chi2_1_True, chi2_2_True

# Combine
df_res = pd.concat(holder).reset_index(None,drop=True)
df_res.to_csv(os.path.join(dir_output,'df_res.csv'),index=False)

print('~~~ End of 2_fragility.py ~~~')