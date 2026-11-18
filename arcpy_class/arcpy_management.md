# ArcPy Data Management: Tutorial Notes and Code Examples

## Learning goals

Use these notes to create GIS datasets, select records, manage fields, combine data, check geometry, and prepare a geodatabase for delivery. Each numbered section includes a purpose, call pattern, code example, and expected result.

`arcpy.management` exposes ArcGIS Pro's **Data Management toolbox**. These notes expand the original classroom examples and cover common workflows. The toolbox also contains specialized raster, topology, enterprise database, and other tools; explore them through the [Data Management toolbox overview](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/an-overview-of-the-data-management-toolbox.html).

`arcpy.Exists`, `arcpy.Describe`, and `arcpy.ListFields` are supporting ArcPy functions, not management tools. Buffer, Clip, and Intersect belong to `arcpy.analysis`.

## Requirements and example data

Run examples in an ArcGIS Pro notebook, its Python window, or a script using ArcGIS Pro's Python environment and an authorized license. Availability and options depend on the installed version, license, and data format.

The paths and datasets below are teaching examples. Supply your own data and adjust the names; these datasets are not included with the notes.

| Input in `C:\GIS\Data.gdb`                    | Type     | Fields used                                                   |
| ----------------------------------------------- | -------- | ------------------------------------------------------------- |
| `Roads`                                       | Polyline | `ROAD_ID`, `ROAD_NAME`, `ROAD_TYPE` (text)              |
| `Roads_North`, `Roads_South`, `Roads_New` | Polyline | Same schema as `Roads` for Append                           |
| `Parcels`                                     | Polygon  | No additional fields required                                 |
| `Counties`                                    | Polygon  | `REGION_NAME` (text), `POPULATION` (numeric)              |
| `Parks`                                       | Polygon  | No additional fields required                                 |
| `BusStops`                                    | Point    | No additional fields required                                 |
| `RoadInspections`                             | Table    | `ROAD_ID`, `CONDITION` (text), `INSPECTION_DATE` (date) |
| `SurveyCoordinates`                           | Table    | `LONGITUDE`, `LATITUDE` (numeric WGS 84 coordinates)      |

The road examples assume `ROAD_TYPE` includes `Primary`. For simple joins, use one inspection row per `ROAD_ID`; repeated keys require a deliberate one-to-many or summary workflow.

### Shared setup

Run this block before the numbered examples. Each example can then run independently. New fields such as `TUTOR_STATUS` should not already exist on the source data.

```python
import os
import arcpy

input_gdb = r"C:\GIS\Data.gdb"  # Change this path.
output_folder = r"C:\GIS\ManagementTutorial"
output_gdb = os.path.join(output_folder, "Training.gdb")

if not arcpy.Exists(input_gdb):
    raise FileNotFoundError(f"Missing input geodatabase: {input_gdb}")

os.makedirs(output_folder, exist_ok=True)
if not arcpy.Exists(output_gdb):
    arcpy.management.CreateFileGDB(output_folder, "Training.gdb")

arcpy.env.workspace = input_gdb
# Rerunning examples replaces outputs with the same names.
arcpy.env.overwriteOutput = True

roads = os.path.join(input_gdb, "Roads")
roads_north = os.path.join(input_gdb, "Roads_North")
roads_south = os.path.join(input_gdb, "Roads_South")
roads_new = os.path.join(input_gdb, "Roads_New")
parcels = os.path.join(input_gdb, "Parcels")
counties = os.path.join(input_gdb, "Counties")
parks = os.path.join(input_gdb, "Parks")
stops = os.path.join(input_gdb, "BusStops")
inspections = os.path.join(input_gdb, "RoadInspections")
coordinates = os.path.join(input_gdb, "SurveyCoordinates")
```

Use raw strings for Windows paths. Geodatabase feature classes and tables do not take `.shp` or `.dbf` extensions. Examples that edit records or schemas work on tutorial copies.

Call patterns show the main parameters, not every option. Inspect the installed tool with `help(arcpy.management.ToolName)`. Discover additional tools with `arcpy.ListTools("*_management")`.

## A. Create, copy, and organize datasets

### 1. Exists: check for a dataset

**Purpose:** Check whether an input or output exists.

**Call:** `arcpy.Exists(dataset)`.

```python
if arcpy.Exists(roads):
    print("Roads are available.")
else:
    print("Check the Roads path.")
```

**Result:** `True` or `False`. Use ArcPy's Exists for geodatabase datasets; a feature class is not an ordinary filesystem file. Exists belongs directly to `arcpy`.

### 2. CreateFileGDB: create a file geodatabase

**Purpose:** Create a container for feature classes and tables.

**Call:** `arcpy.management.CreateFileGDB(out_folder_path, out_name)`.

```python
archive_gdb = os.path.join(output_folder, "Archive.gdb")
if not arcpy.Exists(archive_gdb):
    arcpy.management.CreateFileGDB(output_folder, "Archive.gdb")
print(archive_gdb)
```

**Result:** `Archive.gdb`. The parent folder must already exist. Shared setup uses the same pattern to create `Training.gdb`.

### 3. CreateFeatureDataset: group related feature classes

**Purpose:** Create a feature dataset whose feature classes share a spatial reference, for example before building a topology.

**Call:** `arcpy.management.CreateFeatureDataset(out_dataset_path, out_name, spatial_reference)`.

