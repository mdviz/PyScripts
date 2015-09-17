# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:29:14 2015

@author: mdowd
"""


from simpledbf import Dbf5
import pandas as pd
path1 = "/Users/mdowd/Desktop/PTONOFF_Year2010.DBF"
path2 = "/Users/mdowd/Desktop/PTONOFF_SLR4_Fixed.DBF" 


label1 = path1.split("/")[-1].split(".")[0][8:]
label2 = path2.split("/")[-1].split(".")[0][8:]

dbf = Dbf5(path1, codec='utf-8')
dbf1 = Dbf5(path2, codec='utf-8')

df2010 = dbf.to_dataframe()
df4ft = dbf1.to_dataframe()
df2010 = df2010[["A","MODE","LONGNAME","VOL", "ONA"]]
df4ft = df4ft[["A","MODE","LONGNAME","VOL", "ONA"]]

def nameColumns(df, label):
    baseColumns = df.columns
    newColumns = []
    for col in baseColumns:
        if col == "A":
            newColumns.append(col)
        else:
            newColumns.append(col + "_" + label)
    
    df.columns = newColumns
    return df
    
df2010 = nameColumns(df2010, label1)
df4ft = nameColumns(df4ft, label2)

dfg1 = df2010.groupby("A").sum()
dfg2 = df4ft.groupby("A").sum()
dfg1["A"] = dfg1.index
dfg2["A"] = dfg2.index
df = pd.merge(dfg1,dfg2,on="A", how = "left")
df["diff"] = df["ONA_SLR4_Fixed"] - df["ONA_Year2010"]