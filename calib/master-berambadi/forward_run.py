import os
import multiprocessing as mp
import numpy as np
import pandas as pd
import pyemu
import disolv
import pandas
import os

# function added thru PstFrom.add_py_function()
def flows_from_fracs():
    import pandas as pd
    import os

    # remove previous flows.csv to avoid reusing same file
    try:
        os.remove('flows.csv')
    except:
        print("flows.csv not found.")

    # read files with PEST updated parameters
    tot_flow = pd.read_csv('total_flow.csv').iloc[0].values[-1]
    exp_fac = pd.read_csv('exp_function.csv').iloc[0].values[-1]
    flows_frac = pd.read_csv('flows_frac.csv')

    # force in == out
    #check = flows_frac.iloc[:,1].sum() - abs(flows_frac.iloc[:,2].sum())

    #while abs(check) > 1e-9:
    #    if check > 0:
    #        flows_frac.iloc[:,2] = (1+check) * flows_frac.iloc[:,2]
    #    elif check < 0:
    #        flows_frac.iloc[:,1] = (1+abs(check)) * flows_frac.iloc[:,1]
    #    # recheck
    #    check = flows_frac.iloc[:,1].sum() - abs(flows_frac.iloc[:,2].sum())

    # scale frctions by the largest value and then tot_flow
    for col in [1,2]:
        # exp function
        #avg = flows_frac.iloc[:,col].mean()
        #flows_frac.iloc[:,col] = avg + (avg - flows_frac.iloc[:,col]) ** exp_fac
        #flows_frac.iloc[:,col] = [abs(i) for i in flows_frac.iloc[:,col]]
        # scale by average
        #flows_frac.iloc[:,col] = flows_frac.iloc[:,col]/ flows_frac.iloc[:,col].mean() / flows_frac.iloc[:,col].count()
        flows_frac.iloc[:,col] = flows_frac.iloc[:,col]/ flows_frac.iloc[:,col].sum()
        # scale by total flow; abs used to avoid bugs
        if col == 1:
            flows_frac.iloc[:,col] = tot_flow * abs(flows_frac.iloc[:,col])   
        if col == 2:
            flows_frac.iloc[:,col] = tot_flow * -1*abs(flows_frac.iloc[:,col])

    # check discrepancy
    check = flows_frac.iloc[:,1].sum() - abs(flows_frac.iloc[:,2].sum())
    # write new flows input csv
    flows_frac.to_csv('flows.csv', index=False)
    print(f'error:{check}')
    print('flows.csv has been updated')
    return

# function added thru PstFrom.add_py_function()
def obs_diff_from_sim(sim_output='profiles.csv', diff_file='profiles-diff.csv', tdiff_file='profiles-tdiff.csv'):
    # read model simulated absolute observations
    obs = pd.read_csv(sim_output)
    # make difference observations
    diff = obs.copy().replace(1e30, np.nan)
    diff = diff.diff().replace(np.nan, 1e30)
    # write file
    diff.to_csv(diff_file, index=None)

    # time differnece
    tdiff = obs.copy().replace(1e30, np.nan)
    tdiff.iloc[:, 1] = 1e30
    tdiff.iloc[:, 2] = obs.diff(axis=1).iloc[:, 2:]
    tdiff.to_csv(tdiff_file, index=None)

    return


def main():

    try:
       os.remove(r'profiles-diff.csv')
    except Exception as e:
       print(r'error removing tmp file:profiles-diff.csv')
    try:
       os.remove(r'profiles-tdiff.csv')
    except Exception as e:
       print(r'error removing tmp file:profiles-tdiff.csv')
    try:
       os.remove(r'flows.csv')
    except Exception as e:
       print(r'error removing tmp file:flows.csv')
    pyemu.helpers.apply_list_and_array_pars(arr_par_file='mult2model_info.csv',chunk_len=50)
    flows_from_fracs()
    pyemu.os_utils.run(r'python run_model.py')

    obs_diff_from_sim()

if __name__ == '__main__':
    mp.freeze_support()
    main()

