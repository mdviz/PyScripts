# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 12:29:08 2015

@author: mdowd
"""

import os
import pandas as pd
#path = "C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\ImpactModeling\ScenarioModeling\Iter1_ScenarioModeling"
#path_contents = os.listdir(path)
#outpath = "C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\ImpactModeling\ScenarioModeling\TransitOuputs"
#path_file = "C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\ImpactModeling\ScenarioModeling\RidershipPaths.txt"
""" FORMAT FOR ITERATING: >>> for i in path_contents: transit_loads(path + "\\"+ i) <---"""

#lookup = "C:\\Users\\mdo\\Desktop\\MIT\\MIT_Fall2014\\Thesis\\MiscPythonSQL\\thesis\\tripPurposeLookup.csv"
lookup = "D:\\User_Documents\\Dowd_Michael\\Python\\thesis\\tripPurposeLookup.csv"

#relative_path = "I:\Backups"
relative_path = "D:\User_Documents\Dowd_Michael\MODELS"
fixed_path = 'March13Model\CubeCatCong\Base'
outpath = "C:\Users\mdo\Desktop"

paths2010fixed      = ["Year 2010\Lost_Print_SLR0",
                       "Year 2010\SLR1\SLR1_Fixed\Lost_Print_SLR1",
                       "Year 2010\SLR2\SLR2_Fixed\Lost_Print_SLR2",
                       "Year 2010\SLR3\SLR3_Fixed\Lost_Print_SLR3",
                       "Year 2010\SLR4\SLR4_Fixed\Lost_Print_SLR4",
                       "Year 2010\SLR5\SLR5_Fixed\Lost_Print_SLR5",
                       "Year 2010\SLR6\SLR6_Fixed\Lost_Print_SLR6"]
                       
paths2010variable   =  ["Year 2010\Lost_Print_SLR0",
                        "Year 2010\SLR1\SLR1_Variable\Lost_Print_SLR1",
                        "Year 2010\SLR2\SLR2_Variable\Lost_Print_SLR2",
                        "Year 2010\SLR3\SLR3_Variable\Lost_Print_SLR3",
                        "Year 2010\SLR4\SLR4_Variable\Lost_Print_SLR4",
                        "Year 2010\SLR5\SLR5_Variable\Lost_Print_SLR5",
                        "Year 2010\SLR6\SLR6_Variable\Lost_Print_SLR6"]

                        
pathScenaro1Fixed   =  ["Sc1_2030\Lost_Print_SLR0",
                        "SC1_2030_NOBUS\Lost_Print_SLR0",
                        "Sc1_2030_OuterBus\Lost_Print_SLR0",
                        "Sc1_2030\SC1_2030_4ft_Fixed\Lost_Print_SLR4",
                        "SC1_2030_NOBUS\SC1_2030_NOBUS_4ft_Fixed\Lost_Print_SLR4",
                        "Sc1_2030_OuterBus\SC1_2030_OuterBus_4ft_Fixed\Lost_Print_SLR4"]
                        
pathScenaro2Fixed  =   ["Sc2_2030\Lost_Print_SLR0",
                        "SC2_2030_NOBUS\Lost_Print_SLR0",
                        "Sc2_2030_OuterBus\Lost_Print_SLR0",
                        "Sc2_2030\SC2_2030_4ft_Fixed\Lost_Print_SLR4",
                        "SC2_2030_NOBUS\SC2_2030_NOBUS_4ft_Fixed\Lost_Print_SLR4",
                        "Sc2_2030_OuterBus\SC2_2030_OuterBus_4ft_Fixed\Lost_Print_SLR4"]
                        
pathScenaro1Variable  = ["Sc1_2030\Lost_Print_SLR0",
                        "SC1_2030_NOBUS\Lost_Print_SLR0",
                        "Sc1_2030_OuterBus\Lost_Print_SLR0",
                        "Sc1_2030\SC1_2030_4ft_Variable\Lost_Print_SLR4",
                        "SC1_2030_NOBUS\SC1_2030_NOBUS_4ft_Variable\Lost_Print_SLR4",
                        "Sc1_2030_OuterBus\SC1_2030_OuterBus_4ft_Variable\Lost_Print_SLR4"]
                    
pathScenaro2Variable   = ["Sc2_2030\Lost_Print_SLR0",
                          "SC2_2030_NOBUS\Lost_Print_SLR0",
                          "Sc2_2030_OuterBus\Lost_Print_SLR0",
                          "Sc2_2030\SC2_2030_4ft_Variable\Lost_Print_SLR4",
                          "SC2_2030_NOBUS\SC2_2030_NOBUS_4ft_Variable\Lost_Print_SLR4",
                          "Sc2_2030_OuterBus\SC2_2030_OuterBus_4ft_Variable\Lost_Print_SLR4"]
                        
            
def constructPaths(pathList):
    paths = []
    for i in pathList:
        paths.append(relative_path + "\\" + fixed_path + "\\" + i)
    return paths

def getLostTrips(path, scenario=False):
    """ 
    Takes in one Lost Trip File and Calcualtes the Reduction from the baseline totals    
    """
    with open(path, 'r') as f:
       lines = f.readlines()
    if not scenario:
        slr_lvl = path.split("_")[-1]
    else:
        slr_lvl = path.split("\\")[-2]
    
    splitLines = []
    start_index = None
    total_val = 'Totals after Iteration 1 I loop:\n'
    for index, line in enumerate(lines):
        if line == total_val:
            print "Success", index
            start_index = index
            break
    
        
    lines = lines[start_index:len(lines)]
    for line in lines:
        line = line.replace(":", " ")
        line = line.replace(",", "")
        splitLine = " ".join(line.split())
        #Below checks if the line is an MI or an MO
        if (splitLine[0:2] == "MI" or splitLine[0:2] == "MW"):
            #Below skips the travel time matrices that are MI's
            if ((splitLine[0:2] == "MI") and (int(splitLine[3:5]) < 13)) or (splitLine[0:2] == "MW"):
                info = splitLine.split(" ")
                #Remove thousands commas
                print info
                #NHBW/NHBO Always have Zero for PTDRIVE
                #Below Controls for that
                try: 
                    float(info[1])
                    #Convert the trips to a number with the float()
                    splitLines.append([info[0], float(info[1])])
                except ValueError:
                    print info[0], info[1]
                    splitLines.append([info[0], 0])
            
    #I know this number of trip purposes will always be the same
    #so that is why I am using number 40 instead of a dynamic number

    original            = pd.DataFrame(splitLines[0:42])
    new                 = pd.DataFrame(splitLines[42:len(splitLines)])

    original.columns    = ["Input", "BaseTotal"]
    new.columns         = ["Output","NewTot_"+ slr_lvl]
    df = pd.merge(original, new, left_index=True, right_index=True, how='outer')
    df["Lost_"+ slr_lvl] = df.BaseTotal - df["NewTot_"+slr_lvl]
    df["LostPerc" + slr_lvl] = df["Lost_"+slr_lvl] / df.BaseTotal
    return df    
    



def compareLostTrips(paths, scenario=False):
    paths = constructPaths(paths)
    out_files = []
    for File in paths:
        out_files.append(getLostTrips(File, scenario))
        
    first = True
    for item in out_files:
        if first:
            df =  item
            print df
            first = False
        else:
            df2 = item
            df2 = df2.drop(['Output','BaseTotal'], axis=1)
            df = pd.merge(df, df2, on='Input', how='outer')
    
    l = pd.read_csv(lookup)
    df = pd.merge(df, l, on = 'Input', how='outer')
       
    Base, NewTot, Lost_, LostPerc = [],[],[],[]
    for col in df.columns:
        if 'NewTot' in col:
            NewTot.append(col)
        elif 'Lost_' in col:
            Lost_.append(col)
        elif 'LostPerc' in col:
            LostPerc.append(col)
        else:
            Base.append(col)
    
    #Groups by Mode
    ModeGroup = df[["Mode", "BaseTotal"] + Lost_].groupby('Mode').sum()
    for col in Lost_:
        ModeGroup["Perc_" + col] = ModeGroup[col]/ModeGroup["BaseTotal"]
        
    #groups by TPURP
    TpurpGroup = df[["TPURP", "BaseTotal"] + Lost_].groupby('TPURP').sum()
    for col in Lost_:
        TpurpGroup["Perc_" + col] = TpurpGroup[col]/TpurpGroup["BaseTotal"]
        
    #Choice Captive
    ChoCapGroup = df[["ChoiceCaptive", "BaseTotal"] + Lost_].groupby('ChoiceCaptive').sum()
    for col in Lost_:
        ChoCapGroup["Perc_" + col] = ChoCapGroup[col]/ChoCapGroup["BaseTotal"]
        
        
        
    orderedColumns = Base + NewTot + Lost_ + LostPerc
    df = df[orderedColumns]
    return df, ModeGroup, TpurpGroup, ChoCapGroup
    
#Call
a,b,c,d= compareLostTrips(pathScenaro2Variable, True)    
    
total = []
for col in a.columns:
    if "New" in col:
        total.append(col)

out = a[["Input"]+total]    
        #Summary Command for Excel
       #a[["Input"]+total].to_clipboard()
     