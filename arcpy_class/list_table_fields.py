"""List all fields for bdiv10_customer_meter and bdiv10_customer_meter_camp."""

import arcpy

# --- set this to your GDB ---
WORKSPACE = r"X:\arcGIS\projects\MOCK\MOCK\Stage1_FDB.gdb"

TABLES = [
    "bdiv10_customer_meter",
    "bdiv10_customer_meter_camp",
]

arcpy.env.workspace = WORKSPACE

for name in TABLES:
    path = name if arcpy.Exists(name) else f"{WORKSPACE}\\{name}"
    print("=" * 72)
    if not arcpy.Exists(path):
        print(f"NOT FOUND: {name}")
        print(f"  Looked at: {path}")
        continue

    print(f"Table: {path}")
    print(f"{'Field Name':<32} {'Type':<14} {'Length':<8} {'Alias'}")
    print("-" * 72)
    for f in arcpy.ListFields(path):
        print(f"{f.name:<32} {f.type:<14} {f.length:<8} {f.aliasName}")
    print(f"Total fields: {len(arcpy.ListFields(path))}")