```python
transport = os.path.join(output_gdb, "Transport")
road_sr = arcpy.Describe(roads).spatialReference
if road_sr.name == "Unknown":
    raise ValueError("Identify the Roads coordinate system first.")
if not arcpy.Exists(transport):
    arcpy.management.CreateFeatureDataset(output_gdb, "Transport", road_sr)
```

**Result:** An empty feature dataset, a geodatabase structure rather than a folder of shapefiles.

### 4. CreateFeatureclass: create an empty spatial dataset

**Purpose:** Define geometry and coordinate system before adding features.

**Call:** `arcpy.management.CreateFeatureclass(out_path, out_name, geometry_type, ...)`.

```python
arcpy.management.CreateFeatureclass(
    out_path=output_gdb,
    out_name="SurveyPoles",
    geometry_type="POINT",
    spatial_reference=arcpy.SpatialReference(4326),  # WGS 84
)
```

**Result:** An empty point feature class with a known spatial reference. Common types include `POINT`, `MULTIPOINT`, `POLYLINE`, and `POLYGON`. A template can copy a schema, but does not replace explicitly choosing a spatial reference. Creating the dataset does not insert features.

### 5. CreateTable: create a table without geometry

**Purpose:** Store inspection, inventory, or lookup records.

**Call:** `arcpy.management.CreateTable(out_path, out_name)`.

```python
table = os.path.join(output_gdb, "InspectionLog")
arcpy.management.CreateTable(output_gdb, "InspectionLog")
arcpy.management.AddField(table, "ROAD_ID", "TEXT", field_length=30)
arcpy.management.AddField(table, "VISIT_DATE", "DATE")
```

**Result:** An empty table with an ObjectID and the added fields. It has no Shape field.

### 6. CopyFeatures: copy geometry and attributes

**Purpose:** Create a working copy or save a layer's selected features.

**Call:** `arcpy.management.CopyFeatures(in_features, out_feature_class)`.

```python
road_backup = os.path.join(output_gdb, "Roads_Backup")
arcpy.management.CopyFeatures(roads, road_backup)
```

**Result:** A new road feature class. A layer with a selection copies selected features. A dataset path copies all features, subject to applicable geoprocessing environments.

### 7. CopyRows: copy table records

**Purpose:** Export records without creating geometry.

**Call:** `arcpy.management.CopyRows(in_rows, out_table)`.

```python
inspection_copy = os.path.join(output_gdb, "Inspections_Copy")
arcpy.management.CopyRows(inspections, inspection_copy)
```

**Result:** A new table. Use CopyFeatures when geometry must be retained.

### 8. Rename: change a dataset name

**Purpose:** Give a completed output a meaningful name.

**Call:** `arcpy.management.Rename(in_data, out_data)`.

```python
draft = os.path.join(output_gdb, "Roads_RenameDraft")
final = os.path.join(output_gdb, "Roads_Renamed")
arcpy.management.CopyFeatures(roads, draft)
if arcpy.Exists(final):
    arcpy.management.Delete(final)  # Previous tutorial output only.
arcpy.management.Rename(draft, final)
```

**Result:** The copy has a new name; the draft name no longer exists. Rename changes the dataset name, not an attribute field.

### 9. Delete: remove a dataset or temporary layer

**Purpose:** Remove an output that is no longer needed.

**Call:** `arcpy.management.Delete(in_data)`.

```python
temporary_fc = os.path.join(output_gdb, "Roads_ToDelete")
arcpy.management.CopyFeatures(roads, temporary_fc)
if arcpy.Exists(temporary_fc):
    arcpy.management.Delete(temporary_fc)
print("Dataset remains:", arcpy.Exists(temporary_fc))
```

**Result:** The tutorial copy, schema, and records are removed. Deleting a layer removes the layer object; deleting a feature class path removes the stored dataset.

### 10. GetCount: count records

**Purpose:** Validate inputs, selections, and outputs.

**Call:** `arcpy.management.GetCount(in_rows)`.

```python
result = arcpy.management.GetCount(roads)
count = int(result.getOutput(0))
print(f"Road records: {count}")
```

**Result:** The tool returns a Result object; convert its first output to an integer. With a layer selection, it counts selected records. An inherited processing extent can also restrict the count.

## B. Layers, views, and selections

### 11. MakeFeatureLayer: create a temporary feature layer

**Purpose:** Work with a selection or definition query.

**Call:** `arcpy.management.MakeFeatureLayer(in_features, out_layer, where_clause)`.

```python
road_layer = arcpy.management.MakeFeatureLayer(
    roads, "management_roads_layer", "ROAD_TYPE = 'Primary'"
).getOutput(0)
print("Primary roads visible:", arcpy.management.GetCount(road_layer)[0])
```

**Result:** A temporary layer showing primary roads. The where clause is a definition query; clearing a later selection does not remove it. A layer references stored data. Creating one in a script does not guarantee it is added to a map.

### 12. SelectLayerByAttribute: select with SQL

**Purpose:** Choose records whose attributes meet a condition.

**Call:** `arcpy.management.SelectLayerByAttribute(in_layer_or_view, selection_type, where_clause)`.

```python
layer = arcpy.management.MakeFeatureLayer(
    roads, "attribute_selection_layer"
).getOutput(0)
arcpy.management.SelectLayerByAttribute(
    layer, "NEW_SELECTION", "ROAD_TYPE = 'Primary'"
)
print("Selected:", arcpy.management.GetCount(layer)[0])
arcpy.management.CopyFeatures(
    layer, os.path.join(output_gdb, "PrimaryRoads_Selection")
)
arcpy.management.SelectLayerByAttribute(layer, "CLEAR_SELECTION")
```

