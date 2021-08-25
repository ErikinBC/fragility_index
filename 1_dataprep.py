# Load modules
import os
import pandas as pd
import numpy as np
# Load support functions
import support_funs as sf

dir_base = os.getcwd() 
dir_data = os.path.join(dir_base, 'data')
dir_output = os.path.join(dir_base,'output')
sf.makeifnot(dir_output)

# Check that sheets exist
fn_excel = pd.Series(os.listdir(dir_data))
fn_excel = fn_excel[fn_excel.str.contains('xlsx')]
fn_sheets = ['BBD FI', 'Hydro FQ project', 'FI for non-significant studies']
fn_sheets = pd.Series(fn_sheets) + '.xlsx'
assert len(np.setdiff1d(fn_sheets,fn_excel))==0


#################################################
# ----- (1) BLADDER AND BOWEL DISEASE (BBD) --- #

df_bbd = pd.read_excel(os.path.join(dir_data,fn_sheets[0]))
df_bbd.rename(columns=sf.di_cn_bbd,inplace=True)
assert df_bbd[['Group 1','Group 2']].notnull().all(1).all()

# BBD specific mapping
df_bbd['journal'] = [sf.di_journal_bbd[x] for x in df_bbd.journal]
df_bbd['geo'] = [sf.di_geo_bbd[x] for x in df_bbd.geo]
df_bbd['study_design'] = [sf.di_design_bbd[x] for x in df_bbd.study_design]
df_bbd['type_random'] = [sf.di_random_bbd[x] for x in df_bbd.type_random]
df_bbd['topic'] = [sf.di_topic_bbd[x] for x in df_bbd.topic]

# Remove non-inferential columns
df_bbd.drop(columns=sf.cn_drop,errors='ignore',inplace=True)

# Extract the columns needed to calculate FI
cn_FI_bbd = ['ID'] + df_bbd.columns[df_bbd.columns.str.contains('Group\\s[1-2]$')].to_list()
df_bbd_FI = df_bbd[cn_FI_bbd].copy().astype(int)
df_bbd_FI.columns = df_bbd_FI.columns.str.replace('# pts with outcome Group ','num_out',regex=False).str.replace('Group ','num',regex=False)
df_bbd_FI.insert(0,'tt','bbd')
df_bbd.drop(columns=df_bbd.columns[df_bbd.columns.str.contains('Group')],inplace=True)
df_bbd.insert(0,'tt','bbd')


######################################
# ----- (2) HYDRONEPHROSIS (PHN) --- #

df_phn = pd.read_excel(os.path.join(dir_data,fn_sheets[1]))
df_phn.rename(columns=sf.di_cn_phn,inplace=True)
assert df_phn[['Group 1','Group 2']].notnull().all(1).all()

# Study 612 needs to have columns swapped
df_phn.loc[df_phn.ID == 612,'Group 1'] = \
    df_phn.loc[df_phn.ID == 612,'Group 1 Intervention'].to_list()[0]
df_phn.loc[df_phn.ID == 612,'Group 2'] = \
    df_phn.loc[df_phn.ID == 612,'Group 2 Intervention'].to_list()[0]
# Study 959 has unknown outcome number in group2
# Study 1166 has > 3 million patients
df_phn = df_phn[~df_phn.ID.isin([959, 1166])].reset_index(drop=True)
df_phn['ID'] = df_phn.ID.astype(int)

# PHN specific mapping
df_phn['journal'] = [sf.di_journal_phn[x] for x in df_phn.journal]
df_phn['geo'] = [sf.di_geo_phn[x] for x in df_phn.geo]
df_phn['study_design'] = [sf.di_design_phn[x] for x in df_phn.study_design]
df_phn['type_random'] = [sf.di_random_phn[x] for x in df_phn.type_random]
df_phn['topic'] = [sf.di_topic_phn[x] for x in df_phn.topic]

# Remove non-inferential columns
df_phn.drop(columns=sf.cn_drop,errors='ignore',inplace=True)

