# -*- coding: utf-8 -*-
"""
Created on Mon Nov 03 18:00:20 2014

@author: mdowd
"""
import pandas as pd
skim = r"C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Analysis\ProductionWork\Accessiblity_Work\Skims\Nov1\skim_csv\slr6\timeauto_slr6.csv"
od = r"C:\Users\mdo\Desktop\auto_trip_OD.csv"

#Set Up Skim
skim = pd.read_csv(skim)
name =  skim.columns[0]
skim= skim.drop(name, axis=1)

#Set Up Trip Matrix
od = pd.read_csv(od)
name = od.columns[0]
od = od.drop(name, axis = 1)

#Create Masks
mask500 = skim < 500
mask180 = skim < 180
mask120 = skim < 120
maskBase = skim > 0

print 'm120', mask120.sum().sum()
print 'm180', mask180.sum().sum()
print 'm500', mask500.sum().sum()
print 'maskBase', maskBase.sum().sum()

