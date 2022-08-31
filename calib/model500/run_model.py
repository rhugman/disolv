import disolv
import pandas as pd
import os

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