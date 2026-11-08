# Create field delimeter
# where_clause
#query
# use the query in future/table selection

import arcpy

fc = r"C:\GIS\Data.gdb\Parcels"

# Example One
owner_field = arcpy.AddFieldDelimiters(fc, "OWNER")
where_clause  = f"{owner_field}='John Doe'"

arcpy.management.SelectLayerByAttribute(
    "Parcels_Lyr",
    "NEW_SELECTION",
    where_clause
)

# Example 2

area_field = arcpy.AddFieldDelimiters(fc, "AREA")
sql_where_clause = f"{area_field} < 500"  # AREA < 500

arcpy.management.SelectLayerByAttribute(
    "Parcels_Lyr",
    "NEW_SELECTION",
    sql_where_clause
)

# Multiple Condition SQL Query
sql = f"{owner_field} = 'John Doe' AND {area_field} > 1000"

# When to use field Delimeters
"""
- Building SQL Queries dynamically
- Writing scripts that may run against workspace types
- When using SelectLayerByAttribute
- using cursors with SQL filters
- Where using tools that require where clause
"""

# When not to use
"""
- You already know the db type and you writing a quick script
- When just working with file dgb in arcgis pro """

sql = "CITY = 'Nairobi'"

# arcpy.da.SearchCursor
# arcpy.da.UpdateCursor

# 1 SearchCursor - Used to read data in readonly format

# Example
with arcpy.da.SearchCursor(fc, field_list) as cursor:
    for row in cursor:
        print(row)

# Field Tokens
'''
OID@ --> Object ID
SHAPE@ --> Geometry Object
SHAPE@X --> X coordinate
SHAPE@Y --> Y coordinate
SHAPE@AREA --> Area 
SHAPE@LENGTH  --> lenth

'''

with arcpy.da.SearchCursor(
        fc,
        ["OID@", "SHAPE@X", "SHAPE@Y"]) as cursor:

    for row in cursor:
        print(row)


# UpdateCursor
# Field Tokens
'''
OID@ --> Object ID
SHAPE@ --> Geometry Object
SHAPE@X --> X coordinate
SHAPE@Y --> Y coordinate
SHAPE@AREA --> Area 
SHAPE@LENGTH  --> lenth

'''

# UpdateCursor
with arcpy.da.UpdateCursor(
        fc,
        ["SHAPE@X"]) as cursor:

    for row in cursor:
        row[0] += 1
        cursor.updateRow(row)

# deleteCursor

with arcpy.da.UpdateCursor(
        fc,
        "OID@") as cursor:
    for row in cursor:
        cursor.deleteRow(row)

