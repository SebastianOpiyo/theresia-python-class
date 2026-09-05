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
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
        raise


if __name__ == '__main__':
    main()
