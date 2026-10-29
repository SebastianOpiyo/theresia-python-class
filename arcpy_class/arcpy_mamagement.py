import arcpy

# What we use this module for
'''
1. Create/delete datasets
2. Add/remove fields to a dataset
3. Create/Copy feature
4. Manage a gdb
5. Perform count on a dataset etc 

Graphically its an equivalent of ArcPro --> Geoprocessing Pane --> Data management Tools

Syntax
arcpy.management.<toolname>
'''

# List all the existing management tools
# help(arcpy.management.Delete)
# OR
print(dir(arcpy.management))

# Examples
# 1. Delete a feature class called ROADS
arcpy.management.Delete("ROADS")

#2. Create a file gdb
arcpy.management.CreateFileGDB('X:\projects\theresia-python-class\arcpy_class','example.gdb')

# 3. Create a feature class
arcpy.management.CreateFeatureclass(
    out_path='X:\projects\theresia-python-class\arcpy_class',
    out_name='example',
    geometry_type='POINT'
)

# 4. Adding fields to a dataset
arcpy.management.AddField(
    "Tranformer",
    "AssetID",
    "TEXT"
)

#5 Copy a feature class
arcpy.management.CopyFeatures(
    "example",
    "example_backup"
)

# 6 Create make Feature Layer
arcpy.management.MakeFeatureLayer(
    "Transformers",
    "TransformerLayer"
)

# Other Tools
arcpy.management.SelectLayerByAttribute()
arcpy.management.Append()
arcpy.management.TruncateTable("TableName")

# Important tools to learn
'''
Exists
Delete
CopyFeatures
Append
Merge
Dissolve
AddField
DeleteField
CalculateField
MakeFeatureLayer
SelectLayerByAttribute
AddIndex
CreateFileGDB
CreateFeatureclass
TruncateTable
AddGlobalIDs
EnableEditorTracking
Rename
GetCount'''









