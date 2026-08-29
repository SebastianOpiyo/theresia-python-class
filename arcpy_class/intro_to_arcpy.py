import arcpy

# Create a workspace and a scratch workspace
WORKSPACE = r"X:\arcGIS\GIS-Tutorial\Python-for-ArcGIS-Pro\Chapter2\Chapter2\Chapter2\Chapter2.gdb"
arcpy.env.workspace=WORKSPACE

unique_stops_fc = "UniqueStops_Summer21"
unique_stops_fc_path = f"{WORKSPACE}\\{unique_stops_fc}"

help(arcpy.management)
arcpy.Exists(unique_stops_fc_path)


if __name__ =='__main__':
    #print workspace
    # print(unique_stops_fc_path)
    help(arcpy.management)
    # print(arcpy.Exists(unique_stops_fc_path))
    # print(f"Our workspave is {WORKSPACE}")