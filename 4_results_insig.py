# Analyze results with insignificant findings

# Load modules
import os
import pandas as pd
import numpy as np
from mizani.formatters import percent_format
import scipy.stats as stats
import plotnine as pn

dir_base = os.getcwd()
dir_output = os.path.join(dir_base,'output')
dir_data = os.path.join(dir_base,'data')

alpha = 0.05

def fisher(tbl):
    return stats.fisher_exact(tbl)[1]

def pval_min(tbl):
    pval_fisher = stats.fisher_exact(tbl)[1]
    pval_yates = stats.chi2_contingency(tbl,correction=True)[1]
    pval_chi2 = stats.chi2_contingency(tbl,correction=False)[1]
    pval = np.min([pval_fisher, pval_yates, pval_chi2])
    return pval

def write_excel(df, path):
    if not os.path.exists(path):
        print('Writing excel')
        df.to_excel(path,index=False)

cn_gg = ['tt','ID']

################################################
# ----------- (1) LOAD IN THE DATA ----------- #

# (i) Load the previous processsed data and results
df_FI = pd.read_csv(os.path.join(dir_output,'df_FI.csv'))
df_inf = pd.read_csv(os.path.join(dir_output,'df_inf.csv'))
df_res = pd.read_csv(os.path.join(dir_output,'df_res.csv'))
df_res = df_res.query('tt != "neg"')
# Negative FI implies study was insignificant at baseline
assert df_res.query('FI<0').pval_bl.min() > alpha
# Every study should have the same test/swap measurements
assert np.all(df_res.groupby(cn_gg).size() == 6)
df_res = df_res.assign(insig_bl=lambda x: np.where(x.pval_bl > alpha, 1, 0))

# Combine
df = df_inf.merge(df_FI,'inner',on=cn_gg)
df = df.merge(df_res,'inner',on=cn_gg)

# (ii) Load titles
fn_sheets = ['BBD FI', 'Hydro FQ project']
fn_sheets = pd.Series(fn_sheets) + '.xlsx'
di_sheets = dict(zip(fn_sheets, ['bbd', 'phn']))
holder = []
for sheet in fn_sheets:
    cn = pd.read_excel(os.path.join(dir_data,sheet),nrows=1).columns
    cn = list(cn[cn.str.contains('^ID|ID$',regex=True,case=False)]) + ['TITLE']
    tmp_df = pd.read_excel(os.path.join(dir_data,sheet),usecols=cn)
    tmp_df.columns = ['ID', 'title']
    tmp_df.insert(0,'tt',di_sheets[sheet])
    holder.append(tmp_df)
dat_title = pd.concat(objs=holder,axis=0)
dat_title = dat_title.assign(ID=lambda x: x.ID.astype(int))

# (iii) Subset to fisher and swap == 1
res_fisher = df_res.query('test == "fisher" & swap==1')
res_fisher.drop(columns=['test','swap'], inplace=True)
res_fisher = dat_title.merge(res_fisher,'inner')


#########################################
# ----------- (2) chi2 test ----------- #

cn_test = ['chi2_cont','fisher']

# (i) Find list of fisher insig studies
dat_insig = res_fisher.query('insig_bl==1')[cn_gg].reset_index(None,drop=True)

# (ii) Determine whether chi2 can account for significance
dat_chi2_insig = df_res.merge(dat_insig).pivot_table('insig_bl',cn_gg,'test')
# If fisher is insignificant, chi2 with continuity is as well
assert dat_chi2_insig[cn_test].all().all()
dat_chi2_insig = dat_chi2_insig.drop(columns=cn_test).reset_index()
print(dat_chi2_insig.groupby(['chi2','tt']).size())

# Save data to be spot checked (ones that are still insignificant)
tmp = dat_chi2_insig.merge(dat_title).query('chi2==1')
tmp = tmp.sort_values(cn_gg).reset_index(None,drop=True)
path_spot = os.path.join(dir_output,'insig_spot.xlsx')
write_excel(tmp, path_spot)


###########################################
# ----------- (3) MANUAL SPOT ----------- #

