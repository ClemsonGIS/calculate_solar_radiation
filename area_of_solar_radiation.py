#!/usr/bin/env python
"""------------------------------------------------------------------------------
name:         area_of_solar_radiation.py
arguments:    argv[1] = DEM (in tif format) file to be processed. This script
						assumes that the filename will be <filename>.tif and
						that it will be contained in a zipped file of the 
						same file name with the zip extension <filename>.zip
              argv[2] = Specify the amount of overlap (in meters) of the
						raster file.
			  
version:      python 2.7

dependencies: ArcGIS arcpy python utilities. Raster tif file in zipped format. 
              The file must be stored in the same directory as the python script.
			  
description:  This script will take a raster file (in tif 
              format) and calculate the area of solar radiation for that 
			  raster file using the arcpy AreaSolarRadiation_sa function. It
			  will then clip the middle region of the calculated raster to a
			  new raster file using arcpy's Clip_management. The clipped DEM 
			  file will be zipped up. The other rasters will be  deleted 
			  (except for the original zipped DEM).
			  See ArcGIS documentation for full description of those functons.
			  
-------------------------------------------------------------------------------"""
# Import os and sys python modules which allow python to use file based functions
# and utilities.
import os,sys

# Import ArcGIS's python functions in order to run ArcGIS functions within python.
import arcpy

# Import specific functions from python modules. make_archive allows you to zip
# directories. rmtree allows you to delete non-empty directories. ZipFile allows 
# you to zip or unzip individual files. glob allows you
# to store file names and file directories in to lists.
from shutil import make_archive,rmtree
from zipfile import ZipFile
from glob import glob

# Set the current workspace to the current directory the script is being run from.
arcpy.env.workspace = os.getcwd()

# This arcpy function retrieves the license from the License Manager.
arcpy.CheckOutExtension('Spatial')

#
# Print out all command line arguments for debugging purposes.
print 'argv[1] = %s' % sys.argv[1]
print 'argv[2] = %s' % sys.argv[0]

# DEM file in zipped format
tifFilename = sys.argv[1]
baseFilename = os.path.splitext(os.path.basename(tifFilename))[0]

#debug message...
#print('baseFilename = %s' % baseFilename)

