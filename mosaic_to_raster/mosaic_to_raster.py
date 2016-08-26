#!/usr/bin/env python

""""------------------------------------------------------------------------------
name:         mosaic_to_raster.py
arguments:    argv[1] = File prefix of all the split tiles that need to be 
                        combined. These files need to be in zipped format.
			  
version:      python 2.7

dependencies: ArcGIS arcpy python utilities. Raster tif file in zipped format. 
              The file must be stored in the same directory as the python script.
			  
description:  This script will take multiple raster files (in GRID 
              format) and merge them together to form one complete raster file.
			  It will use the ArcGIS function MosaicToNewRaster_management 
			  function. See the ArcGIS documentation for information on this
			  function.
-------------------------------------------------------------------------------"""


# Import os and sys python modules which allow python to use file based functions
# and utilities.
import os,sys

# Import ArcGIS's python functions in order to run ArcGIS functions within python.
import arcpy

# Import specific functions from python modules. make_archive allows you to zip
# directories. move allows you to move files. ZipFile allows 
# you to zip or unzip individual files. glob allows you
# to store file names and file directories in to lists.
from shutil import move,make_archive
from zipfile import ZipFile
from glob import glob

# Set the current workspace to the current directory the script is being run from.
arcpy.env.workspace = os.getcwd()

# This arcpy function retrieves the license from the License Manager.
arcpy.CheckOutExtension('Spatial')

# Set the variable base_result_name to the raster files prefix.
base_result_name = sys.argv[1]

# unpack any incoming ZIP archives
zips = glob("*.zip")
for z in zips:
  ZipFile(z).extractall()

#debug: print out parts of next line to understand it more clearly.
maps = map(os.path.splitext, zips)
for m in maps:
	print ('maps = %s,%s' % m)
	
print ''
  
rasters = [ base for (base,ext) in map(os.path.splitext, zips) ]
#debug: print out the raster files that we want to join.
for r in rasters:
	print 'rasters = %s' % r
	
#inputs  = ';'.join(rasters[1:])
inputs  = ';'.join(rasters[0:])

#debug: print out the input files that we want to join.
print 'inputs = %s' % inputs

#move(rasters[0], 'result')

#debug: print out the raster files that we want to join.
for r in rasters:
  print 'rasters = %s' % r

# Create a directory with the raster files prefix name.
os.mkdir(base_result_name)

arcpy.MosaicToNewRaster_management(inputs,base_result_name,base_result_name,"","32_BIT_FLOAT","","1","LAST","FIRST")

# zip up the result
make_archive(base_result_name, "zip", os.getcwd(), base_result_name)
