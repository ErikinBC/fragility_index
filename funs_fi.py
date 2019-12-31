# -*- coding: utf-8 -*-
"""
SCRIPT THAT CONTAINS THE FRAGILITY INDEX FUNCTIONS
"""

import sys
import numpy as np
import scipy.stats as stats

def stopifnot(cond,msg='error! condition is not met'):
    if not cond:
        sys.exit(msg)

###############################################################################
# ------------------------ FRGARILITY INDEX FUNCTIONS ----------------------- # 
###############################################################################


# Function to calculate the fragility index
#      n1A : Number of patients in group1 with primary outcome
#      n1 : Total number of patients in group1
#      n2A : Number of patients in group2 with primray outcome
#      n2 : Total of patients in group2

# Returns a dictionary
#      FI: the fragility index
#      group: whether patients were added to group A or B
#      pv_bl: the baseline p-value from the Fisher exact test
#      pv_FI: the infimum of non-signficant p-values

def fi_func(n1A, n1, n2A, n2):
  n1B = n1 - n1A
  n2B = n2 - n2A
  stopifnot((n1B >= 0) & (n2B >= 0),'A exceeds A+B')
  prop1, prop2 = n1A / (n1A + n1B), n2A / (n2A + n2B)
  bl_pval = stats.fisher_exact([[n1A, n1B], [n2A, n2B]])[1]
  fi, fi_pval, ii = 0, 0, 0 # Initialize
  if bl_pval > 0.05: # Check that baseline result is actually significant
    di_ret = {'FI':fi,'group':'NA','pv_bl':bl_pval,'pv_FI':bl_pval}
    return(di_ret)
  while fi_pval < 0.05:
    ii += 1
    if prop1 < prop2:
      n1A += 1
      n1B += -1
    else:
      n2A += 1
      n2B += -1
    fi_pval = stats.fisher_exact([[n1A, n1B], [n2A, n2B]])[1]      
  di_ret = {'FI':ii, 'group':np.where(prop1<prop2,['A'],['B'])[0],
            'pv_bl':bl_pval, 'pv_FI':fi_pval}
  return(di_ret)

def fi_func2(n1A, n1, n2A, n2):
  n1B = n1 - n1A
  n2B = n2 - n2A
  stopifnot((n1B >= 0) & (n2B >= 0),'A exceeds A+B')
  prop1, prop2 = n1A / (n1A + n1B), n2A / (n2A + n2B)
  bl_pval = stats.fisher_exact([[n1A, n1B], [n2A, n2B]])[1]
  fi, fi_pval, ii = 0, 0, 0 # Initialize
  if bl_pval > 0.05: # Check that baseline result is actually significant
    di_ret = {'FI':fi,'group':'NA','pv_bl':bl_pval,'pv_FI':bl_pval}
    return(di_ret)
  while fi_pval < 0.05:
    ii += 1
    if prop1 > prop2:
      n1A += -1
      n1B += +1
    else:
      n2A += -1
      n2B += +1
    tab = [[n1A, n1B], [n2A, n2B]]
    fi_pval = stats.fisher_exact(tab)[1]      
  di_ret = {'FI':ii, 'group':np.where(prop1<prop2,['A'],['B'])[0],
            'pv_bl':bl_pval, 'pv_FI':fi_pval}
  return(di_ret)



# --- EQUIVALENT FUNCTION FOR REVERSE COUNTER --- #
def fi_func_rev(n1A, n1, n2A, n2):
  n1B = n1 - n1A
  n2B = n2 - n2A

  prop1 = n1A / (n1A + n1B)
  prop2 = n2A / (n2A + n2B)
  if prop1 < prop2:
    tbl = np.array([[n1A, n1B], [n2A, n2B]])
  else:
    tbl = np.array([[n2A, n2B], [n1A, n1B]])
  bl_pval = stats.fisher_exact(tbl)[1] # Calculate baseline p-value
  if bl_pval > 0.05:
    di_ret = {'FI':0,'group':'NA','pv_bl':bl_pval,'pv_FI':bl_pval}
    return(di_ret)
  # Start at equal proportion and decrease
  tbl_FI = tbl.copy()
  tbl_FI[0,0] = int(np.floor(tbl_FI[0].sum()*max(prop1,prop2)))
  tbl_FI[0,1] = tbl[0].sum() - tbl_FI[0,0]
  fi_pval = stats.fisher_exact(tbl_FI)[1]
  ii = 0
  while fi_pval > 0.05:
    ii += 1
    tbl_FI[0,0] += -1
    tbl_FI[0, 1] += 1
    fi_pval = stats.fisher_exact(tbl_FI)[1]
  # We need ii - 1 steps
  fi = (tbl_FI[0,0]+1) - tbl[0,0]
  fi_pval = stats.fisher_exact(tbl_FI + [[1,-1],[0,0]])[1]
  # Return
  di_ret = {'FI':fi, 'group':np.where(prop1<prop2,['A'],['B'])[0],
          'pv_bl':bl_pval, 'pv_FI':fi_pval}
  return(di_ret)

# --- FOR CALCULATING INSIFICANT RESULTS --- #
def fi_func_neg(n1A, n1, n2A, n2):
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
  stopifnot(bl_pval  > 0.05,'woah sig result!')
  tbl_FI = tbl.copy()
  fi_pval = 1
  ii = 0
  while fi_pval > 0.05:
    ii += 1
    tbl_FI[0,0] += k
    tbl_FI[0, 1] += -k
    fi_pval = stats.fisher_exact(tbl_FI)[1]
  di_ret = {'FI':ii,'k':k, 'pv_bl':bl_pval, 'pv_FI':fi_pval}
  return(di_ret)  


  
  
  