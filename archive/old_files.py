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


# stats.spearmanr
cn_neg_num = ['IF', 'year', 'h_index', 'citation', 'weighted', 'Plum Usage']
cn_neg_fac = ['geo', 'study_design', 'type_random', 'statistician', 'funding']
df_neg_stat = df_neg_merge.merge(df_neg[['ID'] + cn_neg_num + cn_neg_fac], on='ID')
df_neg_stat[cn_neg_num] = np.where(df_neg_stat[cn_neg_num].isin(['', 'N/A']), np.NaN, df_neg_stat[cn_neg_num])
df_neg_stat[cn_neg_num] = df_neg_stat[cn_neg_num].astype(float)

for cc in cn_neg_num:
    x = df_neg_stat[cc].copy()
    y1 = df_neg_stat.FI.copy()
    y2 = df_neg_stat.FQ.copy()
    print(cc)
    print(stats.spearmanr(x[x.notnull()], y1[x.notnull()]))
    print(stats.spearmanr(x[x.notnull()], y2[x.notnull()]))

sns.scatterplot(x='IF', y='FI', data=df_neg_stat[['FI', 'IF']])

pn.options.figure_size = (10, 5)
pn.ggplot(df_neg_merge, pn.aes(x='FI')) + pn.geom_histogram(bins=15, fill='lightgray', color='blue') + \
pn.labs(y='# of papers', x='RFI') + \
pn.geom_vline(xintercept=5)

"""### Calculate for BBD studies"""

# Run the custom FI on studies with only two groups
holder_bbd = []
for ii in df_bbd_FI.index:
    n1_tot, n2_tot = df_bbd_FI.loc[ii, 'num1'], df_bbd_FI.loc[ii, 'num2']
    n1_out1, n2_out1 = df_bbd_FI.loc[ii, 'num_out1'], df_bbd_FI.loc[ii, 'num_out2']
    n1_out2, n2_out2 = n1_tot - n1_out1, n2_tot - n2_out1
    # Contigency table
    tbl_ii = [[n1_out1, n1_out2], [n2_out1, n2_out2]]
    pval_ii = stats.fisher_exact(tbl_ii)[1]
    df_bbd_FI.loc[ii, 'calc_pval'] = pval_ii
    if n1_tot < 1e3:
        di_ii = fi_func(n1A=df_bbd_FI.loc[ii, 'num_out1'], n1=df_bbd_FI.loc[ii, 'num1'],
                        n2A=df_bbd_FI.loc[ii, 'num_out2'], n2=df_bbd_FI.loc[ii, 'num2'])
    else:
        di_ii = fi_func_rev(n1A=df_bbd_FI.loc[ii, 'num_out1'], n1=df_bbd_FI.loc[ii, 'num1'],
                            n2A=df_bbd_FI.loc[ii, 'num_out2'], n2=df_bbd_FI.loc[ii, 'num2'])
    di_ii['ID'] = df_bbd_FI.loc[ii, 'ID']
    holder_bbd.append(di_ii)

# Merge results
df_bbd_results = pd.DataFrame(holder_bbd)

# Merge
df_bbd_merge = df_bbd_results.merge(df_bbd, 'left', on='ID')
# Calculate sample size
df_bbd_merge = df_bbd_merge.merge(pd.DataFrame({'ID': df_bbd_FI.ID, 'n_tot': df_bbd_FI.num1 + df_bbd_FI.num2}), 'left',
                                  on='ID')
# Calculate fragility quotient
df_bbd_merge.insert(1, 'FQ', df_bbd_merge.FI / df_bbd_merge.n_tot)

"""Calculate for PHN Studies"""

