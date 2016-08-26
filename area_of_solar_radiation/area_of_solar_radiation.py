#!/usr/bin/env python

""""------------------------------------------------------------------------------
name:         area_of_solar_radiation.py
arguments:    argv[1] = tif file to be processed 
              argv[2] = A number of one of the tiles that was created using the 
			            SplitRaster_management function.
              argv[3] = Number of columns for each row of the raster that was split.
			            This should never be zero.
              argv[4] = list of latitude numbers corresponding with each row of
			            tiles created using the SplitRaster_management function.
						The number of latitude numbers MUST match the number of 
						rows used in the SplitRaster_management function.
			  
version:      python 2.7

dependencies: ArcGIS arcpy python utilities. Raster tif file in zipped format. 
              The file must be stored in the same directory as the python script.
			  
description:  This script will take a raster file (in tif 
              format) and calculate the area of solar radiation for that 
			  raster file using the arcpy AreaSolarRadiation_sa function. 
			  See ArcGIS documentation for full description of that functon.
			  The generated DEM file will be zipped up.
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

# unpack any zip archives in the current directory with extentions of "zip".
# We should only have one tif file in zipped format.
for z in glob('*.zip'):
  ZipFile(z).extractall()
  
# Print out all command line arguments for debugging purposes.
print 'argv[1] = %s' % sys.argv[1]
print 'argv[2] = %s' % sys.argv[2]
print 'argv[3] = %s' % sys.argv[3]
print 'argv[4] = %s' % sys.argv[4]
  
# Take the string of latitudes and put them in a list of floats.
latitude_list = [float(x) for x in sys.argv[4].split(',')]


# Print out list of latitudes (float) to use for debugging purposes.
for y in range(len(latitude_list)):
  print 'latitude_list %d) %s' % (y, latitude_list[y])

# Set the latitude_idx variable based on the number of the tile we're processing 
# for latitude_list. We divide the current tile number by the number of columns 
# in each row. This will give us the row that should be associated with a 
# certain latitude. 
latitude_idx = int(sys.argv[2]) // int(sys.argv[3])

# Print out index that will be used in the lattitude_list list for debugging purposes.
print 'latitude_idx = %d' % latitude_idx
 
# Set the in_raster and basename variable to the file being processed.
in_raster  = os.path.abspath(sys.argv[1])
basename   = os.path.splitext(os.path.basename(in_raster))[0]

# Print out the basename of the files created for debugginf purposes.
print  'basename = %s' % basename

# Name each type of output to a specific output filename based on that type.
SR_raster  = 'SR-%s'  % basename
DR_raster  = 'DR-%s'  % basename
DRA_raster = 'DRA-%s' % basename
DD_raster  = 'DD-%s'  % basename


# Run the AreaSolarRadiation_sa function on the raster tile.
arcpy.gp.AreaSolarRadiation_sa(in_raster,
                               SR_raster,
                               latitude_list[latitude_idx],
                               "200",
#                               "MultiDays 2015 5 160",    
#                               "14",							   
                               "[1,365]",
                               "1",
                               "1",
                               "NOINTERVAL",
                               "0.3048",
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

# zip up the grid directories
for f in (SR_raster, DR_raster, DRA_raster, DD_raster):
  make_archive(f, 'zip', os.getcwd(), f)

# clean up
for f in glob('*.aux.xml') + glob('DR-scdem-*.zip') + glob('DD-scdem-*.zip') + glob('DRA-scdem-*.zip') + glob('scdem-*.GRID.zip'):
  os.unlink(f)
  
  
# clean up some more
for f in glob('*.ovr') + glob('*.aux.xml') + glob('*.tif.xml') + glob('*.tif') + glob('*.tfw'):
  os.unlink(f)

# delete log file.  
os.unlink('log')

# delete extraneous directories.
for f in glob(SR_raster) + glob(DR_raster) + glob(DRA_raster) + glob(DD_raster) + glob('info'):
  rmtree(f)


