# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 13:20:14 2014@author: mdowd
A function to calculate accessibiility from a each zone to some a

"""

def gamma_access(skim, access_unit, access_label, intra_zonal=False):
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
    from math import exp
    import numpy as np
    from pandas import DataFrame, read_csv, read_excel
    import pandas as pd
    
    #--------------Prepare skim-----------------------#
    #read the travel matrix skim into a --> dataframe
    print 'Preparing Skim'
    df = read_csv(skim)
    name =  df.columns[0]
    df= df.drop(name, axis=1)

    #convert travel matriz skim dataframe to --> matrix
    dmatrix = df.as_matrix()
    di = np.diag_indices(len(dmatrix))
    if intra_zonal:
        intra_zonal_appx = np.array(df.min(axis = 1)) * .8
    else:
        intra_zonal_appx = 99999 
    
    #set diagnols equal to 80% of the time of the minimum travel time. 
    dmatrix[di] = intra_zonal_appx
    del[df]
    
    #--------------Prepare Accessibility Unit Vector-----------------------#
    #Read in the "accessibility measure" could be persons, jobs, firms, needs to be a zonal total
    #based on the zonal unit. ie. total jobs per taz, function will return access to jobs by taz
    print 'Preparing Accessibiity Vector'
    access_data = read_csv(access_unit)
    
    #Check to make sure the access unit column is actually a number, excel often converts them strings which
    #are represeneted as objects in Pandas
    if isinstance(access_data[access_label], str):
        return "Access unit is not an int, or float"
    else:
        print 'Accessibility Unit is float or int'
        vector = np.array(access_data[access_label])
    del[access_data]
    ###Start by making a boolean array for your condition.
    #Below mask for cut_off values, if using gamma set Cutoff equal to Zero
    

    ##Create Output Matrix
    output = np.ones(dmatrix.shape)*vector
    output = (output/vector.sum()) * (dmatrix**-0.503) * np.exp(-0.078*dmatrix)
    out_df = DataFrame(output, columns = [i for i in xrange(1,len(output)+1)], index = [i for i in xrange(1,len(output)+1)])
    return out_df, out_df.sum(axis=1)
    
    ##Example Call to function
   
access_unit = r"C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\oct27_2014_input_files\TAZ_986_AccessUnits_Oct27.csv"
skimPT = r"C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\oct27_2014_input_files\SKFFUSER1_2010.csv"
skimWalk = r"C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\oct27_2014_input_files\AUTO_Year2010.csv"
skimAuto = r"C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\oct27_2014_input_files\WALK_Year2010.csv"