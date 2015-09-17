# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 16:22:53 2015

@author: mdowd
"""

import shutil


#relative_path = "D:\User_Documents\Dowd_Michael\MODELS"
fixed_path = 'March13Model\CubeCatCong\Base'
relative_path = "I:\Backups"

outpath = "C:\Users\mdo\Desktop\Copied"

def c(someString):
    return someString.replace("/", "//")


walkSkims = ["Year 2010\WALK_Year 2010.MAT",
               "Year 2010\SLR1\SLR1_Fixed\WALK_SLR1_Fixed.MAT",
               "Year 2010\SLR2\SLR2_Fixed\WALK_SLR2_Fixed.MAT",
               "Year 2010\SLR3\SLR3_Fixed\WALK_SLR3_Fixed.MAT",
               "Year 2010\SLR4\SLR4_Fixed\WALK_SLR4_Fixed.MAT",
               "Year 2010\SLR5\SLR5_Fixed\WALK_SLR5_Fixed.MAT",
               "Year 2010\SLR6\SLR6_Fixed\WALK_SLR6_Fixed.MAT"]


def copyFiles(src, dest):
    shutil.copyfile(src,dest)
    
def copyAllFiles(pathList, outpath):
    for a_file in pathList:
        fl = c(relative_path) + "\\" + c(fixed_path) + "\\" + c(a_file)
        out = c(outpath) + "\\" + a_file.split("\\")[-1]
        copyFiles(fl, out)