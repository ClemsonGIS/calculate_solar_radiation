#!/usr/bin/env python
"""--------------------------------------------------------------------
name:         mosaic_to_raster.py
arguments:    argv[1] = path where the DEM files are stored.
              argv[2] = File prefix DEM files that need to be 
                        combined. These files need to be in zipped 
						format.
			  
version:      python 2.7

dependencies: ArcGIS arcpy python utilities. Raster GRID DEM file in 
			  zipped format. 
			  
description:  This script will take multiple raster files (in GRID 
              format) and merge them together to form one complete 
			  raster file. It will use the ArcGIS function 
			  MosaicToNewRaster_management function. 
			  See the ArcGIS documentation for information on this
			  function.
--------------------------------------------------------------------"""
# Import os and sys python modules which allow python to use file 
# based functions and utilities.
import os,sys,ntpath,shutil

# Import ArcGIS's python functions in order to run ArcGIS functions 
# within python.
import arcpy

# Import specific functions from python modules. make_archive allows 
# you to zip directories. move allows you to move files. ZipFile 
# allows you to zip or unzip individual files. glob allows you
# to store file names and file directories in to lists.
from shutil import move,make_archive,rmtree
from zipfile import ZipFile
from glob import glob

# Set the current workspace to the current directory the script is 
# being run from.
arcpy.env.workspace = os.getcwd()

# This arcpy function retrieves the license from the License Manager.
arcpy.CheckOutExtension('Spatial')

# Set the variable base_result_name to the raster files prefix.
pathName = sys.argv[1]
baseFilename = sys.argv[2]

# Put all the DEM zipped files into the zippedDEMs list and then 
# unzip all the DEM files.
# and put them into a folder
newpath = os.getcwd() +'\processed_data' 
if not os.path.exists(newpath):
    os.makedirs(newpath)
zippedDEMs = glob(pathName + '\\' + baseFilename + '*.zip')
for z in zippedDEMs:
	ZipFile(z).extractall()
	shutil.move(z, ".\processed_data")

# This command will populate a list with all the DEM files 
# that were listed in the zippedDEMs list but without the path 
# and extension. 
demRasters = [ ntpath.basename(base) for (base,ext) in map(os.path.splitext, zippedDEMs) ]

#debug: print out the raster files that we want to join.
for r in demRasters:
	print 'demRasters = %s' % r

# Join all the DEM files into a string that are seperated with
# semicolons. This is the format the MosaicToNewRaster_management
# function requires. Also, specify the resultant raster name.
inputs  = ';'.join(demRasters[0:])
base_result_name = baseFilename + 'newzip'

#debug: print out the input files that we want to join.
print('inputs = %s' % inputs)
print('base_result_name = %s' % base_result_name)

# Create a directory with the raster files prefix name.
os.mkdir(base_result_name)


arcpy.MosaicToNewRaster_management(inputs,            # Raster datasets you want to merge
								   base_result_name,  # Folder to place merged raster
								   base_result_name,  # Name of the merged raster dataset.
								                      # The name can't be more than 13 
													  # characters.
								   "",                # Coordinate system for merged raster
								   "32_BIT_FLOAT",    # Pixel Type
								   "",                # Cell size for new raster dataset
								   "1",               # Number of bands for merged raster
								   "LAST",            # Methode used to merge overlapping 
								                      # tiles. "LAST" indicates the output
													  # cell values of the overlapping 
													  # areas will be the value from the
													  # last raster dataset merged into
													  # that location. This is the default.
								   "FIRST")           # Mosaic Colormap mode. "FIRST" is 
													  # the default.
								   
# zip up the result GRID DEM folder
print('Zipping up, %s' % base_result_name)
# make_archive(base_result_name, "zip", os.getcwd(), base_result_name)

# Clean up directories.
print('Deleting all DEMs...')
for d in glob(baseFilename + '*'):
	if (os.path.isdir(d) and (d != base_result_name)):
		rmtree(d)
