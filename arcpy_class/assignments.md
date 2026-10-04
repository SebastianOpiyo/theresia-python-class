Assignment 1: Create a FC of all bus stops that are 1000 off parks in Oakland.


1. Use python to find all the bus stops in **Oakland** that are within 1,000 feet of a park. The end result should be a feature class of all bus stops that fall within 1000 feet of any park. Note:- you will work mostly with CPAD_2020b_Units.shp file. for more info about the dataset, visit https://www.calands.org
2. Examine the data of CPAD_2020b_Units.shp - Open the attribute table
3. Write a selection query code: `arcpy.analysis.Select('CPAD_2020b_Units', 'CPAD_2020b_Units_Oakland',"AGNCY_NAME=\'Oakland, City of\'")`
4. Create a buffer of 1000 feet for the parks. You will have such `arcpy.analysis.Buffer("FireStations_CA", "FireStations_CA_2500ft", "2500 FEET", "", "", "LIST", ["COUNTY_NAME"])`
5. When done use the Make Feature Layer tool to make the a feature layer of the bus stops feature class, that will be used for selecting the bus stops within the 1000 foot buffer of the parks.
6. To do that, type `arcpy.management.MakeFeatureLayer("UniqueStops_Summer21", "AC_TransitStops_Summer21")`
7. You should get an output of `<Result 'AC_TransitStops_Summer21'>`
8. Use the feature layer `<Result 'AC_TransitStops_Summer21'>` with the `Select Layer By Location`tool to select all of the bus stops within the buffer.
9. use `arcpy.management.SelectlayerByLocation("AC_TransitStops_Summer21", "INTERSECT","Oklandparks_1000ft")`
10. Next you can export the results to a table, CSV, or feature class. To achieve these, use `arcpy.management.CopyFeatures()`


- Note: All this processes can be achieved in memory using the Data Access Module and Using Cursors --to be covered in the future.