# Extract the columns needed to calculate FI
cn_FI_phn = ['ID'] + df_phn.columns[df_phn.columns.str.contains('Group\\s[1-2]$')].to_list()
df_phn_FI = df_phn[cn_FI_phn].copy().astype(int)
df_phn_FI.columns = df_phn_FI.columns.str.replace('# pts with outcome Group ','num_out',regex=False).str.replace('Group ','num',regex=False)
df_phn_FI.insert(0,'tt','phn')
# Remove from original dataframe
df_phn.drop(columns=df_phn.columns[df_phn.columns.str.lower().str.contains('group|grp')],inplace=True)
df_phn.insert(0,'tt','phn')


#######################################
# ----- (3) REVERSE FI (NEGATIVE) --- #

df_neg = pd.read_excel(os.path.join(dir_data,fn_sheets[2]))
df_neg.rename(columns=sf.di_cn_neg,inplace=True)
assert df_neg[['Group 1','Group 2']].notnull().all(1).all()
# Replace missing IDs
n_ID_neg_miss = df_neg.ID.isnull().sum()
ID_neg_replace = np.arange(999,999-n_ID_neg_miss,-1)
assert len(np.intersect1d(ID_neg_replace,df_neg.ID))==0
df_neg.loc[df_neg.ID.isnull(),'ID'] = ID_neg_replace
df_neg['ID'] = df_neg.ID.astype(int)

# Negative specific mapping
df_neg['journal'] = [sf.di_journal_neg[x] for x in df_neg.journal]
df_neg['geo'] = [sf.di_geo_neg[x] for x in df_neg.geo]
df_neg['study_design'] = [sf.di_design_neg[x] for x in df_neg.study_design]
df_neg['type_random'] = [sf.di_random_neg[x] for x in df_neg.type_random]
df_neg['topic'] = [sf.di_topic_neg[x] for x in df_neg.topic]

# Remove non-inferential columns
df_neg.drop(columns=np.intersect1d(df_neg.columns, sf.cn_drop),inplace=True)

# Extract the columns needed to calculate FI
cn_FI_neg = ['ID'] + df_neg.columns[df_neg.columns.str.contains('Group\\s[1-2]$')].to_list()
df_neg_FI = df_neg[cn_FI_neg].copy()
df_neg_FI.columns = df_neg_FI.columns.str.replace('# pts with outcome Group ','num_out',regex=False).str.replace('Group ','num',regex=False)
df_neg_FI.insert(0,'tt','neg')
df_neg.drop(columns=df_neg.columns[df_neg.columns.str.contains('Group')],inplace=True)
df_neg.insert(0,'tt','neg')


################################
# ----- (4) MERGE AND SAVE --- #

# Merge the binary outcomes for fragility index counts
df_FI = pd.concat([df_bbd_FI, df_phn_FI, df_neg_FI]).reset_index(drop=True)
cn_num = df_FI.columns[df_FI.columns.str.contains('num')]
df_FI[cn_num] = df_FI[cn_num].astype(int)

# Merge the inferential columns
df_inf = pd.concat([df_bbd, df_phn, df_neg],sort=False).reset_index(drop=True)
# Apply consistent mapping
df_inf['blinding'] = [sf.di_blinding[x] for x in df_inf.blinding]
df_inf['concealment'] = [sf.di_conceal[x] for x in df_inf.concealment]
df_inf['funding'] = [sf.di_funding[x] for x in df_inf.funding]
df_inf['outcome'] = [sf.di_outcome[x] for x in df_inf.outcome]
df_inf['power_just'] = df_inf.power_just.fillna(0) # replace NA with 0 (none)
df_inf['power_just'] = [sf.di_power[x] for x in df_inf.power_just]
df_inf['statistician'] = [sf.di_statistician[x] for x in df_inf.statistician]
# Do feature transformations for consistent comparisons
df_inf['study_design'] = np.where(df_inf.study_design.str.contains('RCT'),'RCT','Other')
# Year should be integer
df_inf['year'] = df_inf.year.astype(int)

assert np.all(df_inf.ID == df_FI.ID)

# Save
df_FI.to_csv(os.path.join(dir_output,'df_FI.csv'),index=False)
df_inf.to_csv(os.path.join(dir_output,'df_inf.csv'),index=False)

print('~~~ End of 1_dataprep.py ~~~')