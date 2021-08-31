

# print('---------- (4) CHECK TABLE 2 ------------')

# print(df_bbd.geo.map(di_geo_bbd).map(di_region).value_counts().reset_index())
# df_bbd['region'] = df_bbd.geo.map(di_geo_bbd).map(di_region).to_list()

# df_region = df_bbd.groupby('region').IF.apply(lambda x: pd.Series({'med':x.median(),
#         'l25':x.quantile(0.25),'l75':x.quantile(0.75)})).reset_index().round(2)
# df_region = df_region.pivot('region','level_1','IF').reset_index()
# tmp = df_region.med.astype(str) + '  (' + df_region.l25.astype(str)+'-'+df_region.l75.astype(str) + ')'
# print(pd.DataFrame({'region':df_region.region, 'val':tmp}))

# uregion = df_bbd.region.unique()
# # Kruskal wallis all way!
# IF_region = [df_bbd.IF[df_bbd.region == rr].to_list() for rr in uregion]
# print(stats.kruskal(*IF_region))

# # Test the h_index
# print(stats.kruskal(*[df_bbd.h_index[df_bbd.region == rr].to_list() for rr in uregion])[1] * 7)

# pstore = []
# for rr in uregion:
#     pstore.append(stats.kruskal(df_bbd.IF[df_bbd.region == rr].to_list(),
#                             df_bbd.IF[~(df_bbd.region == rr)].to_list())[1])
# print(pd.DataFrame({'region':uregion,
#               'sig':multitest.multipletests(pstore, alpha=0.05, method='bonferroni')[0]}))

# # Run t-test to compare FI between regions
# stats.ttest_ind(a=df_bbd.FI[df_bbd.region=='Europe'].to_list(),
#                 b=df_bbd.FI[df_bbd.region=='Africa'].to_list(),equal_var=False)

