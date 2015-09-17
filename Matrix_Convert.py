# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 18:13:59 2014

@author: mdowd
"""
import numpy as np
t = np.matrix([[31,22,63],[14,55,6],[8,33,22]])

def change_shape(t):
    for row in range(len(t)):
        for col in range(len(t)):
            print row+1, col+1, np.array(t)[row][col]


            
change_shape(t)