# Run the custom FI on studies with only two groups
holder_phn = []
for ii in df_phn_FI.index:
    n1_tot, n2_tot = df_phn_FI.loc[ii, 'num1'], df_phn_FI.loc[ii, 'num2']
    n1_out1, n2_out1 = df_phn_FI.loc[ii, 'num_out1'], df_phn_FI.loc[ii, 'num_out2']
    n1_out2, n2_out2 = n1_tot - n1_out1, n2_tot - n2_out1
    # Contigency table
    tbl_ii = [[n1_out1, n1_out2], [n2_out1, n2_out2]]
    pval_ii = stats.fisher_exact(tbl_ii)[1]
    df_phn_FI.loc[ii, 'calc_pval'] = pval_ii
    if (n1_tot < 1e3) & (n2_tot < 1e3):
        di_ii = fi_func(n1A=df_phn_FI.loc[ii, 'num_out1'], n1=df_phn_FI.loc[ii, 'num1'],
                        n2A=df_phn_FI.loc[ii, 'num_out2'], n2=df_phn_FI.loc[ii, 'num2'])
    else:
        di_ii = fi_func_rev(n1A=df_phn_FI.loc[ii, 'num_out1'], n1=df_phn_FI.loc[ii, 'num1'],
                            n2A=df_phn_FI.loc[ii, 'num_out2'], n2=df_phn_FI.loc[ii, 'num2'])
    di_ii['ID'] = df_phn_FI.loc[ii, 'ID']
    holder_phn.append(di_ii)

# Merge results
df_phn_results = pd.DataFrame(holder_phn)
df_phn_merge = df_phn_results.merge(df_phn[cn_int_phn + cn_float_phn], on='ID', how='left')
# Calculate fragility quotient
df_phn_merge = df_phn_merge.merge(pd.DataFrame({'ID': df_phn_FI.ID, 'n_tot': df_phn_FI.num1 + df_phn_FI.num2}), on='ID')
df_phn_merge.insert(1, 'FQ', df_phn_merge.FI / df_phn_merge.n_tot)

"""#####Write csv with FI and FQ"""

# from google.colab import drive
# drive.mount('/content/drive')
# df_bbd_merge.to_csv("/content/drive/My Drive/BBD_with_FI_FQ_20191028.csv")

"""#####Number of insignificant studies"""

print('---- BBD Studies ----\nA total of %i studies were not significant (out of %i)' %
      (sum(df_bbd_results.FI == 0), df_bbd_results.shape[0]))

print('---- PHN Studies ----\nA total of %i studies were not significant (out of %i)' %
      (sum(df_phn_results.FI == 0), df_phn_results.shape[0]))

"""## Step 4: Compare FI/FQ to different metrics"""

# Baseline FI/FQ metrics
print('---- FI Metric ----')
print(np.round(df_bbd_merge.FI.describe(), 1))

print('---- FQ Metric ----')
print(np.round(df_bbd_merge.FQ.describe(), 2))

# pn.ggplot(df_bbd_merge[['ID','FI','FQ']].melt(id_vars='ID'),pn.aes(x='value',color='variable')) + \
#   pn.geom_density() + pn.geom_histogram(bins=100) + pn.facet_wrap('~variable',scales='free')

# Numeric factors
cn_num = ['IF', 'h_index', 'citation', 'wcitation', 'plum1', 'plum2']  # 'fu_loss','pv_bl'

# Categorical factors
cn_fac = ['journal', 'geo', 'study_design', 'type_random', 'concealment',
          'blinding', 'power_just', 'outcome', 'statistician', 'funding']

print('---actual---')
print(stats.spearmanr(df_bbd_merge.FI, df_bbd_merge.pv_bl))
print(stats.spearmanr(df_bbd_merge.FQ, df_bbd_merge.pv_bl))
print('---reported---')
print(stats.spearmanr(df_bbd_merge.FI, df_bbd_merge.pval_rep))
print(stats.spearmanr(df_bbd_merge.FQ, df_bbd_merge.pval_rep))

cn_stat = ['stat_FI', 'pval_FI', 'stat_FQ', 'pval_FQ']

