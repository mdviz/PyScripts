# -*- coding: utf-8 -*-
"""
@author: mdowd
Below code can be used to extract, format ctpp data in the format availbel from the 
current CTPP ftp site. Code will also retreive column names from the look up table provided
by the Census. 

"""
low_memory = False
from pandas import DataFrame, read_csv, read_excel
import pandas as pd

data_loc = r'C:\Users\mdo\Desktop\MIT\RA\ProjectModelFIles\CTPP_2010website\MA\25\MA_2006thru2010_A112305.csv'
ref_loc = r'C:\Users\mdo\Desktop\MIT\RA\ProjectModelFIles\CTPP_2010website\2006-2010_ctpp_lookup.tar\2006-2010_ctpp_lookup\2006-2010_ctpp_lookup\acs_2006thru2010_ctpp_table_shell.csv'

def unpack(geography, data_loc, ref_loc): #geography = the level code for info you want (tract, state, county, etc)
    data = read_csv(data_loc)
    refdata = read_csv(ref_loc)
    print 'read data'
    
    #Extract table number and use it to retreive relevant info from LookUp 
    # table.
    table_id = data_loc[data_loc.find('.')-7:data_loc.find('.')]
    LookUp = refdata.loc[refdata['TBLID']==table_id]
    print 'created lookup table'

    #Now add a colum with the identified for the type of geography we 
    #are interested in.
    data['geography']=data['GEOID'].map(lambda x: x[:3])
    
    #Subset the data based on the geography
    data = data.loc[data['geography']==geography]
    print 'subsetted data'
    
    #Retreive the Look Up value ue, ie. if LINENO = 1, then get the variable description for that code and assign it to COL
    data = pd.merge(data,LookUp,on='LINENO', how = 'outer')
    data['col']=data['LINENO'].map(lambda x: str(int(x)).zfill(3)) + '_' + data['LDESC']

    #Pivot data - essentially a group by 
    piv_data =  data.pivot_table('EST',['GEOID'],'col').fillna(0)
    data.reindex_axis(sorted(data.columns), axis=1)
    return piv_data
      
test = unpack('C13',data_loc, ref_loc)
