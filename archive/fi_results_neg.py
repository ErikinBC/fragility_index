
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

##################################################
# ----------- (2) REVERSE FI RESULTS ----------- #

df_neg = df[df.tt == 'neg'].reset_index(drop=True)
df_neg['FQ'] = df_neg.FI / (df_neg.num1 + df_neg.num2)

print(np.round(df_neg.FI.describe(),1))
print(np.round(df_neg.FQ.describe(),2))

rho_IF = stats.spearmanr(df_neg.FI,df_neg.IF)
print('Rho: %0.3f (p-val: %0.3f) for IF-FI' % (rho_IF[0],rho_IF[1]))

thresh = 12
print('A total of %i studies have a RFI>%i and %i have <=%i' %
      (sum(df_neg.FI > thresh),thresh,sum(df_neg.FI <= thresh),thresh))