# --- numeric factors --- #
tmp = []
for ii, cc in enumerate(cn_num):
    stat_FI = stats.spearmanr(a=df_bbd_merge.FI.values, b=df_bbd_merge[cc].values)
    stat_FQ = stats.spearmanr(a=df_bbd_merge.FQ.values, b=df_bbd_merge[cc].values)
    tmp.append(pd.Series([cc, stat_FI[0], stat_FI[1], stat_FQ[0], stat_FQ[1]]))
    # print('p-value for variable %s: %0.3f' % (cc, stat_FI[1]))

df_num = pd.concat(tmp, axis=1).T
df_num.columns = ['feature'] + cn_stat
df_num.insert(0, 'type', 'num')

# --- categorical factors --- #
tmp = []
for ii, cc in enumerate(cn_fac):
    u_cc = df_bbd_merge[cc].unique()
    stat_FI = stats.kruskal(*[df_bbd_merge.FI[df_bbd_merge[cc] == gg].to_list() for gg in u_cc])
    stat_FQ = stats.kruskal(*[df_bbd_merge.FQ[df_bbd_merge[cc] == gg].to_list() for gg in u_cc])
    tmp.append(pd.Series([cc, stat_FI[0], stat_FI[1], stat_FQ[0], stat_FQ[1]]))
#
df_fac = pd.concat(tmp, axis=1).T
df_fac.columns = ['feature'] + cn_stat
df_fac.insert(0, 'type', 'fac')

df_pval = pd.concat([df_num, df_fac]).reset_index(drop=True)
df_pval[cn_stat] = df_pval[cn_stat].astype(float)

df_pval_long = df_pval.melt(id_vars=['type', 'feature'], var_name='tmp')
tmp = df_pval_long.tmp.str.split('_', expand=True)
df_pval_long['measure'] = tmp.iloc[:, 0]
df_pval_long['method'] = tmp.iloc[:, 1]
df_pval_long = df_pval_long.drop(columns='tmp').pivot_table(values='value', index=['type', 'feature', 'method'],
                                                            columns='measure', aggfunc=lambda x: x).reset_index()
df_pval_long.columns.name = None
df_pval_long.sort_values(by=['type'], ascending=False, inplace=True)

# Melt and FDR adjust
df_pval_long['fdr'] = multitest.fdrcorrection(pvals=df_pval_long.pval, alpha=0.1)[1]

# stat is spearman correlation coeficient for type==num and kruskal-wallis O/E for type==fac
print('--- ALL RESULTS ---')
print(df_pval_long)
print('--- SIGNIFICANT ASSOCIATIONS ---')
print(df_pval_long[df_pval_long.fdr < 0.1])

"""## Step 5: Check against discrepancies

### Which p-values are reported "too low"?
"""

# Merge the data_tables on the relevant factors
cn_both = np.intersect1d(df_phn_merge.columns, df_bbd_merge.columns)
df_both = pd.concat(
    [pd.concat([pd.DataFrame({'ds': np.repeat('phn', df_phn_merge.shape[0])}), df_phn_merge[cn_both]], axis=1),
     pd.concat([pd.DataFrame({'ds': np.repeat('bbd', df_bbd_merge.shape[0])}), df_bbd_merge[cn_both]], axis=1)],
    axis=0).reset_index(drop=True)
# Calculated inflated p-values
df_both['pval_infl'] = np.where(df_both.pval_rep - df_both.pv_bl < -0.01, 'bad', 'good')
df_both['insig'] = np.where(df_both.FI == 0, 'bad', 'good')

df_issue = df_both.groupby(['ds', 'insig', 'pval_infl']).size().reset_index().rename(columns={0: 'n'})
df_issue_geo = df_both.groupby(['ds', 'insig', 'pval_infl', 'geo']).size().reset_index().rename(columns={0: 'n'})
df_issue_geo = df_issue_geo.melt(['ds', 'n', 'geo'], var_name='type', value_name='msr')

# tmp = df_both[df_both.pval_infl == 'bad'][['ds','ID']].copy()
# [str(x)+':'+str(y) for x,y in zip(tmp.ds.to_list(),tmp.ID.to_list())]

