import os,sys,arcpy
from shutil import make_archive
from zipfile import ZipFile
from glob import glob

arcpy.env.workspace = os.getcwd()


# unpack any incoming ZIP archives
for z in glob('scdem-*.zip'):
  ZipFile(z).extractall()