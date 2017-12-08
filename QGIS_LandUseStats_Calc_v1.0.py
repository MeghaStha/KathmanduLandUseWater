# Author: Vera Knook, Petra Izeboud, and Jeff Davids
# Modified: 
# Company: TU Delft
# Date: 161026
# Date Modified:
# Purpose: Merge multiple land use stats files into one flat file .csv
# v1.1
#
# Instructions: Fill in...
#
#   Import system modules

import os
import sys
import subprocess
grass7bin_win = r'C:\OSGeo4W64\bin\grass70.bat'
gisdb = r"E:\GrassData\2016MDP"
location="Loc_KathmanduValley"
mapset="Watersheds_VK"

os.environ['PATH'] += ';' + r"C:\OSGEO4W64\apps\grass\grass-7.0.4\lib"

# QGISinst=u'C:/PROGRA~1/QGIS2~1.14/apps/qgis-ltr'
# qgs = QgsApplication([], False)
# qgs.initQgis()

if sys.platform.startswith('win'):
    grass7bin = grass7bin_win
    print "platform should be configured now"
else:
    raise OSError('Platform not configured.')

print grass7bin

startcmd = [grass7bin, '--config', 'path']
print startcmd

# query GRASS GIS itself for its GISBASE
startcmd = [grass7bin, '--config', 'path']
try:
    p = subprocess.Popen(startcmd, shell=False,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
except OSError as error:
    sys.exit("ERROR: Cannot find GRASS GIS start script"
             " {cmd}: {error}".format(cmd=startcmd[0], error=error))
if p.returncode != 0:
    sys.exit("ERROR: Issues running GRASS GIS start script"
             " {cmd}: {error}"
             .format(cmd=' '.join(startcmd), error=err))
gisbase = out.strip(os.linesep)

# set GISBASE environment variable
os.environ['GISBASE'] = gisbase

# define GRASS-Python environment
grass_pydir = os.path.join(gisbase, "etc", "python")
sys.path.append(grass_pydir)
sys.path.append(r"C:\Program Files\QGIS 2.14\bin")

# import (some) GRASS Python bindings
import grass.script as g
import grass.script.setup as gsetup

gsetup.init(gisbase, gisdb, location, mapset)

print gisbase
sys.path.append(r"C:\OSGEO4~1\apps\grass\grass-7.0.4\bin")
sys.path.append(r"C:\OSGEO4~1\apps\grass\grass-7.0.4\scripts")
sys.path.append(r"C:\OSGEO4~1\apps\grass\grass-7.0.4\lib")
##check Path
print sys.path

#g.message('Current GRASS GIS 7 environment:')
#print g.gisenv()
# 
#g.message('Available raster maps:')
#for rast in g.list_strings(type = 'rast'):
#    print rast
# 
#g.message('Available vector maps:')
#for vect in g.list_strings(type = 'vect'):
#    print vect

##Read CSV File
#   Modify the following variables as desired

inputFilePathArray = [r"E:\Watersheds"]
inputFilePathArray.append(r"E:\Watersheds")
outputFilePath = r"E:\Watersheds\Output"
numHeaders = 0
inputNumRecPerDay = 96
subSampleInterval = 96
numIterations = 50
fNameCriteria1 = ".csv"

#   Import system modules

import os
import sys
import datetime
import random
import numpy as n

print("\nSubsampling input file(s), please wait...\n")
print("Average subSamplingInterval: " + str(subSampleInterval) + "\n")

#   Loop through the entire inputFilePathArray

for inputFilePath in inputFilePathArray:

#   Create directory list and iterate to the next fName if fNameCriteria1 and fNameCriteria2 isn't found
# I'm sure this is an 'omweg' to get the inputfile. Might as well have just named it. but yeah.. all good. 
    dirList=os.listdir(inputFilePath)

    for fName in dirList:
        if fName.find(fNameCriteria1) > 0:
            inFile = open(inputFilePath + '/' + fName, 'r')
            print("Subsampling " + fName + "\n")
        
#   determines the total number of lines in inFile

            numLines = sum(1 for line in inFile)
            print("Input file total lines: " + str(numLines) + "\n")
            inFile.seek(0)
#   Next function makes an array of the offset in bytes that each new line in the file starts at
#   The lineOffset array can then be used to navigate to any line in the file
        
            lineOffset = []
            offset = 0
headings=inFile.readline()

#Create an empty matrix for the data
Riverpoints=n.zeros((numLines-1,3))

# Stores ID number and xyCoordinates in the Riverpoints matrix
for i in range(0,numLines-1):
    dataRow=inFile.readline()
    dataField=dataRow.split(";")
    Riverpoints[i,0]=float(dataField[4])
    Riverpoints[i,1]=float(dataField[5])
    Riverpoints[i,2]=float(dataField[3])
    xyCoordinates=[float(dataField[0]),float(dataField[1])]

# Loops through all riverpoints to create watershed delineation, a vectorfile and statistics 
for k in range(0,numLines-1):
    # Create a string from ID number
    ID=Riverpoints[k,2]
    ID=int(ID)
    IDstring=str(ID)
    # Create Filenames
    rastoutput='delrast'+IDstring
    vectinput=rastoutput+'@Watersheds_VK'
    vectoutput='delvec1_'+IDstring
    statsinput='LandUseMap_15280@Watersheds_VK'
    statsoutput='E:\GrassData\stats'+IDstring
    # Make a string of coordinates
    x=Riverpoints[k,0]
    x=x.astype(str)
    y=Riverpoints[k,1]
    y=y.astype(str)
    coordinates=x+','+y
    # Create a string to make a mask
    Maskstring="if("+rastoutput+"@Watersheds_VK > 0 , 1, null())"
    print ID

# g.run_command('r.watershed', elevation="DEM_KTM_SRTM_30_45n_MS@Deliniation_KV", threshold=500, stream="newmapname")
# Create a rasterfile of the watershed, then vectorize it.     
    g.run_command('r.water.outlet', input="KV_DraiDir@Watersheds_VK", output=rastoutput, coordinates=coordinates, overwrite=True)
    g.run_command('r.to.vect', input=rastoutput, output=vectoutput, type='area', flags='s', overwrite=True)
#Make a mask of the rastermap
    g.run_command('r.mapcalc', MASK=Maskstring, overwrite=True)
    # run stats over the masked landuse map
    g.run_command('r.stats', input=statsinput, output=statsoutput, flags='a', overwrite=True)
    #remove the mask
    g.run_command('r.mask', flags='r')

# python uitproberen
print 'hoi'
print "at least it's all working now. or well.. all"
