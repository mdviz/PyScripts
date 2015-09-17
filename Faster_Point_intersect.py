#########################################################################################################
"""

"""
#########################################################################################################
print "Importing Modules"
import arcpy
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
import time
print "Modules Imported"

## Correct paths if they are copy & pasted from windows explorer
def c(some_string):
    some_string = some_string.replace("\\", "/")
    return some_string

#Set WorkSpace
wrk_space = c("C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Data\General_ArcFiles\General.gdb")
#wrk_space = c("C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\CubeCatFF\Base\GDB_BostonRev_B.gdb")
env.workspace = wrk_space
env.overwriteOutput = True
print "workspace set"



#########################################################################################################
#####   Point Layer
#########################################################################################################
start = 'slrp_6ft'
slr_list = ["slrp_1ft", "slrp_2ft", "slrp_3ft","slrp_4ft", "slrp_5ft", "slrp_6ft"]

def fast_point_layer_slr(point_asset, slr_list = ["slrp_1ft", "slrp_2ft", "slrp_3ft","slrp_4ft", "slrp_5ft", "slrp_6ft"] ):
    #Sea Level Rise Files 
    start_time = time.time()
    lyr = "_lyr"

    # Add a field that will record the first sea level with which the asset intersects
    # Delete the field first - could be removed after debugging and competion of total script
    try:
        arcpy.DeleteField_management(point_asset, 'slr_lvl')
        arcpy.AddField_management(point_asset, 'slr_lvl', "SHORT", 2, "", "", "", "NULLABLE", "NON_REQUIRED")
    except:
        arcpy.AddField_management(point_asset, 'slr_lvl', "SHORT", 2, "", "", "", "NULLABLE", "NON_REQUIRED")

    ## Add Fields to hold Binary for whether or not asset intersects at each level
    for slr_shp in slr_list:
        print "AT Sea Level Rise Layer:  ", slr_shp
        #Delete the Field in Case of Mistakes
        try:
            arcpy.DeleteField_management(point_asset, slr_shp)
            arcpy.AddField_management(point_asset, slr_shp, "SHORT", 2, "", "", "", "NULLABLE", "NON_REQUIRED")
        except:
            arcpy.AddField_management(point_asset, slr_shp, "SHORT", 2, "", "", "", "NULLABLE", "NON_REQUIRED")

    #Need to Create Feature Layer to run SelectLayerByLocation
    
    print "Fields added & Feature Layers Created"
    where = None
    prev_shape = 'slrp_6ft'
    
    for slr_shp in slr_list[::-1]:
        arcpy.MakeFeatureLayer_management(slr_shp, slr_shp + lyr)
        where = "\"%s\" = %s" % (prev_shape, 1)
        
        if slr_shp == 'slrp_6ft':
            arcpy.MakeFeatureLayer_management(point_asset, point_asset + lyr)
        else:
           arcpy.MakeFeatureLayer_management(point_asset, point_asset + lyr, where)
        #Select based on Location
        arcpy.SelectLayerByLocation_management(point_asset + lyr,"INTERSECT", slr_shp + lyr)
        
        print "Update cursor iterating"

        with arcpy.da.UpdateCursor(point_asset + lyr, (slr_shp,'slr_lvl',)) as cursor:
            for row in cursor:
                row[0] = 1
                row[1] = int(slr_shp.split('_')[1][0])
                cursor.updateRow(row)
        
        #Release the Select By Location Created Above
        arcpy.SelectLayerByAttribute_management(point_asset + lyr, "CLEAR_SELECTION")
        arcpy.Delete_management(point_asset + lyr)
        print "cleared selection"

        prev_shape = slr_shp
        print "processed ", slr_shp
    print "DONE"
    print "time", round((time.time() - start_time)/60,5), " minutes"