**Result:** A saved feature class containing the selection. SQL text literals use single quotes; numeric values are unquoted. Use `IS NULL` for missing values and double embedded apostrophes, as in `ROAD_NAME = 'O''Connell'`.

| Selection type            | Effect                                   |
| ------------------------- | ---------------------------------------- |
| `NEW_SELECTION`         | Replace the current selection            |
| `ADD_TO_SELECTION`      | Add matches                              |
| `REMOVE_FROM_SELECTION` | Remove matches                           |
| `SUBSET_SELECTION`      | Keep matches from the existing selection |
| `SWITCH_SELECTION`      | Reverse the selection                    |
| `CLEAR_SELECTION`       | Remove the selection                     |

An active selection containing zero records differs from having no selection. With no selection, tools generally process all records allowed by the definition query.

### 13. SelectLayerByLocation: select by spatial relationship

**Purpose:** Find stops within 1,000 feet of parks without saving a buffer.

**Call:** `arcpy.management.SelectLayerByLocation(in_layer, overlap_type, select_features, ...)`.

```python
stop_layer = arcpy.management.MakeFeatureLayer(
    stops, "location_selection_layer"
).getOutput(0)
arcpy.management.SelectLayerByLocation(
    in_layer=stop_layer,
    overlap_type="WITHIN_A_DISTANCE_GEODESIC",
    select_features=parks,
    search_distance="1000 Feet",
    selection_type="NEW_SELECTION",
)
arcpy.management.CopyFeatures(
    stop_layer, os.path.join(output_gdb, "Stops_NearParks")
)
```

**Result:** A point feature class of matching stops, including those inside parks. Other relationships include `INTERSECT`, `WITHIN`, and `CONTAINS`. Direction matters: input points within polygons and input polygons containing points are different questions.

Reference: [Select Layer By Location](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/select-layer-by-location.html).

### 14. MakeTableView: filter nonspatial records

**Purpose:** Filter a table before counting, copying, or editing records.

**Call:** `arcpy.management.MakeTableView(in_table, out_view, where_clause)`.

```python
view = arcpy.management.MakeTableView(
    inspections, "poor_inspection_view", "CONDITION = 'Poor'"
).getOutput(0)
arcpy.management.CopyRows(view, os.path.join(output_gdb, "PoorInspections"))
```

**Result:** A saved table of poor-condition inspections. The view is temporary; CopyRows saves its records.

## C. Fields and calculations

### 15. AddField: add one field

**Purpose:** Extend a dataset's schema.

**Call:** `arcpy.management.AddField(in_table, field_name, field_type, ...)`.

```python
working = os.path.join(output_gdb, "Roads_AddField")
arcpy.management.CopyFeatures(roads, working)
arcpy.management.AddField(working, "TUTOR_STATUS", "TEXT", field_length=20)
```

**Result:** A new text field on the copy. Adding a field does not populate it. Choose a length that fits the expected text.

| Field type | Typical contents                                 |
| ---------- | ------------------------------------------------ |
| `TEXT`   | Names, codes, and identifiers with leading zeros |
| `SHORT`  | Small whole numbers                              |
| `LONG`   | Whole numbers within its supported range         |
| `DOUBLE` | Decimal measurements                             |
| `DATE`   | Date and time                                    |
| `GUID`   | Globally unique identifier values                |

### 16. AddFields: add several fields

**Purpose:** Build a schema with one call.

**Call:** `arcpy.management.AddFields(in_table, field_description)`.

```python
working = os.path.join(output_gdb, "Roads_AddFields")
arcpy.management.CopyFeatures(roads, working)
arcpy.management.AddFields(
    working,
    [
        ["TUTOR_STATUS", "TEXT", "Survey status", 20],
        ["TUTOR_SCORE", "LONG", "Condition score"],
        ["TUTOR_DATE", "DATE", "Survey date"],
    ],
)
```

**Result:** Three new fields. The inner lists contain name, type, alias, and, where relevant, text length.

### 17. CalculateField: populate attributes

**Purpose:** Assign constants or calculate values from existing fields.

**Call:** `arcpy.management.CalculateField(in_table, field, expression, "PYTHON3", ...)`.

```python
working = os.path.join(output_gdb, "Roads_Calculate")
arcpy.management.CopyFeatures(roads, working)
arcpy.management.AddField(working, "TUTOR_STATUS", "TEXT", field_length=20)
arcpy.management.AddField(working, "FULL_NAME", "TEXT", field_length=255)

# Outer quotes define a string; inner quotes form the Python expression.
arcpy.management.CalculateField(working, "TUTOR_STATUS", "'ACTIVE'", "PYTHON3")

# Exclamation marks identify field tokens. Handle missing names explicitly.
arcpy.management.CalculateField(
    working, "FULL_NAME", "(!ROAD_NAME! or 'Unnamed') + ' Road'", "PYTHON3"
)
```

**Result:** Populated fields. The name expression assumes the source does not already end in `Road`. On a layer with a selection, only selected records are updated. A dataset path updates all applicable records.

For a longer expression, pass a function definition using `code_block` and call it from `expression`.

### 18. CalculateGeometryAttributes: measure geometry

**Purpose:** Store area or length with explicit units.

**Call:** `arcpy.management.CalculateGeometryAttributes(in_features, geometry_property, ...)`.

