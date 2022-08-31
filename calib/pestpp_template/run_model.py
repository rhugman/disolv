import disolv
import pandas as pd
import os
import numpy as np

# remove previous flows.csv to avoid reusing same file
try:
    os.remove('flows.csv')
except:
    print("flows.csv not found.")

# read files with PEST updated parameters
tot_flow = pd.read_csv('total_flow.csv').iloc[0].values[-1]
flows_frac = pd.read_csv('flows_frac.csv')

# scale frctions by the largest value and then tot_flow
for col in [1,2]:
    flows_frac.iloc[:,col] = tot_flow * flows_frac.iloc[:,col]/flows_frac.iloc[:,col].sum()

# write new flows input csv
flows_frac.to_csv('flows.csv', index=False)

# run disolv
disolv.run('.', '.', calibrate=False, convertFEC=False)


def obs_diff_from_sim(sim_output='profiles.csv', diff_file='profiles-diff.csv', tdiff_file='profiles-tdiff.csv'):
    # read model simulated absolute observations
    obs = pd.read_csv(sim_output)
    # make difference observations
    diff = obs.copy().replace(1e30, np.nan)
    diff = diff.diff().replace(np.nan, 1e30)
    # write file
    diff.to_csv(diff_file, index=None)

    # time differnece
    tdiff = obs.copy()
    tdiff.iloc[:, 1:] = obs.iloc[:, 1:].replace(1e30, np.nan).diff(axis=1).fillna(1e30)
    tdiff.to_csv(tdiff_file, index=None)

obs_diff_from_sim(sim_output='profiles.csv', diff_file='profiles-diff.csv', tdiff_file='profiles-tdiff.csv')