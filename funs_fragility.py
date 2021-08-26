import numpy as np
import scipy.stats as stats
from support_funs import stopifnot

# Wrappers for different p-value approaches
def pval_fisher(tbl, *args):
  return stats.fisher_exact(tbl,*args)[1]

def pval_chi2(tbl, *args):
  return stats.chi2_contingency(tbl,*args)[1]

def vprint(stmt, bool):
  if bool:
    print(stmt)


##############################################################################
# ------------------------ FRAGILITY INDEX FUNCTIONS ----------------------- # 
##############################################################################

"""
input: integers of the following
n1A:      Number of patients in group1 with primary outcome
n1:       Total number of patients in group1
n2A:      Number of patients in group2 with primray outcome
n2:       Total of patients in group2
statfun:  "fisher" or "chi2"
mode:     Whether while loop should begin at data (forward) or equality (backward)
swap:     Whether group1 or group2 should have the patients swapped
n1B:      Can be specified is n1 is None
n2B:      Can be specified is n2 is None
*args:    Will be passed into statsfun

output: a dictionary with the following keys
FI:       The fragility index
ineq:     Whether group1 had a proportion less than or greater than group2
swap:     Whether events were swapped from group1 or group2
pv_bl:    The baseline p-value from the Fisher exact test
pv_FI:    The infimum of non-signficant p-values
"""

# n1A, n1, n2A, n2, n1B, n2B = 480, 860, 180, 430, None, None
# statfun, swap, mode, alpha, args = 'fisher', 1, 'forward', 0.05, ()
def FI_func(n1A, n1, n2A, n2, statfun='fisher', swap=1, mode=None, n1B=None, n2B=None, alpha=0.05, *args):
  assert (swap == 1) or (swap == 2)
  assert (statfun == 'fisher') or (statfun == 'chi2')
  if statfun == 'fisher':
    pval_fun = pval_fisher
  else:
    pval_fun = pval_chi2
  if (n1B is None) or (n2B is None):
    assert (n1 is not None) and (n2 is not None)
    n1B = n1 - n1A
    n2B = n2 - n2A
  else:
    assert (n1B is not None) and (n2B is not None)
    n1 = n1A + n1B
    n2 = n2A + n2B
  lst_int = [n1A, n1, n2A, n2, n1B, n2B]
  assert all([isinstance(i,int) for i in lst_int])
  assert (n1B >= 0) & (n2B >= 0)
  prop1, prop2 = n1A / n1, n2A / n2
  # Calculate the baseline p-value
  tbl_bl = [[n1A, n1B], [n2A, n2B]]
  bl_pval = pval_fun(tbl_bl, *args)
  # Determine if we should add or subtract from n1A
  sign1 = int(np.where(prop1 > prop2, -1, +1))
  sign2 = int(np.where(prop1 > prop2, +1, -1))
  # Determine which group should be modified
  if swap == 1:
    sign2 = 0
  if swap == 2:
    sign1 = 0
  ineq = str(np.where(prop1==prop2, 'eq', np.where(prop1>prop2, 'gt', 'lt')))
  if mode is None:
    mode = 'forward'
    if n1 + n2 > 2000:
      mode = 'backward'
  # Initialize FI and p-value
  di_ret = {'FI':0, 'ineq':ineq, 'swap':swap, 'pv_bl':bl_pval, 'pv_FI':bl_pval, 'tbl_bl':tbl_bl, 'tbl_FI':tbl_bl}
  if bl_pval < alpha:  # Check that baseline result is actually significant
    FI, pval, tbl_FI = find_FI(n1A, n1B, n2A, n2B, sign1, sign2, swap, pval_fun, mode, alpha, *args)
    # Update dictionary
    di_ret['FI'] = FI
    di_ret['pv_FI'] = pval
    di_ret['tbl_FI'] = tbl_FI
  return di_ret

# Back end function to perform the for-loop
def find_FI(n1A, n1B, n2A, n2B, sign1, sign2, swap, pval_fun, mode='forward', alpha=0.05, *args):
  is_bool = False
  assert (mode == 'forward') or (mode == 'backward')
  n1a, n1b, n2a, n2b = n1A, n1B, n2A, n2B
  n1, n2 = n1A + n1B, n2A + n2B
  if mode == 'forward':
    FI, pval = 0, 0
    while pval < alpha:
      FI += 1
      vprint('Step %i of %i' % (FI, max(n1-n1A,n1-n1B)), is_bool)
      n1a += sign1 * 1
      n1b += sign1 * -1
      n2a += sign2 * 1
      n2b += sign2 * -1
      tbl = [[n1a, n1b], [n2a, n2b]]
      pval = pval_fun(tbl, *args)
  else:
    prop1 = n1A / n1
    prop2 = n2A / n2
    if swap == 1:
      n1a = int(n1 * prop2)
      n1b = n1 - n1a
    else:
      n2a = int(n2 * prop1)
      n2b = n2 - n2a
    tbl = [[n1a, n1b], [n2a, n2b]]
    pval_test = pval_fun(tbl, *args)
    rFI = 0
    while pval_test > alpha:
      rFI += 1
      vprint('Step %i of %i' % (rFI, max(n1-n1A,n1-n1B)), is_bool)
      tbl_test = [[n1a-sign1, n1b+sign1], [n2a-sign2, n2b+sign2]]
      pval_test = pval_fun(tbl_test, *args)
      if pval_test > alpha:
        n1a, n1b, n2a, n2b = tbl_test[0] + tbl_test[1]
        tbl = [[n1a, n1b], [n2a, n2b]]
        pval = pval_fun(tbl, *args)
    # Reverse calculate FI
    if swap == 1:
      FI = sign1*(n1a-n1A)
    else:
      FI = sign2*(n2a-n2A)
  assert pval > alpha
  return FI, pval, tbl



# --- FOR CALCULATING INSIFICANT RESULTS --- #
def fi_func_neg(n1A, n1, n2A, n2, alpha=0.05):
  n1B, n2B = n1 - n1A, n2 - n2A
  prop1, prop2  = n1A / (n1A + n1B), n2A / (n2A + n2B)
  # If both proportions < 50%, add to largest
  # If both proportions > 50%, subtract from smaller
  # If prop<50% - (100-prop>50%) > 0, subtract from prop<50%
  # If prop<50% - (100-prop>50%) < 0, add to prop>60%
  tbl = np.array([[n1A, n1B], [n2A, n2B]])
  if ((prop1<0.5) & (prop2<0.5)):
      if prop2 > prop1:
          tbl = tbl[[1,0]]
      k = +1
  elif ((prop1>0.5) & (prop2>0.5)):
      if prop2 < prop1:
          tbl = tbl[[1,0]]
      k = -1
  elif ((prop1<=0.5) & (prop2>=0.5)):      
      k = -1
      if prop1 - (1 - prop2) < 0:
          k = +1
          tbl = tbl[[1,0]]
  elif ((prop1>=0.5) & (prop2<=0.5)):
      k = +1
      if (1-prop1) - prop2 < 0:
          k = -1
          tbl = tbl[[1,0]]
  bl_pval = stats.fisher_exact(tbl)[1] # baseline p-value
  stopifnot(bl_pval  > alpha,'woah sig result!')
  tbl_FI = tbl.copy()
  fi_pval = 1
  ii = 0
  while fi_pval > alpha:
    ii += 1
    tbl_FI[0,0] += k
    tbl_FI[0, 1] += -k
    fi_pval = stats.fisher_exact(tbl_FI)[1]
  di_ret = {'FI':ii,'k':k, 'pv_bl':bl_pval, 'pv_FI':fi_pval}
  return(di_ret)  


  
  
  