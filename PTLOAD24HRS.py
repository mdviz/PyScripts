# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 16:42:46 2015

@author: mdowd
"""
import os
import pandas as pd
#path = "C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\ImpactModeling\ScenarioModeling\Iter1_ScenarioModeling"
#path_contents = os.listdir(path)
#outpath = "C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\ImpactModeling\ScenarioModeling\TransitOuputs"
#path_file = "C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\ImpactModeling\ScenarioModeling\RidershipPaths.txt"
""" FORMAT FOR ITERATING: >>> for i in path_contents: transit_loads(path + "\\"+ i) <---"""

path_file = "C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\ImpactModeling\ScenarioModeling\Iter2_TEMPpaths.txt"
outpath = "C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\ImpactModeling\ScenarioModeling\TransitOuputs\Iter2Ridership"
#This function parses a text file for the different paths I need, I want to add 
#some options to it to select only specific seciton for now it will return all 
#entries in the text file.
def load_file_list(path_file):
    with open(path_file, 'r') as p:
        paths = p.readlines()
    files = []
    for line in paths:
        this_file = line.split(',')
        if len(this_file) > 1:
             files.append(this_file[1].strip(' ').strip('\n'))
    return files

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
            base_columns[i+1]= v + label
        data.columns = base_columns
        return data

def Create_Tables(path_file, outpath):
    """This funciton will use all other functions to produce a single runable function to
    create the output. It will use load_file_list to get paths then run the transit_loads
    function while appending the returned file name from transit loads to a list. It will then
    call aggregate output witht that list"""
    files = load_file_list(path_file)
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
    
    return [df, dfPass, dfTime, dfPdist, dfPHrs]
        
    
    