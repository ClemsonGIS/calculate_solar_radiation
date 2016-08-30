# Calculating Solar Radiation from Raster File.
Use ArcGIS (arcpy package) to calculate area of solar radiation on DEM (TIFF formatted) raster file.

Date: 08/30/2016

Author: Patrick Claflin
# Scenario: 
   We need to calculate all the possible intersections between 1,960,371 entry poly-line feature class and a 258 point feature class. 
# Problem: 
   There are too many poly-line observations for this process to be fast or efficient on one machine. Many times the ArcGIS intersect function will run for days and then crash.
# Solution: 
1) Use a python script and ArcGIS to break up the poly-line feature class into separate feature classes. Each new, smaller, feature class will contain at most 5000 poly-line entries. 

2) Submit multiple "jobs" through HTCondor. Each "job" will process one of the smaller poly-line feature classes and then return the results to the owner.

3) Use a python script and ArcGIS to merge the resultant feature classes together to create one large feature class of intersections.
  
# Files needed for this process
## Python script files:
1) split_feature_class.py - used to split the larger feature class into smaller feature classes.

2) intersectStation.py - used to calculate intersections between point feature class and poly-line feature class.

3) merge_feature_classes.py - used to merge all the smaller feature classes into one feature class.

## Condor submission files:
1) IntersectStations.sub
 
