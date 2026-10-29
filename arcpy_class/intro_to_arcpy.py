import arcpy

# Create a workspace and a scratch workspace
WORKSPACE = r"X:\arcGIS\GIS-Tutorial\Python-for-ArcGIS-Pro\Chapter2\Chapter2\Chapter2\Chapter2.gdb"

# Assigns the workspace to the environment
arcpy.env.workspace=WORKSPACE
unique_stops_fc = "UniqueStops_Summer21"

raster_data = "CalFireFVEG_AlamedaCounty_Co"





# Entry point
if __name__ =='__main__':
    # Describe Input FC
    # Describe fc/table etc/workspace
    desc = arcpy.Describe(raster_data)
    # print(desc.shapeType)
    print(desc.spatialReference.name)
    # print(desc.fields)
    print(desc.name)
    print(desc.dataType) 
    print(desc.catalogPath)  
