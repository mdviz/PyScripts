# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import pandas as pd
import os
relative_path = "I:\\Backups"
#relative_path = "D:\User_Documents\Dowd_Michael"

baseFixed = ["Python\\netOutputs_Year 2010.PRN",
             "Python\\netOutputs_SLR1_Fixed.PRN",
             "Python\\netOutputs_SLR2_Fixed.PRN",
             "Python\\netOutputs_SLR3_Fixed.PRN",
             "Python\\netOutputs_SLR4_Fixed.PRN",
             "Python\\netOutputs_SLR5_Fixed.PRN",
             "Python\\netOutputs_SLR6_Fixed.PRN"]

baseVariable = ["Python\\netOutputs_Year 2010.PRN",
                "Python\\netOutputs_SLR2_Variable.PRN",
                "Python\\netOutputs_SLR1_Variable.PRN",
                "Python\\netOutputs_SLR3_Variable.PRN",
                "Python\\netOutputs_SLR4_Variable.PRN",
                "Python\\netOutputs_SLR5_Variable.PRN",
                "Python\\netOutputs_SLR6_Variable.PRN"]

Scenario1Fixed = ["Python\\netOutputs_Sc1_2030.PRN",
                  "Python\\netOutputs_SC1_2030_4ft_Fixed.PRN",
                  "Python\\netOutputs_SC1_2030_NOBUS.PRN",
                  "Python\\netOutputs_SC1_2030_NOBUS_4ft_Fixed.PRN",
                  "Python\\netOutputs_Sc1_2030_OuterBus.PRN",
                  "Python\\netOutputs_SC1_2030_OuterBus_4ft_Fixed.PRN"]

Scenario1Variable = ["Python\\netOutputs_Sc1_2030.PRN",
                     "Python\\netOutputs_SC1_2030_4ft_Variable.PRN",
                     "Python\\netOutputs_SC1_2030_NOBUS.PRN",
                     "Python\\netOutputs_SC1_2030_NOBUS_4ft_Variable.PRN",
                     "Python\\netOutputs_Sc1_2030_OuterBus.PRN",
                     "Python\\netOutputs_SC1_2030_OuterBus_4ft_Variable.PRN"]

Scenario2Fixed = ["Python\\netOutputs_Sc2_2030.PRN",
                  "Python\\netOutputs_SC2_2030_4ft_Fixed.PRN",
                  "Python\\netOutputs_SC2_2030_NOBUS.PRN",
                  "Python\\netOutputs_SC2_2030_NOBUS_4ft_Fixed.PRN",
                  "Python\\netOutputs_Sc2_2030_OuterBus.PRN",
                  "Python\\netOutputs_SC2_2030_OuterBus_4ft_Fixed.PRN"]

Scenario2Variable = ["Python\\netOutputs_Sc2_2030.PRN",
                     "Python\\netOutputs_SC2_2030_4ft_Variable.PRN",
                     "Python\\netOutputs_SC2_2030_NOBUS.PRN",
                     "Python\\netOutputs_SC2_2030_NOBUS_4ft_Variable.PRN",
                     "Python\\netOutputs_Sc2_2030_OuterBus.PRN",
                     "Python\\netOutputs_SC2_2030_OuterBus_4ft_Variable.PRN"]
              
              
def constructPaths(pathList):
    paths = []
    for i in pathList:
        paths.append(relative_path + "\\" + i)
    return paths
    
    
