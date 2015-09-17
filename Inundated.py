# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 16:33:25 2014

@author: mdowd
"""

import pandas as pd
time_matrix = pd.read_csv(r"C:\Users\mdo\Desktop\test_data.csv")
name =  time_matrix.columns[0]
time_matrix = time_matrix.drop(name, axis=1)

#Set Diagnols, won't need to tdo this in real script
time_matrix[time_matrix == 0] = 5

mask = 