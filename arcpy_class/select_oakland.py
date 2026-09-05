import arcpy

WORKSPACE = r"X:\arcGIS\GIS-Tutorial\Python-for-ArcGIS-Pro\Chapter2\Chapter2\Chapter2\Chapter2.gdb"
input_fc = r"X:\arcGIS\GIS-Tutorial\Python-for-ArcGIS-Pro\Chapter2\Chapter2\Chapter2\CPAD_2020b_Units.shp"
output_fc = f"{WORKSPACE}\\Oklandparks"
buffer_fc = f"{WORKSPACE}\\Oklandparks_1000ft"

# Test for existence of locks
def test_for_locks():
    for path in (input_fc, output_fc, buffer_fc):
        if not arcpy.Exists(path):
            print(f"Does not exist: {path}")
        elif arcpy.TestSchemaLock(path):
            print(f"Exclusive schema lock available: {path}")
        else:
            print(f"Cannot acquire exclusive schema lock: {path}")

def main():
    # first test the for schema lock
    if test_for_locks:
        print(f"Schema lock exist")
    print(f"No schema lock!")

    arcpy.env.workspace = WORKSPACE
    for path in (WORKSPACE, input_fc):
        if not arcpy.Exists(path):
            raise FileNotFoundError(f"Required input or workspace not found: {path}")

    # Check both outputs before creating anything; preserve existing results.
    for path in (output_fc, buffer_fc):
        if arcpy.Exists(path):
            raise FileExistsError(f"Output already exists. Choose a new output name: {path}")

    try:
        arcpy.analysis.Select(
            input_fc, output_fc, "AGNCY_NAME = 'Oakland, City of'"
        )
        count = int(arcpy.management.GetCount(output_fc)[0])
        print(f"Created {output_fc} ({count} parks)")
        if count == 0:
            print("No parks matched. Check AGNCY_NAME values; buffer was skipped.")
            return

        arcpy.analysis.Buffer(
            in_features=output_fc,
            out_feature_class=buffer_fc,
            buffer_distance_or_field="1000 FEET",
            dissolve_option="LIST",
            dissolve_field=["UNIT_NAME"],
        )
        print(f"Created {buffer_fc}")

        # Create a temporary layer of the bus stops.
        stops_fc = f"{WORKSPACE}\\UniqueStops_Oklandparks"
        result = arcpy.management.MakeFeatureLayer(
            stops_fc,
            "AC_TransitStops_Summer21"
        )

        # Get the actual layer from the Result object.
        stops_layer = result.getOutput(0)

        # Select bus stops that intersect the parks' 1,000-foot buffer.
        arcpy.management.SelectLayerByLocation(
            in_layer=stops_layer,
            overlap_type="INTERSECT",
            select_features=buffer_fc,
            selection_type="NEW_SELECTION"
        )

        # GetCount respects the layer's selection.
        selected_count = int(arcpy.management.GetCount(stops_layer)[0])
        print(f"Selected {selected_count} bus stops")

        # Save the selected stops as a permanent feature class.
        selected_stops_fc = f"{WORKSPACE}\\OaklandStops_Within1000ft"

        arcpy.management.CopyFeatures(
            in_features=stops_layer,
            out_feature_class=selected_stops_fc
        )

        print(f"Created: {selected_stops_fc}")
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
        raise


if __name__ == '__main__':
    main()