def dynamicSummary(path):
    """ 
    Takes in one Lost Trip File and Calcualtes the Reduction from the baseline totals    
    """
    with open(path, 'r') as f:
       lines = f.readlines()
    
    slr_lvl =  "_" + "".join(path.split("_")[1:]).split(".")[0]
    
    splitLines = []
    start_index =0;
    
    linkPhase = False
    begin = "Variable"
    for index, line in enumerate(lines):
        if (line == 'Begin PROCESS PHASE LINKMERGE\n'):
            linkPhase = True
        
        if linkPhase and (line[0:8] == begin):
            start_index = index
            break
    
    if start_index == 0:
        print "Error"
        return lines
    #Header holds triple tuple (start, len, length)
    header = {
        "Variable": {"loc":0,"end":0, "start":0},
            "Obs<>0":  {"loc":0,"end":0, "start":0},
                "Total":  {"loc":0,"end":0, "start":0},
                    "Ave":  {"loc":0,"end":0, "start":0},
                        "Min":  {"loc":0,"end":0, "start":0},
                            "Max":  {"loc":0,"end":0, "start":0},
                                "RMS":  {"loc":0,"end":0, "start":0}
    }
    order = ["Variable","Obs<>0","Total","Ave","Min","Max","RMS"]

    for key in header.keys():
        if key == "Obs<>0":
             header[key]["loc"] = 18
             header[key]["end"] = header[key]["loc"] + len(key)
        if key == "Variable":
            header[key]["end"] = 17
            header[key]["loc"] = 0            
        else:
            header[key]["loc"] = lines[start_index].index(key)
            header[key]["end"] = header[key]["loc"] + len(key)
        
    for index, key in enumerate(order):
        if key == "Variable" or key == "Obs<>0":
           header[key]["start"] = header[key]["loc"]
        else:
           header[key]["start"] = header[order[index-1]]["end"]
           
    def tryConvert(arg):
        try:
            float(arg)
        except:
            pass
        return arg
    
    splitLines = []
    lines = lines[start_index+2:len(lines)]
    for line in lines:
        if line[0] not in [" ","-"] and "Massachusetts Institute of Technology (MIT)" not in line \
        and "Voyager" not in line :
            Variable = line[header["Variable"]["start"]:header["Variable"]["end"]].replace(",","")
            Obs = line[header["Obs<>0"]["start"]:header["Obs<>0"]["end"]].replace(",","")
            Total = line[header["Total"]["start"]:header["Total"]["end"]].replace(",","")
            Ave = line[header["Ave"]["start"]:header["Ave"]["end"]].replace(",","")
            Min = line[header["Min"]["start"]:header["Min"]["end"]].replace(",","")
            Max = line[header["Max"]["start"]:header["Max"]["end"]].replace(",","")
            Variable 	= tryConvert("".join(Variable.split()))
            Obs 		= tryConvert(" ".join(Obs.split()))	 
            Total 	= tryConvert(" ".join(Total.split()))
            Ave 		= tryConvert(" ".join(Ave.split()))
            Min 		= tryConvert(" ".join(Min.split()))
            Max 		= tryConvert(" ".join(Max.split()))
            
         
        if len(" ".join(line.split())) > 0:
            splitLines.append([Variable,Obs,Total,Ave,Min,Max])
        else:
            break
            
    df = pd.DataFrame(splitLines)
    
    print ("Before LENGTH", len(df))
    order = [i + slr_lvl for i in order[0:6]]
    df.columns = order[0:6]
    df = df.drop_duplicates("Variable"+slr_lvl)

    
    if (df["Variable"+slr_lvl] == "EFF_SLR").sum() == 0:
        top = df.loc[0:38]
        middle = pd.DataFrame([["EFF_SLR",0,0,0,0,0]] , columns = df.columns)
        bottom = df.loc[39:]
        df = pd.concat([top, middle])
        df = pd.concat([df, bottom])
        
    print ("After LENGTH", len(df))
    df["myIndex"] = df["Variable" + slr_lvl]
    df = df[["myIndex"]+order[0:6]]
    
    
    return df
    
    

def CreateTables(paths):
    
    out_files = []
    for fl in paths:
        df = dynamicSummary(fl)
        out_files.append(df)


    df = out_files[0]
    for item in out_files[1:]:
        df = df.merge(item, on="myIndex", how="outer")
    
    
    totals, Max = [], []
    #Totals
    for col in df.columns:
        if "Total" in col:
            totals.append(col)
        if "Max" in col:
            Max.append(col)
            
    dfTotal = df[["myIndex"] + totals]    
    dfMax = df[["myIndex"] + Max]   
    
    return df, dfTotal, dfMax
    