dat_manual = \
 [pd.Series({'tt':'bbd', 'ID':40, 'pval':pval_min([[19,23-19],[13,23-13]]), 'notes':'insig'}),
 pd.Series({'tt':'bbd', 'ID':1302, 'pval':pval_min([[17,31-17],[20,33-20]]), 'notes':'reported insig'}),
 pd.Series({'tt':'bbd', 'ID':6577, 'pval':pval_min([[9,19-9],[68,105-68]]), 'notes':'insig'}),
 # Using t-test rather than binary outcome
 pd.Series({'tt':'bbd', 'ID':26684, 'pval':np.nan, 'notes':'specification'}),
 # We defined normal as completely dry, whereas paper had completely dry + good response. Fragile.
 pd.Series({'tt':'bbd', 'ID':31326, 'pval':pval_min([[8,8-8],[9,27-9]]), 'notes':'specification'}),
 # Our issue: Fisher’s should be sig: stats.fisher_exact([[42,58],[74,26]]), change denominator
 pd.Series({'tt':'bbd', 'ID':31327, 'pval':pval_min([[42,58],[74,26]]), 'notes':'self'}),
 # Compared mean number change instead of table 2
 pd.Series({'tt':'bbd', 'ID':31616, 'pval':np.nan,'notes':'specification'}),
 # No difference with control's grouped: pval_min([[10,38-10],[15,39-15]]) and pval_min([[10,38-10],[32,75-32]]), but paper states "At follow up... no statistical significant differences"
 pd.Series({'tt':'bbd', 'ID':34111, 'pval':np.nan, 'notes':'reported insig'}),
 pd.Series({'tt':'bbd', 'ID':34442, 'pval':pval_min([[125,292-125],[54,158-54]]), 'notes':'insig'}),
 pd.Series({'tt':'bbd', 'ID':34807, 'pval':pval_min([[54,70-54],[34,55-34]]), 'notes':'insig'}),
 pd.Series({'tt':'bbd', 'ID':34906, 'pval':np.nan, 'notes':'self'}),
 pd.Series({'tt':'bbd', 'ID':35024, 'pval':np.nan, 'notes':'non-replicable'}),
 pd.Series({'tt':'bbd', 'ID':35747, 'pval':np.nan, 'notes':'self'}),
 pd.Series({'tt':'phn', 'ID':268, 'pval':np.nan, 'notes':'non-replicable'}),
 # Table 1: Urinary tract infection or Hematuria (n)
 pd.Series({'tt':'phn', 'ID':424, 'pval':pval_min([[1,20-1],[4,20-4]]),'notes':'insig'}), 
 pd.Series({'tt':'phn', 'ID':432, 'pval':np.nan, 'notes':'self'}),
 pd.Series({'tt':'phn', 'ID':469, 'pval':pval_min([[12,18-12],[37,49-37]]), 'notes':'insig'}),
 # Table 1: Silic vs Dx/HA, p-value = 0.015, pval_min([[50,61-50],[11,20-11]]),     
 pd.Series({'tt':'phn', 'ID':613, 'pval':np.nan, 'notes':'self' }),
 # The stone-free rate was 73.5% for the RIRS group and 91.2% for the PCNL group after a single procedure 
 pd.Series({'tt':'phn', 'ID':726, 'pval':pval_min([[25,34-25],[31,34-31]]),'notes':'insig'}),
 # Table 1: Cannot get to 89%
 pd.Series({'tt':'phn', 'ID':941, 'pval':np.nan, 'notes':'non-replicable'}),
 # The pathologist correctly assigned the cause of obstruction...
 pd.Series({'tt':'phn', 'ID':1037, 'pval':pval_min([[5,7-5],[7,9-7]]),'notes':'insig'}),
 # Table 1 is sig
 pd.Series({'tt':'phn', 'ID':1047, 'pval':np.nan, 'notes':'self'}),
 # Leakage of anastomosis with early reinsertion of stent
 pd.Series({'tt':'phn', 'ID':1133, 'pval':pval_min([[3,45-3],[6,45-6]]), 'notes':'insig'}),
 pd.Series({'tt':'phn', 'ID':1201, 'pval':np.nan, 'notes':'self'}),
 # Recal scare % does not make sense relative to n=88 for example
 pd.Series({'tt':'phn', 'ID':1286, 'pval':np.nan, 'notes':'non-replicable'}),
 # Cannot identify where numbers come from (66.7% versus 20.0%)
 pd.Series({'tt':'phn', 'ID':1702, 'pval':np.nan, 'notes':'non-replicable'}),
 # Comparing crossing vessels only
 pd.Series({'tt':'phn', 'ID':2293, 'pval':np.nan, 'notes':'self'}),
 # Does not have p-values
 pd.Series({'tt':'phn', 'ID':2405, 'pval':np.nan, 'notes':'self'}),
 # Combining extravesical uni + bilateral leads to insiginficant
 pd.Series({'tt':'phn', 'ID':2437, 'pval':np.nan, 'notes':'specification'}),
 # Table 4: no with side effects pval_min([[12,50-12],[21,41-21]])
 pd.Series({'tt':'phn', 'ID':2745, 'pval':np.nan, 'notes':'self'})]