```python
working = os.path.join(output_gdb, "Parcels_Measured")
arcpy.management.CopyFeatures(parcels, working)
arcpy.management.CalculateGeometryAttributes(
    in_features=working,
    geometry_property=[["AREA_HA", "AREA_GEODESIC"]],
    area_unit="HECTARES",
)
```

**Result:** `AREA_HA` contains geodesic hectares. The tool creates the field if necessary. For roads, use `LENGTH_GEODESIC` and a length unit such as `KILOMETERS`. Geodesic measurements avoid treating angular coordinates as planar distances. Recalculate stored measurements after geometry changes.

Reference: [Calculate Geometry Attributes](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/calculate-geometry-attributes.html).

### 19. AlterField: rename a field or change its alias

**Purpose:** Improve field names for delivery.

**Call:** `arcpy.management.AlterField(in_table, field, new_field_name, new_field_alias)`.

```python
working = os.path.join(output_gdb, "Roads_AlterField")
arcpy.management.CopyFeatures(roads, working)
arcpy.management.AlterField(working, "ROAD_NAME", "STREET_NAME", "Street name")
```

**Result:** The geodatabase field is renamed. An alias is a display label; scripts normally use the actual name. Changing a field's data type requires an empty table. Other changes have their own restrictions. Required system fields cannot be freely renamed or deleted.

Reference: [Alter Field](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/alter-field-properties.html).

### 20. DeleteField: remove unwanted attributes

**Purpose:** Clean the schema before sharing.

**Call:** `arcpy.management.DeleteField(in_table, drop_field)`.

```python
working = os.path.join(output_gdb, "Roads_DeleteField")
arcpy.management.CopyFeatures(roads, working)
arcpy.management.AddField(working, "TUTOR_TEMP", "TEXT", field_length=20)
arcpy.management.DeleteField(working, ["TUTOR_TEMP"])
```

**Result:** The temporary field and its values are removed. Inspect `arcpy.ListFields(working)` and each field's `required` property before building a deletion list.

## D. Combine and reshape data

### 21. Merge: combine inputs into a new dataset

**Purpose:** Consolidate road deliveries from different teams.

**Call:** `arcpy.management.Merge(inputs, output, ...)`.

```python
all_roads = os.path.join(output_gdb, "Roads_Merged")
arcpy.management.Merge([roads_north, roads_south], all_roads)
```

**Result:** A new feature class containing both inputs' records. Use field mappings when schemas differ. Merge retains individual features; it does not remove overlaps or duplicates.

### 22. Append: load an existing target

**Purpose:** Add a new delivery to an existing dataset.

**Call:** `arcpy.management.Append(inputs, target, schema_type, ...)`.

```python
target = os.path.join(output_gdb, "Roads_AppendTarget")
arcpy.management.CopyFeatures(roads, target)
before = int(arcpy.management.GetCount(target)[0])

# TEST requires matching input and target schemas.
arcpy.management.Append([roads_new], target, "TEST")

after = int(arcpy.management.GetCount(target)[0])
print("Rows added:", after - before)
```

**Result:** The target gains records. `NO_TEST` permits field differences; use field mappings to avoid losing unmatched values. It does not add missing fields to the target. Appending the same delivery repeatedly can create duplicates; this example recreates its target first.

Reference: [Append](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/append.html).

| Tool     | Output behavior             | Geometry behavior                                   |
| -------- | --------------------------- | --------------------------------------------------- |
| Merge    | Creates a new dataset       | Retains input features                              |
| Append   | Modifies an existing target | Basic append adds records without removing overlaps |
| Dissolve | Creates aggregated features | Removes boundaries according to grouping rules      |

### 23. Dissolve: aggregate by attribute

**Purpose:** Combine counties into regions and summarize population.

**Call:** `arcpy.management.Dissolve(in_features, out_feature_class, dissolve_field, statistics_fields, ...)`.

```python
regions = os.path.join(output_gdb, "Regions_Dissolved")
arcpy.management.Dissolve(
    in_features=counties,
    out_feature_class=regions,
    dissolve_field=["REGION_NAME"],
    statistics_fields=[["POPULATION", "SUM"]],
    multi_part="MULTI_PART",
)
```

**Result:** Regional features with `SUM_POPULATION`. Adjacent counties labeled `Nyanza` lose their shared boundary. Disconnected areas may form a multipart feature. Large inputs may produce tiled results, so do not always assume exactly one record per group.

### 24. MultipartToSinglepart: separate disconnected parts

**Purpose:** Give each geometry part its own record.

**Call:** `arcpy.management.MultipartToSinglepart(in_features, out_feature_class)`.

```python
singlepart = os.path.join(output_gdb, "Parcels_Singlepart")
arcpy.management.MultipartToSinglepart(parcels, singlepart)
```

**Result:** Singlepart features. `ORIG_FID` links parts to the source feature. Attributes repeat across parts, so summing copied totals can double-count source values.

## E. Coordinate systems and coordinate tables

### 25. Project: transform coordinates

**Purpose:** Create data in a spatial reference appropriate for the study area.

**Call:** `arcpy.management.Project(in_dataset, out_dataset, out_coor_system, ...)`.

```python
projected_roads = os.path.join(output_gdb, "Roads_Projected")
# Example for Nairobi only: WGS 84 / UTM zone 37S.
# Change the WKID for the actual study area and analysis.
target_sr = arcpy.SpatialReference(32737)
source_sr = arcpy.Describe(roads).spatialReference
if source_sr.name == "Unknown":
    raise ValueError("Identify the source coordinate system before projecting.")
arcpy.management.Project(roads, projected_roads, target_sr)
```

