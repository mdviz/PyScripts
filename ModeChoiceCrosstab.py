# -*- coding: utf-8 -*-

from __future__ import division

path = r'/Users/mdowd/Dropbox (MIT)/ModeChoice/biogeme/TripPurpose/HBW/Choice/ModelB_res.enu'
import pandas as pd

choice_lookup = {1:"SOV", 2:"WALK", 3:"WAT", 4:"DAT"}
captive_lookup = {1:"APAX", 2:"WALK", 3:"WAT"}

def biosimCrossTab(theFile, choiceOrCaptive):
    df = pd.read_table(theFile)
    cols = df.columns
    new_cols = []
    P_cols = []  

    #Clear some of the columns 
    for col in cols:
        if "Residual" not in col and "V_" not in col:
            new_cols.append(col)
        if "P_" in col and "P_choice" not in col:
            P_cols.append(col)
    df = df[new_cols]
    
    
    def filterbyvalue(row):
        myMax = 0
        for col in P_cols:
            if row[col] > myMax: myMax = row[col] 
                
        for col in P_cols:
           if myMax == row[col]: 
               return col.split("P_")[1]
    
    if choiceOrCaptive == "Choice":
        theLookup = choice_lookup
    else:
        theLookup = captive_lookup
    df["actual"] =  df["Choice_Id"].map(lambda x: theLookup[x])
    df["predicted"] = 0
    
    for index, row in df.iterrows():
       df.loc[index,"predicted"] =  filterbyvalue(row)

    xTab = pd.crosstab(df.actual, df.predicted)
    pTab = xTab.apply(lambda r: r/r.sum(), axis=1)
    xTab["Total"] = xTab.apply(lambda r: r.sum(), axis=1)

    return df, xTab, pTab
    
#Example Function Call
#a,b,c = biosimCrossTab(pathCaptive,"Captive")
