# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 17:09:11 2015

@author: mdowd
"""

import pandas as pd
from sqlalchemy import create_engine

choice = pd.read_csv("/Users/mdowd/MIT/RA/Spring2015_ModeChoice/Survey1991/HBW_Choice.csv")
captive = pd.read_csv("/Users/mdowd/MIT/RA/Spring2015_ModeChoice/Survey1991/HBW_Captive.csv")
survey91 = pd.read_csv("/Users/mdowd/MIT/RA/Spring2015_ModeChoice/Survey1991/survey91.csv")


engine = create_engine('postgresql://postgres:killkill@localhost/postgres')
#df3.to_sql("testing222", engine)

new_columns = []
for i in choice.columns:
    new_columns.append(i.lower())
    
choice.columns = new_columns
captive.columns = new_columns
survey91.columns = new_columns

#choice.to_sql("choice91". engine)
#captive.to_sql("captive91",engine)
#survey91.to_sql("survey91", engine)