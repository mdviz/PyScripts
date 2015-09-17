# -*- coding: utf-8 -*-
"""
Created on Wed Nov 05 19:06:08 2014

@author: mdowd
"""
import pandas as pd
import numpy as np
percent_prop = r"C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Data\General_ArcFiles\DBF_SHP_Exports\taz_perc_ind.csv"
prop_ind = pd.read_csv(percent_prop)
prop_ind.index = [i for i in xrange(0,986)]
slr_level = '0ft'

if slr_level == '0ft':
    prop_ind_vector = 0
else:
    prop_ind_vector = np.array(prop_ind['perc' + slr_level])

fake_array = []
for row in range(986):
    fake_array.append(986*[0.0])

fake_array = np.array(fake_array)
di = np.diag_indices(len(fake_array))
fake_array[di] = prop_ind_vector
df = pd.DataFrame(fake_array, index = [i for i in xrange(1,987)], columns = [i for i in xrange(1,987)])
    
def change_shape(alpha_matrix):
    globList = []
    alpha_matrix = alpha_matrix.as_matrix()
    alpha_matrix = alpha_matrix.tolist()
    for row in range(0, len(alpha_matrix)):
        for col in range(0, len(alpha_matrix)):
            globList.append([row + 1, col + 1, alpha_matrix[row][col]])
    key_pair_alphas = pd.DataFrame(globList, columns =['o','d','time'])
    return key_pair_alphas

key_val = change_shape(df)
key_val.to_csv("C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Data\General_ArcFiles\DBF_SHP_Exports\walk_intra_slr0.csv",index=False, header = False)
