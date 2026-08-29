
ArcGIS geoprocessing tools are organized into toolboxes by function. Here's a rundown of the major categories, with a few standout tools in each:

**Data Management**
The broadest toolbox — handles files, fields, projections, and general upkeep.

- `Add Field`, `Calculate Field`, `Delete Field`
- `Project` (reproject data to a different coordinate system)
- `Append`, `Merge`, `Copy Features`
- `Check Geometry` / `Repair Geometry` (the ones we just talked about)
- `Dissolve`, `Feature Class to Feature Class`

**Analysis**
Core spatial analysis operations.

- `Buffer` — create zones around features
- `Clip`, `Intersect`, `Union` — combine or trim datasets by overlap
- `Select` — pull out features matching a query
- `Near` — find distance to nearest feature

**Spatial Analyst / 3D Analyst** (extension-based)
Raster and surface analysis.

- `Slope`, `Aspect`, `Hillshade`
- `Raster Calculator`
- `Interpolation` tools (IDW, Kriging)
- `Viewshed`, `Line of Sight`

**Cartography**
Prepping data for maps.

- `Simplify Polygon` / `Simplify Line`
- `Aggregate Polygons`
- `Feature Outline Masks`

**Conversion**
Moving data between formats.

- `Table to Table`, `Feature Class to Shapefile`
- `Raster to Polygon` and vice versa
- `JSON to Features` / `Features to JSON`

**Data Reviewer / Data Engineering (Clean tools)**
Specifically aimed at data cleaning, which ties into what you asked before:

- `Detect Feature Changes`
- `Remove Fields`, `Standardize Field` (from the Data Engineering "Clean" category — these tools let you remove unnecessary fields and modify or fill missing values)
- `Find/Fill Missing Values`

**Geocoding & Network Analyst**

- `Geocode Addresses`
- `Route`, `Service Area`, `Closest Facility`

If you're specifically building a scripted data-cleaning workflow, the ones most worth digging into are `Check Geometry`/`Repair Geometry`, the Data Engineering "Clean" tools, `Calculate Field`, and `Delete Identical` (for removing duplicate records). Want me to go deeper on any one category — like a cheat sheet of the most useful cleaning tools with example ArcPy syntax?
