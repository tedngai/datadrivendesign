---
title: "GIS Workshop - Terrain Analysis and Modeling"
subtitle: "Creating 3D terrain models from USGS elevation data using QGIS and Rhino3D"
date: "2019-03-07"
category: "gis"
tools: ["QGIS", "Rhino3D", "Python", "3DEP", "USGS"]
difficulty: "intermediate"
youtube_ids: []
thumbnail: ""
---

![Centralia Topo Mesh](../assets/images/gis/centralia_topo_mesh.jpg)

---

## Project Description

The objective of this workshop is to go through all the steps involved to create a 3D terrain model in Rhino using [3D Elevation Program](https://www.usgs.gov/core-science-systems/ngp/3dep/about-3dep-products-services) (3DEP) data from [United States Geological Survey](https://www.usgs.gov/) (USGS), downloadable from [The National Map](https://viewer.nationalmap.gov/basic/). This workshop assumes you already know Rhino3D.

### 3DEP

USGS 3DEP is the national elevation program for the United States. It includes several terrain data products, including DEM rasters derived from LiDAR, IfSAR, and other elevation sources. In this tutorial we will work with DEMs because they are the most direct input for building a terrain mesh.

[The National Map](https://viewer.nationalmap.gov/basic/) distributes elevation datasets at several resolutions. In practical terms, the resolution tells you how much ground each raster cell represents. A 1-meter DEM stores one elevation sample per 1 x 1 meter cell, while 1/9 arc-second data is roughly 3 meters and 1/3 arc-second data is roughly 10 meters. Higher resolution gives you more detail, but it also creates much heavier files and denser meshes.

For design workflows, that tradeoff matters. If you are studying a building site or a compact urban district, 1-meter data may be worth the extra processing time. If you are building a larger regional landform or only need broad topographic variation, 1/3 arc-second data is often easier to manage.

---

# Step 1
## Download Data from The National Map

To begin, go to [The National Map](https://viewer.nationalmap.gov/basic/) and search for elevation products for your area of interest. The interface changes over time, but the basic goal is the same: filter for **Elevation Products (3DEP)**, zoom to your site, and download the highest resolution DEM you can reasonably process on your machine.

If more than one raster format is offered, choose **IMG** or **GeoTIFF**. Either works well in QGIS, but the screenshots below use IMG.

![National Map](../assets/images/gis/pic_GIS_nationalmap.JPG)

On the map, zoom to your area and run the product search for the current extent. The site should return one or more DEM tiles covering your view.

On the results list, use the tile footprint preview to see how many files cover your site. In our case, Lower Manhattan is split across two tiles, so we need both files before we can merge them in QGIS.

![National Map Footprint](../assets/images/gis/pic_GIS_nationalmap_footprint.JPG)

Each download usually arrives as a **.zip** archive containing the raster plus metadata. Extract every archive into its own folder so you do not mix tiles accidentally. In the extracted files, look for the main raster file, typically **.img** or **.tif**.

![National Map Save File](../assets/images/gis/pic_GIS_nationalmap_savefile.JPG)

---

# Step 2
## QGIS

- [QGIS](https://qgis.org/en/site/forusers/download.html)

QGIS is an open-source GIS platform with a very active developer community. It is powerful enough for most raster and vector workflows in this tutorial. Install the current stable release unless you have a specific reason to test a newer development build.

When you are done installing the software, **launch QGIS**. On the upper left corner, click **Project > New**, you should get a blank screen as the following.

![QGIS](../assets/images/gis/pic_GIS_qgis.JPG)

---

# Step 3
## Processing GIS Data

Almost all datasets we downloaded need to be processed before they can become useful, but in this case, the processing only involves stitching the 2 tiles together, reprojecting the image to Google's projection system, and then cropping to the specific area we want.

### Stitching

You should have QGIS running and have a blank screen. Click **Raster > Miscellaneous > Merge** and a window should pop up with a number of parameters.

![QGIS Merge](../assets/images/gis/pic_GIS_qgis_merge.JPG)

![QGIS Merge Parameters](../assets/images/gis/pic_GIS_qgis_mergeparam.JPG)

Under **Input Layers**, click on the **....** button and then **Add File(s)...**, select the 2 **.IMG** files you downloaded earlier, then click **OK**.

![QGIS Add Files](../assets/images/gis/pic_GIS_qgis_addfiles.JPG)

Under **Merged**, click on the **....** button and then **Save to File...**, give your file a name and choose **TIF files (*.tif)** as file type, then click **SAVE**.

Make sure **Open output file after running algorithm** is **checked**, then click **RUN**. If everything is working properly, you should see something like this on your screen.

![QGIS DEM Merged](../assets/images/gis/pic_GIS_qgis_demmerged.JPG)

---

### Reprojection

All maps are 2-dimensional projections of the earth, and every raster is stored in a coordinate reference system (CRS). Before exporting terrain into Rhino, you need to confirm that the DEM is in a projected CRS with linear units you understand, ideally meters.

![Earth Projections](../assets/images/gis/earhprojections.jpg)

In GIS, projection systems are commonly referenced by an **EPSG** code. Choosing the right CRS is critical because it controls your horizontal units and the way your terrain aligns with other data. For example, one DEM might arrive in **EPSG:26918** (`NAD83 / UTM zone 18N`), which is a projected CRS in meters, while another might arrive in **EPSG:4269** (`NAD83` geographic coordinates), which stores locations in latitude and longitude rather than meters.

![Projections Comparison](../assets/images/gis/compare-mercator-utm-wgs-projections.jpg)

If your only goal is to build a terrain mesh in Rhino, you can often stay in the DEM's native projected CRS as long as its units are meters. However, if you plan to align the terrain with web basemaps, Google-derived content, or other web map layers, it is helpful to reproject the DEM to **Web Mercator (`EPSG:3857`)** so everything uses the same map space.

In other words, this step is optional. If your merged DEM is already in a projected CRS with meter units and you do not need web-map alignment, you can skip the warp and continue with the merged raster.

On the left column of QGIS, Under Layer, double click on the layer named **Merged**, you will see the **Layer Properties** window pop up, and under the **Information** tab, you should see this.

![QGIS Layer Info](../assets/images/gis/pic_GIS_qgis_layerinfo.JPG)

**CRS** is the coordinate reference system currently assigned to the layer. In this example the merged raster should still report the CRS inherited from the source DEM tiles. This panel is also where you can confirm the raster's map units and pixel size, both of which matter later when you generate the mesh.

Now click on **Raster > Projections > Warp (Reproject...)**, a window should pop up.

![QGIS Warp](../assets/images/gis/pic_GIS_qgis_warp.JPG)
![QGIS Warp Parameters](../assets/images/gis/pic_GIS_qgis_warpparam.JPG)

Set **Input Layer** to the merged DEM. In most cases QGIS will detect the source CRS automatically from the layer metadata. Do not override the source CRS unless you have confirmed that the file was imported incorrectly. For **Target CRS**, choose **EPSG:3857 - WGS 84 / Pseudo-Mercator** if you need alignment with web basemaps or Google-derived geometry.

![QGIS Google CRS](../assets/images/gis/pic_GIS_qgis_googlecrs.JPG)

Back in the Warp parameter window, click the **....** button under **Reprojected**, give the output a file name, choose **TIF files (*.tif)** as the file type, then click **Save** and **Run**.

Once the new layer is ready, set the **Project CRS** from that layer so your QGIS canvas and measurement tools match the raster you are looking at. In current versions of QGIS, the wording may vary slightly, but the command is still available from the layer context menu.

![QGIS Set CRS](../assets/images/gis/pic_GIS_qgis_setcrsfromlayer.JPG)
![QGIS Reprojected](../assets/images/gis/pic_GIS_qgis_reprojected.JPG)

Before moving on, double-check the output layer properties. The important check is not whether the file says "Google" somewhere, but whether the raster now reports a projected CRS with units in meters and a sensible pixel size for your DEM.

![QGIS Reproject Unit](../assets/images/gis/pic_GIS_qgis_reprounit.JPG)

---

### Analysis

Since the majority of the DEM file is somewhat dark, we need to change the visualization so we see the landmass features easier.

#### Channel and Bitdepth

First thing we need to notice is the DEM file is a single channel 32-bit file. Single channel images usually can be seen as black and white images. 3 channel images are typically RGB. Our computer screens are mostly capable of displaying 8-bit colors, that's 3 channels each with 8-bit, so 256 x 256 x 256 = 16.7 million color variations. But since our DEM file has only 1 channel and we are showing the image as black and white, we are restricted to only 256 levels.

![QGIS Bitdepth](../assets/images/gis/pic_GIS_qgis_bitdepth.JPG)
![QGIS Quantization](../assets/images/gis/pic_GIS_qgis_quantization.JPG)
![QGIS RGB Bitdepth](../assets/images/gis/pic_GIS_qgis_rgbbitdepth.JPG)

What we can do to mitigate this situation is to remap color information to match the landmass variation. So **Double-Click** on the **Layer** to show the **Layer Properties**. Go to **Symbology**, change **Render Type** to **Singleband pseudocolor**, change the **Mode** to **Equal Interval**, click **Apply**.

![QGIS Symbology 01](../assets/images/gis/pic_GIS_qgis_symbology01.JPG)
![QGIS Symbology 02](../assets/images/gis/pic_GIS_qgis_symbology02.JPG)

Now double click on the number under **Value**, change **-17.12 to -2**, **3.68 to 0**, **24.48 to 10**, **45.27 to 20**, click **OK**.

![QGIS Symbology 03](../assets/images/gis/pic_GIS_qgis_symbology03.JPG)
![QGIS Symbology 04](../assets/images/gis/pic_GIS_qgis_symbology04.JPG)

What we have effectively done is to compress all the color variation to within 20 meters of elevation change. Let's say during Storm Sandy in 2012, the storm surge in NYC is at 14'. So let's see if we can modify this visualization to show that.

Back in **Symbology**, click the **Plus Sign** below **Equal Interval** twice to add two additional values. Storm Sandy's 14' storm surge is about 4.2 meters.

![QGIS Symbology 05](../assets/images/gis/pic_GIS_qgis_symbology05.JPG)
![QGIS Symbology 06](../assets/images/gis/pic_GIS_qgis_symbology06.JPG)

---

### Cropping

Bring up the **Layer Properties** window again and take a look at the **width and height**. With this file, width is about 10209 pixels and height is 20140 pixels. If we were to generate a 3D topography out of this DEM file, the mesh will have 10209 x 20104 = 205 million tesselations. This is an enormous file and will most likely crash many computers. So as a strategy, cropping the DEM file to only the areas we need should be the first step in managing the file.

![QGIS Layer Info 2](../assets/images/gis/pic_GIS_qgis_layerinfo2.JPG)

In QGIS, crop is called clip and you access the tool by clicking on **Raster > Extractions > Clip Raster by Extent**.

![QGIS Clip Extent](../assets/images/gis/pic_GIS_qgis_clipextent.JPG)

Click the **....** button under **Clipping extent (xmin, xmax, ymin, ymax)**, then select **Select Extent on Canvas**, then **Click - Drag** your mouse to select the area of interest. Then click on the **....** button under **Clipped (extent)** and give it a file name, choose **TIF files (*.tif)** as type, click **SAVE** and then **RUN**.

![QGIS Clip Extent Parameters](../assets/images/gis/pic_GIS_qgis_clipextentparam.JPG)
![QGIS Clipped](../assets/images/gis/pic_GIS_qgis_clipped.JPG)

Final step before moving to Rhino is to export the DEM to a format that can be parsed easily. Before exporting, check the clipped layer properties again to confirm the width and height are within a manageable range. As a rough rule, staying below about `2000 x 2000` cells will make scripting and meshing much more reliable, but the real limit depends on your hardware.

### Export to .ASC

To bring this DEM into Rhino, we will export it as an **ESRI ASCII Grid (`.asc`)**. This format is easy to inspect in a text editor and straightforward to parse with a short Python script. In QGIS, use **Raster > Conversion > Translate (Convert Format)**, set **Input Layer** to the clipped DEM, and save the output as **ASC (`*.asc`)**.

![QGIS Convert](../assets/images/gis/pic_GIS_qgis_convert.JPG)
![QGIS Convert Parameters](../assets/images/gis/pic_GIS_qgis_convertparam.JPG)

When the `.asc` file has been created, open it in a text editor and inspect the header before moving on. A typical file looks like this:

```
ncols        375
nrows        400
xllcorner    -8239264.087285323068
yllcorner    4969648.230586678721
cellsize     1.322408175983
NODATA_value -9999
 4.3700013160705566406 4.3799986839294433594 ...
```

Some exports include a `NODATA_value` line and some do not. Both are valid. What matters is that `ncols`, `nrows`, and `cellsize` are present and that `cellsize` is expressed in the units of your raster CRS. If you want a Rhino mesh at real-world scale, export from a projected CRS in meters.

---

# Step 4
## 3D Mesh Generation

This part happens inside Rhino. You do not need to be an experienced programmer, but you should be comfortable opening scripts and working with meshes in Rhino 7 or Rhino 8.

We are using a short Rhino Python script to read the ASCII grid and build a mesh. In Rhino 7 or 8, open the Python editor from **Tools > PythonScript > Edit**, or run the command `EditPythonScript`. If you only want to run an existing script file, `RunPythonScript` works as well.

![Rhino Python](../assets/images/gis/pic_GIS_rhinopython.JPG)

If you only care about the result, paste the script below into the editor and run it. Rhino will ask you to choose the exported `.asc` file, then it will build a terrain mesh from the raster values.

![Rhino Python Window](../assets/images/gis/pic_GIS_rhinopython_window.JPG)

If you are interested in the specifics or have problems generating a mesh, read on.

First, make sure the header information in the `.asc` file is readable. The first five or six rows should look something like this:

```python
ncols        375
nrows        400
xllcorner    -8239264.087285323068
yllcorner    4969648.230586678721
cellsize     1.322408175983
NODATA_value -9999
```

`ncols` and `nrows` define the raster dimensions. `xllcorner` and `yllcorner` record the lower-left origin of the raster in map coordinates. `cellsize` is the horizontal size of each raster cell. Some files also include `NODATA_value`, which tells you which number represents missing cells.

Do not delete the `NODATA_value` line if it exists. It is a normal part of the ESRI ASCII Grid format, and the script below accounts for it.

The script below is written to run in current Rhino Python environments and to handle either a five-line or six-line ASCII header.

```python
import rhinoscriptsyntax as rs
 
fname = rs.OpenFileName("Open DEM", "Arc/Grid ASCII Files (*.asc)|*.asc||")
if not fname:
    raise SystemExit

with open(fname, "r") as f:
    lines = [line.strip() for line in f if line.strip()]

header = {}
data_start = 0
for i, line in enumerate(lines[:6]):
    parts = line.split()
    key = parts[0].lower()
    if key in {"ncols", "nrows", "xllcorner", "yllcorner", "cellsize", "nodata_value"}:
        header[key] = parts[1]
        data_start = i + 1
    else:
        break

ncol = int(header["ncols"])
nrow = int(header["nrows"])
dx = float(header["cellsize"])
dy = dx
nodata = float(header.get("nodata_value", -9999))

z = []
for line in lines[data_start:]:
    z.extend(line.split())

vertices = []
for row in range(nrow):
    for col in range(ncol):
        index = row * ncol + col
        value = float(z[index])
        if value == nodata:
            value = 0.0
        vertices.append((col * dx, -row * dy, value))

faces = []
for row in range(nrow - 1):
    for col in range(ncol - 1):
        n = row * ncol + col
        faces.append((n, n + 1, n + ncol + 1, n + ncol))

rs.AddMesh(vertices, faces)
```

This script ignores the original `xllcorner` and `yllcorner` values and rebuilds the terrain as a local mesh starting at the origin. That is usually what you want in Rhino. The important thing it preserves is the cell spacing, so the terrain keeps the correct horizontal scale as long as the DEM was exported in meters.

And that's it.

[View the finished 3D model on Sketchfab](https://sketchfab.com/3d-models/world-trade-center-dem-a7979bace34442d1b6655c37bd348a5b)

---

# Summary

### What You Have Learned

- How to download elevation data from The National Map
- How to stitch multiple DEM tiles together in QGIS
- How to reproject raster data to different coordinate systems
- How to visualize high bit-depth data with false color mapping
- How to clip raster data to a specific extent
- How to export DEM data to ASCII format
- How to generate 3D terrain meshes in Rhino3D using Python
