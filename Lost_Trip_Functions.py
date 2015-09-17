# -*- coding: utf-8 -*-
"""
Created on Mon Nov 03 18:00:20 2014

@author: mdowd
"""
import pandas as pd
skim = r"C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\Accessiblity_Work\Skims\Nov1\skim_csv\slr6\timeauto_slr6.csv"
od = r"C:\Users\mdo\Desktop\auto_trip_OD.csv"
percent_prop = r"C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Data\General_ArcFiles\DBF_SHP_Exports\taz_prop_inundatedNov5th.csv"

def update_od_matrix(skim, od_matrix, cutoff, prop_ind_csv, slr_level):


    #TAZ Index
    taz_index = [i for i in xrange(1,987)]
    #Set Up Skim
    skim = pd.read_csv(skim)
    skim.index = taz_index
    name =  skim.columns[0]
    skim= skim.drop(name, axis=1)
    
    #Set Up Trip Matrix
    od = pd.read_csv(od_matrix)
    od.index = taz_index
    name = od.columns[0]
    od = od.drop(name, axis = 1)
    
    #Set up Proportion Inundated Matrix
    prop_ind = pd.read_csv(prop_ind_csv)
    prop_ind_vector = prop_ind['perc' + slr_level]
    
    
    
    #Create Masks
    mask = skim < cutoff
    mask500 = skim < 500
    mask180 = skim < 180
    mask120 = skim < 120
    maskBase = skim > 0
    
    print 'm120', mask120.sum().sum()
    print 'm180', mask180.sum().sum()
    print 'm500', mask500.sum().sum()
    print 'maskBase', maskBase.sum().sum()
    print ' ' * 30 + '\n'
    working_od = od.copy()
    working_skim = skim.copy()
    working_skim[mask != True] = None
    working_skim[mask] = 1
    
    lost_trips = working_od[working_skim != 1].sum().sum()
    print 'Lost Trips',  lost_trips
    remaining_trips = working_od[working_skim == 1].sum().sum()
    print 'Remaining Trips', remaining_trips
    print 'Original Total', od.sum().sum()
    print 'Current Total', lost_trips + remaining_trips
    
    working_od[working_skim != 1] = 0
    
    print 'Values returned in the following order: working_od, od, skim, prop_ind_vector'
    return working_od, od, skim, prop_ind_vector
    
def change_shape(alpha_matrix):
    globList = []
    alpha_matrix = alpha_matrix.as_matrix()
    alpha_matrix = alpha_matrix.tolist()
    for row in range(0, len(alpha_matrix)):
        for col in range(0, len(alpha_matrix)):
            globList.append([row + 1, col + 1, alpha_matrix[row][col]])
    key_pair_alphas = pd.DataFrame(globList, columns =['o','d','time'])
    return key_pair_alphas

