# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# ProjectToWGS.py
# Created on: 2015-03-21 17:37:50.00000
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
import time

## Correct paths if they are copy & pasted from windows explorer
def c(some_string):
	some_string = some_string.replace("\\", "/")
	return some_string

#Set WorkSpace
wrk_space = c("D:\User_Documents\Dowd_Michael\CubeDataBridge\SHP")
env.workspace = wrk_space
env.overwriteOutput = True
print "workspace set"


# Local variables:
BaseSuba = "BaseSuba"
BaseSuba_Project = c("D:\User_Documents\Dowd_Michael\CubeDataBridge\PRJ_SHP")

def FromCubetoWGS1984(shapefile):
	# Process: Project
	arcpy.Project_management(BaseSuba, BaseSuba_Project, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", 
		"", "PROJCS['NAD_1983_StatePlane_Massachusetts_Mainland_FIPS_2001_Feet',GEOGCS['GCS_GRS_1980',DATUM['D_GRS_1980',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',656166.665808],PARAMETER['False_Northing',2460625.0],PARAMETER['Central_Meridian',-71.5],PARAMETER['Standard_Parallel_1',42.68333333333333],PARAMETER['Standard_Parallel_2',41.71666666666667],PARAMETER['Latitude_Of_Origin',41.0],UNIT['Foot_US',0.30480061]]")