**Result:** A new dataset with transformed coordinates. If datums differ, inspect `arcpy.ListTransformations(source_sr, target_sr)` and supply an appropriate `transform_method` for the location and accuracy needed.

Reference: [Project](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/project.html).

### 26. DefineProjection: assign spatial reference metadata

**Purpose:** Correct missing or incorrect metadata when the true source system is known.

**Call:** `arcpy.management.DefineProjection(in_dataset, coor_system)`.

```python
unlabelled = os.path.join(output_gdb, "KnownWGS84_Points")
# Empty teaching example with no coordinate system assigned.
arcpy.management.CreateFeatureclass(output_gdb, "KnownWGS84_Points", "POINT")

# Use only when the intended coordinates are known to be WGS 84 lon/lat.
arcpy.management.DefineProjection(unlabelled, arcpy.SpatialReference(4326))
```

**Result:** Metadata is assigned without transforming coordinates. This example assigns it before inserting points. For existing data, verify the source system from reliable metadata; assigning a guessed system does not fix misplaced coordinates.

| Tool             | Changes coordinate values?         | Main use                                  |
| ---------------- | ---------------------------------- | ----------------------------------------- |
| DefineProjection | No                                 | Assign the known source spatial reference |
| Project          | Yes, when transformation is needed | Create data in another spatial reference  |

Reference: [Define Projection](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/define-projection.html).

### 27. XYTableToPoint: turn coordinate records into points

**Purpose:** Map survey records with longitude and latitude.

**Call:** `arcpy.management.XYTableToPoint(in_table, out_feature_class, x_field, y_field, ...)`.

```python
survey_points = os.path.join(output_gdb, "SurveyPoints")
arcpy.management.XYTableToPoint(
    in_table=coordinates,
    out_feature_class=survey_points,
    x_field="LONGITUDE",
    y_field="LATITUDE",
    coordinate_system=arcpy.SpatialReference(4326),
)
```

**Result:** Points carrying the table attributes. X is longitude and Y is latitude here. For easting and northing, specify their actual projected system. Check missing values, swapped columns, and coordinate ranges.

Reference: [XY Table To Point](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/xy-table-to-point.html).

## F. Quality checks and record removal

### 28. CheckGeometry: report geometry problems

**Purpose:** Inspect geometry before analysis or delivery.

**Call:** `arcpy.management.CheckGeometry(in_features, out_table)`.

```python
report = os.path.join(output_gdb, "Parcel_GeometryProblems")
arcpy.management.CheckGeometry(parcels, report)
print("Reported problems:", arcpy.management.GetCount(report)[0])
```

**Result:** A report with feature identifiers and problems. The input is not repaired. One feature may have several problems; an empty report does not prove all business rules are satisfied.

### 29. RepairGeometry: repair a working copy

**Purpose:** Correct supported problems after reviewing the report.

**Call:** `arcpy.management.RepairGeometry(in_features, delete_null, validation_method)`.

```python
working = os.path.join(output_gdb, "Parcels_Repaired")
arcpy.management.CopyFeatures(parcels, working)
arcpy.management.RepairGeometry(working, "KEEP_NULL", "ESRI")
arcpy.management.CheckGeometry(
    working, os.path.join(output_gdb, "Parcel_PostRepairProblems")
)
```

**Result:** The copy is modified and checked again. `KEEP_NULL` retains records with null geometry; `DELETE_NULL` removes them where supported. Compare remaining problems, counts, and shapes. Not all source or geometry errors are repairable.

Reference: [Repair Geometry](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/repair-geometry.html).

### 30. FindIdentical: report duplicate combinations

**Purpose:** Locate matching records before deleting them.

**Call:** `arcpy.management.FindIdentical(in_dataset, out_dataset, fields, ...)`.

```python
duplicates = os.path.join(output_gdb, "Road_DuplicateReport")
arcpy.management.FindIdentical(
    in_dataset=roads,
    out_dataset=duplicates,
    fields=["ROAD_ID", "Shape"],
    output_record_option="ONLY_DUPLICATES",
)
```

**Result:** A table with `IN_FID` and `FEAT_SEQ`. Records sharing a sequence match on the tested fields. Shape is compared using the tool's geometry rules and tolerances. Matching `ROAD_ID` alone is a different duplicate rule.

### 31. DeleteIdentical: remove duplicates from a copy

**Purpose:** Keep one record per identical combination after confirming the rule.

**Call:** `arcpy.management.DeleteIdentical(in_dataset, fields, ...)`.

```python
working = os.path.join(output_gdb, "Roads_Deduplicated")
arcpy.management.CopyFeatures(roads, working)
before = int(arcpy.management.GetCount(working)[0])
arcpy.management.DeleteIdentical(working, ["ROAD_ID", "Shape"])
after = int(arcpy.management.GetCount(working)[0])
print("Duplicate rows removed:", before - after)
```

**Result:** Duplicates are removed from the copy. Differences in excluded fields do not prevent deletion. If a specific record must survive, define and verify a retention rule first.

### 32. DeleteRows: delete selected records

**Purpose:** Remove records while keeping the dataset.

**Call:** `arcpy.management.DeleteRows(in_rows)`.

