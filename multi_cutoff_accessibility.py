# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 13:20:14 2014@author: mdowd
A function to calculate accessibiility from a each zone to some a

"""

from math import exp
import numpy as np
from pandas import DataFrame, read_csv, read_excel
import pandas as pd
import os
def multi_gamma_access(path, access_unit, access_label, Inundation_Percent_label, base_vector_sum, intra_zonal=False):
    """
    ________
    Packages necessary: Pandas, numpy
    ________
    
    matrix: must be a travel matrix in csv format.
        <<<<>>>>>
    matrix_label: is whatever value is found in the upper left most corner of the matrix above.Open CSV to check
        <<<<>>>>>    
    access_unit: must be csv table, it can have multiple fields. This should be something like a table of
        of various zonal information.
        <<<<>>>>>    
    access_label: this is the Column Name of the access measue you are interested in.
        <<<<>>>>>    
    cutoff: This is a value whereby all areas below the cutoff have full access to access_units
        in other words if the cutoff is 30 minutes, then any zone that can be reached in 30 minutes
         from another zone will be considered to have full access to that access unit. 
        <<<<>>>>>
    function: Either "Gamma" or "Exp"; when using gamma set the cutoff to zero. 
    decay_not_limt: If decay_not_limit is true then a decay function is applied over the cutoff value, if
        decay_not_limit = False then all access)units accessiblie within a certain time limit are added and
        all units not accessiblit within that time are ignored. 
        DEFAULT = True
    decay_lambda = the value that is used in the decay function that is applied for travel values over the
        cutoff value: Decay Function = Access_Unit * exp(Travel_Time * -decay_lambda5)
        DEFAULT = 0.05
        <<<<>>>>>
    diagnols: True if you want diagnol values set to zero, false if you want to include the intrazonal
        access to access_unts. 
        DEFAULT = False

    """

    
    #--------------Prepare Accessibility Unit Vector-----------------------#
    #Read in the "accessibility measure" could be persons, jobs, firms, needs to be a zonal total
    #based on the zonal unit. ie. total jobs per taz, function will return access to jobs by taz
    print 'Preparing Accessibiity Vector'
    access_data = read_csv(access_unit)
    inundation_data = read_csv(r"C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Data\General_ArcFiles\DBF_SHP_Exports\taz_perc_ind.csv")
    #Check to make sure the access unit column is actually a number, excel often converts them strings which
    #are represeneted as objects in Pandas
    if Inundation_Percent_label == '2010':
        inundation_vector = [1]*986
    else:
        prep_inundation_vector = np.array(inundation_data['perc' + Inundation_Percent_label[-1]+'ft'])
        inundation_vector = []

        for num in prep_inundation_vector:
            if num == 0.0:
                inundation_vector.append(1)
            elif num > 0.75:
                inundation_vector.append(0.0)
            else:
                inundation_vector.append(1-num)
    inundation_vector = np.array(inundation_vector)

    if isinstance(access_data[access_label], str):
        return "Access unit is not an int, or float"
    else:
        print 'Accessibility Unit is float or int'
        vector = np.array(access_data[access_label])
    del[access_data]
    vector_mask = np.isnan(vector)
    vector[vector_mask] = 0
    vector = vector * inundation_vector
    print 'Vector Sum', vector.sum()

    ###Start by making a boolean array for your condition.
    #Below mask for cut_off values, if using gamma set Cutoff equal to Zero
    
    #--------------Prepare skim-----------------------#
    #read the travel matrix skim into a --> dataframe
    #Initialize Dataframe to hold the final access measures
    access_by_zone_df = pd.DataFrame(index=[i for i in xrange(1,987)])
    os.chdir(path)
    for skim in os.listdir(path):
        skim_name = skim.split('.')[0]
        
        print 'Preparing Skim', skim_name
        df = read_csv(skim)
        name =  df.columns[0]
        df= df.drop(name, axis=1)
        

        #convert travel matriz skim dataframe to --> matrix
        dmatrix = df.as_matrix()
        di = np.diag_indices(len(dmatrix))
    
        zero_mask = dmatrix < 0.0001

        if zero_mask.sum()> 0:
            print "There are/is ", zero_mask.sum(), " zero in the skim"
            return 'Error'
        
        if skim_name[0:6] == 'skuser':
            di = np.diag_indices(len(dmatrix))
            if intra_zonal:
                intra_zonal_appx = np.array(df.min(axis = 1)) * .8
                dmatrix[di]=intra_zonal_appx
            else:
                intra_zonal_appx = 99999 
                
        if not intra_zonal:
             di = np.diag_indices(len(dmatrix))
             intra_zonal_appx = 99999 
            #set diagnols equal to 80% of the time of the minimum travel time. 
             dmatrix[di] = intra_zonal_appx
             del[df]
       
        output = np.ones(dmatrix.shape)*vector
        cutoff_mask = dmatrix > 45.0
        output[cutoff_mask] = 0
        output = output/base_vector_sum
        out_df = DataFrame(output, columns = [i for i in xrange(1,len(output)+1)], index = [i for i in xrange(1,len(output)+1)])
        #print out_df
        access_by_zone_df[skim_name] = out_df.sum(axis=1)
        
    return access_by_zone_df
    ##Example Call to function
    
def run_all(intra_zonal_val):    
    folders = ['2010','slr1','slr2','slr3','slr4','slr5','slr6']
    access_unit = r"C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\Accessiblity_Work\Access_units\csvs\Demographics.csv"
    access_label = 'COMMERCIAL'
    
    #Prep the Baseline sum of the access unit vector
    base_vector_temp = read_csv(access_unit)
    base_vector = np.array(base_vector_temp[access_label])
    del[base_vector_temp]
    base_vector_mask = np.isnan(base_vector)
    base_vector[base_vector_mask] = 0
    base_vector_sum = base_vector.sum()
    print base_vector_sum    
    
    for folder in folders:
        path = "C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\Accessiblity_Work\Skims\Nov1\skim_csv\\" +  folder
        if folder == '2010':
            data = multi_gamma_access(path, access_unit, access_label, folder, base_vector_sum, intra_zonal=intra_zonal_val)
        else:
            next_data = multi_gamma_access(path, access_unit, access_label, folder, base_vector_sum, intra_zonal=intra_zonal_val)
            data = pd.merge(data, next_data, on=data.index, how='inner')
            data = data.drop('key_0', axis=1)
        data.index = [i for i in xrange(1,987)]
    return data