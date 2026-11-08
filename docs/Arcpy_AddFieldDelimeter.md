
 **`arcpy.AddFieldDelimiters()`**

`arcpy.AddFieldDelimiters()` is an ArcPy function used when building **SQL where clauses** for geoprocessing tools. It automatically adds the correct field delimiters for the workspace type (File Geodatabase, Personal Geodatabase, shapefile, etc.), making your scripts more portable.

## Why is it needed?

Different data sources use different field delimiters:

| Data Source                | Example                 |
| -------------------------- | ----------------------- |
| File Geodatabase           | `STATUS = 'Active'`   |
| Personal Geodatabase (MDB) | `[STATUS] = 'Active'` |
| Shapefile                  | `"STATUS" = 'Active'` |

Instead of hardcoding delimiters, ArcPy can add them automatically.

---

## Syntax

arcpy.AddFieldDelimiters(datasource, field_name)

### Parameters

* **datasource** : Path to the feature class, shapefile, or table.
* **field_name** : Name of the field to delimit.

### Returns

A properly formatted field name.

---

# Example 1: Selecting Features

Suppose you have a feature class called `Parcels`.

import arcpy

fc = r"C:\GIS\Data.gdb\Parcels"

field = arcpy.AddFieldDelimiters(fc, "OWNER")

where_clause = f"{field} = 'John Doe'"

arcpy.management.SelectLayerByAttribute(

    "Parcels_Lyr",

    "NEW_SELECTION",

    where_clause

)

ArcPy builds the correct expression depending on the data source.

---

# Example 2: Numeric Fields

For numeric fields, don't use quotes around the value.

import arcpy

fc = r"C:\GIS\Data.gdb\Buildings"

field = arcpy.AddFieldDelimiters(fc, "HEIGHT")

where_clause = f"{field} > 50"

print(where_clause)

Output:

HEIGHT > 50

---

# Example 3: Using SearchCursor

import arcpy

fc = r"C:\GIS\Data.gdb\Roads"

field = arcpy.AddFieldDelimiters(fc, "ROAD_TYPE")

sql = f"{field} = 'Highway'"

with arcpy.da.SearchCursor(fc, ["NAME"], sql) as cursor:

    for row in cursor:

        print(row[0])

This returns only roads classified as highways.

---

# Example 4: Multiple Conditions

import arcpy

fc = r"C:\GIS\Data.gdb\Customers"

name_field = arcpy.AddFieldDelimiters(fc, "CITY")

age_field = arcpy.AddFieldDelimiters(fc, "AGE")

sql = f"{name_field} = 'Nairobi' AND {age_field} > 30"

print(sql)

Output:

CITY = 'Nairobi' AND AGE > 30

---

# Practical Tutorial: Select Power Poles in Nairobi

Let's say you're working on a utility network dataset at Kenya Power.

Fields:

* `COUNTY`
* `VOLTAGE`

Goal:
Select poles in Nairobi with voltage greater than 11 kV.

import arcpy

fc = r"C:\UtilityNetwork\KPLC.gdb\PowerPoles"

county = arcpy.AddFieldDelimiters(fc, "COUNTY")

voltage = arcpy.AddFieldDelimiters(fc, "VOLTAGE")

where_clause = (

    f"{county} = 'Nairobi' "

    f"AND {voltage} > 11"

)

arcpy.MakeFeatureLayer_management(fc, "poles_lyr")

arcpy.SelectLayerByAttribute_management(

    "poles_lyr",

    "NEW_SELECTION",

    where_clause

)

count = arcpy.GetCount_management("poles_lyr")

print(f"Selected poles: {count}")

---

# When should you use `AddFieldDelimiters()`?

✅ Use it when:

* Building SQL queries dynamically.
* Writing scripts that may run against different workspace types.
* Using `SelectLayerByAttribute`.
* Using cursors with SQL filters.
* Using tools that require a WHERE clause.

❌ Usually unnecessary when:

* You already know the database type and are writing a quick script.
* Working only with file geodatabases in ArcGIS Pro, where field delimiting requirements are simpler.

---

## Common Beginner Mistake

Wrong:

where_clause = "CITY = Nairobi"

Correct:

field = arcpy.AddFieldDelimiters(fc, "CITY")

where_clause = f"{field} = 'Nairobi'"

Notice that:

* Text values are enclosed in single quotes.
* Field names are handled by `AddFieldDelimiters()`.

### Modern Note

In  **ArcGIS Pro** , `AddFieldDelimiters()` is considered a legacy compatibility function because field delimiters are handled more consistently across many supported data sources. However, it's still useful when writing robust scripts that may work with different workspace types or older datasets.

As someone learning ArcPy, I'd strongly recommend mastering `AddFieldDelimiters()` alongside:

1. `arcpy.da.SearchCursor`
2. `arcpy.da.UpdateCursor`
3. SQL WHERE clauses
4. `SelectLayerByAttribute`
5. `MakeFeatureLayer`

These five topics are frequently used together in real-world geoprocessing scripts.