```python
working = os.path.join(output_gdb, "Roads_DeleteRows")
arcpy.management.CopyFeatures(roads, working)
layer = arcpy.management.MakeFeatureLayer(
    working, "delete_rows_layer"
).getOutput(0)
arcpy.management.SelectLayerByAttribute(
    layer, "NEW_SELECTION", "ROAD_TYPE IS NULL"
)
selected = int(arcpy.management.GetCount(layer)[0])
if selected > 0:
    arcpy.management.DeleteRows(layer)
print("Rows removed:", selected)
```

**Result:** Selected records are deleted from the copy. With no selection, DeleteRows deletes all applicable records. Check the selection before calling it.

### 33. TruncateTable: empty a dataset

**Purpose:** Clear staging data before a full reload.

**Call:** `arcpy.management.TruncateTable(in_table)`.

```python
staging = os.path.join(output_gdb, "Inspection_Staging")
arcpy.management.CopyRows(inspections, staging)
arcpy.management.TruncateTable(staging)
print("Rows remaining:", arcpy.management.GetCount(staging)[0])
```

**Result:** The table retains its fields and has zero rows. TruncateTable ignores selections and cannot be rolled back. Restrictions include no support for versioned data or feature classes with attachments.

| Tool          | Removes records?             | Removes the dataset? | Selection behavior           |
| ------------- | ---------------------------- | -------------------- | ---------------------------- |
| Delete        | Yes, when deleting a dataset | Yes                  | Deletes the specified object |
| DeleteRows    | Yes                          | No                   | Honors a selection           |
| TruncateTable | All rows                     | No                   | Ignores selections           |

Reference: [Truncate Table](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/truncatetable.html).

## G. Joins, indexes, and geodatabase controls

### 34. AddJoin and RemoveJoin: attach a temporary lookup

**Purpose:** View inspection attributes alongside roads using a common ID.

**Calls:** `arcpy.management.AddJoin(in_layer_or_view, in_field, join_table, join_field, ...)` and `arcpy.management.RemoveJoin(in_layer_or_view, join_name)`.

```python
layer = arcpy.management.MakeFeatureLayer(
    roads, "joined_roads_layer"
).getOutput(0)
arcpy.management.AddJoin(layer, "ROAD_ID", inspections, "ROAD_ID", "KEEP_ALL")
arcpy.management.CopyFeatures(layer, os.path.join(output_gdb, "Roads_JoinedCopy"))
arcpy.management.RemoveJoin(layer)  # Remove all joins from this layer.
```

**Result:** The layer temporarily exposes inspection fields; the copy retains them. The source road schema is unchanged. Keys need compatible types and consistent IDs. Duplicate lookup keys can multiply rows, depending on join settings and storage.

Reference: [Add Join](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/add-join.html).

### 35. JoinField: permanently transfer selected attributes

**Purpose:** Store lookup fields on a working feature class.

**Call:** `arcpy.management.JoinField(in_data, in_field, join_table, join_field, fields)`.

```python
working = os.path.join(output_gdb, "Roads_InspectionFields")
arcpy.management.CopyFeatures(roads, working)
arcpy.management.JoinField(
    working, "ROAD_ID", inspections, "ROAD_ID", ["CONDITION", "INSPECTION_DATE"]
)
```

**Result:** The copy gains the specified fields. Use unique lookup keys for this simple example. Repeated keys need a deliberate transfer or aggregation method; do not assume every inspection is retained. Text key matching is case-sensitive.

Reference: [Join Field](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/join-field.html).

### 36. AddIndex and RemoveIndex: manage attribute indexes

**Purpose:** Support repeated queries and joins on large datasets.

**Calls:** `arcpy.management.AddIndex(in_table, fields, index_name)` and `arcpy.management.RemoveIndex(in_table, index_name)`.

```python
working = os.path.join(output_gdb, "Roads_Indexed")
arcpy.management.CopyFeatures(roads, working)
index_name = "TUTOR_ROAD_ID_IDX"
if index_name not in {index.name for index in arcpy.ListIndexes(working)}:
    arcpy.management.AddIndex(working, ["ROAD_ID"], index_name)
print([index.name for index in arcpy.ListIndexes(working)])

# Remove the demonstration index when no longer useful.
arcpy.management.RemoveIndex(working, index_name)
```

**Result:** An index is created and removed. Indexes may improve retrieval but add storage and maintenance costs. A normal index does not establish unique business IDs. File geodatabases ignore the unique-index option.

Reference: [Add Attribute Index](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/add-attribute-index.html).

### 37. Domains: define and assign allowed values

**Purpose:** Standardize a field with geodatabase codes and descriptions.

**Calls:** `CreateDomain`, `AddCodedValueToDomain`, and `AssignDomainToField` in `arcpy.management`.

```python
working = os.path.join(output_gdb, "Roads_WithDomain")
arcpy.management.CopyFeatures(roads, working)
arcpy.management.AddField(working, "TUTOR_STATUS", "TEXT", field_length=20)

domain_name = "TutorialRoadStatus"
if domain_name not in {domain.name for domain in arcpy.da.ListDomains(output_gdb)}:
    arcpy.management.CreateDomain(
        output_gdb, domain_name, "Allowed road status", "TEXT", "CODED"
    )
    arcpy.management.AddCodedValueToDomain(output_gdb, domain_name, "ACTIVE", "Active")
    arcpy.management.AddCodedValueToDomain(output_gdb, domain_name, "RETIRED", "Retired")

arcpy.management.AssignDomainToField(working, "TUTOR_STATUS", domain_name)
arcpy.management.CalculateField(working, "TUTOR_STATUS", "'ACTIVE'", "PYTHON3")
```

