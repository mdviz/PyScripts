# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 19:56:56 2014

@author: mdowd
"""



print "Importing Modules"
import arcpy
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
print "Modules Imported"

## Correct paths if they are copy & pasted from windows explorer
def c(some_string):
    some_string = some_string.replace("\\", "/")
    return some_string

## Delete list of tables or features
def delete(table_list):
    for table in table_list:
        arcpy.Delete_management(table, "")
        
#Set WorkSpace
wrk_space = c("C:\Users\mdo\Desktop\MIT\MIT_Fall2014\Thesis\Data\General_ArcFiles\General.gdb")
env.workspace = wrk_space
env.overwriteOutput = True
print "workspace set"


## Function Call
def poly_or_line_intersect(shape, shp_type, zone_fields='base', class_fields="#",  slr_list = ["slrp_1ft", "slrp_2ft", "slrp_3ft",\
    "slrp_4ft", "slrp_5ft", "slrp_6ft"]):
        
    """
    Function requires a field in the dataset that is being intersected that we are not summarizing by a subset of the 
    input shapefile. We want totals of all shapes by each slr layer, possibly use 
    
    <<<<Paremeters>>>>
    shape = the shape that you want to intersect with sea level rise layers, will be either a polygon or a line/polyline feature
        <<<<>>>>
    shp_type= 'Line' or 'Poly' ; Lines have a tabulated total length intersected, Polygons have an intersected total area intersecte
        <<<<>>>>
    class_fields = Data from shape that will be included in the intersected table, multiple fields can be included in a list format:
        List will be converted into Arcpy required format which is 'Field1;Field2;' so add them as ['field1','field2','field_etc']
        MUST HAVE ONE UNIQUE FIELD PRESENT MUST BE A LIST
    
    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the 
    # layer/table view within the script
    # The following inputs are layers or table views: "slr_pc_1ft"
    """
    
    #Zonefields must be separated by a semi-colon, since this is different from other functions I want the function to be called with
    #with zone_fields as a list, below converts list into proper string format for arcpy.
    #First line checks to see if class_fields is a list, and list has more than one element. 
    
    if not isinstance(class_fields, type([])):
        print 'class fields is not a list'
        return
        
       
    if isinstance(class_fields, type([])): 
        class_fields_str = ''
        zone_fields_str = '' 
        for item in class_fields: class_fields_str += item + ';'
        class_fields = class_fields_str
        
    in_class_features = shape

    table_list = []
    for slr_shp in slr_list:
        in_zone_features = slr_shp
        out_table = "C:/Users/mdo/Desktop/MIT/MIT_Fall2014/Thesis/Data/General_ArcFiles/General.gdb/"+ shape + "_" + slr_shp 
        
        #populate a table list: A list of the tabulate intersection table names
        table = shape+"_"+slr_shp
        table_list.append(table)        
        
        if shp_type == "Poly":
            #TABULATE the Intersection
            arcpy.TabulateIntersection_analysis(
                in_zone_features,             
                zone_fields,
                in_class_features,
                out_table,
                class_fields,
                sum_fields="#",
                xy_tolerance="#",
                out_units="UNKNOWN")
            print "Tabulated Poly Intersection of", shape, "and" , slr_shp
        
        elif shp_type == "Line":
            #TABULATE the Intersection of  line 
            arcpy.TabulateIntersection_analysis(
                in_zone_features,             
                zone_fields,
                in_class_features,
                out_table,
                class_fields,
                sum_fields="#",
                xy_tolerance="#",
                out_units="METERS")
            print "Tabulated Line Intersection of", shape, "and" , slr_shp

    #I want to keep the create_new_tables 
    # Below creates new Master Table View  with unique labels for area 
    print table_list
    master_join_table = table_list[::-1][0]
    fields = arcpy.ListFields(master_join_table)
    fieldinfo = arcpy.FieldInfo()
    for field in fields:
        if shp_type == 'Poly':
            if field.name == "AREA":
                ref = "area_" + table.split('_')[-1]
                fieldinfo.addField(field.name,ref, "VISIBLE", "")
        if shp_type == 'Line':
            if field.name == "LENGTH":
                ref = "len_" + table.split('_')[-1]
                fieldinfo.addField(field.name,ref, "VISIBLE", "")
    print 'made table view'
    # The created table view will have fields as set in fieldinfo objects
    arcpy.MakeTableView_management(master_join_table, "v_master_join_table","", "", fieldinfo)   
    
    #Now iterate through the rest of the layers/
    for table in table_list[:5]:
        if shp_type == 'Poly':
            print "processing table ", table
            #add a Field to the Master Table View that will then get populated with the intersected area
            arcpy.AddField_management("v_master_join_table", "area_"+table.split('_')[-1], 'FLOAT')
            #get fields from your input feature class
            fields = arcpy.ListFields(table)
            
        elif shp_type == 'Line':
            print "processing table ", table
            #add a Field to the Master Table View that will then get populated with the intersected area
            arcpy.AddField_management("v_master_join_table", "len_"+table.split('_')[-1], 'FLOAT')
            #get fields from your input feature class
            fields = arcpy.ListFields(table)
        
        # Create a fieldinfo objects
        fieldinfo = arcpy.FieldInfo()
        
         # Iterate through the fields and set them to fieldinfo
        for field in fields:
            if shp_type == 'Poly':
                if field.name == "AREA":
                    ref = "a_" + table.split('_')[-1]
                    fieldinfo.addField(field.name,ref, "VISIBLE", "")
            elif shp_type == 'Line':
                if field.name == "LENGTH":
                    ref = "l_" + table.split('_')[-1]
                    fieldinfo.addField(field.name,ref, "VISIBLE", "")
            else: continue
        # The created table view will have fields as set in fieldinfo objects
        arcpy.MakeTableView_management(table, "v_"+ table,"", "", fieldinfo)
        arcpy.CopyRows_management("v_" + table, 'out_test')
        ##########################################################################
        #Now we want to execute the join
        #control for there being a join already in place, might need to remove the 
        #previous iteration join
        #join based on the first element of CLASS FIELDS - FIRST ELEMENT MUST BE UNIQUE
        print class_fields
        if class_fields.find(';') >= 0:
            join_field = class_fields[:class_fields.find(';')]
        else: 
            join_field = class_fields[0]
    
        try:
            arcpy.RemoveJoin_management("v_master_join_table")
        except:
            pass

        print 'Trying to executre join'

        #Execute the Join
        arcpy.AddJoin_management("v_master_join_table", join_field, "v_"+table, join_field)
        
        if shp_type == 'Poly':
            arcpy.CalculateField_management("v_master_join_table","area_" + table.split('_')[-1],
                                            "!" + table + ".a_"+table.split('_')[-1]+"!", "PYTHON")
        elif shp_type == 'Line':
            arcpy.CalculateField_management("v_master_join_table","len_" + table.split('_')[-1],
                                "!" + table + ".l_"+table.split('_')[-1]+"!", "PYTHON")
            
        arcpy.RemoveJoin_management('v_master_join_table')        
    
    #Add the area_6ft field   
    if shp_type == 'Poly':
        arcpy.AddField_management("v_master_join_table", "area_"+ master_join_table.split('_')[-1], 'DOUBLE')    
        arcpy.AddField_management("v_master_join_table", 'shp_area', 'DOUBLE')    
        arcpy.CalculateField_management("v_master_join_table","area_" + master_join_table.split('_')[-1],\
            '!AREA!', 'PYTHON')
        arcpy.DeleteField_management("v_master_join_table", ["AREA", "PERCENTAGE"])
            
        #Join and get the total area of the shape
        arcpy.AddJoin_management('v_master_join_table', join_field,in_class_features, join_field)
        arcpy.CalculateField_management('v_master_join_table', 'shp_area', '!Shape_Area!', 'PYTHON')
        arcpy.RemoveJoin_management('v_master_join_table')
        
    if shp_type == 'Line':
        arcpy.AddField_management("v_master_join_table", "len_"+ master_join_table.split('_')[-1], 'DOUBLE')    
        arcpy.AddField_management("v_master_join_table", 'shp_len', 'DOUBLE')    
        arcpy.CalculateField_management("v_master_join_table","len_" + master_join_table.split('_')[-1],\
            '!LENGTH!', 'PYTHON')
        arcpy.DeleteField_management("v_master_join_table", ["LENGTH", "PERCENTAGE"])
        
        #Calculate the total len of the shape
        arcpy.AddJoin_management('v_master_join_table', join_field,in_class_features, join_field)
        arcpy.CalculateField_management('v_master_join_table', 'shp_len', '!Shape_Length!', 'PYTHON')
        arcpy.RemoveJoin_management('v_master_join_table')
        
    #Finally Create a New Table
    arcpy.CopyRows_management('v_master_join_table', shape + '__intsct_tot' )
    #Delete the many other tables that were created
    delete(table_list)
    print 'Process Complete!'

    #Example Basic Call
    # poly_or_line_intersect('taz2727', 'Poly',class_fields = 'TAZ')
    #Example More Specific Call
    # ______