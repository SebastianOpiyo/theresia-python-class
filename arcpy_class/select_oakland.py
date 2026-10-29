"""Run in ArcGIS Pro's Python environment. Edit the paths below first."""
import os
import arcpy

DATA_FOLDER = r"X:\arcGIS\GIS-Tutorial\Python-for-ArcGIS-Pro\Chapter2\Chapter2\Chapter2"
WORKSPACE = os.path.join(DATA_FOLDER, "Chapter2.gdb")
PARKS = os.path.join(DATA_FOLDER, "CPAD_2020b_Units.shp")
BUS_STOPS = os.path.join(WORKSPACE, "UniqueStops_Summer21")

# Set this to a polygon feature class containing ONLY Oakland's boundary.
# Leave None only if BUS_STOPS already contains exclusively Oakland stops.
OAKLAND_BOUNDARY = None # AoI


def main():
    arcpy.env.workspace = WORKSPACE
    arcpy.env.overwriteOutput = False  # Preserve results from previous runs.
    selected_parks = os.path.join(WORKSPACE, "CPAD_2020b_Units_Oakland")
    buffer_fc = os.path.join(WORKSPACE, "Oaklandparks_1000ft")
    output_fc = os.path.join(WORKSPACE, "OaklandStops_Within1000ft")

    # Check/validate every required input and output before creating anything.
    inputs = [WORKSPACE, PARKS, BUS_STOPS]
    if OAKLAND_BOUNDARY is not None:
        inputs.append(OAKLAND_BOUNDARY)
    for path in inputs:
        if not arcpy.Exists(path):
            raise FileNotFoundError(f"Required dataset not found: {path}")
    for path in (selected_parks, buffer_fc, output_fc):
        if arcpy.Exists(path):
            raise FileExistsError(f"Choose another output name: {path}")

    # In ArcGIS Pro, add the parks shapefile to the map, right-click it,
    # and choose Attribute Table to examine AGNCY_NAME and UNIT_NAME.
    # ListFields prints field names without using a data access cursor.
    fields = [field.name for field in arcpy.ListFields(PARKS)]
    print("Park fields:", ", ".join(fields))
    if "AGNCY_NAME" not in fields:
        raise ValueError("The parks dataset must contain AGNCY_NAME.")
    # Validate UNIT_NAME,just like the AGNCY_NAME

    # 1. Select park units using the assignment's exact agency name.
    # Double quotes enclose the Python string; single quotes enclose SQL text.
    # AddFieldDelimiters supplies the field syntax required by the data format.
    field = arcpy.AddFieldDelimiters(PARKS, "AGNCY_NAME")
    query = f"{field} = 'Oakland, City of'"
    arcpy.analysis.Select(PARKS, selected_parks, query)
    park_count = int(arcpy.management.GetCount(selected_parks)[0])
    print(f"Selected {park_count} park units")
    if park_count == 0:
        raise ValueError("No parks matched; examine the AGNCY_NAME values.")

    # 2. Buffer park boundaries outward by 1,000 feet.
    # ALL merges overlapping buffers: proximity to any selected park is enough.
    # GEODESIC measures distance on the earth; FEET specifies the distance unit.
    arcpy.analysis.Buffer(
        in_features=selected_parks,
        out_feature_class=buffer_fc,
        buffer_distance_or_field="1000 FEET",
        dissolve_option="ALL",
        method="GEODESIC",
    )

    # 3. A temporary layer supports selections without changing the source.
    # MakeFeatureLayer returns a Result object; getOutput(0) retrieves its layer.
    result = arcpy.management.MakeFeatureLayer(
        BUS_STOPS, "AC_TransitStops_Summer21"
    )
    stops_layer = result.getOutput(0)
    try:
        # 4. Select bus stops inside or on the edge of the buffer polygons.
        # Tool names are case-sensitive: use SelectLayerByLocation.
        arcpy.management.SelectLayerByLocation(
            in_layer=stops_layer,
            overlap_type="INTERSECT",
            select_features=buffer_fc,
            selection_type="NEW_SELECTION",
        )

        # Agency name alone does not restrict bus stops to Oakland city limits.
        if OAKLAND_BOUNDARY is not None:
            # SUBSET_SELECTION keeps only existing matches inside Oakland.
            arcpy.management.SelectLayerByLocation(
                in_layer=stops_layer,
                overlap_type="INTERSECT",
                select_features=OAKLAND_BOUNDARY,
                selection_type="SUBSET_SELECTION",
            )
        else:
            print("Assumption: the input bus stops contain only Oakland stops.")

        # 5. Save selected stops, including geometry, to a feature class.
        # Both GetCount and CopyFeatures respect the layer's selection.
        # Zero selected stops produces an empty output feature class.
        count = int(arcpy.management.GetCount(stops_layer)[0])
        arcpy.management.CopyFeatures(stops_layer, output_fc)
        print(f"Saved {count} bus stops to {output_fc}")
    finally:
        # Remove the temporary layer; the source bus stops remain available.
        arcpy.management.Delete(stops_layer)


if __name__ == "__main__":
    try:
        main()
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))  # Detailed geoprocessing error messages.
        raise