**Result:** The field references a text coded-value domain in the output geodatabase. Records store codes such as `ACTIVE`; an editing interface may show descriptions. Assignment does not clean existing invalid values. Enforcement depends on the editing or loading operation; validate loaded records separately.

Reference: [Create Domain](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/create-domain.html).

### 38. AddGlobalIDs: add geodatabase-managed identifiers

**Purpose:** Support globally unique feature identifiers for replication and some relationship or service workflows.

**Call:** `arcpy.management.AddGlobalIDs(in_datasets)`.

```python
working = os.path.join(output_gdb, "Roads_GlobalIDs")
arcpy.management.CopyFeatures(roads, working)
if not any(field.type == "GlobalID" for field in arcpy.ListFields(working)):
    arcpy.management.AddGlobalIDs(working)
```

**Result:** A populated, system-managed GlobalID field. It differs from an ObjectID and a business key such as `ROAD_ID`. An ordinary GUID field does not have GlobalID behavior. Copying or appending may generate new GlobalIDs unless supported preservation settings are used.

### 39. EnableEditorTracking and DisableEditorTracking: track edits

**Purpose:** Record creator, creation date, last editor, and last edit date for subsequent edits.

**Call:** `arcpy.management.EnableEditorTracking(in_dataset, creator_field, creation_date_field, last_editor_field, last_edit_date_field, add_fields, record_dates_in)`.

```python
working = os.path.join(output_gdb, "Roads_Tracked")
arcpy.management.CopyFeatures(roads, working)
if arcpy.Describe(working).editorTrackingEnabled:
    arcpy.management.DisableEditorTracking(working)

arcpy.management.EnableEditorTracking(
    in_dataset=working,
    creator_field="TUTOR_CREATED_BY",
    creation_date_field="TUTOR_CREATED_ON",
    last_editor_field="TUTOR_EDITED_BY",
    last_edit_date_field="TUTOR_EDITED_ON",
    add_fields="ADD_FIELDS",
    record_dates_in="UTC",
)
```

**Result:** Missing tracking fields are created and tracking is enabled. Existing fields need appropriate text or date types. Supplying only a dataset name does not automatically create these four fields. Tracking does not reconstruct past edits. User identity depends on the editing connection and environment.

Use `arcpy.management.DisableEditorTracking(working)` to stop tracking later; it does not delete the fields.

Reference: [Enable Editor Tracking](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/enable-editor-tracking.html).

### 40. Compact: maintain a file geodatabase

**Purpose:** Reorganize storage after many edits and deletions.

**Call:** `arcpy.management.Compact(in_workspace)`.

```python
# Separate demonstration geodatabase avoids earlier examples' locks.
compact_gdb = os.path.join(output_folder, "CompactDemo.gdb")
if not arcpy.Exists(compact_gdb):
    arcpy.management.CreateFileGDB(output_folder, "CompactDemo.gdb")
arcpy.management.Compact(compact_gdb)
```

**Result:** A compacted file geodatabase. Close layers, tables, cursors, and connections holding conflicting locks. Compact differs from enterprise geodatabase Compress and is not a backup operation.

## H. Complete workflow: prepare primary roads for delivery

This standalone script validates fields, saves primary roads, adds status, calculates length, and reports the count. Change the input path first. It does not depend on shared setup or earlier examples.

```python
import os
import arcpy

def prepare_primary_roads():
    source = r"C:\GIS\Data.gdb\Roads"
    output_folder = r"C:\GIS\ManagementTutorial"
    delivery_gdb = os.path.join(output_folder, "RoadDelivery.gdb")
    output_fc = os.path.join(delivery_gdb, "PrimaryRoads")
    layer = None

    if not arcpy.Exists(source):
        raise FileNotFoundError(f"Missing input: {source}")
    required_fields = {"ROAD_ID", "ROAD_TYPE"}
    available_fields = {field.name for field in arcpy.ListFields(source)}
    missing = required_fields - available_fields
    if missing:
        raise ValueError(f"Missing fields: {sorted(missing)}")
    if arcpy.Describe(source).spatialReference.name == "Unknown":
        raise ValueError("Identify the Roads coordinate system first.")

    os.makedirs(output_folder, exist_ok=True)
    if not arcpy.Exists(delivery_gdb):
        arcpy.management.CreateFileGDB(output_folder, "RoadDelivery.gdb")

    try:
        with arcpy.EnvManager(overwriteOutput=True, extent=None):
            layer = arcpy.management.MakeFeatureLayer(
                source, "delivery_primary_roads_layer"
            ).getOutput(0)
            arcpy.management.SelectLayerByAttribute(
                layer, "NEW_SELECTION", "ROAD_TYPE = 'Primary'"
            )
            selected_count = int(arcpy.management.GetCount(layer)[0])
            if selected_count == 0:
                print("No primary roads matched; check ROAD_TYPE values.")
                return

            arcpy.management.CopyFeatures(layer, output_fc)
            if "TUTOR_STATUS" not in {
                field.name for field in arcpy.ListFields(output_fc)
            }:
                arcpy.management.AddField(
                    output_fc, "TUTOR_STATUS", "TEXT", field_length=20
                )
            arcpy.management.CalculateField(
                output_fc, "TUTOR_STATUS", "'ACTIVE'", "PYTHON3"
            )
            arcpy.management.CalculateGeometryAttributes(
                in_features=output_fc,
                geometry_property=[["LENGTH_KM", "LENGTH_GEODESIC"]],
                length_unit="KILOMETERS",
            )
            output_count = int(arcpy.management.GetCount(output_fc)[0])
            if output_count != selected_count:
                raise RuntimeError("Saved count differs from the selection count.")
            print("Primary roads saved:", output_count)
            print("Output:", output_fc)
    finally:
        if layer is not None:
            arcpy.management.Delete(layer)

if __name__ == "__main__":
    try:
        prepare_primary_roads()
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
        raise
    except Exception as error:
        print(f"Workflow failed: {error}")
        raise
```

