#!/usr/bin/env python
"""------------------------------------------------------------------------------
name:         split_raster.py
arguments:    argv[1] = tif file to be split 
              argv[2] = filename prefix for input tif file in zipped format and
			            output files that will be generated from SplitRaster_management 
                        function.
              argv[3] = number of columns in which to split the raster file.
			  argv[4] = number of rows in which to split the raster file.
			  argv[5] = overlap (in meters) of each tile.
			  
version:      python 2.7

dependencies: ArcGIS arcpy python utilities. Raster tif file in zipped format. The
              file must have the same prefix as argv[2] and must be
              stored in the same directory as the python script.
			  
description:  This script will take a tif raster file and split it into tile
              segments (rows, columns) using the arcpy python function 
			  SplitRaster_management. See ArcGIS documentation
			  for full description of that functon. After the tif file is 
			  split into multiple tif files. All the tiles will all get zipped 
              up individually to be used in other python scripts.			  
-------------------------------------------------------------------------------"""

# Import os and sys python modules which allow python to use 
# file based functions and utilities.
import os,sys,shutil

# Import ArcGIS's python functions in order to run ArcGIS 
# functions within python.
import arcpy

# Import specific functions from python modules. make_archive allows 
# you to zip directories. 
# ZipFile allows you to zip or unzip individual files. 
# glob allows you to store file names and file directories in to lists.
from zipfile import ZipFile
from glob import glob

# Set the current workspace to the current directory the script is being
# run from.
arcpy.env.workspace = os.getcwd()

#This arcpy function retrieves the license from the License Manager.
arcpy.CheckOutExtension('Spatial')

# unpack any zip archives in the current directory with extentions of "zip".
# We should only have the one tif file in zipped format.
ZipFile(sys.argv[1] + '.zip').extractall()

# Set the in_raster variable to tif file the current working directory.
# Print out the variable for debugging purposes.
in_raster   = os.path.abspath(sys.argv[1])
print ('in_raster=%s ' % in_raster)

# Set the out_raster variable to the file prefix with a dash added at the 
# end. Print out the variable for debugging purposes.
out_raster  = '%s_' % sys.argv[2]
print ('out_raster=%s ' % out_raster)

#cwd = os.getcwd()
# Set the out_folder variable to the current working directory. Print out
# the variable for debugging purposes.
out_folder  = os.getcwd()
print ('out_folder=%s ' % out_folder)

# Set the num_rasters variable to the number of columns and rows (string format)
# that are specified in the command line arguments.
num_rasters = "%s %s" % (sys.argv[3], sys.argv[4])

# The overlay value (in meters) used in the SplitRaster_management function.
overlap = sys.argv[5]

in_raster += ".tif"   ##################### ADDED #############################

# Run the SplitRaster_management function with the parameters we've specified.
arcpy.SplitRaster_management(in_raster,          # in_raster
                             out_folder,         # out_folder
                             out_raster,         # out_base_name
                             "NUMBER_OF_TILES",  # split_method
                             "TIFF",               #format
#                             "GRID",             # format
                             "BILINEAR",         # resampling_type
                             
                             num_rasters,        # num_rasters
                             "#",              # tile_size 
                             overlap,            # overlap
                             "METERS",           # units
                             "#",                # cell_size
                             "#")                # origin					

# Zip up all the tif files generated from the SplitRaster_management 
# function.
# Because some of the tiles that were split from the original 
# contained empty data (white space) not all of the tiles will 
# be created. 

# count is the maximum number of tif files that could have been created.
count = int(sys.argv[3]) * int(sys.argv[4])

newpath = out_folder +'\split_data' 
if not os.path.exists(newpath):
    os.makedirs(newpath)

for i in range(count):
	base = os.path.basename('%s%d' % (out_raster, i))
	print('base = %s' % base)
        tiff_files = glob('%s.TIF.ovr' % base) + glob('%s.TIF.aux.xml' % base) + glob('%s.tif' % base) + glob('%s.tfw' % base)
	if (tiff_files):
		zFile = ZipFile(base + ".zip","w")
		print 'zipping files: %s' % ', '.join(tiff_files)
                for z in tiff_files:
                        zFile.write(z,z)
                zFile.close()
                shutil.move(base + ".zip", ".\split_data")

# Zipping up the tif files doesn't delete the original tif files. 
# This will clean up all the tif files that were generated with 
# the SplitRaster_management function.
print('Deleting tif files...')
for f in glob('*.[*.ovr,*.xml,tif,tfw]*'):
	os.unlink(f)
  
  