print(stats.kruskal(df_both[df_both.pval_infl == 'good'].IF.values, df_both[df_both.pval_infl == 'bad'].IF.values))

# pn.ggplot(df_both,pn.aes(x='pval_infl',y='IF')) + pn.geom_jitter()
phat1 = 49 / 254
print('%0.3f from %0.3f to %0.3f' % (
phat1, phat1 - 2 * np.sqrt(phat1 * (1 - phat1) / 254), phat1 + 2 * np.sqrt(phat1 * (1 - phat1) / 254)))
phat2 = 73 / 254
print('%0.3f from %0.3f to %0.3f' % (
phat2, phat2 - 2 * np.sqrt(phat2 * (1 - phat2) / 254), phat2 + 2 * np.sqrt(phat2 * (1 - phat2) / 254)))

df_insig = df_issue.groupby(['ds', 'insig'])['n'].sum().reset_index()
df_insig = df_insig.merge(df_insig.groupby('ds').sum().reset_index().rename(columns={'n': 'tot'}), on='ds', how='left')
df_insig['prop'] = np.round(df_insig.n / df_insig.tot, 3)
print('insignificance')
print(df_insig)

# print('dataset size')
# print(df_both.ds.value_counts())

print('pval-hacking')
df_issue = df_issue.groupby(['ds', 'pval_infl'])['n'].sum().reset_index()
df_issue = df_issue.merge(df_issue.groupby('ds').sum().reset_index().rename(columns={'n': 'tot'}), on='ds', how='left')
df_issue['prop'] = np.round(df_issue.n / df_issue.tot, 3)
print(df_issue)
print('A total of %i had issues out of %i' % (df_issue[df_issue.pval_infl == 'bad'].n.sum(), df_issue.n.sum()))

# Correct movement
pn.ggplot(df_both[df_both.pval_infl == 'bad'], pn.aes(x='pval_rep', y='pv_bl', color='ds')) + \
pn.geom_point() + pn.scale_x_continuous(limits=(0, 0.05)) + \
pn.labs(y='Actual p-value', x='Reported p-value') + \
pn.scale_color_discrete(name=' ', labels=['BBD', 'HN']) + \
pn.geom_hline(yintercept=0.05)

pn.ggplot(df_issue.melt(id_vars=['ds', 'n']), pn.aes(x='value', y='n', fill='ds')) + \
pn.geom_col(position='stack') + pn.facet_wrap('~variable')

# Enrichment by country
pn.options.figure_size = (10, 5)
pn.ggplot(df_issue_geo, pn.aes(x='geo', y='n', fill='msr')) + \
pn.geom_bar(stat='identity', color='black') + \
pn.facet_wrap('~type') + \
pn.theme(legend_position='right', axis_text_x=pn.element_text(angle=90), axis_title_x=pn.element_blank())

df_both.head(1)

# Scatter plot in log space by ID
pn.ggplot(df_both, pn.aes(x='-np.log(pv_bl)', y='-np.log(pval_rep)')) + \
pn.geom_point() + pn.geom_abline(slope=1, intercept=0, color='blue') + \
pn.labs(x='Calculated p-value', y='Reported p-value', title='-log(p-values) actual vs reported') + \
pn.facet_wrap('~ds', labeller=pn.labeller(cols={'bbd': 'BBD', 'phn': 'HN'}))
# pn.geom_text(pn.aes(label='ID'),size=6,nudge_y=-0.2)

df_bbd_merge['issue'] = np.where(df_bbd_merge.pval_rep - df_bbd_merge.pv_bl < -0.01, 'bad', 'good')
df_geo = df_bbd_merge.groupby(['geo', 'issue']).size().reset_index().rename(columns={0: 'n'})
pn.ggplot(df_geo, pn.aes(x='geo', y='n', fill='issue')) + \
pn.geom_bar(stat='identity', position=pn.position_dodge()) + \
pn.theme(axis_text_x=pn.element_text(angle=90))

df_bbd_merge[(df_bbd_merge.issue == 'bad') & (df_bbd_merge.geo == 'Canada')]