**Expected output:** `RoadDelivery.gdb\PrimaryRoads`, with selected roads, populated `TUTOR_STATUS`, and geodesic `LENGTH_KM`. Successful reruns replace it. If no roads match, no new output is created; an older output, if present, remains from its previous run.

Inspect the output on a map and compare sample records with the source. Geodesic length measures geometry, not travel time or route cost.

## I. Common mistakes and useful checks

| Problem                         | Action                                                                         |
| ------------------------------- | ------------------------------------------------------------------------------ |
| ArcPy cannot be imported        | Use ArcGIS Pro's Python environment and initialize its authorized license.     |
| Input does not exist            | Check path, spelling, workspace, and `arcpy.Exists`.                         |
| Output cannot be created        | Check permissions, location, names, overwrite settings, and locks.             |
| A field already exists          | Check `arcpy.ListFields` or recreate the tutorial copy.                      |
| Selection returns zero records  | Inspect values, SQL types, quoting, and definition queries.                    |
| Calculation affects every row   | Use a layer with an active selection for a subset update.                      |
| A schema edit fails             | Close conflicting connections; inspect system fields and storage restrictions. |
| Data appears in the wrong place | Verify the source system; use Project to transform coordinates.                |
| Append loses attributes         | Compare schemas and configure field mappings for `NO_TEST`.                  |
| A join duplicates records       | Inspect repeated keys and the intended relationship.                           |

Tools usually return a Result object. Use `result.getOutput(0)` for the first output and `result.getMessages()` for its messages. `arcpy.GetMessages(2)` retrieves errors from the most recent geoprocessing call.

Use `arcpy.EnvManager(...)` to scope settings. Processing extent, output coordinate system, and other applicable environments can influence results. Consult each tool's help to see which settings apply.

## J. Assignment: build a road maintenance delivery

**Scenario:** A county GIS office needs primary roads with inspection information and maintenance priorities. Write a Python script using these management tools. Work on copies and retain source data for comparison.

### Inputs

- `Roads` with `ROAD_ID`, `ROAD_NAME`, and `ROAD_TYPE`.
- `RoadInspections` with `ROAD_ID`, `CONDITION`, and `INSPECTION_DATE`.
- A correctly defined spatial reference on the roads.
- One inspection per road ID for the basic task. If IDs repeat, explain and resolve which inspection to use.

### Tasks

1. Validate paths and fields. Print the input count and spatial reference name.
2. Create `RoadMaintenance.gdb` if necessary. Make reruns predictable without editing source data.
3. Make a road layer, select `ROAD_TYPE = 'Primary'`, and print its selected count. Handle zero matches explicitly.
4. Save selected roads as `PrimaryRoads_Working` with CopyFeatures.
5. Run CheckGeometry and save the report. If repairs are needed, repair the copy and check it again. Record count changes.
6. Use FindIdentical to inspect duplicates on `ROAD_ID` and Shape. Explain matching and retention rules before using DeleteIdentical on the copy.
7. Transfer `CONDITION` and `INSPECTION_DATE` with JoinField. Report roads with no matching inspection; distinguish an unmatched ID from a matched row with null condition.
8. Add `MAINT_PRIORITY` as text of length 20. Calculate `HIGH` for `Poor` condition, `REVIEW` for no condition, and `NORMAL` otherwise. Use selections or a CalculateField code block.
9. Calculate geodesic `LENGTH_KM`. Add an index on `ROAD_ID`.
10. Save `HighPriorityRoads` where priority is `HIGH`. Print the final count, high-priority count, total length, and high-priority length. A SearchCursor may sum lengths.
11. Export high-priority attributes to `HighPriorityRoads_Table` with CopyRows. Confirm it is a table and the road output is a feature class.
12. Remove temporary layers. Inspect saved outputs on a map and summarize unresolved issues.

### Deliverables

- `road_maintenance_assignment.py` with meaningful names, comments, and geoprocessing error handling.
- `RoadMaintenance.gdb` with working roads, high-priority roads, their attribute table, geometry report, and duplicate report.
- A short Markdown report with counts before and after cleanup, inspection matches, units, duplicate rules, and assumptions.

### Marking guide

| Criterion                                               |         Marks |
| ------------------------------------------------------- | ------------: |
| Input validation and predictable reruns                 |            15 |
| Correct selections and saved outputs                    |            20 |
| Geometry and duplicate checks with documented decisions |            20 |
| Correct join and priority calculations                  |            20 |
| Measurements, index, and count checks                   |            15 |
| Readable code, error handling, and report               |            10 |
| **Total**                                         | **100** |

**Extension:** Create and assign a domain for `MAINT_PRIORITY`, then enable editor tracking on the working dataset. Explain the differences between ObjectID, GlobalID, and `ROAD_ID`.
