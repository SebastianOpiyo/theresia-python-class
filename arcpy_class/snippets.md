import arcpy

# Configs

WORKSPACE = r"X:\arcGIS\projects\pilot_cleanup\Athi_meterbox_working.gdb"
METERBOXES = "CUSTOMER_METERS"

# Set workspace

arcpy.env.workspace = WORKSPACE

# Full path to the feature class/layer

mb_path = f"{WORKSPACE}\\{METERBOXES}"

# Check if it exists

if arcpy.Exists(mb_path):
    print(f"Layer found: {METERBOXES}\n")

    # List all fields
    fields = arcpy.ListFields(mb_path)

    print(f"{'Field Name':<25}{'Type':<15}{'Length':<10}{'Alias'}")
    print("-" * 70)
    for field in fields:
        print(f"{field.name:<25}{field.type:<15}{str(field.length):<10}{field.aliasName}")
else:
    print(f"Layer not found at: {lv_lines_path}")

# ArcPy Tools: Geoprocessing using ArcPy

Use the following tools in the python window:

- select
- buffer
- Make feature layer
- Select by feature layer
- Select layer by location
- Copy feature
- 
- Assignement:
  1. Use python to find all the bus stops in Oakland that are within 1,000 feet of a park. The end result should be a feature class of all bus stops that fall within 1000 feet of any park. Note:- you will work mostly with CPAD_2020b_Units.shp file. for more info about the dataset, visit https://www.calands.org
  2. Examine the data of CPAD_2020b_Units.shp - Open the attribute table
  3. Write a selection query code: `arcpy.analysis.Select('CPAD_2020b_Units', 'CPAD_2020b_Units_Oakland',"AGNCY_NAME=\'Oakland, City of\'")`
  4. Create a buffer of 1000 feet for the parks. You will have such `arcpy.analysis.Buffer("FireStations_CA", "FireStations_CA_2500ft", "2500 FEET", "", "", "LIST", ["COUNTY_NAME"])`
  5. When done use the Make Feature Layer tool to make the a feature layer of the bus stops feature class, that will be used for selecting the bus stops within the 1000 foot buffer of the parks.
  6. To do that, type `arcpy.management.MakeFeatureLayer("UniqueStops_Summer21", "AC_TransitStops_Summer21")`
- 
-
