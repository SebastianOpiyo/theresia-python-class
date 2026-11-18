# ArcPy Analysis Tools: Tutorial Notes with Code Examples

## 1. What is `arcpy.analysis`?

`arcpy.analysis` provides access to the **Analysis toolbox** in ArcGIS Pro. It contains many tools; it is not a single tool. Use it to answer spatial questions such as:

- Which bus stops are within 1,000 feet of a park?
- Which parcels overlap a flood zone?
- How many bus stops fall inside each city?
- What is the total assessed parcel value in each district?

The general pattern is `arcpy.analysis.ToolName(inputs, output, other_parameters)`.
For example, `arcpy.analysis.Buffer(...)` runs Buffer, while `arcpy.analysis.Clip(...)` runs Clip.

These notes focus on vector features and attribute tables. Raster analysis tools such as Slope belong to other toolboxes, including `arcpy.sa` (Spatial Analyst).

Reference: [Analysis toolbox overview](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/analysis/an-overview-of-the-analysis-toolbox.html).

## 2. Requirements and example data

Run the examples in an **ArcGIS Pro notebook**, its **Python window**, or a script using the Python environment supplied with ArcGIS Pro. You need an authorized ArcGIS Pro installation; installing ordinary Python alone does not provide ArcPy. See [Python in ArcGIS Pro](https://doc.esri.com/en/arcgis-pro/latest/arcpy/get-started/installing-python-for-arcgis-pro.html).

The paths, datasets, and fields below are teaching examples. Supply your own data and change names to match it; these datasets are not included with these notes.

| Input in `C:\GIS\Data.gdb` | Geometry | Fields used in examples |
| --- | --- | --- |
| `Parks` | Polygon | `AGNCY_NAME` (text) |
| `BusStops` | Point | No extra fields required |
| `Cities` | Polygon | `NAME` (text, including `Oakland`) |
| `Roads` | Polyline | No extra fields required |
| `Parcels` | Polygon | `LAND_USE` (text), `DISTRICT` (text), `ASSESSED_VALUE` (numeric) |
| `FloodZones` | Polygon | No extra fields required |

In the class data, `CPAD_2020b_Units` can supply the parks and `UniqueStops_Summer21` can supply the bus stops. A city boundary dataset is also needed for the complete workflow in section 14. Inspect its city-name field before using it.

**Licensing depends on your installed ArcGIS Pro version and tool options.** For example, [Erase in ArcGIS Pro 3.3](https://pro.arcgis.com/en/pro-app/3.3/tool-reference/analysis/erase.htm) requires Advanced, while the [current Erase documentation](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/analysis/erase.html) lists Basic, Standard, and Advanced. Check the help for your version before running an example.

## 3. Set up the workspace

Run this block once before the short examples in sections 4–13. The input geodatabase must already exist. The block creates a separate output geodatabase if necessary.

```python
import os
import arcpy

input_gdb = r"C:\GIS\Data.gdb"       # Change this path.
output_folder = r"C:\GIS\TutorialOutputs"
output_gdb = os.path.join(output_folder, "AnalysisResults.gdb")

if not arcpy.Exists(input_gdb):
    raise FileNotFoundError(f"Input geodatabase not found: {input_gdb}")

os.makedirs(output_folder, exist_ok=True)
if not arcpy.Exists(output_gdb):
    arcpy.management.CreateFileGDB(output_folder, "AnalysisResults.gdb")

arcpy.env.workspace = input_gdb
# Rerunning an example replaces outputs with the same names.
arcpy.env.overwriteOutput = True

parks = os.path.join(input_gdb, "Parks")
stops = os.path.join(input_gdb, "BusStops")
cities = os.path.join(input_gdb, "Cities")
roads = os.path.join(input_gdb, "Roads")
parcels = os.path.join(input_gdb, "Parcels")
flood_zones = os.path.join(input_gdb, "FloodZones")

print("Output geodatabase:", output_gdb)
```

Use raw strings such as `r"C:\GIS\Data.gdb"` for Windows paths. Inside a geodatabase, output feature classes and tables do **not** take `.shp` or `.dbf` extensions.

The examples below are independent after setup. Each tool section shows a **minimal call pattern**, rather than every optional parameter. Click its documentation link for the complete signature.

## 4. Select: extract features using an attribute query

**Question:** Which parks have Oakland city recorded as their agency?

Call pattern: `arcpy.analysis.Select(in_features, out_feature_class, where_clause)`.

```python
oakland_agency_parks = os.path.join(output_gdb, "Parks_OaklandAgency")
agency_name = "Oakland, City of"
# In SQL text literals, an apostrophe is escaped by doubling it.
agency_sql = agency_name.replace("'", "''")
where_clause = f"AGNCY_NAME = '{agency_sql}'"

arcpy.analysis.Select(parks, oakland_agency_parks, where_clause)
print("Selected parks:", arcpy.management.GetCount(oakland_agency_parks)[0])
```

**Expected output:** A polygon feature class containing matching park records.

SQL text values use single quotes: `LAND_USE = 'Residential'`. Numeric values are unquoted: `ASSESSED_VALUE > 100000`. Combine conditions with `AND` or `OR`; use `IS NULL` to find missing values.

Agency ownership does not establish whether a park lies inside a city boundary. Use a spatial operation when the question is geographic.

Unlike `arcpy.management.SelectLayerByAttribute`, which changes a layer's selection, `Select` writes a new feature class. Existing selections on input layers can restrict the records processed.

References: [Select](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/analysis/select.html). You may encounter `arcpy.AddFieldDelimiters` in earlier class scripts; Esri now describes it as a [legacy function](https://doc.esri.com/en/arcgis-pro/latest/arcpy/functions/addfielddelimiters.html), and says delimiters are unnecessary for SQL queries in ArcGIS Pro.

## 5. Buffer: create a distance zone

**Question:** What area lies within 1,000 feet of any park?

Call pattern: `arcpy.analysis.Buffer(in_features, out_feature_class, buffer_distance_or_field, ...)`.

```python
park_buffer = os.path.join(output_gdb, "Parks_Buffer1000ft")

result = arcpy.analysis.Buffer(
    in_features=parks,
    out_feature_class=park_buffer,
    buffer_distance_or_field="1000 Feet",
    dissolve_option="ALL",
    method="GEODESIC",
)

print("Saved:", result.getOutput(0))
```

**Expected output:** Polygon coverage around the parks. `ALL` removes boundaries between overlapping buffers; `NONE` preserves individual feature buffers; `LIST` dissolves by specified fields.

Always include distance units. `GEODESIC` measures over the earth's curved surface. For local planar analysis, use a suitable projected coordinate system. A polygon's full buffer includes the original polygon, so stops inside parks also qualify in a later proximity query.

Reference: [Buffer](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/analysis/buffer.html).

## 6. Clip: keep the part inside a boundary

**Question:** Which road segments lie inside the city boundaries?

Call pattern: `arcpy.analysis.Clip(in_features, clip_features, out_feature_class)`.

```python
roads_in_cities = os.path.join(output_gdb, "Roads_InCities")

arcpy.analysis.Clip(
    in_features=roads,
    clip_features=cities,
    out_feature_class=roads_in_cities,
)
```

**Expected output:** Road segments cut at the city boundaries. The output keeps road attributes; it does not append the city attributes. This example uses all polygons in `Cities`. Select Oakland first if you need only Oakland.

Polygon clip features can cut points, lines, or polygons. `arcpy.analysis.Clip` is a feature tool; raster clipping uses a different tool.

Reference: [Clip](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/analysis/clip.html).

## 7. Intersect: keep overlaps and combine attributes

**Question:** Which portions of parcels overlap flood zones?

Call pattern: `arcpy.analysis.Intersect(in_features, out_feature_class, join_attributes="ALL")`.

```python
flooded_parcels = os.path.join(output_gdb, "Parcels_FloodOverlap")

arcpy.analysis.Intersect(
    in_features=[parcels, flood_zones],
    out_feature_class=flooded_parcels,
    join_attributes="ALL",
)
```

**Expected output:** Overlapping polygon pieces with attributes from both inputs. One original parcel may produce several output records.

The default output geometry follows the lowest-dimensional input: polygons with lines produce lines, while any point input produces points. Basic and Standard licenses limit this tool to two inputs.

Copied values such as assessed value are not automatically reduced in proportion to the retained parcel area. Avoid summing duplicated parcel values after splitting features.

Reference: [Intersect](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/analysis/intersect.html).

## 8. Union: retain all polygon areas

**Question:** How do parcels and flood zones partition the whole area they cover?

Call pattern: `arcpy.analysis.Union(in_features, out_feature_class, join_attributes="ALL")`.

```python
parcel_flood_union = os.path.join(output_gdb, "Parcels_FloodUnion")

arcpy.analysis.Union(
    in_features=[parcels, flood_zones],
    out_feature_class=parcel_flood_union,
    join_attributes="ALL",
)
```

**Expected output:** Polygon pieces covering overlapping and nonoverlapping areas from either input, with attributes describing their sources. Union accepts polygon inputs only. Basic and Standard licenses limit it to two inputs.

Inspect the `FID_<input>` fields: `-1` indicates that a piece has no corresponding feature from that input. Unlike Intersect, Union also retains areas belonging to just one input.

Reference: [Union](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/analysis/union.html).

## 9. Erase: remove overlapping portions

**Question:** Which portions of parcels lie outside flood zones?

Call pattern: `arcpy.analysis.Erase(in_features, erase_features, out_feature_class)`.

```python
parcels_outside_flood = os.path.join(output_gdb, "Parcels_OutsideFlood")

arcpy.analysis.Erase(
    in_features=parcels,
    erase_features=flood_zones,
    out_feature_class=parcels_outside_flood,
)
```

**Expected output:** Parcel geometry remaining after flood-zone areas are removed. A partly flooded parcel is cut; it is not necessarily discarded entirely. Attributes come from the parcel input.

Review the version-specific licensing note in section 2 before using this tool.

Reference: [Erase](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/analysis/erase.html).

## 10. Spatial Join: count features by location

**Question:** How many bus stops intersect each city?

Call pattern: `arcpy.analysis.SpatialJoin(target_features, join_features, out_feature_class, ...)`.

```python
city_stop_counts = os.path.join(output_gdb, "Cities_StopCounts")

arcpy.analysis.SpatialJoin(
    target_features=cities,
    join_features=stops,
    out_feature_class=city_stop_counts,
    join_operation="JOIN_ONE_TO_ONE",
    join_type="KEEP_ALL",
    match_option="INTERSECT",
)
```

**Expected output:** City polygons with `Join_Count`, the number of matching stops. `KEEP_ALL` retains cities with zero matches. The target determines output geometry.

`JOIN_ONE_TO_MANY` can produce several rows per target. For one-to-one joins, use field mappings to control how other joined attributes are aggregated; do not assume numeric attributes are summed by default.

With `INTERSECT`, a stop on a shared boundary can match both cities. Overlapping polygons can also count a stop multiple times. Decide how to treat these cases before adding city counts together.

Reference: [Spatial Join](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/analysis/spatial-join.html).

## 11. Near: find the nearest feature

**Question:** Which park is closest to each stop within a 2-kilometer search radius?

Call pattern: `arcpy.analysis.Near(in_features, near_features, search_radius, ...)`.

**Near updates its input dataset.** Copy the stops first to preserve the source.

```python
stops_near = os.path.join(output_gdb, "BusStops_NearestPark")
arcpy.management.CopyFeatures(stops, stops_near)

arcpy.analysis.Near(
    in_features=stops_near,
    near_features=parks,
    search_radius="2 Kilometers",
    method="GEODESIC",
    distance_unit="Meters",
)

with arcpy.da.SearchCursor(stops_near, ["OID@", "NEAR_FID", "NEAR_DIST"]) as rows:
    for stop_id, park_id, distance in rows:
        print(stop_id, park_id, distance)
```

**Expected output:** The copied stops gain `NEAR_FID` and `NEAR_DIST`. A value of `-1` means no match within the radius; distance zero can mean the stop intersects a park. Here distances are explicitly requested in meters.

These are geometric distances, not walking routes or travel times. License availability varies by version; older releases may require Standard or Advanced.

Reference: [Near](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/analysis/near.html).

## 12. Statistics: summarize numeric attributes

**Question:** What are the total and average assessed parcel values per district?

The toolbox calls this **Summary Statistics**, but the Python function is `Statistics`.

Call pattern: `arcpy.analysis.Statistics(in_table, out_table, statistics_fields, case_field)`.

```python
district_values = os.path.join(output_gdb, "District_ParcelValues")

arcpy.analysis.Statistics(
    in_table=parcels,
    out_table=district_values,
    statistics_fields=[
        ["ASSESSED_VALUE", "SUM"],
        ["ASSESSED_VALUE", "MEAN"],
    ],
    case_field="DISTRICT",
)
```

**Expected output:** A table with a row per district and fields such as `SUM_ASSESSED_VALUE` and `MEAN_ASSESSED_VALUE`. The input can be a feature class because it has an attribute table.

Omit `case_field` to summarize the entire input into one row. Null values are excluded from the statistic calculations. A `COUNT` statistic counts non-null values in its chosen field.

Reference: [Summary Statistics](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/analysis/summary-statistics.html).

## 13. Frequency: count category combinations

**Question:** How many parcels have each district and land-use combination?

Call pattern: `arcpy.analysis.Frequency(in_table, out_table, frequency_fields)`.

```python
land_use_counts = os.path.join(output_gdb, "District_LandUseCounts")

arcpy.analysis.Frequency(
    in_table=parcels,
    out_table=land_use_counts,
    frequency_fields=["DISTRICT", "LAND_USE"],
)
```

**Expected output:** A table containing `DISTRICT`, `LAND_USE`, and `FREQUENCY`. Each unique combination becomes one row; `FREQUENCY` gives its record count. This groups attributes, rather than testing spatial relationships.

Reference: [Frequency](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/analysis/frequency.html).

## 14. Complete workflow: Oakland stops within 1,000 feet of parks

**Goal:** Save stops inside Oakland that are within 1,000 feet of any park in the supplied parks dataset, including stops inside park polygons.

The sequence is: **select the city boundary → clip the stops to the city → buffer parks → clip the city stops to the buffer**.

This script is self-contained. Update the three input paths and city field before running it. All inputs must have known, correctly assigned coordinate systems; check datum transformations when combining datasets with different datums.

```python
import os
import arcpy

def main():
    # Change these paths to match your class data.
    parks_fc = r"C:\GIS\Data.gdb\Parks"
    stops_fc = r"C:\GIS\Data.gdb\BusStops"
    cities_fc = r"C:\GIS\Data.gdb\Cities"
    city_field = "NAME"
    city_name = "Oakland"

    output_folder = r"C:\GIS\TutorialOutputs"
    output_gdb = os.path.join(output_folder, "AnalysisResults.gdb")

    for dataset in (parks_fc, stops_fc, cities_fc):
        if not arcpy.Exists(dataset):
            raise FileNotFoundError(f"Missing input: {dataset}")
        if arcpy.Describe(dataset).spatialReference.name == "Unknown":
            raise ValueError(f"Input has an unknown coordinate system: {dataset}")

    field_names = {field.name for field in arcpy.ListFields(cities_fc)}
    if city_field not in field_names:
        raise ValueError(f"City field {city_field!r} not found in {cities_fc}")

    os.makedirs(output_folder, exist_ok=True)
    if not arcpy.Exists(output_gdb):
        arcpy.management.CreateFileGDB(output_folder, "AnalysisResults.gdb")

    city_boundary = os.path.join(output_gdb, "Oakland_Boundary")
    city_stops = os.path.join(output_gdb, "Oakland_BusStops")
    park_buffer = os.path.join(output_gdb, "AllParks_Buffer1000ft")
    final_stops = os.path.join(output_gdb, "Oakland_Stops_NearParks")

    # Settings are restored when the with block ends.
    # Clear any inherited processing extent for this workflow.
    with arcpy.EnvManager(overwriteOutput=True, extent=None):
        city_sql = city_name.replace("'", "''")
        arcpy.analysis.Select(
            cities_fc, city_boundary, f"{city_field} = '{city_sql}'"
        )

        if int(arcpy.management.GetCount(city_boundary)[0]) == 0:
            raise ValueError(f"No boundary found for city: {city_name}")
        if int(arcpy.management.GetCount(parks_fc)[0]) == 0:
            raise ValueError("The parks input contains no features.")

        arcpy.analysis.Clip(stops_fc, city_boundary, city_stops)

        # Include parks outside the city: their buffers may reach city stops.
        arcpy.analysis.Buffer(
            in_features=parks_fc,
            out_feature_class=park_buffer,
            buffer_distance_or_field="1000 Feet",
            dissolve_option="ALL",
            method="GEODESIC",
        )

        arcpy.analysis.Clip(city_stops, park_buffer, final_stops)

        city_count = int(arcpy.management.GetCount(city_stops)[0])
        final_count = int(arcpy.management.GetCount(final_stops)[0])
        print("Stops inside Oakland:", city_count)
        print("Stops within 1,000 feet of parks:", final_count)
        print("Saved output:", final_stops)
        if final_count == 0:
            print("No stops matched; review input coverage and coordinate systems.")

if __name__ == "__main__":
    try:
        main()
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
        raise
    except Exception as error:
        print(f"Workflow failed: {error}")
        raise
```

Using a dissolved buffer prevents overlapping individual park buffers from becoming separate coverage zones. The final point feature class preserves bus-stop attributes.

If the assignment specifically asks for parks managed by Oakland city, apply the agency selection from section 4 before buffering. This changes the park population used in the analysis. A city-boundary check is still needed to establish which stops lie inside Oakland.

Validate the output in ArcGIS Pro: display the city boundary, parks, buffer, and result together; inspect a few matching and nonmatching stops. The final count should not exceed the count of input stops inside the city. Multiple source records at the same stop location remain multiple records.

References: [EnvManager](https://doc.esri.com/en/arcgis-pro/latest/arcpy/classes/envmanager.html), [ArcPy error handling](https://doc.esri.com/en/arcgis-pro/latest/arcpy/get-started/error-handling-with-python.html).

## 15. Read results and troubleshoot

Most examples create a new feature class or table. Near is different: it adds or updates fields on the input supplied to it.

Geoprocessing calls return a `Result` object. `result.getOutput(0)` retrieves its first output, and `result.getMessages()` retrieves its messages. For example, the Buffer result in section 5 can be inspected with `print(result.getMessages())`. See [Result](https://doc.esri.com/en/arcgis-pro/latest/arcpy/classes/result.html).

| Symptom | What to check |
| --- | --- |
| `ModuleNotFoundError: No module named 'arcpy'` | Run with the ArcGIS Pro Python environment. |
| Input dataset cannot be found | Confirm the path, feature class name, and `arcpy.Exists(path)`. |
| Output cannot be created | Confirm the output geodatabase exists, the name is valid, and no process holds a conflicting lock. |
| Invalid SQL expression | Inspect field names, field types, text quoting, and the data source's SQL syntax. |
| Empty output | Check input coverage, query values, layer selections, and processing extent. |
| Unexpected distances | Check coordinate systems, linear units, and planar versus geodesic settings. |
| Tool unavailable or not licensed | Compare the installed ArcGIS Pro version and license with that version's tool help. |

When combining different coordinate systems, use an appropriate analysis/output coordinate system and any required geographic transformation. Do not use Define Projection to change coordinates that are already correctly defined; use Project when reprojection is required.

Reference: [Project](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/project.html).

## 16. Practice tasks

1. Change the park buffer to 500 feet. Compare the number of matching stops with the 1,000-foot result.
2. Select residential parcels whose assessed value exceeds 100,000, and save them as a new feature class.
3. Run Clip and Intersect on parcels and flood zones. Compare their geometry and attribute fields.
4. Count bus stops per city with Spatial Join. Find any cities with `Join_Count = 0`.
5. Summarize parcel values by both `DISTRICT` and `LAND_USE` using Statistics with a list of case fields.
6. Copy the stops, run Near, and identify records where `NEAR_FID = -1`. Explain how the search radius affects that result.
