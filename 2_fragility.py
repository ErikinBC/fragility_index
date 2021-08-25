import os
import pandas as pd
import scipy.stats as stats
import funs_fragility as fi

dir_base = os.getcwd() 
dir_output = os.path.join(dir_base,'output')
# Load in existing processed data
df_FI = pd.read_csv(os.path.join(dir_output,'df_FI.csv'))
df_inf = pd.read_csv(os.path.join(dir_output,'df_inf.csv'))


####################################
# ----- CALCULATE FI + P-VALUE --- #

holder = []
for ii, rr in df_FI.iterrows():
    n1, n1a, n2, n2a = rr['num1'], rr['num_out1'], rr['num2'], rr['num_out2']
    n1b, n2b = n1 - n1a, n2 - n2a
    tab = [[n1a,n1b], [n2a,n2b]]
    if (ii + 1) % 50 == 0:
        print('Study %i of %i (n=%i)' % (ii+1, df_FI.shape[0], n1+n2))
    # ---- Baseline significance ---- #
    if (n1a==0) & (n2a==0):
        print('Zero events happened for either group')
        pval_FI, pval_chi, pval_chi2 = 1, 1, 1
    else:
        pval_FI, pval_chi, pval_chi2 = stats.fisher_exact(tab)[1], \
                            stats.chi2_contingency(tab,correction=True)[1], \
                            stats.chi2_contingency(tab,correction=False)[1]
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


