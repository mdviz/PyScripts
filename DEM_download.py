# -*- coding: utf-8 -*-
"""
Created on Tue Sep 02 12:10:49 2014

@author: mdowd
"""
#url = "http://wsgw.mass.gov/data/gispub/dtm/d221938.zip"


import urllib2

value = 221830
url_front = "http://wsgw.mass.gov/data/gispub/dtm/d"
count = 0

while value < 333842:
    url = url_front + str(value) + '.zip'
    file_name = url.split('/')[-1]
    try:
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            f.write(buffer)
        
        f.close()
        count += 1
        value += 4
    except:
        pass
print count
