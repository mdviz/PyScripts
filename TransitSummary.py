# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 16:42:46 2015

@author: mdowd
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
#path = "C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\ImpactModeling\ScenarioModeling\Iter1_ScenarioModeling"
#path_contents = os.listdir(path)
#outpath = "C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\ImpactModeling\ScenarioModeling\TransitOuputs"

""" FORMAT FOR ITERATING: >>> for i in path_contents: transit_loads(path + "\\"+ i) <---"""


#2010 Fixed
paths2010fixed      = ["Year 2010\PTLOAD24HRS_Year 2010.PRN",
                       "Year 2010\SLR1\SLR1_Fixed\PTLOAD24HRS_SLR1_Fixed.PRN",
                       "Year 2010\SLR2\SLR2_Fixed\PTLOAD24HRS_SLR2_Fixed.PRN",
                       "Year 2010\SLR3\SLR3_Fixed\PTLOAD24HRS_SLR3_Fixed.PRN",
                       "Year 2010\SLR4\SLR4_Fixed\PTLOAD24HRS_SLR4_Fixed.PRN",
                       "Year 2010\SLR5\SLR5_Fixed\PTLOAD24HRS_SLR5_Fixed.PRN",
                       "Year 2010\SLR6\SLR6_Fixed\PTLOAD24HRS_SLR6_Fixed.PRN"]
#2010 Variable                     
paths2010variable   =  ["Year 2010\PTLOAD24HRS_Year 2010.PRN",
                        "Year 2010\SLR1\SLR1_Variable\PTLOAD24HRS_SLR1_Variable.PRN",
                        "Year 2010\SLR2\SLR2_Variable\PTLOAD24HRS_SLR2_Variable.PRN",
                        "Year 2010\SLR3\SLR3_Variable\PTLOAD24HRS_SLR3_Variable.PRN",
                        "Year 2010\SLR4\SLR4_Variable\PTLOAD24HRS_SLR4_Variable.PRN",
                        "Year 2010\SLR5\SLR5_Variable\PTLOAD24HRS_SLR5_Variable.PRN",
                        "Year 2010\SLR6\SLR6_Variable\PTLOAD24HRS_SLR6_Variable.PRN"]
#Scenarios Fixed
pathScenarioBase =      ["SC1_2030_NOBUS\PTLOAD24HRS_SC1_2030_NOBUS.PRN",
                         "Sc1_2030\PTLOAD24HRS_SC1_2030.PRN",
                         "Sc1_2030_OuterBus\PTLOAD24HRS_SC1_2030_OuterBus.PRN",
                         "SC2_2030_NOBUS\PTLOAD24HRS_SC2_2030_NOBUS.PRN",
                         "Sc2_2030\PTLOAD24HRS_SC2_2030.PRN",                        
                         "Sc2_2030_OuterBus\PTLOAD24HRS_SC2_2030_OuterBus.PRN"]
#Scenarios Fixed
pathScenaroFixed     = ["SC1_2030_NOBUS\SC1_2030_NOBUS_4ft_Fixed\PTLOAD24HRS_SC1_2030_NOBUS_4ft_Fixed.PRN",
                        "Sc1_2030\SC1_2030_4ft_Fixed\PTLOAD24HRS_SC1_2030_4ft_Fixed.PRN",
                        "Sc1_2030_OuterBus\SC1_2030_OuterBus_4ft_Fixed\PTLOAD24HRS_SC1_2030_OuterBus_4ft_Fixed.PRN",
                        "SC2_2030_NOBUS\SC2_2030_NOBUS_4ft_Fixed\PTLOAD24HRS_SC2_2030_NOBUS_4ft_Fixed.PRN",
                        "Sc2_2030\SC2_2030_4ft_Fixed\PTLOAD24HRS_SC2_2030_4ft_Fixed.PRN",
                        "Sc2_2030_OuterBus\SC2_2030_OuterBus_4ft_Fixed\PTLOAD24HRS_SC2_2030_OuterBus_4ft_Fixed.PRN"]
#Scenarios Variable                        
pathScenarioVariable = ["SC1_2030_NOBUS\SC1_2030_NOBUS_4ft_Variable\PTLOAD24HRS_SC1_2030_NOBUS_4ft_Variable.PRN",
                        "Sc1_2030\SC1_2030_4ft_Variable\PTLOAD24HRS_SC1_2030_4ft_Variable.PRN",
                        "Sc1_2030_OuterBus\SC1_2030_OuterBus_4ft_Variable\PTLOAD24HRS_SC1_2030_OuterBus_4ft_Variable.PRN",
                        "SC2_2030_NOBUS\SC2_2030_NOBUS_4ft_Variable\PTLOAD24HRS_SC2_2030_NOBUS_4ft_Variable.PRN",
                        "Sc2_2030\SC2_2030_4ft_Variable\PTLOAD24HRS_SC2_2030_4ft_Variable.PRN",
                        "Sc2_2030_OuterBus\SC2_2030_OuterBus_4ft_Variable\PTLOAD24HRS_SC2_2030_OuterBus_4ft_Variable.PRN"]

