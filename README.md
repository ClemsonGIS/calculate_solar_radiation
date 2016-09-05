# Calculating Solar Radiation from Raster File.
Use ArcGIS (arcpy package) to calculate area of solar radiation on DEM (TIFF formatted) raster file.

Date: 08/30/2016

Authors: Patrick Claflin and Amanda Farthing
## Scenario:
   We needed to calculate the area of [solar radiation](http://desktop.arcgis.com/en/arcmap/latest/tools/spatial-analyst-toolbox/understanding-solar-radiation-analysis.htm) for the entire state of South Carolina using ArcGIS's 
## Problem:
   The time it takes to calculate insolation is extreme for large raster images such as an entire state. It can take days to complete a calculation once.
## Solution:
We used an "[embarrassingly parallel](https://en.wikipedia.org/wiki/Embarrassingly_parallel)" processing system called HTCondor to break up and distribute the calculations among multiple nodes. This concurrent process drastically decreased the time it to to calculate insolation for the entire state of SC. The entire process was broken into the following 3 steps:

1) Submit a python script within a Condor Submission file. This python program would split the raster image into multiple parts and zip each set of files for distributed processing. We used the arcpy tool [SplitRaster_management()](http://desktop.arcgis.com/en/arcmap/latest/tools/data-management-toolbox/split-raster.htm) to split the raster into 600 separate TIFF files.

2) Submit multiple "jobs" through HTCondor. Each "job" will process one of the smaller poly-line feature classes and then return the results to the owner.

3) Use a python script and ArcGIS to merge the resultant feature classes together to create one large feature class of intersections.
 
## Files needed for this process
### Python script files:
1) split_feature_class.py - used to split the larger feature class into smaller feature classes.

2) intersectStation.py - used to calculate intersections between point feature class and poly-line feature class.

3) merge_feature_classes.py - used to merge all the smaller feature classes into one feature class.

### Condor submission files:
1) IntersectStations.sub
