"""
SCRIPT TO GENERATE (REVERSE) FRAILIRT INDEX FOR DIFFERENT STUDIES
"""

import os
import pandas as pd
import scipy.stats as stats

###############################
# ----- Step 1: LOAD DATA --- #
###############################

# Set directory
dir_base = os.getcwd() #'C:\\Users\\erikinwest\\Documents\\SickKids\\projects\\FragilityIndex'
os.chdir(dir_base)

# Load in the fragility index functions
import funs_fi as fi

# Load in existing processed data
df_FI = pd.read_csv(os.path.join(dir_base,'processed','df_FI.csv'))
df_inf = pd.read_csv(os.path.join(dir_base,'processed','df_inf.csv'))

####################################################
# ----- Step 2: CALCULATE FI + ACTUAL P-VALULE --- #
####################################################

holder = []
for ii, rr in df_FI.iterrows():
    n1, n1a, n2, n2a = rr['num1'], rr['num_out1'], rr['num2'], rr['num_out2']
    n1b, n2b = n1 - n1a, n2 - n2a
    tab = [[n1a,n1b], [n2a,n2b]]
    print('Study %i of %i (n=%i)' % (ii+1, df_FI.shape[0], n1+n2))
    # ---- Baseline significance ---- #
    if (n1a==0) & (n2a==0):
        pval_FI, pval_chi = 1, 1
    else:
        pval_FI, pval_chi = stats.fisher_exact(tab)[1], stats.chi2_contingency(tab)[1]
    # ---- Insignificant results ---- #
    if pval_FI > 0.05: # reverse fragility
        tmp_fi = fi.fi_func_neg(n1a, n1, n2a, n2)['FI']
        tmp_fi2 = tmp_fi
    else: # normal fragility
        if (n1+n2>2000): # run it backwards when its high
            tmp_fi = fi.fi_func_rev(n1a,n1,n2a,n2)['FI']
            tmp_fi2 = tmp_fi
        else:
            tmp_fi = fi.fi_func(n1a,n1,n2a,n2)['FI']
            tmp_fi2 = fi.fi_func2(n1a,n1,n2a,n2)['FI']
    # Save results    
    tmp = rr[0:2].append(pd.Series({'pval_FI': pval_FI, 'pval_chi':pval_chi,
                     'FI':tmp_fi,'FI2':tmp_fi2}))    
    holder.append(tmp)

# Combine
df_res = pd.concat(holder,axis=1).T
df_res.to_csv(os.path.join(dir_base,'processed','df_res.csv'),index=False)

if not df_res.shape[0] == df_FI.shape[0]:
    import sys; sys.exit('error! IDs do not line up!')
print('end of script!')