# Merge and clean
dat_manual = pd.concat(objs=dat_manual,axis=1).T
dat_manual['pval'] = dat_manual['pval'].astype(float)
dat_manual['ID'] = dat_manual['ID'].astype(int)
dat_manual.notes.value_counts()


#######################################
# ----------- (4) RESULTS ----------- #

# Combine chi2 with manual
tmp1 = dat_chi2_insig.query('chi2==0').drop(columns='chi2').assign(notes='chi2')
tmp2 = df_res.query('test=="chi2" & swap==1')[cn_gg+['pval_bl']]
tmp3 = tmp1.merge(tmp2).rename(columns={'pval_bl':'pval'})
# Get accounting
df_acc = pd.concat(objs=[dat_manual,tmp3],axis=0)
df_acc['notes'] = pd.Categorical(df_acc.notes,['chi2','insig','specification','non-replicable','reported insig','self'])
df_acc = df_acc.sort_values(['notes']+cn_gg).reset_index(None,drop=True)
df_acc.to_csv(os.path.join(dir_output,'df_acc.csv'),index=False)

drop_notes = ['self','reported insig']

acc_tt = df_acc.groupby(['notes','tt']).size().reset_index()
acc_tt = acc_tt.query('~notes.isin(@drop_notes)').rename(columns={0:'n'})
acc_tt = acc_tt.merge(acc_tt.groupby('notes').n.sum().reset_index().rename(columns={'n':'n_notes'}))
acc_tt = acc_tt.assign(n_tot=lambda x: x.n.sum())

print(acc_tt)
print(acc_tt.groupby('tt').n.sum())


#######################################
# ----------- (5) FIGURES ----------- #



di_tt = {'bbd':'BBD','phn':'HN'}
tmp = res_fisher.merge(df_inf[cn_gg+['pval_rep']])
tmp = tmp.query('pval_rep <= 0.05')
tmp.tt = tmp.tt.map(di_tt)

# (i) Reported versus actual p-value
gg_rep_act = (pn.ggplot(tmp, pn.aes(x='pval_rep',y='pval_bl',color='tt')) + 
    pn.theme_bw() + pn.geom_point() + 
    pn.labs(y="Calculated (Fisher's Exact)",x='Reported') + 
    pn.ggtitle('P-values') + 
    pn.geom_hline(yintercept=alpha, linetype='--') + 
    pn.scale_color_discrete(name='Literature'))
gg_rep_act.save(os.path.join(dir_output,'gg_rep_act.png'),width=8,height=4)


di_notes = {'chi2':'χ2-correction', 'insig':'Erroneous', 'specification':'Specification','non-replicable':'Inconsistent'}
# (ii) Breakdown of counts
tmp = acc_tt.merge(res_fisher.tt.value_counts().reset_index().rename(columns={'index':'tt','tt':'n_lit'}))
tmp = tmp.assign(tt=lambda x: x.tt.map(di_tt), notes=lambda x: x.notes.map(di_notes), share=lambda x: x.n/x.n_lit)

gg_acc_notes = (pn.ggplot(tmp,pn.aes(x='notes',y='share',fill='tt')) + 
    pn.theme_bw() + 
    pn.scale_y_continuous(labels=percent_format(),limits=[0,0.1]) + 
    pn.scale_fill_discrete(name='Literature') + 
    pn.geom_col(color='black',position=pn.position_dodge(0.5),width=0.5) + 
    pn.labs(y='Percent',x='Investigation') + 
    pn.theme(axis_text_x=pn.element_text(angle=45),axis_title_x=pn.element_blank()))
gg_acc_notes.save(os.path.join(dir_output,'gg_acc_notes.png'),width=7,height=3)


print('~~~ End of 4_results_insig.py ~~~')