relative_path = "G:\\Backups"
#relative_path = "D:\User_Documents\Dowd_Michael\MODELS"
fixed_path = 'March13Model\\CubeCatCong\\Base'
#outpath = "D:\User_Documents\Dowd_Michael\TestingFolder\MarchTransitOutput"
outpath = "C:\\Users\\mdo\\Desktop\\March24TransitOut"

#This function parses a text file for the different paths I need, I want to add 
#some options to it to select only specific seciton for now it will return all 
#entries in the text file.
def constructPaths(pathList):
    paths = []
    for i in pathList:
        paths.append(relative_path + "\\" + fixed_path + "\\" + i)
    return paths

#This function will create a formatted text file of the Cube Output
def transit_loads(path, outpath):
    with open(path, 'r') as f:
       lines = f.readlines()
       
    start_index = None
    total_val = 'REPORT LINES  UserClass=Total    \n'
    for index, line in enumerate(lines):
        if line == total_val:
            start_index = index
            break
        
    lines = lines[start_index:]
    
    outname = path.split('\\')[-1].split('.')[0] + 'out.txt' 
    out_file = open( outpath +'\\'+ outname, 'w')
    
    head = False
    
    while not head:
        for line in lines:
            if line.split(' ')[0] == 'Name':
                head = line
    head = ','.join(head.split())
    
    out_file.write(head + '\n')
    for line in lines:
        try:
            int(line[17]) 
            name = line[0:17]
            data = ','.join(line[17:].replace(',','').split())
            if len(data.split(',')) > 10:
                data = ','.join(data.split(',')[0:9])
            out_file.write(name + ',' + data + '\n')
        except (IndexError, ValueError):
            continue
    return outpath + '\\' + outname

    
    
def transit_summary_prn(path, first):
    print 'In here'
    label = path.split('\\')[-1]
    label = label.strip('PTLOAD24HRS').strip('out.txt')
    #load the network
    if first:
        data = pd.read_csv(path)
        base_columns = ['Name','Mode','Op','Stp','Cr','Dist','Time', 'Pass','Pdist','PHr']
        for i in xrange(6,10):
           base_columns[i] = base_columns[i] + label
        data.columns = base_columns
        return data
    else:
        data = pd.read_csv(path)
        print data.columns
        data = data.drop(['Mode','Op','Stp','Cr','Distance'], axis=1)
        print data
        base_columns = ['Name','Time', 'Pass','Pdist','PHr']
        for i,v in enumerate(base_columns[1:len(base_columns)]):
            base_columns[i+1] = v + label
        data.columns = base_columns
        return data

def Create_Tables(pathList, outpath, scenario=False):
    """This funciton will use all other functions to produce a single runable function to
    create the output. It will use load_file_list to get paths then run the transit_loads
    function while appending the returned file name from transit loads to a list. It will then
    call aggregate output witht that list"""
    files = constructPaths(pathList)
    out_files = []
    for fl in files:
        out_files.append(transit_loads(fl, outpath))
        
    first = True
    for item in out_files:
        if first:
            df =  transit_summary_prn(item, first)
            first = False
        else:
            df2 = transit_summary_prn(item, first)
            df = pd.merge(df, df2, on='Name', how='outer')
            
    base_columns = ['Name', 'Mode', 'Stp', 'Dist']

    df = df.replace("--", 0)
    for col in df.columns[7:]:
        df[col] = df[col].astype('float')
    
    #Create specific Dataframes
    dfpass_cols, dfTime_cols, dfPdist_cols, dfPHrs_cols = [],[],[],[]
    for col in df.columns:
        if 'Time' in col:
            dfTime_cols.append(col)
        elif 'Pass' in col:
            dfpass_cols.append(col)
        elif 'Pdist' in col:
            dfPdist_cols.append(col)
        elif 'PHr' in col:
            dfPHrs_cols.append(col)
            
    dfPass = df[base_columns + dfpass_cols]
    dfTime = df[base_columns + dfTime_cols]
    dfPdist = df[base_columns + dfPdist_cols]
    dfPHrs = df[base_columns + dfPHrs_cols]
    
    if not scenario:
        #compute Difference from NO Inundation
        for col in dfPHrs_cols[1:]:
            dfPHrs["D_" + col] = dfPHrs[col] - dfPHrs[dfPHrs_cols[0]]
        for col in dfpass_cols[1:]:
            dfPass["D_" + col] = dfPass[col] - dfPass[dfpass_cols[0]]
    
    return [df, dfPass, dfTime, dfPdist, dfPHrs]
        
    
#Call
#df, dfPass, dfTime, dfPdist, dfPHrs = Create_Tables(paths2010variable, outpath)
