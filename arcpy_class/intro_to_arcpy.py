import arcpy


# CONFIGS
WORKSPACE = r"X:\arcGIS\GIS-Tutorial\Python-for-ArcGIS-Pro\Chapter2\Chapter2\Chapter2\Chapter2.gdb"
arcpy.env.workspace=WORKSPACE
input_fc =r"X:\arcGIS\GIS-Tutorial\Python-for-ArcGIS-Pro\Chapter2\Chapter2\Chapter2\CPAD_2020b_Units.shp"











# Entry point
if __name__ =='__main__':
    # Describe Input FC
    desc = arcpy.Describe(WORKSPACE)
    # print(desc.shapeType)
    # print(desc.spatialReference.name)
    # print(desc.fields)
    print(desc.name)
