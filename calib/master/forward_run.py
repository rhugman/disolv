import os
import multiprocessing as mp
import numpy as np
import pandas as pd
import pyemu
import disolv
import pandas
import os
def main():

    try:
       os.remove(r'profiles.csv')
    except Exception as e:
       print(r'error removing tmp file:profiles.csv')
    try:
       os.remove(r'flows.csv')
    except Exception as e:
       print(r'error removing tmp file:flows.csv')
    pyemu.helpers.apply_list_and_array_pars(arr_par_file='mult2model_info.csv',chunk_len=50)
    pyemu.os_utils.run(r'python run_model.py')


if __name__ == '__main__':
    mp.freeze_support()
    main()