# The clipping edge will be half the value of overlap specified 
# in sys.argv[2].
bounds_val = str(int(sys.argv[2])//2)

#debug message...
print('bounds_val = %s' % bounds_val)

# Set the clipping window from the edges of the raster (in meters)
clip_bounds = {"left":bounds_val,"top":bounds_val,"right":bounds_val,"bottom":bounds_val}

# Let's unpack any zip archive that contains the DEM files include the tif file.
ZipFile(baseFilename + '.zip').extractall()

#
# It's time to calculate the solar insolation of the DEM files.
#

# Set the in_raster and basename variable to the file being processed.
in_raster  = os.path.abspath(tifFilename)
print "in_raster = " + in_raster

# Name each type of output to a specific output filename based on that type.
SR_raster  = 'SR_%s'  % baseFilename
DR_raster  = 'DR_%s'  % baseFilename
DRA_raster = 'DRA_%s' % baseFilename
DD_raster  = 'DD_%s'  % baseFilename

# The clipped raster name. The output basename of the raster cannot be longer
# than 14 characters or the Clip_management function will complain.
clipped_SR_raster = 'c' + SR_raster
"""

rProps = arcpy.GetRasterProperties_management(in_raster,"TOP")
rTop = rProps.getOutput(0)
rProps = arcpy.GetRasterProperties_management(in_raster,"BOTTOM")
rBottom = rProps.getOutput(0)
y_min = float(rBottom) + float(clip_bounds["bottom"])
y_max = float(rTop) - float(clip_bounds["top"])
lat = str(((y_min + y_max) / 2) / 111111)
print ("latitude: " + lat)

"""
"""
# Run the AreaSolarRadiation_sa function on the raster tile.
arcpy.gp.AreaSolarRadiation_sa(in_raster,      # In raster file
                               SR_raster,      # Output raster file (GRID format)
                               "",	           # Latitude
                               "200",          # Sky size. 200 is default.
                               "[1,365]",      # date range. for [1,365] we Start
											   # on Jan 1st and calculate for 365 days.
                               "1",            # Time interval throughout year (in days)
                               "1",            # Time interval throughout day (in hours)
                               "NOINTERVAL",   # NOINTERVAL says we want a single output 
											   # raster for all day intervals.
                               "0.3048",       # z_factor
                               "FROM_DEM",     # How slope and aspect information are 
											   # derived for analysis. FROM_DEM is default.
                               "32",		   # calculation directions. Default is 32.
                               "8",            # zenith divisions. Default is 8.
                               "8",			   # azimuth divisions. Default is 8.
                               "UNIFORM_SKY",  # Type of diffuse radiation model. UNIFORM_SKY
											   # is default.
                               "0.3",          # diffuse proportion. 0.3 is default.
                               "0.5",          # transmittivity. 0.5 is default.
                               DR_raster,      # output raster name for direct radiation raster.
                               DRA_raster,     # output raster name for diffuse radiation raster.
                               DD_raster)      # output raster name for direct duration raster.
"""
outGlobalRadiation = arcpy.sa.AreaSolarRadiation(
                         in_raster,
						 "",
						 "200",
						 "[1,365]",
						 "14",
						 "0.5",
						 "NOINTERVAL",
						 "1",
						 "FROM_DEM",
						 "32",
						 "8",
						 "8",
						 "UNIFORM_SKY",
						 "0.3",         
                         "0.5",
                         DR_raster,      
                         DRA_raster,     
                         DD_raster)
						 
outGlobalRadiation.save(SR_raster)


# Let's try some clipping. 
# 1) Get the extent of the SR raster using GetRasterProperties_management function.
# 2) Apply the clipping boundry to that extent. x_min, y_min, x_max, y_max represent the new rectangle. 
# 3) Use the Clip_management function to clip the middle section from the raster.
#
# 1st step...
rProps = arcpy.GetRasterProperties_management(SR_raster,"LEFT")
rLeft = rProps.getOutput(0)
rProps = arcpy.GetRasterProperties_management(SR_raster,"TOP")
rTop = rProps.getOutput(0)
rProps = arcpy.GetRasterProperties_management(SR_raster,"RIGHT")
rRight = rProps.getOutput(0)
rProps = arcpy.GetRasterProperties_management(SR_raster,"BOTTOM")
rBottom = rProps.getOutput(0)

#debug messages...
print('For raster, %s' % SR_raster)
print('\t\tleft:%s - bottom:%s - right:%s - top:%s' % (rLeft,rBottom,rRight,rTop))

# 2nd step...
x_min = str(float(rLeft) + float(clip_bounds["left"]))
x_max = str(float(rRight) - float(clip_bounds["right"]))
y_min = str(float(rBottom) + float(clip_bounds["bottom"]))
y_max = str(float(rTop) - float(clip_bounds["top"]))
clip_area = x_min + " " + y_min + " " + x_max + " " + y_max

# more debug messages...
print('clip_area:\t%s' % clip_area)
print

# 3rd step...

if(bounds_val != 0):
	arcpy.Clip_management(SR_raster, clip_area, 'c' + SR_raster,"#","#","NONE","NO_MAINTAIN_EXTENT")

# zip up the clipped GRID DEM directory. 
make_archive(clipped_SR_raster, 'zip', os.getcwd(), clipped_SR_raster)


# Clean up files. Using a regex (regular expression to grab most of the files we want to delete).
for f in glob('*.[*.ovr,*.xml,tif,tfw]*') + glob('log'):
	os.unlink(f)


# Clean up directories.
for d in glob('*' + baseFilename) + glob('info'):
        try:
                rmtree(d)
        except WindowsError as e:
                print e
