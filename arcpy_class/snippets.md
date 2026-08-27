
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
