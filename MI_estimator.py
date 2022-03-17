# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 13:42:14 2020

@author: Tomer Fishman
"""
# %% libraries and load dimensions

from os import chdir
import pandas as pd
import seaborn as sns
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

chdir('C:\\Users\\Tomer\\Dropbox\\-the research\\2020 10 IIASA\\MI_project\\git\\MaterialIntensityEstimator')

dims_structure_import = pd.read_excel("data_input_and_ml_processing\\dims_structure.xlsx", sheet_name="dims_structure")

dims_names = list(dims_structure_import.columns)

# HINT remove unused dimensions
dims_names = dims_names[7:]

dims_list = []
# dims_len = []

for dim_x in dims_names:
    # calculate the number of entities in the dimension
    dim_lastvalidrow = dims_structure_import[dim_x].last_valid_index() + 1
    dims_list += [list(dims_structure_import[dim_x][2:dim_lastvalidrow])]

# HINT removed IN 'informal' because there are simply not enough datapoints for meaningful estimations, consider including later
dims_list[0] = dims_list[0][1:]

# %% load the MI database with const. type ML results from Orange

materials = ['concrete', 'steel', 'wood', 'brick']

buildings_import = pd.read_excel("data_input_and_ml_processing\\buildings_v2-const_type_ML.xlsx", sheet_name="Sheet1")

# create new column const_short where U from 'Construction type' is replaced by 'Random Forest'
buildings_import['const_short'] = buildings_import['Random Forest'].where((buildings_import['Construction type'].str.match('U')), buildings_import['Construction type'])

# clean up buildings_import
buildings_import = buildings_import[['id'] + materials + dims_names]

# # SSP 5 regions
# buildings_import['R5'] = buildings_import['R5_32'].str.split('_').str[0]

# %% EDA: database plots


# violin plots https://seaborn.pydata.org/generated/seaborn.violinplot.html
sns.violinplot(x="concrete", y="const_short", data=buildings_import, cut=0, linewidth=1).legend_.remove()
sns.violinplot(x="concrete", y="const_short", hue="use_short", data=buildings_import, cut=0, linewidth=1, scale="width")
sns.violinplot(x="const_short", y="concrete", hue="use_short", data=buildings_import, cut=0, linewidth=.5, scale="width", bw=.1, height=2, aspect=1)
sns.catplot(x="const_short", y="concrete", hue="use_short", kind="violin", data=buildings_import, cut=0, linewidth=1, scale="width", bw=.15, height=8, aspect=1.8)
sns.catplot(x="use_short", y="concrete", hue="const_short", kind="violin", data=buildings_import, cut=0, linewidth=1, scale="width", bw=.15, height=8, aspect=1.8)
sns.catplot(x="use_short", y="concrete", row="const_short", kind="violin", data=buildings_import, cut=0, linewidth=1, scale="width", bw=.2, height=3, aspect=6)

sns.catplot(x="use_short", y="concrete", col="const_short", kind="violin", data=buildings_import, cut=0, linewidth=1, scale="width", bw=.2, height=3, aspect=1.2)
sns.catplot(x="use_short", y="steel", col="const_short", kind="violin", data=buildings_import.query('steel < 450'), cut=0, linewidth=1, scale="width", bw=.2, height=3, aspect=1.2)
sns.catplot(x="use_short", y="wood", col="const_short", kind="violin", data=buildings_import.query('wood < 300'), cut=0, linewidth=1, scale="width", bw=.2, height=3, aspect=1.2)
sns.catplot(x="use_short", y="brick", col="const_short", kind="violin", data=buildings_import, cut=0, linewidth=1, scale="width", bw=.2, height=3, aspect=1.2)

sns.catplot(x="const_short", y="concrete", col="use_short", kind="violin", data=buildings_import, cut=0, linewidth=1, scale="width", bw=.2, height=3, aspect=1.2)
sns.catplot(x="const_short", y="steel", col="use_short", kind="violin", data=buildings_import.query('steel < 450'), cut=0, linewidth=1, scale="width", bw=.2, height=3, aspect=1.2)
sns.catplot(x="const_short", y="wood", col="use_short", kind="violin", data=buildings_import.query('wood < 300'), cut=0, linewidth=1, scale="width", bw=.2, height=3, aspect=1.2)
sns.catplot(x="const_short", y="brick", col="use_short", kind="violin", data=buildings_import, cut=0, linewidth=1, scale="width", bw=.2, height=3, aspect=1.2)

sns.catplot(x="use_short", y="concrete", col="const_short", row="R5", kind="violin", data=buildings_import, cut=0, linewidth=1, scale="width", bw=.2, height=3, aspect=1.2)
sns.catplot(x="use_short", y="steel", col="const_short", row="R5", kind="violin", data=buildings_import.query('steel < 450'), cut=0, linewidth=1, scale="width", bw=.2, height=3, aspect=1.2)
sns.catplot(x="const_short", y="steel", col="use_short", row="R5", kind="violin", data=buildings_import.query('steel < 450'), cut=0, linewidth=1, scale="width", bw=.2, height=3, aspect=1.2)

# bivariate distribution plots https://seaborn.pydata.org/tutorial/distributions.html#visualizing-bivariate-distributions
kdebw = .6
scattersize = 120
scatteralpha = .6
sns.jointplot(data=buildings_import, x="concrete", y="steel", hue="const_short", linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['concrete']), ndigits=-2)),
              ylim=(0, round(max(buildings_import['steel']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))
sns.jointplot(data=buildings_import, x="concrete", y="wood", hue="const_short", linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['concrete']), ndigits=-2)),
              ylim=(0, round(max(buildings_import['wood']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))
sns.jointplot(data=buildings_import, x="concrete", y="brick", hue="const_short", linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['concrete']), ndigits=-2)),
              ylim=(0, round(max(buildings_import['brick']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))

sns.jointplot(data=buildings_import, x="steel", y="brick", hue="const_short", linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['steel']), ndigits=-2)),
              ylim=(0, round(max(buildings_import['brick']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))
sns.jointplot(data=buildings_import, x="steel", y="wood", hue="const_short", linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['steel']), ndigits=-2)),
              ylim=(0, round(max(buildings_import['wood']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))

sns.jointplot(data=buildings_import, x="wood", y="brick", hue="const_short", linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['wood']), ndigits=-2)),
              ylim=(0, round(max(buildings_import['brick']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))
# without outlyiers
sns.jointplot(data=buildings_import, x="concrete", y="steel", hue="const_short", linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['concrete']), ndigits=-2)),
              ylim=(0, 500),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))
sns.jointplot(data=buildings_import, x="concrete", y="wood", hue="const_short", linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['concrete']), ndigits=-2)),
              ylim=(0, 300),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))
sns.jointplot(data=buildings_import, x="concrete", y="brick", hue="const_short", linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['concrete']), ndigits=-2)),
              ylim=(0, round(max(buildings_import['brick']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))

sns.jointplot(data=buildings_import, x="steel", y="brick", hue="const_short", linewidth=0, height=8,
              xlim=(0, 500),
              ylim=(0, round(max(buildings_import['brick']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))
sns.jointplot(data=buildings_import, x="steel", y="wood", hue="const_short", linewidth=0, height=8,
              xlim=(0, 500),
              ylim=(0, 300),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))

sns.jointplot(data=buildings_import, x="wood", y="brick", hue="const_short", linewidth=0, height=8,
              xlim=(0, 300),
              ylim=(0, round(max(buildings_import['brick']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))

# use types, without outlyiers
sns.jointplot(data=buildings_import, x="concrete", y="steel", hue="use_short", linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['concrete']), ndigits=-2)),
              ylim=(0, 500),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))
sns.jointplot(data=buildings_import, x="concrete", y="wood", hue="use_short", linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['concrete']), ndigits=-2)),
              ylim=(0, 300),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))
sns.jointplot(data=buildings_import, x="concrete", y="brick", hue="use_short", linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['concrete']), ndigits=-2)),
              ylim=(0, round(max(buildings_import['brick']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))

sns.jointplot(data=buildings_import, x="steel", y="brick", hue="use_short", linewidth=0, height=8,
              xlim=(0, 500),
              ylim=(0, round(max(buildings_import['brick']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))
sns.jointplot(data=buildings_import, x="steel", y="wood", hue="use_short", linewidth=0, height=8,
              xlim=(0, 500),
              ylim=(0, 300),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))

sns.jointplot(data=buildings_import, x="wood", y="brick", hue="use_short", linewidth=0, height=8,
              xlim=(0, 300),
              ylim=(0, round(max(buildings_import['brick']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize)))

# ssp regions 32 to check that none of the regions govern these results, without outlyiers
sns.jointplot(data=buildings_import, x="concrete", y="steel", hue="R5_32", palette=("Set2"), linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['concrete']), ndigits=-2)),
              ylim=(0, 500),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize / 2)))
sns.jointplot(data=buildings_import, x="concrete", y="wood", hue="R5_32", palette=("Set2"), linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['concrete']), ndigits=-2)),
              ylim=(0, 300),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize / 2)))
sns.jointplot(data=buildings_import, x="concrete", y="brick", hue="R5_32", palette=("Set2"), linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['concrete']), ndigits=-2)),
              ylim=(0, round(max(buildings_import['brick']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize / 2)))

sns.jointplot(data=buildings_import, x="steel", y="brick", hue="R5_32", palette=("Set2"), linewidth=0, height=8,
              xlim=(0, 500),
              ylim=(0, round(max(buildings_import['brick']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize / 2)))
sns.jointplot(data=buildings_import, x="steel", y="wood", hue="R5_32", palette=("Set2"), linewidth=0, height=8,
              xlim=(0, 500),
              ylim=(0, 300),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize / 2)))

sns.jointplot(data=buildings_import, x="wood", y="brick", hue="R5_32", palette=("Set2"), linewidth=0, height=8,
              xlim=(0, 300),
              ylim=(0, round(max(buildings_import['brick']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize / 2)))

# ssp 5 regions to check that none of the regions govern these results, without outlyiers
sns.jointplot(data=buildings_import, x="concrete", y="steel", hue="R5", linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['concrete']), ndigits=-2)),
              ylim=(0, 500),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize / 2)))
sns.jointplot(data=buildings_import, x="concrete", y="wood", hue="R5", linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['concrete']), ndigits=-2)),
              ylim=(0, 300),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize / 2)))
sns.jointplot(data=buildings_import, x="concrete", y="brick", hue="R5", linewidth=0, height=8,
              xlim=(0, round(max(buildings_import['concrete']), ndigits=-2)),
              ylim=(0, round(max(buildings_import['brick']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize / 2)))

sns.jointplot(data=buildings_import, x="steel", y="brick", hue="R5", linewidth=0, height=8,
              xlim=(0, 500),
              ylim=(0, round(max(buildings_import['brick']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize / 2)))
sns.jointplot(data=buildings_import, x="steel", y="wood", hue="R5", linewidth=0, height=8,
              xlim=(0, 500),
              ylim=(0, 300),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize / 2)))

sns.jointplot(data=buildings_import, x="wood", y="brick", hue="R5", linewidth=0, height=8,
              xlim=(0, 300),
              ylim=(0, round(max(buildings_import['brick']), ndigits=-2)),
              marginal_kws=dict(bw_adjust=kdebw, cut=0), joint_kws=(dict(alpha=scatteralpha, s=scattersize / 2)))


# %% EDA: Kolmogorov-Smirnov Tests

group_a = buildings_import.loc[(buildings_import['use_short'].str.match('RM')) & (buildings_import['const_short'].str.match('C')) & (buildings_import['R5_32'].str.match('OECD_JPN')), ('steel')]
group_b = buildings_import.loc[(buildings_import['use_short'].str.match('RS')) & (buildings_import['const_short'].str.match('T')) & (buildings_import['R5_32'].str.match('OECD_JPN')), ('steel')]

group_a = buildings_import.loc[(buildings_import['use_short'].str.match('RU')) & (buildings_import['const_short'].str.match('C')) & (buildings_import['R5_32'].str.match('LAM_LAM-M')), ('steel')]
group_b = buildings_import.loc[(buildings_import['use_short'].str.match('RM')) & (buildings_import['const_short'].str.match('C')) & (buildings_import['R5_32'].str.match('LAM_LAM-M')), ('steel')]

stats.ks_2samp(group_a, group_b)  # if p < 0.05 we reject the null hypothesis. Hence the two sample datasets do not come from the same distribution.
stats.kruskal(group_a, group_b)  # if p < 0.05 we reject the null hypothesis. Hence the two sample datasets have different medians.
stats.epps_singleton_2samp(group_a, group_b, t=(0.4, 0.8))
stats.anderson_ksamp([group_a, group_b])  # works only when n>=2. If p < 0.05 we reject the null hypothesis. Hence the two sets do not come from the same distribution.

stats.ks_2samp(buildings_import.query("R5_32 == 'OECD_JPN' and use_short == 'RM'")['steel'], buildings_import.query("R5_32 == 'OECD_JPN' and use_short == 'RS'")['steel'])

# # approach that goes column by column
# db_combination_index = pd.MultiIndex.from_product(dims_list, names=dims_names)
# i = 0
# current_column = pd.DataFrame(data=None, index=db_combination_index[i:], columns=db_combination_index[i:i + 1])
# group_a = buildings_import.loc[(buildings_import['use_short'].str.match(current_column.index[:][0][0])) & (buildings_import['const_short'].str.match(current_column.index[:][0][1]) & (buildings_import['R5_32'].str.match(current_column.index[:][0][2]))), ('steel')]

# current_column.iloc[:] = stats.ks_2samp(group_a, buildings_import.loc[(buildings_import['use_short'].str.match(current_column.reset_index().iloc[:,0])) & (buildings_import['const_short'].str.match(current_column.reset_index().iloc[:,1]) & (buildings_import['R5_32'].str.match(current_column.reset_index().iloc[:,2]))), ('steel')])

# approach that moves cell by cell with 2 for loops - takes 20+ minutes

db_combination_index = pd.MultiIndex.from_product(dims_list, names=dims_names)
pairwise = pd.DataFrame(data=None, index=db_combination_index, columns=db_combination_index)
pairwise_ks_p = pairwise.copy()
pairwise_ks_s = pairwise.copy()
pairwise_kw_p = pairwise.copy()
pairwise_kw_s = pairwise.copy()
pairwise_ands_p = pairwise.copy()

# i = 0
# j = 0
for i in range(0, len(db_combination_index)):
    for j in range(i + 1, len(db_combination_index)):
        indexname = pairwise.iloc[[i, j]].index
        group_a = buildings_import.loc[(buildings_import['use_short'].str.match(indexname[0][0])) & (buildings_import['const_short'].str.match(indexname[0][1]) & (buildings_import['R5_32'].str.match(indexname[0][2]))), ('steel')]
        group_b = buildings_import.loc[(buildings_import['use_short'].str.match(indexname[1][0])) & (buildings_import['const_short'].str.match(indexname[1][1]) & (buildings_import['R5_32'].str.match(indexname[1][2]))), ('steel')]
#        if not(group_a.empty | group_b.empty):            if not(group_a.empty | group_b.empty):
        if (len(group_a) > 1 | len(group_b) > 1):
            ks_result = stats.ks_2samp(group_a, group_b)
            kp_result = stats.kruskal(group_a, group_b)
            ands_result = stats.anderson_ksamp([group_a, group_b])
            pairwise_ks_p.iloc[j, i] = ks_result[1]
            pairwise_kw_p.iloc[j, i] = kp_result[1]
            pairwise_ands_p.iloc[j, i] = ands_result[-1]
        else:
            pairwise_ks_p.iloc[j, i] = 2
            pairwise_kw_p.iloc[j, i] = 2
            pairwise_ands_p.iloc[j, i] = 2


pairwise_ks_p_clean = pairwise_ks_p.replace(2, np.NAN)
pairwise_ks_p_clean.dropna(how="all", inplace=True)
pairwise_ks_p_clean.dropna(axis='columns', how="all", inplace=True)
pairwise_ks_p_clean.to_excel("db_analysis\\ks_p.xlsx", merge_cells=False)
pairwise_ks_p_clean_long = pairwise_ks_p_clean.stack([0, 1, 2])
sns.heatmap(pairwise_ks_p_clean, cmap="RdYlBu_r", center=0.05, xticklabels=1, yticklabels=1, robust=True)

pairwise_kw_p_clean = pairwise_kw_p.replace(2, np.NAN)
pairwise_kw_p_clean.dropna(how="all", inplace=True)
pairwise_kw_p_clean.dropna(axis='columns', how="all", inplace=True)
pairwise_kw_p_clean.to_excel("db_analysis\\kw_p.xlsx", merge_cells=False)


# long form, seems to take much longer
# pairwise2 = pd.DataFrame(data=None, index=db_combination_index, columns=db_combination_index)
# pairwiselong = pairwise2.stack([0, 1, 2], dropna=False)
# for i in range(0, len(pairwiselong)):
#     group_a = buildings_import.loc[(buildings_import['use_short'].str.match(pairwiselong.index[i][0])) & (buildings_import['const_short'].str.match(pairwiselong.index[i][1]) & (buildings_import['R5_32'].str.match(pairwiselong.index[i][2]))), ('steel')]
#     group_b = buildings_import.loc[(buildings_import['use_short'].str.match(pairwiselong.index[i][3])) & (buildings_import['const_short'].str.match(pairwiselong.index[i][4]) & (buildings_import['R5_32'].str.match(pairwiselong.index[i][5]))), ('steel')]
#     if not(group_a.empty | group_b.empty):
#         ks_result = stats.ks_2samp(group_a, group_b)
#         pairwiselong.iloc[i] = ks_result[1]
#     else:
#         pairwiselong.iloc[i] = 2

# pairwiselong = pairwise2.stack([0, 1, 2], dropna=False)
# pairwiselong.index.names = ['use_short_a', 'const_short_a', 'R5_32_a', 'use_short_b', 'const_short_b', 'R5_32_b']
# pairwiselong = pairwiselong.reset_index()
# pairwiselong.rename(columns={0: 'ks'}, inplace=True)
# pairwiselong['ks'] = stats.ks_2samp(
#     buildings_import.loc[(buildings_import['use_short'].str.match(pairwiselong['use_short_a'])) & (buildings_import['const_short'].str.match(pairwiselong['const_short_a']) & (buildings_import['R5_32'].str.match(pairwiselong['R5_32_a']))), ('steel')].
#     buildings_import.loc[(buildings_import['use_short'].str.match(pairwiselong['use_short_b'])) & (buildings_import['const_short'].str.match(pairwiselong['const_short_b']) & (buildings_import['R5_32'].str.match(pairwiselong['R5_32_b']))), ('steel')])[1]

# %% final setups of the database data

# HINT remove IN 'informal' because there are simply not enough datapoints for meaningful estimations, consider including later
buildings_import = buildings_import[buildings_import.use_short != 'IN']
# set up the same multiindex as the other dataframes
buildings_import.set_index(dims_names, inplace=True)
# sort to make pandas faster and with less warnings
buildings_import = buildings_import.sort_index()


# %% create a new dataframe of the counts of unique combinations that exist in the DB
# including unspecifieds

db_combinations_stats = [pd.DataFrame(data=None, index=pd.MultiIndex.from_product(dims_list, names=dims_names)),
                         buildings_import.groupby(dims_names).count()[materials], buildings_import.groupby(dims_names).mean()[materials],
                         buildings_import.groupby(dims_names).std()[materials], buildings_import.groupby(dims_names).quantile(q=0.05)[materials],
                         buildings_import.groupby(dims_names).quantile(q=0.25)[materials], buildings_import.groupby(dims_names).quantile(q=0.50)[materials],
                         buildings_import.groupby(dims_names).quantile(q=0.75)[materials], buildings_import.groupby(dims_names).quantile(q=0.95)[materials]]
# TODO decide which quantile interpolation is best i.e. what does excel do?

db_combinations_stats = pd.concat(db_combinations_stats, axis=1, keys=['', 'count', 'avg', 'sd', 'p5', 'p25', 'p50', 'p75', 'p95'])

db_combinations_stats[('count', 'concrete')]
db_combinations_stats.loc[('NR', 'C', 'ASIA_CHN'), ('count', 'concrete')]
db_combinations_stats.loc[('NR', 'C', 'ASIA_CHN'), :]
db_combinations_stats.loc[:, db_combinations_stats.columns.isin(['concrete'], level=1)]

# replace NANs with zeros for consistency, or keep only those with values
db_combinations_stats_valid = db_combinations_stats.dropna(how='all')
# db_combinations_stats = db_combinations_stats.fillna(0)


# # exoort db_combinations_stats
# db_combinations_stats.to_excel("MI_results\\db_combinations_stats.xlsx", sheet_name="sheet1")
# db_combinations_stats.unstack().to_clipboard()

# %% separate buildings_import to individual dataframes by valid combinations

# prefiltered as a list only with valid combinations (i.e. existing in buildings_import): [combination tuple, dataframe, [no. of rows in df, counts of each material], expansion score set to 0]

db_combinations_data = {}
for current_material in materials:
    db_combinations_data[current_material] = []
    [db_combinations_data[current_material].append([row[0], buildings_import.loc[row[0]], int(db_combinations_stats_valid.loc[row[0], ('count', current_material)]), 0]) for row in db_combinations_stats_valid.itertuples() if db_combinations_stats_valid.loc[row[0], ('count', current_material)] > 0]


# %% create a dataframe with all practical (i.e. not unspecifieds) combination options to be filled with data

# remove 'unspecified' entities !!make sure to change the list indexes as needed
dims_list_specified = dims_list[:]
dims_list_specified[0] = [x for x in dims_list_specified[0] if 'U' not in x]
dims_list_specified[1] = [x for x in dims_list_specified[1] if 'U' not in x]


# dict for storing the current selection MIs with their IDs for backup and reference
mi_estimation_data = {}
mi_estimation_stats = {}
for current_material in materials:
    mi_estimation_data[current_material] = {}
    mi_estimation_stats[current_material] = pd.DataFrame(data=None, index=pd.MultiIndex.from_product(dims_list_specified, names=dims_names),
                                                         columns=['R5', 'db_count', 'db_avg', 'db_sd', 'db_5', 'db_25', 'db_50', 'db_75', 'db_95',
                                                                  'expand_count', 'expand_avg', 'expand_sd', 'expand_5', 'expand_25', 'expand_50', 'expand_75', 'expand_95', 'expand_rounds'])  # , 'p1', 'p5', 'p10', 'p20', 'p25', 'p30', 'p40', 'p50', 'p60', 'p70', 'p75', 'p80', 'p90', 'p95', 'p99'
    mi_estimation_stats[current_material] = mi_estimation_stats[current_material].reset_index()
    mi_estimation_stats[current_material]['R5'] = mi_estimation_stats[current_material]['R5_32'].str.split('_').str[0]  # SSP 5 regions
    mi_estimation_stats[current_material] = mi_estimation_stats[current_material].set_index(['use_short', 'const_short', 'R5_32'])
    mi_estimation_stats[current_material]['db_count'] = db_combinations_stats[('count', current_material)]
    mi_estimation_stats[current_material]['db_avg'] = db_combinations_stats[('avg', current_material)]
    mi_estimation_stats[current_material]['db_sd'] = db_combinations_stats[('sd', current_material)]
    mi_estimation_stats[current_material]['db_5'] = db_combinations_stats[('p5', current_material)]
    mi_estimation_stats[current_material]['db_25'] = db_combinations_stats[('p25', current_material)]
    mi_estimation_stats[current_material]['db_50'] = db_combinations_stats[('p50', current_material)]
    mi_estimation_stats[current_material]['db_75'] = db_combinations_stats[('p75', current_material)]
    mi_estimation_stats[current_material]['db_95'] = db_combinations_stats[('p95', current_material)]

# %% selection algorithm

stop_count = 30


def expand_selection(selection, count, condition, material):
    newselection = [list(v) for v in db_combinations_data[material] if eval(condition)]
    if newselection:  # pythonic way to check if newselection is not empty
        selection += newselection
        count = 0
        for item in selection:
            item[3] += 1  # counter for how many rounds this selection was in an expansion
            count += item[2] * item[3]  # count how many datapoints are in selection
    return selection, count


# HINT cosmetic: for simple tracking in the sandbox: sort by count of appearances in the db
for current_material in materials:
    mi_estimation_stats[current_material] = mi_estimation_stats[current_material].sort_values(by="db_count", ascending=False)

    for current_index in mi_estimation_stats[current_material].itertuples():  # running index for the current combination in mi_estimation
        current_combi = current_index[0]  # the current combination, a tuple. if a list is needed use list(mi_estimation.index[0])

        current_selection = []
        current_count = 0

        # 1.1 add perfect matches
        if current_count < stop_count:
            current_condition = 'current_combi == v[0]'
            current_selection, current_count = expand_selection(current_selection, current_count, current_condition, current_material)
        # 1.2 add similar use types
        if current_count < stop_count:
            if current_combi[0] == 'NR':
                current_condition = "('UN' == v[0][0]) and (current_combi[1] == v[0][1]) and (current_combi[2] == v[0][2])"  # TODO this reselects the perfect combination! see RS T OECD_USA
                current_selection, current_count = expand_selection(current_selection, current_count, current_condition, current_material)
            else:  # i.e. if current_combi[0][0] == 'R':
                current_condition = "('RU' == v[0][0]) and (current_combi[1] == v[0][1]) and (current_combi[2] == v[0][2])"  # TODO consider whether to first add UN (currently in the IF below) and only then RU?
                current_selection, current_count = expand_selection(current_selection, current_count, current_condition, current_material)
                if current_count < stop_count:  # TODO this adds UN. consider whether to add the opposite R type e.g. if we're at RS then add RM and vice versa
                    current_condition = "('UN' == v[0][0]) and (current_combi[1] == v[0][1]) and (current_combi[2] == v[0][2])"
                    current_selection, current_count = expand_selection(current_selection, current_count, current_condition, current_material)

        # 2.1 repeat for bigger 5-level region, not including the current 32-level region
        if current_count < stop_count:
            current_condition = "(current_combi[0] == v[0][0]) and (current_combi[1] == v[0][1]) and (current_combi[2][:3] in v[0][2]) and (current_combi[2] != v[0][2])"
            current_selection, current_count = expand_selection(current_selection, current_count, current_condition, current_material)
        # 2.2 add similar use types
        if current_count < stop_count:
            if current_combi[0] == 'NR':
                current_condition = "('UN' == v[0][0]) and (current_combi[1] == v[0][1]) and (current_combi[2][:3] in v[0][2]) and (current_combi[2] != v[0][2])"
                current_selection, current_count = expand_selection(current_selection, current_count, current_condition, current_material)
            else:  # make sure to keep it conformed to 1.2 TODO decisions!
                current_condition = "('RU' == v[0][0]) and (current_combi[1] == v[0][1]) and (current_combi[2][:3] in v[0][2]) and (current_combi[2] != v[0][2])"
                current_selection, current_count = expand_selection(current_selection, current_count, current_condition, current_material)
                if current_count < stop_count:
                    current_condition = "('UN' == v[0][0]) and (current_combi[1] == v[0][1]) and (current_combi[2][:3] in v[0][2]) and (current_combi[2] != v[0][2])"
                    current_selection, current_count = expand_selection(current_selection, current_count, current_condition, current_material)

        # 3.1 repeat for all regions
        # TODO consider if stop_count or if stop_count-x to not expand to the entire world if we're already close to stop_count
        if current_count < stop_count:
            current_condition = "(current_combi[0] == v[0][0]) and (current_combi[1] == v[0][1]) and (current_combi[2][:3] not in v[0][2])"
            current_selection, current_count = expand_selection(current_selection, current_count, current_condition, current_material)
        # 3.2 add similar use types
        if current_count < stop_count:
            if current_combi[0] == 'NR':
                current_condition = "('UN' == v[0][0]) and (current_combi[1] == v[0][1]) and (current_combi[2][:3] not in v[0][2])"
                current_selection, current_count = expand_selection(current_selection, current_count, current_condition, current_material)
            else:  # make sure to keep it conformed to 1.2 TODO decisions!
                current_condition = "('RU' == v[0][0]) and (current_combi[1] == v[0][1]) and (current_combi[2][:3] not in v[0][2])"
                current_selection, current_count = expand_selection(current_selection, current_count, current_condition, current_material)
                if current_count < stop_count:
                    current_condition = "('UN' == v[0][0]) and (current_combi[1] == v[0][1]) and (current_combi[2][:3] not in v[0][2])"
                    current_selection, current_count = expand_selection(current_selection, current_count, current_condition, current_material)

        # When done: concatenate current_selection into one dataframe, including repetition of selections from previous expansion rounds i.e. v[3] in the second for loop
        try:  # TODO temporary solution for empty combinations
            current_selection_combined = pd.concat([v[1] for v in current_selection for i in range(v[3])], copy=True).loc[:, ['id', current_material]].dropna()
            current_selection_combined['expansion_round'] = current_selection_combined.groupby('id').cumcount()
            current_selection_combined['expansion_round'] = current_selection_combined['expansion_round'].max() - current_selection_combined['expansion_round']
            if current_combi not in current_selection_combined.index:
                current_selection_combined['expansion_round'] += 1
            # fill results into mi_estimation_stats 'expanded_count', 'avg', 'sd', 'p5', 'p25', 'p50', 'p75', 'p95', 'expansion_rounds'
            mi_estimation_stats[current_material].loc[current_combi, 'expand_count'] = current_count
            mi_estimation_stats[current_material].loc[current_combi, 'expand_avg'] = current_selection_combined[current_material].mean()
            mi_estimation_stats[current_material].loc[current_combi, 'expand_sd'] = current_selection_combined[current_material].std()
            mi_estimation_stats[current_material].loc[current_combi, 'expand_5'] = np.quantile(current_selection_combined[current_material], q=0.05)  # faster than pandas's current_selection_combined['steel'].quantile(q=0.05)
            mi_estimation_stats[current_material].loc[current_combi, 'expand_25'] = np.quantile(current_selection_combined[current_material], q=0.25)
            mi_estimation_stats[current_material].loc[current_combi, 'expand_50'] = np.quantile(current_selection_combined[current_material], q=0.50)
            mi_estimation_stats[current_material].loc[current_combi, 'expand_75'] = np.quantile(current_selection_combined[current_material], q=0.75)
            mi_estimation_stats[current_material].loc[current_combi, 'expand_95'] = np.quantile(current_selection_combined[current_material], q=0.95)
            mi_estimation_stats[current_material].loc[current_combi, 'expand_rounds'] = current_selection[0][3]
        except ValueError:
            current_selection_combined = pd.DataFrame()

        # save current_selection_combined for backup and reference
        mi_estimation_data[current_material][current_combi] = current_selection_combined.copy()

    # HINT cosmetic: resort by index
    mi_estimation_stats[current_material].sort_index(inplace=True)
    filename = current_material + '_stop_at_' + str(stop_count) + '_20200317'
    mi_estimation_stats[current_material].reset_index().to_excel('MI_results\\' + filename + '.xlsx', sheet_name=(current_material + filename))

# %% analysis: prepare the results

# merge results data for boxplots, start with a list of dataframes and then concatenate it to one dataframe
# structure should be: combination dict: use, const, r32, material, value
# then we can do boxplots etc., one page for each region, each plot has the 4 materials

analysis_comparison_data = {}
for current_material in materials:
    for key, value in mi_estimation_data[current_material].items():
        analysis_comparison_data[key + (current_material,)] = mi_estimation_data[current_material][key]
        analysis_comparison_data[key + (current_material,)] = analysis_comparison_data[key + (current_material,)].reset_index()
        analysis_comparison_data[key + (current_material,)] = analysis_comparison_data[key + (current_material,)].drop(['id'] + dims_names, axis=1)
        analysis_comparison_data[key + (current_material,)]['combination'] = str(key)
analysis_comparison_data = pd.concat(analysis_comparison_data)
analysis_comparison_data['value'] = analysis_comparison_data.sum(axis=1, numeric_only=True)
analysis_comparison_data.index.rename(dims_names + ['material', 'id'], inplace=True)
analysis_comparison_data.reset_index(inplace=True)
analysis_comparison_data.drop(materials + ['id'], axis=1, inplace=True)
analysis_comparison_data['R5'] = analysis_comparison_data['R5_32'].str.split('_').str[0]

# %% analysis: boxplots

sns.boxplot(data=analysis_comparison_data.loc[analysis_comparison_data['combination'] == "('RS', 'C', 'OECD_EU15')"], x='material', y='value')
sns.catplot(data=analysis_comparison_data.loc[analysis_comparison_data['R5_32'] == "OECD_EU15"], x='material', y='value', row='use_short', col='const_short', kind="violin")

region = "OECD_EU15"
boxes = sns.catplot(kind="box",
                    data=analysis_comparison_data.loc[analysis_comparison_data['R5_32'] == region],
                    hue='material', y='value',
                    row='const_short', row_order=dims_list_specified[1],
                    x='use_short', order=dims_list_specified[0],
                    linewidth=0.8, showfliers=False,
                    aspect=3, sharey=True, legend_out=False)
boxes.set_titles(region + ", {row_name}")

boxes = sns.catplot(kind="boxen",
                    data=analysis_comparison_data.loc[analysis_comparison_data['R5_32'] == region],
                    hue='material', y='value',
                    row='const_short', row_order=dims_list_specified[1],
                    x='use_short', order=dims_list_specified[0],
                    linewidth=0.8, showfliers=False,
                    aspect=3, sharey=True, legend_out=False, k_depth="proportion", outlier_prop=0.05)
boxes.set_titles(region + ", {row_name}")

sns.catplot(kind="box",
            data=analysis_comparison_data.loc[analysis_comparison_data['R5_32'] == "OECD_EU15"],
            x='material', y='value',
            row='use_short', row_order=dims_list_specified[0],
            col='const_short', col_order=dims_list_specified[1],
            linewidth=0.8, showfliers=False,
            )

with PdfPages('MI_results\\boxplots.pdf') as pdf:
    for region in dims_list_specified[2]:
        boxes = sns.catplot(kind="box",
                            data=analysis_comparison_data.loc[analysis_comparison_data['R5_32'] == region],
                            hue='material', y='value',
                            row='const_short', row_order=dims_list_specified[1],
                            x='use_short', order=dims_list_specified[0],
                            linewidth=0.8, showfliers=False,
                            aspect=3, legend_out=False)
        boxes.set_titles(region + ", {row_name}")
        pdf.savefig(boxes.fig)

# %% analysis: before-after comparisons with violin plots

# merge results data for seaborn
analysis_comparisons = {}
for current_material in materials:
    analysis_comparisons[current_material] = {}
    for row in mi_estimation_stats[current_material].itertuples():
        if buildings_import.index.isin([row[0]]).any():
            analysis_comparisons[current_material][row[0]] = buildings_import.loc[row[0], ['id', current_material]]
        else:
            analysis_comparisons[current_material][row[0]] = pd.DataFrame(data=None)
        analysis_comparisons[current_material][row[0]] = analysis_comparisons[current_material][row[0]].assign(MIs="before")
        analysis_comparisons[current_material][row[0]] = pd.concat([analysis_comparisons[current_material][row[0]], mi_estimation_data[current_material][row[0]].loc[:, ['id', current_material]]])
        analysis_comparisons[current_material][row[0]]['MIs'] = analysis_comparisons[current_material][row[0]]['MIs'].fillna("after")
        analysis_comparisons[current_material][row[0]].dropna(inplace=True)
        analysis_comparisons[current_material][row[0]] = analysis_comparisons[current_material][row[0]].assign(combination=str(row[0]))
        analysis_comparisons[current_material][row[0]] = analysis_comparisons[current_material][row[0]].assign(use=row[0][0])
        analysis_comparisons[current_material][row[0]] = analysis_comparisons[current_material][row[0]].assign(construction=row[0][1])
        analysis_comparisons[current_material][row[0]] = analysis_comparisons[current_material][row[0]].assign(region=row[0][2])

# viol = sns.violinplot(y="combination", x=current_material, data=comparisons[current_material][('RS', 'C', 'OECD_EU15')], hue="MIs", hue_order=("after", "before"), split=True, inner="stick", scale="count", bw=0.1, linewidth=1)
# viol.set_xlim(left=0, right=500)

swar = sns.swarmplot(y="combination", x=current_material, data=analysis_comparisons[current_material][('RS', 'C', 'OECD_EU15')], hue="MIs", hue_order=("before", "after"))
stri = sns.stripplot(y="combination", x=current_material, data=analysis_comparisons[current_material][('RS', 'C', 'OECD_EU15')], hue="MIs", hue_order=("before", "after"))


def compareviolin_landscape(u, c, r, material, axx, axy):
    violcombi = (u, c, r)
    if material == 'steel':
        outliercut = 200
    elif material == 'wood':
        outliercut = 350
    else:
        outliercut = buildings_import.max()[material]
    viol = sns.violinplot(y="combination", x=material, data=analysis_comparisons[material][violcombi], hue="MIs", hue_order=("after", "before"), split=True,
                          inner="quartile", scale="count", bw=.1, linewidth=1, ax=violins_axs[axx, axy])
    viol.set_title(violcombi)
    viol.set_xlim(left=0, right=outliercut)
    viol.set_ylabel("")
    viol.set_yticks([])
    viol.legend([], [], frameon=False)
    viol.annotate('After (n = ' + str(mi_estimation_stats[material].loc[violcombi, "expand_count"]) + ', ' + str(mi_estimation_stats[material].loc[violcombi, "expand_rounds"]) + ' expansions)\n'
                  'p5 = ' + str(round(mi_estimation_stats[material].loc[violcombi, "expand_5"], 2)) + '\n'
                  'p25 = ' + str(round(mi_estimation_stats[material].loc[violcombi, "expand_25"], 2)) + '\n'
                  'median = ' + str(round(mi_estimation_stats[material].loc[violcombi, "expand_50"], 2)) + '\n'
                  'p75 = ' + str(round(mi_estimation_stats[material].loc[violcombi, "expand_75"], 2)) + '\n'
                  'p95 = ' + str(round(mi_estimation_stats[material].loc[violcombi, "expand_95"], 2)),
                  xy=(outliercut - 1, -0.49), va='top', ha='right', color='C0')
    if outliercut < buildings_import.max()[material]:
        viol.annotate('outliers > ' + str(outliercut) + ' = ' + str(analysis_comparisons[material][violcombi].query(material + ' > @outliercut and (MIs == "after")').count()[1]),
                      xy=(outliercut - 1, -0.28), va='top', ha='right', color='C0')

    if mi_estimation_stats[material].loc[violcombi, "db_count"] > 0:
        viol.annotate('Before (n = ' + str(round(mi_estimation_stats[material].loc[violcombi, "db_count"])) + ')\n'
                      'p5 = ' + str(round(mi_estimation_stats[material].loc[violcombi, "db_25"], 2)) + '\n'
                      'p25 = ' + str(round(mi_estimation_stats[material].loc[violcombi, "db_25"], 2)) + '\n'
                      'median = ' + str(round(mi_estimation_stats[material].loc[violcombi, "db_50"], 2)) + '\n'
                      'q75 = ' + str(round(mi_estimation_stats[material].loc[violcombi, "db_75"], 2)) + '\n'
                      'q95 = ' + str(round(mi_estimation_stats[material].loc[violcombi, "db_95"], 2)) + '\n',
                      xy=(outliercut - 1, 0.49), va='bottom', ha='right', color='C1')
        if outliercut < buildings_import.max()[material]:
            viol.annotate('outliers > ' + str(outliercut) + ' = ' + str(analysis_comparisons[material][violcombi].query(material + ' > @outliercut and (MIs == "before")').count()[1]),
                          xy=(outliercut - 1, 0.49), va='bottom', ha='right', color='C1')

    else:
        viol.annotate('Before (n = 0)', va='bottom', ha='right', color='C1', xy=(outliercut - 1, 0.49))
    return viol


for current_material in materials:
    filename = current_material + '_stop_at_' + str(stop_count) + '_20200305'
    with PdfPages('MI_results\\' + filename + '.pdf') as pdf:
        for region in dims_list_specified[2]:
            violins, violins_axs = plt.subplots(3, 4, figsize=(30, 20))
            compareviolin_landscape('NR', 'C', region, current_material, 0, 0)
            compareviolin_landscape('NR', 'M', region, current_material, 0, 1)
            compareviolin_landscape('NR', 'S', region, current_material, 0, 2)
            compareviolin_landscape('NR', 'T', region, current_material, 0, 3)
            compareviolin_landscape('RM', 'C', region, current_material, 1, 0)
            compareviolin_landscape('RM', 'M', region, current_material, 1, 1)
            compareviolin_landscape('RM', 'S', region, current_material, 1, 2)
            compareviolin_landscape('RM', 'T', region, current_material, 1, 3)
            compareviolin_landscape('RS', 'C', region, current_material, 2, 0)
            compareviolin_landscape('RS', 'M', region, current_material, 2, 1)
            compareviolin_landscape('RS', 'S', region, current_material, 2, 2)
            compareviolin_landscape('RS', 'T', region, current_material, 2, 3)
            pdf.savefig(violins)


# %% analysis: growth of distributions by expansion round, histograms

growth = sns.histplot(data=analysis_growth[current_material][current_combi], x=current_material,
                      hue="expansion_round", hue_order=["0", "1", "2", "3", "4", "5", "6"],  # hue_order=["6", "5", "4", "3", "2", "1", "0"],
                      palette="magma", alpha=1, linewidth=0,  # fill=False,
                      stat="count", element="step",
                      binwidth=75)
growth.set_xlim(left=0, right=buildings_import.max()[current_material])

current_combi = ('RS', 'T', 'ASIA_TWN')
current_combi = ('RM', 'T', 'OECD_EU15')


growth, growth_axes = plt.subplots(3, gridspec_kw={"height_ratios": (.1, .1, .8)})

growth_data = mi_estimation_data[current_material][current_combi].copy().reset_index()
growth_data['expansion_round'] = growth_data['expansion_round'].astype("string")
sns.set_palette("magma", 7)
sns.boxplot(data=growth_data, x=current_material,
            linewidth=0.8, showfliers=False,
            color="C" + growth_data['expansion_round'].max(),
            ax=growth_axes[0])
sns.boxplot(data=growth_data.query('expansion_round == "0"'), x=current_material,
            linewidth=0.8, showfliers=False,
            color="C1",
            ax=growth_axes[1])
sns.histplot(data=growth_data, x=current_material,
             hue="expansion_round", hue_order=["0", "1", "2", "3", "4", "5", "6"],
             alpha=1, linewidth=0,
             stat="count", element="step",
             binwidth=20,
             ax=growth_axes[2])
growth_axes[0].set(yticks=[], xticks=[], xlim=(0, 700),
                   xlabel='after, n=' + str(growth_data.count()[0]),
                   title=str(current_combi)[1:-1])
growth_axes[1].set(yticks=[], xticks=[], xlim=(0, 700),
                   xlabel='before, n=' + str(growth_data.query('expansion_round == "0"').count()[0]))
growth_axes[2].set(xlim=(0, 700), xlabel='kg/m2 \n')
sns.despine(ax=growth_axes[0], left=True, bottom=True)
sns.despine(ax=growth_axes[1], left=True, bottom=True)
sns.despine(ax=growth_axes[2])


def comparegrowth_hist(u, c, r, material, axx_before, axx_after, axx_hist, axy):
    combi = (u, c, r)
    if material == 'steel':
        outliercut = 200
        binsize = 15
    elif material == 'wood':
        outliercut = 350
        binsize = 20
    else:
        outliercut = buildings_import.max()[material]
        binsize = 75

    growth_data = mi_estimation_data[material][combi].copy().reset_index()
    growth_data['expansion_round'] = growth_data['expansion_round'].astype("string")

    sns.set_palette("magma", 7)

    sns.boxplot(data=growth_data, x=material,
                linewidth=0.8, showfliers=False,
                color="C" + growth_data['expansion_round'].max(),
                ax=growth_axes[axx_after, axy])
    sns.boxplot(data=growth_data.query('expansion_round == "0"'), x=material,
                linewidth=0.8, showfliers=False,
                color=".6",
                ax=growth_axes[axx_before, axy])
    sns.histplot(data=growth_data, x=material,
                 hue="expansion_round", hue_order=["0", "1", "2", "3", "4", "5", "6"],
                 alpha=1, linewidth=0,
                 stat="count", element="step",
                 binwidth=binsize,
                 ax=growth_axes[axx_hist, axy])

    growth_axes[axx_after, axy].set(yticks=[], xticks=[], xlim=(0, outliercut),
                                    xlabel='after, n=' + str(growth_data.count()[0]))
    growth_axes[axx_before, axy].set(yticks=[], xticks=[], xlim=(0, outliercut),
                                     xlabel='before, n=' + str(growth_data.query('expansion_round == "0"').count()[0]),
                                     title="\n" + str(combi)[1:-1])
    growth_axes[axx_hist, axy].set(xlim=(0, outliercut), xlabel='kg/m2 \n')

    sns.despine(ax=growth_axes[axx_after, axy], left=True, bottom=True)
    sns.despine(ax=growth_axes[axx_before, axy], left=True, bottom=True)
    sns.despine(ax=growth_axes[axx_hist, axy])

    if not(axx_hist == 2 and axy == 3):
        growth_axes[axx_hist, axy].legend([], [], frameon=False)

    return None


for current_material in materials:
    filename = current_material + '_stop_at_' + str(stop_count) + '_20200317'
    with PdfPages('MI_results\\' + filename + '.pdf') as pdf:
        for region in dims_list_specified[2]:
            growth, growth_axes = plt.subplots(9, 4, gridspec_kw={"height_ratios": (.1, .1, .8, .1, .1, .8, .1, .1, .8)}, figsize=(30, 20))
            comparegrowth_hist("NR", "C", region, current_material, 0, 1, 2, 0)
            comparegrowth_hist("NR", "M", region, current_material, 0, 1, 2, 1)
            comparegrowth_hist("NR", "S", region, current_material, 0, 1, 2, 2)
            comparegrowth_hist("NR", "T", region, current_material, 0, 1, 2, 3)
            comparegrowth_hist("RM", "C", region, current_material, 3, 4, 5, 0)
            comparegrowth_hist("RM", "M", region, current_material, 3, 4, 5, 1)
            comparegrowth_hist("RM", "S", region, current_material, 3, 4, 5, 2)
            comparegrowth_hist("RM", "T", region, current_material, 3, 4, 5, 3)
            comparegrowth_hist("RS", "C", region, current_material, 6, 7, 8, 0)
            comparegrowth_hist("RS", "M", region, current_material, 6, 7, 8, 1)
            comparegrowth_hist("RS", "S", region, current_material, 6, 7, 8, 2)
            comparegrowth_hist("RS", "T", region, current_material, 6, 7, 8, 3)
            growth.set_constrained_layout(True)
            pdf.savefig(growth)

# %% analysis: growth of distributions by expansion round, kde

# merge results data for multiple combinations manually (similar to the violin plots)
analysis_growth = {}
for current_material in materials:
    analysis_growth[current_material] = {}
    for row in mi_estimation_stats[current_material].itertuples():
        analysis_growth[current_material][row[0]] = pd.DataFrame(data=None)
        analysis_growth[current_material][row[0]] = mi_estimation_data[current_material][row[0]].copy().reset_index()
        # analysis_growth[current_material][row[0]].drop_duplicates(subset="id", keep="last", inplace=True)
        analysis_growth[current_material][row[0]]['expansion_round'] = analysis_growth[current_material][row[0]]['expansion_round'].astype("string")
        analysis_growth[current_material][row[0]] = analysis_growth[current_material][row[0]].assign(combination=str(row[0]))
        analysis_growth[current_material][row[0]] = analysis_growth[current_material][row[0]].assign(use=row[0][0])
        analysis_growth[current_material][row[0]] = analysis_growth[current_material][row[0]].assign(construction=row[0][1])
        analysis_growth[current_material][row[0]] = analysis_growth[current_material][row[0]].assign(region=row[0][2])

current_combi = ('RS', 'T', 'ASIA_TWN')
growth = sns.kdeplot(data=analysis_growth[current_material][current_combi], x=current_material,
                     hue="expansion_round", hue_order=["4", "3", "2", "1", "0"],
                     linewidth=0, palette="magma",
                     bw_adjust=.2, multiple="stack")
growth.set_xlim(left=0, right=buildings_import.max()[current_material])


def comparegrowth_kde(u, c, r, material, axx, axy):
    combi = (u, c, r)
    if material == 'steel':
        outliercut = 200
    elif material == 'wood':
        outliercut = 350
    else:
        outliercut = buildings_import.max()[material]
    growth = sns.kdeplot(data=analysis_growth[material][combi], x=material,
                         hue="expansion_round", hue_order=["6", "5", "4", "3", "2", "1", "0"],
                         linewidth=0, palette="magma",
                         bw_adjust=.2, multiple="stack",
                         warn_singular=False,
                         ax=growths_axs[axx, axy])
    growth.set_ylabel("")
    growth.set_yticks([])
    growth.set_title(combi)
    growth.set_xlim(left=0, right=outliercut)
    if not(axx == 0 and axy == 3):
        growth.legend([], [], frameon=False)
    return growth


for current_material in materials:
    filename = 'kde_growth_' + current_material + '_stop_at_' + str(stop_count) + '_20200317'
    with PdfPages('MI_results\\' + filename + '.pdf') as pdf:
        for region in dims_list_specified[2]:
            growths, growths_axs = plt.subplots(3, 4, figsize=(30, 20))
            comparegrowth_kde('NR', 'C', region, current_material, 0, 0)
            comparegrowth_kde('NR', 'M', region, current_material, 0, 1)
            comparegrowth_kde('NR', 'S', region, current_material, 0, 2)
            comparegrowth_kde('NR', 'T', region, current_material, 0, 3)
            comparegrowth_kde('RM', 'C', region, current_material, 1, 0)
            comparegrowth_kde('RM', 'M', region, current_material, 1, 1)
            comparegrowth_kde('RM', 'S', region, current_material, 1, 2)
            comparegrowth_kde('RM', 'T', region, current_material, 1, 3)
            comparegrowth_kde('RS', 'C', region, current_material, 2, 0)
            comparegrowth_kde('RS', 'M', region, current_material, 2, 1)
            comparegrowth_kde('RS', 'S', region, current_material, 2, 2)
            comparegrowth_kde('RS', 'T', region, current_material, 2, 3)
            pdf.savefig(growths)


# %% further analysis

# TODO list:
# for the paper we'll select some examples of how the algorithm behaves with lots of perfect matches, the cse of 10-15, and the case of 0-1 datapoints
# maybe create a user interface that shows violin plots and percentiles before users download the data
# TODO 24/2:
# compare results with previous studies: marinova, heeren, etc.
# consider adding glass aluminum copper, etc as in marinova, even though we won't get much between-region variation, it's still an improvement over marinova's simple avg.
# maybe for these extra materials we don't need the regional differentiation, so we'd use a simplified algorithm on 5 ssp or just global but still differentiate use and const.

current_material = 'steel'
mi_estimation_stats[current_material].to_clipboard()

# comparisons of before-after vis a vis number of rounds
mi_estimation_stats[current_material]['db_count'] = mi_estimation_stats[current_material]['db_count'].fillna(0)
sns.relplot(x="expand_count", y="expand_rounds", size="db_count", sizes=(15, 200), hue="use_short", data=mi_estimation_stats[current_material])
sns.relplot(x="expand_count", y="expand_rounds", size="db_count", sizes=(15, 200), hue="const_short", data=mi_estimation_stats[current_material])
sns.relplot(x="expand_count", y="expand_rounds", size="db_count", sizes=(15, 200), hue="R5", data=mi_estimation_stats[current_material])
sns.relplot(x="expand_count", y="db_count", hue="expand_rounds", data=mi_estimation_stats[current_material])
sns.relplot(x="expand_count", y="db_count", hue="R5", data=mi_estimation_stats[current_material])
sns.relplot(x="db_count", y="expand_count", hue="R5", size="expand_rounds", sizes=(10, 300), alpha=0.5, data=mi_estimation_stats[current_material])
sns.relplot(x="expand_rounds", y="db_count", hue="R5", size="expand_count", sizes=(1, 400), alpha=0.3, data=mi_estimation_stats[current_material])
sns.swarmplot(x="expand_rounds", y="expand_count", hue="R5", data=mi_estimation_stats[current_material])
